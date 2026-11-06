import math
import subprocess

import rclpy
from geometry_msgs.msg import PoseStamped, Twist
from nav_msgs.msg import Odometry, Path
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool

from .astar import Grid, astar
from .dwa import choose_velocity


class AStarDwaNode(Node):
    def __init__(self):
        super().__init__("astar_dwa_planner")
        self.declare_parameter("goal_x", 7.0)
        self.declare_parameter("goal_y", 5.0)
        self.declare_parameter("map_size", 12.0)
        self.declare_parameter("resolution", 0.2)
        self.declare_parameter("robot_radius", 0.28)
        self.goal = (float(self.get_parameter("goal_x").value),
                     float(self.get_parameter("goal_y").value))
        self.pose, self.scan, self.path = None, None, []
        self.goal_received = False
        self.sim_active = False
        self.cmd_pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.path_pub = self.create_publisher(Path, "/astar_path", 10)
        self.sim_active_pub = self.create_publisher(Bool, "/sim_active", 10)
        self.create_subscription(Odometry, "/odom", self.odom_callback, 10)
        self.create_subscription(LaserScan, "/scan", self.scan_callback, 10)
        self.create_subscription(PoseStamped, "/goal_pose", self.goal_callback, 10)
        self.create_timer(0.25, self.plan_and_control)
        self.get_logger().info("A* -> DWA planner started")

    def odom_callback(self, message):
        q = message.pose.pose.orientation
        yaw = math.atan2(2 * (q.w * q.z + q.x * q.y),
                         1 - 2 * (q.y * q.y + q.z * q.z))
        self.pose = (message.pose.pose.position.x, message.pose.pose.position.y, yaw)

    def scan_callback(self, message):
        self.scan = message

    def goal_callback(self, message):
        self.goal = (message.pose.position.x, message.pose.position.y)
        self.goal_received = True
        self.path = []
        self._publish_sim_active(False)

    def _publish_sim_active(self, value):
        message = Bool()
        message.data = value
        self.sim_active_pub.publish(message)

    def spawn_path_visual(self, path_points, waypoints, world_name="dwa_world"):
        visuals = []
        for index, (x, y) in enumerate(path_points[::2]):
            visuals.append(
                f'<visual name="path_{index}"><pose>{x:.3f} {y:.3f} 0.02 0 0 0</pose>'
                '<geometry><sphere><radius>0.025</radius></sphere></geometry>'
                '<material><diffuse>0 0.8 1 1</diffuse></material></visual>'
            )
        for index, (x, y) in enumerate(waypoints):
            visuals.append(
                f'<visual name="waypoint_{index}"><pose>{x:.3f} {y:.3f} 0.05 0 0 0</pose>'
                '<geometry><sphere><radius>0.06</radius></sphere></geometry>'
                '<material><diffuse>0 1 0 1</diffuse></material></visual>'
            )
        sdf_xml = (
            '<sdf version="1.8"><model name="debug_path"><static>true</static>'
            '<link name="link">' + ''.join(visuals) + '</link></model></sdf>'
        )
        subprocess.run(
            ["gz", "service", "-s", f"/world/{world_name}/remove",
             "--reqtype", "gz.msgs.Entity", "--reptype", "gz.msgs.Boolean",
             "--timeout", "1000", "--req", 'name: "debug_path"'],
            check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.Popen(
            ["ros2", "run", "ros_gz_sim", "create", "-world", world_name,
             "-string", sdf_xml, "-name", "debug_path"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def obstacles(self):
        result = []
        for index, distance in enumerate(self.scan.ranges):
            if math.isfinite(distance) and self.scan.range_min <= distance <= self.scan.range_max:
                angle = self.pose[2] + self.scan.angle_min + index * self.scan.angle_increment
                result.append((self.pose[0] + distance * math.cos(angle),
                               self.pose[1] + distance * math.sin(angle), 0.08))
        return result

    def build_plan(self):
        size = float(self.get_parameter("map_size").value)
        resolution = float(self.get_parameter("resolution").value)
        origin = self.pose[0] - size / 2, self.pose[1] - size / 2
        width = max(3, math.ceil(size / resolution))
        grid = Grid(width, width, resolution, origin[0], origin[1])
        radius = float(self.get_parameter("robot_radius").value)
        for x, y, _ in self.obstacles():
            grid.add_obstacle(x, y, radius)
        path = astar(grid, grid.world_to_grid(self.pose[0], self.pose[1]),
                     grid.world_to_grid(*self.goal), diagonal=True)
        return [grid.grid_to_world(*cell) for cell in path]

    def publish_path(self):
        message = Path()
        message.header.frame_id = "odom"
        message.header.stamp = self.get_clock().now().to_msg()
        for x, y in self.path:
            pose = PoseStamped()
            pose.header = message.header
            pose.pose.position.x, pose.pose.position.y = x, y
            pose.pose.orientation.w = 1.0
            message.poses.append(pose)
        self.path_pub.publish(message)

    def plan_and_control(self):
        if self.pose is None or self.scan is None:
            self.cmd_pub.publish(Twist())
            self._publish_sim_active(False)
            return
        if not self.goal_received:
            self.cmd_pub.publish(Twist())
            self._publish_sim_active(False)
            return

        if not self.path:
            self.path = self.build_plan()
            if not self.path:
                self.cmd_pub.publish(Twist())
                self._publish_sim_active(False)
                return
            self.spawn_path_visual(self.path, self.path[::2])
            self._publish_sim_active(True)

        self.publish_path()
        if math.hypot(self.goal[0] - self.pose[0], self.goal[1] - self.pose[1]) < 0.3:
            self.cmd_pub.publish(Twist())
            return
        waypoint = self.goal
        for point in self.path:
            if math.hypot(point[0] - self.pose[0], point[1] - self.pose[1]) > 0.5:
                waypoint = point
                break
        velocity, angular_velocity = choose_velocity(
            self.pose, waypoint, self.obstacles(),
            float(self.get_parameter("robot_radius").value))
        command = Twist()
        command.linear.x, command.angular.z = velocity, angular_velocity
        self.cmd_pub.publish(command)


def main(args=None):
    rclpy.init(args=args)
    node = AStarDwaNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
