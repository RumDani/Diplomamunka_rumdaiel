# Indítás három fázisban

**Először: előkészítés → 1. feltérképezés → 2. mentés → teljes leállítás → 3. mentett térképes indítás.**
Később csak az előkészítés és a **3. fázis** kell; ne fussanak párhuzamosan régi szimulációk.

## Előkészítés

**VS Code PowerShell: frissítés** – a pull a követett távoli ágból frissít, a merge önmagában nem tölt le semmit.

```powershell
Set-Location "C:\Users\Rum Dániel\Desktop\Diplomamunka"
git fetch --all
git switch cpp-rethink
git pull --ff-only
git log -1 --oneline
```

**WSL: build, csak kódfrissítés után** – a forrás frissítése nem építi újra a futó programot.

```bash
cd "/mnt/c/Users/Rum Dániel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo"
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src --rosdistro jazzy -r -y
ls -l src/dwa_gazebo_sim/config/slam.yaml
colcon build --symlink-install --packages-select astar_dwa_controller dwa_gazebo_sim
source install/setup.bash
ros2 pkg prefix dwa_gazebo_sim
ls -l "$(ros2 pkg prefix dwa_gazebo_sim)/share/dwa_gazebo_sim/config/slam.yaml"
```

**Ha `No such file .../config/slam.yaml` jelenik meg:** ez a csomag telepítési konfigurációja, nem a `~/maps/palya` mentés.
Ha már a `src/...` fájl hiányzik, előbb frissítsd a megfelelő klónt; ha csak az installból hiányzik, buildeld újra a fenti két csomagot.
Csak sikeres build és a második `ls` által megtalált fájl után indítsd a 3. fázist; az üzenetben a `ros2 pkg prefix` a most buildelt workspace-re mutasson.
A mentett térképet emiatt nem kell újraépíteni vagy felülírni; ha a fájl továbbra is hiányzik, a teljes buildkimenetet küldd vissza.

**Ha a build egy már törölt `robot_controller.launch.py` fájlt akar másolni:** régi generált symlink maradt a buildben; állítsd le a futásokat, frissítsd a kódot, majd új WSL-terminálban:

```bash
cd "/mnt/c/Users/Rum Dániel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo"
source /opt/ros/jazzy/setup.bash
if [ -d build/dwa_gazebo_sim ]; then mv -- build/dwa_gazebo_sim "build/dwa_gazebo_sim_backup_$(date +%Y%m%d_%H%M%S)"; fi
colcon build --symlink-install --packages-select astar_dwa_controller dwa_gazebo_sim
source install/setup.bash
ls -l "$(ros2 pkg prefix dwa_gazebo_sim)/share/dwa_gazebo_sim/config/slam.yaml"
```

Az átnevezés csak az érintett csomag generált buildjét teszi félre, a forrást és a `~/maps` mentést nem módosítja; ne hozd vissza a törölt launch-fájlt.
Csak sikeres build és megtalált `slam.yaml` után folytasd a **3. fázissal**, nem kell újra feltérképezni.

**Minden új WSL-terminál elején ezt futtasd**, a `~` mappából is működik:

```bash
source /opt/ros/jazzy/setup.bash
cd "/mnt/c/Users/Rum Dániel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo"
source install/setup.bash
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
export DISPLAY=:0
export QT_QPA_PLATFORM=xcb
export QT_X11_NO_MITSHM=1
export XDG_RUNTIME_DIR=/tmp/gazebo-runtime
mkdir -p "$XDG_RUNTIME_DIR" results/diagnostics
chmod 700 "$XDG_RUNTIME_DIR"
```

Másik gépen az útvonalat cseréld a sajátodra, az idézőjeleket megtartva; hiba esetén állj meg.

## Tiszta újraindítás hiba után

1. Állítsd meg a robotot, majd Ctrl+C-vel zárd be a teleopot/plannert, az RViz-t és végül a Gazebo–SLAM futást.
2. Nyiss új WSL-terminált, és futtasd a fenti **Minden új WSL-terminál elején** blokkot.
3. Az alábbi paranccsal indíts új feltérképezést; ez az 1. fázis A termináljának indítása helyett használandó, ne indíts két szimulációt.

```bash
ros2 daemon stop
ros2 daemon start
ros2 launch dwa_gazebo_sim simulation.launch.py slam_mode:=mapping start_planner:=false map_resolution:=0.10 2>&1 | tee "results/diagnostics/mapping_$(date +%Y%m%d_%H%M%S).log"
```

Ezután az 1. fázis **B és C termináljával** folytasd: RViz, majd kézi mozgatás.
A daemon újraindítása nem állítja le a régi node-okat és nem hoz létre hiányzó TF-et; ezért szükséges előtte a Ctrl+C-s leállítás.
A `queue is full` nem megtelt tárhely: hiányzó/késő TF miatt is betelhet a mérések várakozási sora.
Ha friss indítás után is `odom ... does not exist` vagy tartós TF-hiba látszik, ne ments és ne indíts lokalizációt; küldd a `mapping_*.log` fájlt a `DIAG_TF`, `DIAG_ODOM` és SLAM sorokkal.

## 1. Feltérképezés

**A terminál: Gazebo + új SLAM-térkép** – a planner még nem vezérli a robotot.

```bash
ros2 launch dwa_gazebo_sim simulation.launch.py slam_mode:=mapping start_planner:=false map_resolution:=0.10 2>&1 | tee "results/diagnostics/mapping_$(date +%Y%m%d_%H%M%S).log"
```

**B terminál: RViz** – itt látod a feltérképezett területet; Fixed Frame: `map`.

```bash
ros2 launch dwa_gazebo_sim visualization.launch.py
```

**C terminál: kézi mozgatás** – az aktív teleop terminál billentyűivel lassan járd körbe a pályát.

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p speed:=0.15 -p turn:=0.5
```

**A térképnek az RViz-ben látszania és bővülnie kell.** Ha üres a nézet, `tf_missing`, `waiting_map` vagy tartós `queue is full` látszik, ne ments és ne indíts lokalizációt.

## 2. Mentés

**C terminál:** állítsd meg a robotot, majd Ctrl+C-vel zárd be a teleopot; az A és B terminál maradjon futva.

Először ellenőrizd, hogy valóban érkezik térkép:

```bash
ros2 lifecycle get /slam_toolbox
timeout 10s ros2 topic echo --once /map --field info
```

Elvárt: `active`, valamint pozitív `width` és `height`; ha nincs adat vagy hibát kapsz, állj meg és küldd az A terminál naplóját.

Ha már létezik régi `~/maps/palya` mentés, előbb másold el:

```bash
cp -a "$HOME/maps" "$HOME/maps_backup_$(date +%Y%m%d_%H%M%S)"
```

Ezután mentsd a térképképet:

```bash
mkdir -p "$HOME/maps"
MAP="$HOME/maps/palya"
ros2 run nav2_map_server map_saver_cli -f "$MAP" --ros-args -p save_map_timeout:=10.0
```

**Csak sikeres térképképmentés után** mentsd a folytatható SLAM-állapotot ugyanebben a terminálban:

```bash
ros2 service call /slam_toolbox/serialize_map slam_toolbox/srv/SerializePoseGraph "{filename: '$MAP'}"
ls -lh "$MAP"*
```

Eredmény: `.yaml` + térképkép és `.posegraph` + `.data`; a későbbi indítás a két utóbbit használja.
A serialize `result: 0` csak sikeres fájlkiírást jelent, nem bizonyít használható térképet.
**Sikeres mentés után állítsd le az A és B terminál futását is Ctrl+C-vel.**

## 3. Indítás a mentett térképpel

**A terminál: új Gazebo a kezdőhelyről + mentett térképes lokalizáció** – nem kell újra kézzel feltérképezni.

```bash
ros2 launch dwa_gazebo_sim simulation.launch.py slam_mode:=localization map_file:="$HOME/maps/palya" initial_x:=0.8 initial_y:=0.8 initial_yaw:=0.0 2>&1 | tee "results/diagnostics/localization_$(date +%Y%m%d_%H%M%S).log"
```

**B terminál: RViz és céladás** – megjeleníti a mentett térképet és a globális utat.

```bash
ros2 launch dwa_gazebo_sim visualization.launch.py
```

1. Ellenőrizd a robot térképbeli helyét; szükség esetén **2D Pose Estimate**-tel jelöld a helyét és irányát.
2. **2D Goal Pose:** ismert szabad helyen kattints, húzd meg az irányt, majd engedd el.
3. A robot az A*-út waypointjait követi DWA-val; ne indíts mellé teleopot vagy második plannert.

Az `initial_x/y/yaw` a mentett térképben adott becslés, nem a Gazebo robotjának áthelyezése; a példa nem garantálja a helyes lokalizációt.
A `map_file` kiterjesztés nélküli előtag: ugyanahhoz a mentéshez tartozó `.posegraph` és `.data` kell.
Az út RViz-ben és Gazebóban ugyanabból a `/astar_path`-ból rajzolódik; a Gazebo-illesztés csak vizualizáció, nem vezérlési visszacsatolás.

### Kétakadályos teszt (RViz nélkül is)

Az A terminál indítása után két mozgó akadály aktív alapból: a szembejövő (`moving_obstacle_2`, kezdet (6.8, 2.0)) a robot `odom x ≥ oncoming_start_x` (alap 0) esetén, az oldalról érkező (`moving_obstacle_1`) `odom x ≥ crossing_start_x` (alap 0.8) esetén indul. Kikapcsolás: `enable_crossing_obstacle:=false`.

Cél megadása RViz helyett (új, előkészített terminálban; a feliratkozó ~40 s után érhető el, ezért ismételd, amíg a naplóban `DIAG_GOAL cpp` megjelenik):

```bash
ros2 topic pub --once /goal_pose geometry_msgs/msg/PoseStamped "{header: {frame_id: map}, pose: {position: {x: 6.5, y: 4.2}, orientation: {w: 1.0}}}"
```

Sikeres futás a naplóban: `DIAG_SCENARIO event=oncoming_started`, `event=crossing_started`, végül `DIAG_CONTROL cpp reason=finished`. A futás szimulációs sebességgel ~2–4 percig tart.

Ha Ctrl+C után újraindításkor régi szimuláció zavar, keresd meg és állítsd le a megmaradt `gz sim` szerver PID-jét (`pgrep -a gz`, majd `kill <PID>`).
Ha `.sh` szkriptet Windowsban szerkesztesz, WSL-ben előtte: `tr -d '\r' < in.sh > /tmp/in.sh`.

## Új térkép vagy felülírás

Állíts le minden futást, majd ismételd az **1. és 2. fázist**, a régi mentés biztonsági másolatával; ezután a **3. fázissal** indulj.
Lokalizációs módban a mentett térkép nem frissül automatikusan; a fájl felülírása nem cseréli le egy már futó node térképét.

## Csak hibakereséshez

Küldd vissza a `results/diagnostics/mapping_*.log` vagy `localization_*.log` fájlt az indulástól a hibáig; RViz-problémánál képernyőképet is.
Külön előkészített WSL-terminálban a következő parancsokat egyesével futtasd, a folyamatos kimenetet Ctrl+C-vel zárd le:

```bash
ros2 lifecycle get /slam_toolbox
ros2 run tf2_ros tf2_echo odom base_scan
ros2 run tf2_ros tf2_echo map odom
```

**Jelenlegi korlát:** a felhasználói naplóban az `odom` frame hiánya miatt nem épült térkép; a teljes ROS/Gazebo működés még nincs igazolva, a leírás átrendezése ezt nem javítja meg.

## TF-fa és rqt_graph – külön terminálokban

A Gazebo és a SLAM maradjon futva; minden alábbi eszközhöz új WSL-terminált nyiss, és először ezt futtasd:

```bash
source /opt/ros/jazzy/setup.bash
cd "/mnt/c/Users/Rum Dániel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo"
source install/setup.bash
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
export DISPLAY=:0
export QT_QPA_PLATFORM=xcb
export QT_X11_NO_MITSHM=1
export XDG_RUNTIME_DIR=/tmp/gazebo-runtime
mkdir -p "$XDG_RUNTIME_DIR" results/diagnostics
chmod 700 "$XDG_RUNTIME_DIR"
```

### TF-fa rajzolása és megnyitása

A koordinátakeretek geometriai kapcsolatait PDF-be menti és megnyitja.

```bash
cd results/diagnostics
ros2 run tf2_tools view_frames --output frames
xdg-open frames.pdf
```

### Élő TF-adatok

A robot térképbeli becsült helyzetét mutatja; néhány sor után Ctrl+C-vel állítható le.

```bash
ros2 run tf2_ros tf2_echo map base_link
```

Ha hibát jelez, külön-külön ellenőrizd a láncot, a parancsok között Ctrl+C-vel:

```bash
ros2 run tf2_ros tf2_echo odom base_scan
ros2 run tf2_ros tf2_echo map odom
```

### rqt_graph megnyitása

A ROS node-ok és topicok adatkapcsolatait rajzolja ki; ez nem a geometriai TF-fa.

```bash
ros2 run rqt_graph rqt_graph
```

Ha hiányzik valamelyik eszköz: `sudo apt install ros-jazzy-tf2-tools ros-jazzy-rqt-graph graphviz xdg-utils`.