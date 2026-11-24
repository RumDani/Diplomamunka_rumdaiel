# A* + DWA a Husarion ROSbot 2-n (ROS 2 Foxy)

## Cél és rögzített környezet

**Célhardver: Husarion ROSbot 2. Meglévő rendszer: ROS 2 Foxy, `colcon` és C++ compiler.** Nem telepítünk rendszer-csomagot, nem használunk `sudo apt`, `pip` vagy `rosdep install` parancsot. A fejlesztés a felhasználói könyvtárban lévő saját ROS workspace-be kerül; a `colcon build` csak ezt a workspace overlay-t építi és az `install/` alkönyvtárába telepít, a robot rendszer-ROS-át nem írja át.

Az aktív Gazebo-vezérlő C++ ROS 2 node-ja, az akadálykövető Python segédnode; a teljes Gazebo launch nem futtatható közvetlenül a roboton, mert Gazebót indít, TurtleBot-paramétereket olvas ki, és `use_sim_time:=true` beállítást használ. A cél a robot saját bringupjának, lokalizációjának és driverének használata. A ROSboton való működés még **nincs hardveren igazolva**; előbb ellenőrizni kell, hogy a meglévő Foxy-környezet tartalmazza-e az adott források fordításához és futtatásához szükséges függőségeket.

## Adatút és szükséges interfészek

| Adat | Téma / keret | Szerepe |
|---|---|---|
| 2D LiDAR-mérés | `/scan` (`sensor_msgs/LaserScan`) | Bemenet az akadálydetektáláshoz; a scan `frame_id`-jéből TF kell az odometria keretébe. |
| Kerék-odometria | `/odom` (`nav_msgs/Odometry`) | A robot helyzete és sebessége; a header keretéből TF kell a `/map` által használt térképkeretbe. |
| Térkép és lokalizáció | `/map` és TF `map → odom` | Az A* globális úttervezése és a pozíciók közös térképi keretbe alakítása. A keretek tényleges nevét a roboton ellenőrizni kell. |
| Követett akadályok | `/tracked_obstacles` (`sensor_msgs/PointCloud2`) | A LiDAR-node az akadálypontokhoz pozíciót és becsült sebességet ad az odometria keretében. |
| Cél | `/goal_pose` (`geometry_msgs/PoseStamped`) | Térképi célpont, például RViz 2D Goal Pose eszközéből. |
| Hajtásparancs | `/cmd_vel` (`geometry_msgs/Twist`) | A vezérlő lineáris és szögsebesség-parancsa, amelyet a ROSbot saját drivere fogad. |

A ROSbot gyári bringupja adja a LiDAR-t, az odometriát, a TF-et és a `/cmd_vel` fogadását. A `lidar_obstacle_node` a `/scan` adatot klaszterezi és a sebességet két egymást követő mérésből becsüli; ez a becslés nem mozgáskövető hardveres garancia, és a jelenlegi 0,35 m/s feletti sebesség-értékeket nullázó szabályt valós LiDAR-adatokon validálni kell. A vezérlő a térképet globális útvonalhoz, a LiDAR-követő pontfelhőjét pedig lokális akadályelkerüléshez használja.

## Lépésről lépésre

### 1. Rögzítsd a már telepített környezetet

Jegyezd fel a ROSbot 2 gyári rendszerének ROS 2 Foxy setup fájlját, a LiDAR típusát, a gyári bringup parancsát, a témák és TF-frame-ek nevét. A további parancsokban a rendszer által már biztosított ROS környezetet használd; ne frissítsd és ne cseréld le a robot rendszerét. Készíts szabad, sík tesztterületet, legyen kéznél működő fizikai vészleállító és felügyelő személy; az első próbán ne legyen ember vagy mozgó akadály a robot útjában.

### 2. Ellenőrizd a meglévő függőségeket telepítés nélkül

Töltsd be a roboton már meglévő ROS 2 Foxy környezetet, majd ellenőrizd a fordító- és Python-függőségeket. A hiányzó komponensnél állj meg: ne telepítsd, hanem a meglevő robot-stackhez igazítsd a megvalósítást.

```bash
source /opt/ros/foxy/setup.bash
command -v colcon
command -v c++
ros2 pkg prefix rclcpp
ros2 pkg prefix ament_cmake_python
ros2 pkg prefix geometry_msgs
ros2 pkg prefix tf2_ros
ros2 pkg prefix nav_msgs
ros2 pkg prefix visualization_msgs
python3 -c "import numpy, rclpy, sensor_msgs_py, tf2_ros; print('ROSbot dependencies available')"
```

Ha a Foxy setup más helyen van, a `source` sort a már működő ROSbot bringup termináljából vedd át. A `ros2 pkg prefix` és az importpróba csak ellenőriz; nem telepít semmit. Az `astar_dwa_controller` C++ csomagját építsd a roboton futó Foxyval, ne a fejlesztői Jazzy/Gazebo buildből másold át a binárist. A Gazebo csomagot ne válaszd ki buildre: annak manifestje Gazebo/TurtleBot függőségeket is deklarál, a roboton ezek nem szükségesek.

Egy privát workspace-ben tartsd meg a CMake által elvárt könyvtárszerkezetet:

```text
~/rosbot_ws/src/rosbot_project/Gazebo_ROS2/
├── python_deps/
└── src/
    ├── astar_dwa_controller/
    └── dwa_gazebo_sim/
```

Másold vagy másold át SSH-val a forrásokat ebbe a felhasználói könyvtár alatti struktúrába; a `build/`, `install/` és `log/` könyvtárakat ne vidd át. A projektből a `python_deps`, az `astar_dwa_controller`, valamint a tracker forrása kell. A csomag CMake-fájlja a `python_deps` mappát relatív útvonalon keresi, ezért a szerkezetet ne lapítsd ki. A workspace gyökeréből:

```bash
cd ~/rosbot_ws
source /opt/ros/foxy/setup.bash
colcon build --packages-select astar_dwa_controller
source install/setup.bash
```

Ez a build a C++ vezérlőt a `~/rosbot_ws/install` overlay-be teszi, nem a rendszerbe. Ha a fordítás egy már meglévő Foxy-függőség hiánya miatt megáll, ne telepíts csomagot: rögzítsd a hibát, és a forrást kell a meglévő Foxy API-hoz vagy a már elérhető könyvtárakhoz igazítani.

### 3. Indítsd el a gyári bringupot, még vezérlő nélkül

Indítsd a Husarion által az adott ROSbot-modellhez dokumentált bringupot, és először csak olvasd a szenzorokat. Ellenőrizd külön a témák elérhetőségét és frekvenciáját:

```bash
ros2 topic list
ros2 topic info /scan
ros2 topic info /odom
ros2 topic info /cmd_vel
ros2 topic hz /scan
ros2 topic hz /odom
ros2 topic echo --once /scan
ros2 topic echo --once /odom
```

Ha a robot más neveket használ, például `/rosbot/scan`, jegyezd fel őket; még ne indítsd el a vezérlőt. Az odometria és a LiDAR időbélyegeinek folyamatosan frissülniük kell, a scan tartományainak pedig életszerű értékeket kell mutatniuk.

### 4. Ellenőrizd a TF-et és a koordinátakereteket

Nézd meg a teljes TF-fát, majd ellenőrizd a LiDAR és az odometria keret közötti átalakítást. A frame-neveket a saját üzenetekből vedd, ne másold át vakon a példaneveket:

```bash
ros2 run tf2_tools view_frames
ros2 run tf2_ros tf2_echo odom base_link
ros2 run tf2_ros tf2_echo odom <LIDAR_FRAME>
```

Itt az `odom`, `base_link` és `<LIDAR_FRAME>` helyére a ROSbot tényleges frame-nevei kerüljenek. A LiDAR-node alapértelmezett `tracking_frame` értéke `odom`; ha nálad más az odometria frame-neve, azt majd paraméterként add át. A TF-nek friss szenzor-időbélyegeknél is elérhetőnek kell lennie, különben a node `tf_missing` diagnosztikával kihagyja az adott adatot.

### 5. Készíts vagy tölts be térképet, majd ellenőrizd a lokalizációt

Ha van a teszthelyszínhez illő, ROS 2-kompatibilis mentett térkép, töltsd be a robot disztribúciójának megfelelő lokalizációs rendszerrel; ellenkező esetben térképezd fel a területet, és ments térképet. A használt lokalizációnak a `/map` témát és a térkép–odometria TF-et is biztosítania kell. RViz-ben ellenőrizd, hogy a robot jelölője a valós helyen van, a térkép nem ugrál, és a térképkeret egyezik a célok keretével. Az induló pózt a lokalizációs rendszernek megfelelően állítsd be. **Ne adj célt és ne indítsd a vezérlőt, amíg ez nem stabil.**

### 6. Indítsd el önállóan a LiDAR-akadálykövetőt

Csak a scan és a TF ellenőrzése után indítsd el az akadálykövetőt. Mivel ez a node jelenleg a Gazebo segédcsomag része, a hiányzó Gazebo függőségek miatt ne buildeld a teljes `dwa_gazebo_sim` csomagot. Ha a fenti Python importellenőrzés sikeres, a meglévő Foxy környezetben közvetlenül a forrásból is futtatható, a saját útvonalad behelyettesítésével:

```bash
python3 ~/rosbot_ws/src/rosbot_project/Gazebo_ROS2/src/dwa_gazebo_sim/dwa_gazebo_sim/lidar_obstacle_node.py \
  --ros-args \
  -p use_sim_time:=false \
  -p tracking_frame:=odom
```

Ha más a scan- vagy odometria-téma/frame neve, igazítsd a remapet és a `tracking_frame` értéket. Ellenőrizd a `/tracked_obstacles` témát és a `DIAG_LIDAR` naplókat; a `frame`, `age`, `points`, `clusters`, `motion_fits` és `tf_missing` mezők jelzik, hogy friss adat érkezik-e. Először álló akadállyal ellenőrizz, majd csak biztonságos körülmények között mozgó tárggyal. Ha az importellenőrzés hiányzó Python-csomagot jelez, ne használd a `pip`-et: a következő implementációs lépés a tracker átírása a roboton már meglévő ROS/C++ függőségekre vagy a gyári akadálydetektorra történő illesztése.

### 7. Mérd fel a robotparamétereket, és készíts külön paraméterfájlt

Mérd meg vagy a robot dokumentációjából ellenőrizd a keréksugarat (`r_kerek`), a fél keréktávolságot (`b`), a robot körülíró sugarát (`rob_radius`), a kerék maximális szögsebességét (`w_kerek_max`) és a biztonságosan használható gyorsulást (`a_max`). A Gazebo TurtleBot Waffle-értékei nem tekinthetők ROSbot-beállításnak. A maximális lineáris sebesség közelítőleg `w_kerek_max * r_kerek`; ezért a kezdeti sebességkorlátot alacsonyan válaszd, és ellenőrizd a driver tényleges korlátait is.

Példa `rosbot_dwa.yaml` paraméterfájlra; a `0.0` értékeket **indítás előtt** cseréld a felmért, pozitív és konzisztens értékekre:

```yaml
astar_dwa_node:
  ros__parameters:
    use_sim_time: false
    r_kerek: 0.0
    b: 0.0
    w_kerek_max: 0.0
    a_max: 0.0
    rob_radius: 0.0
    map_inflation_radius: 0.0
    static_safety_margin: 0.03
    safety_margin: 0.15
    dt: 0.1
    predict_time: 3.0
    Alfa: 5.0
    Beta: 2.0
    Gamma: 3.0
    dynamic_clearance_weight: 4.0
    dynamic_clearance_distance: 0.6
```

`map_inflation_radius` legyen legalább a mért robotkörülíró sugár és a választott statikus ráhagyás összege; a dinamikus akadályráhagyás külön paraméter. A fenti súlyok és időértékek a jelenlegi implementáció alapértékei, nem ROSboton igazolt hangolások. A node érvénytelen vagy nulla robotméret-, kerék- és gyorsulásparaméterrel leáll, ezért a mintát kitöltés nélkül ne használd.

### 8. Ellenőrizd a névtereket, majd indítsd el a vezérlőt célt még nem küldve

A forrásban a vezérlő és a tracker abszolút témaneveket használ (`/scan`, `/odom`, `/map`, `/tracked_obstacles`, `/goal_pose`, `/cmd_vel`). Ha a robot például `/rosbot/scan` témát publikál, explicit ROS remap szükséges; ugyanez érvényes a kimeneti `/cmd_vel`-re. A TF frame-neveket nem lehet pusztán témaremapből kijavítani, azoknak a TF-fában is helyesnek kell lenniük. Több robot esetén ügyelj rá, hogy ne ugyanazt a közös `/cmd_vel` témát vezéreljék.

Indítás a paraméterfájllal, példa remap nélkül:

```bash
ros2 run astar_dwa_controller astar_dwa_node --ros-args \
  --params-file ~/rosbot_dwa.yaml \
  -p use_sim_time:=false
```

Ha szükséges, add hozzá a megfelelő `-r /scan:=/rosbot/scan` és hasonló remapeket a saját topicjaidhoz. A node indulása után ellenőrizd a `DIAG_CONFIG`, `DIAG_MAP`, `DIAG_TF_CPP` és `DIAG_CONTROL` sorokat. A `waiting_inputs`, `stale_input`, `tf_missing` vagy `localization_jump` okát előbb javítsd; ne próbáld ezeket gyorsabb célküldéssel vagy a biztonsági logika kikapcsolásával megkerülni. A vezérlő bemenetként térképet, odometriát és akadály-felhőt vár akkor is, ha az akadályok listája üres.

### 9. Végezz fokozatos, felügyelt mozgáspróbát

Elsőként sík, tágas, akadálymentes területen adj közeli célt RViz 2D Goal Pose eszközével, miközben valaki a fizikai vészleállító mellett áll. A sebességkorlátot a paraméterfájlban konzervatív, alacsony értékre állítsd; ellenőrizd az irányt, a megállást, az odometria és a tényleges mozgás egyezését, majd mérd a fékutat. A `/cmd_vel`-re egyszerre csak a DWA vezérlő publikáljon: teleoperátort ne futtass vele párhuzamosan, kivéve ha dokumentált parancs-multiplexert használsz. Hiba, váratlan mozgás, adatkimaradás vagy lokalizációs ugrás esetén azonnal állítsd le a próbát.

Ha az alapmozgás megbízható, külön teszteld az álló akadályt, majd az alacsony sebességű mozgó akadályt, végül ismételd meg a teszteket több indulópozícióval. Minden futásnál rögzítsd a paramétereket, a célbaérést, az időt, a minimális akadálytávolságot, az esetleges megállásokat és a `DIAG_*` naplókat. Az ütközésmentes egyedi futás nem bizonyít általános biztonságot; az eredményeket ismétlésszámmal és korlátokkal együtt közöld.

## Hibakeresési rövid útmutató

| Jelenség | Első ellenőrzés |
|---|---|
| `waiting_inputs` vagy `stale_input` | Érkezik-e friss `/map`, `/odom` és `/tracked_obstacles`; valós idejű órát használnak-e a node-ok; egyeznek-e az időbélyegek. A vezérlő 0,5 s-nál régebbi bemenetet leállással kezel. |
| `tf_missing` | A scan `frame_id`, az odometria kerete, a tracker `tracking_frame` értéke és a TF-ek elérhetősége az üzenetek időbélyegén. |
| `localization_jump` | Térkép–odometria TF, induló póz, lokalizációs stabilitás és óra; ez biztonsági leállás, ne kerüld meg. |
| Nem látszik akadály vagy a sebességbecslés nulla | `/scan` frekvencia/tartomány, LiDAR–odom TF, scan zaj, klaszterek mérete és a `DIAG_LIDAR` sebességbecslése. |
| A robot nem mozdul vagy túl gyors | Csak egy `/cmd_vel` publisher legyen; ellenőrizd a driver parancsformátumát, sebességkorlátját, a mért kerékparamétereket és a `DIAG_CONTROL` eredményét. |
| RViz-ben hibás a cél vagy az út | A cél és a `/map` `frame_id`-je, a map→odom TF és a kezdeti lokalizáció. |

## Mit lehet állítani a dolgozatban?

Az átvitel jelenleg architekturális terv, nem igazolt ROSbot-demonstráció. Hardveres futtatás és mérések nélkül úgy fogalmazz, hogy a csomag **szabványos ROS 2 üzeneteken keresztül integrálható**, és sorold fel a szükséges interfészeket, kalibrálást és biztonsági ellenőrzéseket. Csak elvégzett próbák alapján állítsd, hogy a ROSboton működik vagy biztonságosan kerül akadályt. Jó dokumentációs ábra a Gazebo- és ROSbot-adatút egymás mellett: a vezérlő azonos, de a szenzor-, lokalizációs és hajtásoldali node-ok eltérnek.
