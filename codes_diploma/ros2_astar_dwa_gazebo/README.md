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
colcon build --symlink-install --packages-select astar_dwa_controller dwa_gazebo_sim
```

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