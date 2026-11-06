import math
import os
import xml.etree.ElementTree as ET

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription, OpaqueFunction, SetEnvironmentVariable, SetLaunchConfiguration
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def start_reference(context):
    from dwa_gazebo_sim.python_world import write_world_with_pose_odometry

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
    start_environment = LaunchConfiguration("start_environment").perform(context).lower() == "true"
    slam_mode = LaunchConfiguration("slam_mode").perform(context)
    map_file = LaunchConfiguration("map_file").perform(context).strip()
    map_file = os.path.abspath(os.path.expanduser(map_file)) if map_file else ""
    if start_environment and slam_mode == "localization" and not map_file:
        raise RuntimeError("Localization requires map_file:=/absolute/path/prefix without an extension")
    if start_environment and map_file:
        for extension in (".posegraph", ".data"):
            if not os.path.isfile(map_file + extension):
                raise RuntimeError(f"Missing saved SLAM file: {map_file + extension}")
    initial_pose = [float(LaunchConfiguration(name).perform(context))
                    for name in ("initial_x", "initial_y", "initial_yaw")]
    if not all(math.isfinite(value) for value in initial_pose):
        raise RuntimeError("Initial map pose must contain finite values")
    slam_launch = "localization_launch.py" if slam_mode == "localization" else "online_async_launch.py"
    runtime_world = write_world_with_pose_odometry(
        world_path, os.path.join(model_root, "turtlebot3_waffle", "model.sdf")) if start_environment else world_path
    return [
        SetLaunchConfiguration("map_file", map_file),
        SetLaunchConfiguration("initial_x", str(initial_pose[0])),
        SetLaunchConfiguration("initial_y", str(initial_pose[1])),
        SetLaunchConfiguration("initial_yaw", str(initial_pose[2])),
        SetEnvironmentVariable("GZ_SIM_RESOURCE_PATH", os.pathsep.join(
            [model_root, os.environ.get("GZ_SIM_RESOURCE_PATH", "")])),
        ExecuteProcess(cmd=["gz", "sim", "-r", "-v", LaunchConfiguration("verbose"), runtime_world],
                   output="screen", condition=IfCondition(LaunchConfiguration("start_environment"))),
        Node(
            package="ros_gz_bridge", executable="parameter_bridge", output="screen",
            condition=IfCondition(LaunchConfiguration("start_environment")),
            arguments=[
                "/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist",
                "/model/moving_obstacle_1/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist",
                "/model/moving_obstacle_2/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist",
                "/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry",
                "/world_pose_odom@nav_msgs/msg/Odometry[gz.msgs.Odometry",
                "/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan",
                "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
                "/world/dwa_world/create@ros_gz_interfaces/srv/SpawnEntity",
                "/world/dwa_world/remove@ros_gz_interfaces/srv/DeleteEntity",
            ],
            remappings=[("/odom", "/gazebo/wheel_odom"),
                        ("/world_pose_odom", "/gazebo/ground_truth_odom")],
            parameters=[{"use_sim_time": True}],
        ),
        Node(
            package="dwa_gazebo_sim", executable="python_simulation_node", output="screen",
            condition=IfCondition(LaunchConfiguration("start_environment")),
            parameters=[{"use_sim_time": True, "world_file": world_path,
                         "laser_pose": laser_pose[:3], "base_link_z": base_pose[2],
                         "odom_child_frame": drive.findtext("child_frame_id", "base_footprint")}],
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(
                get_package_share_directory("slam_toolbox"), "launch", slam_launch)),
            launch_arguments={"use_sim_time": "true", "autostart": "true",
                              "use_lifecycle_manager": "false",
                              "slam_params_file": os.path.join(package_share, "config", "slam.yaml")}.items(),
            condition=IfCondition(LaunchConfiguration("start_environment")),
        ),
        Node(
            package="dwa_gazebo_sim", executable="python_planner_node", output="screen",
            condition=IfCondition(LaunchConfiguration("start_planner")),
            parameters=[{"use_sim_time": True, "external_control_ticks": False,
                         "map_source": "topic", "r_kerek": wheel_radius, "b": wheel_base,
                         "rob_radius": robot_radius, "map_inflation_radius": robot_radius + 0.03,
                         "static_safety_margin": 0.03, "w_kerek_max": 0.26 / wheel_radius,
                         "a_max": float(drive.findtext("max_linear_acceleration", "1.0")),
                         "obstacle_source": "tracked", "autostart": False}],
        ),
        Node(
            package="dwa_gazebo_sim", executable="lidar_obstacle_node", output="screen",
            condition=IfCondition(LaunchConfiguration("start_planner")),
            parameters=[{"use_sim_time": True, "tracking_frame": "odom"}],
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
        DeclareLaunchArgument("start_planner", default_value="true",
                      description="Set false for manual SLAM mapping without a cmd_vel controller"),
        DeclareLaunchArgument("start_environment", default_value="true",
                      description="Set false to start only the planner against an already running SLAM simulation"),
        DeclareLaunchArgument("map_resolution", default_value="0.10",
                      description="SLAM grid cell size in metres"),
        DeclareLaunchArgument("slam_mode", default_value="mapping", choices=["mapping", "localization"],
                      description="Build a map or localize against a saved pose graph"),
        DeclareLaunchArgument("map_file", default_value="",
                      description="Saved SLAM prefix without .posegraph or .data extension"),
        DeclareLaunchArgument("initial_x", default_value="0.8", description="Initial x estimate in map metres"),
        DeclareLaunchArgument("initial_y", default_value="0.8", description="Initial y estimate in map metres"),
        DeclareLaunchArgument("initial_yaw", default_value="0.0", description="Initial map yaw estimate in radians"),
        SetEnvironmentVariable(
            "LIBGL_ALWAYS_SOFTWARE", "1", condition=IfCondition(LaunchConfiguration("software_rendering"))),
        SetEnvironmentVariable("ROS_AUTOMATIC_DISCOVERY_RANGE", "LOCALHOST"),
        OpaqueFunction(function=start_reference),
    ])
