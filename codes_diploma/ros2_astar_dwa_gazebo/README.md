# ROS 2 + Gazebo A* + DWA

ROS 2 Jazzy + Gazebo szimulacio TurtleBot3 Waffle robottal:

- A* globalis utvonaltervezes;
- DWA lokalis sebessegvezerles;
- elore ismert statikus akadalyterkep;
- RViz-bol kuldheto celpozicio.

## Forditas WSL2 alatt

WSL Ubuntu terminalban:

```bash
cd "/mnt/c/Users/Rum Dániel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo"
unset AMENT_PREFIX_PATH
unset COLCON_PREFIX_PATH
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source install/setup.bash
```

Ha a launch vagy a vilagfajl modosult, elegendo a Gazebo-csomagot ujraepiteni:

```bash
colcon build --symlink-install --packages-select dwa_gazebo_sim
source install/setup.bash
```

## Mukodo Gazebo-inditas

A megbízható indítási sorrend mindig ez:

1. Gazebo világ;
2. ROS–Gazebo bridge, A* + DWA vezérlő és mozgó akadály node;
3. RViz;
4. célpozíció küldése az RViz `2D Goal Pose` eszközével vagy terminálból.

Egy munkamenetben csak egy Gazebo, egy bridge/vezérlő launch és egy RViz
példány fusson. Ha a robot nem mozog, először a folyamatokat és a topicokat
ellenőrizd, ne küldj egymás után több új célt.

A WSLg-s Gazebo GUI a projekt világával közvetlenül indítva működik. A fekete
képernyő elkerüléséhez ne kényszerítsd az OpenGL/llvmpipe változókat; az
`xcb` mód és a rendszer alapértelmezett OpenGL beállítása működik.

```bash
export TURTLEBOT3_MODEL=waffle
export DISPLAY=:0
export XDG_RUNTIME_DIR=/tmp/gazebo-runtime
mkdir -p "$XDG_RUNTIME_DIR"
chmod 700 "$XDG_RUNTIME_DIR"
export QT_QPA_PLATFORM=xcb
export QT_X11_NO_MITSHM=1
export GZ_SIM_RESOURCE_PATH=/opt/ros/jazzy/share/turtlebot3_gazebo/models

gz sim -v 4 -r \
"/mnt/c/Users/Rum Dániel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/worlds/dwa_world.sdf"
```

A `GZ_SIM_RESOURCE_PATH` azért szükséges, mert a világfájl a
`model://turtlebot3_waffle` modellt használja. Ha ez nincs beállítva, a Gazebo
ablaka elindulhat, de a világ vagy a robot nem töltődik be.

A közvetlen `gz sim` indítás a tesztelt megoldás. A ROS bridge és az A* node
külön, második terminálban indítandó, miután a Gazebo szerver és GUI már fut.
E nélkül az RViz és a vezérlő nem kap `/scan`, `/odom` és `/clock` adatokat.

```bash
cd "/mnt/c/Users/Rum Dániel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo"
unset AMENT_PREFIX_PATH
unset COLCON_PREFIX_PATH
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch dwa_gazebo_sim bridge_and_controller.launch.py
```

Ellenőrizd, hogy a bridge és a vezérlő tényleg létrehozta-e a kapcsolatokat:

```bash
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
ros2 topic list
ros2 topic info /odom
ros2 topic info /scan
ros2 topic info /goal_pose
```

Elvárt állapot:

- `/odom`: `Publisher count: 1`;
- `/scan`: `Publisher count: 1`;
- `/goal_pose`: `Subscription count: 1`;
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

A Gazebo térképe jelenleg `8 x 5 m`, `0,2 m` felbontással, vagyis `40 x 25`
cellás tervezési terület. A Gazebo robotmodell `(0,8; 0,8) m` helyen spawnol.
Az `/odom` plugin lokális koordinátáját a vezérlő a
`rosbot.yaml` `initial_pose_x/y = 0,8 m` offsetjével alakítja térképi
világkoordinátává. A tesztelt célpozíció `(6,5; 4,2) m`.

Az RViz-ben az A* útvonal zöld, a kiválasztott DWA-trajektória kék, a
statikus akadályok pirosak, azok robotmérettel növelt biztonsági zónája
halványsárga, a LiDAR által érzékelt pontok pedig sárgák. A vezérlő alapértelmezett
maximális lineáris sebessége `0,32 m/s`; ez a `rosbot.yaml` paraméterben
állítható.

## RViz inditasa

Harmadik terminalban:

```bash
source /opt/ros/jazzy/setup.bash
source "/mnt/c/Users/Rum Dániel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo/install/setup.bash"
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
export DISPLAY=:0
export XDG_RUNTIME_DIR=/tmp/gazebo-runtime
mkdir -p "$XDG_RUNTIME_DIR"
chmod 700 "$XDG_RUNTIME_DIR"
export QT_QPA_PLATFORM=xcb
export QT_X11_NO_MITSHM=1
ros2 launch dwa_gazebo_sim visualization.launch.py
```

Az RViz konfiguráció automatikusan az `odom` Fixed Frame-et és a
`2D Goal Pose` eszközt tölti be. Ha a gomb nem látható, az RViz bal oldali
eszköztárában válaszd ki a `2D Goal Pose` ikont, majd kattints a térképen a
célhelyre és húzd meg a kívánt irányt.

Terminálból ugyanígy küldhető cél:

```bash
ros2 topic pub --once /goal_pose geometry_msgs/msg/PoseStamped \
  "{header: {frame_id: odom}, pose: {position: {x: 6.5, y: 4.2, z: 0.0}, orientation: {w: 1.0}}}"
```

Új célpozíciót mindig azután küldj, hogy az `/odom`, `/scan` és `/goal_pose`
kapcsolatokat ellenőrizted. A célpozíció nem marad meg a vezérlő
újraindítása után.

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

## Fontos topicok

- `/goal_pose`: kezi celpozicio;
- `/astar_path`: A* utvonal;
- `/astar_map`: ismert akadalyterkep;
- `/scan`: LiDAR-meres;
- `/cmd_vel`: Gazebo fele kuldott sebessegparancs.

## Leallitas

A futo Gazebo-terminalban nyomd meg a `Ctrl+C` billentyukombinaciot. Ez nem
beirando shell-parancs.
