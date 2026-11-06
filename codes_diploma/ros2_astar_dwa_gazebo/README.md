## Terminal 0: regi folyamatok leallitasa

```bash
source /opt/ros/jazzy/setup.bash
pkill -TERM -f 'ros2 launch dwa_gazebo_sim (simulation|visualization)\.launch\.py' 2>/dev/null || true
pkill -TERM -f '/(python_planner_node|python_simulation_node|lidar_obstacle_node|gazebo_path_node|moving_obstacle_node)( |$)' 2>/dev/null || true
pkill -TERM -x astar_dwa_node 2>/dev/null || true
pkill -TERM -f '/parameter_bridge( |$)' 2>/dev/null || true
pkill -TERM -x rviz2 2>/dev/null || true
pkill -TERM -f 'gz sim|gz-sim-[0-9]+-(server|gui)' 2>/dev/null || true
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
ros2 daemon stop
ros2 daemon start
```

## Terminal 0: cpp-rethink lehuzasa es build

```bash
source /opt/ros/jazzy/setup.bash
cd "/mnt/c/Users/Z0057VYV/Desktop/Diplomamunka_rumdaiel/codes_diploma/ros2_astar_dwa_gazebo"
git fetch origin
git switch --track -c cpp-rethink origin/cpp-rethink 2>/dev/null || git switch cpp-rethink
git pull --ff-only origin cpp-rethink
rosdep install --from-paths src --ignore-src --rosdistro jazzy -r -y
colcon build --symlink-install --packages-select astar_dwa_controller dwa_gazebo_sim
source install/setup.bash
```

## Terminal 1: C++ vezerlo es TurtleBot Gazebo

```bash
source /opt/ros/jazzy/setup.bash
cd "/mnt/c/Users/Z0057VYV/Desktop/Diplomamunka_rumdaiel/codes_diploma/ros2_astar_dwa_gazebo"
source install/setup.bash
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
export DISPLAY=:0
export TURTLEBOT3_MODEL=waffle
export XDG_RUNTIME_DIR=/tmp/gazebo-runtime
mkdir -p "$XDG_RUNTIME_DIR"
chmod 700 "$XDG_RUNTIME_DIR"
ros2 launch dwa_gazebo_sim simulation.launch.py software_rendering:=true
# Elvart C++ indulo uzenet: A* + DWA: cpp-world-pose-scan-tracking-v2.
# A robot az RViz 2D Goal Pose celra indul; a fizika folyamatos.
```

Ha a regi indulo uzenet jelenik meg, a masik gepen pull es uj C++ build kell
(Terminal 0). A `final_v1` Python-plannert inditott; itt a C++ megvalositas
marad, a scan-idobelyeges kovetes es a frissessegi vedelem annak mintajat koveti.
Az akadaly kikerulese meg Gazebo-futasban ellenorizendo; nincs futasi garancia.

## Terminal 2: RViz es celadas

```bash
source /opt/ros/jazzy/setup.bash
cd "/mnt/c/Users/Z0057VYV/Desktop/Diplomamunka_rumdaiel/codes_diploma/ros2_astar_dwa_gazebo"
source install/setup.bash
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
export DISPLAY=:0
export QT_QPA_PLATFORM=xcb
export QT_X11_NO_MITSHM=1
export XDG_RUNTIME_DIR=/tmp/gazebo-runtime
mkdir -p "$XDG_RUNTIME_DIR"
chmod 700 "$XDG_RUNTIME_DIR"
ros2 launch dwa_gazebo_sim visualization.launch.py
# Fixed Frame: odom. Celadaszkoz: 2D Goal Pose.
# Az A* ut zold az RViz-ben es vizualis modelkent a Gazebo padlojan is.
```

## Terminal 3: odometria, cel es vezerles ellenorzese

```bash
source /opt/ros/jazzy/setup.bash
cd "/mnt/c/Users/Z0057VYV/Desktop/Diplomamunka_rumdaiel/codes_diploma/ros2_astar_dwa_gazebo"
source install/setup.bash
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
ros2 node list
ros2 topic info /cmd_vel
ros2 topic info /scan
ros2 topic info /odom
ros2 topic info /gazebo/wheel_odom
ros2 topic info /goal_pose
ros2 topic echo --once /odom
ros2 topic echo --once /gazebo/wheel_odom
```

## Terminal 4: TF-fa mentese es megjelenitese

Az alabbi parancsokat te futtasd WSL/Linux terminalban, mikozben a Terminal 1
szimulacioja fut. Nem elore megrajzolt abrakat inditanak: az aktualis ROS
adatokbol kerik le a TF-fat, illetve a Terminal 6-ban a node/topic grafot.

A jelenlegi controller az `odom -> base_link -> base_scan` transzformaciokat
publikalja. A `view_frames --output frames` a futas kozben latott TF-fat
a munkakonyvtarba menti (`frames.gv`, `frames.pdf`), ezert ezt a kulon
diagnosztikai mappabol inditsd:

```bash
source /opt/ros/jazzy/setup.bash
cd "/mnt/c/Users/Z0057VYV/Desktop/Diplomamunka_rumdaiel/codes_diploma/ros2_astar_dwa_gazebo/results/diagnostics"
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
export DISPLAY=:0
ros2 run tf2_tools view_frames --output frames
xdg-open frames.pdf
```

Hianyzo eszkozok telepitese: `sudo apt install ros-jazzy-tf2-tools graphviz xdg-utils`.
Az `xdg-open` a PDF-et az alapertelmezett megjelenitoben nyitja meg; ha nincs
PDF-megjelenito, a `frames.pdf` VS Code-bol is megnyithato.

## Terminal 5: eloben kovetheto TF-transzformacio

```bash
source /opt/ros/jazzy/setup.bash
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
ros2 run tf2_ros tf2_echo odom base_scan
```

## Terminal 6: ROS node- es topicgraf

Ezt a szimulacio es az RViz futasa kozben inditsd. Az `rqt_graph` a node-ok
kozotti ROS topic-kapcsolatokat mutatja; nem azonos a fenti geometriai TF-faval.

```bash
source /opt/ros/jazzy/setup.bash
cd "/mnt/c/Users/Z0057VYV/Desktop/Diplomamunka_rumdaiel/codes_diploma/ros2_astar_dwa_gazebo"
source install/setup.bash
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
export DISPLAY=:0
export QT_QPA_PLATFORM=xcb
ros2 run rqt_graph rqt_graph
```

Ha a parancs nem talalja a csomagot: `sudo apt install ros-jazzy-rqt-graph`.