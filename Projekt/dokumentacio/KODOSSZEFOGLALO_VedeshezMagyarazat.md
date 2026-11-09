# Kódösszefoglaló a védéshez (tömören)

## 1. A teljes rendszer egy mondatban
A robot **tudja, hol van a fal** (térkép), az **A\*** kitalálja a legrövidebb szabad utat a célig, a **DWA** pedig ezen az úton, lépésről lépésre, a mozgó akadályokat kikerülve vezeti. Két megvalósítás van: egy **Python 2D** (matematikai, gyorsan kipróbálható) és egy **ROS 2 + Gazebo** (valósághoz közeli, ez kerül a Husarion robotra).

## 2. Három fogalom
| Fogalom | Mit csinál | Hétköznapi kép |
|---|---|---|
| **A\*** | Rácson (cellák) megkeresi a legrövidebb szabad utat. Költség = eddigi út + becslés a célig (heurisztika). | Navigáció: térkép alapján útvonal. |
| **Waypoint** | Az útból 0,2 m-enként vett célpontok. | Útközbeni „következő sarokpont". |
| **DWA** | Kipróbál sok lehetséges kerékpár-sebességet, 3 s-ra előre szimulálja, kiszűri az ütközőket, a legjobb pontszámút választja. | Vezetés: „most merre és mennyire gyorsan, hogy ne menjek neki semmihez". |

DWA pontszám: `Alfa·irány + Béta·akadálytávolság + Gamma·sebesség` (alap 5 / 2 / 3). Béta nélkül (0) a robot ütközik (súlyvizsgálat), a sebesség túlzott súlya is rontja a biztonságot.

**Felbontás (`resolution`)**: egy rácscella oldala méterben. 0,2 m → a (2, 3) cella középpontja x = 0,7 m, y = 0,5 m. A Gazebo-térkép felbontása 0,1 m.

## 3. Python_szimulacio – melyik fájl miért van
| Fájl | Miért van rá szükség |
|---|---|
| `simulation.py` | Ezt indítod. Beállítóablak, pálya (falak, mozgó akadályok), animáció. |
| `DWA+A.py` | Összeköti a kettőt: A* út → waypointok → a DWA a soron következőt célozza. |
| `DWA.py` | A helyi, valós idejű döntés: sebességminták, ütközésszűrés, pontozás. |
| `robot.py` | A robot „fizikája": differenciális kormányzás, gyorsulási korlát, méret, paraméterek. |
| `astar_project/grid_map.py` | A világ rácsként: méter ↔ cella átváltás, akadályok, **felfújás** (a robot méretével növelt akadály, hogy a pont-robot is biztonságos legyen). |
| `astar_project/astar_baseline.py` | Maga az A* (8 irány, átlós költség √2). |
| `astar_project/astar_variants.py` | Heurisztikák (Manhattan, euklideszi, Csebisev, oktilis) az összehasonlításhoz. |
| `astar_project/path_smoothing.py` | Az éles sarkok Bézier-lekerekítése, hogy a robot simán tudjon menni. |
| `sulyvizsgalat/dwa_weight_sweep.py` | A DWA súlyainak szisztematikus vizsgálata (eredmény: `DWA_SULYVIZSGALAT.md`). |

## 4. Gazebo_ROS2 – rövid áttekintés
**`astar_dwa_controller` (C++, az „agy"):**
| Fájl | Miért van |
|---|---|
| `reference_controller.cpp` | A ROS 2 node (`astar_dwa_node`): fogadja a térképet, pozíciót, akadályokat, célt; tervez; 10 Hz-en `/cmd_vel`-t küld. Ha adat elavult (`stale_input`), leáll. |
| `reference_planner.hpp` | A* a rácson, útsimítás, 0,2 m-es újramintavételezés, DWA mintavételezés és pontozás. |
| `path_tracking.hpp` | Útkövetés: a robot helyét az útra vetíti, és 0,35–0,8 m-es (sebességfüggő) **előretekintéssel** választja a célpontot. |
| `rviz/astar_dwa.rviz` | RViz nézet: térkép, zöld A* út, akadályok. |

**`dwa_gazebo_sim` (a szimuláció és az illesztés):**
| Fájl | Miért van |
|---|---|
| `launch/simulation.launch.py` | Egy paranccsal elindít mindent (Gazebo, híd, SLAM, node-ok). |
| `launch/visualization.launch.py` | RViz indítása. |
| `worlds/dwa_world.sdf` | A világ: falak, fix akadályok, két mozgó akadály, TurtleBot3. |
| `config/slam.yaml` | SLAM beállítások (0,1 m felbontás, 3 m lidar). |
| `lidar_obstacle_node.py` | A lidar-pontokból akadályokat csinál, követi őket, és **sebességet becsül** → így tud a DWA mozgó akadályt kikerülni. |
| `python_simulation_node.py` | Gazebo-illesztés: kerékodometriából `/odom`, kezdőpozíció-eltolás, TF, mozgó akadályok indítása. |
| `python_world.py` | Indítás előtt módosítja a világfájlt (pozíció-odometria, keresztező akadály). |
| `python_reference.py` | A világfájlból rácstérképet készít a tervezőnek. |
| `gazebo_path_node.py` | A tervezett utat kirajzolja magában a Gazebóban. |

### Adatfolyam röviden
`Gazebo` → `/scan`, odometria → `slam_toolbox` (térkép + `map→odom`) és `lidar_obstacle_node` (`/tracked_obstacles`) → `astar_dwa_node` (A* + DWA) → `/cmd_vel` → Gazebo.
Cél megadása: RViz „2D Goal Pose" vagy `/goal_pose`. A node tervez, publikálja az utat (`/astar_path`), majd vezet, és `DIAG_CONTROL cpp reason=finished` jelzi a célba érést.
## 5. Gazebo_ROS2 – részletes fájlmagyarázat

A Gazebo-megvalósítás a `Projekt/Gazebo_ROS2/src/` alatti két ROS 2 csomagból áll. Az `astar_dwa_controller` végzi a tervezést és a robot vezérlését; a `dwa_gazebo_sim` biztosítja a Gazebo-világot, a szenzoradatok ROS 2-es feldolgozását és a megjelenítést.

### Mit jelent a `.hpp` kiterjesztés?

A `.hpp` C++ fejlécfájlt jelöl. A fejlécet egy vagy több `.cpp` forrásfájl be tudja emelni a `#include` utasítással. Gyakran deklarációk és típusok kerülnek bele, de ebben a projektben a `reference_planner.hpp` és a `path_tracking.hpp` az algoritmusok megvalósítását is tartalmazza. Nem önálló ROS 2 node-ok: a `reference_controller.cpp` használja a bennük lévő függvényeket. A `#pragma once` megakadályozza, hogy ugyanaz a fejléc egy fordítási egységben többször kerüljön feldolgozásra.

### `astar_dwa_controller` – C++ tervező és vezérlő

- **`src/reference_controller.cpp` – a ROS 2 node.** Az `astar_dwa_node` feliratkozik a `/map`, `/odom`, `/tracked_obstacles` és `/goal_pose` témákra. A térképet és a szenzoradatokat a TF transzformációk figyelembevételével dolgozza fel. Új cél érkezésekor útvonalat számol, majd a 0,1 másodpercenként futó vezérlési ciklusban kiválasztja a következő követendő pontot és meghívja a DWA-tervezőt. A `/cmd_vel` témán sebességparancsot, az `/astar_path` témán a globális utat publikálja. A hiányzó vagy elavult bemenet, érvénytelen cél, illetve sikertelen úttervezés esetén nulla sebességparanccsal állítja meg a robotot.
- **`src/reference_planner.hpp` – rács, A* és DWA.** Ez a fejléc tartalmazza a tervezés fő algoritmusait és adattípusait. A `Grid` az occupancy grid celláit kezeli, akadályfelfújást és biztonsági ellenőrzést végez; az A* nyolc irányban keres, átlós lépésnél ellenőrzi a sarokütközést is. A talált út simítása után a kód nagyjából 0,2 méterenként waypointokra mintavételezi azt. A `optimise()` függvény keréksebesség-jelölteket állít elő, előre szimulálja a robot és a mozgó akadályok helyzetét, elveti az ütköző vagy fékezéssel nem biztonságos jelölteket, majd pontozással kiválasztja a megfelelő parancsot. Ez a fájl tehát nem pusztán deklarálja, hanem meg is valósítja a tervező működését.
- **`src/path_tracking.hpp` – útkövetési segédfüggvények.** A robot aktuális helyét a globális út szakaszaira vetíti, kiszámítja az út menti előrehaladást és az úttól való távolságot, majd sebességfüggő, 0,35–0,8 méteres előretekintési célt választ. A fejlécben szereplő ütközési pálya- és jelölt-összehasonlító függvényeket a DWA is használja. Ez az algoritmikus segédmodul nem indít node-ot, és nem küld ROS-üzenetet.
- **`rviz/astar_dwa.rviz` – megjelenítési beállítás.** Meghatározza, milyen ROS-témákat és koordináta-keretet mutasson az RViz, például a térképet, a tervezett utat és az akadályokat.
- **`CMakeLists.txt` és `package.xml` – fordítás és csomagfüggőségek.** A CMake lefordítja a C++ node-ot és telepíti az RViz-beállítást; a csomagleíró tartalmazza a ROS 2-es függőségeket.

### `dwa_gazebo_sim` – szimuláció és ROS 2 illesztés

- **`launch/simulation.launch.py` – az indítás vezérlése.** Kiolvassa a TurtleBot Waffle modellből a kerék-, méret- és LiDAR-paramétereket, előkészíti a futásidejű világot, majd elindítja a Gazebót, a `ros_gz_bridge`-et, a SLAM/localizációs node-ot, a C++ vezérlőt és a LiDAR-akadálykövetőt. A `slam_mode` lehet térképezés (`mapping`) vagy mentett térképen lokalizálás (`localization`); a `start_planner:=false` lehetővé teszi a kézi térképezést vezérlő nélkül. A `launch/visualization.launch.py` ettől külön az RViz-t indítja.
- **`worlds/dwa_world.sdf` – a Gazebo pályaleírása.** SDF formátumban írja le a világot: a talajt, a határoló falakat, a rögzített és mozgó akadályokat, valamint a TurtleBot modellt és annak fizikai/szenzoros tulajdonságait.
- **`config/slam.yaml` – SLAM paraméterek.** A `slam_toolbox` beállításait tárolja; többek között a térkép 0,10 méteres felbontását és a LiDAR 3 méteres használati hatótávolságát.
- **`dwa_gazebo_sim/lidar_obstacle_node.py` – LiDAR-alapú akadálykövetés.** A `/scan` méréseket a TF segítségével az `odom` keretbe alakítja, a közeli pontokat csoportokba rendezi, majd egymást követő szkenek alapján hely- és sebességbecslést készít. A pontfelhőt `/tracked_obstacles` témán küldi tovább; ezt használja a C++ DWA az akadályok jövőbeli helyzetének becslésére. A túl nagy sebességbecslést a node nullázza, hogy a zajos mérés ne minősítsen falat mozgó akadálynak.
- **`dwa_gazebo_sim/python_simulation_node.py` – szimulációs adapter.** A Gazebo kerékodometriáját `/odom` formában továbbítja a tervezőnek, közzéteszi a szükséges dinamikus és statikus TF kapcsolatokat, figyeli a vezérlő aktív állapotát, és a beállított feltételek teljesülésekor sebességparanccsal elindítja a mozgó akadályokat. A robot mozgatását nem ez a node végzi: azt a C++ vezérlő `/cmd_vel` parancsa és a Gazebo DiffDrive hajtása végzi.
- **`dwa_gazebo_sim/python_world.py` – futásidejű SDF-módosítás.** A TurtleBot modell másolatához hozzáadja a Gazebo világpozícióját publikáló odometria-bővítményt; igény szerint a keresztező akadályt vagy a nem használt kamerát is kezeli. Az eredeti telepített robotmodell helyett a launch egy ideiglenes, módosított SDF-et ad át a Gazebónak.
- **`dwa_gazebo_sim/python_reference.py` – pálya- és térképsegéd.** Beolvassa a világ SDF-fájlját, a falak és a robot indulóhelyzete alapján rácstérképet készít, és akadálymintákat állít elő. Emellett megtartja a Python-szimuláció jeleneteinek ROS-os másolatát, amelyet az adapter használ az akadályok és a kezdőhely beállításához.
- **`dwa_gazebo_sim/gazebo_path_node.py` – Gazebo-beli útvonalrajzolás.** Az `/astar_path` üzenetet a Gazebo világkoordinátáihoz igazítja, majd a Gazebo modellkezelő szolgáltatásaival zöld vonalként megjeleníti a padlón. Ez kizárólag vizuális visszajelzés, nem módosítja a navigáció vagy a robot pozícióját.
- **`setup.py`, `setup.cfg`, `package.xml` és `resource/` – Python ROS 2 csomagolás.** Telepítik a Python modulokat, és regisztrálják a `python_simulation_node` és `lidar_obstacle_node` futtatható ROS 2 parancsokat.

### A Gazebo-futás adatútja

1. A Gazebo szimulálja a robotot és a környezetet; a `/scan` LiDAR-adatot és a kerékodometriát a `ros_gz_bridge` teszi elérhetővé ROS 2-ben.
2. A `slam_toolbox` a LiDAR-t és az odometriát használva térképet, illetve `map→odom` transzformációt állít elő. Térképezéskor új térképet épít; lokalizációkor a korábban mentett térképen határozza meg a helyzetet.
3. A `lidar_obstacle_node` a szkenből akadálypontokat és sebességbecsléseket készít, majd `/tracked_obstacles` témán publikálja őket.
4. Az RViz-ben megadott `/goal_pose` célból a `reference_controller.cpp` a `/map` alapján A* útvonalat tervez. A `/astar_path` útvonalat és a megjelenítéshez felfújt `/astar_map` térképet is közzéteszi.
5. A vezérlési ciklus az odometria, az előretekintési cél és a követett akadályok alapján a `reference_planner.hpp` DWA-jával választ biztonságos keréksebességet, majd `/cmd_vel`-en a Gazebo DiffDrive hajtásának küldi.
6. A `python_simulation_node` a mozgó akadályokat vezérli; a `gazebo_path_node.py` az útvonalat csak megjeleníti. Sikeres célba éréskor a vezérlő naplójában a `DIAG_CONTROL cpp reason=finished` sor jelenik meg.

## 6. Várható kérdések és rövid válaszok
- **Miért A\* és miért DWA?** Az A* globálisan optimális, de statikus térképen; a DWA lokálisan, dinamikus akadályokat kezel. A kettő együtt adja a teljes navigációt.
- **Miért kell felfújt akadály?** A tervező a robotot ponttal modellezi; a felfújás a valós méretet és a biztonsági sávot adja.
- **Miért van Python és Gazebo is?** A Python gyors, paraméterezhető kísérletekhez (súlyvizsgálat); a Gazebo/ROS 2 ugyanazt a logikát a valós robotarchitektúrával (SLAM, TF, lidar) teszteli.
- **Mi volt a súlyvizsgálat fő tanulsága?** Béta = 0 → mindig ütközés; β 2 és 6 azonos; az 5/2/3 alap ütközés nélkül ért célba mindkét helyzetben.
- **Miért kell előretekintés?** Hogy a robot ne a legközelebbi, hanem egy kicsit előrébb lévő pontot kövesse, így simán halad, nem rángat.
- **Mi a SLAM?** A robot egyszerre épít térképet és határozza meg benne a helyét; mentés után csak lokalizál a mentett térképen.

*Részletesebb, függvényenkénti magyarázat: `KODMAGYARAZATOK.md`; sweep: `DWA_SULYVIZSGALAT.md`.*
