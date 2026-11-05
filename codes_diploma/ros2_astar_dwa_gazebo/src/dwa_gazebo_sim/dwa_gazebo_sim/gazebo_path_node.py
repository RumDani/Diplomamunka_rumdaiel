"""Draw a non-colliding global path on the Gazebo floor without blocking control."""

from concurrent.futures import ThreadPoolExecutor
import math
import os
import subprocess
import tempfile
import xml.etree.ElementTree as ET

import rclpy
from nav_msgs.msg import Path
from rclpy.node import Node


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


class GazeboPathNode(Node):
    def __init__(self):
        super().__init__("gazebo_global_path")
        self.latest = self.drawn = self.pending = self.future = None
        self.worker = ThreadPoolExecutor(max_workers=1)
        self.create_subscription(Path, "/astar_path", self.path, 10)
        self.create_timer(1.0, self.tick)

    def path(self, message):
        if message.header.frame_id != "odom":
            return
        points = tuple((pose.pose.position.x, pose.pose.position.y) for pose in message.poses)
        if all(math.isfinite(value) for point in points for value in point):
            self.latest = points

    def tick(self):
        if self.future is not None:
            if not self.future.done():
                return
            try:
                self.future.result()
                self.drawn = self.pending
            except Exception as error:
                self.get_logger().warning(f"Gazebo path drawing failed: {error}", throttle_duration_sec=5.0)
            self.future = None
        if self.latest is not None and self.latest != self.drawn:
            self.pending = self.latest
            self.future = self.worker.submit(self.draw, self.pending)

    @staticmethod
    def draw(points):
        subprocess.run([
            "gz", "service", "-s", "/world/dwa_world/remove", "--reqtype", "gz.msgs.Entity",
            "--reptype", "gz.msgs.Boolean", "--timeout", "2000",
            "--req", 'name: "python_global_path" type: MODEL',
        ], capture_output=True, timeout=4, check=False)
        if len(points) < 2:
            return
        filename = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".sdf", delete=False) as handle:
                filename = handle.name
                handle.write(path_sdf(points))
            result = subprocess.run([
                "gz", "service", "-s", "/world/dwa_world/create", "--reqtype", "gz.msgs.EntityFactory",
                "--reptype", "gz.msgs.Boolean", "--timeout", "3000",
                "--req", f'sdf_filename: "{filename}"',
            ], capture_output=True, text=True, timeout=5, check=True)
            if "data: true" not in result.stdout:
                raise RuntimeError(result.stderr or result.stdout or "No Gazebo creation response")
        finally:
            if filename is not None:
                os.unlink(filename)

    def destroy_node(self):
        self.worker.shutdown(wait=False, cancel_futures=True)
        return super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = GazeboPathNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()