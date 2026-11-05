"""Convert LiDAR surface points and cluster velocity estimates into planner input."""

import math

import rclpy
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile, qos_profile_sensor_data
from rclpy.time import Time
from nav_msgs.msg import OccupancyGrid
from sensor_msgs.msg import LaserScan, PointCloud2, PointField
from sensor_msgs_py import point_cloud2
from std_msgs.msg import Header
from tf2_ros import Buffer, TransformException, TransformListener


class LidarObstacleNode(Node):
    def __init__(self):
        super().__init__("lidar_obstacles")
        self.tracking_frame = self.declare_parameter("tracking_frame", "odom").value
        self.max_range = float(self.declare_parameter("max_range", 3.0).value)
        self.previous, self.last_stamp, self.map = [], None, None
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.publisher = self.create_publisher(PointCloud2, "/tracked_obstacles", 10)
        self.create_subscription(LaserScan, "/scan", self.scan, qos_profile_sensor_data)
        latched = QoSProfile(depth=1, durability=DurabilityPolicy.TRANSIENT_LOCAL)
        self.create_subscription(OccupancyGrid, "/map", self.set_map, latched)

    def set_map(self, message):
        self.map = message

    @staticmethod
    def transform_point(transform, x, y):
        rotation = transform.rotation
        yaw = math.atan2(2 * (rotation.w * rotation.z + rotation.x * rotation.y),
                         1 - 2 * (rotation.y ** 2 + rotation.z ** 2))
        return (transform.translation.x + math.cos(yaw) * x - math.sin(yaw) * y,
                transform.translation.y + math.sin(yaw) * x + math.cos(yaw) * y)

    def scan(self, message):
        try:
            transform = self.tf_buffer.lookup_transform(
                self.tracking_frame, message.header.frame_id, Time.from_msg(message.header.stamp)
            ).transform
            map_transform = None if self.map is None else self.tf_buffer.lookup_transform(
                self.map.header.frame_id, self.tracking_frame, Time.from_msg(message.header.stamp)
            ).transform
        except TransformException:
            self.get_logger().warning("Waiting for LiDAR/localization TF.", throttle_duration_sec=2.0)
            return
        clusters, last_index = [], -2
        for index, value in enumerate(message.ranges):
            if not math.isfinite(value) or not message.range_min <= value <= min(message.range_max, self.max_range):
                continue
            angle = message.angle_min + index * message.angle_increment
            point = self.transform_point(transform, value * math.cos(angle), value * math.sin(angle))
            if (not clusters or index - last_index > 2 or
                    math.hypot(point[0] - clusters[-1][-1][0], point[1] - clusters[-1][-1][1]) > 0.15):
                clusters.append([])
            clusters[-1].append(point)
            last_index = index
        stamp = message.header.stamp.sec + message.header.stamp.nanosec * 1e-9
        dt = None if self.last_stamp is None else stamp - self.last_stamp
        tracks, points, used = [], [], set()
        for cluster in clusters:
            x = sum(point[0] for point in cluster) / len(cluster)
            y = sum(point[1] for point in cluster) / len(cluster)
            vx = vy = 0.0
            if dt is not None and 0.02 < dt < 0.5 and len(cluster) >= 2:
                matches = [(math.hypot(x - old[0] - old[2] * dt, y - old[1] - old[3] * dt), index)
                           for index, old in enumerate(self.previous) if index not in used]
                if matches:
                    error, index = min(matches)
                    if error < 0.35:
                        old = self.previous[index]
                        used.add(index)
                        vx, vy = 0.6 * old[2] + 0.4 * (x - old[0]) / dt, 0.6 * old[3] + 0.4 * (y - old[1]) / dt
                        if math.hypot(vx, vy) < 0.06:
                            vx = vy = 0.0
            known_wall = False
            if self.map is not None and map_transform is not None and self.map.info.resolution > 0:
                info = self.map.info
                for point in cluster:
                    map_x, map_y = self.transform_point(map_transform, *point)
                    column = math.floor((map_x - info.origin.position.x) / info.resolution)
                    row = math.floor((map_y - info.origin.position.y) / info.resolution)
                    if 0 <= row < info.height and 0 <= column < info.width:
                        if self.map.data[row * info.width + column] >= 65:
                            known_wall = True
                            break
            if known_wall:
                vx = vy = 0.0
            tracks.append((x, y, vx, vy))
            points.extend((point[0], point[1], 0.0, 0.0, vx, vy) for point in cluster)
        self.previous, self.last_stamp = tracks, stamp
        fields = [PointField(name=name, offset=4 * index, datatype=PointField.FLOAT32, count=1)
                  for index, name in enumerate(("x", "y", "z", "radius", "vx", "vy"))]
        self.publisher.publish(point_cloud2.create_cloud(
            Header(stamp=message.header.stamp, frame_id=self.tracking_frame), fields, points
        ))


def main(args=None):
    rclpy.init(args=args)
    node = LidarObstacleNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()