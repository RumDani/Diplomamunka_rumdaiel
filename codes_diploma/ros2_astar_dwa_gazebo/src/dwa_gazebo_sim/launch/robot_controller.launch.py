"""Hardware entry point: only the planner; robot bringup supplies odom, scan and TF."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def start_controller(context):
    filename = LaunchConfiguration("params_file").perform(context)
    if not filename:
        raise RuntimeError("Set params_file with the real robot radius, wheel geometry and dynamic limits.")
    parameters = [filename]
    parameters.append({"use_sim_time": False, "external_control_ticks": False,
                       "map_source": "topic",
                       "base_frame": LaunchConfiguration("base_frame").perform(context),
                       "obstacle_source": LaunchConfiguration("obstacle_source").perform(context)})
    nodes = [Node(package="dwa_gazebo_sim", executable="python_planner_node",
                  output="screen", parameters=parameters)]
    if (LaunchConfiguration("obstacle_source").perform(context) == "tracked" and
            LaunchConfiguration("start_tracker").perform(context).lower() == "true"):
        nodes.append(Node(package="dwa_gazebo_sim", executable="lidar_obstacle_node",
                          output="screen", parameters=[{"use_sim_time": False}]))
    map_yaml = LaunchConfiguration("map_yaml").perform(context)
    if map_yaml:
        nodes.extend([
            Node(package="nav2_map_server", executable="map_server", name="map_server",
                 output="screen", parameters=[{"yaml_filename": map_yaml, "use_sim_time": False}]),
            Node(package="nav2_amcl", executable="amcl", name="amcl", output="screen",
                 parameters=[{"use_sim_time": False, "global_frame_id": "map",
                              "odom_frame_id": "odom",
                              "base_frame_id": LaunchConfiguration("base_frame").perform(context),
                              "scan_topic": "/scan", "tf_broadcast": True}]),
            Node(package="nav2_lifecycle_manager", executable="lifecycle_manager",
                 name="localization_lifecycle", output="screen",
                 parameters=[{"use_sim_time": False, "autostart": True,
                              "node_names": ["map_server", "amcl"]}]),
        ])
    return nodes


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument("params_file", default_value=""),
        DeclareLaunchArgument("map_yaml", default_value=""),
        DeclareLaunchArgument("base_frame", default_value="base_link"),
        DeclareLaunchArgument("obstacle_source", default_value="tracked"),
        DeclareLaunchArgument("start_tracker", default_value="true"),
        OpaqueFunction(function=start_controller),
    ])