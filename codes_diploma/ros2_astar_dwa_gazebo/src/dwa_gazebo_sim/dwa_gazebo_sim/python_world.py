"""Generate Gazebo geometry from the ROS copy of the unchanged Python scene."""

import math
import tempfile
import xml.etree.ElementTree as ET

from codes_diploma.robot import robotconfig
from .python_reference import PHYSICS_STEP, create_scene


def element(parent, tag, value=None, **attributes):
    child = ET.SubElement(parent, tag, attributes)
    if value is not None:
        child.text = str(value)
    return child


def inertial(link, mass, inertia):
    node = element(link, "inertial")
    element(node, "mass", mass)
    tensor = element(node, "inertia")
    for axis in ("ixx", "iyy", "izz"):
        element(tensor, axis, inertia)
    for axis in ("ixy", "ixz", "iyz"):
        element(tensor, axis, 0)


def cylinder(link, radius, length, color, pose="0 0 0 0 0 0"):
    for name in ("collision", "visual"):
        item = element(link, name, name=name)
        element(item, "pose", pose)
        geometry = element(item, "geometry")
        shape = element(geometry, "cylinder")
        element(shape, "radius", radius)
        element(shape, "length", length)
        if name == "visual":
            material = element(item, "material")
            element(material, "ambient", color)
            element(material, "diffuse", color)


def write_world():
    grid, start, _, _, statics, dynamic = create_scene()
    config = robotconfig()
    sdf = ET.Element("sdf", version="1.8")
    world = element(sdf, "world", name="dwa_world")
    physics = element(world, "physics", name="python_steps", type="ignored")
    element(physics, "max_step_size", PHYSICS_STEP)
    element(physics, "real_time_factor", 1)
    for library, system in (("physics", "Physics"), ("scene-broadcaster", "SceneBroadcaster"),
                            ("user-commands", "UserCommands")):
        element(world, "plugin", filename=f"gz-sim-{library}-system", name=f"gz::sim::systems::{system}")
    light = element(world, "light", name="sun", type="directional")
    element(light, "pose", "0 0 10 0 0 0")
    element(light, "direction", "-0.5 0.1 -0.9")
    ground = element(world, "model", name="ground_plane")
    element(ground, "static", "true")
    link = element(ground, "link", name="link")
    for kind in ("collision", "visual"):
        item = element(link, kind, name=kind)
        geometry = element(item, "geometry")
        plane = element(geometry, "plane")
        element(plane, "normal", "0 0 1")
        element(plane, "size", f"{grid.width * grid.resolution} {grid.height * grid.resolution}")
        if kind == "visual":
            element(item, "pose", f"{grid.width * grid.resolution / 2} {grid.height * grid.resolution / 2} 0 0 0 0")
            material = element(item, "material")
            element(material, "ambient", "0.7 0.75 0.75 1")
            element(material, "diffuse", "0.7 0.75 0.75 1")
    for index, obstacle in enumerate(statics + dynamic):
        moving = index >= len(statics)
        name = f"moving_obstacle_{index - len(statics) + 1}" if moving else f"static_obstacle_{index}"
        model = element(world, "model", name=name)
        element(model, "static", "false" if moving else "true")
        element(model, "pose", f"{obstacle.x} {obstacle.y} 0.45 0 0 0")
        link = element(model, "link", name="link")
        element(link, "gravity", "false")
        inertial(link, 10, 0.1)
        color = "0.1 0.4 0.9 1" if moving else ("0.9 0.7 0.1 1" if obstacle.x > 4 else "0.8 0.15 0.2 1")
        cylinder(link, obstacle.radius, 0.9, color)
    robot = element(world, "model", name="python_robot")
    element(robot, "pose", f"{start[0]} {start[1]} {config.r_kerek} 0 0 0")
    body = element(robot, "link", name="base_link")
    inertial(body, 1, 0.005)
    cylinder(body, config.rob_radius, 0.05, "0.1 0.6 0.6 1", "0 0 0.025 0 0 0")
    for side, sign in (("left", 1), ("right", -1)):
        wheel = element(robot, "link", name=f"{side}_wheel")
        element(wheel, "pose", f"0 {sign * config.b} 0 0 0 0")
        inertial(wheel, 0.05, 0.00003)
        cylinder(wheel, config.r_kerek, 0.02, "0.1 0.1 0.1 1", f"0 0 0 {math.pi / 2} 0 0")
        joint = element(robot, "joint", name=f"{side}_wheel_joint", type="revolute")
        element(joint, "parent", "base_link")
        element(joint, "child", f"{side}_wheel")
        axis = element(joint, "axis")
        element(axis, "xyz", "0 1 0")
    for name, direction in (("front", 1), ("rear", -1)):
        caster = element(robot, "link", name=f"{name}_caster")
        element(caster, "pose", f"{direction * 0.075} 0 -0.023 0 0 0")
        inertial(caster, 0.01, 0.000001)
        collision = element(caster, "collision", name="collision")
        sphere = element(element(collision, "geometry"), "sphere")
        element(sphere, "radius", 0.01)
        friction = element(element(element(collision, "surface"), "friction"), "ode")
        element(friction, "mu", 0.01)
        element(friction, "mu2", 0.01)
        joint = element(robot, "joint", name=f"{name}_caster_joint", type="fixed")
        element(joint, "parent", "base_link")
        element(joint, "child", f"{name}_caster")
    drive = element(robot, "plugin", filename="gz-sim-diff-drive-system", name="gz::sim::systems::DiffDrive")
    for key, value in {
        "left_joint": "left_wheel_joint", "right_joint": "right_wheel_joint",
        "wheel_separation": 2 * config.b, "wheel_radius": config.r_kerek,
        "topic": "/cmd_vel", "odom_topic": "/odom", "tf_topic": "/gazebo/tf",
        "frame_id": "odom", "child_frame_id": "base_link", "odom_publish_frequency": 100,
        "max_linear_acceleration": config.a_max,
        "max_angular_acceleration": config.a_max / config.b,
    }.items():
        element(drive, key, value)
    with tempfile.NamedTemporaryFile(suffix=".sdf", prefix="python_reference_", delete=False) as handle:
        ET.ElementTree(sdf).write(handle, encoding="utf-8", xml_declaration=True)
        return handle.name