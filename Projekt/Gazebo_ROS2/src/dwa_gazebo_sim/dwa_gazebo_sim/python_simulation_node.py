"""Continuous Gazebo odometry and obstacle adapter; no physics stepping."""

import copy
import math
import time

import rclpy
from geometry_msgs.msg import TransformStamped, Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile, qos_profile_sensor_data
from rclpy.time import Time
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool
from tf2_ros import Buffer, StaticTransformBroadcaster, TransformBroadcaster, TransformListener

from .python_reference import create_gazebo_scene
from .gazebo_path_node import GazeboPathDisplay


class GazeboSimulationAdapter:
    def __init__(self, node):
        self.node = node
        self.ground_truth = None
        self.last_diagnostic_wall = -math.inf
        self.last_diagnostic_sim = None
        self.last_tf_diagnostic_wall = -math.inf
        self.last_odom_stamp = None
        self.last_odom_child = None
        self.tf_buffer = Buffer(node=node)
        self.tf_listener = TransformListener(self.tf_buffer, node)
        if not node.has_parameter("world_file"):
            node.declare_parameter("world_file", "")
        world_file = node.get_parameter("world_file").value
        _, self.start, _, _, _, self.obstacles = create_gazebo_scene(world_file)
        self.crossing_enabled = node.declare_parameter("enable_crossing_obstacle", False).value
        obstacle_specs = [(f"moving_obstacle_{index + 1}", obstacle)
                  for index, obstacle in enumerate(self.obstacles)
                  if self.crossing_enabled or index == 1]
        self.obstacles = [obstacle for _, obstacle in obstacle_specs]
        self.obstacle_names = [name for name, _ in obstacle_specs]
        self.oncoming_start_x = float(node.declare_parameter("oncoming_start_x", 0.0).value)
        if not math.isfinite(self.oncoming_start_x):
            raise ValueError("oncoming_start_x must be finite")
        self.crossing_start_x = float(node.declare_parameter("crossing_start_x", 0.8).value)
        if not math.isfinite(self.crossing_start_x):
            raise ValueError("crossing_start_x must be finite")
        self.robot_odom_x = None
        self.oncoming_started = False
        self.crossing_started = False
        self.active = False
        self.last_time = node.get_clock().now().nanoseconds * 1e-9
        self.odom_pub = node.create_publisher(Odometry, "/odom", 10)
        self.obstacle_commands = [node.create_publisher(
            Twist, f"/model/{name}/cmd_vel", 10) for name, _ in obstacle_specs]
        latched = QoSProfile(depth=1, durability=DurabilityPolicy.TRANSIENT_LOCAL)
        node.create_subscription(Bool, "/controller_active", self.set_active, latched)
        node.create_subscription(Odometry, "/gazebo/wheel_odom", self.odom, qos_profile_sensor_data)
        node.create_subscription(Odometry, "/gazebo/ground_truth_odom", self.record_ground_truth, qos_profile_sensor_data)
        node.create_subscription(LaserScan, "/scan", self.inspect_scan_tf, qos_profile_sensor_data)
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
        node.create_timer(0.10, self.tick)
        node.get_logger().info(
            "python-turtlebot-physical: odometry=wheel; obstacles=LiDAR; "
            "simulation-only adapter; velocity-driven obstacles; physical cmd_vel control")
        node.get_logger().info(
            f"DIAG_SCENARIO crossing_enabled={self.crossing_enabled} "
            f"moving_models={[name for name, _ in obstacle_specs]} "
            f"oncoming_start_x={self.oncoming_start_x} "
            f"crossing_start_x={self.crossing_start_x}")

    def set_active(self, message):
        self.active = message.data

    def record_ground_truth(self, message):
        self.ground_truth = message

    def inspect_scan_tf(self, message):
        wall_time = time.monotonic()
        if wall_time - self.last_tf_diagnostic_wall < 2.0:
            return
        self.last_tf_diagnostic_wall = wall_time
        stamp = Time.from_msg(message.header.stamp)
        scan_age = (self.node.get_clock().now().nanoseconds - stamp.nanoseconds) * 1e-9
        odom_delta = None if self.last_odom_stamp is None else (
            self.last_odom_stamp - stamp.nanoseconds) * 1e-9
        checks = []
        for target, source in (("base_link", message.header.frame_id),
                               ("odom", "base_link"), ("map", "odom")):
            ready, detail = self.tf_buffer.can_transform(
                target, source, stamp, return_debug_tuple=True)
            latest = self.tf_buffer.can_transform(target, source, Time())
            checks.append(f"{target}<-{source}:at_scan={ready},latest={latest},detail={detail}")
        self.node.get_logger().info(
            f"DIAG_TF scan_stamp={stamp.nanoseconds * 1e-9:.3f} scan_age={scan_age:.3f} "
            f"scan_frame={message.header.frame_id} odom_received={self.last_odom_stamp is not None} "
            f"wheel_publishers={self.node.count_publishers('/gazebo/wheel_odom')} "
            f"odom_minus_scan={odom_delta} configured_child={self.odom_child} "
            f"received_child={self.last_odom_child} checks={checks}")

    def odom(self, message):
        mapped = copy.deepcopy(message)
        mapped.header.frame_id = "odom"
        mapped.child_frame_id = message.child_frame_id or self.odom_child
        mapped.pose.pose.position.x += self.start[0]
        mapped.pose.pose.position.y += self.start[1]
        self.robot_odom_x = mapped.pose.pose.position.x
        self.odom_pub.publish(mapped)
        transform = TransformStamped()
        transform.header, transform.child_frame_id = mapped.header, mapped.child_frame_id
        transform.transform.translation.x = mapped.pose.pose.position.x
        transform.transform.translation.y = mapped.pose.pose.position.y
        transform.transform.translation.z = mapped.pose.pose.position.z
        transform.transform.rotation = mapped.pose.pose.orientation
        self.tf.sendTransform(transform)
        self.last_odom_stamp = Time.from_msg(mapped.header.stamp).nanoseconds
        self.last_odom_child = mapped.child_frame_id
        wall_time = time.monotonic()
        if wall_time - self.last_diagnostic_wall >= 2.0:
            stamp = message.header.stamp.sec + message.header.stamp.nanosec * 1e-9
            real_time_factor = None if self.last_diagnostic_sim is None else (
                (stamp - self.last_diagnostic_sim) / (wall_time - self.last_diagnostic_wall))
            self.last_diagnostic_wall = wall_time
            self.last_diagnostic_sim = stamp
            truth_position = None
            truth_delta = None
            error = None
            if self.ground_truth is not None:
                truth = self.ground_truth
                truth_stamp = truth.header.stamp.sec + truth.header.stamp.nanosec * 1e-9
                truth_delta = stamp - truth_stamp
                truth_position = (truth.pose.pose.position.x, truth.pose.pose.position.y)
                if abs(truth_delta) <= 0.2:
                    error = math.hypot(mapped.pose.pose.position.x - truth_position[0],
                                       mapped.pose.pose.position.y - truth_position[1])
            self.node.get_logger().info(
                f"DIAG_ODOM stamp={stamp:.3f} source=wheel "
                f"raw_xy=({message.pose.pose.position.x:.3f},{message.pose.pose.position.y:.3f}) "
                f"spawn_offset={self.start} "
                f"odom_xy=({mapped.pose.pose.position.x:.3f},{mapped.pose.pose.position.y:.3f}) "
                f"truth_xy={truth_position} truth_dt={truth_delta} xy_error={error} "
                f"real_time_factor={real_time_factor} "
                f"child={mapped.child_frame_id}")

    def tick(self):
        now = self.node.get_clock().now().nanoseconds * 1e-9
        dt, self.last_time = max(0.0, now - self.last_time), now
        if (self.active and not self.oncoming_started and self.robot_odom_x is not None and
                self.robot_odom_x >= self.oncoming_start_x):
            self.oncoming_started = True
            self.node.get_logger().info(
                f"DIAG_SCENARIO event=oncoming_started sim_t={now:.3f} "
                f"robot_odom_x={self.robot_odom_x:.3f} threshold={self.oncoming_start_x}")
        if (self.crossing_enabled and self.active and not self.crossing_started and
                self.robot_odom_x is not None and
                self.robot_odom_x >= self.crossing_start_x):
            self.crossing_started = True
            self.node.get_logger().info(
                f"DIAG_SCENARIO event=crossing_started sim_t={now:.3f} "
                f"robot_odom_x={self.robot_odom_x:.3f} threshold={self.crossing_start_x}")
        for name, obstacle, publisher in zip(self.obstacle_names, self.obstacles, self.obstacle_commands):
            moving = self.oncoming_started if name == "moving_obstacle_2" else self.crossing_started
            if moving:
                obstacle.move(dt)
            command = Twist()
            if moving:
                command.linear.x, command.linear.y = obstacle.vx, obstacle.vy
            publisher.publish(command)


class PythonSimulationNode(Node):
    def __init__(self):
        super().__init__("python_simulation")
        self.adapter = GazeboSimulationAdapter(self)
        self.path_display = GazeboPathDisplay(self)


def main(args=None):
    rclpy.init(args=args)
    node = PythonSimulationNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()