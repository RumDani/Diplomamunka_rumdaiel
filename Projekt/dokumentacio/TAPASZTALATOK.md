# Tapasztalatok – A* + DWA ROS 2 / Gazebo

Rövid összefoglaló a dokumentáláshoz. Részletek: `KODMAGYARAZATOK.md` (17–20. fejezet).

## Rendszer
- ROS 2 Jazzy (WSL), Gazebo, TurtleBot Waffle, mentett SLAM-térkép (`slam_toolbox`, lokalizációs mód).
- Adatfolyam: `/scan` → `lidar_obstacle_node` (klaszterezés, követés) → `/tracked_obstacles`; a vezérlő `/odom`, `/map`, `/tracked_obstacles` alapján A* utat tervez, DWA-val követi, kimenet `/cmd_vel`.
- A vezérlő forrása: `astar_dwa_controller/src/reference_controller.cpp`.

## Tapasztalt problémák és okok
| Tünet | Ok | Javítás |
|---|---|---|
| Elakadás, helyben forgás, `lookahead=0` | `prune_lookahead` a vetületre állította a célt, ha nem volt elérhető előretekintési pont | célpont: `along_path(lookahead)` |
| Nincs megengedett DWA-parancs | minden jelölt ütközik | biztonságos helyben forgás tartalék |
| Fal mozgó akadálynak látszik | zajos sebességbecslés a falpontokon | statikus térképpontok egyesítése, 0.35 m/s feletti becslés = statikus |
| `localization_jump` (3.4 m) | SLAM-lokalizáció ugrása | biztonsági leállás, kezdőpozíció pontos megadása |
| Nem érhető el a `/goal_pose` | a feliratkozó ~40 s után él | a cél küldését ismételni kell |
| Régi szimuláció zavar | Ctrl+C után megmarad a `gz sim` szerver | PID alapján leállítani |

## Eredmény
Cél `(6.5, 4.2)`, szembejövő `(6.8, 2.0)` és oldalról érkező akadállyal: mindkettő elindult, a kikerülés látható (`avoidance_priority=1`), a futás `reason=finished`-del végződött. A valós idejű tényező ~0.1–0.2, egy futás 2–4 perc.

## Korlátok és valós robot
- Csak szimulációban igazolt; hardveren nem tesztelt, a futások száma kevés (statisztika nincs).
- Át kell hangolni: LiDAR-zaj, küszöbök, robotparaméterek, késleltetés (`stale_input`).
- Kell hardveres vészleállító; a kikerülés nem garantált minden esetben.
- A ROS-témák szabványosak, ezért a kód átvihető (`/scan`, `/odom`, `/map`, `/cmd_vel`).

## Ötletek a diplomamunkához (a dokumentumot nem módosítottam)
- **Ábrák:** TF-fa (`ros2 run tf2_tools view_frames`), `rqt_graph`, RViz-kép az útról és az akadályokról, útvonal-idősor (x,y) a naplóból.
- **Mérések:** idő a célig, minimális akadálytávolság, elakadások száma, több futás ismételve (pl. 5), a javítás előtti és utáni eset összevetése.
- **Fejezetek:** hibaelemzés (a fenti táblázat), korlátok és valós robotra átvitel, jövőbeli munka (hardveres teszt, több dinamikus akadály, időzítésmérés).
- **Reprodukálhatóság:** a README indítási lépései, a használt paraméterek, a napló kulcssorai (`DIAG_GOAL`, `DIAG_SCENARIO`, `DIAG_CONTROL`).

## Javasolt további fájlrendszer-tisztítás (jóváhagyásra vár)
- Archívumba vagy törlésre: `s (5).pdf`, `DOLGOZAT_KOD_AUDIT.md`, `Önlab`, `tanulmanyok_letoltva`, régi `astar_project`, a gyökérszintű `DWA.py`, `DWA+A.py`, `robot.py`, `simulation.py`.
- Megmaradó mag: `codes_diploma/ros2_astar_dwa_gazebo`, ez a dokumentum, `KODMAGYARAZATOK.md`, a `.gv`/ábrafájlok.
