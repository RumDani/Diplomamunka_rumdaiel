"""Create a runtime copy of the TurtleBot world with world-pose odometry."""

import copy
import tempfile
import xml.etree.ElementTree as ET


def add_world_pose_odometry(world_file, model_file):
    world_tree = ET.parse(world_file)
    world = world_tree.getroot().find("world")
    model_root = ET.parse(model_file).getroot().find("model")
    include = None if world is None else world.find("include")
    if world is None or include is None or model_root is None:
        raise ValueError("Expected a world with an included TurtleBot model")

    robot = copy.deepcopy(model_root)
    robot.set("name", include.findtext("name", "turtlebot3_waffle"))
    pose = robot.find("pose")
    if pose is None:
        pose = ET.SubElement(robot, "pose")
    pose.text = include.findtext("pose", "0 0 0 0 0 0")
    if robot.find("plugin[@name='gz::sim::systems::DiffDrive']") is None:
        raise ValueError("TurtleBot model is missing the DiffDrive plugin")

    odometry = ET.SubElement(
        robot, "plugin", filename="gz-sim-odometry-publisher-system",
        name="gz::sim::systems::OdometryPublisher",
    )
    for key, value in {
        "odom_frame": "odom",
        "robot_base_frame": "base_link",
        "odom_topic": "/world_pose_odom",
        "tf_topic": "/gazebo/world_pose_tf",
        "dimensions": 2,
        "odom_publish_frequency": 50,
        "gaussian_noise": 0,
    }.items():
        ET.SubElement(odometry, key).text = str(value)

    world.remove(include)
    world.append(robot)
    with tempfile.NamedTemporaryFile(suffix=".sdf", prefix="turtlebot_world_pose_", delete=False) as handle:
        world_tree.write(handle, encoding="utf-8", xml_declaration=True)
        return handle.name