import math

import rclpy
from geometry_msgs.msg import PoseStamped, Twist
from nav_msgs.msg import Odometry, Path
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

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
        self.cmd_pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.path_pub = self.create_publisher(Path, "/astar_path", 10)
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
        self.path = []

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
            return
        self.path = self.build_plan()
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
