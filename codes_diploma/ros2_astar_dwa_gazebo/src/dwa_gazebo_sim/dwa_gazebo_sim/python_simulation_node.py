"""Gazebo-only obstacle and stepping node; never used on the real robot."""

import copy
import time

import rclpy
from geometry_msgs.msg import TransformStamped
from nav_msgs.msg import Odometry
from rclpy.clock import Clock, ClockType
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile
from ros_gz_interfaces.srv import ControlWorld, SetEntityPose
from sensor_msgs.msg import PointCloud2, PointField
from sensor_msgs_py import point_cloud2
from std_msgs.msg import Bool, Header
from tf2_ros import TransformBroadcaster

from codes_diploma.robot import robotconfig
from .python_reference import PHYSICS_STEP, create_scene


class PythonSimulationNode(Node):
    def __init__(self):
        super().__init__("python_simulation")
        _, self.start, _, _, _, self.obstacles = create_scene()
        self.dt = robotconfig().dt
        self.active = self.busy = self.failed = self.ready_step = self.have_odom = False
        self.step_until = None
        self.expected_tick = None
        self.odom_stamp, self.bootstrap_steps = 0.0, 0
        self.deadline = 0.0
        self.odom_pub = self.create_publisher(Odometry, "/odom", 10)
        self.obstacle_pub = self.create_publisher(PointCloud2, "/tracked_obstacles", 10)
        self.tick_pub = self.create_publisher(Header, "/control_tick", 10)
        latched = QoSProfile(depth=1, durability=DurabilityPolicy.TRANSIENT_LOCAL)
        self.create_subscription(Bool, "/controller_active", self.set_active, latched)
        self.create_subscription(Header, "/control_done", self.control_done, 10)
        self.create_subscription(Odometry, "/gazebo/odom", self.odom, 10)
        self.tf = TransformBroadcaster(self)
        self.pose_client = self.create_client(SetEntityPose, "/world/dwa_world/set_pose")
        self.control_client = self.create_client(ControlWorld, "/world/dwa_world/control")
        self.wall_clock = Clock(clock_type=ClockType.STEADY_TIME)
        self.create_timer(0.02, self.tick, clock=self.wall_clock)
        self.get_logger().info("python-reference-lockstep: Gazebo paused between Python control steps")

    def fail(self, reason):
        self.failed = True
        self.get_logger().error(reason)

    def set_active(self, message):
        self.active = message.data

    def odom(self, message):
        mapped = copy.deepcopy(message)
        mapped.header.frame_id, mapped.child_frame_id = "odom", "base_link"
        mapped.pose.pose.position.x += self.start[0]
        mapped.pose.pose.position.y += self.start[1]
        self.odom_stamp = message.header.stamp.sec + message.header.stamp.nanosec * 1e-9
        self.have_odom = True
        self.odom_pub.publish(mapped)
        transform = TransformStamped()
        transform.header, transform.child_frame_id = mapped.header, "base_link"
        transform.transform.translation.x = mapped.pose.pose.position.x
        transform.transform.translation.y = mapped.pose.pose.position.y
        transform.transform.translation.z = mapped.pose.pose.position.z
        transform.transform.rotation = mapped.pose.pose.orientation
        self.tf.sendTransform(transform)

    def control_done(self, message):
        if self.expected_tick is None or message.stamp != self.expected_tick.stamp:
            return
        self.expected_tick = None
        self.busy = False
        self.ready_step = True

    def tick(self):
        if self.failed:
            return
        if self.busy:
            if time.monotonic() > self.deadline:
                self.fail("No service/planner response for 120 s; simulation remains paused.")
            return
        if not self.control_client.service_is_ready() or not self.pose_client.service_is_ready():
            return
        if self.step_until is not None:
            if self.get_clock().now().nanoseconds * 1e-9 + 1.5 * PHYSICS_STEP < self.step_until:
                return
            if self.have_odom and self.odom_stamp < self.step_until - 0.011:
                return
            self.step_until = None
        if self.ready_step:
            self.ready_step = False
            self.request_step()
            return
        if not self.have_odom:
            if self.bootstrap_steps >= 10:
                self.fail("No Gazebo odometry; check the bridge and differential-drive plugin.")
                return
            self.bootstrap_steps += 1
            self.ready_step = True
            return
        if not self.active:
            return
        for obstacle in self.obstacles:
            obstacle.move(self.dt)
        self.busy, self.deadline = True, time.monotonic() + 120.0
        self.move_obstacle(0)

    def move_obstacle(self, index):
        if index == len(self.obstacles):
            header = Header(stamp=self.get_clock().now().to_msg(), frame_id="odom")
            fields = [PointField(name=name, offset=4 * offset, datatype=PointField.FLOAT32, count=1)
                      for offset, name in enumerate(("x", "y", "z", "radius", "vx", "vy"))]
            cloud = point_cloud2.create_cloud(header, fields, [
                (obstacle.x, obstacle.y, 0.0, obstacle.radius, obstacle.vx, obstacle.vy)
                for obstacle in self.obstacles
            ])
            self.obstacle_pub.publish(cloud)
            self.expected_tick = header
            self.tick_pub.publish(header)
            return
        obstacle = self.obstacles[index]
        request = SetEntityPose.Request()
        request.entity.name, request.entity.type = f"moving_obstacle_{index + 1}", request.entity.MODEL
        request.pose.position.x, request.pose.position.y = obstacle.x, obstacle.y
        request.pose.position.z, request.pose.orientation.w = 0.45, 1.0
        future = self.pose_client.call_async(request)

        def complete(result):
            try:
                if not result.result().success:
                    self.fail("Gazebo rejected an obstacle pose.")
                    return
            except Exception as error:
                self.fail(f"Obstacle service failed: {error}")
                return
            self.move_obstacle(index + 1)

        future.add_done_callback(complete)

    def request_step(self):
        request = ControlWorld.Request()
        request.world_control.pause = True
        request.world_control.multi_step = round(self.dt / PHYSICS_STEP)
        self.step_until = self.get_clock().now().nanoseconds * 1e-9 + self.dt
        self.busy, self.deadline = True, time.monotonic() + 120.0
        future = self.control_client.call_async(request)

        def complete(result):
            self.busy = False
            try:
                if not result.result().success:
                    self.fail("Gazebo rejected a simulation step.")
            except Exception as error:
                self.fail(f"World control service failed: {error}")

        future.add_done_callback(complete)


def main(args=None):
    rclpy.init(args=args)
    node = PythonSimulationNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()