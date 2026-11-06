# Rövid indítás: Gazebo + SLAM + Python A*/DWA

**Sorrend: frissítés/build → SLAM → RViz → kézi térképezés → waypointos navigáció.**
A SLAM eleinte csak a belátott területet mutatja; nincs automatikus felfedezés.
Minden parancsot soronként futtass, és hiba esetén állj meg.

Az útvonalak a tesztgép `C:\Users\Rum Dániel\Desktop\Diplomamunka` mappáját
használják; másik gépen ezt cseréld a saját projektmappádra, az idézőjeleket megtartva.

## 0. Frissítés: VS Code PowerShell Extension terminál

A pull a követett távoli ágból frissít; a merge önmagában nem tölt le változást.

```powershell
Set-Location "C:\Users\Rum Dániel\Desktop\Diplomamunka"
git rev-parse --show-toplevel
git status --short --branch
git fetch --all
git switch cpp-rethink
git pull --ff-only
git log -1 --oneline --decorate
git rev-list --left-right --count 'HEAD...@{upstream}'
```

Az utolsó sorban `0 0` egyezést jelent; a helyi módosításokat ne töröld.
A remote neve lehet `master` is; a `final_v1` a commit szövegében nem a HEAD verziója.

## 1. Build: WSL/Linux terminál

Ez telepíti a függőségeket és a friss forrásból újraépíti a futtatott csomagokat.

```bash
cd "/mnt/c/Users/Rum Dániel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo"
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src --rosdistro jazzy -r -y
colcon build --symlink-install --packages-select astar_dwa_controller dwa_gazebo_sim
```

WSL-ben ugyanazt a projektmásolatot használd; külön WSL-klónban külön pull kell.

## Minden új futtatóterminál elején: WSL/Linux

Ez az adott terminált a megfelelő ROS-workspace-re és helyi kommunikációra állítja.

Az alábbi blokk a `~` mappából is indítható; nem feltételezi, hogy már egy Git-repóban állsz.

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

## 2. Terminál A: Gazebo és SLAM

Elindítja a fizikai világot, kerékodometriát és LiDAR-térképezést, automatikus vezérlő nélkül.

```bash
ros2 launch dwa_gazebo_sim simulation.launch.py start_planner:=false map_resolution:=0.10 2>&1 | tee "results/diagnostics/slam_$(date +%Y%m%d_%H%M%S).log"
```

Ezt a terminált a térképezés és a navigáció alatt is hagyd futni.

## 3. Terminál B: RViz

Megjeleníti a SLAM `/map` térképét, a LiDAR-t és a zöld globális `/astar_path` útvonalat.

```bash
ros2 launch dwa_gazebo_sim visualization.launch.py
```

Fixed Frame: `map`; a `Planner inflated map` réteg a robotmérettel felfújt tiltott területet mutatja.

## 4. Terminál C: kézi feltérképezés

Az aktív teleop terminál billentyűivel lassan körbevezetheted a robotot, miközben az RViz térképe bővül.

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p speed:=0.15 -p turn:=0.5
```

Ha kész a kívánt terület, állítsd meg a robotot és zárd be a teleopot Ctrl+C-vel; az A és B terminál maradjon futva.

## 5. Terminál C: waypointos navigáció

Csak a Python plannert és LiDAR-követőt indítja el a már futó Gazebo/SLAM mellé.

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist '{}'
ros2 launch dwa_gazebo_sim simulation.launch.py start_environment:=false start_planner:=true 2>&1 | tee "results/diagnostics/planner_$(date +%Y%m%d_%H%M%S).log"
```

RViz: **2D Goal Pose → ismert szabad területen kattintás, húzás, elengedés**.
Ne fusson közben teleop vagy második planner; az ismeretlen/foglalt/felfújt célcellát a rendszer elutasítja.

## 6. Terminál D: állapotellenőrzés

Ezekkel ellenőrizhető a tényleges build, az aktív SLAM és a cél-/szenzortopicok kapcsolata.

```bash
git log -1 --oneline
ros2 pkg prefix dwa_gazebo_sim
ros2 lifecycle get /slam_toolbox
ros2 param get /astar_dwa_node map_source
ros2 topic info /map --verbose
ros2 topic info /tracked_obstacles --verbose
ros2 topic info /goal_pose --verbose
ros2 topic info /cmd_vel --verbose
```

Elvárt: SLAM `active`, planner `map_source=topic`, `/tracked_obstacles` publisher `lidar_obstacles`, induláskor `DIAG_CONFIG schema=slam-waypoints-1`.

## 7. Terminál E: TF-fa

A futó rendszer koordinátakapcsolatait PDF-be menti és megnyitja.

```bash
cd "/mnt/c/Users/Rum Dániel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo/results/diagnostics"
ros2 run tf2_tools view_frames --output frames
xdg-open frames.pdf
```

Hiányzó eszközök: `sudo apt install ros-jazzy-tf2-tools graphviz xdg-utils`.

## 8. Terminál F: élő robotpóz

Folyamatosan mutatja a robot SLAM-térképen becsült helyzetét; Ctrl+C-vel állítható le.

```bash
ros2 run tf2_ros tf2_echo map base_link
```

## 9. Terminál G: rqt_graph

Megmutatja a ROS node-ok és topicok kapcsolatait, nem a geometriai TF-fát.

```bash
ros2 run rqt_graph rqt_graph
```

Hiányzó csomag: `sudo apt install ros-jazzy-rqt-graph`.

## 10. Terminál H: az elkészült térkép mentése

Álló robot és továbbra is futó SLAM mellett, egy előkészített WSL-terminálból elmenti a térképképet és a később folytatható SLAM-állapotot.

```bash
mkdir -p "$HOME/maps"
MAP="$HOME/maps/palya_$(date +%Y%m%d_%H%M%S)"
ros2 run nav2_map_server map_saver_cli -f "$MAP"
ros2 service call /slam_toolbox/serialize_map slam_toolbox/srv/SerializePoseGraph "{filename: '$MAP'}"
ls -lh "$MAP"*
```

- `.yaml` és térképkép: foglaltsági térkép, például navigációhoz.
- `.posegraph` és `.data`: SLAM-pózgráf és mérési adatok a térképezés folytatásához.
- A serialize válaszában `result: 0` sikert jelent; hiba esetén a teljes kimenetet küldd vissza.

A fájlok a WSL `~/maps` mappájába kerülnek, időbélyeges névvel; új térképezés előtt ments, ha a jelenlegi térképet meg akarod őrizni.

## 11. Új térkép építése a nulláról

Leállítás és újraindítás után a jelenlegi launch üres SLAM-térképet kezd, a korábban mentett fájlok törlése nélkül.

Először állítsd meg a robotot, zárd be a teleopot/plannert, majd a Gazebo–SLAM termináljában is nyomj Ctrl+C-t; ezután előkészített WSL-terminálban:

```bash
ros2 launch dwa_gazebo_sim simulation.launch.py start_planner:=false map_resolution:=0.10
```

Másik előkészített terminálban járd körbe újra a pályát:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p speed:=0.15 -p turn:=0.5
```

A mentett térkép automatikus visszatöltése és a mentett SLAM-munkamenet folytatása még nincs bekötve a projekt launch-ába; a mentés önmagában ezt nem kapcsolja be.

## Naplók és leállítás

Hibánál a `results/diagnostics/slam_*.log` és `planner_*.log` fájlt küldd vissza az indulástól az esetig, RViz-problémánál képernyőképpel.
Leállítás: előbb teleop/planner, majd RViz és Gazebo/SLAM termináljában Ctrl+C; egyszerre csak egy szimuláció fusson.

**Korlát:** a Gazebo-padlóra rajzolt SLAM-es globális út még nincs bekötve; az RViz-út aktív.
A sikeres kikerülés és SLAM-pontosság még nincs futással igazolva.

<details>
<summary>Korábbi részletes referencia és hibakeresés</summary>

## Python A* + DWA, LiDAR es SLAM Gazeboban

Az aktiv inditas a valtozatlan Matplotlibes Python A*/DWA magot hasznalja.
A `cpp-rethink` ag neve megmaradt, de nem a C++ controller fut.
A `/scan` adja a LiDAR-bemenetet, a SLAM Toolbox a `/map`-et es a
`map -> odom` korrekciot. A robotot `/cmd_vel` hajtja; az odometria a
kerekekbol szarmazik. A Gazebo ground truth csak a `DIAG_ODOM` meresi
osszeveteseben szerepel, nem javitja vissza a robot tervezesi poziciojat.

Uj celra egyszer keszul globalis A*-ut, utana waypointos kovetes es lokalis
DWA mukodik. A SLAM terkepfrissitese azonos frame-ben nem torli az utat,
nem lepteti vissza a waypoint-indexet es nem indit uj A*-keresest.
Nincs automatikus ismeretlen-terulet felfedezes: csak feltetelezett szabad
terkepcellaba adhato cel. A dinamikus akadalyok a fizikai motorban
sebessegvezerelt testek, nem `set_pose`-szal athelyezett objektumok.
Ez idealizalt modell, nem kalibralt valos robot vagy ember modellje.

## Frissítés a VS Code PowerShell Extension termináljából

A Git-parancsok ebben a terminálban is működnek. A ROS-os `source`, `colcon`
és `ros2` parancsokat viszont később WSL/Linux terminálban kell futtatni.
A parancsokat soronként futtasd; hiba esetén ne folytasd automatikusan.

### Mit jelent a fetch, pull és merge?

- `fetch`: letölti a távoli Git-állapotot, de a nyitott forrásfájlokat nem írja át.
- `pull`: letölti a követett távoli ág állapotát és beilleszti a jelenlegi helyi ágba.
- `pull --ff-only`: csak előretekerhető, merge-commit nélküli frissítést enged.
	Ha a két ág eltérő saját commitokat tartalmaz, hibával megáll; ez szándékos védelem.
- `merge`: már letöltött ágakat egyesít; önmagában nem tölt le GitHub-változásokat.
- `switch`: ágat vált; a pull önmagában nem vált át a kívánt ágra.

A bővítmény Pull/Merge/Sync művelete a kiválasztott repositoryra és ágra hat.
Ezért a gomb megnyomása nem bizonyítja, hogy a megfelelő mappát vagy ágat
frissítetted. Ezen a projekten nem kell a `master` ágat kézzel belemerge-elni
a `cpp-rethink` ágba. Az alábbi terminálos ellenőrzés egyértelműbb.

### 1. Ellenőrizd a projektmappát és a helyi változásokat

```powershell
Get-Location
git rev-parse --show-toplevel
git status --short --branch
git remote -v
```

A repoútvonal ugyanahhoz a projektmásolathoz tartozzon, amelynek fájljait
a VS Code-ban nézed. A távoli cím a `RumDani/Diplomamunka_rumdaiel` repository
legyen. Az `M` helyi módosítást jelent, nem régi verziót; például a módosított
Word-dokumentumot nem kell törölni. Ne használj `reset --hard` vagy kényszerített
checkout parancsot a pull helyettesítésére.

### 2. Töltsd le és frissítsd a megfelelő ágat

```powershell
git fetch --all
git switch cpp-rethink
git branch -vv
git pull --ff-only
```

A `git branch -vv` sorában például `[origin/cpp-rethink]` vagy
`[master/cpp-rethink]` látható. A második példában a `master` a remote neve,
nem a helyi `master` ág. A távoli név nem minden gépen `origin`, ezért a
beállított upstreamet használó `git pull --ff-only` parancsot alkalmazzuk.
Ha nincs upstream, az ág nem található vagy konfliktust jelez, állj meg,
és küldd vissza a teljes kimenetet; ne nyomj rá találomra Merge-re.

### 3. Bizonyítsd a frissítést

```powershell
git status --short --branch
git log -1 --oneline --decorate
git rev-list --left-right --count 'HEAD...@{upstream}'
```

Az utolsó sorban `0 0` teljes commit-egyezést jelent a követett távoli ággal.
`0 N` esetén még le vagy maradva; `N 0` esetén saját helyi commitjaid vannak;
ha mindkettő pozitív, az ágak szétváltak, és egyeztetni kell a folytatást.
Az `Everything up-to-date` vagy `Already up to date` csak a kiválasztott
repository és upstream viszonyáról szól, nem egy másik gép fájljairól.

A SLAM-es tesztkód alapcommitja `f4c75e9`; a későbbi README- vagy kódjavítások
miatt a HEAD ennél újabb is lehet. A commit üzenetében szereplő `final_v1`
nem azt jelenti, hogy a HEAD azon a régi tagen áll. A `.venv` a promptban
csak az aktív Python-környezet neve, nem Git-verzió.

### 4. A forrás frissítése nem a futó program frissítése

A sikeres pull után a megfelelő WSL-mappában újra kell buildelni, betölteni
az ottani `install/setup.bash` fájlt, és újraindítani a futást. A következő
Terminal 0 blokk ezt tartalmazza. Ha WSL-ben külön klónod van, nem a
Windows-mappa `/mnt/c/...` megfelelőjét használod, abban a klónban külön
fetch/pull kell. A `ros2 pkg prefix dwa_gazebo_sim` az elvárt workspace
`install` könyvtárába mutasson.

Az aktuális futásban `DIAG_CONFIG schema=slam-waypoints-1` és a tényleges
Python `source=` útvonal jelenik meg. Régi `cpp-world-pose...` üzenet régi
vagy másik buildet jelent. A friss commit önmagában nem bizonyít sikeres
SLAM-et vagy akadálykikerülést; azt a futási naplóval kell ellenőrizni.

## Terminal 0: regi folyamatok leallitasa

```bash
source /opt/ros/jazzy/setup.bash
pkill -TERM -f 'ros2 launch dwa_gazebo_sim (simulation|visualization)\.launch\.py' 2>/dev/null || true
pkill -TERM -f '/(python_planner_node|python_simulation_node|lidar_obstacle_node|gazebo_path_node|moving_obstacle_node)( |$)' 2>/dev/null || true
pkill -TERM -x astar_dwa_node 2>/dev/null || true
pkill -TERM -f '/async_slam_toolbox_node( |$)' 2>/dev/null || true
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
cd "/mnt/c/Users/Rum Dániel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo"
git fetch --all
git switch cpp-rethink
git pull --ff-only
rosdep install --from-paths src --ignore-src --rosdistro jazzy -r -y
colcon build --symlink-install --packages-select astar_dwa_controller dwa_gazebo_sim
source install/setup.bash
```

Hianyzo ROS-csomagok: `sudo apt install ros-jazzy-slam-toolbox ros-jazzy-teleop-twist-keyboard`.
Az `astar_dwa_controller` csomag a Python magot es az RViz-beallitasokat is
telepiti, ezert ezt is buildelni kell. Az ottani C++ binaris nem az aktiv planner.

## Terminal 1: SLAM, Python waypointok es fizikai Gazebo

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
mkdir -p results/diagnostics
RUN_LOG="results/diagnostics/run_$(date +%Y%m%d_%H%M%S).log"
set -o pipefail
{
	git rev-parse --show-toplevel
	git status --short --branch
	git log -1 --oneline --decorate
	ros2 pkg prefix dwa_gazebo_sim
	ros2 pkg prefix astar_dwa_controller
	ros2 launch dwa_gazebo_sim simulation.launch.py software_rendering:=true map_resolution:=0.10
} 2>&1 | tee "$RUN_LOG"
```

Elvart uzenetek: `DIAG_CONFIG schema=slam-waypoints-1`, `python-lidar-reference`,
`python-turtlebot-physical` es `LiDAR-only tracker`. A SLAM lifecycle allapota
`active` legyen. C++ indulouzenet regi vagy masik buildet jelez.
A `RUN_LOG` fajlt kuldd vissza hibakereseskor, az indulastol az esetig.
Ne vagd ki csak a hibas sort: az elozo bemenetek es a megallasi ok is szukseges.

A `final_v1` csak az algoritmus alapja: ott meg ismert Gazebo-akadalyadatok es
vilagpozicios odometria volt. Az aktualis szenzoros/SLAM valtozat nincs
Gazebo-futassal vagy valos roboton igazolva.

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
# Fixed Frame: map. Celadaszkoz: 2D Goal Pose.
# A SLAM terkep es a zold A*-ut az RViz-ben lathato.
```

A `Planner inflated map` reteget bekapcsolva lathato a robotmerettel bovelt
terkep. A korabbi Gazebo-padlo utvonalrajzolas alapbol ki van kapcsolva,
mert a SLAM `map` koordinatai nem azonosithatok vakon Gazebo-vilagkoordinatakkal.

## Terminal 3: odometria, cel es vezerles ellenorzese

```bash
source /opt/ros/jazzy/setup.bash
cd "/mnt/c/Users/Rum Dániel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo"
source install/setup.bash
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
ros2 node list
ros2 lifecycle get /slam_toolbox
ros2 param get /slam_toolbox resolution
ros2 param get /astar_dwa_node map_source
ros2 topic info /cmd_vel
ros2 topic info /scan
ros2 topic info /map --verbose
ros2 topic info /tracked_obstacles --verbose
ros2 topic info /odom
ros2 topic info /gazebo/wheel_odom
ros2 topic info /goal_pose
ros2 topic echo --once /odom
ros2 topic echo --once /gazebo/wheel_odom
ros2 topic echo --once /gazebo/ground_truth_odom
```

A `/tracked_obstacles` egyetlen publishere a `lidar_obstacles` legyen.
A `/map` es `map -> odom` csak a SLAM-tol erkezzen. A robot `/cmd_vel`
topicjat egyszerre csak egy controller vagy teleop vezerelje.

## Terminal 4: TF-fa mentese es megjelenitese

Az alabbi parancsokat te futtasd WSL/Linux terminalban, mikozben a Terminal 1
szimulacioja fut. Nem elore megrajzolt abrakat inditanak: az aktualis ROS
adatokbol kerik le a TF-fat, illetve a Terminal 6-ban a node/topic grafot.

A lanc `map -> odom -> base_footprint -> base_link -> base_scan` lehet;
a `base_footprint` koztes keret az SDF hajtasbeallitasatol fugg.
A `view_frames --output frames` a futas kozben latott TF-fat
a munkakonyvtarba menti (`frames.gv`, `frames.pdf`), ezert ezt a kulon
diagnosztikai mappabol inditsd:

```bash
source /opt/ros/jazzy/setup.bash
cd "/mnt/c/Users/Rum Dániel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo/results/diagnostics"
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
ros2 run tf2_ros tf2_echo map base_link
```

## Terminal 6: ROS node- es topicgraf

Ezt a szimulacio es az RViz futasa kozben inditsd. Az `rqt_graph` a node-ok
kozotti ROS topic-kapcsolatokat mutatja; nem azonos a fenti geometriai TF-faval.

```bash
source /opt/ros/jazzy/setup.bash
cd "/mnt/c/Users/Rum Dániel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo"
source install/setup.bash
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
export DISPLAY=:0
export QT_QPA_PLATFORM=xcb
ros2 run rqt_graph rqt_graph
```

Ha a parancs nem talalja a csomagot: `sudo apt install ros-jazzy-rqt-graph`.

## Kezi feltérkepezes, majd waypointos navigacio ugyanabban a futasban

A Terminal 1 launch parancsat eloszor `start_planner:=false` argumentummal
inditsd. A Gazebo, bridge, odometria es SLAM fut; controller es LiDAR-tracker nem.
Kulon elokeszitett ROS-terminalban mozgasd a robotot:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p speed:=0.15 -p turn:=0.5
```

Ha az RViz-ben felépult a kivant szabad terulet, allitsd le a teleopot,
de ne a Gazebot vagy a SLAM-et. Egy uj, a Terminal 1 szerint elokeszitett
terminalban inditsd csak a waypointos plannert es kovetot:

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist '{}'
ros2 launch dwa_gazebo_sim simulation.launch.py start_environment:=false start_planner:=true
```

Ez nem hoz letre masodik Gazebot, bridge-et vagy SLAM-et. Most adhato RViz-cel
a mar megismert szabad teruleten. Uj celra uj A* fut; a terkep frissulesere nem.

## Terkepracs es poziciohiba

A `map_resolution:=0.20` es `map_resolution:=0.10` ket kulon, teljesen uj
futasban osszehasonlithato; ne fusson ket kornyezet egyszerre. Ugyanaz a
`8.2 x 5.2 m` Gazebo-vilag marad, a SLAM-terkep merete azonban a meresekkel novekszik.
A finomabb racs nem jelenti a fizikai vilag felnagyitasat, es nem garantal
pontosabb poziciobecsleset. A SLAM scan matching es loop closure kulon lepes.

Egy fix origós GridMap-koordinataellenorzesben a `(7.38,4.25) m` cel
cellakozep-elterese `0.20 m` cellanal `0.053852 m`, `0.10 m` cellanal
`0.030000 m` volt. Ez nem mért robot-celhiba; a SLAM origója elterhet.
A kert vegcel pontos koordinatai megmaradnak, a racskozep-elteres kulon naplozott.

## Naplok ertelmezese

- `DIAG_CONFIG`: tenyleges forrasutvonal, robotparameterek es vezerlesi mod.
- `DIAG_MAP`: aktualis origó, felbontas, terkepsorszam es `waypoints_kept` vagy frame-reset.
- `DIAG_ODOM`: nyers kerekpozicio, egyszeri spawn-eltolas es idoben illesztett meresi ground truth.
- `DIAG_LIDAR`: scan-kor, pontok/klaszterek, parositott kovetesek es becsult sebesseg.
- `DIAG_CONTROL`: bemeneti idobelyegek, pozicio, waypoint, DWA-jeloltek, kiadott parancs es okkod.

A `braking_no_pair` jelolthianyt, a `stale_input` elavult bemenetet,
a `planner_deadline` tul keson elkeszult szamitast jelent. Az `admissible`
a Python fekezesi feltetelen atmeno jeloltek szama, nem biztonsagi garancia.
A ground truth csak az odom-frame meresi osszevetese; a SLAM map-frame
helyzetet nem szabad kozvetlenul, frame-illesztes nelkul kivonni belole.

</details>