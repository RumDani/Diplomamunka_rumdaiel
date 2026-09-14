from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Paraméterek
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    
    # Robot leírásának betöltése (URDF/XACRO fájl)
    # Ha nincs URDF-ed, ezt a részt ki kell egészíteni a robotod adataival
    robot_description_content = """
    <?xml version="1.0"?>
    <robot name="diff_drive_robot">
        <link name="base_footprint"/>
        
        <joint name="base_joint" type="fixed">
            <parent link="base_footprint"/>
            <child link="base_link"/>
            <origin xyz="0 0 0.1" rpy="0 0 0"/>
        </joint>
        
        <link name="base_link"/>
        
        <joint name="laser_joint" type="fixed">
            <parent link="base_link"/>
            <child link="base_scan"/>
            <origin xyz="0.1 0 0.15" rpy="0 0 0"/>
        </joint>
        
        <link name="base_scan"/>
    </robot>
    """
    
    # Ha van külső URDF fájlod, ezt használd:
    # urdf_file = os.path.join(get_package_share_directory('dwa_planner'), 'urdf', 'robot.urdf')
    # with open(urdf_file, 'r') as f:
    #     robot_description_content = f.read()
    
    # Robot State Publisher - A robot kinematikai modelljét publikálja
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{
            'use_sim_time': use_sim_time,
            'robot_description': robot_description_content
        }],
        output='screen'
    )
    
    # Bridge - Összeköti a Gazebot a ROS-szal
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='ros_gz_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V'
        ],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )
    
    # Static TF - A szenzor pozíciója (ha a robot_state_publisher már tartalmazza, ez nem kell)
    static_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_tf_publisher',
        arguments=['0', '0', '0.1', '0', '0', '0', 'base_footprint', 'base_scan'],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )
    
    # SLAM Toolbox - Térképezés (mapping mód)
    slam_toolbox = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        parameters=[{
            'use_sim_time': use_sim_time,
            'odom_frame': 'odom',
            'map_frame': 'map',
            'base_frame': 'base_footprint',
            'scan_topic': '/scan',
            'mode': 'mapping',  # 'mapping' vagy 'localization'
            
            # SLAM paraméterek
            'map_update_interval': 5.0,
            'resolution': 0.05,
            'max_laser_range': 12.0,
            'minimum_time_interval': 0.5,
            'transform_timeout': 0.2,
            'transform_publish_period': 0.05,
            'minimum_travel_distance': 0.2,
            'minimum_travel_heading': 0.5,
            'scan_buffer_maximum_scan_distance': 10.0,
            'scan_buffer_maximum_scan_time': 0.05,
            'link_match_minimum_response_frequency': 0.1,
            
            # Kerülő megoldások
            'loop_search_maximum_distance': 3.0,
            'do_loop_closing': True,
            'loop_match_minimum_chain_size': 10,
            'loop_match_maximum_variance_coarse': 3.0,
            'loop_match_minimum_response_fine': 0.1,
            
            # Korrelációs paraméterek
            'correlation_search_space_dimension': 0.5,
            'correlation_search_space_resolution': 0.01,
            'correlation_search_space_smear_deviation': 0.03,
            
            # Particle filter paraméterek (lokalizációhoz)
            'particles': 100,
            'update_rate': 1.0,
        }],
        output='screen'
    )
    
    # DWA Node - A te csomagod
    dwa_node = Node(
        package='dwa_planner',
        executable='dwa_node',
        name='dwa_node',
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )
    
    # RViz2 - Vizualizáció (opcionális)
    rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', os.path.join(get_package_share_directory('dwa_planner'), 'config', 'slam_config.rviz')],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen',
        condition=IfCondition(LaunchConfiguration('rviz', default='false'))
    )
    
    # Launch argumentek
    declare_rviz_arg = DeclareLaunchArgument(
        'rviz',
        default_value='false',
        description='Indítsa el az RViz2-t'
    )
    
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Használjon szimulációs időt'
    )
    
    return LaunchDescription([
        declare_use_sim_time,
        declare_rviz_arg,
        
        robot_state_publisher,
        bridge,
        static_tf,
        slam_toolbox,
        dwa_node,
        rviz2,
    ])

# Feltételes import a RViz feltételhez
from launch.conditions import IfCondition