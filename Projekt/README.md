# Projekt – fájlok és működésük

Két, egymástól független rész van, mindkettő ugyanazt az ötletet valósítja meg: az **A\*** globális utat tervez, a **DWA** (Dynamic Window Approach) ezen az úton vezeti a robotot, és kikerüli a mozgó akadályokat.

```
Projekt/
├── Python_szimulacio/   Python 2D (matematikai) szimuláció   → README.md az indításhoz
├── Gazebo_ROS2/         ROS 2 + Gazebo szimuláció            → README.md az indításhoz
└── dokumentacio/        jegyzetek (kódmagyarázat, tapasztalatok, Husarion-átvitel)
```

## 1. Python_szimulacio\codes_diploma\
| Fájl | Mit csinál |
|---|---|
| `simulation.py` | Indító és megjelenítő: felépíti a pályát (30×20 cella, 0,2 m, falak, két mozgó akadály), animálja a robotot. |
| `DWA+A.py` | A* és DWA összekapcsolása: az A* útból 0,2 m-enkénti waypointokat készít, a robot a soron következőt célozza. |
| `DWA.py` | DWA: kiválasztja a lehetséges kerékszögsebesség-párokat, kiszűri az ütközőket, pontoz: `Alfa·irány + Béta·akadálytávolság + Gamma·sebesség`. |
| `robot.py` | Robotmodell: differenciális kinematika, gyorsulási korlát, paraméterek (`robotconfig`), állapot, akadály, cél. |
| `astar_project\astar_baseline.py` | A* keresés rácson, 8 irányban (átlós √2 költség). |
| `astar_project\astar_variants.py` | Heurisztikák: Manhattan, euklideszi, Csebisev, oktilis. |
| `astar_project\grid_map.py` | Rácstérkép: koordináta ↔ cella átváltás, akadályok, felfújás a robotméret miatt, szomszédok. |
| `astar_project\path_smoothing.py` | Az A* éles sarkainak lekerekítése Bézier-görbékkel. |
| `sulyvizsgalat\dwa_weight_sweep.py` + `.csv` | DWA paraméter-sweep és eredménye. |

## 2. Gazebo_ROS2\src\astar_dwa_controller\ (C++ vezérlő)
| Fájl | Mit csinál |
|---|---|
| `src\reference_controller.cpp` | A vezérlő ROS 2 node-ja (`astar_dwa_node`): fogadja a térképet, odometriát, akadályokat, célt; A*-gal tervez; `/cmd_vel`-t küld. |
| `src\reference_planner.hpp` | A* a rácson, az út 0,2 m-es újramintavételezése, DWA pontozás, kerékparancsok. |
| `src\path_tracking.hpp` | Útkövetés: a robotot az útra vetíti, az előretekintési távolsággal (0,35–0,8 m) célpontot választ. |
| `rviz\astar_dwa.rviz` | RViz beállítás (térkép, út, akadályok). |
| `CMakeLists.txt`, `package.xml` | Build; telepíti az RViz fájlt és a `python_deps` fájljait. |

## 3. Gazebo_ROS2\src\dwa_gazebo_sim\ (szimuláció)
| Fájl | Mit csinál |
|---|---|
| `launch\simulation.launch.py` | Mindent elindít: Gazebo, híd, slam_toolbox, odometria-node, akadálykövető, vezérlő. |
| `launch\visualization.launch.py` | RViz indítása. |
| `worlds\dwa_world.sdf` | Gazebo világ: falak, fix akadályok, két mozgó akadály, TurtleBot3 Waffle. |
| `config\slam.yaml` | SLAM beállítások (felbontás 0,1 m, lidar-hatótáv 3 m, hurokzárás). |
| `dwa_gazebo_sim\lidar_obstacle_node.py` | Akadályfelismerés: a `/scan` pontjait 0,15 m-es csoportokba rendezi, követi, sebességet becsül (`/tracked_obstacles`). |
| `dwa_gazebo_sim\python_simulation_node.py` | Gazebo-illesztés: kerékodometria → `/odom` kezdőpozíció-eltolással, TF, mozgó akadályok indítása. |
| `dwa_gazebo_sim\python_world.py` | A világfájl módosítása indítás előtt (odometria-bővítmény). |
| `dwa_gazebo_sim\python_reference.py` | Rácstérkép készítése a világfájlból. |
| `dwa_gazebo_sim\gazebo_path_node.py` | A tervezett út megjelenítése a Gazebóban. |
| `setup.py`, `setup.cfg`, `package.xml`, `resource\` | A Python csomag telepítése és a node-ok regisztrálása. |

## Adatfolyam a Gazebóban
`Gazebo → /scan, wheel_odom → híd` → `slam_toolbox` (térkép, `map→odom`), `lidar_obstacle_node` (`/tracked_obstacles`), `python_simulation_node` (`/odom`) → `astar_dwa_node` (A* + DWA) → `/cmd_vel → híd → Gazebo`.
