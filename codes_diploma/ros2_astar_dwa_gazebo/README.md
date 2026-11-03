## Terminalparancsok

### Terminal 0: regi folyamatok leallitasa

```bash
pkill -9 -x astar_dwa_node 2>/dev/null || true
pkill -9 -x moving_obstacle 2>/dev/null || true
pkill -9 -x parameter_bridge 2>/dev/null || true
pkill -9 -x ruby 2>/dev/null || true
pkill -9 -x rviz2 2>/dev/null || true
pkill -9 -x ros2 2>/dev/null || true
ros2 daemon stop 2>/dev/null || true
ros2 daemon start 2>/dev/null || true
```

### Terminal 0: teljes ujraforditas

```bash
source /opt/ros/jazzy/setup.bash
cd "/mnt/c/Users/Rum Dániel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo"
colcon build --symlink-install
```

### Terminal 1: szimulacio

```bash
source /opt/ros/jazzy/setup.bash
export TURTLEBOT3_MODEL=waffle
export DISPLAY=:0
export XDG_RUNTIME_DIR=/tmp/gazebo-runtime
mkdir -p "$XDG_RUNTIME_DIR"
chmod 700 "$XDG_RUNTIME_DIR"
cd "/mnt/c/Users/Rum Dániel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo"
source install/setup.bash
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
ros2 launch dwa_gazebo_sim simulation.launch.py software_rendering:=true
```

### Terminal 1 ellenorzes: csak egy ido- es odom-forras

```bash
source /opt/ros/jazzy/setup.bash
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
ros2 topic info /clock
ros2 topic info /odom
ros2 topic info /clock -v
```

```text
/clock Publisher count: 1
/odom Publisher count: 1
```

Ha bármelyik érték `2`, ne indíts RViz-t; ismételd meg a Terminal 0
leállító blokkot, majd indítsd újra csak a fő szimulációt.

RViz-t csak ezek után indítsd.

### Terminal 2: RViz

```bash
source /opt/ros/jazzy/setup.bash
export DISPLAY=:0
export XDG_RUNTIME_DIR=/tmp/gazebo-runtime
mkdir -p "$XDG_RUNTIME_DIR"
chmod 700 "$XDG_RUNTIME_DIR"
export QT_QPA_PLATFORM=xcb
export QT_X11_NO_MITSHM=1
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
cd "/mnt/c/Users/Rum Dániel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo"
source install/setup.bash
ros2 launch dwa_gazebo_sim visualization.launch.py
```

### Terminal 3: cel kuldese

```bash
source /opt/ros/jazzy/setup.bash
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
ros2 topic info /goal_pose
ros2 topic pub --once /goal_pose geometry_msgs/msg/PoseStamped \
  "{header: {frame_id: odom}, pose: {position: {x: 6.5, y: 4.2, z: 0.0}, orientation: {w: 1.0}}}"
```

Az RViz-ben a Fixed Frame `odom`, a célküldéshez a `2D Goal Pose` eszköz
használható. A `GZ_SIM_RESOURCE_PATH` beállítását a fő launch automatikusan
elvégzi a `turtlebot3_waffle` modell feloldásához.

Az RViz konfigurációban a nyers `Odometry` display alapból ki van kapcsolva,
mert a Gazebo lokális odometriája és az A* világkoordinátája külön offsetet
használ. A robot és az útvonal megjelenítéséhez a TF, az `/astar_map`, az
`/astar_path` és az `/astar_dwa_markers` rétegek szolgálnak.

A C++ ROS 2 szimuláció a Python DWA-val azonos alapelveket használja
(differenciális kerékkinematika, gyorsuláskorlát, trajektória-predikció,
fékezhetőség és pontozás), de nem azonos program: a robot sugara, a
`predict_time`, a DWA-súlyok és az akadálybemenet eltérhetnek.

A statikus falakat az A* kezeli a `rosbot.yaml` ismert akadálypontjaiból.
A DWA a LiDAR-bemenetből csak a statikus fal közvetlen visszaverődési pontjait
szűri ki; a mozgó akadályok távolabbi pontjai megmaradnak a lokális vizsgálathoz.

Ellenőrizd, hogy a bridge és a vezérlő tényleg létrehozta-e a kapcsolatokat:

```bash
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
ros2 topic list
ros2 topic info /odom
ros2 topic info /scan
ros2 topic info /goal_pose
ros2 topic info /clock
```

Elvárt állapot:

- `/odom`: `Publisher count: 1`;
- `/scan`: `Publisher count: 1`;
- `/goal_pose`: `Subscription count: 1`;
- `/clock`: `Publisher count: 1`;
- `/astar_path`: aktív publisher.

Ha az `/odom` vagy `/scan` még nem létezik, várj néhány másodpercet. Ha
továbbra sem jelenik meg, ellenőrizd, hogy a Gazebo szerver fut-e, majd a
bridge-et indítsd újra.

Az `rqt_graph` előtt várd meg, hogy a bridge létrehozza az `/scan` és `/odom`
topicokat. A ROS2 discovery gyorsításához ezt használd:

```bash
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
rqt_graph --force-discover
```

Ha az `rqt_graph` üres, ne indíts újabb Gazebo-példányt. Ellenőrizd a gráfot
közvetlen discovery-val:

```bash
ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST ros2 node list --no-daemon
ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST ros2 topic list --no-daemon
```

Egy munkamenetben csak egy Gazebo-példány és egy bridge fusson. Több régi
`gz sim`, `parameter_bridge` vagy `ros2 launch` folyamat üres vagy hibás
`rqt_graph`-ot okozhat.

Az A* a statikus akadályokat a robot sugarával növeli, de kör alakú
inflációval. Ez azért fontos, mert a két akadály közötti fizikailag átjárható
rés így nem záródik le mesterségesen négyzetes blokkal.

A két mozgó akadály a Python-szimulátorral azonos kezdőállapotból indul:
`moving_obstacle_1=(2.4, 0.4) m`, sebessége `(vx, vy)=(0, 0.20) m/s`,
valamint `moving_obstacle_2=(6.8, 2.1) m`, sebessége
`(vx, vy)=(-0.25, 0) m/s`. A `moving_obstacle_node` a bridge-en keresztül
bekötött `/world/dwa_world/set_pose` szolgáltatással frissíti őket. A node
egyszerre csak egy pozíciófrissítést tart függőben, ezért nem árasztja el a
Gazebo szolgáltatást egymásra torlódó kérésekkel.

Ellenőrzéshez:

```bash
ros2 node list
ros2 service list | grep set_pose
ros2 service type /world/dwa_world/set_pose
```

Ha a node elindult, de a modell nem mozog, ellenőrizd, hogy a world új példánya
indult-e a módosított forrásból, és ne maradjon futva egy régi Gazebo-példány.
Az új world és az akadálymozgás a Python-szimuláció `0,1 s` időlépéses,
egyenletes `vx/vy` modelljét követi.

A Gazebo térképe jelenleg `8,2 x 5,2 m`, `0,2 m` felbontással. A robot az SDF
világban `(0,8; 0,8) m` helyen spawnol. A Gazebo `/odom` üzenete lokális
koordinátát ad, ezért a vezérlő egyszer hozzáadja a `rosbot.yaml`
`initial_pose_x/y = 0,8 m` értékeit, és így képezi a térképi világkoordinátát.
A tesztelt célpozíció `(6,5; 4,2) m`.

Az RViz-ben az A* útvonal zöld, a kiválasztott DWA-trajektória kék, a
statikus akadályok pirosak, azok robotmérettel növelt biztonsági zónája
halványsárga, a LiDAR által érzékelt pontok pedig sárgák. A vezérlő alapértelmezett
maximális lineáris sebessége `0,32 m/s`; ez a `rosbot.yaml` paraméterben
állítható.

## Gyors hibaellenőrzés

```bash
ros2 node list
ros2 topic list
ros2 topic info /odom
ros2 topic info /scan
ros2 topic info /goal_pose
ros2 topic echo /astar_path --once
```

Ha az RViz-ben nem tudsz célt adni, ellenőrizd, hogy az `astar_dwa_node` fut-e
és a `/goal_pose` topicnál `Subscription count: 1` látható-e. Ha az RViz
ablak üres, ellenőrizd az `odom` Fixed Frame-et és azt, hogy az `/odom` és
`/scan` publisher számlálója egy-e. Ha a robot szűk akadályrésben lassít,
az aktuális DWA-diagnosztika a bridge/vezérlő terminálban látható:

```text
DWA jeloltek: teszt=..., sebesseg=..., hatar=..., akadaly=..., fekezes=...
```

Az `akadaly` érték növekedése LiDAR-alapú biztonsági elutasítást jelent; ez
szűk átjáróban lassulást okozhat, de önmagában nem jelenti azt, hogy az A*
nem talált útvonalat.

## Fekete Gazebo-kepernyo

Először csak egy Gazebo-példány fusson. A régi példányok ellenőrzése:

```bash
ps -ef | grep -E 'gz sim|ros2 launch|rviz2' | grep -v grep
```

Ha régi folyamat maradt, zárd le a saját PID-jeit, majd indítsd újra a fő
launchot. Ne indítsd egyszerre a `gz sim` közvetlen parancsot és a
`simulation.launch.py` fájlt.

A modellútvonal ellenőrzése:

```bash
source /opt/ros/jazzy/setup.bash
echo "$GZ_SIM_RESOURCE_PATH"
ls /opt/ros/jazzy/share/turtlebot3_gazebo/models/turtlebot3_waffle
```

Ha a GUI fekete, de a `gz sim` folyamat fut, közvetlenül teszteld a Gazebo-t
az önlabos működő paranccsal:

```bash
source /opt/ros/jazzy/setup.bash
export TURTLEBOT3_MODEL=waffle
export DISPLAY=:0
export XDG_RUNTIME_DIR=/tmp/gazebo-runtime
mkdir -p "$XDG_RUNTIME_DIR"
chmod 700 "$XDG_RUNTIME_DIR"
export GZ_SIM_RESOURCE_PATH=/opt/ros/jazzy/share/turtlebot3_gazebo/models
export LIBGL_ALWAYS_SOFTWARE=1
gz sim -v 4 -r \
  "/mnt/c/Users/Rum Dániel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/worlds/dwa_world.sdf"
```

Ha ez a közvetlen parancs is fekete, a hiba WSLg/Mesa grafikus környezeti
hiba, nem A* vagy DWA hiba. Ellenőrizd:

```bash
echo "$DISPLAY"
echo "$WAYLAND_DISPLAY"
glxinfo -B 2>/dev/null | grep -E 'OpenGL renderer|OpenGL version'
```

Ha a `glxinfo` nincs telepítve, ez nem akadályozza a szimulációt. A Gazebo
indítási logja és a `gz sim` folyamat megléte fontosabb, mint az RViz topiclista.

## Fontos topicok

- `/goal_pose`: kezi celpozicio;
- `/astar_path`: A* utvonal;
- `/astar_map`: ismert akadalyterkep;
- `/scan`: LiDAR-meres;
- `/cmd_vel`: Gazebo fele kuldott sebessegparancs.

## Leallitas

A futo Gazebo-terminalban nyomd meg a `Ctrl+C` billentyukombinaciot. Ez nem
beirando shell-parancs.
