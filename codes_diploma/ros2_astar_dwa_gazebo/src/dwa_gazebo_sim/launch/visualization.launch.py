from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo, SetEnvironmentVariable
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    rviz_config = os.path.join(
        get_package_share_directory("astar_dwa_controller"),
        "rviz",
        "astar_dwa.rviz",
    )
    return LaunchDescription([
        DeclareLaunchArgument("software_rendering", default_value="true",
                              description="Use software OpenGL for WSL map shader compatibility"),
        SetEnvironmentVariable("ROS_AUTOMATIC_DISCOVERY_RANGE", "LOCALHOST"),
        SetEnvironmentVariable("QT_QPA_PLATFORM", "xcb"),
        SetEnvironmentVariable("QT_X11_NO_MITSHM", "1"),
        SetEnvironmentVariable("LIBGL_ALWAYS_SOFTWARE", "1",
                       condition=IfCondition(LaunchConfiguration("software_rendering"))),
        SetEnvironmentVariable("QT_OPENGL", "software",
                       condition=IfCondition(LaunchConfiguration("software_rendering"))),
        LogInfo(msg=["DIAG_RVIZ software_rendering=", LaunchConfiguration("software_rendering"),
                 " fixed_frame=map config=", rviz_config]),
        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            output="screen",
            arguments=["-d", rviz_config, "-f", "map"],
            parameters=[{"use_sim_time": True}],
        )
    ])
