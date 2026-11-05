"""Draw a non-colliding global path on the Gazebo floor without blocking control."""

import math
import time
import xml.etree.ElementTree as ET

import rclpy
from nav_msgs.msg import Path
from rclpy.node import Node
from ros_gz_interfaces.srv import DeleteEntity, SpawnEntity


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
        self.busy, self.generation, self.deadline = False, 0, 0.0
        self.spawn = node.create_client(SpawnEntity, "/world/dwa_world/create")
        self.delete = node.create_client(DeleteEntity, "/world/dwa_world/remove")
        node.create_subscription(Path, "/astar_path", self.path, 10)
        node.create_timer(0.5, self.tick)

    def path(self, message):
        if message.header.frame_id != "odom":
            return
        points = tuple((pose.pose.position.x, pose.pose.position.y) for pose in message.poses)
        if all(math.isfinite(value) for point in points for value in point):
            self.latest = points

    def tick(self):
        if self.busy:
            if time.monotonic() > self.deadline:
                self.generation += 1
                self.busy = False
                self.node.get_logger().warning("Gazebo path service timed out.", throttle_duration_sec=5.0)
            return
        if self.latest is None or self.latest == self.drawn:
            return
        if not self.spawn.service_is_ready() or not self.delete.service_is_ready():
            self.node.get_logger().warning("Waiting for Gazebo create/remove bridge.", throttle_duration_sec=5.0)
            return
        self.pending = self.latest
        self.busy, self.deadline = True, time.monotonic() + 10.0
        self.generation += 1
        generation = self.generation
        request = DeleteEntity.Request()
        request.entity.name, request.entity.type = "python_global_path", request.entity.MODEL
        future = self.delete.call_async(request)

        def deleted(result):
            if generation != self.generation:
                return
            try:
                result.result()
                if len(self.pending) < 2:
                    self.drawn, self.busy = self.pending, False
                    return
                create = SpawnEntity.Request()
                create.entity_factory.name = "python_global_path"
                create.entity_factory.sdf = path_sdf(self.pending)
                create.entity_factory.pose.orientation.w = 1.0
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
                self.node.get_logger().info(f"Gazebo global path visible: {len(self.drawn)} points")
            except Exception as error:
                failed(error)

        def failed(error):
            self.busy = False
            self.node.get_logger().warning(f"Gazebo path drawing failed: {error}", throttle_duration_sec=5.0)

        future.add_done_callback(deleted)


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