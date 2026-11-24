# A* + DWA átvitele Husarion ROSbotra

## Cél és jelenlegi korlát

Az átültetés célja, hogy a Gazebo helyett a ROSbot adja a szenzoradatokat, és a vezérlő a robot driverén keresztül küldjön sebességparancsokat. Az aktív Gazebo-vezérlő C++ ROS 2 node-ja, az akadálykövető pedig Python segédnode; a teljes Gazebo launch nem használható közvetlenül a roboton, mert Gazebót indít, TurtleBot-paramétereket olvas ki, és `use_sim_time:=true` beállítást használ. A vezérlő hardverfüggetlen ROS-üzenetekkel dolgozik, de a ROSboton való működés még **nem igazolt**: a ROS-verziót, témákat, koordinátakereteket, paramétereket és a hajtás viselkedését a konkrét roboton kell ellenőrizni.

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

### 1. Azonosítsd a robotot és készíts biztonságos teszttervet

Jegyezd fel a ROSbot pontos modelljét és ROS 2 disztribúcióját, a LiDAR típusát, a gyári bringup parancsát, a ROS-témák nevét és a TF-frame-eket. Ellenőrizd a ROS-verzió és a projekt függőségeinek kompatibilitását; a fejlesztői Gazebo-workspace nem feltétlenül telepíthető változtatás nélkül a robot gyári rendszerére. Készíts szabad, sík tesztterületet, legyen kéznél működő fizikai vészleállító és egy felügyelő személy; a kezdeti próbán ne legyen ember vagy mozgó akadály a robot útjában.

### 2. Fordítsd le és ellenőrizd a csomagokat

Építsd az `astar_dwa_controller` és `dwa_gazebo_sim` ROS-csomagot a robot ROS-verziójával kompatibilis workspace-ben, a hiányzó függőségeket annak hivatalos csomagkezelőjével telepítve. A Gazebo launchot ne indítsd el: a fizikai robothoz csak a gyári bringup és a két szükséges node kell. Ha a ROSbot gyári környezete nem teszi lehetővé a csomagok biztonságos telepítését, a fordítást külön, kompatibilis ROS-gépen végezd, majd a workspace-et a dokumentált ROS-módszerrel juttasd el a robotra.

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

Csak a scan és a TF ellenőrzése után indítsd el az akadálykövető node-ot, valós idő használatával:

```bash
ros2 run dwa_gazebo_sim lidar_obstacle_node --ros-args \
  -p use_sim_time:=false \
  -p tracking_frame:=odom
```

Ha más a scan- vagy odometria-téma/frame neve, igazítsd a remapet és a `tracking_frame` értéket a ROSbothoz. Ellenőrizd a `/tracked_obstacles` témát és a node `DIAG_LIDAR` naplóit; a `frame`, `age`, `points`, `clusters`, `motion_fits` és `tf_missing` mezők segítenek eldönteni, hogy valódi, friss adat érkezik-e. Először álló, ismert akadállyal ellenőrizz, majd – a vészleállítót készenlétben tartva – lassan mozgó tárggyal. A sebességbecslés helyességét ne feltételezd pusztán attól, hogy a pontfelhő látszik.

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
