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

## 4. Gazebo_ROS2 – melyik fájl miért van
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

## 5. Adatfolyam (Gazebo)
`Gazebo` → `/scan`, odometria → `slam_toolbox` (térkép + `map→odom`) és `lidar_obstacle_node` (`/tracked_obstacles`) → `astar_dwa_node` (A* + DWA) → `/cmd_vel` → Gazebo.
Cél megadása: RViz „2D Goal Pose" vagy `/goal_pose`. A node tervez, publikálja az utat (`/astar_path`), majd vezet, és `DIAG_CONTROL cpp reason=finished` jelzi a célba érést.

## 6. Várható kérdések és rövid válaszok
- **Miért A\* és miért DWA?** Az A* globálisan optimális, de statikus térképen; a DWA lokálisan, dinamikus akadályokat kezel. A kettő együtt adja a teljes navigációt.
- **Miért kell felfújt akadály?** A tervező a robotot ponttal modellezi; a felfújás a valós méretet és a biztonsági sávot adja.
- **Miért van Python és Gazebo is?** A Python gyors, paraméterezhető kísérletekhez (súlyvizsgálat); a Gazebo/ROS 2 ugyanazt a logikát a valós robotarchitektúrával (SLAM, TF, lidar) teszteli.
- **Mi volt a súlyvizsgálat fő tanulsága?** Béta = 0 → mindig ütközés; β 2 és 6 azonos; az 5/2/3 alap ütközés nélkül ért célba mindkét helyzetben.
- **Miért kell előretekintés?** Hogy a robot ne a legközelebbi, hanem egy kicsit előrébb lévő pontot kövesse, így simán halad, nem rángat.
- **Mi a SLAM?** A robot egyszerre épít térképet és határozza meg benne a helyét; mentés után csak lokalizál a mentett térképen.

*Részletesebb, függvényenkénti magyarázat: `KODMAGYARAZATOK.md`; sweep: `DWA_SULYVIZSGALAT.md`.*
