from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    package_share = get_package_share_directory("astar_dwa_controller")
    return LaunchDescription([
        Node(
            package="astar_dwa_controller",
            executable="astar_dwa_node",
            name="astar_dwa_node",
            output="screen",
            parameters=[
                os.path.join(package_share, "config", "rosbot.yaml"),
                {"use_sim_time": True},
            ],
        )
    ])
