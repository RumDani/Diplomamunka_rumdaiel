import math

import rclpy
from geometry_msgs.msg import PoseStamped, Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


def yaw_from_quaternion(q):
    return math.atan2(
        2.0 * (q.w * q.z + q.x * q.y),
        1.0 - 2.0 * (q.y * q.y + q.z * q.z),
    )


class DwaNode(Node):
    def __init__(self):
        super().__init__("dwa_node")
        self.declare_parameter("goal_x", 7.0)
        self.declare_parameter("goal_y", 5.0)
        self.declare_parameter("goal_tolerance", 0.25)
        self.declare_parameter("simulation_time", 1.5)
        self.declare_parameter("robot_radius", 0.28)

        self.cmd_pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.create_subscription(Odometry, "/odom", self.odom_callback, 10)
        self.create_subscription(LaserScan, "/scan", self.scan_callback, 10)
        self.create_subscription(PoseStamped, "/goal_pose", self.goal_callback, 10)
        self.create_timer(0.1, self.control_callback)

        self.x = self.y = self.yaw = 0.0
        self.goal_x = float(self.get_parameter("goal_x").value)
        self.goal_y = float(self.get_parameter("goal_y").value)
        self.obstacles = []
        self.have_odom = False
        self.have_scan = False
        self.get_logger().info(
            f"DWA elindult, cel: ({self.goal_x:.2f}, {self.goal_y:.2f})"
        )

    def odom_callback(self, msg):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        self.yaw = yaw_from_quaternion(msg.pose.pose.orientation)
        self.have_odom = True

    def goal_callback(self, msg):
        self.goal_x = msg.pose.position.x
        self.goal_y = msg.pose.position.y
        self.get_logger().info(f"Uj cel: ({self.goal_x:.2f}, {self.goal_y:.2f})")

    def scan_callback(self, msg):
        self.obstacles = []
        for index, distance in enumerate(msg.ranges):
            if math.isfinite(distance) and msg.range_min <= distance <= msg.range_max:
                angle = msg.angle_min + index * msg.angle_increment
                self.obstacles.append(
                    (self.x + distance * math.cos(self.yaw + angle),
                     self.y + distance * math.sin(self.yaw + angle))
                )
        self.have_scan = True

    def rollout(self, velocity, angular_velocity, horizon):
        x, y, yaw = self.x, self.y, self.yaw
        step = 0.1
        for _ in range(max(1, int(horizon / step))):
            x += velocity * math.cos(yaw) * step
            y += velocity * math.sin(yaw) * step
            yaw += angular_velocity * step
            if any(
                math.hypot(x - ox, y - oy)
                < float(self.get_parameter("robot_radius").value)
                for ox, oy in self.obstacles
            ):
                return None
        return x, y, yaw

    def control_callback(self):
        if not self.have_odom or not self.have_scan:
            return
        distance = math.hypot(self.goal_x - self.x, self.goal_y - self.y)
        if distance <= float(self.get_parameter("goal_tolerance").value):
            self.cmd_pub.publish(Twist())
            return

        horizon = float(self.get_parameter("simulation_time").value)
        best = None
        for velocity in (0.0, 0.1, 0.2, 0.3, 0.4):
            for angular_velocity in (
                -1.0, -0.75, -0.5, -0.25, 0.0, 0.25, 0.5, 0.75, 1.0
            ):
                end = self.rollout(velocity, angular_velocity, horizon)
                if end is None:
                    continue
                end_x, end_y, end_yaw = end
                goal_heading = math.atan2(self.goal_y - end_y, self.goal_x - end_x)
                heading_error = abs(
                    math.atan2(math.sin(goal_heading - end_yaw),
                               math.cos(goal_heading - end_yaw))
                )
                score = (
                    -math.hypot(self.goal_x - end_x, self.goal_y - end_y)
                    - 0.2 * heading_error
                    + 0.1 * velocity
                )
                if best is None or score > best[0]:
                    best = score, velocity, angular_velocity

        command = Twist()
        if best is not None:
            command.linear.x = best[1]
            command.angular.z = best[2]
        self.cmd_pub.publish(command)


def main(args=None):
    rclpy.init(args=args)
    node = DwaNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
