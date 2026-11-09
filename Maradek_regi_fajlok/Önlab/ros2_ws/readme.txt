# --- TERMINÁL 1: Gazebo ---
export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:/opt/ros/jazzy/share/turtlebot3_gazebo/models
export LIBGL_ALWAYS_SOFTWARE=1
gz sim -v 4 ~/ros2_ws/src/my_gazebo_worlds/worlds/dwa_test.sdf

# --- TERMINÁL 2: Bridge + DWA (launch fájllal) ---
cd ~/ros2_ws
source install/setup.bash
ros2 launch dwa_planner dwa_launch.py

# --- TERMINÁL 3: SLAM Toolbox ---
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=True

# --- TERMINÁL 4: RViz2 ---
rviz2


🎯 RViz beállítások (egyszer elég elmenteni):
Állítsd be a Fixed Frame-et map-re

Add hozzá a Map display-t (/map topic)

Add hozzá a TF display-t