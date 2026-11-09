# Átvitel Husarion ROSbotra

Ez egy terv és ellenőrzőlista, **hardveren nem tesztelt**. A robotadatokat (típus, szenzor, ROS-verzió, névtér) a konkrét robot dokumentációja alapján kell ellenőrizni.

## Hogyan működne
A vezérlő csak szabványos ROS-témákat használ, ezért a Gazebo helyett a valódi robot drivere adja ugyanazokat:

| Téma | Irány | Valós robotnál |
|---|---|---|
| `/scan` | be | a ROSbot LiDAR-ja (pl. RPLidar/SLAMTEC) |
| `/odom` + TF `odom -> base_link` | be | a robot kerékodometriája (a driver adja) |
| `/map` + TF `map -> odom` | be | `slam_toolbox` lokalizáció vagy AMCL a mentett térképpel |
| `/goal_pose` | be | RViz 2D Goal Pose |
| `/cmd_vel` | ki | a robot drivere hajtja meg a kerekeket |

A `/tracked_obstacles` a `lidar_obstacle_node`-ból jön a `/scan` alapján, ez nem szimulációfüggő.

Menete: robot bringup (a ROSbot saját launch-a: driver, LiDAR, odom, TF) → térkép mentése vagy betöltése → lokalizáció → `lidar_obstacle_node` + vezérlő indítása **a Gazebo nélkül**, `use_sim_time:=false` beállítással → célküldés RViz-ből.

## Mire kell figyelni
1. **Idő:** `use_sim_time` hamis legyen; a Gazebo-launch ezt igaznak állítja. Az óraszinkron (robot és PC) számít, különben `stale_input` leállás jön.
2. **Névterek és témanevek:** a Husarion robotok gyakran névtérben futnak (pl. `/rosbot/...`). Ilyenkor remap kell a `/scan`, `/odom`, `/cmd_vel` témákra, és a TF-keretek nevét (`base_link`, `odom`, a LiDAR-keret) ellenőrizni kell.
3. **Robotparaméterek:** mérd át a valódi robot sugarát, kerékátmérőjét, kerékközét, maximális sebességét és gyorsulását. A jelenlegi értékek a TurtleBot Waffle modellből jönnek. A `config/rosbot.yaml` a régi, inaktív `astar_dwa_node`-hoz tartozik; a használt vezérlő paramétereit külön kell ellenőrizni.
4. **LiDAR:** a pozíciója (`scan_offset`), a látómező, a mérési tartomány és a zaj eltér a szimulációtól. Az akadálykövetés küszöbeit (klaszterezés, 0.35 m/s feletti statikus becslés) újra kell hangolni.
5. **Lokalizáció:** a valós környezet eltér a mentett térképtől. A `localization_jump` biztonsági leállás hasznos, de a kezdőpozíciót pontosan kell megadni (2D Pose Estimate).
6. **Késleltetés:** Wi-Fi és a robot saját számítógépe miatt a bemenetek késhetnek. Mérd a `/scan` és `/odom` korát, és szükség esetén csökkentsd a sebességet.
7. **Biztonság:** hardveres vagy távoli vészleállító legyen kéznél. Az első próbákat emelt kerekekkel vagy nagyon alacsony sebességgel, szabad területen végezd. Mérd a fékezési távolságot.
8. **Sebességkorlát:** kezdd például a szimulációs `0.22 m/s` maximum felével. Ha `0.11 m/s`-nál 1 s a reakció, a robot ~0.11 m-t tesz meg, ez még biztonságos.
9. **Hiányzó teszt:** a szimulációs sikeres futás nem bizonyít semmit a valós működésről. Ismételt mérések kellenek (pl. 5 futás szembejövő akadállyal), mielőtt állítást írsz a dolgozatba.

## Javasolt lépések
1. A robot bringup-ja, és ellenőrizd a témákat: `ros2 topic list`, `ros2 topic hz /scan /odom`, `ros2 run tf2_tools view_frames`.
2. Mentsd a térképet a valós helyről, indítsd a lokalizációt, ellenőrizd RViz-ben a pozíciót.
3. Indítsd a LiDAR-követőt, nézd meg a `/tracked_obstacles`-t álló és mozgó emberrel.
4. Indítsd a vezérlőt alacsony sebességgel, kis célt adj, akadály nélkül.
5. Akadályokkal tesztelj, naplózd a `DIAG_*` sorokat, és hasonlítsd a szimulációhoz.

## Ábraötlet a dolgozathoz
Egy összehasonlító ábra: szimuláció (Gazebo → `/scan`, `/odom`) és valós robot (driver → `/scan`, `/odom`) ugyanazzal a vezérlővel; a különbség csak a forrás és az időkezelés.
