import math
import os
import xml.etree.ElementTree as ET

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, EmitEvent, ExecuteProcess, LogInfo, OpaqueFunction, RegisterEventHandler, SetEnvironmentVariable, SetLaunchConfiguration
from launch.conditions import IfCondition
from launch.events import matches_action
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import LifecycleNode, Node
from launch_ros.descriptions import ParameterFile
from launch_ros.event_handlers import OnStateTransition
from launch_ros.events.lifecycle import ChangeState
from lifecycle_msgs.msg import Transition


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
    enable_crossing = LaunchConfiguration("enable_crossing_obstacle").perform(context).lower() == "true"
    enable_camera = LaunchConfiguration("enable_camera").perform(context).lower() == "true"
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
    map_resolution = float(LaunchConfiguration("map_resolution").perform(context))
    if not math.isfinite(map_resolution) or map_resolution <= 0:
        raise RuntimeError("Map resolution must be finite and positive")
    slam_executable = "localization_slam_toolbox_node" if slam_mode == "localization" else "async_slam_toolbox_node"
    scan_motion_threshold = 0.1
    slam_config = os.path.join(package_share, "config", "slam.yaml")
    if start_environment and not os.path.isfile(slam_config):
        raise RuntimeError(
            f"Installed SLAM config is missing: {slam_config}. "
            "From the ROS workspace run: colcon build --symlink-install "
            "--packages-select astar_dwa_controller dwa_gazebo_sim; "
            "then source install/setup.bash and verify ros2 pkg prefix dwa_gazebo_sim. "
            "Do not recreate the saved map: the missing file is package configuration.")
    slam_node = LifecycleNode(
        package="slam_toolbox", executable=slam_executable, name="slam_toolbox", namespace="",
        output="screen", condition=IfCondition(LaunchConfiguration("start_environment")),
        parameters=[ParameterFile(slam_config, allow_substs=True),
                    {"use_sim_time": True, "mode": slam_mode, "map_file_name": map_file,
                     "map_start_pose": initial_pose, "resolution": map_resolution,
                     "odom_frame": "odom", "map_frame": "map", "base_frame": "base_link",
                     "scan_topic": "/scan", "max_laser_range": 3.0,
                     "minimum_travel_distance": scan_motion_threshold,
                     "minimum_travel_heading": scan_motion_threshold,
                     "check_min_dist_and_heading_precisely": True,
                     "use_lifecycle_manager": False}],
    )
    runtime_world = write_world_with_pose_odometry(
        world_path, os.path.join(model_root, "turtlebot3_waffle", "model.sdf"),
        enable_crossing_obstacle=enable_crossing, enable_camera=enable_camera) if start_environment else world_path
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
                "/world/dwa_world/set_pose@ros_gz_interfaces/srv/SetEntityPose",
            ],
            remappings=[("/odom", "/gazebo/wheel_odom"),
                        ("/world_pose_odom", "/gazebo/ground_truth_odom")],
            parameters=[{"use_sim_time": True}],
        ),
        Node(
            package="dwa_gazebo_sim", executable="python_simulation_node", output="screen",
            condition=IfCondition(LaunchConfiguration("start_environment")),
            parameters=[{"use_sim_time": True, "world_file": world_path,
                         "enable_crossing_obstacle": enable_crossing,
                         "oncoming_start_x": float(LaunchConfiguration("oncoming_start_x").perform(context)),
                         "laser_pose": laser_pose[:3], "base_link_z": base_pose[2],
                         "odom_child_frame": drive.findtext("child_frame_id", "base_footprint")}],
        ),
        LogInfo(msg=f"DIAG_SLAM_CONFIG executable={slam_executable} mode={slam_mode} "
                    f"map_file={map_file!r} initial_pose={initial_pose} "
                    f"resolution={map_resolution} scan_motion_threshold={scan_motion_threshold} params_file={slam_config}",
                condition=IfCondition(LaunchConfiguration("start_environment"))),
        slam_node,
        RegisterEventHandler(
            OnStateTransition(target_lifecycle_node=slam_node, start_state="configuring",
                              goal_state="inactive", entities=[EmitEvent(event=ChangeState(
                                  lifecycle_node_matcher=matches_action(slam_node),
                                  transition_id=Transition.TRANSITION_ACTIVATE))]),
            condition=IfCondition(LaunchConfiguration("start_environment")),
        ),
        EmitEvent(event=ChangeState(lifecycle_node_matcher=matches_action(slam_node),
                                   transition_id=Transition.TRANSITION_CONFIGURE),
                  condition=IfCondition(LaunchConfiguration("start_environment"))),
        Node(
            package="astar_dwa_controller", executable="astar_dwa_node",
            output="screen",
            condition=IfCondition(LaunchConfiguration("start_planner")),
            parameters=[{"use_sim_time": True, "r_kerek": wheel_radius, "b": wheel_base,
                         "rob_radius": robot_radius, "map_inflation_radius": robot_radius + 0.03,
                         "static_safety_margin": 0.03, "w_kerek_max": 0.26 / wheel_radius,
                         "dynamic_clearance_weight": float(LaunchConfiguration("dynamic_clearance_weight").perform(context)),
                         "dynamic_clearance_distance": float(LaunchConfiguration("dynamic_clearance_distance").perform(context)),
                         "w_kerek_resolution": float(LaunchConfiguration("wheel_resolution").perform(context)),
                         "a_max": float(drive.findtext("max_linear_acceleration", "1.0"))}],
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
        DeclareLaunchArgument("dynamic_clearance_weight", default_value="4.0",
                  description="DWA weight for predicted moving-obstacle clearance"),
        DeclareLaunchArgument("dynamic_clearance_distance", default_value="0.6",
              description="Soft predicted clearance target beyond the unchanged safety margin, in metres"),
        DeclareLaunchArgument("wheel_resolution", default_value="0.5",
              description="DWA wheel angular speed sampling interval in rad/s"),
        DeclareLaunchArgument("start_environment", default_value="true",
                      description="Set false to start only the planner against an already running SLAM simulation"),
        DeclareLaunchArgument("enable_crossing_obstacle", default_value="false", choices=["true", "false"],
                      description="Include the crossing obstacle; false keeps only the oncoming obstacle"),
        DeclareLaunchArgument("enable_camera", default_value="false", choices=["true", "false"],
                      description="Enable unused camera rendering in the runtime TurtleBot model"),
        DeclareLaunchArgument("oncoming_start_x", default_value="2.4",
                      description="Start the oncoming obstacle after the robot reaches this odom x in metres"),
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
