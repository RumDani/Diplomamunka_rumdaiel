"""Continuous Gazebo odometry and obstacle adapter; no physics stepping."""

import copy

import rclpy
from geometry_msgs.msg import TransformStamped
from nav_msgs.msg import Odometry
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile
from ros_gz_interfaces.srv import SetEntityPose
from sensor_msgs.msg import PointCloud2, PointField
from sensor_msgs_py import point_cloud2
from std_msgs.msg import Bool, Header
from tf2_ros import StaticTransformBroadcaster, TransformBroadcaster

from .python_reference import create_gazebo_scene


class GazeboSimulationAdapter:
    def __init__(self, node):
        self.node = node
        self.odometry_is_world = node.declare_parameter("odometry_is_world", False).value
        self.wheel_pose = None
        if not node.has_parameter("world_file"):
            node.declare_parameter("world_file", "")
        world_file = node.get_parameter("world_file").value
        _, self.start, _, _, _, self.obstacles = create_gazebo_scene(world_file)
        self.active = self.busy = False
        self.applied = copy.deepcopy(self.obstacles)
        self.last_time = node.get_clock().now().nanoseconds * 1e-9
        self.odom_pub = node.create_publisher(Odometry, "/odom", 10)
        self.obstacle_pub = node.create_publisher(PointCloud2, "/tracked_obstacles", 10)
        latched = QoSProfile(depth=1, durability=DurabilityPolicy.TRANSIENT_LOCAL)
        node.create_subscription(Bool, "/controller_active", self.set_active, latched)
        node.create_subscription(Odometry, "/gazebo/odom", self.odom, 10)
        node.create_subscription(Odometry, "/gazebo/wheel_odom", self.wheel_odom, 10)
        self.tf = TransformBroadcaster(node)
        self.static_tf = StaticTransformBroadcaster(node)
        self.odom_child = node.declare_parameter("odom_child_frame", "base_footprint").value
        base_z = float(node.declare_parameter("base_link_z", 0.01).value)
        laser_pose = node.declare_parameter("laser_pose", [-0.064, 0.0, 0.121]).value
        base = TransformStamped()
        base.header.frame_id, base.child_frame_id = self.odom_child, "base_link"
        base.transform.translation.z, base.transform.rotation.w = base_z, 1.0
        laser = TransformStamped()
        laser.header.frame_id, laser.child_frame_id = "base_link", "base_scan"
        laser.transform.translation.x, laser.transform.translation.y, laser.transform.translation.z = laser_pose
        laser.transform.rotation.w = 1.0
        self.static_tf.sendTransform([laser] if self.odom_child == "base_link" else [base, laser])
        self.pose_client = node.create_client(SetEntityPose, "/world/dwa_world/set_pose")
        node.create_timer(0.10, self.tick)
        node.get_logger().info(
            f"python-turtlebot-continuous: odometry={'Gazebo-world' if self.odometry_is_world else 'wheel-local'}; "
            "embedded adapter; physical cmd_vel control")

    def set_active(self, message):
        self.active = message.data

    def wheel_odom(self, message):
        self.wheel_pose = (message.pose.pose.position.x + self.start[0],
                           message.pose.pose.position.y + self.start[1],
                           message.header.stamp.sec + message.header.stamp.nanosec * 1e-9)

    def odom(self, message):
        mapped = copy.deepcopy(message)
        mapped.header.frame_id = "odom"
        mapped.child_frame_id = message.child_frame_id or self.odom_child
        if not self.odometry_is_world:
            mapped.pose.pose.position.x += self.start[0]
            mapped.pose.pose.position.y += self.start[1]
        stamp = message.header.stamp.sec + message.header.stamp.nanosec * 1e-9
        if (self.odometry_is_world and self.wheel_pose is not None and
            abs(stamp - self.wheel_pose[2]) <= 0.2):
            error = ((mapped.pose.pose.position.x - self.wheel_pose[0]) ** 2 +
                     (mapped.pose.pose.position.y - self.wheel_pose[1]) ** 2) ** 0.5
            if error > 0.15:
                self.node.get_logger().warning(
                    f"Wheel/world odometry mismatch: {error:.3f} m; using Gazebo world pose.",
                    throttle_duration_sec=2.0)
        self.odom_pub.publish(mapped)
        transform = TransformStamped()
        transform.header, transform.child_frame_id = mapped.header, mapped.child_frame_id
        transform.transform.translation.x = mapped.pose.pose.position.x
        transform.transform.translation.y = mapped.pose.pose.position.y
        transform.transform.translation.z = mapped.pose.pose.position.z
        transform.transform.rotation = mapped.pose.pose.orientation
        self.tf.sendTransform(transform)

    def tick(self):
        now = self.node.get_clock().now().nanoseconds * 1e-9
        dt, self.last_time = max(0.0, now - self.last_time), now
        if self.active:
            for obstacle in self.obstacles:
                obstacle.move(dt)
        if not self.busy and self.pose_client.service_is_ready():
            self.busy = True
            self.move_obstacle(0, copy.deepcopy(self.obstacles))
        header = Header(stamp=self.node.get_clock().now().to_msg(), frame_id="odom")
        fields = [PointField(name=name, offset=4 * index, datatype=PointField.FLOAT32, count=1)
                  for index, name in enumerate(("x", "y", "z", "radius", "vx", "vy"))]
        self.obstacle_pub.publish(point_cloud2.create_cloud(header, fields, [
            (obstacle.x, obstacle.y, 0.0, obstacle.radius,
             obstacle.vx if self.active else 0.0, obstacle.vy if self.active else 0.0)
            for obstacle in self.applied
        ]))

    def move_obstacle(self, index, snapshot):
        if index == len(snapshot):
            self.busy = False
            return
        obstacle = snapshot[index]
        request = SetEntityPose.Request()
        request.entity.name, request.entity.type = f"moving_obstacle_{index + 1}", request.entity.MODEL
        request.pose.position.x, request.pose.position.y = obstacle.x, obstacle.y
        request.pose.position.z, request.pose.orientation.w = 0.45, 1.0
        future = self.pose_client.call_async(request)

        def complete(result):
            try:
                if not result.result().success:
                    raise RuntimeError("Gazebo rejected an obstacle pose")
            except Exception as error:
                self.busy = False
                self.node.get_logger().error(f"Obstacle service failed: {error}", throttle_duration_sec=2.0)
                return
            self.applied[index] = obstacle
            self.move_obstacle(index + 1, snapshot)

        future.add_done_callback(complete)


class PythonSimulationNode(Node):
    def __init__(self):
        super().__init__("python_simulation")
        self.adapter = GazeboSimulationAdapter(self)


def main(args=None):
    rclpy.init(args=args)
    node = PythonSimulationNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()