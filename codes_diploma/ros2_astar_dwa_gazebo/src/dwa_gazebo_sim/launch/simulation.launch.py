from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription, SetEnvironmentVariable
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    package_share = get_package_share_directory("dwa_gazebo_sim")
    turtlebot_share = get_package_share_directory("turtlebot3_gazebo")
    model_path = os.path.join(turtlebot_share, "models")
    package_model_path = os.path.join(package_share, "models")
    resource_path = os.pathsep.join([model_path, package_model_path])
    world_path = os.path.join(package_share, "worlds", "dwa_world.sdf")
    verbose = LaunchConfiguration("verbose")
    software_rendering = LaunchConfiguration("software_rendering")
    gazebo = ExecuteProcess(
        cmd=["gz", "sim", "-v", verbose, "-r", world_path],
        output="screen",
    )
    bridge = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(package_share, "launch", "bridge_and_controller.launch.py")
        ),
        launch_arguments={}.items(),
    )
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
        SetEnvironmentVariable("GZ_SIM_RESOURCE_PATH", resource_path),
        SetEnvironmentVariable(
            "LIBGL_ALWAYS_SOFTWARE", "1", condition=IfCondition(software_rendering)),
        SetEnvironmentVariable("ROS_AUTOMATIC_DISCOVERY_RANGE", "LOCALHOST"),
        gazebo,
        bridge,
    ])
