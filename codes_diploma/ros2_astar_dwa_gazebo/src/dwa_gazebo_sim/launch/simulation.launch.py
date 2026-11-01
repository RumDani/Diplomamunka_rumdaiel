from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    package_share = get_package_share_directory("dwa_gazebo_sim")
    turtlebot_share = get_package_share_directory("turtlebot3_gazebo")
    model_path = os.path.join(turtlebot_share, "models")
    world_path = os.path.join(package_share, "worlds", "dwa_world.sdf")
    gui = LaunchConfiguration("gui")
    verbose = LaunchConfiguration("verbose")
    qt_platform = LaunchConfiguration("qt_platform")
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("ros_gz_sim"),
                         "launch", "gz_sim.launch.py")
        ),
        launch_arguments={
            # gz_sim.launch.py tokenizes this argument string; quote the path
            # because the workspace may be located under a Windows user name
            # containing spaces.
            "gz_args": ['"' + world_path + '" -r -v ', verbose, ' ', gui],
        }.items(),
    )
    bridge = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(package_share, "launch", "bridge_and_controller.launch.py")
        ),
        launch_arguments={}.items(),
    )
    return LaunchDescription([
        DeclareLaunchArgument(
            "gui",
            default_value="-g",
            description="Gazebo mod: -g GUI-val, -s szerver modban",
        ),
        DeclareLaunchArgument(
            "verbose",
            default_value="1",
            description="Gazebo naplózási szintje (0-4)",
        ),
        DeclareLaunchArgument(
            "qt_platform",
            default_value="xcb",
            description="Qt platform: xcb WSLg/X11-hez, wayland alternatívaként",
        ),
        SetEnvironmentVariable("GZ_SIM_RESOURCE_PATH", model_path),
        SetEnvironmentVariable("QT_QPA_PLATFORM", qt_platform),
        SetEnvironmentVariable("QT_X11_NO_MITSHM", "1"),
        SetEnvironmentVariable("ROS_AUTOMATIC_DISCOVERY_RANGE", "LOCALHOST"),
        gazebo,
        bridge,
    ])
