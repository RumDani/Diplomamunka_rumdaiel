from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, OpaqueFunction, SetEnvironmentVariable
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def start_reference(context):
    from dwa_gazebo_sim.python_world import write_world

    world_path = write_world()
    return [
        ExecuteProcess(cmd=["gz", "sim", "-v", LaunchConfiguration("verbose"), world_path], output="screen"),
        Node(
            package="ros_gz_bridge", executable="parameter_bridge", output="screen",
            arguments=[
                "/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist",
                "/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry",
                "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
                "/world/dwa_world/set_pose@ros_gz_interfaces/srv/SetEntityPose",
                "/world/dwa_world/control@ros_gz_interfaces/srv/ControlWorld",
            ],
            remappings=[("/odom", "/gazebo/odom")],
            parameters=[{"use_sim_time": True}],
        ),
        Node(
            package="dwa_gazebo_sim", executable="python_planner_node", output="screen",
            parameters=[{"use_sim_time": True, "external_control_ticks": True,
                         "obstacle_source": "tracked",
                         "autostart": LaunchConfiguration("autostart").perform(context).lower() == "true"}],
        ),
        Node(package="dwa_gazebo_sim", executable="python_simulation_node", output="screen",
             parameters=[{"use_sim_time": True}]),
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
