import math
import os
import xml.etree.ElementTree as ET

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, OpaqueFunction, SetEnvironmentVariable
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def start_simulation(context):
    package_share = get_package_share_directory("dwa_gazebo_sim")
    controller_share = get_package_share_directory("astar_dwa_controller")
    model_root = os.path.join(get_package_share_directory("turtlebot3_gazebo"), "models")
    model_file = os.path.join(model_root, "turtlebot3_waffle", "model.sdf")
    world_file = os.path.join(package_share, "worlds", "dwa_world.sdf")
    model = ET.parse(model_file).getroot()
    drive = model.find(".//plugin[@name='gz::sim::systems::DiffDrive']")
    laser = model.find(".//sensor[@type='gpu_lidar']")
    collision = model.find(".//link[@name='base_link']/collision")
    if drive is None or laser is None or collision is None:
        raise RuntimeError("Installed TurtleBot Waffle model is missing DiffDrive, LiDAR or body geometry")
    from dwa_gazebo_sim.gazebo_odometry_world import add_world_pose_odometry
    runtime_world = add_world_pose_odometry(world_file, model_file)
    body_pose = [float(value) for value in collision.findtext("pose", "0 0 0 0 0 0").split()]
    body_size = [float(value) for value in collision.findtext("geometry/box/size").split()]
    robot_radius = math.hypot(abs(body_pose[0]) + body_size[0] / 2,
                              abs(body_pose[1]) + body_size[1] / 2)
    laser_pose = [float(value) for value in laser.findtext("pose", "0 0 0 0 0 0").split()]
    return [
        SetEnvironmentVariable("GZ_SIM_RESOURCE_PATH", os.pathsep.join(
            [model_root, os.environ.get("GZ_SIM_RESOURCE_PATH", "")])),
        ExecuteProcess(cmd=["gz", "sim", "-r", "-v", LaunchConfiguration("verbose"), runtime_world],
                       output="screen"),
        Node(
            package="ros_gz_bridge", executable="parameter_bridge", output="screen",
            arguments=[
                "/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist",
                "/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry",
                "/world_pose_odom@nav_msgs/msg/Odometry[gz.msgs.Odometry",
                "/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan",
                "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
                "/world/dwa_world/set_pose@ros_gz_interfaces/srv/SetEntityPose",
            ],
            remappings=[("/odom", "/gazebo/wheel_odom"),
                        ("/world_pose_odom", "/odom")],
            parameters=[{"use_sim_time": True}],
        ),
        Node(
            package="astar_dwa_controller", executable="astar_dwa_node", name="astar_dwa_node",
            output="screen",
            parameters=[
                os.path.join(controller_share, "config", "rosbot.yaml"),
                {"use_sim_time": True,
                 "initial_pose_x": 0.0, "initial_pose_y": 0.0,
                 "robot_radius": robot_radius,
                 "wheel_radius": float(drive.findtext("wheel_radius")),
                 "wheel_base": float(drive.findtext("wheel_separation")) / 2.0,
                 "scan_offset_x": laser_pose[0],
                 "scan_offset_y": laser_pose[1],
                 "scan_offset_z": laser_pose[2],
                 "acceleration_limit": float(drive.findtext("max_linear_acceleration", "1.0")),
                 "max_linear_velocity": 0.22,
                 "gazebo_world": "dwa_world"},
            ],
        ),
        Node(package="dwa_gazebo_sim", executable="moving_obstacle_node", output="screen",
             parameters=[{"use_sim_time": True}]),
    ]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument("verbose", default_value="4"),
        DeclareLaunchArgument("software_rendering", default_value="true"),
        SetEnvironmentVariable("LIBGL_ALWAYS_SOFTWARE", "1",
                               condition=IfCondition(LaunchConfiguration("software_rendering"))),
        SetEnvironmentVariable("ROS_AUTOMATIC_DISCOVERY_RANGE", "LOCALHOST"),
        OpaqueFunction(function=start_simulation),
    ])