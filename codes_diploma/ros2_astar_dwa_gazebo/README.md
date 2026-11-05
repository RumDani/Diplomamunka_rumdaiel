## Terminal 0: regi szimulacio leallitasa

```bash
source /opt/ros/jazzy/setup.bash
pkill -TERM -f 'ros2 launch dwa_gazebo_sim (simulation|visualization)\.launch\.py' 2>/dev/null || true
pkill -TERM -f '/(python_planner_node|python_simulation_node|lidar_obstacle_node|moving_obstacle_node|gazebo_path_node)( |$)' 2>/dev/null || true
pkill -TERM -x astar_dwa_node 2>/dev/null || true
pkill -TERM -x moving_obstacle 2>/dev/null || true
pkill -TERM -f '/parameter_bridge( |$)' 2>/dev/null || true
pkill -TERM -x rviz2 2>/dev/null || true
pkill -TERM -f 'gz sim|gz-sim-[0-9]+-(server|gui)' 2>/dev/null || true
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
ros2 daemon stop
ros2 daemon start
```

## Terminal 0: letoltes, fuggosegek, ujraforditas

```bash
source /opt/ros/jazzy/setup.bash
cd "/mnt/c/Users/Rum Dániel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo"
git pull --no-rebase origin master
rosdep install --from-paths src --ignore-src --rosdistro jazzy -r -y
colcon build --symlink-install --packages-select astar_dwa_controller dwa_gazebo_sim
source install/setup.bash
ros2 pkg executables dwa_gazebo_sim
```

## Terminal 1: TurtleBot es folyamatos Gazebo

```bash
source /opt/ros/jazzy/setup.bash
cd "/mnt/c/Users/Rum Dániel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo"
source install/setup.bash
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
export DISPLAY=:0
export TURTLEBOT3_MODEL=waffle
export XDG_RUNTIME_DIR=/tmp/gazebo-runtime
mkdir -p "$XDG_RUNTIME_DIR"
chmod 700 "$XDG_RUNTIME_DIR"
ros2 launch dwa_gazebo_sim simulation.launch.py software_rendering:=true autostart:=false
# A regi dwa_world.sdf es TurtleBot Waffle folyamatosan fut.
# Indulo jelzesek: python-original-planner es python-turtlebot-continuous.
# Egy sajat vezerlo node indul; a Gazebo-adapter es az utrajzolo azon belul fut.
# Celadas utan a zold globalis ut a Gazebo talajan is megjelenik.
```

## Terminal 2: RViz es celadas

```bash
source /opt/ros/jazzy/setup.bash
cd "/mnt/c/Users/Rum Dániel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo"
source install/setup.bash
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
export DISPLAY=:0
export QT_QPA_PLATFORM=xcb
export QT_X11_NO_MITSHM=1
export XDG_RUNTIME_DIR=/tmp/gazebo-runtime
mkdir -p "$XDG_RUNTIME_DIR"
chmod 700 "$XDG_RUNTIME_DIR"
ros2 launch dwa_gazebo_sim visualization.launch.py
# Fixed Frame: odom. Celadas: 2D Goal Pose.
# Regi palya: 8.2 x 5.2 m; start: (0.8, 0.8) m; mintacel: (6.5, 4.2) m.
# Reteg: /astar_map, /astar_path, /astar_dwa_markers, /scan es TF.
```

## Terminal 3: ellenorzes

```bash
source /opt/ros/jazzy/setup.bash
cd "/mnt/c/Users/Rum Dániel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo"
source install/setup.bash
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
ros2 node list
ros2 topic info /clock
ros2 topic info /gazebo/odom
ros2 topic info /gazebo/wheel_odom
ros2 topic info /odom
ros2 topic info /cmd_vel
ros2 topic info /scan
ros2 topic info /tracked_obstacles
ros2 topic info /goal_pose
ros2 param get /astar_dwa_node autostart
ros2 param get /astar_dwa_node obstacle_source
ros2 param get /astar_dwa_node external_control_ticks
ros2 param get /astar_dwa_node gazebo_runtime
ros2 param get /astar_dwa_node odometry_is_world
ros2 service type /world/dwa_world/create
ros2 service type /world/dwa_world/remove
# Mindegyik felsorolt adat-topicnak csak egy aktiv publishere legyen.
# A /goal_pose topicnal Subscription count: 1; autostart: false.
# obstacle_source: tracked; external_control_ticks: false.
# gazebo_runtime: true; create: SpawnEntity; remove: DeleteEntity.
# odometry_is_world: true; indulo sor: odometry=Gazebo-world.
# Celnaplo: RViz goal, Planned goal, Goal reached. A default_goal csak mintacel.
# Utvonalrajz visszajelzese: Gazebo global path visible: ... points.
```