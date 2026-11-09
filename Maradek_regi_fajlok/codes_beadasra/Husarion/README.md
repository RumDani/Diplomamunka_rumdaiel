# Husarion ROSbot – mit kell implementálni

A vezérlő csak szabványos ROS 2 témákat használ, ezért a Gazebo helyett a valós robot drivere adja a bemeneteket. A részletes terv: [HUSARION_ATVITEL.md](HUSARION_ATVITEL.md). Hardveren nem tesztelt.

## Változatlanul átvehető (ebben a mappában)
- `reference_controller.cpp`, `reference_planner.hpp`, `path_tracking.hpp` – A* + DWA vezérlő (`astar_dwa_node`)
- `lidar_obstacle_node.py` – akadályfelismerés és -követés a `/scan` alapján

## A robot adja (nem kell megírni)
- `/scan` (LiDAR), `/odom` + TF `odom -> base_link`, `/cmd_vel` fogadása

## Amit el kell készíteni
1. **Bringup launch fájl:** a ROSbot driver + LiDAR, majd `lidar_obstacle_node` és `astar_dwa_node` indítása Gazebo nélkül, `use_sim_time:=false`-szal.
2. **Lokalizáció:** `slam_toolbox` (localization mód) vagy AMCL a mentett térképpel, kezdőpozíció megadásával (`map -> odom` TF).
3. **Remap / névterek:** `/scan`, `/odom`, `/cmd_vel` és a TF-keretnevek (`base_link`, `odom`, LiDAR-keret) illesztése a robot névteréhez (pl. `/rosbot/...`).
4. **Paraméterek:** a valós robot sugara, kerékátmérője, nyomtávja, max. sebessége/gyorsulása, LiDAR-eltolás és -tartomány (a mostani értékek a TurtleBot Waffle modellből jönnek).
5. **Hangolás:** az akadálykövetés küszöbei (0,15 m csoportosítás, 0,35 m/s sebességkorlát) és a DWA súlyok a valós zajhoz.
6. **Biztonság:** kezdetben alacsony sebesség, vészleállító, mért késleltetés.

A szimulációs `python_simulation_node.py` valós robotnál nem kell: a robot odometriáját közvetlenül használjuk.
