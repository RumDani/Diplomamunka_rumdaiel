# Gazebo + ROS 2 szimuláció (A* + DWA)

ROS 2 Jazzy, Gazebo (gz sim), TurtleBot3 Waffle, slam_toolbox. Linuxon vagy Windows alatt WSL2 Ubuntu-ban futtatható.

## Mappák
```
Gazebo_ROS2/
├── src/
│   ├── astar_dwa_controller/   C++ vezérlő (A* + DWA), RViz beállítás
│   └── dwa_gazebo_sim/         Gazebo világ, SLAM, akadálykövetés, launch fájlok
└── python_deps/                robot.py és astar_project/grid_map.py (a Python node-ok használják, a build telepíti)
```

## Build (egyszer, kódváltozás után újra)
```bash
cd <ez a mappa>          # pl. "/mnt/c/Users/.../Projekt/Gazebo_ROS2"
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src --rosdistro jazzy -r -y
colcon build --symlink-install
source install/setup.bash
```

## Környezet (minden új terminálban)
```bash
source /opt/ros/jazzy/setup.bash
cd <ez a mappa>
source install/setup.bash
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
export DISPLAY=:0 QT_QPA_PLATFORM=xcb QT_X11_NO_MITSHM=1
export XDG_RUNTIME_DIR=/tmp/gazebo-runtime
mkdir -p "$XDG_RUNTIME_DIR" && chmod 700 "$XDG_RUNTIME_DIR"
```

## 1. Feltérképezés (egyszer)
A terminál:
```bash
ros2 launch dwa_gazebo_sim simulation.launch.py slam_mode:=mapping start_planner:=false map_resolution:=0.10
```
B terminál (RViz, Fixed Frame: `map`):
```bash
ros2 launch dwa_gazebo_sim visualization.launch.py
```
C terminál (kézi vezetés lassan, amíg a térkép teljes nem lesz):
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p speed:=0.15 -p turn:=0.5
```

## 2. Térkép mentése
```bash
mkdir -p "$HOME/maps"; MAP="$HOME/maps/palya"
ros2 run nav2_map_server map_saver_cli -f "$MAP" --ros-args -p save_map_timeout:=10.0
ros2 service call /slam_toolbox/serialize_map slam_toolbox/srv/SerializePoseGraph "{filename: '$MAP'}"
```
Ezután állíts le mindent (Ctrl+C).

## 3. Futtatás a mentett térképpel
A terminál:
```bash
ros2 launch dwa_gazebo_sim simulation.launch.py slam_mode:=localization map_file:="$HOME/maps/palya" initial_x:=0.8 initial_y:=0.8 initial_yaw:=0.0
```
B terminál:
```bash
ros2 launch dwa_gazebo_sim visualization.launch.py
```
RViz-ben **2D Goal Pose**-szal adj célt (ha kell, előbb **2D Pose Estimate**). A robot az A* útját követi DWA-val, és kikerüli a két mozgó akadályt (a szembejövő a robot `odom x ≥ 0`, az oldalról érkező `x ≥ 0,8` esetén indul; kikapcsolás: `enable_crossing_obstacle:=false`).

Cél parancssorból (a feliratkozó ~40 s után érhető el, ismételd, amíg a naplóban `DIAG_GOAL` megjelenik):
```bash
ros2 topic pub --once /goal_pose geometry_msgs/msg/PoseStamped "{header: {frame_id: map}, pose: {position: {x: 6.5, y: 4.2}, orientation: {w: 1.0}}}"
```
Siker: a naplóban `DIAG_CONTROL cpp reason=finished`. A futás ~2–4 perc (a Gazebo lassú, RTF ≈ 0,1–0,2).

## Hibakeresés
- **Új indítás előtt mindig tiszta állapot kell.** A régi folyamatok (gz sim, parameter_bridge, régi node-ok) két szimulációt eredményeznek: a robot nem indul (`DIAG_CONTROL cpp reason=stale_input`), a cél nem érkezik meg. Megoldás: Windows PowerShellben `wsl --shutdown`, majd nyiss új WSL terminált.
- Ctrl+C után megmaradt `gz sim`: `pgrep -a gz`, majd `kill <PID>`.
- Villogó/eltűnő zöld útvonal RViz-ben: javítva (nulla időbélyeg + Transient Local); kódváltozás után `colcon build --symlink-install` kell.
- Üres térkép / `tf_missing`: ne ments; indítsd újra a feltérképezést.
- TF-fa: `ros2 run tf2_tools view_frames`; gráf: `rqt_graph`.
