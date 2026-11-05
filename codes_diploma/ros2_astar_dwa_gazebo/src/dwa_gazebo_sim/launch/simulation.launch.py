import math
import os
import xml.etree.ElementTree as ET

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, OpaqueFunction, SetEnvironmentVariable
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def start_reference(context):
    package_share = get_package_share_directory("dwa_gazebo_sim")
    model_root = os.path.join(get_package_share_directory("turtlebot3_gazebo"), "models")
    world_path = os.path.join(package_share, "worlds", "dwa_world.sdf")
    model = ET.parse(os.path.join(model_root, "turtlebot3_waffle", "model.sdf")).getroot()
    drive = model.find(".//plugin[@name='gz::sim::systems::DiffDrive']")
    laser = model.find(".//sensor[@type='gpu_lidar']")
    collision = model.find(".//link[@name='base_link']/collision")
    if drive is None or laser is None or collision is None:
        raise RuntimeError("The installed TurtleBot Waffle model lacks drive, LiDAR or body geometry")
    wheel_radius = float(drive.findtext("wheel_radius"))
    wheel_base = float(drive.findtext("wheel_separation")) / 2
    body_pose = [float(value) for value in collision.findtext("pose", "0 0 0 0 0 0").split()]
    size = [float(value) for value in collision.findtext("geometry/box/size").split()]
    robot_radius = math.hypot(abs(body_pose[0]) + size[0] / 2, abs(body_pose[1]) + size[1] / 2)
    laser_pose = [float(value) for value in laser.findtext("pose", "0 0 0 0 0 0").split()]
    if any(abs(value) > 1e-6 for value in laser_pose[3:]):
        raise RuntimeError("The reference expects an unrotated TurtleBot LiDAR")
    base_pose = [float(value) for value in model.findtext(
        ".//joint[@name='base_joint']/pose", "0 0 0.01 0 0 0").split()]
    return [
        SetEnvironmentVariable("GZ_SIM_RESOURCE_PATH", os.pathsep.join(
            [model_root, os.environ.get("GZ_SIM_RESOURCE_PATH", "")])),
        ExecuteProcess(cmd=["gz", "sim", "-r", "-v", LaunchConfiguration("verbose"), world_path], output="screen"),
        Node(
            package="ros_gz_bridge", executable="parameter_bridge", output="screen",
            arguments=[
                "/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist",
                "/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry",
                "/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan",
                "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
                "/world/dwa_world/set_pose@ros_gz_interfaces/srv/SetEntityPose",
                "/world/dwa_world/create@ros_gz_interfaces/srv/SpawnEntity",
                "/world/dwa_world/remove@ros_gz_interfaces/srv/DeleteEntity",
            ],
            remappings=[("/odom", "/gazebo/odom")],
            parameters=[{"use_sim_time": True}],
        ),
        Node(
            package="dwa_gazebo_sim", executable="python_planner_node", output="screen",
            parameters=[{"use_sim_time": True, "external_control_ticks": False,
                         "gazebo_runtime": True,
                         "world_file": world_path, "r_kerek": wheel_radius, "b": wheel_base,
                         "rob_radius": robot_radius, "map_inflation_radius": robot_radius + 0.03,
                         "static_safety_margin": 0.03, "w_kerek_max": 0.26 / wheel_radius,
                         "a_max": float(drive.findtext("max_linear_acceleration", "1.0")),
                         "laser_pose": laser_pose[:3], "base_link_z": base_pose[2],
                         "odom_child_frame": drive.findtext("child_frame_id", "base_footprint"),
                         "obstacle_source": "tracked",
                         "autostart": LaunchConfiguration("autostart").perform(context).lower() == "true"}],
        ),
    ]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            "verbose",
            default_value="4",
            description="Gazebo naplózási szintje (0-4)",
        ),
        DeclareLaunchArgument(
            "software_rendering",
            default_value="true",
            description="Szoftveres Mesa renderelés bekapcsolása WSLg renderelési hibákhoz",
        ),
        DeclareLaunchArgument("autostart", default_value="false",
                              description="Start the Python default goal without an RViz goal"),
        SetEnvironmentVariable(
            "LIBGL_ALWAYS_SOFTWARE", "1", condition=IfCondition(LaunchConfiguration("software_rendering"))),
        SetEnvironmentVariable("ROS_AUTOMATIC_DISCOVERY_RANGE", "LOCALHOST"),
        OpaqueFunction(function=start_reference),
    ])
