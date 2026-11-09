"""Draw a non-colliding global path on the Gazebo floor without blocking control."""

import math
import time
import xml.etree.ElementTree as ET
from collections import deque

import rclpy
from nav_msgs.msg import Odometry, Path
from rclpy.node import Node
from rclpy.time import Time
from ros_gz_interfaces.srv import DeleteEntity, SetEntityPose, SpawnEntity
from tf2_ros import Buffer, TransformException, TransformListener


def project_path_points(points, source_to_odom, odom_pose, world_pose):
    """Align display coordinates only; never correct the navigation state."""
    offset_x, offset_y, source_yaw = source_to_odom
    correction_yaw = world_pose[2] - odom_pose[2]
    source_cos, source_sin = math.cos(source_yaw), math.sin(source_yaw)
    world_cos, world_sin = math.cos(correction_yaw), math.sin(correction_yaw)
    projected = []
    for point_x, point_y in points:
        delta_x = offset_x + source_cos * point_x - source_sin * point_y - odom_pose[0]
        delta_y = offset_y + source_sin * point_x + source_cos * point_y - odom_pose[1]
        projected.append((world_pose[0] + world_cos * delta_x - world_sin * delta_y,
                          world_pose[1] + world_sin * delta_x + world_cos * delta_y))
    return tuple(projected)


def pose_2d(pose):
    rotation = pose.orientation
    yaw = math.atan2(2 * (rotation.w * rotation.z + rotation.x * rotation.y),
                     1 - 2 * (rotation.y ** 2 + rotation.z ** 2))
    return pose.position.x, pose.position.y, yaw


def path_sdf(points):
    sdf = ET.Element("sdf", version="1.8")
    model = ET.SubElement(sdf, "model", name="python_global_path")
    ET.SubElement(model, "static").text = "true"
    link = ET.SubElement(model, "link", name="path")
    for index, (start, end) in enumerate(zip(points, points[1:])):
        dx, dy = end[0] - start[0], end[1] - start[1]
        length = math.hypot(dx, dy)
        if length < 1e-6:
            continue
        visual = ET.SubElement(link, "visual", name=f"segment_{index}")
        ET.SubElement(visual, "pose").text = (
            f"{(start[0] + end[0]) / 2} {(start[1] + end[1]) / 2} 0.015 0 0 {math.atan2(dy, dx)}")
        ET.SubElement(visual, "cast_shadows").text = "false"
        geometry = ET.SubElement(visual, "geometry")
        ET.SubElement(ET.SubElement(geometry, "box"), "size").text = f"{length} 0.04 0.01"
        material = ET.SubElement(visual, "material")
        ET.SubElement(material, "ambient").text = "0.1 0.9 0.2 1"
        ET.SubElement(material, "diffuse").text = "0.1 0.9 0.2 1"
    return ET.tostring(sdf, encoding="unicode")


class GazeboPathDisplay:
    def __init__(self, node):
        self.node = node
        self.latest = self.drawn = self.pending = None
        self.drawn_source = self.pending_source = None
        self.model_pose = self.pending_model_pose = None
        self.fixed_alignment = None
        self.alignment_frame = None
        self.path_frame = None
        self.odometry = deque(maxlen=200)
        self.ground_truth = None
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, node)
        self.busy, self.generation, self.deadline = False, 0, 0.0
        self.spawn = node.create_client(SpawnEntity, "/world/dwa_world/create")
        self.delete = node.create_client(DeleteEntity, "/world/dwa_world/remove")
        self.move = node.create_client(SetEntityPose, "/world/dwa_world/set_pose")
        node.create_subscription(Path, "/astar_path", self.path, 10)
        node.create_subscription(Odometry, "/odom", self.record_odometry, 10)
        node.create_subscription(Odometry, "/gazebo/ground_truth_odom", self.record_ground_truth, 10)
        node.create_timer(0.5, self.tick)

    def record_odometry(self, message):
        self.odometry.append(message)

    def record_ground_truth(self, message):
        self.ground_truth = message

    def path(self, message):
        points = tuple((pose.pose.position.x, pose.pose.position.y) for pose in message.poses)
        if all(math.isfinite(value) for point in points for value in point):
            self.latest = points
            self.path_frame = message.header.frame_id

    def world_points(self):
        if not self.latest:
            return self.latest
        if self.fixed_alignment is not None and self.alignment_frame == self.path_frame:
            self.model_pose = self.fixed_alignment
            offset_x, offset_y, yaw = self.fixed_alignment
            cosine, sine = math.cos(yaw), math.sin(yaw)
            return tuple((offset_x + cosine * point_x - sine * point_y,
                          offset_y + sine * point_x + cosine * point_y)
                         for point_x, point_y in self.latest)
        if self.ground_truth is None or not self.odometry or not self.path_frame:
            self.node.get_logger().warning(
                "DIAG_PATH reason=waiting_alignment", throttle_duration_sec=5.0)
            return None
        truth = self.ground_truth
        truth_time = Time.from_msg(truth.header.stamp).nanoseconds
        odom = min(self.odometry, key=lambda message: abs(
            Time.from_msg(message.header.stamp).nanoseconds - truth_time))
        odom_time = Time.from_msg(odom.header.stamp).nanoseconds
        if abs(odom_time - truth_time) > 50000000 or odom.child_frame_id != truth.child_frame_id:
            self.node.get_logger().warning(
                f"DIAG_PATH reason=alignment_mismatch odom_child={odom.child_frame_id} "
                f"world_child={truth.child_frame_id}", throttle_duration_sec=5.0)
            return None
        age = self.node.get_clock().now().nanoseconds - truth_time
        if age < 0 or age > 500000000:
            self.node.get_logger().warning("DIAG_PATH reason=stale_alignment", throttle_duration_sec=5.0)
            return None
        if self.path_frame == odom.header.frame_id:
            source_to_odom = (0.0, 0.0, 0.0)
        else:
            try:
                transform = self.tf_buffer.lookup_transform(
                    odom.header.frame_id, self.path_frame, Time.from_msg(odom.header.stamp)).transform
            except TransformException as error:
                self.node.get_logger().warning(
                    f"DIAG_PATH reason=tf_missing frame={self.path_frame} error={error}",
                    throttle_duration_sec=5.0)
                return None
            rotation = transform.rotation
            yaw = math.atan2(2 * (rotation.w * rotation.z + rotation.x * rotation.y),
                             1 - 2 * (rotation.y ** 2 + rotation.z ** 2))
            source_to_odom = (transform.translation.x, transform.translation.y, yaw)
        projected = project_path_points(self.latest, source_to_odom,
                                        pose_2d(odom.pose.pose), pose_2d(truth.pose.pose))
        if not all(math.isfinite(value) for point in projected for value in point):
            self.node.get_logger().warning("DIAG_PATH reason=nonfinite_projection", throttle_duration_sec=5.0)
            return None
        anchors = project_path_points(((0.0, 0.0), (1.0, 0.0)), source_to_odom,
                                      pose_2d(odom.pose.pose), pose_2d(truth.pose.pose))
        self.model_pose = (anchors[0][0], anchors[0][1],
                           math.atan2(anchors[1][1] - anchors[0][1],
                                      anchors[1][0] - anchors[0][0]))
        self.fixed_alignment = self.model_pose
        self.alignment_frame = self.path_frame
        self.node.get_logger().info(
            f"DIAG_PATH reason=alignment_locked frame={self.path_frame} "
            f"world_transform={self.fixed_alignment} navigation_feedback=false")
        return projected

    def tick(self):
        if self.busy:
            if time.monotonic() > self.deadline:
                self.generation += 1
                self.busy = False
                self.node.get_logger().warning("Gazebo path service timed out.", throttle_duration_sec=5.0)
            return
        projected = self.world_points()
        if projected is None:
            return
        if not projected and not self.drawn:
            return
        if self.drawn is not None and len(projected) == len(self.drawn) and all(
                math.hypot(current[0] - previous[0], current[1] - previous[1]) < 0.02
                for current, previous in zip(projected, self.drawn)):
            return
        if not all(client.service_is_ready() for client in (self.spawn, self.delete, self.move)):
            self.node.get_logger().warning("Waiting for Gazebo path services.", throttle_duration_sec=5.0)
            return
        self.pending = projected
        self.pending_source = (self.path_frame, self.latest)
        self.pending_model_pose = self.model_pose
        self.busy, self.deadline = True, time.monotonic() + 10.0
        self.generation += 1
        generation = self.generation
        def place_pose(pose):
            pose.position.x, pose.position.y, yaw = self.pending_model_pose
            pose.orientation.z, pose.orientation.w = math.sin(yaw / 2), math.cos(yaw / 2)

        def failed(error):
            self.busy = False
            self.node.get_logger().warning(f"Gazebo path drawing failed: {error}", throttle_duration_sec=5.0)

        if self.drawn and self.drawn_source == self.pending_source:
            request = SetEntityPose.Request()
            request.entity.name, request.entity.type = "python_global_path", request.entity.MODEL
            place_pose(request.pose)

            def moved(result):
                if generation != self.generation:
                    return
                try:
                    if not result.result().success:
                        raise RuntimeError("Gazebo rejected path pose update")
                    self.drawn, self.busy = self.pending, False
                except Exception as error:
                    failed(error)

            self.move.call_async(request).add_done_callback(moved)
            return

        def deleted(result):
            if generation != self.generation:
                return
            try:
                if result is not None:
                    result.result()
                if len(self.pending) < 2:
                    self.drawn, self.busy = self.pending, False
                    return
                create = SpawnEntity.Request()
                create.entity_factory.name = "python_global_path"
                create.entity_factory.sdf = path_sdf(self.pending_source[1])
                place_pose(create.entity_factory.pose)
                self.spawn.call_async(create).add_done_callback(created)
            except Exception as error:
                failed(error)

        def created(result):
            if generation != self.generation:
                return
            try:
                if not result.result().success:
                    raise RuntimeError("Gazebo rejected the path model")
                self.drawn, self.busy = self.pending, False
                self.drawn_source = self.pending_source
                self.node.get_logger().info(
                    f"DIAG_PATH reason=drawn source_frame={self.path_frame} "
                    f"points={len(self.drawn)} first={self.drawn[0]} last={self.drawn[-1]} "
                    "ground_truth_usage=visualization_only")
            except Exception as error:
                failed(error)

        if not self.drawn:
            deleted(None)
        else:
            request = DeleteEntity.Request()
            request.entity.name, request.entity.type = "python_global_path", request.entity.MODEL
            self.delete.call_async(request).add_done_callback(deleted)


class GazeboPathNode(Node):
    def __init__(self):
        super().__init__("gazebo_global_path")
        self.display = GazeboPathDisplay(self)


def main(args=None):
    rclpy.init(args=args)
    node = GazeboPathNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()