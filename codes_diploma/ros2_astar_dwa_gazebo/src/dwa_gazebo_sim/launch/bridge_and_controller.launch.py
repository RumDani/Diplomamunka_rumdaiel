from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
import os


def generate_launch_description():
    controller_share = get_package_share_directory("astar_dwa_controller")
    return LaunchDescription([
        Node(
            package="ros_gz_bridge",
            executable="parameter_bridge",
            arguments=[
                "/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist",
                "/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry",
                "/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan",
                "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
                "/world/dwa_world/set_pose@ros_gz_interfaces/srv/SetEntityPose",
            ],
            parameters=[{"use_sim_time": True}],
        ),
        Node(
            package="astar_dwa_controller",
            executable="astar_dwa_node",
            parameters=[
                os.path.join(controller_share, "config", "rosbot.yaml"),
                {"use_sim_time": True},
            ],
        ),
        Node(
            package="dwa_gazebo_sim",
            executable="moving_obstacle_node",
            parameters=[{"use_sim_time": True}],
        ),
    ])
