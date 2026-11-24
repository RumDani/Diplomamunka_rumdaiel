# AI-kódcsomag – átadás a Projekt jelenlegi forrásaiból

Generálva: 2026-11-24

Ez a fájl a `Projekt/` könyvtár fontos, szöveges forrásait egyetlen átadható dokumentumba gyűjti. A teljes kódtörzseket alább találod fájlútvonal szerint, így önállóan is továbbadható egy másik AI-nak.

## Átadási tudnivalók

- A snapshot a generáláskor a helyi munkafában lévő állapotot tükrözi, ezért a forrásokban lehetnek még nem commitolt változások.
- Benne vannak az aktív Python-szimuláció, a ROS 2/Gazebo csomagok, a konfigurációk, a tesztek, a README-k és a kapcsolódó Markdown dokumentáció.
- A `build/`, `install/`, `log/`, `results/`, `__pycache__/` könyvtárak, binárisok, ábrák és táblázatfájlok nincsenek beágyazva. A mérési CSV-k viszont bekerülnek, ha a projektforrás részei.
- A `Maradek_regi_fajlok/` archívum és a diplomamunka DOCX/PDF fájlja nincs ebben a kódcsomagban; a dolgozat szövegét külön add át, ha az AI-nak a megfogalmazást is folytatnia kell.
- A dokumentációban szereplő személyes, abszolút workspace-útvonalak `<WORKSPACE>` jelölésre vannak cserélve. A másik gépen ezt a saját projektútvonalra kell cserélni.
- A Gazebo vezérlés aktív implementációját a C++ ROS 2 csomagban keresd; a Python szimuláció külön, referencia-/összehasonlító megvalósítás. A roboton való fizikai tesztet ne tekintsd elvégzettnek, ha nincs erre kifejezett mérési bizonyíték.

## Tartalomjegyzék

- `Projekt/dokumentacio/DWA_SULYVIZSGALAT.md`
- `Projekt/dokumentacio/DWA_SULYVIZSGALAT_ROVID.csv`
- `Projekt/dokumentacio/HUSARION_ATVITEL.md`
- `Projekt/dokumentacio/KODMAGYARAZATOK.md`
- `Projekt/dokumentacio/KODOSSZEFOGLALO_VedeshezMagyarazat.md`
- `Projekt/dokumentacio/TAPASZTALATOK.md`
- `Projekt/Gazebo_ROS2/env.sh`
- `Projekt/Gazebo_ROS2/python_deps/astar_project/__init__.py`
- `Projekt/Gazebo_ROS2/python_deps/astar_project/grid_map.py`
- `Projekt/Gazebo_ROS2/python_deps/robot.py`
- `Projekt/Gazebo_ROS2/README.md`
- `Projekt/Gazebo_ROS2/src/astar_dwa_controller/CMakeLists.txt`
- `Projekt/Gazebo_ROS2/src/astar_dwa_controller/package.xml`
- `Projekt/Gazebo_ROS2/src/astar_dwa_controller/rviz/astar_dwa.rviz`
- `Projekt/Gazebo_ROS2/src/astar_dwa_controller/src/path_tracking.hpp`
- `Projekt/Gazebo_ROS2/src/astar_dwa_controller/src/reference_controller.cpp`
- `Projekt/Gazebo_ROS2/src/astar_dwa_controller/src/reference_planner.hpp`
- `Projekt/Gazebo_ROS2/src/astar_dwa_controller/test/test_path_tracking.cpp`
- `Projekt/Gazebo_ROS2/src/dwa_gazebo_sim/config/slam.yaml`
- `Projekt/Gazebo_ROS2/src/dwa_gazebo_sim/dwa_gazebo_sim/__init__.py`
- `Projekt/Gazebo_ROS2/src/dwa_gazebo_sim/dwa_gazebo_sim/gazebo_path_node.py`
- `Projekt/Gazebo_ROS2/src/dwa_gazebo_sim/dwa_gazebo_sim/lidar_obstacle_node.py`
- `Projekt/Gazebo_ROS2/src/dwa_gazebo_sim/dwa_gazebo_sim/python_reference.py`
- `Projekt/Gazebo_ROS2/src/dwa_gazebo_sim/dwa_gazebo_sim/python_simulation_node.py`
- `Projekt/Gazebo_ROS2/src/dwa_gazebo_sim/dwa_gazebo_sim/python_world.py`
- `Projekt/Gazebo_ROS2/src/dwa_gazebo_sim/launch/simulation.launch.py`
- `Projekt/Gazebo_ROS2/src/dwa_gazebo_sim/launch/visualization.launch.py`
- `Projekt/Gazebo_ROS2/src/dwa_gazebo_sim/package.xml`
- `Projekt/Gazebo_ROS2/src/dwa_gazebo_sim/resource/dwa_gazebo_sim`
- `Projekt/Gazebo_ROS2/src/dwa_gazebo_sim/setup.cfg`
- `Projekt/Gazebo_ROS2/src/dwa_gazebo_sim/setup.py`
- `Projekt/Gazebo_ROS2/src/dwa_gazebo_sim/worlds/dwa_world.sdf`
- `Projekt/Python_szimulacio/codes_diploma/astar_project/__init__.py`
- `Projekt/Python_szimulacio/codes_diploma/astar_project/astar_baseline.py`
- `Projekt/Python_szimulacio/codes_diploma/astar_project/astar_variants.py`
- `Projekt/Python_szimulacio/codes_diploma/astar_project/grid_map.py`
- `Projekt/Python_szimulacio/codes_diploma/astar_project/path_smoothing.py`
- `Projekt/Python_szimulacio/codes_diploma/DWA+A.py`
- `Projekt/Python_szimulacio/codes_diploma/DWA.py`
- `Projekt/Python_szimulacio/codes_diploma/robot.py`
- `Projekt/Python_szimulacio/codes_diploma/simulation.py`
- `Projekt/Python_szimulacio/codes_diploma/sulyvizsgalat/dwa_weight_sweep.csv`
- `Projekt/Python_szimulacio/codes_diploma/sulyvizsgalat/dwa_weight_sweep.py`
- `Projekt/Python_szimulacio/README.md`
- `Projekt/README.md`

## Fájlok teljes tartalma

### `Projekt/dokumentacio/DWA_SULYVIZSGALAT.md`

````````markdown
# DWA súlyvizsgálat – eredmények
## Módszer

A 2D Python szimulációban (A* + DWA) a DWA pontszámának súlyait változtattam: `pont = α·irány + β·távolság + γ·sebesség`. Két helyzetet futtattam: **S1** – alappálya, **S2** – az alappálya kiegészítve egy keresztező mozgó akadállyal. A futásidő **szimulált idő** (lépésszám · dt, dt = 0,1 s), ezért nem függ a gép sebességétől. Ütközésnek számít, ha a robot és egy akadály távolsága bármelyik lépésben negatív. Összesen 64 eset: α ∈ {2, 5, 8} × β ∈ {0, 2, 6} × γ ∈ {1, 3, 5} (predikciós idő 3 s, biztonsági sáv 0,15 m), továbbá predikciós idő {2, 4} s és biztonsági sáv {0,10; 0,20; 0,25} m az alapsúlyokkal (5/2/3). Maximum 400 lépés (40 s).

## Összesítés

| Helyzet | Esetek | Célba ért | Ütközés nélkül célba ért | Ütközött |
|---|---|---|---|---|
| S1 | 32 | 30 | 18 | 12 |
| S2 | 32 | 30 | 17 | 13 |

## Súlykombinációk (predikciós idő 3 s, biztonsági sáv 0,15 m)

Cellák: eredmény; szimulált idő; legkisebb akadálytávolság (negatív = ütközés).

| α | β | γ | S1 | S2 |
|---|---|---|---|---|
| 2 | 0 | 1 | ÜTKÖZÉS; 23.9 s; -0.27 m | ÜTKÖZÉS; 25.8 s; -0.27 m |
| 2 | 0 | 3 | ÜTKÖZÉS; 23.6 s; -0.27 m | ÜTKÖZÉS; 25.6 s; -0.28 m |
| 2 | 0 | 5 | ÜTKÖZÉS; 23.5 s; -0.27 m | ÜTKÖZÉS; 25.5 s; -0.27 m |
| 2 | 2 | 1 | OK; 25.2 s; 0.07 m | OK; 25.7 s; 0.07 m |
| 2 | 2 | 3 | OK; 27.3 s; 0.03 m | ÜTKÖZÉS; 25.8 s; -0.22 m |
| 2 | 2 | 5 | nem ért célba; 40.0 s; 0.02 m | nem ért célba; 40.0 s; 0.03 m |
| 2 | 6 | 1 | OK; 25.2 s; 0.07 m | OK; 25.7 s; 0.07 m |
| 2 | 6 | 3 | OK; 27.3 s; 0.03 m | OK; 25.9 s; 0.01 m |
| 2 | 6 | 5 | nem ért célba; 40.0 s; 0.02 m | nem ért célba; 40.0 s; 0.03 m |
| 5 | 0 | 1 | ÜTKÖZÉS; 24.5 s; -0.28 m | ÜTKÖZÉS; 26.2 s; -0.27 m |
| 5 | 0 | 3 | ÜTKÖZÉS; 23.7 s; -0.27 m | ÜTKÖZÉS; 25.8 s; -0.27 m |
| 5 | 0 | 5 | ÜTKÖZÉS; 23.7 s; -0.27 m | ÜTKÖZÉS; 25.5 s; -0.27 m |
| 5 | 2 | 1 | OK; 27.4 s; 0.08 m | OK; 27.5 s; 0.10 m |
| 5 (alap) | 2 | 3 | OK; 25.6 s; 0.11 m | OK; 25.4 s; 0.05 m |
| 5 | 2 | 5 | ÜTKÖZÉS; 25.4 s; -0.05 m | ÜTKÖZÉS; 25.0 s; -0.05 m |
| 5 | 6 | 1 | OK; 27.4 s; 0.08 m | OK; 27.5 s; 0.10 m |
| 5 | 6 | 3 | OK; 25.6 s; 0.11 m | OK; 25.4 s; 0.05 m |
| 5 | 6 | 5 | ÜTKÖZÉS; 25.4 s; -0.05 m | ÜTKÖZÉS; 25.0 s; -0.05 m |
| 8 | 0 | 1 | ÜTKÖZÉS; 24.5 s; -0.27 m | ÜTKÖZÉS; 26.4 s; -0.28 m |
| 8 | 0 | 3 | ÜTKÖZÉS; 24.0 s; -0.26 m | ÜTKÖZÉS; 25.7 s; -0.28 m |
| 8 | 0 | 5 | ÜTKÖZÉS; 23.8 s; -0.27 m | ÜTKÖZÉS; 25.9 s; -0.28 m |
| 8 | 2 | 1 | OK; 27.3 s; 0.09 m | OK; 27.5 s; 0.09 m |
| 8 | 2 | 3 | OK; 27.1 s; 0.06 m | OK; 27.1 s; 0.07 m |
| 8 | 2 | 5 | OK; 25.2 s; 0.07 m | OK; 25.5 s; 0.05 m |
| 8 | 6 | 1 | OK; 27.3 s; 0.09 m | OK; 27.5 s; 0.09 m |
| 8 | 6 | 3 | OK; 27.1 s; 0.06 m | OK; 27.1 s; 0.07 m |
| 8 | 6 | 5 | OK; 25.2 s; 0.07 m | OK; 25.5 s; 0.05 m |

## Predikciós idő és biztonsági sáv (α/β/γ = 5/2/3)

| Paraméter | Érték | S1 | S2 |
|---|---|---|---|
| predikciós idő | 2 s | ÜTKÖZÉS; 25.6 s; -0.22 m | ÜTKÖZÉS; 26.6 s; -0.08 m |
| predikciós idő | 3 s | OK; 25.6 s; 0.11 m | OK; 25.4 s; 0.05 m |
| predikciós idő | 4 s | OK; 24.0 s; 0.13 m | OK; 24.9 s; 0.13 m |
| biztonsági sáv | 0.10 m | OK; 24.9 s; 0.03 m | OK; 25.1 s; 0.05 m |
| biztonsági sáv | 0.15 m | OK; 25.6 s; 0.11 m | OK; 25.4 s; 0.05 m |
| biztonsági sáv | 0.20 m | OK; 25.7 s; 0.12 m | OK; 26.7 s; 0.03 m |
| biztonsági sáv | 0.25 m | OK; 28.2 s; 0.05 m | OK; 28.2 s; 0.05 m |

## Értékelés (dolgozatba szánt szöveg)

A súlyvizsgálat célja annak megállapítása volt, mely paraméterek határozzák meg a DWA biztonságos működését. A β (akadálytávolság-súly) a legkritikusabb: **β = 0 esetén mind a 18 futás ütközéssel végződött** mindkét helyzetben (átlagos legkisebb távolság −0,27 m), vagyis akadályérzékelés nélkül a pontozás csak az irányt és a sebességet jutalmazza, és a robot nekimegy az akadályoknak. β = 2 és β = 6 között az eredmény gyakorlatilag azonos (a távolság-pontszám korlátos, ezért telítődik), ezért a β = 2 elegendő. A γ (sebességsúly) növelése rontja a biztonságot, ha az α nem elég nagy: γ = 5 mellett α = 2 esetén a robot nem ért célba, α = 5 esetén ütközött, csak α = 8 mellett volt biztonságos. Vagyis a sebesség jutalmazása az irányítás súlyához viszonyítva számít. Az α = 2 lassúbb, bizonytalanabb haladást ad (több ütközés vagy nem teljesített út), az α = 5–8 megbízhatóbb.

Az alapbeállítás (α/β/γ = 5/2/3, predikciós idő 3 s, sáv 0,15 m) mindkét helyzetben ütközés nélkül célba ért (S1: 25,6 s, 0,108 m; S2: 25,4 s, 0,050 m legkisebb távolság), ezért ez maradt a választott konfiguráció. A 4 s-os predikciós idő valamivel nagyobb távolságot (0,126 / 0,132 m) és rövidebb időt adott, a 2 s-os viszont ütközést okozott, mert a robot későn reagál. A biztonsági sáv növelése nagyobb távolságot ad, de lassabbá teszi a haladást.

*Megjegyzés:* a Gazebo-szimulációban futó C++ vezérlő saját paraméterezésű, ezért ez a vizsgálat a Python 2D szimulációra vonatkozik. Az idő szimulált idő, a futási idő géptől független.
````````

### `Projekt/dokumentacio/DWA_SULYVIZSGALAT_ROVID.csv`

````````csv
Sorszám,α,β,γ,Predikciós idő [s],S1 eredmény,S1 idő [s],S2 eredmény,S2 idő [s]
1,5,0,3,3,ÜTKÖZÉS,23.7,ÜTKÖZÉS,25.8
2,2,2,5,3,nem ért célba,40.0,nem ért célba,40.0
3,5,2,5,3,ÜTKÖZÉS,25.4,ÜTKÖZÉS,25.0
4,5,2,1,3,OK,27.4,OK,27.5
5,5,2,3,3,OK,25.6,OK,25.4
6,5,6,3,3,OK,25.6,OK,25.4
7,5,2,3,4,OK,24.0,OK,24.9
8,8,2,5,3,OK,25.2,OK,25.5
````````

### `Projekt/dokumentacio/HUSARION_ATVITEL.md`

````````markdown
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
````````

### `Projekt/dokumentacio/KODMAGYARAZATOK.md`

````````markdown
---

# `astar_project/grid_map.py`

## 1. A `GridMap` feladata

A `GridMap` kétdimenziós rácstérképet valósít meg az A* algoritmus számára. A folytonos világot kis, négyzet alakú cellákra osztja. Az A* ezeken a cellákon keres útvonalat.

Egy cella állapota:

- `0`: szabad
- `1`: akadály
- `2`: ismeretlen

A rácskoordináta formája `(row, column)`, vagyis `(sor, oszlop)`.

## 2. A konstruktor paraméterei

```python
GridMap(
    width,
    height,
    resolution=0.1,
    origin_x=0.0,
    origin_y=0.0,
    unknown=False,
)
```

- `width`: a térkép szélessége cellákban.
- `height`: a térkép magassága cellákban.
- `resolution`: egy cella fizikai mérete méterben.
- `origin_x`, `origin_y`: a rács kezdőpontja a világkoordináta-rendszerben.
- `unknown`: ha igaz, minden cella kezdetben ismeretlen (`2`); egyébként szabad (`0`).

A szélességnek, magasságnak és felbontásnak pozitívnak kell lennie.

## 3. Mit jelent a `resolution`?

A `resolution` egy cella oldalhosszát jelenti. Például:

```python
resolution = 0.1
```

esetén egy cella `0,1 m x 0,1 m`, azaz `10 cm x 10 cm`.

A teljes fizikai térképméret:

```text
szélesség = width * resolution
magasság  = height * resolution
```

Ezért a következő térkép:

```python
GridMap(width=10, height=6, resolution=0.1)
```

fizikailag `1,0 m x 0,6 m` területet fed le.

Kisebb felbontás részletesebb térképet eredményez, de több cellát és több számítást jelent. Nagyobb felbontás gyorsabb, de pontatlanabb lehet, és keskeny átjárókat vagy kisebb akadályokat elveszíthet.

## 4. A belső rács

A térkép egy `height` sorból és soronként `width` cellából álló listában tárolódik:

```python
self.grid[row][column]
```

Például egy 4 x 3-as térkép kezdetben:

```text
[0, 0, 0, 0]
[0, 0, 0, 0]
[0, 0, 0, 0]
```

A Python-indexelés miatt az első cella `(0, 0)`, az utolsó pedig `(height - 1, width - 1)`.

## 5. Rács- és világkoordináták

A program két koordinátarendszert használ:

- rácskoordináta: `(row, column)`, egész cellaindexekkel;
- világkoordináta: `(x, y)`, jellemzően méterben.

A `column` az `x` irányhoz, a `row` az `y` irányhoz tartozik. A `world_to_grid` és `grid_to_world` függvények fordítanak a két rendszer között.

## 6. `world_to_grid`

```python
column = floor((x - origin_x) / resolution)
row = floor((y - origin_y) / resolution)
```

A függvény megkeresi, hogy egy világkoordinátájú pont melyik cellába esik.

Ha `resolution=0.1`, az origó pedig `(0, 0)`, akkor a `(0.26, 0.14)` pont:

```text
column = floor(0.26 / 0.1) = 2
row    = floor(0.14 / 0.1) = 1
```

Így az eredmény `(1, 2)`. A `floor` azért kell, mert a pontot tartalmazó cella indexét keressük, nem a legközelebbi cellát.

## 7. `grid_to_world`

```python
x = origin_x + (column + 0.5) * resolution
y = origin_y + (row + 0.5) * resolution
```

A függvény egy cella középpontját adja vissza világkoordinátában. A `+0.5` azt jelenti, hogy nem a cella sarkát, hanem a közepét használjuk.

Például `resolution=0.1`, origó `(0, 0)` és cella `(1, 2)` esetén:

```text
x = (2 + 0.5) * 0.1 = 0.25
 y = (1 + 0.5) * 0.1 = 0.15
```

A két átalakítás nem feltétlenül adja vissza ugyanazt a világpontot: a `world_to_grid` egy teljes cellába kerekít, a `grid_to_world` pedig annak középpontját adja vissza.

## 8. Cellák és akadályok

- `is_inside(row, column)`: ellenőrzi, hogy a cella a térképen belül van-e.
- `is_free(row, column)`: akkor igaz, ha a cella a térképen belül van és értéke `0`.
- `add_obstacle(row, column)`: a cellát akadállyá (`1`) teszi.
- `remove_obstacle(row, column)`: a cellát szabaddá (`0`) teszi.
- `mark_free(row, column)`: a vizsgált cellát szabadnak (`0`) jelöli.

A cellán kívüli módosítások `ValueError` kivételt okoznak.

## 9. `add_obstacle_world`

Ez a függvény világkoordinátában megadott akadályt alakít át rácsos akadállyá. Először a középpont celláját keresi meg a `world_to_grid` segítségével, majd a sugár alapján közeli cellákat vizsgál.

A cellák középpontja és az akadály középpontja közötti távolságot számolja. A megfelelően közeli cellákat akadálynak jelöli. A `radius + resolution` feltétel szándékosan kissé konzervatív: biztonsági távolságot is figyelembe vesz.

## 10. `update_from_obstacles`

A függvény több akadályobjektumból frissíti a térképet. Az objektumoktól `x` és `y` attribútumot vár, a `radius` pedig opcionális. Minden akadályt az `add_obstacle_world` dolgoz fel.

## 11. `get_neighbors`

Alapértelmezésben a négy főirány szomszédait vizsgálja:

```text
    fel
bal     jobb
    le
```

`diagonal=True` esetén a négy átlós irány is engedélyezett, így legfeljebb nyolc szomszéd lehet. A függvény csak a pályán belüli és szabad cellákat adja vissza.

Átlós lépésnél külön ellenőrzi a két köztes oldalsó cellát is. Ha például a robot egy sarok körül próbálna átlósan lépni, de a két oldalcellából valamelyik akadály, akkor az átlós lépést elutasítja. Ezzel nem lehet két akadálycellának a közös sarkán átvágni.

## 12. `inflate_obstacles`

```python
grid_map.inflate_obstacles(radius)
```

Ez a függvény a robot mérete miatt biztonsági tartalékot épít a térképbe. Az akadálycellák körüli közeli cellákat is akadálynak jelöli.

Ha a rácsfelbontás `0,2 m`, a robot sugara pedig `0,08 m`, akkor a program egy cellányi környezetet is figyelembe vesz, mert a robot nem matematikai pontként mozog. Az A* így nem olyan útvonalat tervez, amelynek a középvonala ugyan szabad, de a robot széle már hozzáérne az akadályhoz.

Ez a művelet a tervezés előtt módosítja a `GridMap` celláit. A szimulációban ezért a megjelenített szürke akadályterület már a biztonsági zónát is tartalmazza.

## 13. `print_map`

A térkép egyszerű szöveges megjelenítése:

- `.`: szabad cella
- `#`: akadály
- `?`: ismeretlen cella
- `S`: kezdőpont
- `G`: célpont

A `start` és `goal` paraméter csak a kiírást módosítja, a térkép belső állapotát nem.

## 14. Rövid példa

```python
example_map = GridMap(width=10, height=6, resolution=0.1)
example_map.add_obstacle(2, 3)
example_map.print_map(start=(0, 0), goal=(5, 9))
```

Itt a térkép 10 x 6 cellás, minden cella 10 cm x 10 cm, ezért a teljes terület 1,0 m x 0,6 m. A `(2, 3)` cella akadállyá válik.

---

# `astar_project/astar_baseline.py`

## 1. A fájl célja

Az `astar_baseline.py` a klasszikus A* algoritmust valósítja meg a `GridMap` rácstérképén. Ez a projekt referenciaalgoritmusa: először egy egyszerű, ellenőrizhető A* kell, és csak utána érdemes továbbfejlesztett heurisztikákat vagy szomszédsági szabályokat vizsgálni.

Az algoritmus bemenete rácskoordinátákat használ:

```python
start = (sor, oszlop)
goal = (sor, oszlop)
```

A `resolution` itt nem változtatja meg a keresés cellaszintű logikáját. A mozgási költségek cellalépésekben vannak megadva; a világkoordinátákra történő átváltást a `GridMap` végzi.

## 2. Az `astar_search` függvény

```python
astar_search(
    grid_map, start, goal, diagonal=False, return_details=False, heuristic=None
)
```

Paraméterek:

- `grid_map`: a `GridMap` példánya, amely megmondja, mely cellák szabadok.
- `start`: kezdőcella `(row, column)` formában.
- `goal`: célcella `(row, column)` formában.
- `diagonal`: ha `False`, csak a négy főirány használható; ha `True`, az átlós irányok is engedélyezettek.
- `return_details`: ha `False`, csak az útvonalat adja vissza; ha `True`, az útvonal mellett a tervezés közben kibővített cellákat is visszaadja.
- `heuristic`: opcionális, `(position, goal)` paraméterű saját heurisztika. Ha nincs megadva, a `diagonal` értéke alapján Manhattan- vagy Euklideszi-becslés fut.

A visszatérési érték egy cellákból álló lista, például:

```python
[(0, 0), (0, 1), (0, 2)]
```

Az első elem a kezdőcella, az utolsó a célcella. Ha nincs út, a függvény `None` értéket ad vissza. Ha a kezdő- vagy célcella érvénytelen, illetve akadály, `ValueError` keletkezik.

## 3. Az A* alapgondolata

Az A* minden vizsgált cellához költséget rendel:

$$
f(n) = g(n) + h(n)
$$

- `g(n)`: a kezdőtől az aktuális celláig megtett út tényleges költsége.
- `h(n)`: becslés az aktuális cellától a célig.
- `f(n)`: a teljes becsült költség; ezt használja a keresés a következő cella kiválasztására.

A prioritási sor mindig azt a nyitott cellát veszi előre, amelynek a legkisebb `f` értéke van.

## 4. A prioritási sor és az adatszerkezetek

Az egyszerűbb tanulási változat egy sima `open_list` listát használ. A lista elemei:

```python
(f_cost, g_cost, position)
```

Az első érték az `f_cost`, ez alapján keressük meg a következő cellát. A `g_cost` az eddig megtett út költsége, a `position` pedig a cella koordinátája. A kiválasztás így történik:

```python
best_node = min(open_list)
open_list.remove(best_node)
```

Ez könnyebben érthető, mint egy külön prioritási sor használata: végignézzük a listát, kiválasztjuk a legkisebb tuple-t, majd eltávolítjuk.

Két szótár tárolja a keresés állapotát:

- `g_costs`: az ismert legjobb költség a kezdőtől az adott celláig;
- `came_from`: minden elért cellához eltárolja, melyik cellából érkeztünk.

A `came_from` nem a teljes útvonalat tárolja minden lépésnél, hanem szülőkapcsolatokat. Ezután a célból visszafelé követjük ezeket a kapcsolatokat, majd megfordítjuk a listát.

`return_details=True` esetén az A* eredménye ilyen szótár:

```python
{
    "path": [(0, 0), (1, 1), (2, 2)],
    "expanded_nodes": [(0, 0), (0, 1), (1, 1)],
    "search_steps": [
        {
            "current": (0, 0),
            "current_g": 0.0,
            "current_h": 4.0,
            "current_f": 4.0,
            "neighbors": [(0, 1), (1, 0)],
            "neighbor_scores": [
                {"position": (0, 1), "g": 1.0, "h": 3.0, "f": 4.0},
                {"position": (1, 0), "g": 1.0, "h": 3.0, "f": 4.0},
            ],
            "priority_queue": [
                {"position": (0, 1), "g": 1.0, "h": 3.0, "f": 4.0},
                {"position": (1, 0), "g": 1.0, "h": 3.0, "f": 4.0},
            ],
        },
    ],
}
```

Az `expanded_nodes` a tervezés megfigyeléséhez kell. A cellák sorrendben kerülnek bele, amikor az A* ténylegesen kiválasztja és feldolgozza őket. A matplotlib szimuláció ezeket világoskék pontokként vagy cellaközéppontokként jeleníti meg.

Az új `search_steps` minden feldolgozott aktuális cellához eltárolja a
`GridMap.get_neighbors()` által visszaadott szomszédokat. Ez fontos különbség:
az A* egy aktuális cella összes engedélyezett szomszédját megvizsgálja, de nem
mindegyikből lesz következő feldolgozott cella. A szomszédok költségét
összehasonlítja, majd a prioritási sorból a legjobb `f = g + h` értékű cellát
választja ki.

Például a `(0, 0)` cellából a szabad szomszédok lehetnek `(0, 1)` és `(1, 0)`.
Mindkettő megjelenik a `neighbor_scores` adatai között. Ha `(0, 1)` kapja a
kedvezőbb prioritást, akkor ez lesz a következő feldolgozott cella, míg
`(1, 0)` várakozó jelöltként maradhat a `priority_queue` adataiban.

A `priority_queue` ugyanezen lépés után a még várakozó, érvényes jelölteket
tárolja `f` szerint rendezve. A szimuláció bal oldali panelje ezt a listát
mutatja. A lista első eleme az a cella, amelyet az A* a következő körben
kiválasztana. A lista minden kézi `Kovetkezo` lépésnél frissül, ezért a térkép
és a prioritási sorrend együtt magyarázza az útvonal kialakulását.

A szimuláció a prioritási panelen kiírja a `neighbor_scores` és a
`priority_queue` alapján megjelenített súlyokat:

- `g`: a starttól a jelöltig vezető eddigi költség;
- `h`: a jelölttől a célig becsült költség;
- `f`: `g + h`, vagyis az A* által összehasonlított teljes becslés.

Például egy vízszintes lépésnél, ha a jelöltig `g=1,0`, a célig becsült
távolság pedig `h=3,0`, akkor `f=4,0`. Két azonos `f` értékű jelölt közül a
program a tuple-sorrend és a pillanatnyi prioritási lista alapján választ; ez
nem azt jelenti, hogy valamelyik cellát kihagyta, hanem azt, hogy az egyik
jelölt előbb kerül feldolgozásra.

## 5. A heurisztika

4-szomszédos keresésnél a Manhattan-távolságot használja:

$$
h(n) = |row_n-row_g| + |column_n-column_g|
$$

Ez azt számolja meg, hány vízszintes és függőleges lépés kellene akadályok nélkül.

Átlós keresésnél az alapimplementáció egyszerű Euklideszi heurisztikát használ:

$$
h(n) = \sqrt{(row_n-row_g)^2 + (column_n-column_g)^2}
$$

Ez légvonalbeli becslést ad az aktuális cellától a célig. Nem számol az akadályokkal,
ezért az akadályok miatt ténylegesen szükséges út nem lehet rövidebb ennél.
Az átlós mozgás tényleges költsége ettől függetlenül `sqrt(2)` marad.

Az `astar_variants.py` további, összehasonlítható függvényeket tartalmaz:

- `manhattan`: vízszintes és függőleges mozgáshoz;
- `euclidean`: légvonalbeli becslés;
- `chebyshev`: az eltérő koordináták közül a nagyobbik;
- `octile`: egyenes és `sqrt(2)` költségű átlós mozgáshoz.

A kiválasztott heurisztika az `astar_search(..., heuristic=...)` paraméterrel adható át.
Például: `astar_search(grid_map, start, goal, diagonal=True, heuristic=octile)`.
Saját függvényhez elég a `(position, goal)` paramétereket fogadó függvény, például
`lambda position, goal: 0`.

## 6. A bemenetek módosítása a felületen

A `astar_simulation.py` Tkinter beállítási ablaka a `Szimulacio inditasa` gombbal
indítja el a szimulációt. Itt módosítható a térkép szélessége és magassága, a
`resolution`, a robot sugara, a start- és célcella, az átlós mozgás, valamint a
heurisztika. Az automatikus lejátszás alapértelmezés szerint be van kapcsolva,
így a tervezés és a robot mozgása kattintás nélkül végigfut; kikapcsolva a
`Kovetkezo` gombbal lehet léptetni.
A start és a cél formátuma `sor,oszlop`, például `2,17`.

Az `Utvonal simitasa` kapcsoló alapértelmezés szerint be van kapcsolva. Bekapcsolt
állapotban az A* útvonalát a
`path_smoothing.py` dolgozza fel. A jelenlegi megoldás megkeresi a közel
derékszögű kanyarokat, a valódi kanyarokhoz másodfokú Bézier-görbét készít,
majd a mintapontokat kerekítve ütközés és szomszédság szempontjából ellenőrzi.
Ha a görbe nem biztonságos, az eredeti A* útvonal marad meg.

## 7. A mozgási költség

Az `_movement_cost` két szomszédos cella között számol:

- egyenes lépés költsége: `1.0`;
- átlós lépés költsége: `sqrt(2)`.

Ha `resolution=0.1`, akkor ezek a cellalépések fizikailag 0,1 méteres, illetve körülbelül 0,1414 méteres mozgást jelentenek. Az alapimplementáció költségei azonban cellaegységekben maradnak.

## 8. A keresési ciklus

1. A kezdőcella bekerül a prioritási sorba.
2. A legkisebb prioritású cellát kivesszük.
3. Ha ez a cél, a `came_from` kapcsolatokból visszaépítjük az utat.
4. Egyébként lekérjük a szabad szomszédokat a `GridMap.get_neighbors` segítségével.
5. Minden szomszédra kiszámoljuk az új `g` költséget.
6. Ha ez jobb, mint a korábban ismert költség, frissítjük a szülőt és a prioritást.
7. Ha az `open_list` lista kiürül cél elérése nélkül, nincs út.

Az elavult lista-bejegyzéseket ez a feltétel hagyja figyelmen kívül:

```python
if current_g > g_costs[current]:
    continue
```

Erre azért van szükség, mert egy cellához később jobb út is érkezhet, miközben a régi bejegyzés még bent marad a listában. Ez a megoldás tanulási célból egyszerűbb, de nagy térképen lassabb lehet, mert a `min(open_list)` minden körben végignézi a listát.

## 8. Konkrét számolási példa

Legyen a kezdőcella `(0, 0)`, a cél `(0, 3)`, és használjunk 4-szomszédos keresést. A kezdőcellánál:

```text
g = 0
h = |0 - 0| + |0 - 3| = 3
f = 0 + 3 = 3
```

Ha az algoritmus a `(0, 1)` cellába lép:

```text
g = 1
h = |0 - 0| + |1 - 3| = 2
f = 1 + 2 = 3
```

A `(0, 2)` cellánál:

```text
g = 2
h = |0 - 0| + |2 - 3| = 1
f = 2 + 1 = 3
```

A cél `(0, 3)` elérésekor:

```text
g = 3
h = 0
f = 3
```

Ha a közvetlen útban akadály van, a közvetlen szomszéd nem kerül be a jelöltek közé, és az A* olyan kerülő cellákat vizsgál, amelyek `f` értéke alapján ígéretesek.

## 9. Tesztelés

A `tests/test_astar_baseline.py` teszteli:

- az egyenes út megtalálását;
- akadály megkerülését;
- elérhetetlen cél esetén a `None` eredményt;
- az átlós mozgást;
- a beépített és egyedi heurisztikák kiválasztását;
- a részletes `search_steps` és `priority_queue` adatok létrejöttét;
- foglalt kezdőcella elutasítását.

A tesztek a Python beépített `unittest` modulját használják, ezért külön tesztkeretrendszer nélkül is futtathatók:

```text
python -m unittest codes_diploma.astar_project.tests.test_astar_baseline -v
```

---

# `astar_project/astar_simulation.py`

## 1. A szimuláció célja

Az `astar_simulation.py` az A* működését mutatja meg egy ismert, statikus térképen. A térkép már előre tartalmazza az akadályokat, ezért az A* a tervezés előtt ismeri a teljes pályát.

Ez a szimuláció nem DWA. Nem vizsgál sebességpárokat, gyorsulást, fékezést vagy mozgó akadályokat. A robot egy egyszerű, `0,08 m` sugarú kör alakú testként követi az A* által készített globális útvonalat. A demo az A* átlós keresési módját használja, ezért ahol nincs akadály, átlósan is tud haladni.

```text
GridMap -> A* tervezési nyom -> A* útvonal -> világkoordináták -> robottrajektória -> matplotlib animáció
```

Ez jó első szimuláció, mert külön látható benne a térkép, a tervezett útvonal és a robot mozgása. Később erre lehet ráépíteni a sebességet, a fordulási korlátot vagy a teljes robotmodellt.

## 2. `create_demo_map`

```python
grid_map, start, goal = create_demo_map()
```

Ez létrehoz egy `30 x 20` cellás térképet `0,2 m` felbontással. A térkép fizikai mérete:

```text
szélesség = 30 * 0,2 m = 6,0 m
magasság  = 20 * 0,2 m = 4,0 m
```

A függvény két falat helyez el. A falakban szándékosan rések vannak, ezért az A* a nyílásokon keresztül keres kerülőutat.

A visszatérési értékek:

- `grid_map`: az ismert statikus térkép;
- `start`: kezdő rácscella;
- `goal`: cél rácscella.

## 3. Robotméret és akadálybiztonság

A demo robot sugara `0,08 m`. A `create_demo_map()` az akadályok felvétele után meghívja:

```python
grid_map.inflate_obstacles(robot_radius)
```

Ezután az A* már a kitágított akadálytérképen tervez. A szimulációban megjelenített narancssárga robot köre ugyanekkora sugarú, ezért a képen látható robotméret és a tervezésben használt biztonsági távolság egymáshoz tartozik.

Az átlós sarokvágást a `GridMap.get_neighbors()` külön is tiltja. Így két akadálycellának a közös sarkán sem tud áthaladni a robot középpontja.

## 4. `create_robot_trajectory`

```python
trajectory = create_robot_trajectory(grid_map, path)
```

Az A* útvonala cellák listája. A robot mozgásához világkoordináták kellenek, ezért minden cellát a `grid_to_world` alakít át a cella középpontjára.

Ezután a függvény két egymást követő cellaközéppont között `steps_per_cell` köztes pontot készít. Alapértelmezésben `steps_per_cell=4`, ezért `resolution=0.2` esetén egy egyenes cellalépés 0,2 méter, egy szimulációs lépés pedig körülbelül 0,05 méter.

A függvény nem új útvonalat keres. Csak az A* által már kiszámolt cellaútvonalból készít folytonosabb megjelenítési mozgást.

## 5. `draw_map`

```python
draw_map(axes, grid_map, start, goal)
```

Kirajzolja az akadálycellákat szürke négyzetként, a startot zöld pontként, a célt piros pontként, valamint a világkoordináta-tengelyeket méterben.

Az akadálycellák helye a rácsból így alakul át:

```text
x = origin_x + column * resolution
y = origin_y + row * resolution
```

Így a téglalap pontosan a megfelelő fizikai cellaterületre kerül.

## 6. `plot_simulation`

```python
figure, robot_animation = plot_simulation(
    grid_map, path, trajectory, start, goal
)
```

Ez egy szándékosan rövid, kétpaneles megjelenítő, amely a DWA-szimuláció egyszerű működéséhez hasonlóan egyetlen fő animációs ciklusban frissíti az ábrát:

1. a bal oldalon az aktuális prioritási sort mutatja `g`, `h`, `f` értékekkel;
2. ugyanitt kiírja a prioritási függvényt: $f(n)=g(n)+h(n)$, ahol `g(n)` az eddigi út költsége, `h(n)` a célhoz tartozó becslés, `f(n)` pedig a teljes prioritási érték;
3. átlós keresésnél a könnyebben értelmezhető Euklideszi heurisztikát használja: `h(n) = sqrt(dr^2 + dc^2)`, ahol `dr` és `dc` az aktuális cella és a cél sor-, illetve oszlopkülönbsége;
4. ugyanitt láthatók a lépésköltségek: egyenes lépés `1,0`, átlós lépés `sqrt(2)`, valamint a demo-paraméterek;
5. a jobb oldalon kirajzolja az akadályokat, a vizsgált cellákat, az aktuális keresési cellát, a startot és a célt;
6. a tervezés végén megjeleníti az eredeti és szükség esetén a Bézier-simított útvonalat;
7. a robot a kiválasztott trajektóriát és annak nyomát animálja;
8. az automatikus lejátszás mellett a `Kovetkezo` és `Ujrakezdes` gomb, illetve a jobb nyíl kézi vezérlést ad.

A prioritási panel a tényleges `priority_queue` tartalmát mutatja, legfeljebb
nyolc várakozó elemmel. A térképen a halvány pontok a feldolgozott
`expanded_nodes` cellák, a narancssárga jelölő az aktuális keresési cella, a
robot pedig csak a tervezési szakasz után jelenik meg. A kód nem használ külön
`X`, `N` vagy `O` szöveges cellajelöléseket.

Jelölések:

- `C`: az animáció adott pillanatában ezt a cellát dolgozza fel az A*;
- a halvány pontok: az A* által már vizsgált cellák;
- a kék szaggatott vonal: a végső, visszaépített útvonal.

A `show=False` használható teszteléskor, így az ábra létrejön, de nem nyílik meg grafikus ablak. A szimuláció kézi léptetésű, ezért a keresés és a robotmozgás egyaránt könnyen követhető. A megjelenítő nem modellez sebességet, gyorsulást vagy valódi robotkinematikát; a célja az A* működésének szemléltetése.

## 7. `run_simulation`

```python
run_simulation()
```

Ez a szimuláció belépési pontja:

```text
beállítási ablak
    -> create_demo_map
    -> astar_search(diagonal=..., heuristic=..., return_details=True)
    -> expanded_nodes megjelenitese
    -> smooth_path (ha engedélyezett)
    -> create_robot_trajectory
    -> plot_simulation
```

A tényleges belépési sorrendben a `run_simulation()` először a Tkinter
beállítási ablakot nyitja meg. Az alkalmazott értékekből a `_run_simulation()`
létrehozza a demo térképet, kiválasztja a heurisztikát, lefuttatja az A*-ot,
opcionálisan simít, majd létrehozza a trajektóriát és az animációt.

A fájl közvetlen futtatása:

```text
python -m codes_diploma.astar_project.astar_simulation
```

## 8. Mit mutat és mit nem mutat?

Mutatja:

- az ismert statikus rácstérképet;
- az A* által vizsgált cellákat (`expanded_nodes`) és az aktuális keresési cellát;
- az aktuális prioritási sor részletes adatait (`g`, `h`, `f`);
- az akadálykerülő A* globális útvonalat;
- az eredeti és a ténylegesen használt útvonalat, ha a simítás engedélyezett;
- a rács- és világkoordináták kapcsolatát;
- a robot mozgását az útvonalon;
- az útvonalat és a robot nyomát.

Nem mutatja:

- a robot valódi gyorsulását és fékezését;
- a differenciális hajtás kinematikáját;
- a DWA sebességpár-keresését;
- új akadályok érzékelését futás közben;
- mozgó akadályok elkerülését.

Ezek későbbi fejlesztési fázisok lehetnek, de nem tartoznak ehhez az első statikus A* demonstrációhoz.

## 9. Tesztelés

A `tests/test_astar_simulation.py` ellenőrzi a demo útvonalat, a trajektória kezdő- és végpontját, a pontok számát, valamint a matplotlib ábra ablak nélküli létrehozását.

```text
python -m unittest codes_diploma.astar_project.tests.test_astar_simulation -v
```

---

# `astar_project/path_smoothing.py`

## A jelenlegi kód

```python
def _bezier_point(start_point, control_point, end_point, parameter):
    """Egy pontot számol egy másodfokú Bézier-görbén."""


def _remove_straight_points(path):
    """Eltávolítja az egyenes szakaszok köztes pontjait."""


def bezier_curve_points(path, samples_per_segment=10):
    """Folytonos pontokat készít a valódi kanyarok körül."""


def _is_path_safe(grid_map, path, diagonal=False):
    """Kerekített cellákon ellenőrzi az akadályt és a szomszédságot."""


def smooth_path_bezier(grid_map, path, samples_per_curve=8, diagonal=False):
    """Biztonságos másodfokú Bézier-simítást készít."""


def smooth_path(grid_map, path, diagonal=False, samples_per_curve=8):
    """Kompatibilis belépési pont a Bézier-simításhoz."""
```

## 1. A fájl célja

Ez a modul az A* által készített rácsos útvonalat próbálja kevésbé tördeltté
tenni. Nem keres új utat, és nem módosítja az A* `g`, `h` vagy `f` költségeit.
Utófeldolgozásként működik:

```text
A* útvonal
    -> egyenes köztes pontok eltávolítása
    -> három kontrollpont meghatározása minden kanyarnál
    -> másodfokú Bézier-pontok mintavétele
    -> ellenőrzéshez cellákra kerekítés
    -> rácsos akadály- és szomszédsági ellenőrzés
    -> elfogadott simított út vagy eredeti útvonal
```

## 2. Az útvonal adatai

Az A* útvonala `(row, column)` párok listája. Például:

```python
[(0, 0), (0, 1), (0, 2), (1, 2)]
```

Ez azt jelenti, hogy a robot két cellát vízszintesen halad, majd egy sort
lefelé fordul. A rácskoordináta nem méterben megadott világkoordináta. Ha a
`GridMap` `resolution` értéke `0.2`, akkor egy rácslépés `0.2 m`.

## 3. A másodfokú Bézier-matematika

Egy kanyarhoz három pontot használunk:

- `P0`: a kanyar kezdőpontja;
- `P1`: az eredeti A* kanyarcellája, vagyis a kontrollpont;
- `P2`: a kanyar végpontja.

A képlet:

$$
B(t)=(1-t)^2P_0+2(1-t)tP_1+t^2P_2,
\qquad 0\leq t\leq 1.
$$

A `t` értéke `0` és `1` között változik. A görbe a `P0` pontból indul, a
`P2` pontba érkezik, és a `P1` kontrollpont felé hajlik.

### Konkrét számolási példa

Legyen:

```text
P0 = (0, 0)
P1 = (0, 2)
P2 = (2, 2)
t  = 0,5
```

Ekkor a sorérték:

```text
(1 - 0,5)^2 * 0 + 2 * (1 - 0,5) * 0,5 * 0 + 0,5^2 * 2
= 0,5
```

Az oszlopérték:

```text
(1 - 0,5)^2 * 0 + 2 * (1 - 0,5) * 0,5 * 2 + 0,5^2 * 2
= 1,5
```

A görbe mintapontja tehát `(0,5; 1,5)`. Ez folytonos koordináta, amelyet a
megjelenítő megtart, a biztonsági ellenőrzés viszont egész rácscellára kerekít.

## 4. A fontos függvények

### `_bezier_point(start_point, control_point, end_point, parameter)`

A másodfokú Bézier-képletet alkalmazza egyetlen `t` értékre. A `weight` a
`1 - t`, ezért a három pont súlya fokozatosan változik a görbe mentén.

### `_remove_straight_points(path)`

A három egymást követő pontból képzett irányvektorok kereszt-szorzatát vizsgálja.
Ha az érték nulla, a pontok egy egyenesre esnek, ezért a középső pontot nem kell
simítani. Így egyenes útvonalnál nem keletkezik felesleges görbe.

### `bezier_curve_points(path, samples_per_segment=10)`

Először eltávolítja az egyenes szakaszok köztes pontjait, majd minden valódi
kanyarhoz három pontot választ. A szomszédos élek felezőpontjai adják a `P0`
és `P2` kezdő- és végpontot, az eredeti kanyarcellája pedig a `P1` kontrollpont.
Az eredmény folytonos, lebegőpontos rácskoordinátákból áll.

### `_is_path_safe(grid_map, path, diagonal=False)`

Egész cellákra kerekíti a görbe pontjait, majd ellenőrzi, hogy minden cella
szabad-e, és minden egymást követő cella a `GridMap` engedélyezett szomszédja-e.
Így az akadályba lógó görbe és a tiltott átlós sarokvágás elutasításra kerül.

### `smooth_path_bezier(grid_map, path, samples_per_curve=8, diagonal=False)`

A rácstérképpel együtt meghívja a folytonos Bézier-simítást, majd biztonsági
ellenőrzést végez. Ha a simítás veszélyes, az eredeti A* útvonalat adja vissza.

### `smooth_path(grid_map, path, diagonal=False, samples_per_curve=8)`

Kompatibilis belépési pont, amely a `smooth_path_bezier` függvényt hívja.
Azért maradt meg, mert az `astar_simulation.py` és a korábbi hívók ezt a nevet
használják.

### `bezier_curve_points(path, samples_per_segment=10)`

Ez a függvény folytonos, lebegőpontos Bézier-pontokat készít. A szimuláció ezt
használja a robot trajektóriájához.

## 5. Kapcsolat a szimulációval

Az `astar_simulation.py` simítás nélkül az eredeti A* cellautat használja.
Simításkor a `smooth_path()` biztonsági ellenőrzéssel folytonos Bézier-pontokat
ad vissza, amelyeket a `create_robot_trajectory()` világkoordinátára alakít.
Ha a biztonsági ellenőrzés elutasítja a görbét, az eredeti A* útvonal marad.
A `plot_simulation()` `smoothed=True` jelzője ilyenkor a Bézier-vonalat a
folytonos robottrajektóriából rajzolja, ezért a megjelenített út nem esik vissza
az eredeti rácsos vonalra akkor sem, ha a kerekített cellalista változatlan marad.
A piros vonal mindig a ténylegesen használt, biztonságos trajektóriát mutatja.

Az automatikus lejátszás alapértelmezett időzítése `250 ms` a tervezési
képkockáknál és `60 ms` a robotmozgásnál. A nem simított mozgás cellánként négy
köztes mintapontot kap; a simított mozgás szakaszonként húsz Bézier-mintát
használ, hogy a görbe rácsos ellenőrzése ne ugorjon át cellákat.

## 6. Tesztelés és korlátok

A `test_path_smoothing.py` ellenőrzi, hogy:

- a Bézier-simítás eltérhet az eredeti törött úttól;
- az egyenes útvonal változatlan marad;
- akadály mellett az útvonal nem kerülhet tiltott cellába;
- a kezdő- és végpont megmarad.

Futtatás:

```text
python -m unittest codes_diploma.astar_project.tests.test_path_smoothing -v
```

Szűk folyosóban vagy akadály sarkánál a görbe elutasítható. Ilyenkor a modul
nem erőlteti a simítást, hanem az eredeti A* útvonalat tartja meg.

---

# A közös robotmag és az A*–DWA első integrációja

## 1. A fájlok célja

A `codes_diploma/robot.py` a robotmodellt, a `codes_diploma/DWA.py` a lokális DWA-t, a `codes_diploma/DWA+A.py` pedig az A* és a DWA kapcsolatát tartalmazza.

## 2. Adatfolyam és fontos adatok

Az A* bemenete `GridMap`, valamint a start- és célpont világkoordinátája. A `DWA+A.py` az `astar_search()` eredményét waypointlistává alakítja, majd a `robotstate` és `Obstacle` lista alapján meghívja az `optimisation()` függvényt. A kimenet az eredeti `[v, w, w_L, w_R]` forma.

`robotstate` mezői: `x`, `y`, `v`, `w`, `irany`, `w_L` és `w_R`. Az `Obstacle` kör alakú; a `vx` és `vy` mezők az egyenletes mozgás sebességét jelentik. A `move(dt)` frissíti az akadály helyét.

## 3. Robotparaméterek és kinematika

Az alapértelmezett `robotconfig` keréksugara `0,033 m`, tengelytávja `0,08 m`, maximális keréksebessége `15 rad/s`, időlépése `0,1 s`, előretekintése `3 s`, robotrádiusza `0,10 m`, biztonsági margója pedig `0,15 m`.

A differenciális hajtás összefüggései:

$$
v = r\frac{\omega_L + \omega_R}{2},
\qquad
\omega = r\frac{\omega_R - \omega_L}{b}
$$

Itt `r` a kerék sugara méterben, `b` a tengelytáv méterben, `omega_L` és `omega_R` a kerekek radián/másodperc egységű szögsebességei, `v` a robot lineáris sebessége méter/másodpercben, `omega` pedig a fordulási sebesség radián/másodpercben. Például `10 rad/s` azonos keréksebességnél:

$$
v = 0{,}033\frac{10+10}{2} = 0{,}33\ \mathrm{m/s},
\qquad
\omega = 0{,}033\frac{10-10}{0{,}08} = 0\ \mathrm{rad/s}
$$

Ez egyenes haladást jelent. Az `update()` az eredeti képlettel korlátozza a keréksebesség változását: egy `0,1 s` időlépésben legfeljebb `(2 / 0,033) * 0,1` radián/másodperc változás engedélyezett.

## 4. A DWA döntési menete

A `pairstochoose()` és a `safepairs()` az aktuális keréksebesség körül dinamikus ablakot képez. A `safepairs()` csak előrehaladó (`v >= 0`) párokat engedélyez. Az `optimisation()` a köztes waypointok előtt bátran halad, és csak az utolsó `0,2 m`-en igazítja a sebességet; a végső célpontnál a lassítási zóna `0,5 m`.

Egy `0,10 m` sugarú robot, egy `0,20 m` sugarú akadály és `0,15 m` margója akkor ütközik, ha a középpontok távolsága legfeljebb `0,10 + 0,20 + 0,15 = 0,45 m`. A mozgó akadálynál a távolságvizsgálat az adott predikciós időpontra számolt pozíciót használja.

Az eredeti logika szerint a `get_dist_on_trajectory()` csak a robot szenzorhatárán belüli (`3 m`) és a robot előtti `180` fokos látómezőben lévő akadályokat vizsgálja. A mozgó akadály pozíciója `x + vx * t`, illetve `y + vy * t` alapján változik. Az `AdmissableVelocity()` ezután a megállíthatóságot is ellenőrzi:

$$
|v| \leq \sqrt{2 a_{max} d}
$$

`v` a pillanatnyi lineáris sebesség, `a_max = 2,0 m/s^2` a lassulási korlát, `d` pedig az első ütközésig számított távolság. Például `d = 0,5 m` esetén a megengedett sebesség legfeljebb `sqrt(2 * 2,0 * 0,5) = 1,41 m/s`. Ha egy trajektória nem teljesíti ezt, a DWA elutasítja.

Az érvényes sebességpárok pontszáma az aktuális `Alfa = 5`, `Beta = 2`, `Gamma = 3` súlyokat használja: a célirányt, az ütközésig megtett távolságot és a sebességet kombinálja. A robot hátramenete a szimulációban tiltott. Ha nincs biztonságos pár, az `optimisation()` `(None, [])` értéket ad vissza.

## 5. A* és DWA kapcsolata

Az A* nem ad ki közvetlenül `cmd_vel` üzenetet. A `DWA+A.py` mindig az aktuális
aktív waypointot adja a DWA-nak. A következő waypoint csak akkor válik aktívvá,
ha a robot `0,20 m`-es helyzettűrésen belülre ér és a sebessége legfeljebb
`0,30 m/s`. A köztes pontoknál a befogási zóna kicsi, a végső célpontnál
viszont `0,5 m`-es lassítási zóna működik.

## 6. Biztonsági korlátok és jelenlegi határ

Az A* térkép statikus; a mozgó akadályt a jelenlegi prototípus csak a DWA lokális predikciójában kezeli. A LiDAR-pontfelhőből körakadály-listát készítő ROS2-adapter, a zajszűrés, a teljes fékezési teszt és a globális újratervezés még külön feladat. A robotmodell és a DWA-modul ezért közvetlenül nem importál ROS2- vagy Matplotlib-csomagot.

## 7. Tesztelés

Az alábbi tesztek ellenőrzik a közös robotmagot, a kinematikát, a gyorsuláskorlátot, a mozgó akadály előrejelzését, a DWA ütközéselutasítását és az A* waypoint-kimenetét:

```text
python -m unittest codes_diploma.astar_project.tests.test_robot_and_dwa codes_diploma.astar_project.tests.test_dwa_a
```

## 8. Egyszerű újrahasználat

Az A* és a DWA minimális használata:

```python
from codes_diploma.astar_project.grid_map import GridMap
from codes_diploma.DWA import optimisation
from codes_diploma.robot import Goal, Obstacle, robotconfig, robotstate

config = robotconfig()
state = robotstate(x=0.5, y=0.5)
grid_map = GridMap(width=20, height=20, resolution=0.1)
goal = Goal(1.5, 1.5)

result, safe_pairs = optimisation(config, state, goal, [Obstacle(1.0, 0.8, radius=0.15)])

if result is not None:
    linear_speed = result[0]
    angular_speed = result[1]
```

ROS2-ben a `linear_speed` értéke kerülhet a `Twist.linear.x`, az
`angular_speed` pedig a `Twist.angular.z` mezőbe. A ROS2-node feladata az
odometriából létrehozott `robotstate`, a LiDAR-ból létrehozott `Obstacle` lista
és a `Twist` publikálása.

Az új fájlok röviden:

- `robot.py`: robotállapot, kinematika és akadályok;
- `DWA.py`: DWA-sebességpárok, biztonság és pontozás;
- `DWA+A.py`: A* waypoint és DWA összekötése;
- `test_robot_and_dwa.py`, `test_dwa_a.py`: a két egység tesztjei.

Az A*–DWA teljes folyamatát a `DWA+A.py` osztálya kezeli. A `best_pair` formája
`[v, w, w_L, w_R]`; a ROS2-node a `v` és `w` értékeket `Twist.linear.x` és
`Twist.angular.z` mezőbe írhatja.

## 10. A szimulációs felület A* szerinti megjelenítése

A `codes_diploma/simulation.py` a meglévő A* szimuláció felépítését követi,
de a robotmozgást DWA-val egészíti ki. A bal oldali információs panel az A*
aktuális celláját és a prioritási sor rövid részletét mutatja. A térképen:

- a vékony vonalak a rácscellák határai;
- a sötét cellák a statikus akadályok;
- a kék pontok az A* által már vizsgált cellák;
- a narancssárga pont az A* aktuális keresési pontja;
- a sárga csillag a DWA aktuális waypointja;
- a fekete szaggatott vonal az A* globális útvonala;
- a narancssárga vonal a DWA lokális előrejelzett trajektóriája;
- a piros körök a statikus és mozgó akadályok;
- a kék vonal a robot eddigi nyomvonala.

A program indításakor az A* szimulációjához hasonló beállítási ablak jelenik
meg. Megadható a rács szélessége, magassága, felbontása, start- és célcellája,
az átlós mozgás, valamint az automatikus lejátszás. A beállított start- és
célcella rácskoordináta, például `(2, 2)`, amely a `0,2 m` felbontású térképen
a cella középpontján keresztül világkoordinátává alakul.

A szimuláció két vizuális fázisból áll. Először az A* keresés lépései jelennek
meg egymás után. Ezután minden animációs időlépésben a mozgó akadályok
frissülnek, a DWA kiválasztja a `best_pair` értéket, a `robot.py` `update()`
függvénye mozgatja a robotot, végül a rajz frissül. A globális A* és Bézier-
útvonal minden megjelenítési pontját kis piros pont jelöli; ezek a pontok a
teljes animáció alatt láthatók. A vezérlés ettől külön ritkított waypoint-listát
használ.

Az aktív waypoint-index monoton növekszik: a DWA nem választhat ki újra korábbi
útvonalpontot, és nem ugorhat át előre pontokat. Egy waypoint csak akkor vált,
ha a robot `0,20 m`-en belülre ért és a sebessége legfeljebb `0,30 m/s`. A végső waypoint elérésekor a
`plan_local()` `[0, 0, 0, 0]` parancsot ad vissza, ezért a célba ért robot nem
kap újabb mozgási utasítást.

Az indítóablakban beállítható a rács szélessége, magassága, felbontása,
akadályinflációja, start- és célcellája, továbbá az A* heurisztikája
(`manhattan`, `euclidean`, `chebyshev`, `octile`), az átlós mozgás, az
automatikus lejátszás, valamint az `Alfa`, `Beta` és `Gamma` DWA-súlyok.
Külön kapcsolóval engedélyezhető vagy kikapcsolható a waypoint-lassítás.

A Bézier-simítás kanyarainál a kontrollponttól mért vágási távolság legfeljebb
`3 * resolution` méter. Így például `0,20 m` felbontásnál legfeljebb `0,60 m`
vágás engedélyezett. Ha a görbe akadályt érintene, a biztonsági ellenőrzés az
eredeti A* útvonalat tartja meg.

## 9. Egyszerű A*–DWA szimuláció

A `codes_diploma/simulation.py` külön megjelenítési réteg. Nem tartalmaz új
útvonaltervezési vagy DWA-algoritmust, hanem a `robot.py`, a `DWA.py` és a
`DWA+A.py` függvényeit hívja meg.

A `create_scene()` létrehoz egy rácstérképet, statikus akadályokat, két mozgó
akadályt, robotállapotot és célt. A `create_simulation()` ezután A* útvonalat
keres, Matplotlib-ábrát készít, és minden animációs lépésben ezt a sorrendet
hajtja végre:

```text
mozgó akadályok frissítése
    -> aktuális waypoint kiválasztása
    -> DWA best_pair kiválasztása
    -> robot.py: update()
    -> robot, akadályok és trajektóriák kirajzolása
```

A `best_pair` formája `[v, w, w_L, w_R]`. Ha a DWA nem ad biztonságos párt,
a szimuláció nullás keréksebességgel frissíti a robotot. A narancssárga vonal
a kiválasztott keréksebesség-pár rövid előrejelzett trajektóriája, a kék vonal
pedig a robot eddigi nyomvonala.

### Futtatás

A projekt gyökeréből:

```text
python -m codes_diploma.simulation
```

## 11. A jelenlegi vegso A*--Bezier--DWA rendszer reszletes magyarazata

### 11.1. A rendszer szerepei

A rendszer negy kulon felelossegi szintet tartalmaz:

1. A `GridMap` a vilagot racsos cellakra osztja.
2. Az A* a statikus racson globalis utvonalat keres.
3. A `path_smoothing.py` a racsos ut kanyarait biztonsagos Bezier-gorbevel
     simitja.
4. A DWA rovid, lokalis mozgasparancsot valaszt a robot aktualis allapotabol,
     az akadalyokbol es az aktualis utvonalpontbol.

A fo adatfolyam:

```text
GridMap
    -> astar_search()
    -> astar_path
    -> smooth_path_bezier()
    -> bezier_path
    -> _create_waypoints()
    -> aktualis waypoint
    -> DWA optimisation()
    -> [v, w, w_L, w_R]
    -> robot.update()
```

### 11.2. `robot.py`: a robot fizikai modellje

A `robotconfig` tarolja a differencialis meghajtasu robot adatait:

- `r_kerek = 0,033 m`: a kerek sugara;
- `b = 0,08 m`: a ket kerek tengelyiranyu tavolsaga;
- `w_kerek_max = 15 rad/s`: maximalis kerekszogsebesseg;
- `a_max = 2 m/s^2`: gyorsulasi/lassulasi korlat;
- `dt = 0,1 s`: egy vezerlesi lepes idotartama;
- `predict_time = 3 s`: DWA eloretekintesi ideje;
- `rob_radius = 0,10 m`: a robot kor sugaru kozelitese;
- `safety_margin = 0,15 m`: biztonsagi tavolsag;
- `Alfa = 5`, `Beta = 2`, `Gamma = 3`: a DWA pontozasi sulya;
- `allow_reverse = False`: a szimulacioban a hatramenet tiltott.

A differencialis kerekkinematika:

$$
v = r\frac{\omega_L+\omega_R}{2}
$$

$$
\omega = r\frac{\omega_R-\omega_L}{2b}
$$

`r` a kerek sugara, `b` a tengelytav, `omega_L` es `omega_R` a bal es jobb
kerek szogsebessege, `v` a robot linearis sebessege, `omega` pedig a robot
szogsebessege.

Pelda az aktualis parameterekkel, azonos `10 rad/s` kerekszogsebessegnel:

$$
v = 0{,}033\frac{10+10}{2}=0{,}33\ \mathrm{m/s}
$$

$$
\omega = 0{,}033\frac{10-10}{2\cdot0{,}08}=0\ \mathrm{rad/s}
$$

Ez egyenes haladast jelent, mert a ket kerek azonos sebesseggel forog.

Az `update()` eloszor korlatozza a celzott kerekszogsebesseg valtozasat, majd
az aktualis `v` es `omega` ertekekkel frissiti a robot helyzetet. Nem egyetlen
ponttal ugrik a kovetkezo koordinatara, hanem a korpalyas kinematikai keplettel
szamolja ki az uj `x`, `y` es `irany` erteket.

### 11.3. Mozgo akadalyok

Az `Obstacle` adatai:

```python
Obstacle(x, y, radius, vx, vy)
```

Az `x`, `y` a kozepont, a `radius` a kor sugara, a `vx`, `vy` pedig a
vilagkoordinatas sebesseg komponensei. A szimulacios ciklus minden `dt` utan
meghivja az akadaly `move(dt)` metodusat:

$$
x_{uj}=x_{regi}+v_x\cdot dt
$$

$$
y_{uj}=y_{regi}+v_y\cdot dt
$$

Pelda: `v_y=0,25 m/s` es `dt=0,1 s` esetben az akadaly minden ciklusban
`0,025 m`-rel mozog felfele.

### 11.4. `DWA.py`: dinamikus ablak es biztonsag

A `pairstochoose()` az aktualis kerekszogsebessegek korul mintakat general.
Az ablak szelesseget az `a_max / r_kerek` kerekszoggyorsulas es a `dt` ido
hatarozza meg.

Az `AdmissableVelocity()` minden jelolt parnal meghivja a
`get_dist_on_trajectory()` metodust. Ez a kovetkezoket vizsgalja:

- legfeljebb `3 m` szenzortavolsag;
- a robot elotti `180 fokos` latomezo;
- a mozgo akadaly elore jelzett pozicioja;
- a robot, az akadaly es a biztonsagi sav egyuttes sugara.

Az elso utkozesig szamolt tavolsag legyen `d`. A megallithatosagi feltetel:

$$
|v|\leq\sqrt{2a_{max}d}
$$

Peldaul `a_max=2 m/s^2` es `d=0,5 m` eseten:

$$
|v|\leq\sqrt{2\cdot2\cdot0{,}5}=1{,}41\ \mathrm{m/s}
$$

Az ennel gyorsabb jelolt par kiesik a `safepairs()` listabol.

Az `optimisation()` a megmaradt parokat heading, akadalybiztonsag es sebesseg
alapjan pontozza. A cel kozeli lassitas csak az aktualis konfiguracio szerint
kapcsolhato; a vegso cel elerese ettol fuggetlenul explicit nullas parancsot
ad.

### 11.5. `path_smoothing.py`: a Bezier-utvonal

Az A* racspontjai torott vonalat alkotnak. A `_remove_straight_points()` az
egyenes reszek felesleges pontjait kiszedi, a valodi kanyarokat megtartja.

A masodfoku Bezier-keplet:

$$
B(t)=(1-t)^2P_0+2(1-t)tP_1+t^2P_2,
\qquad 0\leq t\leq1
$$

`P_0` a kanyar kezdopontja, `P_1` a kontrollpont, `P_2` a kanyar vegpontja.
Peldaul `t=0,5` eseten a kontrollpont a gorbe kozepere gyakorol hatast, de a
gorbe nem feltetlenul megy at pontosan a kontrollponton.

A kontrollponttol valo vagas alapertelmezetten `0,5 * resolution` meretu. A
`_is_path_safe()` a gorbe koztes pontjait cellakra bontja, ellenorzi a szabad
cellakat es a szomszedsagi kapcsolatokat. A `_has_direction_reversal()` a
lokalis visszafordulast tiltja. Ha barmelyik biztonsagi ellenorzes sikertelen,
a modul az eredeti A* utat adja vissza.

Ezert a Bezier-utvonal ketfele lehet:

- biztonsagos esetben folytonos, simitott gorbe;
- szuk vagy veszelyes kanyarban az eredeti, torott A* ut.

### 11.6. `DWA+A.py`: waypoint-allapotgep

Az `AStarDWAPlanner.plan_global()` eltarolja az `astar_path` es a
`bezier_path` listat, majd a simitott utbol vezerlesi waypointokat keszit.
Az aktiv index a `waypoint_index`.

Az aktiv waypoint csak akkor lep tovabb, ha:

1. a robot a dinamikus waypoint-turesen belul van;
2. a robot sebessege eleg kicsi;
3. vagy a skalarszorzas alapjan mar elhaladt a waypoint mellett.

Ez megakadályozza, hogy a DWA egy mar elhagyott ponthoz visszaforduljon.
Az `optimisation()` bemeneti celja az aktiv waypoint, nem egy kulon, elugro
racskoordinata.

### 11.7. `simulation.py`: grafikus szimulacio

A szimulacios ciklus sorrendje:

```text
1. A* vizsgalt cellak megjelenitese
2. statikus es mozgo akadalyak letrehozasa
3. mozgó akadalyak frissitese
4. aktiv waypoint es DWA cel meghatarozasa
5. DWA best_pair kivalsztasa
6. robot.update()
7. robotnyom, Bézier-ut, pontok es akadalyak kirajzolasa
```

A megjelenites jelolesei:

- vilagos kek pontok: A* altal vizsgalt cellak;
- zold vonal: Bézier-utvonal;
- kis piros pontok: DWA vezerlesi waypointok;
- sarga csillag: aktualis aktiv waypoint;
- narancssarga vonal: DWA rovid lokalis trajektoria;
- piros korok: statikus es mozgo akadalyak;
- kek kor: robot.

A program inditasa:

```text
python -m codes_diploma.simulation
```

Az ablakban a racs, a resolution, az akadalyinflacio, az A* heurisztika,
az Alfa/Beta/Gamma sullyok, a Bezier-simitas es a waypoint-lassitas is
allithato.

### 11.8. Teszteles

A teljes tesztcsomag parancsa:

```text
python -m unittest discover -s codes_diploma/astar_project/tests -p "test_*.py"
```

A tesztek ellenorzik az A* alapot, a racterkepet, a Bezier-biztonsagot, a
robotkinematikat, a DWA-t, az A*--DWA kapcsolatot, a mozgó akadalyat es a
szimulacios jelenetet. A legutobbi teljes ellenorzes eredmenye: `32 teszt
sikeres`.

A megjelenítés automatikusan elindul és legfeljebb `600` animációs lépést
futtat. A szimulációhoz nem kell ROS2; a Matplotlib és NumPy telepítése
szükséges.

## 12. ROS 2 / Gazebo robotfüggetlen C++ A* + DWA integráció

**Aktív ág:** a `cpp-rethink` alapértelmezett Gazebo launch-a ezt a C++
`astar_dwa_node` vezérlőt indítja. A 17–24. fejezetek későbbi, eltávolított
Python ROS-adapter kísérletének archív leírásai; nem a jelenlegi indítási
útmutató részei. Az aktuális C++ adatfolyamot és dolgozatszöveget a 25.
fejezet tartalmazza.

### 12.1. A csomag célja

Az új `ros2_astar_dwa_gazebo/src/astar_dwa_controller` csomag a korábbi
Python prototípustól független, C++17 alapú ROS 2 vezérlő. A
[astar_dwa_node.cpp](./ros2_astar_dwa_gazebo/src/astar_dwa_controller/src/astar_dwa_node.cpp)
nem tartalmaz TurtleBot3- vagy ROSbot-specifikus meghajtási kódot. Szabványos
ROS üzeneteket fogad és küld, ezért a robotmodell később topic-paraméterekkel
cserélhető.

### 12.2. Adatfolyam

```text
/scan + /odom
    -> obstacles(): világkoordinátás LiDAR-pontok, sebességbecslés
ismert statikus akadályok + /odom + /goal_pose
    -> astar(): statikus Grid cellák -> világkoordinátás útvonal
    -> control(): látható waypoint és előretekintési cél
    -> dwa(): LiDAR-alapú sebességvizsgálat és útvonalközelségi pontozás
    -> /cmd_vel
```

A `/goal_pose` üzenet új világkoordinátás célt állít be. Az A* útvonalat a
`/astar_path` `nav_msgs/Path` topicon teszi közzé. A robot számára a lényeges
interfész tehát: `LaserScan`, `Odometry`, `PoseStamped`, `Twist` és `Path`.

### 12.3. Fontos paraméterek és koordináták

Az `astar_dwa_controller/config/rosbot.yaml` tartalmazza a topic-neveket,
a célt, a `map_size` értéket, a `resolution` cellaméretet és a
`robot_radius` biztonsági sugarat. A C++ node rögzített, téglalap alakú rácsot
épít a konfigurált térképorigótól. A rácskoordináta:

```text
row = floor((y - origin_y) / resolution)
column = floor((x - origin_x) / resolution)
```

Például `resolution = 0.20 m`, `origin_y = -6.0 m`, `y = 0.4 m` esetén
`row = floor(6.4 / 0.2) = 32`. A cellaközéppont visszaalakítása:
`y = origin_y + (row + 0.5) * resolution`, ezért a 32-es sor középpontja
`-6 + 32.5 * 0.2 = 0.5 m`.

### 12.4. A* és DWA működése

Az A* prioritási sort használ. A `g` az eddigi cellaköltség, a `h` az
egyenes vonalú becslés a célig, az `f = g + h` pedig a kiválasztási érték.
Egy átlós lépés költsége `sqrt(2)`, egyenes lépésé `1`. Például egy két
egyenes és egy átlós lépés költsége `1 + 1 + 1.414 = 3.414` cellaköltség.
Átlós sarokvágás csak akkor engedélyezett, ha a két oldalsó cella is szabad.

A DWA kerék-szögsebességeket mintavételez a gyorsuláskorlátos dinamikus
ablakban. A YAML szerint az előremeneti sebesség felső határa `0.22 m/s`,
a szögsebességé `1.0 rad/s`. Az előrejelzés `0.1 s` lépéssel, a helyi
célpont távolságától függő, `0.8...2.0 s` időtávon fut. Ütközés észlelésekor
a fékezhetőség és az ütközésig hátralévő idő feltétele dönti el az elfogadást;
nem minden későbbi ütközés jelent automatikus kiesést.

A pontozás célirány-, szabad tér- és sebességtagot, továbbá a globális
útvonaltól és a helyi céltól mért távolság büntetését tartalmazza. A jelenlegi
képletet, a változók egységeit és a behelyettesítési példát a dokumentum végén
a 14. fejezet részletezi. A legnagyobb pontszámú elfogadott jelölt adja a
`/cmd_vel` parancsot; elfogadható jelölt nélkül helyben elfordulás következik.

### 12.5. ROSbot átültethetőség

A ROSbot saját bringupja biztosítja a motorvezérlést, odometriát és LiDAR-t.
Az algoritmus nem nyúl közvetlenül a motorokhoz. Ha a ROSbot például
`/rosbot/scan`, `/rosbot/odom` és `/rosbot/cmd_vel` topicokat használ, a
paraméterekkel ezek adhatók meg; a C++ forrás nem változik. A Gazebo-világ
robotmodellje jelenleg TurtleBot3, ezért a ROSbot modellcsere külön
szimulációs konfigurációs lépés, nem algoritmusmódosítás.

### 12.6. Ellenőrzés

Windows alatt a ROS fejlécek hiányában a Python launch-fájlok szintaxisa
ellenőrizhető. A tényleges C++ fordítás WSL-ben történik:

```bash
cd ~/projects/ros2_astar_dwa_gazebo
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
```

### 12.7. Ismert térkép, LiDAR és megjelenítés

Az `astar_dwa_node` kizárólag az előre ismert statikus térképet használja.
Az `known_obstacle_x`, `known_obstacle_y` és
`known_obstacle_radius` paraméterekből építi fel az A* statikus térképét.
Ez a szimulációban azt jelenti, hogy a piros és narancssárga statikus
akadályok helye előre ismert. A DWA ettől még a `/scan` aktuális mérését
használja, így az előre nem ismert vagy mozgó akadályokra is reagál.

Az automatikus `lidar_map` és `frontier` módok eltávolítva, ezért a LiDAR
csak a DWA pillanatnyi akadályvizsgálatához használatos.

A `visualization.launch.py` RViz2-konfigurációja az `odom` fix keretben
megjeleníti a TF-fa koordinátáit, a narancssárga `/scan` pontokat, a kék
odometriát és a zöld `/astar_path` útvonalat. Ez a megjelenítés nem avatkozik
be a vezérlésbe: ugyanazok a szabványos ROS topicok használhatók Gazebo-ban
és a valódi ROSboton.

### 12.8. Mozgó akadály szimuláció

A `moving_obstacle_node.py` a Gazebo `SetEntityPose` szolgáltatásán keresztül
mozgatja a `moving_obstacle` nevű kék hengert. A pozíció:

```text
x = 3.0 m
y = 1.8 m + 1.2 m * sin(0.6 * t)
```

ahol `t` másodpercben mért szimulációs idő. Például `t = 0` esetén
`y = 1.8 m`, `t = 1` esetén pedig körülbelül
`1.8 + 1.2 * 0.565 = 2.478 m`. A henger a LiDAR-ban megjelenik, és a DWA
ütközésvizsgálata a következő előrejelzett pontoknál figyelembe veszi.

### 12.9. RViz-hibakeresés és a látható működés

Az RViz konfiguráció fix koordinátakerete `odom`, nem `map`. A jelenlegi
Gazebo-változatban nincs SLAM vagy térképkiszolgáló, ezért `map` TF nem
létezik; a `Fixed Frame: map` hiba emiatt helyes hibajelzés. A
`visualization.launch.py` az `astar_dwa.rviz` konfigurációt és az `odom`
fix frame-et tölti be.

Az `astar_dwa_node` minden vezérlési ciklusban közzéteszi az
`/astar_dwa_markers` `visualization_msgs/MarkerArray` üzenetet:

- zöld gömb: aktuális A* cél/waypoint;
- zöld vonal: A* útvonal;
- piros hengerek: ismert statikus akadályok;
- kék vonal: a kiválasztott DWA sebességpár 15 lépéses előrejelzése.

Az odometriából a node dinamikusan publikálja az `odom -> base_link`, majd a
`base_link -> base_scan` TF-et. Ez teszi lehetővé, hogy az RViz a `/scan`
LiDAR-pontokat az `odom` fix frame-be transzformálja. A valós ROSboton ezt a
TF-et célszerű a robot saját bringupjára bízni; a vezérlő topic- és frame
paraméterezése mellett a szabványos interfész változatlan marad.

## 13. RViz-es célkijelölés és OccupancyGrid térkép

### A fájlok célja

Az `astar_dwa_node.cpp` most az `/astar_map` `nav_msgs/OccupancyGrid` topicot
is publikálja. Ez a `known_map` módban a statikus akadályokat, a robot
ráhagyásával inflált tiltott cellákat és a térkép szélét mutatja. Az
`astar_dwa.rviz` ehhez hozzáadja a `Known occupancy map` displayt, valamint a
`SetGoal` eszközt, amely a `/goal_pose` topicon küld célt.

### Adatfolyam és célkijelölés

Az RViz `2D Goal Pose` eszköz kattintásból és az egér húzásának irányából
`PoseStamped` üzenetet készít. A node a pozíció `x` és `y` mezőjét eltárolja
`goal_x_` és `goal_y_` értékként, naplózza az új célt, majd a következő
vezérlési ciklusban újra lefuttatja az A*-t. Például egy `(4.0, 2.0)` cél az
`odom` koordinátarendszerben a térkép origójától 4 méterre keletre és 2 méterre
északra van; a node ezt a világkoordinátát cellává alakítja.

### Térkép és koordináta-átalakítás

Az OccupancyGrid origója `(-map_size/2, -map_size/2)`, a cellaméret
`resolution`. Egy `(x, y) = (4.0, 2.0)` pont `resolution = 0.20 m` és
`map_size = 16 m` mellett:

```text
column = floor((4.0 + 8.0) / 0.20) = 60
row    = floor((2.0 + 8.0) / 0.20) = 50
```

Ez azt jelenti, hogy a pont a 80x80 cellás térkép 60. oszlopába és 50. sorába
kerül. Az akadályok körül a kód
`ceil((obstacle.radius + robot_radius) / resolution)` sugarú körben 100-as
értékű, foglalt cellákat állít be; a többi ismert szabad cella 0.

### Látható működés

A célmarker most gömbből, célfeliratból és síkbeli céljelből áll. Az A* vonal
vastagabb, a DWA előrejelzett vonala külön kék magasságban fut, továbbá a
robot footprintje és haladási nyila is látható. A `/astar_map` tartós
QoS-szal készül, ezért az RViz későbbi csatlakozásakor is megkapja az egyszer
publikált statikus térképet. A node az odom első beérkezése után, majd minden
vezérlési ciklusban meghívja a `publish_map()` függvényt. A `known_map` mód
akadálylistája nem függ a LiDAR első üzenetétől, ezért a térkép akkor is
nem üres, ha a szenzoradat néhány pillanattal később érkezik.

Az RViz célüzenete nem Gazebo-topic. A `/goal_pose` a vezérlő node bemenete;
az új cél alapján az A* útvonal újraszámolódik, majd a DWA a Gazebo felé a
`/cmd_vel` topicot használja. Ha még nincs LiDAR, a node már akkor is közzéteszi
a célmarkert, de sebességparancsot csak érvényes szenzoradat után ad.

### Korlátok és ellenőrzés

Az RViz-ből érkező cél az `odom` keretben legyen. A statikus térkép nem
tartalmazza a mozgó kék akadályt, mert annak aktuális helyét a LiDAR és a DWA
kezeli. Ellenőrizhető:

```bash
ros2 topic echo /astar_map --once
ros2 topic echo /goal_pose --once
```

Az RViz `TF` display tengelyei korábban piros X-tengelyeket és nyilakat
rajzoltak a `base_link` és `base_scan` keretekhez. Ezek vizualizációs elemek,
nem akadályok és nem A*-útvonalak; a projekt konfigurációjában a nyilak,
tengelyek és frame-nevek most ki vannak kapcsolva a tisztább nézet érdekében.

## 14. LiDAR-alapú felhalmozott térkép

### A fájl célja

Az `astar_dwa_node.cpp` `planning_source` paramétere két működést választ:
`known_map` esetén a YAML-ben megadott statikus akadályokból készül a tervezési
térkép; `lidar_map` esetén a node a LiDAR-mérésekből fokozatosan felépített
`OccupancyGrid`-et használja. Ez a mód a korábbi ismerttérképes megoldást nem
törli, csak alternatív forrást ad az A* számára.

### Adatfolyam

Az `scan()` eltárolja az új `LaserScan` üzenetet, majd `lidar_map` vagy
`frontier` módban
meghívja az `update_lidar_map()` függvényt. Ez a robot aktuális
`pose_` értékével az `odom` keretbe alakítja a LiDAR-sugarakat. A
`mark_lidar_ray()` a robot cellájától a mérési végpontig halad:

- a köztes cellák értéke `0`, vagyis szabad;
- érvényes akadálymérésnél a végpont értéke `100`, vagyis foglalt;
- `inf` vagy tartományon kívüli mérésnél a `range_max` végpontja nem lesz
  foglalt, csak a sugár köztes cellái lesznek szabadok;
- a korábbi cellaértékek megmaradnak, így a térkép összeadja a több
  pozícióból érkező megfigyeléseket.

Az `astar()` a `planning_obstacles()` eredményét használja. `lidar_map`
módban a `lidar_map_obstacles()` minden `100`-as cellából akadálypontot
képez, majd az A* a robot sugarával és a cella félméretével inflálja az
akadály környezetét. A DWA ettől külön továbbra is az aktuális, nyers
`obstacles()` LiDAR-pontokat használja. A lokális DWA csak a robot előtti
180 fokos és legfeljebb 3 méteres mérési tartományt használja, így a falak
és akadályok mögötti 360 fokos pontfelhő nem kényszeríti indokolatlan
megállásra vagy helyben forgásra.

### Rács, koordináták és képlet

A térkép négyzetes, oldala `map_size` méter, cellamérete `resolution` méter,
origója az `odom` rendszerben `(-map_size/2, -map_size/2)`. A
`map_cell(x, y, row, column)` képlete:

```text
column = floor((x + map_size / 2) / resolution)
row    = floor((y + map_size / 2) / resolution)
```

Itt `x` és `y` méterben mért világkoordináta, `row` és `column` egész
cellaindex. Például `map_size = 16 m`, `resolution = 0.20 m` és
`(x, y) = (4.0, 2.0)` esetén:

```text
column = floor((4.0 + 8.0) / 0.20) = floor(60.0) = 60
row    = floor((2.0 + 8.0) / 0.20) = floor(50.0) = 50
```

Ez a 80x80 cellás térkép `(50, 60)` cellája. Ha a robot
`(0, 0)` ponton áll, és egy sugár `2.0 m` távolságban, `0` radián szögben
akadályt mér, akkor a végpont `(2.0, 0.0)`, amelynek cellája:

```text
column = floor((2.0 + 8.0) / 0.20) = 50
row    = floor((0.0 + 8.0) / 0.20) = 40
```

A `mark_lidar_ray()` a robot cellájától a `(40, 50)` végpontig a diszkrét
vonal celláit jelöli szabadnak, majd a `(40, 50)` cellát foglaltra állítja.

### Megjelenítés és használat

Az `publish_map()` `lidar_map` módban közvetlenül ezt a rácsot publikálja
`/astar_map` néven. Az `OccupancyGrid` jelentése:

- `-1`: még nem látott / ismeretlen;
- `0`: LiDAR-sugár által szabadnak látott cella;
- `100`: LiDAR-mérés végpontja, feltételezett akadály.

A mód a launch paraméterével kapcsolható, a YAML alapértelmezése mellett:

```bash
ros2 launch dwa_gazebo_sim simulation.launch.py planning_source:=lidar_map
```

Ezután újra kell fordítani a workspace-t, majd a teljes
`simulation.launch.py` indítással lehet futtatni. `known_map` módban az
OccupancyGrid továbbra is a YAML statikus akadályait és a biztonsági
inflációt mutatja.

### Biztonsági korlátok

Ez a megoldás LiDAR-odometriai térkép, nem teljes SLAM. Az `odom` driftje a
térképben is megjelenhet, nincs loop closure és nincs map->odom korrekció.
A cellán kívüli sugarakat a node elutasítja. Az ismeretlen cellákat a jelenlegi egyszerű
szimulációs A* nem tiltja le, ezért a robot a cél felé haladva fedezhet fel
új területet; valódi biztonságkritikus navigációhoz az ismeretlen cellákat
blokkolni vagy Nav2/SLAM Toolbox megoldással kezelni kell.

### Ellenőrzés

A C++ változtatás WSL-ben fordítható és indítható:

```bash
cd "<WORKSPACE>/codes_diploma/ros2_astar_dwa_gazebo"
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source install/setup.bash
ros2 launch dwa_gazebo_sim simulation.launch.py
```

Futás közben a térkép ellenőrzése:

```bash
ros2 topic echo /astar_map --once
```

Az üzenetben a `data` tömbben kell megjelenniük a `-1`, `0` és `100`
értékeknek; `known_map` módban a `-1` érték nem része az előre ismert
statikus térképnek.

## 15. Frontier-alapú automatikus feltérképezés

### Működés

Az új `planning_source: frontier` mód nem használ előre megadott célt. A
vezérlő induló állapota és alapértelmezett célkoordinátája `(0, 0)`, de a cél
nem aktív, ezért `known_map` és `lidar_map` módban is csak `/goal_pose`
üzenet után indul a robot. Frontier módban a node a felhalmozott LiDAR-rács
alapján automatikusan aktivál célt.

Frontier célcellának azt az ismert szabad cellát tekinti, amely:

- legalább egy 8-szomszédja még ismeretlen (`-1`);
- legalább `0.6 m` távolságra van a robottól.

A `select_frontier_goal()` a feltételeknek megfelelő szabad cellák közül a
legközelebbit választja. Ezt a világkoordinátás cellaközéppontot az A* céljaként állítja be,
majd a DWA a következő waypoint felé mozgatja a robotot. A frontier elérése
után a cél deaktiválódik, és a következő vezérlési ciklus új frontiert keres.
Ha nincs több ilyen cella, a node nulla sebességet publikál és megáll.

Ha a frontier célhoz az aktuális, inflált LiDAR-térképen az A* nem talál
útvonalat, a cél nem törlődik azonnal. A node megtartja a kiválasztott
frontiert, és korlátozott recovery-forgatást indít. A haladásfigyelő akkor is
recovery-t indít, ha több másodpercig nincs legalább `0.10 m` odometriai
elmozdulás. A forgatás legfeljebb `2.5 s`, utána új A* útvonal készül. A cél
így nem kerül törlésre, és a vezérlés nem keveri össze a DWA által választott
nullasebességet a sikeres célbaéréssel.

A LiDAR-térkép ray-castinget használ. Valós, érvényes végpontnál a sugár
köztes cellái szabadak, a végpont foglalt; `inf` vagy tartományon kívüli
mérésnél a sugár a `range_max` határig csak szabad cellákat jelöl. Így a
nyitott előre irány nem marad tévesen teljesen ismeretlen, és a frontier
kereső ténylegesen tud elérhető célcellát találni.

A Gazebo-fizika stabilitása érdekében a DWA kimenete sebességrámpán halad:
a lineáris sebesség legfeljebb `0.20 m/s`, a szögsebesség legfeljebb
`0.8 rad/s`, egy 0,1 másodperces ciklusban pedig a változás legfeljebb
`0.04 m/s` és `0.20 rad/s`. Üres A* útvonal esetén a node nulla sebességet
publikál és megáll.

### Adatfolyam és példa

```text
LiDAR -> lidar_map -> szabad/ismeretlen határ keresése
                         -> frontier cél
                         -> A* -> DWA -> /cmd_vel
                                      |
                                      +-> új LiDAR-mérés
```

Ha a robot `(0, 0)` helyen van, `resolution = 0.20 m`, és egy szabad cella
középpontja `(1.1, 0.3)`, akkor a frontier cél ez a világpont lesz. Az A*
ezt a célcellát használja; amikor a robot `0.3 m`-nél közelebb ér, a cél
lezárul, és új határcella kiválasztása indul.

### Korlátok

Ez a frontier-mód egyszerű odometria-alapú feltérképezés. Az `odom` driftje
eltolhatja a korábbi méréseket, és nincs loop closure. Az ismeretlen cellákat
az egyszerű A* átjárhatónak kezeli, miközben a frontier kiválasztása csak
ismert szabad cellára esik. Valós, biztonságkritikus roboton az ismeretlen
cellákat konzervatívan blokkolni, illetve SLAM Toolbox/Nav2 rendszert használni
célszerű.

### Indítás és ellenőrzés

```bash
ros2 launch dwa_gazebo_sim simulation.launch.py planning_source:=frontier
```

A naplóban az automatikusan kiválasztott cél ilyen formában jelenik meg:

```text
Uj frontier cel: x=..., y=... m
```

---

# `simulation.py` – 1.1 Szimulációs eredmények és forgatókönyvek

## 1. A fájl célja

A `simulation.py` az A* globális útvonaltervezést és a DWA lokális mozgástervezést
egy közös, kétdimenziós jelenetben mutatja be. A szimuláció nem csak a végső
útvonalat rajzolja ki: az A* keresés közben megjeleníti a vizsgált cellákat és
a prioritási sort, a DWA szakaszban pedig a lehetséges pályákat, a mozgó
akadályokat, a waypointot és a fékezési szakaszokat is.

Az alapbeállításokkal a térkép `30 x 20` cellás, a felbontás `0,2 m/cella`,
ezért a megjelenített terület `6,0 m x 4,0 m`. A kezdőcella `(2, 2)`, a
célcella `(17, 27)`, ahol a koordináta formája `(sor, oszlop)`. A világban
ezek középpontjai rendre `(0,5 m, 0,5 m)` és `(5,5 m, 3,5 m)`.

## 2. Adatfolyam

Az `create_scene()` elkészíti a rácstérképet, a statikus akadályokat, a két
mozgó akadályt és a robot kezdeti állapotát. Az akadályinfláció után az
`astar_search()` megkeresi a globális útvonalat. Ezt az `AStarDWAPlanner`
Bezier-simítással waypointokká alakítja. Az animáció első része az A* keresés
lépéseit, a második része pedig a DWA ciklusait futtatja:

```text
create_scene -> A* keresés -> Bezier útvonal és waypointok
             -> mozgó akadályok -> DWA pályajelöltek -> robotfrissítés
```

A `compute_onlab_trajectories()` minden DWA sebességpárhoz előre kiszámítja a
jósolt pályát, majd a pálya végéről indított fékezési szakaszt. A pálya piros,
ha ütközésveszélyes vagy a megálláshoz szükséges távolság nem elegendő; a
biztonságos pályák szürkék, a kiválasztott pálya zöld.

## 3. Fontos függvények és adatok

- `load_planner_class()`: betölti a `DWA+A.py` fájlban lévő
  `AStarDWAPlanner` osztályt.
- `parse_cell(value)`: a `"sor,oszlop"` szöveget egész koordinátapárrá alakítja.
- `create_scene(...)`: a rácsot és az akadályokat hozza létre.
- `create_simulation(...)`: elvégzi a tervezést, felépíti a Matplotlib-ábrát,
  majd visszaadja a `figure` és `FuncAnimation` objektumot.
- `compute_onlab_trajectories(...)`: a DWA jelöltek biztonságát és fékezési
  útját számolja.
- `update_frame(frame)`: A* vagy DWA állapot szerint frissíti az ábrát.
- `run_simulation()`: a Tkinter beállítóablakot indítja el.

Az ábra bal oldali információs panelje az A* lépését és prioritási értékeit,
illetve a DWA fázisban a robot helyzetét, sebességét, az összes, veszélyes és
biztonságos pályák darabszámát mutatja. A jobb oldali térképen a sötét cellák
az inflált akadályterületet, a piros körök a dinamikus vagy statikus akadályokat,
a világoszöld vonal a simított útvonalat, a kék nyomvonal pedig a robot tényleges
mozgását jelzi.

## 4. A képek értelmezése

Az alapbeállításokkal mentett képkockák a
`codes_diploma/astar_project/results/figures/` mappában találhatók.

1. `simulation_01_frame_0000.png`: az A* keresés első lépése. A bal oldali
   panelen az aktuális cella `(2, 2)`, a prioritási sorban pedig az `f` értékek
   láthatók. A világoskék pontok a már kibővített A* cellákat jelölik.
2. `simulation_02_frame_0100.png`: az A* keresés késői szakasza. A statikus
   akadályok közötti átjárók és az infláció miatt tiltott biztonsági zónák
   szemléltetik, hogy a robot nem matematikai pontként tervez útvonalat.
3. `simulation_03_frame_0250.png`: a DWA mozgás közbeni állapota. A robot
   körül sok piros és szürke jelölt pálya látható; a piros jelöltek veszélyesek,
   a szürke jelöltek a pillanatnyilag megengedett alternatívák. A vastag zöld
   görbe az aktuálisan választott pályát, a csillag a waypointot jelöli.
4. `simulation_04_frame_0500.png`: a robot a középső akadályrendszer után
   közelít a felső átjáróhoz. Ez jó kép az akadálykerülés és a waypoint-követés
   együttes bemutatására.
5. `simulation_05_frame_0650.png`: késői DWA állapot, amikor a robot már a cél
   előtti szakaszon halad. A kék nyomvonal és a zöld globális útvonal közötti
   eltérés a lokális korrekciót szemlélteti.
6. `simulation_06_frame_0725.png`: végállapot. A panelen `Cel elerve`, a
   sebesség `0,00 m/s`, a robot pedig a cél körül áll. Ez a legjobb összefoglaló
   kép a sikeres útvonaltervezés és végrehajtás bemutatására.

## 5. Konkrét számolási példa

Az alapbeállításban a célcella `(17, 27)`, a felbontás `0,2 m`, az origó
`(0,0)`. A célpont világkoordinátája:

```text
x = (27 + 0,5) * 0,2 m = 5,5 m
y = (17 + 0,5) * 0,2 m = 3,5 m
```

Az animációban a tervezési fázis 125 képkockából áll. A DWA mozgás ezért a
`movement_start = 126` képkockánál kezdődik, és legfeljebb 600 mozgási lépést
kap. A `frame = 250` kép így a `250 - 126 = 124`-edik mozgási állapot környékét
mutatja, nem egy újratervezett globális A* útvonalat.

## 6. Korlátok és indítás

A közvetlen

```text
python -m codes_diploma.simulation
```

indítás a Tkinter beállítóablakot és utána a blokkoló Matplotlib-ablakot nyitja
meg, ezért parancssori futtatásban az ablak bezárásáig nem ad vissza promptot.
Képek mentéséhez a `create_simulation(..., show=False)` visszaadott ábrájának
képkockái menthetők. A jelenlegi képek az `euclidean` heurisztikával,
átlós mozgással, `0,11 m` inflációval és Bezier-simítással készültek.

A vizsgálat nem jelent statisztikai összehasonlítást: egy rögzített jelenet
egy futását dokumentálja. Több forgatókönyvhöz külön kell változtatni például
a kezdő- és célcellát, az inflációt, a heurisztikát, a simítást vagy a DWA
`alpha`, `beta`, `gamma` súlyait, majd azonos módon menteni és összevetni a
képeket és a mérőszámokat.

## 7. Ellenőrzés

Lefutott a kért `python -m codes_diploma.simulation` parancs; a grafikus
ablakos működés miatt a folyamatot a képernyőmentésre szolgáló vezérelt futás
egészítette ki. A vezérelt futás hat képet mentett a
`codes_diploma/astar_project/results/figures/` mappába, összesen 726 animációs
képkockával. A képeken ellenőrizhető az A* tervezési szakasz, a DWA jelölt
pályái, a fékezési megjelenítés és a cél elérése.

---

# `experiments.py` és `run_experiment.py` – heurisztika- és mozgásmód-vizsgálat

## 1. A vizsgálat célja

Az összehasonlító mérés négy heurisztikát vizsgál azonos pályákon:
Manhattan, Euklideszi, Chebyshev és octile. Minden pálya két módban fut:
átlós mozgással (`diagonal=True`) és csak négy főirányú mozgással
(`diagonal=False`). Így külön látható a heurisztika hatása, valamint az,
hogy az átlós lépés megengedése vagy tiltása megváltoztatja-e a megoldhatóságot.

## 2. Pályák és adatfolyam

A `build_experiment_scenarios()` négy rögzített pályát készít:

- `original_simulation`: az eredeti `simulation.py` 30×20 cellás fal- és
  átjáróelrendezése, start `(2,2)` és cél `(17,27)` ponttal;
- `compact_corridor`: ennek kisebb, 10×7 cellás szemléltető változata;
- `corner_cutting`: saroknál elhelyezett akadályok, ahol a közös sarok
  átvágását a `GridMap.get_neighbors()` tiltja;
- `diagonal_only`: kereszt alakú akadály, amelyben a start és a cél között
  csak egy nem engedélyezett átlós átkelés lenne.

Az `original_simulation` pálya az eredeti szimuláció fal- és átjáróelrendezését
használja. A `compact_corridor` ennek kisebb, 10×7 cellás változata. A képek
elsődleges eredménye az eredeti térképen készült; az inflációt és a DWA
mozgó akadályait ez az A* összehasonlítás külön nem tartalmazza.

A `run_scenario_comparison()` minden pályát mindkét mozgásmódban, azon belül
mind a négy heurisztikával lefuttat. A `compare_heuristics()` az A* részletes
eredményéből a következőket menti: sikeresség, útvonal költsége, útvonalhossz,
vizsgált csomópontok száma és maga az útvonal. A `write_results()` az útvonal
kivételével CSV-be írja az összehasonlítható mérőszámokat.

## 3. Eredmények

Az eredményfájl:

`codes_diploma/astar_project/results/tables/heuristic_comparison.csv`

Összesen 32 sor készült: 4 pálya × 2 mozgásmód × 4 heurisztika.

Az `original_simulation` pályán főirányú mozgásnál minden heurisztika 40,00
költségű utat talált. Átlós mozgásnál a Manhattan költsége 32,38, az
Euklideszi, Chebyshev és octile változatoké 31,21 lett. Ez a különbség nem
heurisztikai hiba, hanem az engedélyezett mozgások és a heurisztika együttese.

A `compact_corridor` pályán az átjárók miatt minden konfiguráció talált utat.
Főirányú módban a költség `15,0`, átlós módban `12,0711` lett. Az
`diagonal_only` pályán viszont mind a négy heurisztika helyesen `success=False`
eredményt adott nem átlós és átlós módban is: a cél körüli akadályok miatt a
tiltott sarokátvágással sem lehet szabályos útvonalat létrehozni.

## 4. Sarokvágás kezelése

Átlós mozgás esetén sem elég azt ellenőrizni, hogy az átlós célcella szabad-e.
A `GridMap.get_neighbors()` a két köztes oldalsó cellát is megvizsgálja. Ha
például `(1,1)` cellából a `(2,2)` cellába lépne a robot, akkor a `(1,2)` és
`(2,1)` cellának is szabadnak kell lennie. Ha valamelyik akadály, az átlós
szomszédot elutasítja. Ez akadályozza meg, hogy a robot két akadály közös
sarkán fizikailag átvágjon.

A `corner_cutting` teszt ezt ellenőrzi: a talált út nem tartalmazza a
tiltott `(2,2)` sarokátvágási cellát. A teszt ugyanakkor azt is ellenőrzi,
hogy a pálya kerülő úton továbbra is megoldható marad.

## 5. Konkrét költségpélda

Az eredeti szimulációs pályán a start `(2,2)`, a cél `(17,27)`. Főirányú
módban 40 egyenes lépés szükséges. Átlós mozgásnál a start és a cél
koordinátakülönbsége `15` sor és `25` oszlop, ezért az ideális, akadályt nem
keresztező geometriai alsó becslés 15 átlós és 10 egyenes lépés:

```text
15 * sqrt(2) + 10 * 1
= 15 * 1,41421356 + 10
= 31,2132
```

Az eredeti falak miatt a tényleges út ennél hosszabb lehet. A mérésben a
Manhattan változat 32,38, a másik három heurisztika 31,21 költséget adott;
ez azt is megmutatja, hogy a Manhattan heurisztika átlós költség mellett nem
ugyanolyan természetes választás, mint az octile vagy az Euklideszi heurisztika.

Az egyenes lépés költsége 1 cella, az átlós lépés költsége
`sqrt(2) ≈ 1,4142` cella. A heurisztika a kibővített csomópontok számát
befolyásolhatja, de szabályos, megengedett mozgásoknál nem vezethet
olcsóbb útvonalhoz az optimálisnál.

## 6. Indítás és tesztelés

Az összehasonlítás indítása:

```text
python -m codes_diploma.astar_project.run_experiment
```

A célzott tesztek:

```text
python -m unittest codes_diploma.astar_project.tests.test_experiments codes_diploma.astar_project.tests.test_astar_baseline codes_diploma.astar_project.tests.test_grid_map -v
```

A futtatás eredménye: 13 teszt sikeres. A tesztek ellenőrzik mind a négy
heurisztika és mindkét mozgásmód lefutását, a nem átlós módban elutasított
megoldhatatlan pályát és a sarokvágás tiltását.

## 7. Az egységes, kontrasztos összehasonlító ábrák

Az aktuális ábrák ismét egyetlen térképen jelenítik meg mind a négy heurisztika útvonalát. A heurisztikákat nagy kontrasztú színek különböztetik meg: Manhattan kék, Euklideszi narancssárga, Chebyshev zöld, Octile lila. A folytonos vonal az átlós mozgás tiltását, a szaggatott vonal az átlós mozgás engedélyezését jelenti. Az útvonalak vastagok, fehér kontúrt kapnak, ezért a szomszédos vagy egymást fedő szakaszok is jobban elkülönülnek. A kezdőpont zöld `S`, a célpont piros `G` jelölést kapott.

Az ábrákat a `python -m codes_diploma.astar_project.generate_comparison_figures` parancs generálja újra. A program minden forgatókönyvhöz egy képet ment a `codes_diploma/astar_project/results/figures/` könyvtárba.

### 7.1. Eredeti szimulációs térkép

**Kép:** `heuristics_original_simulation.png`

**Képaláírás:** *A négy A* heurisztika útvonalainak összehasonlítása az eredeti szimulációs térképen.*

**Beilleszthető szöveg:**
Az ábra ugyanazon, 30×20 cellás térképen mutatja be a Manhattan, Euklideszi, Chebyshev és Octile heurisztika által talált útvonalakat. A szín a heurisztikát, a vonal típusa pedig a mozgási módot jelöli. Így egyetlen térképen látható, hogy az átlós lépések engedélyezése rövidebb útvonalakat eredményezhet, miközben az akadályok megkerülésének szabályai minden változatban érvényben maradnak.

### 7.2. Kisebb, átjárós ellenőrző pálya

**Kép:** `heuristics_compact_corridor.png`

**Képaláírás:** *Heurisztika-összehasonlítás kisebb, átjárókat tartalmazó rácstérképen.*

**Beilleszthető szöveg:**
A kisebb ellenőrző pálya egy függőleges és egy vízszintes akadályfalon kialakított átjárókat tartalmaz. Az ábra azt szemlélteti, hogy az összes vizsgált heurisztika képes megtalálni a falak közötti szabályos útvonalat, az átlós mozgás pedig csökkenti az útvonal geometriai költségét.

### 7.3. Sarokvágási vizsgálat

**Kép:** `heuristics_corner_cutting.png`

**Képaláírás:** *A sarokvágás elleni szomszédvizsgálat hatása átlós mozgásnál.*

**Beilleszthető szöveg:**
Az átlós mozgás engedélyezése mellett az algoritmus nem léphet át két akadály közös sarkán. A szomszédvizsgálat a két köztes oldalsó cellát is ellenőrzi, ezért a megtalált útvonal szabályos kerülőutat használ.

### 7.4. Megoldhatatlan pálya

**Kép:** `heuristics_diagonal_only.png`

**Képaláírás:** *Megoldhatatlan rácspálya felismerése két mozgási módban.*

**Beilleszthető szöveg:**
A kereszt alakú akadályrendszer elzárja a kezdő- és a célcellát. Egyik heurisztika sem tud szabályos útvonalat létrehozni, ezért az algoritmus mindkét mozgási módban helyesen jelzi a `NO PATH` eredményt. Ez megerősíti, hogy a heurisztika a keresés sorrendjét befolyásolja, az akadály- és szomszédsági szabályokat nem írja felül.
## 7. K?tpaneles, szimul?ci?s st?lus? ?sszehasonl?t? ?bra

Az aktu?lis k?p az eredeti `python -m codes_diploma.simulation` t?rk?prajzol?si
st?lus?hoz igazodik. A t?rk?p k?t egym?s melletti panelen l?that?: balra a
n?gyir?ny?, jobbra az ?tl?s mozg?st is enged?lyez? A* keres?s eredm?nye. Mindk?t
panelen egyszerre szerepel a Manhattan, Euklideszi, Chebyshev ?s Octile
heurisztika. Az akad?lyok sz?rk?s t?glalapok, a cellahat?rok finom r?csvonalak,
az ?tvonal pedig v?kony, szaggatott vonal apr? csom?ponti jel?l?sekkel. Ez a
jel?l?s k?zelebb ?ll a szimul?ci? eredeti A* ?tvonal-megjelen?t?s?hez, ?s nem
takarja el az akad?lyokat vagy a t?bbi ?tvonalat.

**K?p:** `heuristics_original_simulation.png`

**K?pal??r?s:** *A n?gy A* heurisztika ?sszehasonl?t?sa az eredeti szimul?ci?s
t?rk?pen: balra a n?gyir?ny?, jobbra az ?tl?s mozg?st is enged?lyez? eset.*

**Beilleszthet? sz?veg:**
Az ?bra az eredeti szimul?ci? t?rk?pelrendez?s?t ?s megjelen?t?si logik?j?t
k?veti. A bal oldali panelen csak a n?gy f?ir?ny, a jobb oldali panelen pedig
az ?tl?s szomsz?dcell?k is haszn?lhat?k. Az ?tvonalakat a sz?nek k?l?n?tik el,
a v?kony szaggatott vonal ?s az apr? csom?ponti jel?l?s pedig az A* r?cs?tvonal
alakj?t mutatja. A vil?gkoordin?t?s tengelyek miatt az ?bra a szimul?ci?ban
l?that? t?rk?phez hasonl?an ?rtelmezhet?.


## 8. Val?di szimul?ci?s t?rk?pen v?gzett heurisztika-?sszehasonl?t?s

A `simulation_heuristic_comparison.py` k?l?n ?sszehasonl?t? ?br?t k?sz?t az
alap szimul?ci? t?rk?p?p?t?s?t felhaszn?lva. A `simulation.create_scene()`
hozza l?tre a 30?20 cell?s t?rk?pet, majd az `inflation_radius=0.1` param?terrel
a `GridMap.inflate_obstacles()` biztons?gi z?n?val kib?v?ti az akad?lyokat. Ez
fontos k?l?nbs?g a puszt?n nyers akad?lycell?kat rajzol? k?s?rleti ?br?khoz
k?pest: az ?tvonaltervez?s a robot k?r?li tiltott r?hagy?st is figyelembe veszi.

A program mind a n?gy heurisztik?hoz l?trehozza az `AStarDWAPlanner` p?ld?ny?t,
majd a `plan_global()` f?ggv?nyt futtatja egyszer n?gyir?ny? ?s egyszer ?tl?s
mozg?ssal. Az ?gy kapott, nem sim?tott A* glob?lis ?tvonalakat egy k?z?s, k?t paneles ?br?n jelen?ti meg. A bal panel a n?gyir?ny?, a jobb panel az ?tl?s mozg?s eredm?nye; mindk?t panelen egyszerre l?that? mind a n?gy heurisztika. Az akad?lyok ?s a biztons?gi z?na v?ltozatlanul az alap szimul?ci?b?l sz?rmaznak, a heurisztik?kat pedig csak elt?r? sz?nek k?l?nb?ztetik meg. A panelenk?nti jelmagyar?zat az ?tvonal-k?lts?get jel?li.

**Kimeneti k?p:** `astar_project/results/figures/simulation_heuristic_comparison.png`

**?jragener?l?s:**

```text
python -m codes_diploma.astar_project.generate_simulation_heuristic_comparison
```

A friss?tett v?ltozatban a n?gy heurisztika kontrasztos sz?neket kapott. A t?rk?p ?s az ?tvonalak geometri?ja nem v?ltozott, ?gy a megjelen?t?s csak az elk?l?n?thet?s?get jav?tja.

Ez az ?bra a megl?v? `heuristics_original_simulation.png` k?pet nem ?rja fel?l;
a k?t k?p elt?r? c?lt szolg?l. A megl?v? k?p a kor?bbi vizu?lis ?sszehasonl?t?
st?lust ?rzi meg, az ?j k?p viszont az alap szimul?ci? t?nyleges, infl?lt
GridMap-j?re ?s A*+DWA ?tvonaltervez?j?re ?p?l.
## 6. Ind?t?s ?s tesztel?s

Az ?sszehasonl?t?s ind?t?sa:

```text
python -m codes_diploma.astar_project.run_experiment
```

A c?lzott tesztek:

```text
python -m unittest codes_diploma.astar_project.tests.test_experiments codes_diploma.astar_project.tests.test_astar_baseline codes_diploma.astar_project.tests.test_grid_map -v
```

A k?s?rleti tesztek ellen?rzik a n?gy heurisztika ?s a k?t mozg?si m?d lefut?s?t, a sarokv?g?s tilt?s?t ?s a megoldhatatlan p?lya kezel?s?t.

## 7. A `simulation_heuristic_comparison.png` ?bra le?r?sa

**K?p:** `astar_project/results/figures/simulation_heuristic_comparison.png`

**K?pal??r?s:** *A n?gy A* heurisztika ?sszehasonl?t?sa az eredeti, akad?lyinfl?ci?val kib?v?tett szimul?ci?s t?rk?pen: balra a n?gyir?ny?, jobbra az ?tl?s mozg?s.*

**Beilleszthet? sz?veg:**

Az ?bra az alap szimul?ci? `create_scene()` f?ggv?ny?vel l?trehozott, 30?20 cell?s t?rk?pet haszn?lja. A t?rk?p akad?lyai az `inflation_radius=0.1` param?terrel vannak kib?v?tve, ez?rt a sz?rke akad?lyter?let a robot sz?m?ra fenntartott biztons?gi z?n?t is tartalmazza.

A bal oldali panelen az A* csak fel, le, balra ?s jobbra l?phet. A jobb oldali panelen az ?tl?s szomsz?dcella is enged?lyezett. Mindk?t panelen ugyanaz a n?gy heurisztika fut le az `AStarDWAPlanner.plan_global()` f?ggv?nyen kereszt?l, sim?t?s n?lk?l. A k?t panel ugyanazon szimul?ci?s t?rk?pen hasonl?tja ?ssze a mozg?si szab?lyokat.

A heurisztik?k sz?nei:

- Manhattan: k?k;
- Euklideszi: narancss?rga;
- Chebyshev: z?ld;
- Octile: magenta.

A panelenk?nti jelmagyar?zat az adott ?tvonal k?lts?g?t mutatja. A geometriai ?tvonalak a t?nyleges, infl?lt `GridMap`-b?l sz?rmaznak; a sz?nek csak az ?tvonalak vizu?lis elk?l?n?t?s?t szolg?lj?k.

**?jragener?l?s:**

```text
python -m codes_diploma.astar_project.generate_simulation_heuristic_comparison
```

A kor?bbi `heuristics_original_simulation.png` k?pet meghagytam, de a szakdolgozati le?r?s ehhez az ?j, biztons?gi z?n?t is tartalmaz? `simulation_heuristic_comparison.png` k?phez tartozik.
## 8. ROS 2 A* + DWA akadályinfláció és útvonalhiba

Az `astar_dwa_node.cpp` az odometriából, a célból és a statikus akadályokból
A* rácstérképet készít, majd a DWA-val sebességet küld a `/cmd_vel` témára.
A mostani javítás az akadályinflációt érinti: a korábbi négyzetes tiltás
lezárhatta a fizikailag átjárható réseket.

A paraméterek szerint a rács felbontása `resolution=0.20 m`, a robot sugara
`robot_radius=0.28 m`. Egy 0,35 m sugarú akadálynál a biztonsági sugár:

```text
0,35 m + 0,28 m = 0,63 m
```

Az új kód a cellaközéppont és az akadályközéppont euklideszi távolságát méri:

```text
d = sqrt((x_c - x_o)^2 + (y_c - y_o)^2)
```

ahol `x_c,y_c` a cellaközéppont, `x_o,y_o` az akadály középpontja méterben.
Csak a `d <= 0,63 m` feltételnek megfelelő cellák lesznek blokkoltak.
Korábban a teljes négyzetes rácsblokk tiltott volt, így két akadály között
összeérhettek a biztonsági zónák.

Például 1,80 m középponttávolság és két 0,63 m-es biztonsági sugár esetén:

```text
1,80 m - 2 * 0,63 m = 0,54 m
```

marad geometriai szabad távolság. A kör alakú infláció ezért kevésbé
konzervatív, miközben a robot sugarát továbbra is figyelembe veszi.

Ha a kezdő- vagy célcella kívül esik a térképen, vagy blokkolt, a node most
diagnosztikai figyelmeztetést ír ki a `start=(row,column)`, `goal=(row,column)`,
`start_blocked` és `goal_blocked` értékekkel. Ez megmutatja, hogy érvénytelen
cella vagy ténylegesen megszakadt A* kapcsolat okozza-e az üres útvonalat.

A DWA külön réteg: az A* útvonal megtalálása után a LiDAR-pontok alapján még
megállíthatja a robotot, ha minden kipróbált sebességpálya ütközne. A javítás
az A* statikus térképét teszi pontosabbá, a lokális LiDAR-viselkedést nem
rejti el.

Ellenőrzés:

```bash
colcon build --symlink-install --packages-select astar_dwa_controller
```

Ezután az `/astar_path`, `/astar_map` és `/astar_dwa_markers` témákon lehet
ellenőrizni, hogy a két akadály közötti útvonal létrejön-e.
## 9. A ROS 2 A* + DWA tesztelési vizualizációja és sebességkorlátja

Az `astar_dwa_node.cpp` vezérlője két külön feladatot végez. Az A* a statikus
akadályokból útvonalat készít, a DWA pedig a LiDAR alapján kiválasztja a
következő sebességpárt. A tesztelés áttekinthetőbb lett az RViz
`/astar_dwa_markers` témáján:

- zöld vonal: A* útvonal;
- kék vonal: az aktuálisan kiválasztott DWA-előrejelzés;
- piros hengerek: ismert statikus akadályok;
- halványsárga lapok: statikus akadály plusz robot-sugár biztonsági zónája;
- sárga pontok: a LiDAR által éppen érzékelt akadálypontok;
- kék áttetsző henger és nyíl: robotpozíció és haladási irány.

A maximális lineáris sebesség most paraméterezett. A `rosbot.yaml`
`max_linear_velocity=0.32 m/s` értéke azt jelenti, hogy a kiadott
`Twist.linear.x` nem lehet nagyobb 0,32 m/s-nél. A korábbi kód ezt 0,20 m/s-ra
korlátozta, miközben a DWA 0,40 m/s-ig vizsgált sebességeket. A
`max_angular_velocity=1.00 rad/s` az elfordulási sebesség felső határa.

A vezérlő ciklusa 0,10 s. Az új lineáris gyorsítási lépés legfeljebb 0,08 m/s
ciklusonként, vagyis ideális esetben:

```text
0,32 m/s / 0,08 m/s = 4 ciklus
4 * 0,10 s = 0,40 s
```

alatt éri el a maximális értéket. Ez nem gyorsítja fel a veszélyes helyzeteket:
az ütközésvizsgálat minden DWA-jelölt pályán továbbra is lefut.

Az RViz-es vizsgálat menete:

1. `/astar_path`: van-e globális útvonal;
2. `/astar_map`: a statikus biztonsági zónák helye;
3. sárga LiDAR-pontok: lát-e a robot váratlan akadályt;
4. kék DWA-vonal: a lokális vezérlő merre tervezi a következő 1,5 másodpercet.

Ha zöld útvonal van, de a kék vonal rövid vagy a robot áll, akkor a DWA
LiDAR-biztonsági ellenőrzése állította meg. Ha zöld útvonal sincs, akkor az
A* statikus térképét vagy a célt kell ellenőrizni.

## 10. A Gazebo mozgó akadály működése és javítása

### A fájlok célja

A mozgó akadály működését három fájl együtt adja:

- `worlds/dwa_world.sdf`: a `moving_obstacle` Gazebo-modellje;
- `dwa_gazebo_sim/moving_obstacle_node.py`: a modell új pozícióját számítja;
- `launch/bridge_and_controller.launch.py`: ROS 2 service bridge-et indít a
  Gazebo `/world/dwa_world/set_pose` szolgáltatásához.

### Adatfolyam

Az akadály kezdeti világkoordinátája `(x, y, z) = (3.0, 1.8, 0.45) m`.
A `moving_obstacle_node` 0,05 másodpercenként frissítési ciklust futtat. A
pozíció y-koordinátája:

```text
y(t) = 1,8 + 1,2 * sin(0,6 * t) m
```

Itt `t` a node által követett idő másodpercben, a `1,8 m` a középvonal, a
`1,2 m` a kitérés amplitúdója, a `0,6 1/s` pedig a szögsebesség jellegű
szorzó. Például `t = 0 s` esetén:

```text
y(0) = 1,8 + 1,2 * sin(0) = 1,8 m
```

`t = 2 s` esetén `0,6 * 2 = 1,2`, ezért
`y(2) ≈ 1,8 + 1,2 * 0,932 ≈ 2,92 m`. Az x-koordináta végig `3,0 m`,
tehát az akadály függőleges irányban mozog.

### Mi akadályozta a mozgást?

Korábban a world fájlban ez szerepelt:

```xml
<static>true</static>
```

Ez azt jelentette, hogy a Gazebo a modellt statikus objektumként kezelte.
Ezt `<static>false</static>` értékre módosítottam. Ezen kívül a node ugyan
meghívta a service klienst, de a launch fájl nem bridge-elte a
`SetEntityPose` szolgáltatást. Most ez is bekerült:

```text
/world/dwa_world/set_pose@ros_gz_interfaces/srv/SetEntityPose
```

Ez a kapcsolat továbbítja a ROS 2 service-kérést a Gazebo transport felé.

### A node biztonságos frissítése

A node a `request_in_flight` állapottal biztosítja, hogy ne küldjön új
pozíciókérést addig, amíg az előző válasz meg nem érkezett. Így a 20 Hz-es
timer nem halmozza fel a Gazebo service-kéréseket. A válasz `success` mezőjét
ellenőrzi, és sikertelen frissítésnél figyelmeztetést ír a ROS 2 naplóba.

### Ellenőrzés

A módosítás után lefutott:

```bash
colcon build --symlink-install --packages-select dwa_gazebo_sim
python3 -m py_compile moving_obstacle_node.py
```

A futási ellenőrzés során a Gazebo pose-adatában a `moving_obstacle` y-értéke
változott, például `2,8703 m`, majd `2,8536 m`, később `2,8359 m` lett. Ez
igazolja, hogy az akadály már nem csak a node-ban számolja a pályát, hanem a
Gazebo-modell tényleges pozíciója is frissül.

## 11. A mozgó akadály kezelése az A* + DWA C++ vezérlőben

### A fájl célja

Az `astar_dwa_node.cpp` a ROS 2 vezérlőben két külön feladatot kapcsol össze:
az A* egy rövid, globális útvonalat keres, a DWA pedig a következő útvonalpont
felé választ sebességet. A korábbi működésben az A* csak a YAML-ben megadott
statikus akadályokat használta. A mozgó akadályt ugyan látta a LiDAR, de az A*
útvonala nem változott, ezért az útvonal a dinamikus akadályon keresztül is
vezethetett.

### Adatfolyam és módosítás

A vezérlési ciklus az `obstacles()` függvénnyel a `/scan` LaserScan mérési
pontjait világkoordinátára alakítja, és csak a robot előtti, legfeljebb 3,0 m-es
tartományt tartja meg. Az aktuális LiDAR-akadályokat a lokális DWA használja; a globális A* rács
továbbra is a statikus akadálymodellt használja, a Python-szimulátor logikájával
összhangban.

### Fontos függvények

- `obstacles()`: a LiDAR-pontokat szűri és `Obstacle{x, y, radius}` adatokká
  alakítja;
- `astar(const std::vector<Obstacle>& sensed_obstacles, bool use_sensed)`:
    a `control()` jelenleg `astar({}, false)` formában hívja, tehát csak a
    statikus térképből építi a rácsot; a LiDAR-listát a lokális DWA kezeli;
- `dwa(target_x, target_y, target_index, sensed)`: előrehaladó és helyben
    forduló keréksebességpárokat vizsgál, a negatív lineáris sebességet kizárja;
    az elfogadott jelölteket útvonalközelséggel is pontozza;
- `control()`: egy ciklusban egyszer gyűjti a LiDAR-akadályokat, újratervez,
  kiválasztja a waypointot, majd publikálja a `/cmd_vel` üzenetet.

### DWA biztonsági változás

A DWA előremenő és helyben forduló jelölteket vizsgál, `0.1 s` lépéssel,
a helyi cél távolságától függő `0.8...2.0 s` időtávon. A LiDAR-pontok sugara
`0 m`; a YAML szerinti robotsugár `0.24 m`, a statikus tartalék `0.04 m`, a mozgó
akadályoké `0.10 m`. Például álló ponttól `0.36 m` távolságban a szabad tér
`0.36 - (0.24 + 0.04 + 0) = 0.08 m`: először a test és a tartalék együttes
sugarát számoljuk ki, majd ezt levonjuk a középpontok távolságából. Ebben a
példában nincs ütközés. Mozgó pontnál ugyanott `0.02 m` maradna.

Az ütközésjelzés a kezdeti szabad távolsághoz is viszonyít, így a már
biztonsági margón belül lévő robot nem minden mozdulatát tiltja le. Az
elfogadást ezután a fékezhetőség és a `min_ttc` feltétel dönti el. Ha nincs
elfogadott minta, a DWA nulla lineáris sebességgel az akadálytól elfelé fordul;
a forgásirányt a `recovery_dir_` őrzi. Ez nem tolatás és nem célirányú forgás.

### Miért oldja meg az elakadást?

Ha a mozgó akadály a globális A* útvonalra kerül, a DWA a lokális
előrejelzésben kerüli ki vagy fékezi le. A LiDAR minden mérési pontját nem
szabad külön A* akadályként inflálni, mert egy fizikai akadály sok sűrű pontot
ad, és a cellák körüli zónák tévesen teljes átjárókat zárhatnak le.

### Ellenőrzés

A csomag ROS2-környezetben ellenőrizhető az alábbi paranccsal:

```bash
source /opt/ros/jazzy/setup.bash
cd ros2_astar_dwa_gazebo
colcon build --packages-select astar_dwa_controller --symlink-install
```

A korábbi build eredménye nem igazolja az új pontozás Gazebo-beli működését.
Az RViz-ben az `/astar_path`, a sárga LiDAR-pontok
és a kék DWA-trajektória együttesét kell figyelni. Ha a robot mégsem halad,
a vezérlő naplójában az `Az A* nem talált elérhető útvonalat` üzenet
különválasztja a valódi útvonalhiányt a DWA biztonsági megállásától.

## 12. A ROS/Gazebo térkép és a Python-szimulátor összehangolása

A ROS/Gazebo változat most a Python `simulation.py` alapértelmezett térképét
használja referenciaként. A rács 30 oszlopból és 20 sorból áll, a
`resolution=0,2 m`, ezért a tervezési terület 6,0 m széles és 4,0 m magas.
A rács origója `(0,0) m`, így a `(2,2)` kezdőcella középpontja:

```text
x = (2 + 0,5) * 0,2 = 0,5 m
y = (2 + 0,5) * 0,2 = 0,5 m
```

A `(17,27)` célcella középpontja ugyanígy `(5,5; 3,5) m`. A függőleges
akadálysor a 10. oszlopban, a 7-12. sorok között nyitott réssel, a vízszintes
akadálysor pedig a 12. sorban, a 19-24. oszlopok közötti nyitott réssel
szerepel. A Gazebo SDF-ben ezek összefüggő, 0,2 m vastag falszakaszokként
jelennek meg; ez a cellák fizikai megfelelője.

### A két mozgó akadály

A Python-szimulátorban szereplő akadályok ROS oldali kezdőpozíciója és
sebessége:

```text
moving_obstacle_1: (2,4; 0,4) m + (0; 0,20) m/s * t
moving_obstacle_2: (6,8; 2,1) m + (-0,25; 0) m/s * t
```

Például 5 másodpercnél az első akadály helye
`(2,4; 1,4) m`, a másodiké pedig `(5,55; 2,1) m`. A
`moving_obstacle_node.py` ezeket a pozíciókat a
`/world/dwa_world/set_pose` szolgáltatáson keresztül adja át a Gazebónak.
Egyszerre csak egy service-kérés van függőben, ezért az akadályfrissítés nem
halmozódik fel.

### A DWA működési egyezése

Az `astar_dwa_node.cpp` DWA-része a Python-változattal közös kinematikai
alapokat használ, de a paraméterezése nem mindenben azonos. A jelenlegi
ROS2 YAML szerint a keréksugár `0,033 m`, a keréktávolság `0,08 m`, a
maximális keréksebesség `15 rad/s`, a mintavételi lépés `0,5 rad/s`, a
gyorsulási korlát `1,8 m/s²`, `dt=0,1 s`, a maximális előrejelzési idő `2 s`.
A biztonsági ráhagyás mozgó akadálynál `0,10 m`, állónál `0,04 m`; a
jutalomsúlyok `alpha=5`, `beta=3`, `gamma=2`. A két új távolságbüntetés
részleteit a 14. fejezet tartalmazza.

Egy bal és jobb keréksebességből a Python- és ROS-kód azonos módon számolja:

```text
v = ((w_L + w_R) / 2) * r
w = ((w_R - w_L) / (2 * b)) * r
```

Például `w_L=w_R=10 rad/s` esetén `v=0,33 m/s`, `w=0 rad/s`, tehát a robot
egyenesen halad. A ROS DWA a dinamikus ablakban ezeket a keréksebességeket
vizsgálja, a pályát 0,1 s-os lépésekben integrálja, és az ütközésig mért
távolság alapján alkalmazza a Python-féle megállíthatósági feltételt:

```text
|v| <= sqrt(2 * a_max * distance_to_obstacle)
```

Ez a dokumentáció és az `ASTAR_PROJEKT_FOLYAMATBRA.gv` az új,
keréksebesség-alapú ROS DWA-hívási sorrendet tükrözi.

---

# `astar_dwa_node.cpp` – ROS odometria, cél és A* útvonal ellenőrzése

## 1. A fájl célja

Az `astar_dwa_node.cpp` a ROS 2 és Gazebo közötti vezérlőcsomópont. Az
`/odom` és `/scan` adataiból felépíti a robot aktuális állapotát és a
pillanatnyi akadályképet, az RViz `/goal_pose` üzenetéből célt vesz át, majd
A*-útvonalat és DWA-sebességet publikál `/astar_path` és `/cmd_vel` témákon.

## 2. Odometriai kezdőeltolás

A TurtleBot Gazebo odometria-pluginja a robot spawnhelyéhez képest lokális
koordinátát ad vissza, miközben a modell `(0.8, 0.8)` méteren spawnol. Ezért a
konfigurációban `initial_pose_x = 0.8 m` és `initial_pose_y = 0.8 m`. Az `odom()`
ezt a világkoordinátára állító offsetet adja hozzá:

```cpp
pose_.x = msg->pose.pose.position.x + initial_pose_x_;
pose_.y = msg->pose.pose.position.y + initial_pose_y_;
```

A Gazebo-odom `(0, 0)` mérés így a tervezőben `(0.8, 0.8)` világpozícióvá
válik. `resolution = 0.2 m/cella` mellett ez:

```text
column = floor(0.8 / 0.2) = 4
row    = floor(0.8 / 0.2) = 4
```

tehát a Python-szimulátor kezdőcellája `(4, 4)`, nem egy kétszeresen eltolt
pozíció.

## 3. Cél- és útvonal-adatfolyam

Az RViz `2D Goal Pose` eszköze `geometry_msgs/msg/PoseStamped` üzenetet küld
`/goal_pose` témán. A node a világkoordinátás `x` és `y` értéket eltárolja,
majd a vezérlési ciklusban a jelenlegi pozícióból és a célból cellát készít.
Az A* eredménye `nav_msgs/msg/Path` formában jelenik meg `/astar_path`-on;
az útvonal pontjai az `odom` frame-ben, 0,2 méteres cellaközéppontokként
szerepelnek. A következő waypointot a DWA lokális vezérlése követi, amely a
`/cmd_vel` Twist üzenetet publikálja.

## 4. Biztonsági feltételek

Odometria nélkül a vezérlő nem tervez. Érvénytelen vagy foglalt kezdő- illetve
célcella esetén az A* figyelmeztetést ír, üres útvonalat publikál és nulla
sebességgel állítja meg a robotot. Ezért a `/astar_path` topic megléte önmagában
nem elég: az üzenet `poses` tömbjének is tartalmaznia kell útvonalpontokat.

## 5. Ellenőrzött futás

A javítás ellenőrzéséhez a következő parancs futott:

```bash
colcon build --packages-select astar_dwa_controller --symlink-install
```

A build sikeres volt. Tiszta Gazebo- és bridge-indítás után a `/goal_pose`
cél `(5.50, 3.50)` értékkel érkezett meg, a node `ut=27 pont` útvonalat írt
a naplóba, és az `/astar_path` üzenet 27, a célhoz vezető pontot tartalmazott.

---

# Pályahatár-védelem és a Gazebo-pálya nagyítása

A korábbi `6,0 m x 4,0 m` térkép csak az A* cellakeresésének határa volt. A DWA
előrejelzése azonban kizárólag a LiDAR által érzékelt akadályokat vizsgálta,
ezért a pálya szélén nem volt olyan feltétel, amely a sebességjelöltet
elutasította volna. A Gazebo-világban sem volt fizikai határfal.

Az aktuális pálya `8,0 m x 5,0 m`, `0,2 m/cella` felbontással, vagyis
`40 x 25` cellás. A robot kezdőpontja `(0,8 m, 0,8 m)`, amelynek cellája:

```text
column = floor(0.8 / 0.2) = 4
row    = floor(0.8 / 0.2) = 4
```

A DWA most minden előrejelzett pontnál ellenőrzi a
`robot_radius + safety_margin = 0,28 + 0,15 = 0,43 m` biztonsági sávot.
Ez azt jelenti, hogy a robot középpontja nem közelítheti meg a pálya szélét
`0,43 m`-nél jobban. Például az alsó határnál a megengedett tartomány kezdete
`y = 0,43 m`; az ennél kisebb `y` értéket eredményező DWA-jelöltet a node
veszélyesnek jelöli és nem választja ki.

A világfájl négy statikus falat is tartalmaz a `0..8 m` és `0..5 m` terület
körül. Így a vizuális pálya és a tervező rácsa ugyanazt a koordinátatartományt
használja. Ha a robot már a biztonsági határon kívül van, a vezérlő nulla
`/cmd_vel` értéket küld, és figyelmeztetést ír a naplóba.

A ROS- és Python-DWA közötti fontos különbség, hogy a ROS-vezérlő a
keréksebesség-jelöltekből számított `v` és `w` értékeket publikálja. Ha a
jelölt túllépi a publikált sebességhatárt, a korábbi kód csak a végső Twist
üzenetet vágta le. Például egy `w = 1,86 rad/s` jelöltből `1,0 rad/s` került
ki a topicra, miközben a belső kerékállapot továbbra is az `1,86` értékű
jelöltet követte. Ez eltérést okozott a tervezett és a tényleges mozgás között.
Az aktuális kód már a DWA pontozása előtt elutasítja azokat a jelölteket,
amelyek `v > 0,32 m/s` vagy `|w| > 1,0 rad/s` értéket adnak.

Ha a LiDAR-biztonsági feltétel, a pályahatár vagy a sebességkorlát miatt egyetlen
előremeneti jelölt sem marad, a node ezt külön kezeli. A korábbi keréksebesség
helyett lenullázza a kerékállapotot, és a cél irányába legfeljebb
`1,0 rad/s` helyben forgást ad vissza. Így a robot nem marad csendben nulla
sebességen egy régi vagy érvénytelen DWA-állapot miatt.

---

# Iránybaállítás a körkörös mozgás elkerülésére

A vezérlő a következő waypoint és a robot aktuális `pose_.yaw` értéke alapján
irányhibát számol:

```text
heading_error = wrap(atan2(target_y - pose_y, target_x - pose_x) - yaw)
```

Az `atan2` a cél felé mutató szöget adja radiánban, a `yaw` a robot jelenlegi
irányultsága, a `wrap` pedig `[-pi, pi]` tartományba hozza a különbséget.
Például ha a célirány `1,2 rad`, a robot iránya `-0,2 rad`, akkor a hiba
`1,4 rad`, ezért a robot először helyben fordul, nem pedig előremenetben
köröz.

Az aktuális vezérlőben nincs külön `0,6 rad` feletti teljes megállási ág. A
heading-score, az akadálypredikció és a fékezhetőségi feltétel együtt dönti el,
hogy a DWA helyben forduljon, vagy lassú íves előremenetet válasszon. Ez azért
fontos a rés előtt, mert a korábbi külön ág minden nagyobb irányhibánál
`linear.x=0` értéket küldött, és a robot megtorpanhatott. A módosított logban
például `cmd=(0.15, 0.62)`, majd `cmd=(0.32, 0.21)` látható, ami előremeneti
befordulást jelent.

## 13. C++ DWA frissítés a Python referencia alapján

Az aktuális `dwa()` trajektória közben kumulálja az ívhosszt. Ha a pálya később
ér akadályt, a jelölt nem esik ki automatikusan: a `collision_dist` adja az
ütközésig megtett úthosszt méterben. A fékezhetőségi ellenőrzésben a sebesség
nem haladhatja meg a kétszeres gyorsulás és az úthossz szorzatának négyzetgyökét.
Például `2 m/s²` lassulásnál, `0.01 m` úthosszból a sebességhatár
`sqrt(2 * 2 * 0.01) = 0.2 m/s`. A `0.26 m/s` jelölt ekkor kiesik.
A külön `min_ttc` vizsgálat az ütközésig szükséges minimális időt ellenőrzi.

Az adaptív időtáv `clamp(goal_dist * 2.0, 0.8, predict_time_)`: a helyi
célpont méterben mért távolságát egy `2 s/m` tényező szorozza, majd a kód
`0.8 s` és a YAML-ben konfigurált `2.0 s` közé szorítja. `0.3 m` céltávolságnál
`0.6 s` adódna, ezért `0.8 s` lesz az időtáv. A sebességpont célsebességhez
viszonyít, az új útvonalközelségi tag ettől különálló büntetés.

Az A* akadályinflációjában a robot sugara, az akadály sugara és a
`planning_margin` szerepel. A `control()` a YAML alapján `0.40 m` ívhosszú
előretekintést használ; a diszkrét pontok miatt a kiválasztott waypoint ennél
távolabb is lehet. A `line_free()` a statikus akadályokon átvezető közvetlen
célpontot visszalépteti. A jelenlegi `obstacles()` a statikus falpontokat is
megtartja a DWA számára; a fal közelsége a sebességbecslést tiltja, nem a
pontok ütközésvizsgálatát.

Ellenőrzés:

```text
colcon build --packages-select astar_dwa_controller dwa_gazebo_sim --symlink-install
```

## 14. Visszatérés az A* útvonalra akadálykerülés után

Az alábbi pontozás az első javítás leírása. A jelenlegi, kétlépcsős döntést,
az új időtávot és a szigorított ütközésszűrést a 16. fejezet rögzíti;
a korábbi fékezhetőség-alapú ütközéselfogadás már nem érvényes.

### A vezérlő célja és a hiba oka

Az `astar_dwa_node.cpp` továbbra is a ROS2-integráció vezérlője. A módosítás a
lokális DWA pontozását érinti, nem az A* keresést és nem a Python-szimulátort.
A korábbi célirány-pont azt mérte, hogy az előrejelzés végén a robot orra
mennyire néz a helyi cél felé. Nem mérte külön, milyen messze marad az eredeti
útvonaltól, vagy ténylegesen közelebb kerül-e a célponthoz. Az akadálytávolság
és a sebesség jutalma ezért előnyben részesíthetett egy oldalra eltolt ívet.
Ez kódszinten igazolható hiányosság; a konkrét Gazebo-futás teljes ok-okozati
bizonyításához új szimulációs próba szükséges.

### Adatfolyam, függvények és adatok

A `control()` a `current_path_` világkoordinátás pontpárlistát követi. A
`waypoint_index_` csak előre halad: nyolc ponton belül a legközelebbi látható
waypointot keresi. Ezután az útvonal ívhosszán választ előretekintési célpontot,
és a `line_free()` segítségével ellenőrzi annak statikus láthatóságát.

A hívás most `dwa(target_x, target_y, target_index, sensed)`: az első két
paraméter a cél méterben megadott világkoordinátája, a harmadik az útvonalon
elfoglalt indexe, a negyedik az aktuális LiDAR-akadálylista. Visszatérése a
lineáris és szögsebesség párja, `m/s` és `rad/s` egységben. A jelöltek
dinamikus ablakát, gyorsuláskorlátját, fékezhetőségét és ütközési idővizsgálatát
a módosítás nem változtatja meg.

Az elfogadott rollout `(x, y)` végpontjára a `path_tracking::tracking_cost()`
büntetést számol. A vizsgált útvonaldarab a jelenlegi waypoint előtti ponttól
az előretekintési célpont utáni pontig tart, az útvonal határaihoz igazítva.
Így nem egy tetszőleges, későbbi útvonalág közelsége ad jutalmat, és a kerülés
utáni eltolás nem válik új referencia-egyenessé.

### Pontozás és számpélda

```text
score = alpha * heading_score + beta * clear_score + gamma * vel_score
    - path_distance_bias * path_distance
    - goal_distance_bias * target_distance
```

A `score` dimenzió nélküli összehasonlító érték, a nagyobb a jobb. A
`heading_score` a rollout végén a célirány és a robot iránya közötti abszolút
szöghibát vonja le a pi értékéből, majd pi-vel oszt; egysége nincs. A
`clear_score` a legkisebb megmaradt biztonsági távolságot `1 m`-hez viszonyítja
és 0 és 1 közé szorítja. A `vel_score` a jelölt sebesség és a célsebesség
abszolút különbségét osztja a maximális lineáris sebességgel, majd ezt kivonja
egyből. A súlyok dimenzió nélküliek: a forrásbeli alapértékek `alpha=5`,
`beta=2`, `gamma=3`; az összevezetett YAML ezeket `5`, `3`, `2` értékekre
állítja. Az alábbi regressziós számpélda a forrásbeli alapértékeket használja,
nem a távoli hangolás mérési eredményét mutatja.

A `path_distance` a végpont és a helyi A* vonallánc legkisebb távolsága
méterben. A `target_distance` a végpont és a helyi cél távolsága méterben.
A két új paraméter `path_distance_bias=6.0` és `goal_distance_bias=2.0`,
pontszám/méter értelmű súly. Először a három jutalmat összeadjuk, majd az
útvonaltól és a céltól mért súlyozott távolságokat levonjuk.

Konkrét példa: az útvonal az x tengelyen fut, a helyi cél `(1.0, 0.0) m`.
Egy párhuzamos jelölt végpontja `(0.8, 0.4) m`: az útvonalhibája `0.4 m`,
célhibája `sqrt(0.2² + 0.4²) = 0.4472 m`. Büntetése
`6 * 0.4 + 2 * 0.4472 = 3.2944` pont. Egy visszatérő jelölt vége
`(0.75, 0.1) m`: a két távolság `0.1 m` és `sqrt(0.25² + 0.1²) = 0.2693 m`,
ezért büntetése `6 * 0.1 + 2 * 0.2693 = 1.1385` pont.

Ha a párhuzamos jelölt három részpontja `(0.95, 0.8, 1.0)`, a visszatérőé
`(0.9, 0.6, 1.0)`, a régi jutalmuk `9.35`, illetve `8.70` pont. A régi
pontozás a párhuzamosat választaná. Az új értékek `6.0556` és `7.5615` pont:
ugyanilyen feltételek mellett a visszatérő jelölt nyer. Ezek tesztbemenetek,
nem Gazebo-ból mért trajektóriák.

### Biztonsági korlátok és megfigyelés

Az útvonalközelség puha büntetés, nem tiltott folyosó: az akadálykerüléshez
szükséges eltérés továbbra is lehetséges. Az új tag csak a meglévő biztonsági
vizsgálatokon átjutott jelöltek sorrendjét változtatja. Ez nem jelent új,
szigorú ütközésmentességi garanciát, hiszen a jelenlegi DWA a későbbi ütközést
a fékezhetőség alapján is elfogadhatja. Túl nagy útvonalsúly szűk helyen
ronthatja a kerülést, ezért a súlyokat csak méréssel érdemes tovább emelni.

A `Vezerles` napló új `utvonal_elteres` mezője az aktuális robotpozíció
távolsága a vizsgált útvonaldarabtól, méterben. Ez az érték a normál DWA-ágon
jelenik meg, nem a külön helyben forgató vagy megállító ágakon. Kerülés közben
nőhet, utána viszont az útvonalra visszatérő robotnál csökkennie kell.
Üres útvonalnál a `control()` megállítja a robotot, nem hívja a DWA-t.

### Kapcsolat és tesztelés

A hívási lánc: `control()` -> `dwa()` -> `path_tracking::tracking_cost()` ->
`path_tracking::distance_to_path()` -> legjobb jelölt -> `/cmd_vel`.
Az ábra ROS2-blokkja ugyanezt mutatja. A YAML tárolja az új súlyokat;
a node az indulásakor olvassa be őket, ezért módosítás után újra kell indítani.
Mindkét súly nullázásával az új büntetés kikapcsolható összehasonlító futáshoz.

ROS2-környezetben, a `ros2_astar_dwa_gazebo` könyvtárból:

```bash
colcon build --packages-select astar_dwa_controller --symlink-install --cmake-args -DBUILD_TESTING=ON
colcon test --packages-select astar_dwa_controller --event-handlers console_direct+
colcon test-result --verbose
```

A teljes node fordítása és a Gazebo/RViz célbaérési próba ebben a
Windows-munkamenetben nem igazolható: ROS2 és telepített WSL nem érhető el.
A regressziós teszt a geometriai függvényeket és a pontozási példákat méri,
nem a teljes robot zárt hurkú mozgását.

A helyi hordozható C++ fordítóval megkísérelt ellenőrzésből nem született
sikeres tesztfutási eredmény. A felhasználó kérésére további teszt nem fut;
a ROS2-fordítást, a regressziós tesztet és a Gazebo-próbát ő végzi el.

## 15. Útvonaltávolság számítása: path_tracking.hpp

### Cél, bemenet és kimenet

A `ros2_astar_dwa_gazebo/src/astar_dwa_controller/src/path_tracking.hpp`
ROS2-től független C++17 segédfájl. A `Path` a világkoordinátás `(x, y)`
pontpárok vektora. A `distance_to_path(path, first, last, x, y)` a megadott,
inkluzív indextartomány vonalláncától mért legkisebb távolságot adja méterben.
A `tracking_cost(path, first, last, x, y, target_x, target_y,
path_distance_bias, goal_distance_bias)` a két súlyozott távolság összegét adja,
amelyet a DWA levon a jutalompontszámból. A paraméterek a 14. fejezetben
bemutatott rollout-végpontot, helyi célt és súlyokat jelentik.

### Szakaszra vetítés hétköznapi példával

Nemcsak a waypointok távolságát mérjük: az összekötő vonalra ejtett
merőleges talppont is számít. Képzelj el egy kifeszített zsinórt két szög
között: a robot távolságát a zsinór legközelebbi pontjától kell mérni,
nem feltétlenül valamelyik szögtől.

Minden szakasz két végpontja `start` és `end`, méterben. A `dx` és `dy` a
két végpont koordinátakülönbsége, a `length_squared` ezek négyzetösszege,
négyzetméterben. A `fraction` a kezdőponttól a vizsgált pontig tartó vektornak
a szakaszirányra vett skalárszorzata, osztva a szakaszhossz négyzetével;
dimenzió nélküli arány. Ezt a kód 0 és 1 közé szorítja, hogy a véges
szakaszt, ne a végtelen egyenest mérje. A kapott aránnyal a kezdőponttól
a szakasz mentén haladunk, majd e talppont és a vizsgált `(x, y)` pont
euklideszi távolságát számítjuk.

Például `(0,0)` és `(1,0) m` között, `(0.5,0.4) m` végpontra `dx=1 m`,
`dy=0 m`, `length_squared=1 m²`, a skalárszorzat `0.5 m²`. Az arány `0.5`,
tehát a talppont `(0.5,0) m`, a távolság `0.4 m`. Csak a waypointokhoz mérve
hibásan `sqrt(0.5² + 0.4²) = 0.6403 m` adódna. A `(-0.3,0.4) m` pontnál
az arány negatív lenne, ezért 0-ra szorítjuk, és a szakasz kezdőpontjához
mérjük a `0.5 m` távolságot.

### Szélső esetek és tesztelés

Azonos szakaszvégpontoknál a vetítési arány 0, így nincs nullával osztás.
Egypontos útvonalnál ponttávolságot kapunk. A kód a túl nagy indexeket az
útvonal végéhez igazítja. Üres útvonalra a távolság pozitív végtelen; a
vezérlő ezt az esetet korábban kezeli, így nem pontoz ilyen pályát.

A `test/test_path_tracking.cpp` ellenőrzi az egyenes és kanyarodó szakaszt,
az ismételt és egyetlen pontot, az üres listát, a végpontra szorított vetítést,
a vizsgált tartományból kizárt későbbi visszatérő ágat, a visszatérés és a
párhuzamos haladás összehasonlítását, a cél megközelítését és a nullázott
súlyokkal kikapcsolt büntetést. Sikertelen állításnál kivétellel és nem nulla
kilépési kóddal áll le. A `CMakeLists.txt` `BUILD_TESTING` esetén önálló
`test_path_tracking` futtatható programként fordítja, és `path_tracking`
néven regisztrálja a CTest-ben; külön ROS2- vagy tesztkönyvtár nem kell a
teszt forrásának közvetlen C++17 fordításához.

### A távoli hangolás összevezetése

Az összevezetés megőrzi a távoli statikus akadálypontokat és a következő
YAML-értékeket: `robot_radius=0.24 m`, `safety_margin=0.10 m`,
`static_safety_margin=0.04 m`, `planning_margin=0.15 m`,
`lookahead_distance=0.40 m`, `max_linear_velocity=0.22 m/s`,
`acceleration_limit=1.8 m/s²`, `predict_time=2.0 s`, `min_ttc=0.8 s`,
valamint `alpha=5`, `beta=3`, `gamma=2`. Ezek mellé kerül a két új
útvonalkövetési súly: `path_distance_bias=6.0`, `goal_distance_bias=2.0`.
A `planning_margin` csak egyszer szerepel a konfigurációban.

Az útvonaltávolság-számítás, a DWA-ból történő hívása és az eltérés naplózása
megmarad. A hívási lánc nem változik. A távoli commitban lévő build-binárisokat
az összevezetés megőrzi, de azok nem az új közös forrásból készültek: indítás
előtt új `colcon build` szükséges. A felhasználó kérésére az összevezetés után
sem futott teszt; a diff ellenőrzése nem helyettesíti a fordítást vagy a
Gazebo-próbát.

## 16. Visszatérési elsőbbség az egyszerű súlyozás helyett

Aktuális kiegészítés: az `avoiding_obstacle_` állapot közeli mozgó vagy nem
ismert statikus pontnál felfüggeszti a visszatérést. A `control()` a kis
sebességű, ismert falhoz `wall.radius + 0.08 m`-nél közelebbi pontokat ebből
kizárja. A `collision_course(relative_x, relative_y, relative_vx, relative_vy,
clearance, horizon)` logikai eredménnyel jelzi a becsült ütközési pályát.
A relatív hely méterben, a relatív sebesség `m/s` egységben értendő; a kód
az akadály sebességéből a robot jelenlegi irányú maximális sebességét vonja
ki. A clearance a robot és akadály sugara plusz a biztonsági margó méterben,
a horizon az előrejelzési idő másodpercben. Biztonságos kezdeti távolságnál
nemnegatív hely-sebesség skalárszorzat távolodást jelent, tehát nincs veszély.
Egyébként a legközelebbi időpont a negatív skalárszorzat osztva a relatív
sebesség négyzetösszegével, `[0,horizon]` közé szorítva. Ekkorra előrevetíti
a relatív helyet, és a távolságát a clearance-hez hasonlítja. Például
`(0.8,0) m`, `(-0.42,0) m/s`, `2 s` horizont esetén az idő `1.905 s`, a
távolság nulla: veszély. A már elhaladt `(-0.5,0) m` pont ugyanilyen
sebességgel távolodik, ezért nem tiltja a visszatérést. Elhanyagolható
relatív sebességnél nincs osztás; clearance-en belül mindig veszélyt jelez.
Ez állandó sebességű becslés, nem zárt hurkú biztonsági bizonyítás. Az utolsó
fenyegetés után `0.6 s` késleltetés marad.
Kerüléskor nincs rögzített cél vagy oldaleltérés-büntetés, a teljes horizont
és a normál DWA választás működik. Utána `2*0.10=0.20 m` eltérés fölött
rögzülhet a cél; `0.10 m` útvonaltávolság vagy célponttávolság feloldja.

A `path_tracking.hpp` `rejoin_command(distance, heading_error, max_linear,
max_angular)` sebességpárt ad: szögsebessége a radiánban mért hiba kétszerese,
a határhoz szorítva; előremenete `min(max_linear, 1.5*distance)*cos(error)`,
nemnegatív koszinusszal, `1.2 rad` abszolút hiba fölött nulla. Az `1.5`
tényező `1/s` értelmű: `0.05 m` és nulla hiba esetén `0.075 m/s` adódik.
A `command_error(linear, angular, reference, max_linear, max_angular)` a két
sebesség referenciaeltérését saját maximummal osztja, majd négyzeteiket
összeadja: dimenzió nélküli, a kisebb jobb. Szabad rögzített célfolyosón ezt
minimalizálja a DWA az ütközésszűrésen átjutott jelöltek között; a referencia
és a fékezés pontos kerékmintái is szerepelnek. Blokkolt cél esetén a normál
pontozás marad. A hívások továbbra is `control()` -> `dwa()` -> rollout/szűrés
-> referenciahiba vagy normál pontozás -> `/cmd_vel`. A napló `kerules`
mezője jelzi az új fázist, az induló jelzés `cpa-rejoin`.
A tesztforrás módosult, futtatás nem történt a felhasználó kérésére;
diffellenőrzés és szerkesztődiagnosztika nem igazolja a Gazebo-célbaérést.

Az `astar_dwa_node.cpp` DWA-ja már nem csak a végpont távolságát bünteti.
A `returning_to_path_` mód a `path_return_tolerance=0.10 m` kétszerese fölött
bekapcsol, a tolerancián belül kikapcsol; közben megtartja az állapotát.
Új cél nullázza. Aktív módban a teljes `predict_time_` fut, és a célirány
a ciklus eleji robotpozícióból rögzített irány, nem a rollout végpontjából
visszafelé mutató irány. A normál mód adaptív időtávja megmarad.

A rollout az ismert statikus falakat és a LiDAR-akadályokat is ellenőrzi.
A kezdeti biztonsági margón belül a nem romló kimozdulás kivétele megmarad.
A fékezés/TTC után minden fennmaradó, ütközésnek jelzett jelölt is kiesik;
ilyen félbeszakadt pálya végpontja nem pontozható visszatérésként.

A `path_tracking.hpp` új `return_progress(initial_distance, final_distance,
max_travel)` függvénye dimenzió nélküli arányt ad: a kezdeti hibából kivonja
a végsőt, majd az adott idő alatt elérhető maximális úthosszal oszt, és
`[-1,1]` közé szorít. Minden bemenet méterben értendő, az osztó legalább
`0.001 m`. `0.22 m/s * 2 s = 0.44 m` elérhető út és `0.40 -> 0.35 m`
eltérés esetén az arány `(0.40-0.35)/0.44=0.1136`. Aktív módban ezt a
`path_return_bias=8` dimenzió nélküli súly szorozza: `0.9091` pont jutalom.

Az `is_returning(initial_distance, final_distance, tolerance, max_travel)`
logikai eredményt ad. A kezdő hiba a tolerancián túl legyen, és a végpont
vagy érje el a toleranciát, vagy az arány legalább `0.05` legyen. A példában
ez `0.05*0.44=0.022 m` javulás: `0.001 m` nem elég, `0.05 m` igen.
A `prefer_candidate(returning, score, best_returning, best_score)` eltérő
osztályoknál a visszatérőt, azonosaknál a nagyobb pontszámot választja.
Aktív módban egy szűrésen átjutott visszatérő `-10` ponttal is megelőzhet
egy párhuzamosat `100` ponttal. Visszatérő jelölt nélkül normál kerülés is
választható; elfogadott jelölt nélkül megmarad a forgó fallback.

Hívások: `control()` -> `dwa()` -> rollout/szűrés -> `tracking_cost()` +
`return_progress()` + `is_returning()` -> `prefer_candidate()` -> `/cmd_vel`.
A `DWA` napló `visszateres`, `visszatero_jelolt`, `valasztott_visszatero`
és `elteres=kezdeti->josolt m` mezői a módot, jelöltszámot és jósolt eredményt
mutatják; ez utóbbi nem két tényleges odometriamérés. A két távolságsúly
nullázása már nem kapcsolja ki a visszatérési elsőbbséget.

A `test_path_tracking.cpp` új esetei e három függvényt és a jelöltsorrendtől
független elsőbbséget rögzítik. A felhasználó kérésére teszt nem futott;
csak diffellenőrzés és szerkesztődiagnosztika történt. A kiválasztási
elsőbbség nem teljes zárt hurkú célbaérési vagy fizikai ütközésmentességi
bizonyítás. Újrafordítás és Gazebo-próba szükséges.

## 17. Aktív C++ ROS 2 / Gazebo megvalósítás

### Folyamat és csomópontok

A `cpp-rethink` ág alapértelmezett `simulation.launch.py` indítása az
`astar_dwa_controller` C++ `astar_dwa_node` vezérlőjét, a `ros_gz_bridge`
hidat és a már meglévő `moving_obstacle_node` szimulációs csomópontot indítja.
Az RViz külön megjelenítő. A launch nem indítja a korábbi Python ROS-plannert.
A párhuzamos ROS-Python prototípus törölve lett; a működő Matplotlibes
`simulation.py`, `DWA+A.py`, `DWA.py`, `robot.py` és az `astar_project`
forrásaihoz nem nyúltunk.

A vezérlő fő adatútja:

```text
Gazebo world-pose /odom + TurtleBot /scan + RViz /goal_pose
    -> statikus rács/A* -> látható waypoint és előretekintési cél
    -> C++ DWA-jelöltek, statikus/LiDAR ütközés- és fékezésvizsgálat
    -> /cmd_vel -> TurtleBot fizikai DiffDrive
```

Az `astar_dwa_node.cpp` egy ROS node-ban egyesíti az A*, a waypointkövetés,
a LiDAR feldolgozás és mozgásbecslés, a DWA, a `/cmd_vel`, az RViz-markerek
és a Gazebo-padlóra rajzolt A* útvonal funkcióját. Nem általános célú
navigációs keretrendszer: az aktuális statikus térképet a `rosbot.yaml`
ismert akadálypontjai adják.

### A hiba feltételezett oka és a napló jelentése

A megosztott futási napló a régi Python ROS-adapterből származott, nem a
`cpp-world-pose` C++ buildből. A végén a vezérlő `target=(6.8,3.8) m` és
`pose=(6.735,3.723) m` értéket írt. A két koordinátakülönbség `0.065 m`
és `0.077 m`; távolságuk `sqrt(0.065^2 + 0.077^2) ~= 0.101 m`. Ez a
naplóban használt helyzet szerint közeli célpontot mutat, miközben a
felhasználó a Gazebo-ban távolinak látta a robotot. A `target` lokális
waypoint, nem feltétlenül a megadott globális cél. A sor nem bizonyította
sem a tényleges célbaérést, sem a hiba egyetlen okát.

A korábbi indításban a DiffDrive kerékelfordulásból integrált lokális
odometriájához a vezérlő még a `(0.8,0.8) m` spawnhelyet is hozzáadta.
Falérintés és kerékcsúszás mellett a kerékből becsült helyzet eltérhet a
Gazebo világpozíciójától; a spawn-offset ismételt hozzáadása pedig kettős
eltolást okozhat. Ez magyarázhatja, hogy a log szerinti pozíció és a látható
robot nem egyezett. A régi Python-naplóból az egyes okok nem választhatók
szét biztosan.

A `gazebo_odometry_world.py` a TurtleBot modell runtime SDF-másolatához
Gazebo `OdometryPublisher` plugint ad. Ez a modell világpozícióját
`/world_pose_odom` üzenetként publikálja; a bridge ezt `/odom`-ra köti.
A DiffDrive kerékodometriája külön `/gazebo/wheel_odom` diagnosztikai
topicon marad. A C++ vezérlő `initial_pose_x/y=0` értékkel fogadja a
világpozíciót, tehát nem ad hozzá spawn-offsetet. A fizikai robot továbbra
is `/cmd_vel` parancsokkal mozog, nincs teleportálás. A `cpp-world-pose`
induló sor jelzi, hogy ezt a buildet indították el.

Ez a világpozíció csak szimulációban áll rendelkezésre. Valódi roboton nem
használható Gazebo ground truthként; ott az encoder-, IMU- és esetleg LiDAR-
adatokból lokalizációs becslés kell. A módosítás szimulációs hibakeresés,
nem kész hardveres lokalizációs rendszer.

### Térkép felépítése

A `dwa_world.sdf` pályája `8.2 x 5.2 m`. A C++ rácsorigója `(-0.1,-0.1) m`,
felbontása `0.20 m`, így a rács `ceil(8.2/0.2)=41` oszlopból és
`ceil(5.2/0.2)=26` sorból áll. A `ceil` felfelé kerekít, hogy a teljes
világot lefedje. A leképezés:

```text
column = floor((x - origin_x) / resolution)
row    = floor((y - origin_y) / resolution)
```

Például `(x,y)=(0.8,0.8) m`, origó `(-0.1,-0.1) m` és `0.20 m`
felbontás esetén mindkét index `floor(0.9/0.2)=4`. A cella középpontja
`origin+(index+0.5)*resolution`, ennél a példánál mindkét tengelyen
`-0.1+4.5*0.2=0.8 m`. A `column` az x, a `row` az y tengelyhez tartozik.

A `rosbot.yaml` `known_obstacle_x/y/radius` listái a statikus SDF dobozfalait
körakadály-mintákkal közelítik. Az A* tiltott celláinak sugara az
akadálysugár, a robot sugara és a `planning_margin` összege; például
`0.10+0.24+0.15=0.49 m`. Minden tag méterben értendő. Ez körös közelítés,
nem a doboz egzakt geometriája, ezért a falpontokat a Gazebo-világgal együtt
kell karbantartani. Az A* a statikus térképet használja; a DWA ezen felül
a LiDAR-pillanatfelvételeket ellenőrzi.

A Waffle SDF-ből a launch olvassa ki a keréksugarat, a keréktávolságot,
a testméretet, a gyorsuláskorlátot és a LiDAR `base_scan` eltolását. A
`scan_offset_x/y/z` ugyanazt a szenzorhelyzetet adja a pontvilág-koordinátás
számításának és a TF-nek. Az A* út utolsó pontját a C++ kód a tényleges
RViz-célra állítja, hogy ne csak a célcella közepét közelítse.

### Cél és fizikai vezérlés

Az RViz `2D Goal Pose` a `/goal_pose` topicon küldi a célkoordinátát. A
`control()` A*-útvonalat készít, `/astar_path` üzenetben publikálja, majd
látható waypointot és előretekintési célt választ. A DWA a kinematikailag
elérhető keréksebesség-párokat szimulálja és akadály-/fékezésvizsgálat után
publikál `/cmd_vel` parancsot. A fizikai Waffle DiffDrive hajtja a robotot.
Az RViz útvonal és a Gazebo talajára rajzolt vizuális A* út ugyanannak a
tervezett pathnak két megjelenítése.

A DWA waypoint-indexe nem a robot által bizonyítottan elért pontok száma.
Az indexet a vezérlő a path menti aktuális helyzet és a kiválasztási logika
alapján lépteti. A tényleges célbaérést a végponttól mért pozíció, a robot
Gazebo-pozíciója és a `Goal reached`/megállási feltétel együtt igazolja; a
waypointszám önmagában nem.

### Valós robot és mentett térkép

A C++ node topicnevei paraméterezhetők, és `/odom`, `/scan`, `/goal_pose`,
`/cmd_vel` szabványos interfészt használ, de a jelenlegi A* még a YAML
`known_obstacle_*` statikus pontlistáiból épít rácsot. Mentett SLAM-térképhez
ezt `nav_msgs/OccupancyGrid /map` bemenetre kell cserélni; a térkép YAML
metaadatot és képállományt tartalmaz. Mentés például:

```bash
ros2 run nav2_map_server map_saver_cli -f ~/maps/palya
```

Valódi roboton a map_server publikálhatja a mentett `/map`-et, AMCL vagy más
lokalizáció pedig becsülheti a `map -> odom` transzformációt. Szükséges a
`map -> odom -> base_link -> base_scan` TF-fa, a cél frame-transzformációja,
a tényleges footprint, kerékgeometria, gyorsulás/sebességhatár, watchdog és
hardveres vészleállítás. A mostani Gazebo world-pose plugin nem kerülhető
át hardverre: a roboton lokalizációs becslés kell. A vezérlő jelenleg nem
minősített biztonsági rendszer.

### Diplomamunkába illeszthető összefoglaló

> A rendszer globális útvonalát rácsalapú A* algoritmus tervezi meg a
> statikus, ismert akadályok figyelembevételével. A lokális mozgást Dynamic
> Window Approach (DWA) vezérli: a differenciális meghajtás korlátai között
> keréksebesség-jelölteket vizsgál, majd azok előrejelzett trajektóriáit az
> akadálytávolság, fékezhetőség, ütközési idő és célirány szerint értékeli.
> A kiválasztott parancs ROS 2 `/cmd_vel` üzenetként jut a TurtleBot
> Gazebo-meghajtásához; a tervezett útvonal RViz-ben és vizuális Gazebo-
> modellként is megjelenik. A hibakeresés során felmerült, hogy a
> kerékelfordulásból integrált odometria fizikai csúszás vagy falérintés
> után eltérhet a Gazebo modell tényleges világpozíciójától. Emiatt a
> szimulációs vezérlő a Gazebo világpozícióját használja `/odom` bemenetként,
> a kerékodometriát pedig külön diagnosztikai topicon tartja meg. A korábbi
> napló célközeli becsült helyzetet, de vizuálisan eltérő robotpozíciót
> mutatott; ez az odometria-eltérés hipotézisét indokolta, de önmagában nem
> bizonyította annak okát. Valódi roboton a Gazebo ground truth helyett
> mentett SLAM-térkép, lokalizáció, megfelelő TF-keretek és a konkrét
> robothoz mért dinamikai paraméterek szükségesek. A célbaérés és a
> biztonság csak lefuttatott szimulációs, majd hardveres próbával igazolható.

### Újrafelhasználható megírási prompt

```text
Írj magyar, diplomamunkába illeszthető műszaki alfejezetet az aktuális
cpp-rethink ROS 2 / Gazebo C++ A* + DWA rendszerről. Ellenőrizd a tényleges
astar_dwa_node.cpp, rosbot.yaml, dwa_world.sdf és simulation.launch.py
forrásokat. Ismertesd a node-adatfolyamot, a rács méretét/felbontását/
origóját, az akadályok reprezentációját, az A* és DWA döntéseit, valamint
a /goal_pose, /astar_path, /scan, /odom és /cmd_vel interfészeket. Magyarázd
el a kerékodometria és Gazebo world-pose különbségét, de a korábbi naplót
csak hipotézis alátámasztására használd, ne bizonyított okként. Térj ki a
mentett SLAM-térkép, map_server/AMCL, TF, footprint, watchdog és hardveres
vészleállítás szükségességére. Ne állíts futtatást, célbaérést vagy
biztonságot bizonyíték nélkül; az eredeti Matplotlib Python-szimulátort
változatlan referenciaként kezeld. Minden számot és állítást a jelenlegi
forráshoz vagy tényleges méréshez köss.
```

## 18. C++ DWA kerékállapot és blokkolt pályák

Az `astar_dwa_node.cpp` `dwa()` függvénye a `wheel_left_` és `wheel_right_`
parancsállapotból képez gyorsuláskorlátozott dinamikus ablakot. Ezek nem mért
keréksebességek. A jelöltek bemenete a lokális cél és a LiDAR-ból becsült
akadálylista; a kimenet a lineáris és szögsebesség parancspárja.

A korábbi recovery-ág nullázta mindkét belső keréksebességet, majd mégis
nem nulla szögsebességű forgást küldött. Emiatt a következő ciklus dinamikus
ablaka nem a kiadott parancsból indult. A köztes javítás a tartalék forgásból
számította vissza a kerékállapotot; az aktuális változat viszont megszünteti
ezt az ellenőrizetlen forgást, és üres jelöltlistánál nullaparancsot ad ki.
A mintavétel minden ciklusban tartalmazza az aktuális
keréksebességet és a nullához legközelebbi, gyorsuláskorláton belül elérhető
fékező értéket is, nem csak az egyenletes mintarácsot.

A differenciális hajtásnál nulla előremenethez és `omega` forgáshoz a bal
keréksebesség `-omega * wheel_base / wheel_radius`, a jobb ennek ellentettje.
Az `omega` rad/s, a `wheel_base` a keréktávolság fele méterben, a
`wheel_radius` méterben értendő; az eredmény kerék-szögsebesség rad/s-ban.
Például `omega=0.6 rad/s`, `wheel_base=0.08 m`, `wheel_radius=0.033 m`
esetén a két parancs `-1.455` és `1.455 rad/s`. Átlaguk nulla, így az
előremenet nulla; különbségükből a `wheel_kinematics()` visszaadja a
`0.6 rad/s` forgást. A launch által kiolvasott geometria ettől eltérhet.

Ez nem igazolja a szembejövő akadály kikerülését. A C++ továbbra is elutasítja
a teljes predikciós idő alatt ütköző jelölteket; a régi tartalék forgás nem
esik át ezen a pályavizsgálaton, és önmagában nem véd egy közeledő akadálytól.
A Python `simulation.py` üres `best_pair` esetén megállítja a robotot, tehát
ott sem valósul meg feltétlenül sikeres menekülés. A Python akadályai ismert
középpontot, sugarat és sebességet adnak, a C++ LiDAR-pontokat és becsült
sebességet használ; a két bemenet nem azonos.

Ellenőrzés: a módosított C++ fájl editor-diagnosztikája hibamentes.
Teszt, ROS-build és Gazebo-futás nem történt. A további hibakereséshez a
`DWA: ...`, `DWA: nincs elfogadhato jelolt` és `Vezerles: ...` futási sorok
szükségesek az ütközést megelőző időszakból. A folyamatábrát a felhasználó
korábbi megkötése miatt nem módosítottuk.

A beküldött futási naplóban 23 blokkolt ciklus után újra megjelenik haladó
parancs, ezért nem bizonyított a program végleges lefagyása. A
`cmd=(0.00,-0.60)` a tartalék forgással egyezik, de az egymástól függetlenül
ritkított DWA- és vezérlési sorok nem mindig ugyanazt a ciklust írják le.
Az akadálysebesség becslése és a scan frissessége ebből a régi naplóból
nem állapítható meg.

A `Vezerles` napló ezért további diagnosztikai mezőket kapott:
`sim_t` a ROS szimulációs idő másodpercben; `scan_kor` az aktuális ROS idő
és a LaserScan időbélyegének különbsége másodpercben; `lidar_pont` a
feldolgozott pontok száma; `mozgo_pont` a nem nulla becsült sebességű
pontok száma; `kozeli_v` a legközelebbi LiDAR-pont becsült világkoordinátás
sebessége m/s-ban. Ez nem az akadály ismert valódi sebessége. Például
`sim_t=12.4` és `scan_kor=0.1` esetén a scan időbélyege `12.3 s`;
`kozeli_v=(-0.2,0.0)` az x tengely negatív irányú becsült mozgását jelzi,
nem feltétlenül a robothoz viszonyított közeledést. E mezők naplózása nem
módosítja a vezérlési döntést; az új futási adatok még hiányoznak.

## 19. A final_v1 alapján javított LiDAR-követés

A `final_v1` tag a `8db40ea` commitra mutat. Annak `simulation.launch.py`
fájlja a Python `python_planner_node` vezérlőt indította, nem a C++ DWA-t.
A felhasználó ezt sikeres futásként jelölte meg; a Gitben tárolt ellenőrzési
leírás azonban csak statikus ellenőrzést rögzít, ezért a futási eredményt
nem állítjuk saját mérésként. Az aktuális C++ architektúrát megtartjuk.

Az `astar_dwa_node.cpp` `obstacles()` függvénye a LaserScan érvényes,
három méteren belüli elülső pontjait klaszterezi, majd az előző pontcsoportok
alapján becsült világkoordinátás sebességet rendel hozzájuk. A visszatérés
`std::vector<Obstacle>`: felületi pontok nulla akadálysugárral és becsült
`vx`, `vy` sebességekkel, nem ismert testközéppontokkal.

A régi C++ feldolgozás a vezérlő aktuális idejéből számította a követési
időkülönbséget. Így ugyanaz a scan újra feldolgozható volt, és az azonos
klaszterközéppont nulla elmozdulása a sebességbecslést csökkentette. A javítás
a scan időbélyegét használja: egy már feldolgozott időbélyegnél a
`sensed_cache_` kerül visszaadásra, a követési állapot nem változik.
Új időbélyegnél az `obstacles()` frissít, a `control()` eltárolja az eredményt.

A referencia `lidar_obstacle_node.py` mintájára a klaszterpárosítás az előző
klaszter becsült jövőbeli helyéhez keres közeli csoportot, és a `used` lista
egy korábbi csoportot legfeljebb egyszer enged felhasználni. A párosítás
küszöbe `0.35 m`; becslés csak legalább kétpontos klaszternél és
`0.02 < dt < 0.5 s` időközzel történik. A fal közelsége önmagában már nem
nullázza a sebességet, mert az ott haladó dinamikus akadályt is elrejthette.

A sebességbecslés tengelyenként `0.6 * előző_sebesség + 0.4 * elmozdulás / dt`.
A sebességek m/s-ban, az elmozdulás méterben, a `dt` másodpercben értendő.
Először két scan klaszterközéppontjának különbségét osztjuk a scan-időközzel,
majd ezt simítjuk az előző becsléssel. Például `dt=0.1 s`,
`elmozdulás=-0.025 m`, `előző_sebesség=-0.20 m/s` esetén
`0.6*(-0.20)+0.4*(-0.025/0.1)=-0.22 m/s` az új x sebesség.
Ugyanannak a scan-nek az újraolvasása ezt nem változtatja `-0.132 m/s`-ra.
A `0.06 m/s` alatti becsült mozgás nullázódik, a C++ meglévő `0.6 m/s`
felső sebességkorlátja megmarad. Ez heurisztikus követés, nem garantált
objektumazonosítás; a falak felületi pontjai is adhatnak zajos becslést.

A `control()` a referenciához hasonlóan megállítja a robotot, ha az odometria
vagy a scan kora meghaladja `max(0.5, 3*dt_) s` értéket. Például
`dt_=0.1 s` vezérlési periódusnál a határ `0.5 s`. A `dwa()` üres
jelöltlistánál nullázza a kerékparancs-állapotot és `(0,0)` parancsot ad;
nem hajt végre pályavizsgálat nélküli tartalék forgást. A nulla parancs nem
véd meg attól, ha egy másik akadály a robotnak megy, ezért az időben történő
felismerést és kikerülést külön kell mérni.

Korlátok: a C++ továbbra is teljes horizontú ütközéselutasítást használ,
míg a Python admisszibilitása nem azonos szabályú; a C++ pontátalakítása
a feldolgozáskori robotpózt használja, nem a referencia TF-időbélyeges
lekérdezését. A két megvalósítás nem lett azonossá téve. A scan frissességét,
becsült akadálysebességet és blokkolt ciklusokat az új naplóval kell vizsgálni.

Ellenőrzés: a C++ editor-diagnosztikája hibamentes. ROS-build, teszt és
Gazebo-futás nem történt; a sikeres kikerülés nincs igazolva. Az új induló
marker `cpp-world-pose-scan-tracking-v2`; ennek hiánya régi buildre utal.
A Python-szimulátor és a felhasználó által védett folyamatábra változatlan.


## 20. Kétakadályos Gazebo-teszt és az elakadás javítása

### Mi volt a hiba?
A robot a `(2.0–2.3, 1.75–1.85)` környékén megállt: a napló `lookahead=0.000`, `forward_pairs=0` értéket és helyben forgást mutatott. A `path_tracking.hpp` `prune_lookahead()` függvénye akkor is a pálya vetületére állította a célpontot, ha nem volt elérhető előretekintési pont, vagy nem volt elérhető vetület. Így a célpont a robot alatt volt, nem adódott előremutató parancs.

### Javítás
- `path_tracking.hpp`: mindkét esetben `along_path(lookahead)` adja a célt, vagyis az úton előre lévő pontot. A blokkolt esetben nincs metszés (`waypoint == 1` marad). A teszt: `test_path_tracking.cpp`.
- `reference_planner.hpp`: ha a DWA-nak nincs megengedett parancsa, biztonságos, helyben forgó tartalék parancs.
- `reference_controller.cpp`: a statikus térképhez tartozó LiDAR-pontok cellánként statikus akadályként egyesülnek, így a fal nem jelenik meg zajos mozgó akadályként.
- `lidar_obstacle_node.py`: a 0.35 m/s feletti becsült sebességet statikusnak tekinti (zaj).

### Forgatókönyv (szimuláció)
Szembejövő akadály: `(6.8, 2.0)`-ról, `(-0.26, 0)` m/s sebességgel, amint az odom `x >= oncoming_start_x` (0). Oldalról érkező: `(2.4, 0.4)`-ről, `(0, +0.20)` m/s sebességgel, amint `x >= crossing_start_x` (0.8). Példa: ha a robot x=0.8-nál jár, a másodperc törtrésze alatt mindkét akadály mozgásban van; 0.26 m/s mellett a szembejövő kb. 5 m-t kb. 19 s alatt tesz meg szimulációs időben.

### Eredmény
Cél `(6.5, 4.2)`: mindkét akadály elindult, `avoidance_priority=1`, a kikerülés látható, a futás `reason=finished` állapottal ért véget. Valós idő: a szimuláció ~0.1–0.2-es valós idejű tényezővel 2–4 percig tart.

### Korlát
Csak szimuláció; hardveren nem tesztelt. Valós robotnál a paramétereket újra kell hangolni, és kell hardveres vészleállító.
````````

### `Projekt/dokumentacio/KODOSSZEFOGLALO_VedeshezMagyarazat.md`

````````markdown
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
````````

### `Projekt/dokumentacio/TAPASZTALATOK.md`

````````markdown
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
````````

### `Projekt/Gazebo_ROS2/env.sh`

````````bash
#!/usr/bin/env bash
# Használat minden új terminálban:  source env.sh   (ebből a mappából, vagy teljes útvonallal)
source /opt/ros/jazzy/setup.bash
source "$(dirname "${BASH_SOURCE[0]}")/install/setup.bash"
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
export DISPLAY=:0 QT_QPA_PLATFORM=xcb QT_X11_NO_MITSHM=1
export XDG_RUNTIME_DIR=/tmp/gazebo-runtime
mkdir -p "$XDG_RUNTIME_DIR" && chmod 700 "$XDG_RUNTIME_DIR"
export MAP="$HOME/maps/palya"
````````

### `Projekt/Gazebo_ROS2/python_deps/astar_project/__init__.py`

````````python

````````

### `Projekt/Gazebo_ROS2/python_deps/astar_project/grid_map.py`

````````python
"""Egyszeru racsterkep az A* algoritmushoz."""

import math


class GridMap:
    """Negyzetes cellakbol allo, ketdimenzios terkep."""

    def __init__(
        self,
        width,
        height,
        resolution=0.1,
        origin_x=0.0,
        origin_y=0.0,
        unknown=False,
    ):
        if width <= 0 or height <= 0:
            raise ValueError("A terkep merete legyen pozitiv.")
        if resolution <= 0:
            raise ValueError("A felbontas legyen pozitiv.")

        self.width = width
        self.height = height
        self.resolution = resolution
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.grid = []

        initial_value = 2 if unknown else 0
        for _ in range(height):
            self.grid.append([initial_value] * width)

    def is_inside(self, row, column):
        """Megadja, hogy a cella a terkepen belul van-e."""
        return 0 <= row < self.height and 0 <= column < self.width

    def is_free(self, row, column):
        """Megadja, hogy a cella szabad-e."""
        return self.is_inside(row, column) and self.grid[row][column] == 0

    def world_to_grid(self, x, y):
        """Vilagkoordinatat (meterben) racskoordinatava alakit."""
        column = math.floor((x - self.origin_x) / self.resolution)
        row = math.floor((y - self.origin_y) / self.resolution)
        return row, column

    def grid_to_world(self, row, column):
        """A cella kozepontjat visszaadja vilagkoordinataban."""
        x = self.origin_x + (column + 0.5) * self.resolution
        y = self.origin_y + (row + 0.5) * self.resolution
        return x, y

    def add_obstacle(self, row, column):
        """Akadalykent megjelol egy cellat."""
        if not self.is_inside(row, column):
            raise ValueError("Az akadaly a terkepen kivul van.")
        self.grid[row][column] = 1

    def remove_obstacle(self, row, column):
        """Szabad cellava tesz egy cellat."""
        if not self.is_inside(row, column):
            raise ValueError("A cella a terkepen kivul van.")
        self.grid[row][column] = 0

    def mark_free(self, row, column):
        """A robot altal megvizsgalt cellat szabadnak jelol."""
        if not self.is_inside(row, column):
            raise ValueError("A cella a terkepen kivul van.")
        self.grid[row][column] = 0

    def add_obstacle_world(self, x, y, radius=0.0):
        """Vilagkoordinatas akadalyat egy vagy tobb cellaba ir."""
        center_row, center_column = self.world_to_grid(x, y)
        cell_radius = int(radius / self.resolution) + 1

        for row in range(center_row - cell_radius, center_row + cell_radius + 1):
            for column in range(
                center_column - cell_radius,
                center_column + cell_radius + 1,
            ):
                if not self.is_inside(row, column):
                    continue
                cell_x, cell_y = self.grid_to_world(row, column)
                distance = ((cell_x - x) ** 2 + (cell_y - y) ** 2) ** 0.5
                if distance <= radius + self.resolution:
                    self.add_obstacle(row, column)

    def update_from_obstacles(self, obstacles):
        """Szimulacios akadalyobjektumokbol frissiti a terkepet.

        Az objektumoknak ``x``, ``y`` es opcionisan ``radius`` attributummal
        kell rendelkezniuk, ahogy a DWA Obstacle osztályának.
        """
        for obstacle in obstacles:
            radius = getattr(obstacle, "radius", 0.0)
            self.add_obstacle_world(obstacle.x, obstacle.y, radius)

    def inflate_obstacles(self, radius):
        """Biztonsagi tavolsaggal kitagitja az akadalycellakat."""
        if radius < 0:
            raise ValueError("A biztonsagi sugar nem lehet negativ.")
        if radius == 0:
            return

        obstacle_cells = [
            (row, column)
            for row in range(self.height)
            for column in range(self.width)
            if self.grid[row][column] == 1
        ]
        cell_radius = math.ceil(radius / self.resolution)

        for obstacle_row, obstacle_column in obstacle_cells:
            for row in range(
                obstacle_row - cell_radius,
                obstacle_row + cell_radius + 1,
            ):
                for column in range(
                    obstacle_column - cell_radius,
                    obstacle_column + cell_radius + 1,
                ):
                    if self.is_inside(row, column):
                        self.grid[row][column] = 1

    def get_neighbors(self, row, column, diagonal=False):
        """Visszaadja a szabad szomszedos cellakat."""
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        if diagonal:
            directions += [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        neighbors = []
        for row_change, column_change in directions:
            new_row = row + row_change
            new_column = column + column_change
            if self.is_free(new_row, new_column):
                is_diagonal = row_change != 0 and column_change != 0
                if is_diagonal:
                    if not self.is_free(row, new_column):
                        continue
                    if not self.is_free(new_row, column):
                        continue
                neighbors.append((new_row, new_column))

        return neighbors
````````

### `Projekt/Gazebo_ROS2/python_deps/robot.py`

````````python
"""Differenciális meghajtású robotmodell."""

import math

import numpy as np


def get_robot_kinematics(w_L, w_R, config):
	"""Keréksebességből lineáris és szögsebességet számol."""
	v = ((w_L + w_R) / 2) * config.r_kerek
	w = ((w_R - w_L) / (2 * config.b)) * config.r_kerek
	return v, w


class Obstacle:
	def __init__(self, x, y, radius=0.1, vx=0.0, vy=0.0):
		self.x = x
		self.y = y
		self.radius = radius
		self.vx = vx
		self.vy = vy

	def move(self, dt):
		self.x += self.vx * dt
		self.y += self.vy * dt


class Goal:
	def __init__(self, x, y, tolerance=0.15, slow_down=True, slow_down_distance=0.8, heading=None):
		self.x = x
		self.y = y
		self.tolerance = tolerance
		self.slow_down = slow_down
		self.slow_down_distance = slow_down_distance
		self.heading = heading


class robotconfig:
	def __init__(robot):
		robot.r_kerek = 0.033
		robot.b = 0.08
		robot.w_kerek_max = 15
		robot.a_max = 2
		robot.w_kerek_min = -robot.w_kerek_max
		robot.w_kerek_resolution = 1
		robot.allow_reverse = False
		robot.dt = 0.1
		robot.predict_time = 3
		robot.rob_radius = robot.b + 0.02
		robot.safety_margin = 0.15
		robot.static_safety_margin = 0.01  # Új paraméter a statikus falak melletti tűréshez
		robot.Alfa = 5
		robot.Beta = 2
		robot.Gamma = 3
		robot.enable_waypoint_slowdown = False


class robotstate:
	def __init__(robot, x=0, y=0, v=0, w=0, irany=0, w_L=0, w_R=0):
		robot.x = x
		robot.y = y
		robot.v = v
		robot.w = w
		robot.irany = irany
		robot.w_L = w_L
		robot.w_R = w_R


def update(robot, config, w_L_target, w_R_target, dt):
	"""Frissíti a robotot a gyorsuláskorlátozás és a kinematika alapján."""
	max_w_dot = config.a_max / config.r_kerek
	w_L_new = robot.w_L + np.clip(
		w_L_target - robot.w_L,
		-max_w_dot * dt,
		max_w_dot * dt,
	)
	w_R_new = robot.w_R + np.clip(
		w_R_target - robot.w_R,
		-max_w_dot * dt,
		max_w_dot * dt,
	)
	v, w = get_robot_kinematics(w_L_new, w_R_new, config)
	theta_0 = robot.irany

	if abs(w) > 1e-6:
		robot.x += (v / w) * (math.sin(theta_0 + w * dt) - math.sin(theta_0))
		robot.y += -(v / w) * (math.cos(theta_0 + w * dt) - math.cos(theta_0))
	else:
		robot.x += v * math.cos(theta_0) * dt
		robot.y += v * math.sin(theta_0) * dt

	robot.irany += w * dt
	robot.v = v
	robot.w = w
	robot.w_L = w_L_new
	robot.w_R = w_R_new

	return np.array([robot.x, robot.y, robot.irany, robot.v, robot.w, robot.w_L, robot.w_R])
````````

### `Projekt/Gazebo_ROS2/README.md`

````````markdown
# Gazebo + ROS 2 szimuláció (A* + DWA)

ROS 2 Jazzy, Gazebo (gz sim), TurtleBot3 Waffle, slam_toolbox. Linuxon vagy Windows alatt WSL2 Ubuntu-ban futtatható.

## Mappák
```
Gazebo_ROS2/
├── src/
│   ├── astar_dwa_controller/   C++ vezérlő (A* + DWA), RViz beállítás
│   └── dwa_gazebo_sim/         Gazebo világ, SLAM, akadálykövetés, launch fájlok
└── python_deps/                robot.py és astar_project/grid_map.py (a Python node-ok használják, a build telepíti)
```

## Build (egyszer, kódváltozás után újra)
```bash
cd <ez a mappa>          # pl. "<WORKSPACE>/Projekt/Gazebo_ROS2"
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src --rosdistro jazzy -r -y
colcon build --symlink-install
source install/setup.bash
```

## Környezet (minden új terminálban, A/B/C mindegyikben)
```bash
source "<WORKSPACE>/Projekt/Gazebo_ROS2/env.sh"
```
[env.sh](env.sh) betölti a ROS-t, a build eredményét, a Gazebo/RViz változókat és a `MAP=$HOME/maps/palya` útvonalat. Nélküle `Package 'dwa_gazebo_sim' not found` hiba jön.

## 1. Feltérképezés (egyszer)
A terminál:
```bash
ros2 launch dwa_gazebo_sim simulation.launch.py slam_mode:=mapping start_planner:=false map_resolution:=0.10
```
B terminál (RViz, Fixed Frame: `map`):
```bash
ros2 launch dwa_gazebo_sim visualization.launch.py
```
C terminál (kézi vezetés lassan, amíg a térkép teljes nem lesz):
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p speed:=0.15 -p turn:=0.5
```

## 2. Térkép mentése
```bash
mkdir -p "$HOME/maps"; MAP="$HOME/maps/palya"
ros2 run nav2_map_server map_saver_cli -f "$MAP" --ros-args -p save_map_timeout:=10.0
ros2 service call /slam_toolbox/serialize_map slam_toolbox/srv/SerializePoseGraph "{filename: '$MAP'}"
```
A mentést a még futó feltérképezés mellett, egy új (környezettel beállított) terminálban kell kiadni. Ellenőrzés – mind a 4 fájlnak léteznie kell, különben a lokalizáció nem indul (`Missing saved SLAM file`):
```bash
ls -l "$HOME/maps/palya".{yaml,pgm,posegraph,data}
```
Ha a `.posegraph`/`.data` hiányzik, a `serialize_map` hívás hibázott: ismételd meg (a `result: 0` jelzi a sikert). Ezután állíts le mindent (Ctrl+C).

## 3. Futtatás a mentett térképpel
Előtte tiszta állapot kell (lásd Hibakeresés). A `.posegraph` és `.data` fájloknak léteznie kell.
A terminál:
```bash
source "<WORKSPACE>/Projekt/Gazebo_ROS2/env.sh"
ls "$MAP".posegraph "$MAP".data || echo "HIÁNYZIK a mentett térkép – ismételd meg a 2. lépést"
ros2 launch dwa_gazebo_sim simulation.launch.py slam_mode:=localization map_file:="$MAP" initial_x:=0.8 initial_y:=0.8 initial_yaw:=0.0
```
(`map_file`: abszolút útvonal, kiterjesztés nélkül, `~` nélkül; az `initial_*` egyezzen a feltérképezés kezdőpozíciójával.)
B terminál:
```bash
ros2 launch dwa_gazebo_sim visualization.launch.py
```
RViz-ben **2D Goal Pose**-szal adj célt (ha kell, előbb **2D Pose Estimate**). A robot az A* útját követi DWA-val, és kikerüli a két mozgó akadályt (a szembejövő a robot `odom x ≥ 0`, az oldalról érkező `x ≥ 0,8` esetén indul; kikapcsolás: `enable_crossing_obstacle:=false`).

Cél parancssorból (a feliratkozó ~40 s után érhető el, ismételd, amíg a naplóban `DIAG_GOAL` megjelenik):
```bash
ros2 topic pub --once /goal_pose geometry_msgs/msg/PoseStamped "{header: {frame_id: map}, pose: {position: {x: 6.5, y: 4.2}, orientation: {w: 1.0}}}"
```
Siker: a naplóban `DIAG_CONTROL cpp reason=finished`. A futás ~2–4 perc (a Gazebo lassú, RTF ≈ 0,1–0,2).

## Hibakeresés
- Ha a robot akadálykerülés után elakad vagy eltolódik, ne tekintsd sikeresnek a futást. A `DIAG_CONTROL` és `DIAG_ODOM` sorok alapján ellenőrizhető az útpontkövetés és a kerék-odometria eltérése a Gazebo pozíciójától. Az elakadás jelenleg nem minden esetben megoldott.
- **Új indítás előtt mindig tiszta állapot kell.** A régi folyamatok (gz sim, parameter_bridge, régi node-ok) két szimulációt eredményeznek: a robot nem indul (`DIAG_CONTROL cpp reason=stale_input`), a cél nem érkezik meg. Megoldás: Windows PowerShellben `wsl --shutdown`, majd nyiss új WSL terminált.
- Ctrl+C után megmaradt `gz sim`: `pgrep -a gz`, majd `kill <PID>`.
- Villogó/eltűnő zöld útvonal RViz-ben: javítva (nulla időbélyeg + Transient Local); kódváltozás után `colcon build --symlink-install` kell.
- Üres térkép / `tf_missing`: ne ments; indítsd újra a feltérképezést.
- TF-fa: `ros2 run tf2_tools view_frames`; gráf: `rqt_graph`.
````````

### `Projekt/Gazebo_ROS2/src/astar_dwa_controller/CMakeLists.txt`

````````text
cmake_minimum_required(VERSION 3.8)
project(astar_dwa_controller)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(Python3 REQUIRED COMPONENTS Interpreter)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(visualization_msgs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)

add_executable(astar_dwa_node src/reference_controller.cpp)
ament_target_dependencies(astar_dwa_node rclcpp geometry_msgs nav_msgs sensor_msgs std_msgs visualization_msgs tf2 tf2_ros)

install(TARGETS astar_dwa_node DESTINATION lib/${PROJECT_NAME})
install(DIRECTORY rviz DESTINATION share/${PROJECT_NAME})
ament_get_python_install_dir(PYTHON_INSTALL_DIR)
set(PYTHON_REFERENCE_SOURCE "${CMAKE_CURRENT_SOURCE_DIR}/../../python_deps")
ament_python_install_module("${PYTHON_REFERENCE_SOURCE}/robot.py" DESTINATION_SUFFIX codes_diploma)
install(FILES "${PYTHON_REFERENCE_SOURCE}/astar_project/__init__.py"
  "${PYTHON_REFERENCE_SOURCE}/astar_project/grid_map.py"
  DESTINATION "${PYTHON_INSTALL_DIR}/codes_diploma/astar_project")
if(BUILD_TESTING)
  enable_testing()
  add_executable(test_path_tracking test/test_path_tracking.cpp)
  add_test(NAME path_tracking COMMAND test_path_tracking)
endif()
ament_package()
````````

### `Projekt/Gazebo_ROS2/src/astar_dwa_controller/package.xml`

````````xml
<?xml version="1.0"?>
<package format="3">
  <name>astar_dwa_controller</name>
  <version>0.1.0</version>
  <description>Robotfüggetlen C++ A* és DWA ROS 2 vezérlő.</description>
  <maintainer email="rumdaniel@todo.todo">rumdaniel</maintainer>
  <license>MIT</license>
  <buildtool_depend>ament_cmake</buildtool_depend>
  <buildtool_depend>ament_cmake_python</buildtool_depend>
  <exec_depend>python3-numpy</exec_depend>
  <depend>rclcpp</depend>
  <depend>geometry_msgs</depend>
  <depend>nav_msgs</depend>
  <depend>sensor_msgs</depend>
  <depend>std_msgs</depend>
  <depend>visualization_msgs</depend>
  <depend>tf2</depend>
  <depend>tf2_ros</depend>
  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>
````````

### `Projekt/Gazebo_ROS2/src/astar_dwa_controller/rviz/astar_dwa.rviz`

````````yaml
Panels:
  - Class: rviz_common/Displays
    Name: Displays
  - Class: rviz_common/Views
    Name: Views
Visualization Manager:
  Class: ""
  Displays:
    - Class: rviz_default_plugins/Grid
      Name: Ground grid
      Enabled: true
      Cell Size: 1
      Plane: XY
      Plane Cell Count: 20
      Reference Frame: <Fixed Frame>
    - Class: rviz_default_plugins/Map
      Name: SLAM occupancy map
      Enabled: true
      Topic:
        Depth: 1
        Durability Policy: Transient Local
        History Policy: Keep Last
        Reliability Policy: Reliable
        Value: /map
      Alpha: 0.45
      Color Scheme: map
      Draw Behind: true
    - Class: rviz_default_plugins/Map
      Name: Planner inflated map
      Enabled: false
      Topic:
        Depth: 1
        Durability Policy: Transient Local
        History Policy: Keep Last
        Reliability Policy: Reliable
        Value: /astar_map
      Alpha: 0.35
      Color Scheme: map
      Draw Behind: true
    - Class: rviz_default_plugins/TF
      Name: TF
      Enabled: true
      Frame Timeout: 15
      Marker Scale: 0.5
      Show Arrows: false
      Show Axes: false
      Show Names: false
    - Class: rviz_default_plugins/LaserScan
      Name: LiDAR
      Enabled: true
      Topic:
        Depth: 5
        Durability Policy: Volatile
        History Policy: Keep Last
        Reliability Policy: Best Effort
        Value: /scan
      Size (m): 0.04
      Style: Points
      Color: 255; 170; 0
      Decay Time: 0.2
    - Class: rviz_default_plugins/Path
      Name: A* planned path
      Enabled: true
      Topic:
        Depth: 1
        Durability Policy: Transient Local
        History Policy: Keep Last
        Reliability Policy: Reliable
        Value: /astar_path
      Color: 0; 255; 40
      Line Style: Billboards
      Line Width: 0.05
    - Class: rviz_default_plugins/Odometry
      Name: Odometry
      Enabled: false
      Topic:
        Depth: 5
        Durability Policy: Volatile
        History Policy: Keep Last
        Reliability Policy: Reliable
        Value: /odom
      Keep: 100
      Shape: Arrow
      Color: 80; 150; 255
      Shaft Length: 0.35
      Shaft Radius: 0.04
    - Class: rviz_default_plugins/MarkerArray
      Name: A* and DWA internals
      Enabled: true
      Marker Topic: /astar_dwa_markers
  Enabled: true
  Global Options:
    Background Color: 35; 40; 48
    Fixed Frame: map
    Frame Rate: 30
  Name: root
  Tools:
    - Class: rviz_default_plugins/Interact
    - Class: rviz_default_plugins/MoveCamera
    - Class: rviz_default_plugins/Select
    - Class: rviz_default_plugins/SetInitialPose
      Topic: /initialpose
    - Class: rviz_default_plugins/SetGoal
      Topic: /goal_pose
  Views:
    Current:
      Class: rviz_default_plugins/TopDownOrtho
      Name: Top view
      Angle: 0
      Scale: 80
      Target Frame: map
      X: 4
      Y: 2.5
Window Geometry:
  Height: 900
  Width: 1400
  X: 50
  Y: 50
````````

### `Projekt/Gazebo_ROS2/src/astar_dwa_controller/src/path_tracking.hpp`

````````cpp
#pragma once

#include <algorithm>
#include <cmath>
#include <cstddef>
#include <functional>
#include <limits>
#include <utility>
#include <vector>

namespace path_tracking {
using Path = std::vector<std::pair<double, double>>;

struct PathPosition {
  double along{0.0};
  double distance{std::numeric_limits<double>::infinity()};
};

inline PathPosition project_position(const Path & path, std::size_t first, std::size_t last,
                                     double x, double y) {
  PathPosition result;
  if (path.empty()) return result;
  first = std::min(first, path.size() - 1);
  last = std::clamp(last, first, path.size() - 1);
  result.distance = std::hypot(x - path[first].first, y - path[first].second);
  double accumulated = 0.0;
  for (std::size_t index = first; index < last; ++index) {
    const double delta_x = path[index + 1].first - path[index].first;
    const double delta_y = path[index + 1].second - path[index].second;
    const double length = std::hypot(delta_x, delta_y);
    const double fraction = length > 0.0 ? std::clamp(
      ((x - path[index].first) * delta_x + (y - path[index].second) * delta_y) / (length * length), 0.0, 1.0) : 0.0;
    const double distance = std::hypot(x - path[index].first - fraction * delta_x,
                                       y - path[index].second - fraction * delta_y);
    if (distance < result.distance) {
      result.distance = distance;
      result.along = accumulated + fraction * length;
    }
    accumulated += length;
  }
  return result;
}

struct TrackingTarget {
  std::size_t waypoint{0}, target_index{0};
  std::pair<double, double> projection, target;
  double lookahead{0.35};
};

inline TrackingTarget prune_lookahead(
  const Path & path, std::size_t current, double x, double y, double velocity,
  const std::function<bool(const std::pair<double, double> &)> & reachable) {
  TrackingTarget result;
  if (path.empty()) return result;
  current = std::min(current, path.size() - 1);
  result.waypoint = result.target_index = current;
  result.projection = result.target = path[current];
  result.lookahead = std::clamp(0.35 + std::abs(velocity) * 1.2, 0.35, 0.80);
  if (path.size() == 1) return result;
  const std::size_t first = current > 0 ? current - 1 : 0;
  const std::size_t end = std::min(path.size() - 1, current + 25);
  std::size_t segment = first;
  bool found = false;
  double nearest = std::numeric_limits<double>::infinity();
  for (std::size_t index = first; index < end; ++index) {
    const double delta_x = path[index + 1].first - path[index].first;
    const double delta_y = path[index + 1].second - path[index].second;
    const double length_squared = delta_x * delta_x + delta_y * delta_y;
    const double fraction = length_squared > 0.0 ? std::clamp(
      ((x - path[index].first) * delta_x + (y - path[index].second) * delta_y) / length_squared, 0.0, 1.0) : 0.0;
    const std::pair<double, double> projected{
      path[index].first + fraction * delta_x, path[index].second + fraction * delta_y};
    const double distance = std::hypot(projected.first - x, projected.second - y);
    // Never skip to a distant branch when nearby projections are temporarily blocked.
    if (distance > std::max(1.0, 2.0 * result.lookahead)) continue;
    if (distance >= nearest || !reachable(projected)) continue;
    nearest = distance;
    found = true;
    segment = index;
    result.projection = projected;
    result.waypoint = std::max(current, index + (fraction > 1e-9 ? 1 : 0));
  }
  const auto along_path = [&](double remaining) {
    auto start = result.projection;
    for (std::size_t index = segment + 1; index < path.size(); ++index) {
      const double delta_x = path[index].first - start.first;
      const double delta_y = path[index].second - start.second;
      const double length = std::hypot(delta_x, delta_y);
      if (length > 0.0 && remaining < length) {
        return std::make_pair(std::pair<double, double>{start.first + remaining / length * delta_x,
                                                       start.second + remaining / length * delta_y}, index);
      }
      remaining -= length;
      start = path[index];
    }
    return std::make_pair(path.back(), path.size() - 1);
  };
  if (!found) {
    const auto fallback = along_path(result.lookahead);
    result.target = fallback.first;
    result.target_index = fallback.second;
    return result;
  }
  for (double lookahead = result.lookahead; lookahead >= 0.05; lookahead *= 0.5) {
    const auto candidate = along_path(lookahead);
    if (!reachable(candidate.first)) continue;
    result.target = candidate.first;
    result.target_index = candidate.second;
    result.lookahead = lookahead;
    return result;
  }
  const auto fallback = along_path(std::max(0.05, result.lookahead));
  result.target = fallback.first;
  result.target_index = fallback.second;
  return result;
}

inline double distance_to_path(const Path & path, std::size_t first, std::size_t last,
                               double x, double y) {
  if (path.empty()) return std::numeric_limits<double>::infinity();
  first = std::min(first, path.size() - 1);
  last = std::clamp(last, first, path.size() - 1);
  double nearest = std::hypot(x - path[first].first, y - path[first].second);
  for (std::size_t index = first; index < last; ++index) {
    const auto & start = path[index];
    const auto & end = path[index + 1];
    const double dx = end.first - start.first;
    const double dy = end.second - start.second;
    const double length_squared = dx * dx + dy * dy;
    // Measure against the finite segment, not just its waypoints or an infinite line.
    const double fraction = length_squared > 0.0 ? std::clamp(
      ((x - start.first) * dx + (y - start.second) * dy) / length_squared, 0.0, 1.0) : 0.0;
    nearest = std::min(nearest, std::hypot(
      x - start.first - fraction * dx, y - start.second - fraction * dy));
  }
  return nearest;
}

inline double tracking_cost(const Path & path, std::size_t first, std::size_t last,
                            double x, double y, double target_x, double target_y,
                            double path_distance_bias, double goal_distance_bias) {
  return path_distance_bias * distance_to_path(path, first, last, x, y) +
         goal_distance_bias * std::hypot(target_x - x, target_y - y);
}

inline double return_progress(double initial_distance, double final_distance, double max_travel) {
  return std::clamp((initial_distance - final_distance) / std::max(max_travel, 1e-3), -1.0, 1.0);
}

inline bool is_returning(double initial_distance, double final_distance,
                         double tolerance, double max_travel) {
  return initial_distance > tolerance &&
         (final_distance <= tolerance ||
          return_progress(initial_distance, final_distance, max_travel) >= 0.05);
}

inline bool prefer_candidate(bool returning, double score, bool best_returning, double best_score) {
  return returning != best_returning ? returning : score > best_score;
}

inline std::pair<double, double> rejoin_command(double target_distance, double heading_error,
                                               double max_linear, double max_angular) {
  const double angular = std::clamp(2.0 * heading_error, -max_angular, max_angular);
  const double linear = std::abs(heading_error) >= 1.2 ? 0.0 :
    std::min(max_linear, 1.5 * target_distance) * std::max(0.0, std::cos(heading_error));
  return {linear, angular};
}

inline double command_error(double linear, double angular,
                             const std::pair<double, double> & reference,
                             double max_linear, double max_angular) {
  const double linear_error = (linear - reference.first) / std::max(max_linear, 1e-3);
  const double angular_error = (angular - reference.second) / std::max(max_angular, 1e-3);
  return linear_error * linear_error + angular_error * angular_error;
}

inline bool collision_course(double relative_x, double relative_y,
                              double relative_vx, double relative_vy,
                              double clearance, double horizon) {
  if (std::hypot(relative_x, relative_y) <= clearance) return true;
  const double closing_dot = relative_x * relative_vx + relative_y * relative_vy;
  const double speed_squared = relative_vx * relative_vx + relative_vy * relative_vy;
  if (closing_dot >= 0.0 || speed_squared < 1e-9) return false;
  const double closest_time = std::clamp(-closing_dot / speed_squared, 0.0, horizon);
  return std::hypot(relative_x + relative_vx * closest_time,
                    relative_y + relative_vy * closest_time) <= clearance;
}
}
````````

### `Projekt/Gazebo_ROS2/src/astar_dwa_controller/src/reference_controller.cpp`

````````cpp
#include <chrono>
#include <deque>
#include <memory>
#include <stdexcept>
#include <string>

#include "geometry_msgs/msg/pose_stamped.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "nav_msgs/msg/occupancy_grid.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include "nav_msgs/msg/path.hpp"
#include "rclcpp/rclcpp.hpp"
#include "rclcpp/create_timer.hpp"
#include "sensor_msgs/msg/point_cloud2.hpp"
#include "sensor_msgs/point_cloud2_iterator.hpp"
#include "std_msgs/msg/bool.hpp"
#include "tf2/exceptions.h"
#include "tf2_ros/buffer.h"
#include "tf2_ros/transform_listener.h"
#include "reference_planner.hpp"

namespace planner = reference_planner;

class ReferenceController final : public rclcpp::Node {
public:
  ReferenceController() : Node("astar_dwa_node") {
    config_.wheel_radius = declare_parameter("r_kerek", config_.wheel_radius);
    config_.half_axle = declare_parameter("b", config_.half_axle);
    config_.wheel_max = declare_parameter("w_kerek_max", config_.wheel_max);
    config_.wheel_resolution = declare_parameter("w_kerek_resolution", config_.wheel_resolution);
    config_.acceleration = declare_parameter("a_max", config_.acceleration);
    config_.dt = declare_parameter("dt", config_.dt);
    config_.predict_time = declare_parameter("predict_time", config_.predict_time);
    config_.radius = declare_parameter("rob_radius", config_.radius);
    config_.safety_margin = declare_parameter("safety_margin", config_.safety_margin);
    config_.static_margin = declare_parameter("static_safety_margin", config_.static_margin);
    config_.alpha = declare_parameter("Alfa", config_.alpha);
    config_.beta = declare_parameter("Beta", config_.beta);
    config_.gamma = declare_parameter("Gamma", config_.gamma);
    config_.dynamic_clearance_weight = declare_parameter("dynamic_clearance_weight", config_.dynamic_clearance_weight);
    config_.dynamic_clearance_distance = declare_parameter("dynamic_clearance_distance", config_.dynamic_clearance_distance);
    config_.waypoint_slowdown = declare_parameter("enable_waypoint_slowdown", false);
    inflation_ = declare_parameter("map_inflation_radius", config_.radius + config_.static_margin);
    for (double value : {config_.wheel_radius, config_.half_axle, config_.wheel_max,
                        config_.wheel_resolution, config_.acceleration, config_.dt,
                        config_.predict_time, config_.radius, config_.dynamic_clearance_distance})
      if (!std::isfinite(value) || value <= 0.0) throw std::invalid_argument("Invalid robot parameter");
    for (double value : {inflation_, config_.safety_margin, config_.static_margin,
                        config_.alpha, config_.beta, config_.gamma, config_.dynamic_clearance_weight})
      if (!std::isfinite(value) || value < 0.0) throw std::invalid_argument("Invalid margin or weight");
    buffer_ = std::make_unique<tf2_ros::Buffer>(get_clock());
    listener_ = std::make_unique<tf2_ros::TransformListener>(*buffer_);
    command_pub_ = create_publisher<geometry_msgs::msg::Twist>("/cmd_vel", 10);
    const auto latched = rclcpp::QoS(1).transient_local();
    active_pub_ = create_publisher<std_msgs::msg::Bool>("/controller_active", latched);
    path_pub_ = create_publisher<nav_msgs::msg::Path>("/astar_path", latched);
    goal_pub_ = create_publisher<geometry_msgs::msg::PoseStamped>("/accepted_goal", latched);
    map_pub_ = create_publisher<nav_msgs::msg::OccupancyGrid>("/astar_map", latched);
    map_sub_ = create_subscription<nav_msgs::msg::OccupancyGrid>("/map", latched,
      [this](nav_msgs::msg::OccupancyGrid::ConstSharedPtr message) { receive_map(message); });
    odom_sub_ = create_subscription<nav_msgs::msg::Odometry>("/odom", rclcpp::SensorDataQoS(),
      [this](nav_msgs::msg::Odometry::ConstSharedPtr message) {
        odometry_.push_back(message);
        if (odometry_.size() > 50) odometry_.pop_front();
      });
    obstacle_sub_ = create_subscription<sensor_msgs::msg::PointCloud2>("/tracked_obstacles", 10,
      [this](sensor_msgs::msg::PointCloud2::ConstSharedPtr message) {
        clouds_.push_back(message);
        if (clouds_.size() > 10) clouds_.pop_front();
      });
    goal_sub_ = create_subscription<geometry_msgs::msg::PoseStamped>("/goal_pose", 10,
      [this](geometry_msgs::msg::PoseStamped::ConstSharedPtr message) {
        pending_goal_ = message;
        active_ = false;
        waypoints_.clear();
        path_.clear();
        publish_path();
        stop("new_goal");
      });
    timer_ = rclcpp::create_timer(this, get_clock(), rclcpp::Duration::from_seconds(config_.dt),
                                 [this]() { control(); });
    RCLCPP_INFO(get_logger(),
      "DIAG_CONFIG backend=cpp-python-reference schema=cpp-dwa-8 lidar_fov=360 pruning=25 path_progress=1 dt=%.3f horizon=%.3f radius=%.3f "
      "half_axle=%.4f wheel_max=%.3f weights=(%.1f,%.1f,%.1f) dynamic_clearance_weight=%.1f dynamic_clearance_distance=%.2f wheel_resolution=%.2f",
      config_.dt, config_.predict_time, config_.radius, config_.half_axle,
      config_.wheel_max, config_.alpha, config_.beta, config_.gamma, config_.dynamic_clearance_weight,
      config_.dynamic_clearance_distance, config_.wheel_resolution);
  }

  void shutdown_command() { command_pub_->publish(geometry_msgs::msg::Twist{}); }

private:
  static double seconds(const builtin_interfaces::msg::Time & stamp) {
    return stamp.sec + stamp.nanosec * 1e-9;
  }
  static double yaw(const geometry_msgs::msg::Quaternion & rotation) {
    return std::atan2(2.0 * (rotation.w * rotation.z + rotation.x * rotation.y),
                      1.0 - 2.0 * (rotation.y * rotation.y + rotation.z * rotation.z));
  }
  bool transform(const std::string & source, const builtin_interfaces::msg::Time & stamp,
                 geometry_msgs::msg::Transform & result) {
    if (source.empty()) return false;
    if (source == frame_) {
      result = geometry_msgs::msg::Transform{};
      result.rotation.w = 1.0;
      return true;
    }
    try {
      result = buffer_->lookupTransform(frame_, source, rclcpp::Time(stamp)).transform;
      return true;
    } catch (const tf2::TransformException & error) {
      RCLCPP_WARN_THROTTLE(get_logger(), *get_clock(), 2000,
        "DIAG_TF_CPP %s -> %s: %s", source.c_str(), frame_.c_str(), error.what());
      return false;
    }
  }
  static planner::Point project(double x, double y, const geometry_msgs::msg::Transform & transform) {
    const double heading = yaw(transform.rotation);
    return {transform.translation.x + std::cos(heading) * x - std::sin(heading) * y,
            transform.translation.y + std::sin(heading) * x + std::cos(heading) * y};
  }
  void receive_map(nav_msgs::msg::OccupancyGrid::ConstSharedPtr message) {
    const auto & info = message->info;
    if (message->header.frame_id.empty() || !std::isfinite(info.resolution) || info.resolution <= 0.0 ||
        info.width == 0 || info.height == 0 || info.width > 10000 || info.height > 10000 ||
        message->data.size() != static_cast<std::size_t>(info.width) * info.height ||
        !std::isfinite(info.origin.position.x) || !std::isfinite(info.origin.position.y) ||
        std::abs(yaw(info.origin.orientation)) > 1e-6 ||
        std::abs(info.origin.orientation.x) > 1e-6 || std::abs(info.origin.orientation.y) > 1e-6) {
      RCLCPP_ERROR(get_logger(), "DIAG_MAP invalid or rotated map");
      return;
    }
    if (!frame_.empty() && frame_ != message->header.frame_id) {
      active_ = false;
      path_.clear();
      waypoints_.clear();
      have_odom_ = have_obstacles_ = false;
      odometry_.clear();
      clouds_.clear();
      stop("map_frame_changed");
    }
    frame_ = message->header.frame_id;
    grid_.width = static_cast<int>(info.width);
    grid_.height = static_cast<int>(info.height);
    grid_.resolution = info.resolution;
    grid_.origin_x = info.origin.position.x;
    grid_.origin_y = info.origin.position.y;
    grid_.blocked.resize(message->data.size());
    static_occupied_.resize(message->data.size());
    for (std::size_t index = 0; index < message->data.size(); ++index) {
      static_occupied_[index] = message->data[index] >= 65;
      grid_.blocked[index] = message->data[index] < 0 ? 2 : message->data[index] >= 65 ? 1 : 0;
    }
    const int radius = static_cast<int>(std::ceil(inflation_ / grid_.resolution));
    for (int row = 0; row < grid_.height; ++row) {
      for (int column = 0; column < grid_.width; ++column) {
        if (message->data[static_cast<std::size_t>(row) * grid_.width + column] < 65) continue;
        for (int delta_row = -radius; delta_row <= radius; ++delta_row) {
          for (int delta_column = -radius; delta_column <= radius; ++delta_column) {
            const int next_row = row + delta_row, next_column = column + delta_column;
            if (next_row < 0 || next_column < 0 || next_row >= grid_.height || next_column >= grid_.width ||
                std::hypot(delta_row, delta_column) * grid_.resolution > inflation_) continue;
            grid_.blocked[static_cast<std::size_t>(next_row) * grid_.width + next_column] = 1;
          }
        }
      }
    }
    auto inflated = *message;
    for (std::size_t index = 0; index < grid_.blocked.size(); ++index)
      inflated.data[index] = grid_.blocked[index] == 2 ? -1 : grid_.blocked[index] == 1 ? 100 : 0;
    map_pub_->publish(inflated);
    have_map_ = true;
    publish_path();
    RCLCPP_INFO(get_logger(), "DIAG_MAP cpp size=%dx%d resolution=%.3f preserved_waypoints=%zu",
      grid_.width, grid_.height, grid_.resolution, waypoints_.size());
  }
  void process_inputs() {
    if (!have_map_) return;
    for (auto iterator = odometry_.rbegin(); iterator != odometry_.rend(); ++iterator) {
      const auto & message = **iterator;
      geometry_msgs::msg::Transform conversion;
      if (!transform(message.header.frame_id, message.header.stamp, conversion)) continue;
      const auto position = project(message.pose.pose.position.x, message.pose.pose.position.y, conversion);
      if (active_ && have_odom_) {
        const double elapsed = std::max(0.0, seconds(message.header.stamp) - odom_stamp_);
        const double jump = std::hypot(position.first - state_.x, position.second - state_.y);
        const double limit = std::max(0.5, config_.wheel_max * config_.wheel_radius * elapsed + 0.2);
        if (jump > limit) {
          active_ = false;
          pending_goal_.reset();
          waypoints_.clear();
          path_.clear();
          publish_path();
          stop("localization_jump");
          RCLCPP_ERROR(get_logger(),
            "DIAG_LOCALIZATION jump=%.3f limit=%.3f previous=(%.3f,%.3f) received=(%.3f,%.3f); "
            "navigation cancelled; verify localization before sending a new goal",
            jump, limit, state_.x, state_.y, position.first, position.second);
        }
      }
      state_.x = position.first;
      state_.y = position.second;
      state_.yaw = yaw(message.pose.pose.orientation) + yaw(conversion.rotation);
      state_.velocity = message.twist.twist.linear.x;
      state_.angular = message.twist.twist.angular.z;
      state_.left = (state_.velocity - state_.angular * config_.half_axle) / config_.wheel_radius;
      state_.right = (state_.velocity + state_.angular * config_.half_axle) / config_.wheel_radius;
      odom_stamp_ = seconds(message.header.stamp);
      have_odom_ = std::isfinite(state_.x) && std::isfinite(state_.y) && std::isfinite(state_.yaw) &&
        std::isfinite(state_.left) && std::isfinite(state_.right);
      break;
    }
    while (!odometry_.empty() && seconds(odometry_.front()->header.stamp) <= odom_stamp_) odometry_.pop_front();
    for (auto iterator = clouds_.rbegin(); iterator != clouds_.rend(); ++iterator) {
      const auto & message = **iterator;
      geometry_msgs::msg::Transform conversion;
      if (!transform(message.header.frame_id, message.header.stamp, conversion)) continue;
      std::vector<planner::Obstacle> points;
      std::vector<bool> represented_static_cells(static_occupied_.size(), false);
      const double heading = yaw(conversion.rotation);
      try {
        if (!message.data.empty()) {
          sensor_msgs::PointCloud2ConstIterator<float> point_x(message, "x"), point_y(message, "y"),
            radius(message, "radius"), velocity_x(message, "vx"), velocity_y(message, "vy");
          for (; point_x != point_x.end(); ++point_x, ++point_y, ++radius, ++velocity_x, ++velocity_y) {
            if (!std::isfinite(*point_x) || !std::isfinite(*point_y) || !std::isfinite(*radius) ||
                !std::isfinite(*velocity_x) || !std::isfinite(*velocity_y) || *radius < 0.0) continue;
            const auto position = project(*point_x, *point_y, conversion);
            const auto [row, column] = grid_.cell(position);
            if (row >= 0 && column >= 0 && row < grid_.height && column < grid_.width) {
              const auto cell_index = static_cast<std::size_t>(row) * grid_.width + column;
              if (cell_index < static_occupied_.size() && static_occupied_[cell_index]) {
                if (represented_static_cells[cell_index]) continue;
                represented_static_cells[cell_index] = true;
                const auto cell_center = grid_.world(row, column);
                points.push_back({cell_center.first, cell_center.second,
                  grid_.resolution / std::sqrt(2.0), 0.0, 0.0});
                continue;
              }
            }
            points.push_back({position.first, position.second, *radius,
              std::cos(heading) * *velocity_x - std::sin(heading) * *velocity_y,
              std::sin(heading) * *velocity_x + std::cos(heading) * *velocity_y});
          }
        }
      } catch (const std::runtime_error & error) {
        RCLCPP_ERROR(get_logger(), "DIAG_CLOUD invalid fields: %s", error.what());
        have_obstacles_ = false;
        return;
      }
      obstacles_ = std::move(points);
      obstacle_stamp_ = seconds(message.header.stamp);
      have_obstacles_ = true;
      break;
    }
    while (!clouds_.empty() && seconds(clouds_.front()->header.stamp) <= obstacle_stamp_) clouds_.pop_front();
  }
  void publish_path() {
    nav_msgs::msg::Path message;
    message.header.frame_id = frame_.empty() ? "map" : frame_;
    // Zero stamp: RViz uses the latest TF, so the path is not dropped when the map->odom TF lags behind.
    message.header.stamp = rclcpp::Time(0, 0, get_clock()->get_clock_type());
    for (const auto & point : path_) {
      geometry_msgs::msg::PoseStamped pose;
      pose.header = message.header;
      pose.pose.position.x = point.first;
      pose.pose.position.y = point.second;
      pose.pose.orientation.w = 1.0;
      message.poses.push_back(pose);
    }
    path_pub_->publish(message);
  }
  void plan_goal() {
    if (!pending_goal_ || !have_map_ || !have_odom_) return;
    geometry_msgs::msg::Transform conversion;
    const auto message = pending_goal_;
    if (!transform(message->header.frame_id.empty() ? frame_ : message->header.frame_id,
                   message->header.stamp, conversion)) return;
    pending_goal_.reset();
    const auto goal = project(message->pose.position.x, message->pose.position.y, conversion);
    if (!std::isfinite(goal.first) || !std::isfinite(goal.second)) { stop("invalid_goal"); return; }
    path_ = grid_.smooth(grid_.astar({state_.x, state_.y}, goal));
    if (path_.empty()) { publish_path(); stop("no_global_path"); return; }
    path_.back() = goal;
    if (!grid_.safe(path_)) { path_.clear(); publish_path(); stop("unsafe_endpoint"); return; }
    waypoints_ = planner::resample(path_);
    waypoint_ = std::min<std::size_t>(1, waypoints_.size() - 1);
    active_ = true;
    auto accepted = *message;
    accepted.header.frame_id = frame_;
    accepted.header.stamp = now();
    accepted.pose.position.x = goal.first;
    accepted.pose.position.y = goal.second;
    goal_pub_->publish(accepted);
    publish_path();
    RCLCPP_INFO(get_logger(), "DIAG_GOAL cpp accepted=(%.3f,%.3f) waypoints=%zu", goal.first, goal.second, waypoints_.size());
  }
  void stop(const char * reason) {
    shutdown_command();
    std_msgs::msg::Bool status;
    status.data = active_;
    active_pub_->publish(status);
    RCLCPP_INFO_THROTTLE(get_logger(), *get_clock(), 2000, "DIAG_CONTROL cpp reason=%s", reason);
  }
  void control() {
    process_inputs();
    if (!have_map_ || !have_odom_ || !have_obstacles_) { stop("waiting_inputs"); return; }
    const double age = now().seconds() - std::min(odom_stamp_, obstacle_stamp_);
    if (age > std::max(0.5, 3.0 * config_.dt) || age < -0.05) { stop("stale_input"); return; }
    plan_goal();
    if (!active_ || waypoints_.empty()) { stop("inactive"); return; }
    const double goal_distance = std::hypot(waypoints_.back().first - state_.x, waypoints_.back().second - state_.y);
    const double tolerance = std::max(0.05, std::min(0.2, goal_distance * 0.2));
    if (goal_distance <= tolerance) { active_ = false; stop("finished"); return; }
    const auto previous_waypoint = waypoint_;
    const auto tracking = path_tracking::prune_lookahead(
      waypoints_, waypoint_, state_.x, state_.y, state_.velocity,
      [this](const planner::Point & point) {
        return grid_.safe(planner::Path{{state_.x, state_.y}, point});
      });
    waypoint_ = tracking.waypoint;
    auto obstacles = obstacles_;
    for (auto & obstacle : obstacles) {
      obstacle.x += obstacle.vx * (odom_stamp_ - obstacle_stamp_);
      obstacle.y += obstacle.vy * (odom_stamp_ - obstacle_stamp_);
    }
    const auto start = std::chrono::steady_clock::now();
    const auto result = planner::optimise(config_, state_, tracking.target,
                        tracking.target == waypoints_.back(), obstacles, &waypoints_, waypoint_);
    const double compute_ms = std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - start).count();
    if (now().seconds() - std::min(odom_stamp_, obstacle_stamp_) > std::max(0.5, 3.0 * config_.dt)) {
      waypoint_ = previous_waypoint;
      stop("planner_deadline");
      return;
    }
    auto predicted = state_;
    planner::update(predicted, config_, result.command);
    geometry_msgs::msg::Twist command;
    command.linear.x = predicted.velocity;
    command.angular.z = predicted.angular;
    command_pub_->publish(command);
    std_msgs::msg::Bool status;
    status.data = active_;
    active_pub_->publish(status);
    std::size_t moving_points = 0;
    double max_obstacle_speed = 0.0;
    for (const auto & obstacle : obstacles) {
      const double speed = std::hypot(obstacle.vx, obstacle.vy);
      if (speed > 0.0) ++moving_points;
      max_obstacle_speed = std::max(max_obstacle_speed, speed);
    }
    RCLCPP_INFO_THROTTLE(get_logger(), *get_clock(), 1000,
      "DIAG_CONTROL cpp reason=%s pose=(%.3f,%.3f,%.3f) measured=(%.3f,%.3f) "
      "waypoint=%zu/%zu pruned=%zu lookahead=%.3f target_index=%zu target=(%.3f,%.3f) observed=%zu pairs=%zu admissible=%zu "
      "reject_velocity=%zu reject_dynamic=%zu reject_dynamic_now=%zu reject_braking=%zu forward_pairs=%zu moving_points=%zu max_obstacle_speed=%.3f "
      "score_progress=%.3f score_dynamic=%.3f score_distance=%.3f clearance_gain=%.3f clearance_preferred=%d "
      "cmd=(%.3f,%.3f) avoidance_priority=%d reorient=%d goal_heading_error=%.3f odom_age=%.3f obstacle_age=%.3f compute_ms=%.2f",
      result.found ? "command" : "braking_no_pair", state_.x, state_.y, state_.yaw,
      state_.velocity, state_.angular, waypoint_, waypoints_.size(), waypoint_ - previous_waypoint,
      tracking.lookahead, tracking.target_index, tracking.target.first, tracking.target.second,
      obstacles.size(), result.candidates, result.admissible,
      result.rejected_velocity, result.rejected_dynamic, result.rejected_dynamic_now, result.rejected_braking,
      result.forward_pairs, moving_points, max_obstacle_speed,
      result.score_progress, result.score_dynamic, result.score_distance,
      result.clearance_gain, result.clearance_preferred,
      command.linear.x, command.angular.z,
      result.approaching_obstacle, result.reorient,
      planner::angle_error(std::atan2(tracking.target.second - state_.y,
          tracking.target.first - state_.x) - state_.yaw),
      now().seconds() - odom_stamp_, now().seconds() - obstacle_stamp_, compute_ms);
  }

  planner::Config config_;
  planner::Grid grid_;
  planner::State state_;
  planner::Path path_, waypoints_;
  std::vector<planner::Obstacle> obstacles_;
  std::vector<bool> static_occupied_;
  std::size_t waypoint_{0};
  double inflation_{0.0}, odom_stamp_{0.0}, obstacle_stamp_{0.0};
  bool have_map_{false}, have_odom_{false}, have_obstacles_{false}, active_{false};
  std::string frame_;
  std::deque<nav_msgs::msg::Odometry::ConstSharedPtr> odometry_;
  std::deque<sensor_msgs::msg::PointCloud2::ConstSharedPtr> clouds_;
  geometry_msgs::msg::PoseStamped::ConstSharedPtr pending_goal_;
  std::unique_ptr<tf2_ros::Buffer> buffer_;
  std::unique_ptr<tf2_ros::TransformListener> listener_;
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr command_pub_;
  rclcpp::Publisher<std_msgs::msg::Bool>::SharedPtr active_pub_;
  rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr path_pub_;
  rclcpp::Publisher<nav_msgs::msg::OccupancyGrid>::SharedPtr map_pub_;
  rclcpp::Publisher<geometry_msgs::msg::PoseStamped>::SharedPtr goal_pub_;
  rclcpp::Subscription<nav_msgs::msg::OccupancyGrid>::SharedPtr map_sub_;
  rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr odom_sub_;
  rclcpp::Subscription<sensor_msgs::msg::PointCloud2>::SharedPtr obstacle_sub_;
  rclcpp::Subscription<geometry_msgs::msg::PoseStamped>::SharedPtr goal_sub_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char ** argv) {
  rclcpp::init(argc, argv);
  auto node = std::make_shared<ReferenceController>();
  rclcpp::spin(node);
  if (rclcpp::ok()) node->shutdown_command();
  rclcpp::shutdown();
  return 0;
}
````````

### `Projekt/Gazebo_ROS2/src/astar_dwa_controller/src/reference_planner.hpp`

````````cpp
#pragma once

#include <algorithm>
#include <cmath>
#include <cstddef>
#include <cstdint>
#include <functional>
#include <limits>
#include <queue>
#include <tuple>
#include <utility>
#include <vector>
#include "path_tracking.hpp"

namespace reference_planner {
constexpr double pi = 3.14159265358979323846;
using Point = std::pair<double, double>;
using Path = std::vector<Point>;

inline double angle_error(double angle) {
	return std::atan2(std::sin(angle), std::cos(angle));
}

struct Config {
	double wheel_radius{0.033}, half_axle{0.1435}, wheel_max{0.26 / 0.033};
	double wheel_resolution{0.5}, acceleration{1.0}, dt{0.1}, predict_time{3.0};
	double radius{0.237}, safety_margin{0.15}, static_margin{0.03};
	double alpha{5.0}, beta{2.0}, gamma{3.0};
	double dynamic_clearance_weight{4.0}, dynamic_clearance_distance{0.6};
	bool waypoint_slowdown{false};
};

struct State {
	double x{0.0}, y{0.0}, yaw{0.0}, velocity{0.0}, angular{0.0}, left{0.0}, right{0.0};
};

struct Obstacle { double x, y, radius, vx, vy; };
struct Command { double velocity{0.0}, angular{0.0}, left{0.0}, right{0.0}; };
struct Result {
	Command command;
	std::size_t candidates{0}, admissible{0};
	std::size_t rejected_velocity{0}, rejected_dynamic{0}, rejected_braking{0};
	std::size_t rejected_dynamic_now{0};
	std::size_t forward_pairs{0};
	double score_progress{0.0}, score_dynamic{0.0}, score_distance{0.0};
	double clearance_gain{0.0};
	bool found{false};
	bool clearance_preferred{false};
	bool reorient{false}, approaching_obstacle{false};
};

inline Command kinematics(double left, double right, const Config & config) {
	return {(left + right) * 0.5 * config.wheel_radius,
					(right - left) * config.wheel_radius / (2.0 * config.half_axle), left, right};
}

inline void update(State & state, const Config & config, const Command & target) {
	const double step = config.acceleration / config.wheel_radius * config.dt;
	state.left += std::clamp(target.left - state.left, -step, step);
	state.right += std::clamp(target.right - state.right, -step, step);
	const auto command = kinematics(state.left, state.right, config);
	if (std::abs(command.angular) > 1e-6) {
		state.x += command.velocity / command.angular *
			(std::sin(state.yaw + command.angular * config.dt) - std::sin(state.yaw));
		state.y -= command.velocity / command.angular *
			(std::cos(state.yaw + command.angular * config.dt) - std::cos(state.yaw));
	} else {
		state.x += command.velocity * std::cos(state.yaw) * config.dt;
		state.y += command.velocity * std::sin(state.yaw) * config.dt;
	}
	state.yaw += command.angular * config.dt;
	state.velocity = command.velocity;
	state.angular = command.angular;
}

struct Trajectory {
	double distance{10.0};
	double dynamic_clearance{std::numeric_limits<double>::infinity()};
	bool dynamic_collision{false};
	bool initial_dynamic_collision{false};
};

inline Trajectory trajectory_distance(const Config & config, const State & state,
																	const Command & command, const std::vector<Obstacle> & obstacles) {
	State predicted = state;
	double travelled = 0.0;
	Trajectory result;
	for (std::size_t step = 0; step * config.dt < config.predict_time; ++step) {
		for (const auto & obstacle : obstacles) {
			const bool moving = obstacle.vx != 0.0 || obstacle.vy != 0.0;
			const double clearance = config.radius + obstacle.radius +
				(moving ? config.safety_margin : config.static_margin);
			const double separation = std::hypot(predicted.x - obstacle.x - obstacle.vx * step * config.dt,
				predicted.y - obstacle.y - obstacle.vy * step * config.dt) - clearance;
			if (moving) result.dynamic_clearance = std::min(result.dynamic_clearance, separation);
			if (separation <= 0.0) {
				if (result.distance == 10.0) result.distance = travelled;
				if (moving) {
					result.dynamic_collision = true;
					result.initial_dynamic_collision = step == 0;
					return result;
				}
			}
		}
		update(predicted, config, command);
		travelled += std::abs(command.velocity) * config.dt;
	}
	return result;
}

inline std::vector<double> wheel_samples(double measured, const Config & config) {
	const double step = config.acceleration / config.wheel_radius * config.dt;
	const double lower = std::clamp(measured - step, -config.wheel_max, config.wheel_max);
	const double upper = std::clamp(measured + step, -config.wheel_max, config.wheel_max);
	std::vector<double> samples;
	const auto count = static_cast<std::size_t>(std::ceil((upper - lower) / config.wheel_resolution));
	for (std::size_t index = 0; index <= count; ++index)
		samples.push_back(std::min(upper, lower + index * config.wheel_resolution));
	return samples;
}

inline void add_rotation_samples(std::vector<double> & left_samples,
								 std::vector<double> & right_samples,
								 const State & state, const Config & config,
								 double preferred_left) {
	const double step = config.acceleration / config.wheel_radius * config.dt;
	const double left_min = std::max(-config.wheel_max, state.left - step);
	const double left_max = std::min(config.wheel_max, state.left + step);
	const double right_min = std::max(-config.wheel_max, state.right - step);
	const double right_max = std::min(config.wheel_max, state.right + step);
	const double rotation_min = std::max(left_min, -right_max);
	const double rotation_max = std::min(left_max, -right_min);
	if (rotation_min > rotation_max) return;
	const auto append_unique = [](std::vector<double> & samples, double value) {
		if (std::none_of(samples.begin(), samples.end(), [value](double sample) {
				return std::abs(sample - value) < 1e-9;
			})) samples.push_back(value);
	};
	for (const double left : {rotation_min, rotation_max,
							  std::clamp(preferred_left, rotation_min, rotation_max)}) {
		append_unique(left_samples, left);
		append_unique(right_samples, -left);
	}
}

inline Result optimise(const Config & config, const State & state, Point goal,
											 bool final_waypoint, const std::vector<Obstacle> & sensed,
											 const Path * reference_path = nullptr, std::size_t waypoint = 0) {
	std::vector<Obstacle> visible;
	for (const auto & obstacle : sensed) {
		if (std::hypot(obstacle.x - state.x, obstacle.y - state.y) <= 3.0)
			visible.push_back(obstacle);
	}
	const double goal_distance = std::hypot(goal.first - state.x, goal.second - state.y);
	const double near_goal_horizon = goal_distance < 1.0 ? std::max(0.5, goal_distance * 2.0) : config.predict_time;
	const double maximum_velocity = config.wheel_max * config.wheel_radius;
	const bool track_path = reference_path != nullptr && !reference_path->empty();
	const std::size_t first = track_path ? std::min(waypoint > 0 ? waypoint - 1 : 0, reference_path->size() - 1) : 0;
	const std::size_t last = track_path ? std::min(first + 25, reference_path->size() - 1) : 0;
	const double initial_path_position = track_path ?
		path_tracking::project_position(*reference_path, first, last, state.x, state.y).along : 0.0;
	const double heading_error = angle_error(std::atan2(goal.second - state.y, goal.first - state.x) - state.yaw);
	bool approaching_obstacle = false;
	for (const auto & obstacle : visible) {
		if (obstacle.vx == 0.0 && obstacle.vy == 0.0) continue;
		if (path_tracking::collision_course(obstacle.x - state.x, obstacle.y - state.y,
				obstacle.vx - maximum_velocity * std::cos(state.yaw + heading_error),
				obstacle.vy - maximum_velocity * std::sin(state.yaw + heading_error),
				config.radius + obstacle.radius + config.safety_margin, config.predict_time)) {
			approaching_obstacle = true;
			break;
		}
	}
	const double horizon = approaching_obstacle ? config.predict_time : near_goal_horizon;
	const double heading_scale = approaching_obstacle ? 0.25 : 1.0;
	const auto braking_trajectory = approaching_obstacle ?
		trajectory_distance(config, state, Command{}, visible) : Trajectory{};
	const bool reorient = std::abs(heading_error) > pi / 2.0 && !approaching_obstacle;
	const double target_speed = reorient ? 0.0 : maximum_velocity;
	const double velocity_limit = reorient ? std::max(0.0, state.velocity - config.acceleration * config.dt) : maximum_velocity;
	auto left_samples = wheel_samples(state.left, config);
	auto right_samples = wheel_samples(state.right, config);
	const double preferred_rotation = reorient ?
		-heading_error * config.half_axle / config.wheel_radius : 0.0;
	add_rotation_samples(left_samples, right_samples, state, config, preferred_rotation);
	const bool slowdown = config.waypoint_slowdown || final_waypoint;
	const double slowdown_distance = final_waypoint ? 0.5 : 0.35;
	double best_score = -std::numeric_limits<double>::infinity();
	double best_rotation_score = -std::numeric_limits<double>::infinity();
	Command best_rotation;
	bool have_rotation = false;
	Result result;
	result.reorient = reorient;
	result.approaching_obstacle = approaching_obstacle;
	for (double left : left_samples) {
		for (double right : right_samples) {
			++result.candidates;
			const auto command = kinematics(left, right, config);
			if (command.velocity < 0.0 || command.velocity > velocity_limit + 1e-9) {
				++result.rejected_velocity;
				continue;
			}
			const auto trajectory = trajectory_distance(config, state, command, visible);
			if (trajectory.dynamic_collision) {
				++result.rejected_dynamic;
				if (trajectory.initial_dynamic_collision) ++result.rejected_dynamic_now;
				continue;
			}
			if (command.velocity > std::sqrt(2.0 * config.acceleration * trajectory.distance)) {
				++result.rejected_braking;
				continue;
			}
			++result.admissible;
			if (command.velocity > 0.01) ++result.forward_pairs;
			State predicted = state;
			for (std::size_t step = 0; step * config.dt < horizon; ++step) update(predicted, config, command);
			const double heading = std::atan2(goal.second - predicted.y, goal.first - predicted.x);
			const double heading_score = (pi - std::abs(angle_error(heading - predicted.yaw))) / pi;
			const double predicted_goal_distance = std::hypot(goal.first - predicted.x, goal.second - predicted.y);
			const double progress = track_path ?
				path_tracking::project_position(*reference_path, first, last, predicted.x, predicted.y).along - initial_path_position :
				goal_distance - predicted_goal_distance;
			const double progress_score = std::clamp(
				progress / (maximum_velocity * horizon), -1.0, 1.0);
			const double target_velocity = std::min(target_speed, std::max(0.08, goal_distance * 1.4));
			const double velocity_score = !slowdown && goal_distance > slowdown_distance ?
				command.velocity / maximum_velocity :
				1.0 - std::abs(target_velocity - command.velocity) / maximum_velocity;
			const double dynamic_score = std::isfinite(trajectory.dynamic_clearance) ?
				std::clamp(trajectory.dynamic_clearance / config.dynamic_clearance_distance, 0.0, 1.0) : 0.0;
			const double clearance_gain = approaching_obstacle && std::isfinite(braking_trajectory.dynamic_clearance) ?
				trajectory.dynamic_clearance - braking_trajectory.dynamic_clearance : 0.0;
			const bool clearance_preferred = approaching_obstacle && command.velocity > 0.01 && clearance_gain > 0.02;
			const double score = config.alpha * (heading_scale * heading_score + progress_score) + config.beta * trajectory.distance +
				config.gamma * velocity_score + config.dynamic_clearance_weight * dynamic_score;
			if (std::abs(command.velocity) <= 1e-9 && std::abs(command.angular) > 1e-6) {
				if (!have_rotation || score > best_rotation_score) {
					best_rotation_score = score;
					best_rotation = command;
					have_rotation = true;
				}
				continue;
			}
			if (!result.found || path_tracking::prefer_candidate(
					clearance_preferred, score, result.clearance_preferred, best_score)) {
				best_score = score;
				result.command = command;
				result.found = true;
				result.clearance_preferred = clearance_preferred;
				result.clearance_gain = clearance_gain;
				result.score_progress = config.alpha * progress_score;
				result.score_dynamic = config.dynamic_clearance_weight * dynamic_score;
				result.score_distance = config.beta * trajectory.distance;
			}
		}
	}
	if (result.forward_pairs == 0 && have_rotation) {
		result.command = best_rotation;
		result.found = true;
	}
	return result;
}

struct Grid {
	int width{0}, height{0};
	double resolution{0.1}, origin_x{0.0}, origin_y{0.0};
	std::vector<std::int8_t> blocked;

	bool free(int row, int column) const {
		return row >= 0 && column >= 0 && row < height && column < width &&
			blocked[static_cast<std::size_t>(row) * width + column] == 0;
	}
	std::pair<int, int> cell(Point point) const {
		return {static_cast<int>(std::floor((point.second - origin_y) / resolution)),
						static_cast<int>(std::floor((point.first - origin_x) / resolution))};
	}
	Point world(int row, int column) const {
		return {origin_x + (column + 0.5) * resolution, origin_y + (row + 0.5) * resolution};
	}
	bool connected(std::pair<int, int> start, std::pair<int, int> finish) const {
		const int row_step = finish.first - start.first, column_step = finish.second - start.second;
		return std::abs(row_step) <= 1 && std::abs(column_step) <= 1 && free(finish.first, finish.second) &&
			(row_step == 0 || column_step == 0 || (free(start.first, finish.second) && free(finish.first, start.second)));
	}
	Path astar(Point start_world, Point goal_world) const {
		const auto start = cell(start_world), goal = cell(goal_world);
		if (!free(start.first, start.second) || !free(goal.first, goal.second)) return {};
		const auto index = [this](int row, int column) { return row * width + column; };
		const auto heuristic = [&goal](int row, int column) { return std::hypot(goal.first - row, goal.second - column); };
		using Entry = std::tuple<double, double, int, int>;
		std::priority_queue<Entry, std::vector<Entry>, std::greater<Entry>> open;
		std::vector<double> costs(blocked.size(), std::numeric_limits<double>::infinity());
		std::vector<int> parents(blocked.size(), -1);
		costs[index(start.first, start.second)] = 0.0;
		open.emplace(heuristic(start.first, start.second), 0.0, start.first, start.second);
		const int directions[8][2] = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}, {-1, -1}, {-1, 1}, {1, -1}, {1, 1}};
		while (!open.empty()) {
			const auto [priority, cost, row, column] = open.top();
			(void)priority;
			open.pop();
			if (cost > costs[index(row, column)]) continue;
			if (std::make_pair(row, column) == goal) break;
			for (const auto & direction : directions) {
				const int next_row = row + direction[0], next_column = column + direction[1];
				if (!connected({row, column}, {next_row, next_column})) continue;
				const double next_cost = cost + std::hypot(direction[0], direction[1]);
				const int next_index = index(next_row, next_column);
				if (next_cost >= costs[next_index]) continue;
				costs[next_index] = next_cost;
				parents[next_index] = index(row, column);
				open.emplace(next_cost + heuristic(next_row, next_column), next_cost, next_row, next_column);
			}
		}
		int current = index(goal.first, goal.second);
		const int first = index(start.first, start.second);
		if (current != first && parents[current] < 0) return {};
		Path path;
		while (current >= 0) {
			path.push_back(world(current / width, current % width));
			if (current == first) break;
			current = parents[current];
		}
		std::reverse(path.begin(), path.end());
		return path;
	}
	bool safe(const Path & path) const {
		if (path.empty()) return true;
		auto previous = cell(path.front());
		if (!free(previous.first, previous.second)) return false;
		for (std::size_t index = 1; index < path.size(); ++index) {
			const Point delta{path[index].first - path[index - 1].first, path[index].second - path[index - 1].second};
			const int count = std::max(1, static_cast<int>(std::ceil(std::max(std::abs(delta.first), std::abs(delta.second)) / resolution)));
			for (int step = 1; step <= count; ++step) {
				const double fraction = static_cast<double>(step) / count;
				const auto next = cell({path[index - 1].first + fraction * delta.first, path[index - 1].second + fraction * delta.second});
				if (!connected(previous, next)) return false;
				previous = next;
			}
		}
		return true;
	}
	Path smooth(const Path & path) const {
		if (path.size() < 3) return path;
		Path turns{path.front()};
		for (std::size_t index = 1; index + 1 < path.size(); ++index) {
			const double incoming_x = path[index].first - path[index - 1].first;
			const double incoming_y = path[index].second - path[index - 1].second;
			const double outgoing_x = path[index + 1].first - path[index].first;
			const double outgoing_y = path[index + 1].second - path[index].second;
			if (std::abs(incoming_x * outgoing_y - incoming_y * outgoing_x) > 1e-10) turns.push_back(path[index]);
		}
		turns.push_back(path.back());
		if (turns.size() < 3) return path;
		const auto cut = [this](Point center, Point neighbor) {
			const double length = std::hypot(neighbor.first - center.first, neighbor.second - center.second);
			const double fraction = length == 0.0 ? 1.0 : std::min(1.0, 0.5 * resolution / length);
			return Point{center.first + fraction * (neighbor.first - center.first), center.second + fraction * (neighbor.second - center.second)};
		};
		Path curve{turns.front()};
		for (std::size_t index = 1; index + 1 < turns.size(); ++index) {
			const Point start = index == 1 ? turns.front() : cut(turns[index], turns[index - 1]);
			const Point finish = index + 2 == turns.size() ? turns.back() : cut(turns[index], turns[index + 1]);
			for (int sample = 1; sample <= 8; ++sample) {
				const double parameter = sample / 8.0, weight = 1.0 - parameter;
				curve.emplace_back(weight * weight * start.first + 2.0 * weight * parameter * turns[index].first + parameter * parameter * finish.first,
													 weight * weight * start.second + 2.0 * weight * parameter * turns[index].second + parameter * parameter * finish.second);
			}
		}
		curve.push_back(turns.back());
		for (std::size_t index = 1; index + 1 < curve.size(); ++index) {
			if ((curve[index].first - curve[index - 1].first) * (curve[index + 1].first - curve[index].first) +
					(curve[index].second - curve[index - 1].second) * (curve[index + 1].second - curve[index].second) < -1e-9) return path;
		}
		return safe(curve) ? curve : path;
	}
};

inline Path resample(const Path & path, double spacing = 0.2) {
	if (path.empty()) return {};
	Path points{path.front()};
	double remaining = spacing;
	Point start = path.front();
	for (std::size_t index = 1; index < path.size(); ++index) {
		double delta_x = path[index].first - start.first, delta_y = path[index].second - start.second;
		double length = std::hypot(delta_x, delta_y);
		if (length == 0.0) continue;
		while (length >= remaining) {
			const double fraction = remaining / length;
			start = {start.first + fraction * delta_x, start.second + fraction * delta_y};
			points.push_back(start);
			delta_x = path[index].first - start.first;
			delta_y = path[index].second - start.second;
			length = std::hypot(delta_x, delta_y);
			remaining = spacing;
		}
		remaining -= length;
		start = path[index];
	}
	if (points.back() != path.back()) points.push_back(path.back());
	return points;
}
}
````````

### `Projekt/Gazebo_ROS2/src/astar_dwa_controller/test/test_path_tracking.cpp`

````````cpp
#include "../src/path_tracking.hpp"

#include <cmath>
#include <iostream>
#include <stdexcept>

int main() {
  path_tracking::Path path;
  for (int i = 0; i <= 30; ++i) path.emplace_back(i * 0.2, 0.0);

  const auto local = path_tracking::prune_lookahead(
    path, 3, 0.6, 0.5, 0.0, [](const auto &) { return true; });
  if (local.waypoint > 4 || local.target.first > 1.1) {
    throw std::runtime_error("Nearby path tracking must stay local");
  }

  const auto distant_only = path_tracking::prune_lookahead(
    path, 3, 0.6, 0.5, 0.0, [](const auto & point) { return point.first >= 3.0; });
  if (distant_only.waypoint != 3 || distant_only.target.first > 1.1) {
    throw std::runtime_error("An unreachable local path must not cause a distant waypoint jump");
  }
  std::cout << "Path tracking checks passed\n";
}
````````

### `Projekt/Gazebo_ROS2/src/dwa_gazebo_sim/config/slam.yaml`

````````yaml
slam_toolbox:
  ros__parameters:
    solver_plugin: solver_plugins::CeresSolver
    ceres_linear_solver: SPARSE_NORMAL_CHOLESKY
    ceres_preconditioner: SCHUR_JACOBI
    ceres_trust_strategy: LEVENBERG_MARQUARDT
    ceres_dogleg_type: TRADITIONAL_DOGLEG
    ceres_loss_function: None
    odom_frame: odom
    map_frame: map
    base_frame: base_link
    scan_topic: /scan
    use_map_saver: true
    mode: $(var slam_mode)
    map_file_name: "$(var map_file)"
    map_start_pose: [$(var initial_x), $(var initial_y), $(var initial_yaw)]
    use_sim_time: true
    debug_logging: false
    throttle_scans: 1
    transform_publish_period: 0.02
    map_update_interval: 2.0
    resolution: $(var map_resolution)
    restamp_tf: false
    min_laser_range: 0.0
    max_laser_range: 3.0
    minimum_time_interval: 0.1
    transform_timeout: 0.2
    tf_buffer_duration: 30.0
    stack_size_to_use: 40000000
    enable_interactive_mode: true
    use_scan_matching: true
    use_scan_barycenter: true
    minimum_travel_distance: 0.1
    minimum_travel_heading: 0.1
    scan_buffer_size: 10
    scan_buffer_maximum_scan_distance: 3.0
    link_match_minimum_response_fine: 0.1
    link_scan_maximum_distance: 1.5
    loop_search_maximum_distance: 3.0
    do_loop_closing: true
    loop_match_minimum_chain_size: 10
    loop_match_maximum_variance_coarse: 3.0
    loop_match_minimum_response_coarse: 0.35
    loop_match_minimum_response_fine: 0.45
    correlation_search_space_dimension: 0.5
    correlation_search_space_resolution: 0.01
    correlation_search_space_smear_deviation: 0.1
    loop_search_space_dimension: 8.0
    loop_search_space_resolution: 0.05
    loop_search_space_smear_deviation: 0.03
    distance_variance_penalty: 0.5
    angle_variance_penalty: 1.0
    fine_search_angle_offset: 0.00349
    coarse_search_angle_offset: 0.349
    coarse_angle_resolution: 0.0349
    minimum_angle_penalty: 0.9
    minimum_distance_penalty: 0.5
    use_response_expansion: true
    min_pass_through: 2
    occupancy_threshold: 0.1
````````

### `Projekt/Gazebo_ROS2/src/dwa_gazebo_sim/dwa_gazebo_sim/__init__.py`

````````python

````````

### `Projekt/Gazebo_ROS2/src/dwa_gazebo_sim/dwa_gazebo_sim/gazebo_path_node.py`

````````python
"""Draw a non-colliding global path on the Gazebo floor without blocking control."""

import math
import time
import xml.etree.ElementTree as ET
from collections import deque

import rclpy
from nav_msgs.msg import Odometry, Path
from rclpy.node import Node
from rclpy.time import Time
from ros_gz_interfaces.srv import DeleteEntity, SetEntityPose, SpawnEntity
from tf2_ros import Buffer, TransformException, TransformListener


def project_path_points(points, source_to_odom, odom_pose, world_pose):
    """Align display coordinates only; never correct the navigation state."""
    offset_x, offset_y, source_yaw = source_to_odom
    correction_yaw = world_pose[2] - odom_pose[2]
    source_cos, source_sin = math.cos(source_yaw), math.sin(source_yaw)
    world_cos, world_sin = math.cos(correction_yaw), math.sin(correction_yaw)
    projected = []
    for point_x, point_y in points:
        delta_x = offset_x + source_cos * point_x - source_sin * point_y - odom_pose[0]
        delta_y = offset_y + source_sin * point_x + source_cos * point_y - odom_pose[1]
        projected.append((world_pose[0] + world_cos * delta_x - world_sin * delta_y,
                          world_pose[1] + world_sin * delta_x + world_cos * delta_y))
    return tuple(projected)


def pose_2d(pose):
    rotation = pose.orientation
    yaw = math.atan2(2 * (rotation.w * rotation.z + rotation.x * rotation.y),
                     1 - 2 * (rotation.y ** 2 + rotation.z ** 2))
    return pose.position.x, pose.position.y, yaw


def path_sdf(points):
    sdf = ET.Element("sdf", version="1.8")
    model = ET.SubElement(sdf, "model", name="python_global_path")
    ET.SubElement(model, "static").text = "true"
    link = ET.SubElement(model, "link", name="path")
    for index, (start, end) in enumerate(zip(points, points[1:])):
        dx, dy = end[0] - start[0], end[1] - start[1]
        length = math.hypot(dx, dy)
        if length < 1e-6:
            continue
        visual = ET.SubElement(link, "visual", name=f"segment_{index}")
        ET.SubElement(visual, "pose").text = (
            f"{(start[0] + end[0]) / 2} {(start[1] + end[1]) / 2} 0.015 0 0 {math.atan2(dy, dx)}")
        ET.SubElement(visual, "cast_shadows").text = "false"
        geometry = ET.SubElement(visual, "geometry")
        ET.SubElement(ET.SubElement(geometry, "box"), "size").text = f"{length} 0.04 0.01"
        material = ET.SubElement(visual, "material")
        ET.SubElement(material, "ambient").text = "0.1 0.9 0.2 1"
        ET.SubElement(material, "diffuse").text = "0.1 0.9 0.2 1"
    return ET.tostring(sdf, encoding="unicode")


class GazeboPathDisplay:
    def __init__(self, node):
        self.node = node
        self.latest = self.drawn = self.pending = None
        self.drawn_source = self.pending_source = None
        self.model_pose = self.pending_model_pose = None
        self.fixed_alignment = None
        self.alignment_frame = None
        self.path_frame = None
        self.odometry = deque(maxlen=200)
        self.ground_truth = None
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, node)
        self.busy, self.generation, self.deadline = False, 0, 0.0
        self.spawn = node.create_client(SpawnEntity, "/world/dwa_world/create")
        self.delete = node.create_client(DeleteEntity, "/world/dwa_world/remove")
        self.move = node.create_client(SetEntityPose, "/world/dwa_world/set_pose")
        node.create_subscription(Path, "/astar_path", self.path, 10)
        node.create_subscription(Odometry, "/odom", self.record_odometry, 10)
        node.create_subscription(Odometry, "/gazebo/ground_truth_odom", self.record_ground_truth, 10)
        node.create_timer(0.5, self.tick)

    def record_odometry(self, message):
        self.odometry.append(message)

    def record_ground_truth(self, message):
        self.ground_truth = message

    def path(self, message):
        points = tuple((pose.pose.position.x, pose.pose.position.y) for pose in message.poses)
        if all(math.isfinite(value) for point in points for value in point):
            self.latest = points
            self.path_frame = message.header.frame_id

    def world_points(self):
        if not self.latest:
            return self.latest
        if self.fixed_alignment is not None and self.alignment_frame == self.path_frame:
            self.model_pose = self.fixed_alignment
            offset_x, offset_y, yaw = self.fixed_alignment
            cosine, sine = math.cos(yaw), math.sin(yaw)
            return tuple((offset_x + cosine * point_x - sine * point_y,
                          offset_y + sine * point_x + cosine * point_y)
                         for point_x, point_y in self.latest)
        if self.ground_truth is None or not self.odometry or not self.path_frame:
            self.node.get_logger().warning(
                "DIAG_PATH reason=waiting_alignment", throttle_duration_sec=5.0)
            return None
        truth = self.ground_truth
        truth_time = Time.from_msg(truth.header.stamp).nanoseconds
        odom = min(self.odometry, key=lambda message: abs(
            Time.from_msg(message.header.stamp).nanoseconds - truth_time))
        odom_time = Time.from_msg(odom.header.stamp).nanoseconds
        if abs(odom_time - truth_time) > 50000000 or odom.child_frame_id != truth.child_frame_id:
            self.node.get_logger().warning(
                f"DIAG_PATH reason=alignment_mismatch odom_child={odom.child_frame_id} "
                f"world_child={truth.child_frame_id}", throttle_duration_sec=5.0)
            return None
        age = self.node.get_clock().now().nanoseconds - truth_time
        if age < 0 or age > 500000000:
            self.node.get_logger().warning("DIAG_PATH reason=stale_alignment", throttle_duration_sec=5.0)
            return None
        if self.path_frame == odom.header.frame_id:
            source_to_odom = (0.0, 0.0, 0.0)
        else:
            try:
                transform = self.tf_buffer.lookup_transform(
                    odom.header.frame_id, self.path_frame, Time.from_msg(odom.header.stamp)).transform
            except TransformException as error:
                self.node.get_logger().warning(
                    f"DIAG_PATH reason=tf_missing frame={self.path_frame} error={error}",
                    throttle_duration_sec=5.0)
                return None
            rotation = transform.rotation
            yaw = math.atan2(2 * (rotation.w * rotation.z + rotation.x * rotation.y),
                             1 - 2 * (rotation.y ** 2 + rotation.z ** 2))
            source_to_odom = (transform.translation.x, transform.translation.y, yaw)
        projected = project_path_points(self.latest, source_to_odom,
                                        pose_2d(odom.pose.pose), pose_2d(truth.pose.pose))
        if not all(math.isfinite(value) for point in projected for value in point):
            self.node.get_logger().warning("DIAG_PATH reason=nonfinite_projection", throttle_duration_sec=5.0)
            return None
        anchors = project_path_points(((0.0, 0.0), (1.0, 0.0)), source_to_odom,
                                      pose_2d(odom.pose.pose), pose_2d(truth.pose.pose))
        self.model_pose = (anchors[0][0], anchors[0][1],
                           math.atan2(anchors[1][1] - anchors[0][1],
                                      anchors[1][0] - anchors[0][0]))
        self.fixed_alignment = self.model_pose
        self.alignment_frame = self.path_frame
        self.node.get_logger().info(
            f"DIAG_PATH reason=alignment_locked frame={self.path_frame} "
            f"world_transform={self.fixed_alignment} navigation_feedback=false")
        return projected

    def tick(self):
        if self.busy:
            if time.monotonic() > self.deadline:
                self.generation += 1
                self.busy = False
                self.node.get_logger().warning("Gazebo path service timed out.", throttle_duration_sec=5.0)
            return
        projected = self.world_points()
        if projected is None:
            return
        if not projected and not self.drawn:
            return
        if self.drawn is not None and len(projected) == len(self.drawn) and all(
                math.hypot(current[0] - previous[0], current[1] - previous[1]) < 0.02
                for current, previous in zip(projected, self.drawn)):
            return
        if not all(client.service_is_ready() for client in (self.spawn, self.delete, self.move)):
            self.node.get_logger().warning("Waiting for Gazebo path services.", throttle_duration_sec=5.0)
            return
        self.pending = projected
        self.pending_source = (self.path_frame, self.latest)
        self.pending_model_pose = self.model_pose
        self.busy, self.deadline = True, time.monotonic() + 10.0
        self.generation += 1
        generation = self.generation
        def place_pose(pose):
            pose.position.x, pose.position.y, yaw = self.pending_model_pose
            pose.orientation.z, pose.orientation.w = math.sin(yaw / 2), math.cos(yaw / 2)

        def failed(error):
            self.busy = False
            self.node.get_logger().warning(f"Gazebo path drawing failed: {error}", throttle_duration_sec=5.0)

        if self.drawn and self.drawn_source == self.pending_source:
            request = SetEntityPose.Request()
            request.entity.name, request.entity.type = "python_global_path", request.entity.MODEL
            place_pose(request.pose)

            def moved(result):
                if generation != self.generation:
                    return
                try:
                    if not result.result().success:
                        raise RuntimeError("Gazebo rejected path pose update")
                    self.drawn, self.busy = self.pending, False
                except Exception as error:
                    failed(error)

            self.move.call_async(request).add_done_callback(moved)
            return

        def deleted(result):
            if generation != self.generation:
                return
            try:
                if result is not None:
                    result.result()
                if len(self.pending) < 2:
                    self.drawn, self.busy = self.pending, False
                    return
                create = SpawnEntity.Request()
                create.entity_factory.name = "python_global_path"
                create.entity_factory.sdf = path_sdf(self.pending_source[1])
                place_pose(create.entity_factory.pose)
                self.spawn.call_async(create).add_done_callback(created)
            except Exception as error:
                failed(error)

        def created(result):
            if generation != self.generation:
                return
            try:
                if not result.result().success:
                    raise RuntimeError("Gazebo rejected the path model")
                self.drawn, self.busy = self.pending, False
                self.drawn_source = self.pending_source
                self.node.get_logger().info(
                    f"DIAG_PATH reason=drawn source_frame={self.path_frame} "
                    f"points={len(self.drawn)} first={self.drawn[0]} last={self.drawn[-1]} "
                    "ground_truth_usage=visualization_only")
            except Exception as error:
                failed(error)

        if not self.drawn:
            deleted(None)
        else:
            request = DeleteEntity.Request()
            request.entity.name, request.entity.type = "python_global_path", request.entity.MODEL
            self.delete.call_async(request).add_done_callback(deleted)


class GazeboPathNode(Node):
    def __init__(self):
        super().__init__("gazebo_global_path")
        self.display = GazeboPathDisplay(self)


def main(args=None):
    rclpy.init(args=args)
    node = GazeboPathNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
````````

### `Projekt/Gazebo_ROS2/src/dwa_gazebo_sim/dwa_gazebo_sim/lidar_obstacle_node.py`

````````python
"""Convert LiDAR surface points and cluster velocity estimates into planner input."""

import math
import time

import numpy as np

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from rclpy.time import Time
from sensor_msgs.msg import LaserScan, PointCloud2, PointField
from sensor_msgs_py import point_cloud2
from std_msgs.msg import Header
from tf2_ros import Buffer, TransformException, TransformListener

MAX_TRACKED_OBSTACLE_SPEED = 0.35


def estimate_cluster_translation(current, previous, initial):
    translation = np.asarray(initial, dtype=float)
    for _ in range(3):
        offsets = current[:, None, :] - (previous[None, :, :] + translation)
        squared_distances = np.sum(offsets * offsets, axis=2)
        nearest = np.argmin(squared_distances, axis=1)
        matched = squared_distances[np.arange(len(current)), nearest] <= 0.15 ** 2
        if np.count_nonzero(matched) < 2:
            return None
        translation = np.median(current[matched] - previous[nearest[matched]], axis=0)
    return translation


class LidarObstacleNode(Node):
    def __init__(self):
        super().__init__("lidar_obstacles")
        self.tracking_frame = self.declare_parameter("tracking_frame", "odom").value
        self.max_range = float(self.declare_parameter("max_range", 3.0).value)
        self.previous, self.last_stamp = [], None
        self.scan_sequence = 0
        self.last_diagnostic_wall = -math.inf
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.publisher = self.create_publisher(PointCloud2, "/tracked_obstacles", 10)
        self.create_subscription(LaserScan, "/scan", self.scan, qos_profile_sensor_data)
        self.get_logger().info(
            f"LiDAR-only tracker: /scan -> /tracked_obstacles; frame={self.tracking_frame}")

    @staticmethod
    def transform_point(transform, x, y):
        rotation = transform.rotation
        yaw = math.atan2(2 * (rotation.w * rotation.z + rotation.x * rotation.y),
                         1 - 2 * (rotation.y ** 2 + rotation.z ** 2))
        return (transform.translation.x + math.cos(yaw) * x - math.sin(yaw) * y,
                transform.translation.y + math.sin(yaw) * x + math.cos(yaw) * y)

    def scan(self, message):
        self.scan_sequence += 1
        stamp = message.header.stamp.sec + message.header.stamp.nanosec * 1e-9
        try:
            transform = self.tf_buffer.lookup_transform(
                self.tracking_frame, message.header.frame_id, Time.from_msg(message.header.stamp)
            ).transform
        except TransformException as error:
            self.get_logger().warning(
                f"DIAG_LIDAR seq={self.scan_sequence} stamp={stamp} reason=tf_missing "
                f"transform={message.header.frame_id}->{self.tracking_frame} error={error}",
                throttle_duration_sec=2.0)
            return
        clusters, last_index = [], -2
        for index, value in enumerate(message.ranges):
            if not math.isfinite(value) or not message.range_min <= value <= min(message.range_max, self.max_range):
                continue
            angle = message.angle_min + index * message.angle_increment
            point = self.transform_point(transform, value * math.cos(angle), value * math.sin(angle))
            if (not clusters or index - last_index > 2 or
                    math.hypot(point[0] - clusters[-1][-1][0], point[1] - clusters[-1][-1][1]) > 0.15):
                clusters.append([])
            clusters[-1].append(point)
            last_index = index
        dt = None if self.last_stamp is None else stamp - self.last_stamp
        tracks, points, used = [], [], set()
        motion_fits = 0
        speed_rejections = 0
        for cluster in clusters:
            surface = np.asarray(cluster[::max(1, (len(cluster) + 63) // 64)], dtype=float)
            x = sum(point[0] for point in cluster) / len(cluster)
            y = sum(point[1] for point in cluster) / len(cluster)
            vx = vy = 0.0
            if dt is not None and 0.02 < dt < 0.5 and len(cluster) >= 2:
                matches = [(math.hypot(x - old[0] - old[2] * dt, y - old[1] - old[3] * dt), index)
                           for index, old in enumerate(self.previous) if index not in used]
                if matches:
                    error, index = min(matches)
                    if error < 0.35:
                        old = self.previous[index]
                        used.add(index)
                        translation = estimate_cluster_translation(
                            surface, old[4], (old[2] * dt, old[3] * dt))
                        if translation is not None:
                            motion_fits += 1
                            vx = 0.6 * old[2] + 0.4 * float(translation[0]) / dt
                            vy = 0.6 * old[3] + 0.4 * float(translation[1]) / dt
                            if math.hypot(vx, vy) < 0.06:
                                vx = vy = 0.0
            if math.hypot(vx, vy) > MAX_TRACKED_OBSTACLE_SPEED:
                vx = vy = 0.0
                speed_rejections += 1
            tracks.append((x, y, vx, vy, surface))
            points.extend((point[0], point[1], 0.0, 0.0, vx, vy) for point in cluster)
        self.previous, self.last_stamp = tracks, stamp
        fields = [PointField(name=name, offset=4 * index, datatype=PointField.FLOAT32, count=1)
                  for index, name in enumerate(("x", "y", "z", "radius", "vx", "vy"))]
        self.publisher.publish(point_cloud2.create_cloud(
            Header(stamp=message.header.stamp, frame_id=self.tracking_frame), fields, points
        ))
        wall_time = time.monotonic()
        if wall_time - self.last_diagnostic_wall >= 2.0:
            self.last_diagnostic_wall = wall_time
            moving = sum(math.hypot(track[2], track[3]) > 0 for track in tracks)
            max_speed = max((math.hypot(track[2], track[3]) for track in tracks), default=0.0)
            age = self.get_clock().now().nanoseconds * 1e-9 - stamp
            self.get_logger().info(
                f"DIAG_LIDAR seq={self.scan_sequence} stamp={stamp:.3f} age={age:.3f} "
                f"frame={self.tracking_frame} scan_dt={dt} rays={len(message.ranges)} "
                f"points={len(points)} clusters={len(clusters)} matches={len(used)} "
                f"motion_fits={motion_fits} speed_rejections={speed_rejections} "
                f"moving_clusters={moving} max_speed={max_speed:.3f} "
                f"sensor_xy=({transform.translation.x:.3f},{transform.translation.y:.3f})")


def main(args=None):
    rclpy.init(args=args)
    node = LidarObstacleNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
````````

### `Projekt/Gazebo_ROS2/src/dwa_gazebo_sim/dwa_gazebo_sim/python_reference.py`

````````python
"""ROS-only copy of the Python scene; original simulation sources stay unchanged."""

import math
import xml.etree.ElementTree as ET

from codes_diploma.astar_project.grid_map import GridMap
from codes_diploma.robot import Obstacle, robotstate

PHYSICS_STEP = 0.001


def create_scene(
    width=30, height=20, resolution=0.2, start_cell=(2, 2),
    goal_cell=(17, 27), inflation_radius=0.11,
):
    grid = GridMap(width=width, height=height, resolution=resolution)
    cells = [(row, min(10, width - 2)) for row in range(2, max(2, height - 2))
             if row not in range(7, 13)]
    cells += [(min(12, height - 2), column) for column in range(12, max(12, width - 2))
              if column not in range(19, 25)]
    for cell in cells:
        if grid.is_inside(*cell) and cell not in (start_cell, goal_cell):
            grid.add_obstacle(*cell)
    grid.inflate_obstacles(inflation_radius)
    start, goal = grid.grid_to_world(*start_cell), grid.grid_to_world(*goal_cell)
    statics = [Obstacle(*grid.grid_to_world(*cell), radius=0.12) for cell in cells]
    dynamic = [Obstacle(2.4, 0.4, radius=0.18, vx=0.0, vy=0.20),
               Obstacle(6.8, 2.1, radius=0.18, vx=-0.25, vy=0.0)]
    return grid, start, goal, robotstate(x=start[0], y=start[1], irany=0.0), statics, dynamic


def create_gazebo_scene(world_file, resolution=0.2, inflation_radius=0.27):
    if not math.isfinite(resolution) or resolution <= 0:
        raise ValueError("Map resolution must be finite and positive")
    world = ET.parse(world_file).getroot().find("world")
    if world is None:
        raise ValueError("Missing Gazebo world")
    models = {model.get("name"): model for model in world.findall("model")}
    poses = {name: [float(value) for value in model.findtext("pose", "0 0 0 0 0 0").split()]
             for name, model in models.items()}
    origin_x, origin_y = poses["boundary_left"][0], poses["boundary_bottom"][1]
    width = math.ceil((poses["boundary_right"][0] - origin_x) / resolution)
    height = math.ceil((poses["boundary_top"][1] - origin_y) / resolution)
    grid = GridMap(width, height, resolution, origin_x, origin_y)
    statics = []
    for name, model in models.items():
        size = model.findtext("link/collision/geometry/box/size")
        if model.findtext("static") != "true" or size is None:
            continue
        x, y, _, roll, pitch, yaw = poses[name]
        if abs(roll) + abs(pitch) + abs(yaw) > 1e-6:
            raise ValueError("The reference world requires axis-aligned walls")
        size_x, size_y, _ = map(float, size.split())
        half_x, half_y = size_x / 2, size_y / 2
        cell_margin = inflation_radius + resolution / math.sqrt(2)
        for row in range(height):
            for column in range(width):
                cell_x, cell_y = grid.grid_to_world(row, column)
                dx, dy = max(abs(cell_x - x) - half_x, 0), max(abs(cell_y - y) - half_y, 0)
                if math.hypot(dx, dy) <= cell_margin:
                    grid.add_obstacle(row, column)
        along_x = size_x >= size_y
        length, thickness = (size_x, size_y) if along_x else (size_y, size_x)
        count = max(1, math.ceil(length / resolution))
        radius = math.hypot(thickness / 2, length / count / 2)
        for index in range(count + 1):
            offset = -length / 2 + length * index / count
            statics.append(Obstacle(x + offset if along_x else x,
                                    y if along_x else y + offset, radius=radius))
    include = world.find("include")
    if include is None:
        raise ValueError("Missing TurtleBot include")
    spawn = [float(value) for value in include.findtext("pose", "0 0 0 0 0 0").split()]
    if abs(spawn[5]) > 1e-6:
        raise ValueError("The reference spawn yaw must be zero")
    start = (spawn[0], spawn[1])
    velocities = {"moving_obstacle_1": (0.0, 0.20), "moving_obstacle_2": (-0.26, 0.0)}
    dynamic = []
    for name, (vx, vy) in velocities.items():
        radius = float(models[name].findtext("link/collision/geometry/cylinder/radius"))
        dynamic.append(Obstacle(*poses[name][:2], radius=radius, vx=vx, vy=vy))
    return grid, start, (6.5, 4.2), robotstate(x=start[0], y=start[1]), statics, dynamic
````````

### `Projekt/Gazebo_ROS2/src/dwa_gazebo_sim/dwa_gazebo_sim/python_simulation_node.py`

````````python
"""Continuous Gazebo odometry and obstacle adapter; no physics stepping."""

import copy
import math
import time

import rclpy
from geometry_msgs.msg import TransformStamped, Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile, qos_profile_sensor_data
from rclpy.time import Time
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool
from tf2_ros import Buffer, StaticTransformBroadcaster, TransformBroadcaster, TransformListener

from .python_reference import create_gazebo_scene
from .gazebo_path_node import GazeboPathDisplay


class GazeboSimulationAdapter:
    def __init__(self, node):
        self.node = node
        self.ground_truth = None
        self.last_diagnostic_wall = -math.inf
        self.last_diagnostic_sim = None
        self.last_tf_diagnostic_wall = -math.inf
        self.last_odom_stamp = None
        self.last_odom_child = None
        self.tf_buffer = Buffer(node=node)
        self.tf_listener = TransformListener(self.tf_buffer, node)
        if not node.has_parameter("world_file"):
            node.declare_parameter("world_file", "")
        world_file = node.get_parameter("world_file").value
        _, self.start, _, _, _, self.obstacles = create_gazebo_scene(world_file)
        self.crossing_enabled = node.declare_parameter("enable_crossing_obstacle", False).value
        obstacle_specs = [(f"moving_obstacle_{index + 1}", obstacle)
                  for index, obstacle in enumerate(self.obstacles)
                  if self.crossing_enabled or index == 1]
        self.obstacles = [obstacle for _, obstacle in obstacle_specs]
        self.obstacle_names = [name for name, _ in obstacle_specs]
        self.oncoming_start_x = float(node.declare_parameter("oncoming_start_x", 0.0).value)
        if not math.isfinite(self.oncoming_start_x):
            raise ValueError("oncoming_start_x must be finite")
        self.crossing_start_x = float(node.declare_parameter("crossing_start_x", 0.8).value)
        if not math.isfinite(self.crossing_start_x):
            raise ValueError("crossing_start_x must be finite")
        self.robot_odom_x = None
        self.oncoming_started = False
        self.crossing_started = False
        self.active = False
        self.last_time = node.get_clock().now().nanoseconds * 1e-9
        self.odom_pub = node.create_publisher(Odometry, "/odom", 10)
        self.obstacle_commands = [node.create_publisher(
            Twist, f"/model/{name}/cmd_vel", 10) for name, _ in obstacle_specs]
        latched = QoSProfile(depth=1, durability=DurabilityPolicy.TRANSIENT_LOCAL)
        node.create_subscription(Bool, "/controller_active", self.set_active, latched)
        node.create_subscription(Odometry, "/gazebo/wheel_odom", self.odom, qos_profile_sensor_data)
        node.create_subscription(Odometry, "/gazebo/ground_truth_odom", self.record_ground_truth, qos_profile_sensor_data)
        node.create_subscription(LaserScan, "/scan", self.inspect_scan_tf, qos_profile_sensor_data)
        self.tf = TransformBroadcaster(node)
        self.static_tf = StaticTransformBroadcaster(node)
        self.odom_child = node.declare_parameter("odom_child_frame", "base_footprint").value
        base_z = float(node.declare_parameter("base_link_z", 0.01).value)
        laser_pose = node.declare_parameter("laser_pose", [-0.064, 0.0, 0.121]).value
        base = TransformStamped()
        base.header.frame_id, base.child_frame_id = self.odom_child, "base_link"
        base.transform.translation.z, base.transform.rotation.w = base_z, 1.0
        laser = TransformStamped()
        laser.header.frame_id, laser.child_frame_id = "base_link", "base_scan"
        laser.transform.translation.x, laser.transform.translation.y, laser.transform.translation.z = laser_pose
        laser.transform.rotation.w = 1.0
        self.static_tf.sendTransform([laser] if self.odom_child == "base_link" else [base, laser])
        node.create_timer(0.10, self.tick)
        node.get_logger().info(
            "python-turtlebot-physical: odometry=wheel; obstacles=LiDAR; "
            "simulation-only adapter; velocity-driven obstacles; physical cmd_vel control")
        node.get_logger().info(
            f"DIAG_SCENARIO crossing_enabled={self.crossing_enabled} "
            f"moving_models={[name for name, _ in obstacle_specs]} "
            f"oncoming_start_x={self.oncoming_start_x} "
            f"crossing_start_x={self.crossing_start_x}")

    def set_active(self, message):
        self.active = message.data

    def record_ground_truth(self, message):
        self.ground_truth = message

    def inspect_scan_tf(self, message):
        wall_time = time.monotonic()
        if wall_time - self.last_tf_diagnostic_wall < 2.0:
            return
        self.last_tf_diagnostic_wall = wall_time
        stamp = Time.from_msg(message.header.stamp)
        scan_age = (self.node.get_clock().now().nanoseconds - stamp.nanoseconds) * 1e-9
        odom_delta = None if self.last_odom_stamp is None else (
            self.last_odom_stamp - stamp.nanoseconds) * 1e-9
        checks = []
        for target, source in (("base_link", message.header.frame_id),
                               ("odom", "base_link"), ("map", "odom")):
            ready, detail = self.tf_buffer.can_transform(
                target, source, stamp, return_debug_tuple=True)
            latest = self.tf_buffer.can_transform(target, source, Time())
            checks.append(f"{target}<-{source}:at_scan={ready},latest={latest},detail={detail}")
        self.node.get_logger().info(
            f"DIAG_TF scan_stamp={stamp.nanoseconds * 1e-9:.3f} scan_age={scan_age:.3f} "
            f"scan_frame={message.header.frame_id} odom_received={self.last_odom_stamp is not None} "
            f"wheel_publishers={self.node.count_publishers('/gazebo/wheel_odom')} "
            f"odom_minus_scan={odom_delta} configured_child={self.odom_child} "
            f"received_child={self.last_odom_child} checks={checks}")

    def odom(self, message):
        mapped = copy.deepcopy(message)
        mapped.header.frame_id = "odom"
        mapped.child_frame_id = message.child_frame_id or self.odom_child
        mapped.pose.pose.position.x += self.start[0]
        mapped.pose.pose.position.y += self.start[1]
        self.robot_odom_x = mapped.pose.pose.position.x
        self.odom_pub.publish(mapped)
        transform = TransformStamped()
        transform.header, transform.child_frame_id = mapped.header, mapped.child_frame_id
        transform.transform.translation.x = mapped.pose.pose.position.x
        transform.transform.translation.y = mapped.pose.pose.position.y
        transform.transform.translation.z = mapped.pose.pose.position.z
        transform.transform.rotation = mapped.pose.pose.orientation
        self.tf.sendTransform(transform)
        self.last_odom_stamp = Time.from_msg(mapped.header.stamp).nanoseconds
        self.last_odom_child = mapped.child_frame_id
        wall_time = time.monotonic()
        if wall_time - self.last_diagnostic_wall >= 2.0:
            stamp = message.header.stamp.sec + message.header.stamp.nanosec * 1e-9
            real_time_factor = None if self.last_diagnostic_sim is None else (
                (stamp - self.last_diagnostic_sim) / (wall_time - self.last_diagnostic_wall))
            self.last_diagnostic_wall = wall_time
            self.last_diagnostic_sim = stamp
            truth_position = None
            truth_delta = None
            error = None
            if self.ground_truth is not None:
                truth = self.ground_truth
                truth_stamp = truth.header.stamp.sec + truth.header.stamp.nanosec * 1e-9
                truth_delta = stamp - truth_stamp
                truth_position = (truth.pose.pose.position.x, truth.pose.pose.position.y)
                if abs(truth_delta) <= 0.2:
                    error = math.hypot(mapped.pose.pose.position.x - truth_position[0],
                                       mapped.pose.pose.position.y - truth_position[1])
            self.node.get_logger().info(
                f"DIAG_ODOM stamp={stamp:.3f} source=wheel "
                f"raw_xy=({message.pose.pose.position.x:.3f},{message.pose.pose.position.y:.3f}) "
                f"spawn_offset={self.start} "
                f"odom_xy=({mapped.pose.pose.position.x:.3f},{mapped.pose.pose.position.y:.3f}) "
                f"truth_xy={truth_position} truth_dt={truth_delta} xy_error={error} "
                f"real_time_factor={real_time_factor} "
                f"child={mapped.child_frame_id}")

    def tick(self):
        now = self.node.get_clock().now().nanoseconds * 1e-9
        dt, self.last_time = max(0.0, now - self.last_time), now
        if (self.active and not self.oncoming_started and self.robot_odom_x is not None and
                self.robot_odom_x >= self.oncoming_start_x):
            self.oncoming_started = True
            self.node.get_logger().info(
                f"DIAG_SCENARIO event=oncoming_started sim_t={now:.3f} "
                f"robot_odom_x={self.robot_odom_x:.3f} threshold={self.oncoming_start_x}")
        if (self.crossing_enabled and self.active and not self.crossing_started and
                self.robot_odom_x is not None and
                self.robot_odom_x >= self.crossing_start_x):
            self.crossing_started = True
            self.node.get_logger().info(
                f"DIAG_SCENARIO event=crossing_started sim_t={now:.3f} "
                f"robot_odom_x={self.robot_odom_x:.3f} threshold={self.crossing_start_x}")
        for name, obstacle, publisher in zip(self.obstacle_names, self.obstacles, self.obstacle_commands):
            moving = self.oncoming_started if name == "moving_obstacle_2" else self.crossing_started
            if moving:
                obstacle.move(dt)
            command = Twist()
            if moving:
                command.linear.x, command.linear.y = obstacle.vx, obstacle.vy
            publisher.publish(command)


class PythonSimulationNode(Node):
    def __init__(self):
        super().__init__("python_simulation")
        self.adapter = GazeboSimulationAdapter(self)
        self.path_display = GazeboPathDisplay(self)


def main(args=None):
    rclpy.init(args=args)
    node = PythonSimulationNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
````````

### `Projekt/Gazebo_ROS2/src/dwa_gazebo_sim/dwa_gazebo_sim/python_world.py`

````````python
"""Generate Gazebo geometry from the ROS copy of the unchanged Python scene."""

import copy
import math
import tempfile
import xml.etree.ElementTree as ET

from codes_diploma.robot import robotconfig
from .python_reference import PHYSICS_STEP, create_scene


def element(parent, tag, value=None, **attributes):
    child = ET.SubElement(parent, tag, attributes)
    if value is not None:
        child.text = str(value)
    return child


def inertial(link, mass, inertia):
    node = element(link, "inertial")
    element(node, "mass", mass)
    tensor = element(node, "inertia")
    for axis in ("ixx", "iyy", "izz"):
        element(tensor, axis, inertia)
    for axis in ("ixy", "ixz", "iyz"):
        element(tensor, axis, 0)


def cylinder(link, radius, length, color, pose="0 0 0 0 0 0"):
    for name in ("collision", "visual"):
        item = element(link, name, name=name)
        element(item, "pose", pose)
        geometry = element(item, "geometry")
        shape = element(geometry, "cylinder")
        element(shape, "radius", radius)
        element(shape, "length", length)
        if name == "visual":
            material = element(item, "material")
            element(material, "ambient", color)
            element(material, "diffuse", color)


def write_world_with_pose_odometry(world_file, model_file, enable_crossing_obstacle=True,
                                   enable_camera=True):
    tree = ET.parse(world_file)
    world = tree.getroot().find("world")
    if world is None:
        raise ValueError("Missing Gazebo world")
    include = world.find("include")
    model = ET.parse(model_file).getroot().find("model")
    if include is None or model is None:
        raise ValueError("Missing TurtleBot model/include")
    robot = copy.deepcopy(model)
    if not enable_crossing_obstacle:
        for obstacle_model in world.findall("model"):
            if obstacle_model.get("name") == "moving_obstacle_1":
                world.remove(obstacle_model)
    if not enable_camera:
        for link in robot.findall("link"):
            for sensor in link.findall("sensor"):
                if sensor.get("type") in ("camera", "depth_camera", "rgbd_camera"):
                    link.remove(sensor)
    robot.set("name", include.findtext("name", "turtlebot3_waffle"))
    pose = robot.find("pose")
    if pose is None:
        pose = ET.SubElement(robot, "pose")
    pose.text = include.findtext("pose", "0 0 0 0 0 0")
    drive = robot.find("plugin[@name='gz::sim::systems::DiffDrive']")
    if drive is None:
        raise ValueError("Missing TurtleBot differential drive")
    odometry = ET.SubElement(robot, "plugin", filename="gz-sim-odometry-publisher-system",
                             name="gz::sim::systems::OdometryPublisher")
    for key, value in {
        "odom_frame": "odom", "robot_base_frame": drive.findtext("child_frame_id", "base_footprint"),
        "odom_topic": "/world_pose_odom", "tf_topic": "/gazebo/world_pose_tf",
        "dimensions": 2, "odom_publish_frequency": 50, "gaussian_noise": 0,
    }.items():
        element(odometry, key, value)
    world.remove(include)
    world.append(robot)
    with tempfile.NamedTemporaryFile(suffix=".sdf", prefix="turtlebot_pose_", delete=False) as handle:
        tree.write(handle, encoding="utf-8", xml_declaration=True)
        return handle.name


def write_world():
    grid, start, _, _, statics, dynamic = create_scene()
    config = robotconfig()
    sdf = ET.Element("sdf", version="1.8")
    world = element(sdf, "world", name="dwa_world")
    physics = element(world, "physics", name="python_steps", type="ignored")
    element(physics, "max_step_size", PHYSICS_STEP)
    element(physics, "real_time_factor", 1)
    for library, system in (("physics", "Physics"), ("scene-broadcaster", "SceneBroadcaster"),
                            ("user-commands", "UserCommands")):
        element(world, "plugin", filename=f"gz-sim-{library}-system", name=f"gz::sim::systems::{system}")
    light = element(world, "light", name="sun", type="directional")
    element(light, "pose", "0 0 10 0 0 0")
    element(light, "direction", "-0.5 0.1 -0.9")
    ground = element(world, "model", name="ground_plane")
    element(ground, "static", "true")
    link = element(ground, "link", name="link")
    for kind in ("collision", "visual"):
        item = element(link, kind, name=kind)
        geometry = element(item, "geometry")
        plane = element(geometry, "plane")
        element(plane, "normal", "0 0 1")
        element(plane, "size", f"{grid.width * grid.resolution} {grid.height * grid.resolution}")
        if kind == "visual":
            element(item, "pose", f"{grid.width * grid.resolution / 2} {grid.height * grid.resolution / 2} 0 0 0 0")
            material = element(item, "material")
            element(material, "ambient", "0.7 0.75 0.75 1")
            element(material, "diffuse", "0.7 0.75 0.75 1")
    for index, obstacle in enumerate(statics + dynamic):
        moving = index >= len(statics)
        name = f"moving_obstacle_{index - len(statics) + 1}" if moving else f"static_obstacle_{index}"
        model = element(world, "model", name=name)
        element(model, "static", "false" if moving else "true")
        element(model, "pose", f"{obstacle.x} {obstacle.y} 0.45 0 0 0")
        link = element(model, "link", name="link")
        element(link, "gravity", "false")
        inertial(link, 10, 0.1)
        color = "0.1 0.4 0.9 1" if moving else ("0.9 0.7 0.1 1" if obstacle.x > 4 else "0.8 0.15 0.2 1")
        cylinder(link, obstacle.radius, 0.9, color)
    robot = element(world, "model", name="python_robot")
    element(robot, "pose", f"{start[0]} {start[1]} {config.r_kerek} 0 0 0")
    body = element(robot, "link", name="base_link")
    inertial(body, 1, 0.005)
    cylinder(body, config.rob_radius, 0.05, "0.1 0.6 0.6 1", "0 0 0.025 0 0 0")
    for side, sign in (("left", 1), ("right", -1)):
        wheel = element(robot, "link", name=f"{side}_wheel")
        element(wheel, "pose", f"0 {sign * config.b} 0 0 0 0")
        inertial(wheel, 0.05, 0.00003)
        cylinder(wheel, config.r_kerek, 0.02, "0.1 0.1 0.1 1", f"0 0 0 {math.pi / 2} 0 0")
        joint = element(robot, "joint", name=f"{side}_wheel_joint", type="revolute")
        element(joint, "parent", "base_link")
        element(joint, "child", f"{side}_wheel")
        axis = element(joint, "axis")
        element(axis, "xyz", "0 1 0")
    for name, direction in (("front", 1), ("rear", -1)):
        caster = element(robot, "link", name=f"{name}_caster")
        element(caster, "pose", f"{direction * 0.075} 0 -0.023 0 0 0")
        inertial(caster, 0.01, 0.000001)
        collision = element(caster, "collision", name="collision")
        sphere = element(element(collision, "geometry"), "sphere")
        element(sphere, "radius", 0.01)
        friction = element(element(element(collision, "surface"), "friction"), "ode")
        element(friction, "mu", 0.01)
        element(friction, "mu2", 0.01)
        joint = element(robot, "joint", name=f"{name}_caster_joint", type="fixed")
        element(joint, "parent", "base_link")
        element(joint, "child", f"{name}_caster")
    drive = element(robot, "plugin", filename="gz-sim-diff-drive-system", name="gz::sim::systems::DiffDrive")
    for key, value in {
        "left_joint": "left_wheel_joint", "right_joint": "right_wheel_joint",
        "wheel_separation": 2 * config.b, "wheel_radius": config.r_kerek,
        "topic": "/cmd_vel", "odom_topic": "/odom", "tf_topic": "/gazebo/tf",
        "frame_id": "odom", "child_frame_id": "base_link", "odom_publish_frequency": 100,
        "max_linear_acceleration": config.a_max,
        "max_angular_acceleration": config.a_max / config.b,
    }.items():
        element(drive, key, value)
    with tempfile.NamedTemporaryFile(suffix=".sdf", prefix="python_reference_", delete=False) as handle:
        ET.ElementTree(sdf).write(handle, encoding="utf-8", xml_declaration=True)
        return handle.name
````````

### `Projekt/Gazebo_ROS2/src/dwa_gazebo_sim/launch/simulation.launch.py`

````````python
import math
import os
import xml.etree.ElementTree as ET

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, EmitEvent, ExecuteProcess, LogInfo, OpaqueFunction, RegisterEventHandler, SetEnvironmentVariable, SetLaunchConfiguration
from launch.conditions import IfCondition
from launch.events import matches_action
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import LifecycleNode, Node
from launch_ros.descriptions import ParameterFile
from launch_ros.event_handlers import OnStateTransition
from launch_ros.events.lifecycle import ChangeState
from lifecycle_msgs.msg import Transition


def start_reference(context):
    from dwa_gazebo_sim.python_world import write_world_with_pose_odometry

    package_share = get_package_share_directory("dwa_gazebo_sim")
    model_root = os.path.join(get_package_share_directory("turtlebot3_gazebo"), "models")
    world_path = os.path.join(package_share, "worlds", "dwa_world.sdf")
    model = ET.parse(os.path.join(model_root, "turtlebot3_waffle", "model.sdf")).getroot()
    drive = model.find(".//plugin[@name='gz::sim::systems::DiffDrive']")
    laser = model.find(".//sensor[@type='gpu_lidar']")
    collision = model.find(".//link[@name='base_link']/collision")
    if drive is None or laser is None or collision is None:
        raise RuntimeError("The installed TurtleBot Waffle model lacks drive, LiDAR or body geometry")
    wheel_radius = float(drive.findtext("wheel_radius"))
    wheel_base = float(drive.findtext("wheel_separation")) / 2
    body_pose = [float(value) for value in collision.findtext("pose", "0 0 0 0 0 0").split()]
    size = [float(value) for value in collision.findtext("geometry/box/size").split()]
    robot_radius = math.hypot(abs(body_pose[0]) + size[0] / 2, abs(body_pose[1]) + size[1] / 2)
    laser_pose = [float(value) for value in laser.findtext("pose", "0 0 0 0 0 0").split()]
    if any(abs(value) > 1e-6 for value in laser_pose[3:]):
        raise RuntimeError("The reference expects an unrotated TurtleBot LiDAR")
    base_pose = [float(value) for value in model.findtext(
        ".//joint[@name='base_joint']/pose", "0 0 0.01 0 0 0").split()]
    start_environment = LaunchConfiguration("start_environment").perform(context).lower() == "true"
    enable_crossing = LaunchConfiguration("enable_crossing_obstacle").perform(context).lower() == "true"
    enable_camera = LaunchConfiguration("enable_camera").perform(context).lower() == "true"
    slam_mode = LaunchConfiguration("slam_mode").perform(context)
    map_file = LaunchConfiguration("map_file").perform(context).strip()
    map_file = os.path.abspath(os.path.expanduser(map_file)) if map_file else ""
    if start_environment and slam_mode == "localization" and not map_file:
        raise RuntimeError("Localization requires map_file:=/absolute/path/prefix without an extension")
    if start_environment and map_file:
        for extension in (".posegraph", ".data"):
            if not os.path.isfile(map_file + extension):
                raise RuntimeError(f"Missing saved SLAM file: {map_file + extension}")
    initial_pose = [float(LaunchConfiguration(name).perform(context))
                    for name in ("initial_x", "initial_y", "initial_yaw")]
    if not all(math.isfinite(value) for value in initial_pose):
        raise RuntimeError("Initial map pose must contain finite values")
    map_resolution = float(LaunchConfiguration("map_resolution").perform(context))
    if not math.isfinite(map_resolution) or map_resolution <= 0:
        raise RuntimeError("Map resolution must be finite and positive")
    slam_executable = "localization_slam_toolbox_node" if slam_mode == "localization" else "async_slam_toolbox_node"
    slam_config = os.path.join(package_share, "config", "slam.yaml")
    if start_environment and not os.path.isfile(slam_config):
        raise RuntimeError(
            f"Installed SLAM config is missing: {slam_config}. "
            "From the ROS workspace run: colcon build --symlink-install "
            "--packages-select astar_dwa_controller dwa_gazebo_sim; "
            "then source install/setup.bash and verify ros2 pkg prefix dwa_gazebo_sim. "
            "Do not recreate the saved map: the missing file is package configuration.")
    slam_node = LifecycleNode(
        package="slam_toolbox", executable=slam_executable, name="slam_toolbox", namespace="",
        output="screen", condition=IfCondition(LaunchConfiguration("start_environment")),
        parameters=[ParameterFile(slam_config, allow_substs=True),
                    {"use_sim_time": True, "mode": slam_mode, "map_file_name": map_file,
                     "map_start_pose": initial_pose, "resolution": map_resolution,
                     "odom_frame": "odom", "map_frame": "map", "base_frame": "base_link",
                     "scan_topic": "/scan", "max_laser_range": 3.0,
                     "use_lifecycle_manager": False}],
    )
    runtime_world = write_world_with_pose_odometry(
        world_path, os.path.join(model_root, "turtlebot3_waffle", "model.sdf"),
        enable_crossing_obstacle=enable_crossing, enable_camera=enable_camera) if start_environment else world_path
    return [
        SetLaunchConfiguration("map_file", map_file),
        SetLaunchConfiguration("initial_x", str(initial_pose[0])),
        SetLaunchConfiguration("initial_y", str(initial_pose[1])),
        SetLaunchConfiguration("initial_yaw", str(initial_pose[2])),
        SetEnvironmentVariable("GZ_SIM_RESOURCE_PATH", os.pathsep.join(
            [model_root, os.environ.get("GZ_SIM_RESOURCE_PATH", "")])),
        ExecuteProcess(cmd=["gz", "sim", "-r", "-v", LaunchConfiguration("verbose"), runtime_world],
                   output="screen", condition=IfCondition(LaunchConfiguration("start_environment"))),
        Node(
            package="ros_gz_bridge", executable="parameter_bridge", output="screen",
            condition=IfCondition(LaunchConfiguration("start_environment")),
            arguments=[
                "/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist",
                "/model/moving_obstacle_1/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist",
                "/model/moving_obstacle_2/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist",
                "/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry",
                "/world_pose_odom@nav_msgs/msg/Odometry[gz.msgs.Odometry",
                "/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan",
                "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
                "/world/dwa_world/create@ros_gz_interfaces/srv/SpawnEntity",
                "/world/dwa_world/remove@ros_gz_interfaces/srv/DeleteEntity",
                "/world/dwa_world/set_pose@ros_gz_interfaces/srv/SetEntityPose",
            ],
            remappings=[("/odom", "/gazebo/wheel_odom"),
                        ("/world_pose_odom", "/gazebo/ground_truth_odom")],
            parameters=[{"use_sim_time": True}],
        ),
        Node(
            package="dwa_gazebo_sim", executable="python_simulation_node", output="screen",
            condition=IfCondition(LaunchConfiguration("start_environment")),
            parameters=[{"use_sim_time": True, "world_file": world_path,
                         "enable_crossing_obstacle": enable_crossing,
                         "oncoming_start_x": float(LaunchConfiguration("oncoming_start_x").perform(context)),
                         "crossing_start_x": float(LaunchConfiguration("crossing_start_x").perform(context)),
                         "laser_pose": laser_pose[:3], "base_link_z": base_pose[2],
                         "odom_child_frame": drive.findtext("child_frame_id", "base_footprint")}],
        ),
        LogInfo(msg=f"DIAG_SLAM_CONFIG executable={slam_executable} mode={slam_mode} "
                    f"map_file={map_file!r} initial_pose={initial_pose} "
                    f"resolution={map_resolution} params_file={slam_config}",
                condition=IfCondition(LaunchConfiguration("start_environment"))),
        slam_node,
        RegisterEventHandler(
            OnStateTransition(target_lifecycle_node=slam_node, start_state="configuring",
                              goal_state="inactive", entities=[EmitEvent(event=ChangeState(
                                  lifecycle_node_matcher=matches_action(slam_node),
                                  transition_id=Transition.TRANSITION_ACTIVATE))]),
            condition=IfCondition(LaunchConfiguration("start_environment")),
        ),
        EmitEvent(event=ChangeState(lifecycle_node_matcher=matches_action(slam_node),
                                   transition_id=Transition.TRANSITION_CONFIGURE),
                  condition=IfCondition(LaunchConfiguration("start_environment"))),
        Node(
            package="astar_dwa_controller", executable="astar_dwa_node",
            output="screen",
            condition=IfCondition(LaunchConfiguration("start_planner")),
            parameters=[{"use_sim_time": True, "r_kerek": wheel_radius, "b": wheel_base,
                         "rob_radius": robot_radius, "map_inflation_radius": robot_radius + 0.03,
                         "static_safety_margin": 0.03, "w_kerek_max": 0.26 / wheel_radius,
                         "dynamic_clearance_weight": float(LaunchConfiguration("dynamic_clearance_weight").perform(context)),
                         "dynamic_clearance_distance": float(LaunchConfiguration("dynamic_clearance_distance").perform(context)),
                         "w_kerek_resolution": float(LaunchConfiguration("wheel_resolution").perform(context)),
                         "a_max": float(drive.findtext("max_linear_acceleration", "1.0"))}],
        ),
        Node(
            package="dwa_gazebo_sim", executable="lidar_obstacle_node", output="screen",
            condition=IfCondition(LaunchConfiguration("start_planner")),
            parameters=[{"use_sim_time": True, "tracking_frame": "odom"}],
        ),
    ]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            "verbose",
            default_value="4",
            description="Gazebo naplózási szintje (0-4)",
        ),
        DeclareLaunchArgument(
            "software_rendering",
            default_value="true",
            description="Szoftveres Mesa renderelés bekapcsolása WSLg renderelési hibákhoz",
        ),
        DeclareLaunchArgument("start_planner", default_value="true",
                      description="Set false for manual SLAM mapping without a cmd_vel controller"),
        DeclareLaunchArgument("dynamic_clearance_weight", default_value="4.0",
                  description="DWA weight for predicted moving-obstacle clearance"),
        DeclareLaunchArgument("dynamic_clearance_distance", default_value="0.6",
              description="Soft predicted clearance target beyond the unchanged safety margin, in metres"),
        DeclareLaunchArgument("wheel_resolution", default_value="0.5",
              description="DWA wheel angular speed sampling interval in rad/s"),
        DeclareLaunchArgument("start_environment", default_value="true",
                      description="Set false to start only the planner against an already running SLAM simulation"),
        DeclareLaunchArgument("enable_crossing_obstacle", default_value="true", choices=["true", "false"],
                      description="Include the crossing obstacle; false keeps only the oncoming obstacle"),
        DeclareLaunchArgument("enable_camera", default_value="false", choices=["true", "false"],
                      description="Enable unused camera rendering in the runtime TurtleBot model"),
        DeclareLaunchArgument("oncoming_start_x", default_value="0.0",
                      description="Start the oncoming obstacle after the robot reaches this odom x in metres"),
        DeclareLaunchArgument("crossing_start_x", default_value="0.8",
                      description="Start the right-side crossing obstacle after the robot reaches this odom x in metres"),
        DeclareLaunchArgument("map_resolution", default_value="0.10",
                      description="SLAM grid cell size in metres"),
        DeclareLaunchArgument("slam_mode", default_value="mapping", choices=["mapping", "localization"],
                      description="Build a map or localize against a saved pose graph"),
        DeclareLaunchArgument("map_file", default_value="",
                      description="Saved SLAM prefix without .posegraph or .data extension"),
        DeclareLaunchArgument("initial_x", default_value="0.8", description="Initial x estimate in map metres"),
        DeclareLaunchArgument("initial_y", default_value="0.8", description="Initial y estimate in map metres"),
        DeclareLaunchArgument("initial_yaw", default_value="0.0", description="Initial map yaw estimate in radians"),
        SetEnvironmentVariable(
            "LIBGL_ALWAYS_SOFTWARE", "1", condition=IfCondition(LaunchConfiguration("software_rendering"))),
        SetEnvironmentVariable("ROS_AUTOMATIC_DISCOVERY_RANGE", "LOCALHOST"),
        OpaqueFunction(function=start_reference),
    ])
````````

### `Projekt/Gazebo_ROS2/src/dwa_gazebo_sim/launch/visualization.launch.py`

````````python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo, SetEnvironmentVariable
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    rviz_config = os.path.join(
        get_package_share_directory("astar_dwa_controller"),
        "rviz",
        "astar_dwa.rviz",
    )
    return LaunchDescription([
        DeclareLaunchArgument("software_rendering", default_value="true",
                              description="Use software OpenGL for WSL map shader compatibility"),
        SetEnvironmentVariable("ROS_AUTOMATIC_DISCOVERY_RANGE", "LOCALHOST"),
        SetEnvironmentVariable("QT_QPA_PLATFORM", "xcb"),
        SetEnvironmentVariable("QT_X11_NO_MITSHM", "1"),
        SetEnvironmentVariable("LIBGL_ALWAYS_SOFTWARE", "1",
                       condition=IfCondition(LaunchConfiguration("software_rendering"))),
        SetEnvironmentVariable("QT_OPENGL", "software",
                       condition=IfCondition(LaunchConfiguration("software_rendering"))),
        LogInfo(msg=["DIAG_RVIZ software_rendering=", LaunchConfiguration("software_rendering"),
                 " fixed_frame=map config=", rviz_config]),
        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            output="screen",
            arguments=["-d", rviz_config, "-f", "map"],
            parameters=[{"use_sim_time": True}],
        )
    ])
````````

### `Projekt/Gazebo_ROS2/src/dwa_gazebo_sim/package.xml`

````````xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>dwa_gazebo_sim</name>
  <version>0.1.0</version>
  <description>Gazebo világ és ROS-Gazebo bridge az A* + DWA vezérlőhöz.</description>
  <maintainer email="rumdaniel@todo.todo">rumdaniel</maintainer>
  <license>MIT</license>

  <depend>rclpy</depend>
  <depend>geometry_msgs</depend>
  <depend>nav_msgs</depend>
  <depend>sensor_msgs</depend>
  <exec_depend>sensor_msgs_py</exec_depend>
  <exec_depend>std_msgs</exec_depend>
  <exec_depend>tf2_ros_py</exec_depend>
  <exec_depend>visualization_msgs</exec_depend>
  <exec_depend>python3-numpy</exec_depend>
  <exec_depend>slam_toolbox</exec_depend>
  <exec_depend>lifecycle_msgs</exec_depend>
  <exec_depend>teleop_twist_keyboard</exec_depend>
  <exec_depend>nav2_map_server</exec_depend>
  <exec_depend>nav2_amcl</exec_depend>
  <exec_depend>nav2_lifecycle_manager</exec_depend>
  <depend>ros_gz_interfaces</depend>
  <depend>ros_gz_bridge</depend>
  <depend>ros_gz_sim</depend>
  <exec_depend>turtlebot3_gazebo</exec_depend>
  <exec_depend>astar_dwa_controller</exec_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
````````

### `Projekt/Gazebo_ROS2/src/dwa_gazebo_sim/resource/dwa_gazebo_sim`

````````text

````````

### `Projekt/Gazebo_ROS2/src/dwa_gazebo_sim/setup.cfg`

````````ini
[develop]
script_dir=$base/lib/dwa_gazebo_sim
[install]
install_scripts=$base/lib/dwa_gazebo_sim
````````

### `Projekt/Gazebo_ROS2/src/dwa_gazebo_sim/setup.py`

````````python
from glob import glob
import os
from setuptools import find_packages, setup

package_name = "dwa_gazebo_sim"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "launch"), [
            "launch/simulation.launch.py",
            "launch/visualization.launch.py",
        ]),
        (os.path.join("share", package_name, "config"), ["config/slam.yaml"]),
        (os.path.join("share", package_name, "worlds"), glob("worlds/*.sdf")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    entry_points={
        "console_scripts": [
            "python_simulation_node = dwa_gazebo_sim.python_simulation_node:main",
            "lidar_obstacle_node = dwa_gazebo_sim.lidar_obstacle_node:main",
        ],
    },
)
````````

### `Projekt/Gazebo_ROS2/src/dwa_gazebo_sim/worlds/dwa_world.sdf`

````````xml
<sdf version="1.8">
  <world name="dwa_world">
    <physics name="default_physics" type="ignored">
      <max_step_size>0.001</max_step_size>
      <real_time_update_rate>1000</real_time_update_rate>
      <real_time_factor>1</real_time_factor>
    </physics>
    <plugin filename="gz-sim-physics-system" name="gz::sim::systems::Physics"/>
    <plugin filename="gz-sim-sensors-system" name="gz::sim::systems::Sensors">
      <render_engine>ogre2</render_engine>
    </plugin>
    <plugin filename="gz-sim-scene-broadcaster-system" name="gz::sim::systems::SceneBroadcaster"/>
    <plugin filename="gz-sim-user-commands-system" name="gz::sim::systems::UserCommands"/>
    <light type="directional" name="sun">
      <pose>0 0 10 0 0 0</pose>
      <direction>-0.5 0.1 -0.9</direction>
    </light>
    <model name="ground_plane">
      <static>true</static>
      <link name="link">
        <collision name="collision"><geometry><plane><normal>0 0 1</normal></plane></geometry></collision>
        <visual name="visual"><geometry><plane><normal>0 0 1</normal></plane></geometry>
          <material><ambient>0.16 0.18 0.22 1</ambient><diffuse>0.22 0.25 0.30 1</diffuse></material>
        </visual>
      </link>
    </model>
    <model name="boundary_bottom">
      <static>true</static><pose>4 -0.10 0.5 0 0 0</pose>
      <link name="link"><collision name="collision"><geometry><box><size>8.2 0.2 1</size></box></geometry></collision>
        <visual name="visual"><geometry><box><size>8.2 0.2 1</size></box></geometry>
          <material><ambient>0.15 0.15 0.18 1</ambient><diffuse>0.15 0.15 0.18 1</diffuse></material>
        </visual></link>
    </model>
    <model name="boundary_top">
      <static>true</static><pose>4 5.10 0.5 0 0 0</pose>
      <link name="link"><collision name="collision"><geometry><box><size>8.2 0.2 1</size></box></geometry></collision>
        <visual name="visual"><geometry><box><size>8.2 0.2 1</size></box></geometry>
          <material><ambient>0.15 0.15 0.18 1</ambient><diffuse>0.15 0.15 0.18 1</diffuse></material>
        </visual></link>
    </model>
    <model name="boundary_left">
      <static>true</static><pose>-0.10 2.5 0.5 0 0 0</pose>
      <link name="link"><collision name="collision"><geometry><box><size>0.2 5.2 1</size></box></geometry></collision>
        <visual name="visual"><geometry><box><size>0.2 5.2 1</size></box></geometry>
          <material><ambient>0.15 0.15 0.18 1</ambient><diffuse>0.15 0.15 0.18 1</diffuse></material>
        </visual></link>
    </model>
    <model name="boundary_right">
      <static>true</static><pose>8.10 2.5 0.5 0 0 0</pose>
      <link name="link"><collision name="collision"><geometry><box><size>0.2 5.2 1</size></box></geometry></collision>
        <visual name="visual"><geometry><box><size>0.2 5.2 1</size></box></geometry>
          <material><ambient>0.15 0.15 0.18 1</ambient><diffuse>0.15 0.15 0.18 1</diffuse></material>
        </visual></link>
    </model>
    <model name="obstacle_1">
      <static>true</static><pose>2.1 0.9 0.5 0 0 0</pose>
      <link name="link"><collision name="collision"><geometry><box><size>0.2 0.8 1</size></box></geometry></collision>
        <visual name="visual"><geometry><box><size>0.2 0.8 1</size></box></geometry>
          <material><ambient>0.8 0.1 0.1 1</ambient><diffuse>0.8 0.1 0.1 1</diffuse></material>
        </visual></link>
    </model>
    <model name="obstacle_2">
      <static>true</static><pose>2.1 3.1 0.5 0 0 0</pose>
      <link name="link"><collision name="collision"><geometry><box><size>0.2 0.8 1</size></box></geometry></collision>
        <visual name="visual"><geometry><box><size>0.2 0.8 1</size></box></geometry>
          <material><ambient>0.9 0.4 0.05 1</ambient><diffuse>0.9 0.4 0.05 1</diffuse></material>
        </visual></link>
    </model>
    <model name="obstacle_3">
      <static>true</static><pose>3.2 2.5 0.5 0 0 0</pose>
      <link name="link"><collision name="collision"><geometry><box><size>1.6 0.2 1</size></box></geometry></collision>
        <visual name="visual"><geometry><box><size>1.6 0.2 1</size></box></geometry>
          <material><ambient>0.55 0.1 0.75 1</ambient><diffuse>0.55 0.1 0.75 1</diffuse></material>
        </visual></link>
    </model>
    <model name="obstacle_4">
      <static>true</static><pose>6.7 2.5 0.5 0 0 0</pose>
      <link name="link"><collision name="collision"><geometry><box><size>2.6 0.2 1</size></box></geometry></collision>
        <visual name="visual"><geometry><box><size>2.6 0.2 1</size></box></geometry>
          <material><ambient>0.95 0.75 0.05 1</ambient><diffuse>0.95 0.75 0.05 1</diffuse></material>
        </visual></link>
    </model>
    <model name="moving_obstacle_1">
      <static>false</static>
      <pose>2.4 0.4 0.45 0 0 0</pose>
      <plugin filename="gz-sim-velocity-control-system" name="gz::sim::systems::VelocityControl">
        <topic>/model/moving_obstacle_1/cmd_vel</topic>
      </plugin>
      <link name="link">
        <collision name="collision">
          <geometry><cylinder><radius>0.18</radius><length>0.9</length></cylinder></geometry>
        </collision>
        <visual name="visual">
          <geometry><cylinder><radius>0.18</radius><length>0.9</length></cylinder></geometry>
          <material><ambient>0.1 0.4 0.9 1</ambient><diffuse>0.1 0.4 0.9 1</diffuse></material>
        </visual>
      </link>
    </model>
    <model name="moving_obstacle_2">
      <static>false</static>
      <pose>6.8 2.0 0.45 0 0 0</pose>
      <plugin filename="gz-sim-velocity-control-system" name="gz::sim::systems::VelocityControl">
        <topic>/model/moving_obstacle_2/cmd_vel</topic>
      </plugin>
      <link name="link">
        <collision name="collision">
          <geometry><cylinder><radius>0.18</radius><length>0.9</length></cylinder></geometry>
        </collision>
        <visual name="visual">
          <geometry><cylinder><radius>0.18</radius><length>0.9</length></cylinder></geometry>
          <material><ambient>0.1 0.8 0.4 1</ambient><diffuse>0.1 0.8 0.4 1</diffuse></material>
        </visual>
      </link>
    </model>
    <include>
      <uri>model://turtlebot3_waffle</uri>
      <name>turtlebot3_waffle</name>
      <pose>0.8 0.8 0.05 0 0 0</pose>
    </include>
  </world>
</sdf>
````````

### `Projekt/Python_szimulacio/codes_diploma/astar_project/__init__.py`

````````python

````````

### `Projekt/Python_szimulacio/codes_diploma/astar_project/astar_baseline.py`

````````python
"""Klasszikus A* útvonaltervezés rácstérképen."""

import math


def _heuristic(position, goal, diagonal, heuristic=None):
	"""Heurisztikus becslést ad a pozíció és a cél között."""
	if heuristic is not None:
		return heuristic(position, goal)

	row, column = position
	goal_row, goal_column = goal
	row_distance = abs(goal_row - row)
	column_distance = abs(goal_column - column)

	if diagonal:
		return math.sqrt(row_distance ** 2 + column_distance ** 2)

	return row_distance + column_distance


def _movement_cost(current, neighbor):
	"""Megadja két szomszédos cella mozgási költségét."""
	row_change = abs(neighbor[0] - current[0])
	column_change = abs(neighbor[1] - current[1])
	return math.sqrt(row_change ** 2 + column_change ** 2)


def _reconstruct_path(came_from, current):
	"""A célcellától visszalépve összeállítja a startig vezető utat."""
	path_from_goal = [current]

	while current in came_from:
		previous_position = came_from[current]
		path_from_goal.append(previous_position)
		current = previous_position

	path_from_goal.reverse()
	return path_from_goal


def astar_search(
	grid_map,
	start,
	goal,
	diagonal=False,
	return_details=False,
	heuristic=None,
):
	"""Megkeresi a legkisebb költségű utat a start és a cél között."""
 
	if not grid_map.is_inside(*start) or not grid_map.is_inside(*goal):
		raise ValueError("A start és a cél a térképen belül legyen.")
	if not grid_map.is_free(*start) or not grid_map.is_free(*goal):
		raise ValueError("A start és a cél szabad cella legyen.")

	open_list = [(_heuristic(start, goal, diagonal, heuristic), 0.0, start)]	#heurisztika értéke, g költség, pozíció

	came_from = {}	#lista a szülő pozíciókhoz
	g_costs = {start: 0.0}	#az egyes pozíciókhoz tartozó g költségek
	expanded_nodes = []	#csomópontokhoz tartozó lista, a hozzáférhető csomopontokhoz
	search_steps = []	#a lépéseket tarolja a kereses folyaman

	while open_list:	#amig van open státuszban csomópont addig csinálja
		best_node = min(open_list)	#legjobb node kiválasztása f költség alapján
		open_list.remove(best_node)	#kiveszi a legjobb nodeot
		current_g_cost = best_node[1]	#g költség a legjobb nodehoz
		current_position = best_node[2]	#pozíció a legjobb nodehoz

		if current_g_cost > g_costs[current_position]:	#ha a g költség nagyobb mint a tárolt g költség akkor nem kell tovább vizsgálni
			continue

		expanded_nodes.append(current_position)	# már feldolgozott csomópontokhoz hozzáadja a jelenlegi pozíciót

		if current_position == goal:
			path = _reconstruct_path(came_from, current_position)
			if return_details:
				return {
					"path": path,
					"expanded_nodes": expanded_nodes,
					"search_steps": search_steps,
				}
			return path

		neighbors = grid_map.get_neighbors(current_position[0], current_position[1], diagonal)	 #szomszédos cellák lekérése a grid_mapből, ahol [0] a sor, [1] az oszlop
		neighbor_scores = []	#a szomszédos cellákhoz tartozó f, g, h költségek
		for neighbor in neighbors:	#a szomszédos cellákhoz tartozó f, g, h költségek kiszámítása
			movement_cost = _movement_cost(current_position, neighbor)	#mozgás költsége a jelenlegi és a szomszédos pozíció között
			new_g_cost = current_g_cost + movement_cost	#g költség a szomszédokhoz
			h_cost = _heuristic(neighbor, goal, diagonal, heuristic)	#h költség a szomszédokhoz
			f_cost = new_g_cost + h_cost	#f költség a szomszédokhoz
			accepted = new_g_cost < g_costs.get(neighbor, math.inf)	#ha a szomszédos cella g költsége kisebb mint a tárolt g költség akkor elfogadja a szomszédos cellát

			if return_details:
				neighbor_scores.append(	
					{
						"position": neighbor,
						"g": new_g_cost,
						"h": h_cost,
						"f": new_g_cost + h_cost,
						"accepted": accepted,
					}
				)

			if not accepted:
				continue

			came_from[neighbor] = current_position	#a szomszédos cella szülő pozíciója a jelenlegi pozíció
			g_costs[neighbor] = new_g_cost	#szomszédos cella g költsége a jelenlegi g költség + mozgás költség
			f_cost = new_g_cost + h_cost	#szomszédos cella f költsége a jelenlegi g költség + h költség
			open_list.append((f_cost, new_g_cost, neighbor))	#szomszédos cella hozzáadása az open listához a f költség, g költség és pozíció alapján

		if not return_details:
			continue

		
		current_h_cost = _heuristic(current_position, goal, diagonal, heuristic)	# a jelenlegi pozíció h költsége
		search_steps.append(	#hozzáadja a keresési lépésekhez a jelenlegi pozíciót, szomszédos cellákat, g költséget, h költséget, f költséget és szomszédos cellákhoz tartozó f, g, h költségeket
			{
				"current": current_position,
				"neighbors": neighbors,
				"current_g": current_g_cost,
				"current_h": current_h_cost,
				"current_f": current_g_cost + current_h_cost,
				"neighbor_scores": neighbor_scores,
			}
		)

		valid_open_nodes = []
		for entry in open_list:
			stored_g_cost = entry[1]
			position = entry[2]
			best_known_g_cost = g_costs.get(position, math.inf)

			if stored_g_cost <= best_known_g_cost:
				valid_open_nodes.append(entry)

		# Az érvényes tuple-ökből olvasható szótárakat készítünk a megjelenítéshez.
		priority_queue = [
			{
				"position": position,  # A várakozó node cellakoordinátája.
				"g": cost,  # A starttól eddig vezető út költsége.
				"h": priority - cost,  # A cellától a célig becsült költség: h = f - g.
				"f": priority,  # A teljes becsült költség: f = g + h.
			}
			# A sorted tuple-jeiből rendre az f, g és pozíció értékeket vesszük ki.
			for priority, cost, position in sorted(valid_open_nodes)
		]
		search_steps[-1]["priority_queue"] = priority_queue  # A -1 az utolsó keresési lépést jelenti.
		search_steps[-1]["next_position"] = (min(valid_open_nodes)[2] if valid_open_nodes else None)  # A legkisebb f-költségű következő pozíció, vagy None.

	if return_details:
		return {
			"path": None,
			"expanded_nodes": expanded_nodes,
			"search_steps": search_steps,
		}

	return None


# A priority_queue blokk működése részletesen:
#
# 1. A valid_open_nodes elemei tuple-ök:
#
#        (f_költség, g_költség, pozíció)
#
#    Például:
#
#        [
#            (7.0, 3.0, (2, 4)),
#            (6.0, 4.0, (1, 5)),
#        ]
#
# 2. A sorted(valid_open_nodes) rendezi ezeket a tuple-öket. Elsőként az
#    f-költséget hasonlítja össze, ezért a kisebb f-költségű node kerül előre.
#    Ebben a példában a (6.0, 4.0, (1, 5)) node lesz az első.
#
# 3. A list comprehension minden tuple-ből egy szótárat készít. Ez azért
#    hasznos, mert a szótár kulcsai alapján később könnyebb megjeleníteni és
#    értelmezni az adatokat:
#
#        {
#            "position": (1, 5),
#            "g": 4.0,
#            "h": 2.0,
#            "f": 6.0,
#        }
#
#    A for ciklus változói a tuple elemeit jelentik:
#    - priority: az entry[0], vagyis az f-költség;
#    - cost: az entry[1], vagyis a g-költség;
#    - position: az entry[2], vagyis a cella pozíciója.
#
# 4. A h-költséget a kód nem tárolta külön a valid_open_nodes tuple-ben.
#    Mivel f = g + h, ezért vissza lehet számolni:
#
#        h = f - g
#        h = priority - cost
#
#    A példában:
#
#        h = 6.0 - 4.0 = 2.0
#
# 5. A search_steps[-1] az utolsóként létrehozott keresési lépés szótára.
#    A priority_queue kulcs alá bekerül az aktuális körben még várakozó node-ok
#    listája, így ezt a szimuláció később meg tudja jeleníteni.
#
# 6. A next_position meghatározása:
#
#        min(valid_open_nodes)[2]
#
#    A min kiválasztja a legkisebb tuple-t, tehát elsősorban a legkisebb
#    f-költségű node-ot. A [2] ezután csak a pozíciót veszi ki belőle.
#    Ha nincs érvényes várakozó node, akkor a feltételes kifejezés None értéket
#    ad vissza:
#
#        next_position = (1, 5)
#        vagy
#        next_position = None
#
# 7. A return_details kapcsoló dönti el, hogy ezek a részletes adatok
#    visszakerülnek-e a hívó kódhoz. Ha True, az eredmény egy szótár:
#
#        {
#            "path": ...,             # megtalált út vagy None
#            "expanded_nodes": ...,   # már feldolgozott cellák
#            "search_steps": ...,     # a keresés minden részletes lépése
#        }
#
#    Ha return_details False, a függvény csak az útvonalat vagy sikertelen
#    keresés esetén None értéket ad vissza, a részletes megjelenítési adatokra
#    nincs szükség.


# ---------------------------------------------------------------------------
# ADATSTRUKTÚRAI ÁTTEKINTÉS AZ A* ALGORITMUSHOZ
# ---------------------------------------------------------------------------
# Ebben a megvalósításban a "node" nem külön osztály vagy objektum, hanem
# egy tuple, amely három adatot tartalmaz:
#
#     (f_költség, g_költség, pozíció)
#
# Példa egy node-ra:
#
#     (7.0, 3.0, (2, 4))
#
# A tuple elemei:
# - entry[0] = f-költség = g-költség + h-költség.
#   Ezt használja az A* annak eldöntésére, melyik node legyen a következő.
# - entry[1] = g-költség, vagyis a startcellától az adott celláig megtett út
#   eddigi költsége.
# - entry[2] = position, vagyis a cella (sor, oszlop) koordinátája.
#
# A példában:
# - f = 7.0;
# - g = 3.0;
# - h = f - g = 7.0 - 3.0 = 4.0;
# - position = (2, 4), tehát a cella a 2. sorban és a 4. oszlopban van.
#
# A fontosabb A* adatszerkezetek felépítése:
#
# 1. open_list
#    Azokat a node-okat tartalmazza, amelyeket az algoritmus még nem dolgozott
#    fel teljesen. Egy lista például így nézhet ki:
#
#        [
#            (7.0, 3.0, (2, 4)),
#            (6.5, 4.5, (1, 5)),
#        ]
#
#    Az első elem az f-költség, a második a g-költség, a harmadik a pozíció.
#    A min(open_list) a legkisebb tuple-t választja ki, ezért elsősorban az
#    f-költség alapján keresünk, egyezés esetén pedig a további tuple-elemek
#    alapján dönt a Python.
#
# 2. g_costs
#    Egy szótár, amely minden már felfedezett cellához eltárolja az eddig
#    ismert legjobb g-költséget:
#
#        {
#            (2, 4): 3.0,
#            (1, 5): 4.5,
#        }
#
#    A (2, 4): 3.0 azt jelenti, hogy a startcellától a (2, 4) celláig jelenleg
#    ismert legolcsóbb út költsége 3.0.
#
# 3. came_from
#    A cellák szülőcelláját tárolja. Ez kell ahhoz, hogy a cél elérésekor az
#    algoritmus vissza tudja építeni az útvonalat:
#
#        {
#            (2, 4): (2, 3),
#            (2, 3): (1, 3),
#        }
#
#    Ez azt jelenti, hogy a (2, 4) cellába a (2, 3) cellából érkeztünk.
#
# 4. valid_open_nodes
#    Az open_list megtisztított változata. Ugyanaz a cella több alkalommal is
#    bekerülhet az open_list-be, ha később olcsóbb úton találjuk meg. A régi,
#    drágább node ilyenkor elavult. A szűrés csak azt tartja meg, amelynek a
#    g-költsége még megfelel a g_costs szótárban tárolt legjobb értéknek.
#
#    Példa:
#
#        open_list: [(8.0, 5.0, (2, 4)), (7.0, 3.0, (2, 4))]
#        g_costs:   {(2, 4): 3.0}
#
#    A g = 5.0 értékű régi node kiesik, a g = 3.0 értékű aktuális node marad.
#
# 5. priority_queue
#    A valid_open_nodes elemeit könnyebben olvasható szótárakká alakítja:
#
#        {
#            "position": (2, 4),
#            "g": 3.0,
#            "h": 4.0,
#            "f": 7.0,
#        }
#
#    Itt a h-költség külön is megjelenik, amely az open_list tuple-jában nem
#    szerepel közvetlenül, mert kiszámítható az f - g képlettel.
#
# 6. search_steps
#    A search_steps egy lista, amely a keresés közben létrejövő lépéseket
#    tárolja. Egy listaelem egy olyan szótár, amely egyetlen feldolgozott
#    aktuális cella teljes állapotát írja le.
#
#    Egy search_steps elem felépítése:
#
#        {
#            "current": (2, 3),
#            "neighbors": [(1, 3), (2, 4)],
#            "current_g": 2.0,
#            "current_h": 4.0,
#            "current_f": 6.0,
#            "neighbor_scores": [
#                {
#                    "position": (1, 3),
#                    "g": 3.0,
#                    "h": 3.0,
#                    "f": 6.0,
#                    "accepted": True,
#                }
#            ],
#            "priority_queue": [
#                {
#                    "position": (1, 3),
#                    "g": 3.0,
#                    "h": 3.0,
#                    "f": 6.0,
#                }
#            ],
#            "next_position": (1, 3),
#        }
#
#    A mezők jelentése:
#    - current: az a cella, amelyet az A* algoritmus ebben a körben feldolgoz.
#    - neighbors: a current cella szabad és elérhető szomszédai.
#    - current_g: a startcellától a current celláig ismert út költsége.
#    - current_h: a current cellától a célig becsült költség.
#    - current_f: current_g + current_h; ezt használja az A* a rangsoroláshoz.
#    - neighbor_scores: minden szomszédhoz kiszámított g, h és f értékek listája.
#    - accepted: True, ha a szomszédhoz talált új út olcsóbb a korábbinál,
#      ezért a szomszéd bekerülhet az open_list-be.
#    - priority_queue: az adott kör után érvényes, még feldolgozásra váró
#      node-ok könnyebben olvasható formában.
#    - next_position: az a következő cella, amelyet az A* a legkisebb f alapján
#      várhatóan kiválaszt. Ha nincs több node, az értéke None.
#
#    A search_steps lista így épül fel:
#
#        search_steps = [
#            első keresési lépés szótára,
#            második keresési lépés szótára,
#            harmadik keresési lépés szótára,
#            ...,
#        ]
#
#    A ciklus minden feldolgozott current cella után létrehoz egy új szótárat,
#    majd a priority_queue és a next_position adatait ugyanebbe a szótárba
#    írja bele. Ezután a szótár bekerül a search_steps lista végére.
#
#    Például:
#
#        search_steps[0]
#
#    a keresés első feldolgozási körének adatait jelenti, míg a
#
#        search_steps[1]
#
#    a második kör adatait. A szimuláció ezt használja arra, hogy a keresést
#    lépésenként, animációs képkockák formájában meg tudja jeleníteni.
#
# Az adatok működési sorrendje röviden:
#
#     szomszédos cella
#       -> g, h és f költség kiszámítása
#       -> (f, g, position) hozzáadása az open_list-hez
#       -> jobb út esetén g_costs frissítése
#       -> elavult node-ok kiszűrése valid_open_nodes segítségével
#       -> priority_queue létrehozása az áttekinthető megjelenítéshez


# ---------------------------------------------------------------------------
# A valid_open_nodes szűrésének részletes magyarázata
# ---------------------------------------------------------------------------
#
# A programban az open_list elemei három adatot tartalmazó tuple-ök:
#
#     (f_költség, g_költség, pozíció)
#
# Például:
#
#     (8.0, 5.0, (2, 4))
#
# Ez azt jelenti, hogy a (2, 4) cellához a startcellától eddig ismert út
# költsége 5.0. Az f-költség 8.0, amely a g- és h-költség összege:
#
#     f = g + h
#
# A kód az open_list minden elemét egyenként megvizsgálja:
#
#     valid_open_nodes = []
#     for entry in open_list:
#         stored_g_cost = entry[1]
#         position = entry[2]
#         best_known_g_cost = g_costs.get(position, math.inf)
#
#         if stored_g_cost <= best_known_g_cost:
#             valid_open_nodes.append(entry)
#
# Az entry az open_list egyik tuple-je. Az entry[1] az ebben a tuple-ben
# tárolt g-költség, az entry[2] pedig a cella pozíciója.
#
# A g_costs szótár minden már felfedezett cellához eltárolja a jelenleg
# ismert legjobb g-költséget. Például:
#
#     g_costs = {
#         (2, 4): 3.0
#     }
#
# Ez azt jelenti, hogy a (2, 4) cellához jelenleg ismert legolcsóbb út költsége
# 3.0.
#
# Ugyanaz a cella többször is bekerülhet az open_list-be. Ez akkor történik,
# ha az A* először egy drágább, majd később egy olcsóbb útvonalat talál hozzá.
# Például:
#
#     open_list = [
#         (8.0, 5.0, (2, 4)),
#         (6.0, 3.0, (2, 4)),
#     ]
#
#     g_costs = {
#         (2, 4): 3.0
#     }
#
# Az első bejegyzés elavult, mert a benne lévő g-költség 5.0, miközben már
# ismert egy 3.0 költségű út ugyanahhoz a cellához:
#
#     5.0 <= 3.0  -> False
#
# Ezért ez az elem nem kerül bele a valid_open_nodes listába.
#
# A második bejegyzés érvényes, mert az általa tárolt g-költség megegyezik
# a jelenleg ismert legjobb értékkel:
#
#     3.0 <= 3.0  -> True
#
# Ezért bekerül a valid_open_nodes listába.
#
# A valid_open_nodes tehát az open_list megtisztított változata: csak azok a
# bejegyzések maradnak benne, amelyek még a cellához ismert legjobb útvonalat
# képviselik. Az eredeti open_list ettől nem változik, a program csak egy új
# listát készít a még érvényes elemekből.
#
# Ez a szűrt lista a priority_queue létrehozásához és a megjelenítéshez kell.
# A priority_queue már olvasható szótárakká alakítja ezeket az elemeket, és
# külön megjeleníti a cella pozícióját, valamint a g, h és f költségeket.


# ---------------------------------------------------------------------------
# 				Az A* teljes működésének rövid, végigkövetett példája
# ---------------------------------------------------------------------------
#
# Példa:
#
#     rácsméret: 3 oszlop x 2 sor
#     start:     (0, 0)
#     cél:       (1, 2)
#     akadály:   nincs
#     diagonal:  False
#
# A cellákat (sor, oszlop) formában jelöljük. Átlós mozgás nélkül egy lépés
# költsége 1. A Manhattan-heurisztika képlete:
#
#     h = abs(cél_sor - sor) + abs(cél_oszlop - oszlop)
#
# 1. Kezdőállapot
#
# Az algoritmus létrehozza az üres adatszerkezeteket, majd a startcellát
# beteszi az open_list-be:
#
#     open_list = [(3.0, 0.0, (0, 0))]
#     g_costs = {(0, 0): 0.0}
#     came_from = {}
#     expanded_nodes = []
#     search_steps = []
#
# A startcellánál g = 0.0, a célig becsült h = 3.0, ezért f = g + h = 3.0.
#
# 2. A startcellát kiválasztjuk, majd kivesszük az open_list-ből
#
# Induláskor az open_list-ben még csak a startcellához tartozó node van:
#
#     open_list = [(3.0, 0.0, (0, 0))]
#
# Ez a node nem a semmiből került a listába: az algoritmus a keresés elején
# készíti el a startcellából. A tuple elemei rendre az f-költség, a g-költség
# és a pozíció. A startnál g = 0.0, mert még nem tettünk meg lépést.
#
# A min(open_list) kiválasztja a legkisebb f-költségű node-ot. Ezt a node-ot
# a program eltávolítja az open_list-ből, majd current_position néven kezdi
# feldolgozni:
#
#     best_node = (3.0, 0.0, (0, 0))
#     open_list = []
#     current_position = (0, 0)
#
# Ezután a startcellát feldolgozott cellaként eltároljuk:
#
#     expanded_nodes = [(0, 0)]
#
# 3. A start szomszédainak felderítése és az open_list feltöltése
#
# A program ezután lekéri a current_position, vagyis (0, 0) szabad szomszédait:
#
#     (1, 0) és (0, 1)
#
# Ezek még nem voltak benne az open_list-ben. A for ciklus mindkét szomszédra
# kiszámítja a mozgási költséget, az új g-költséget, a h-költséget és az
# f-költséget. Mindkét cellához 1.0 költséggel jutunk el, majd a program
# eltárolja a szülőt és a legjobb ismert g-költséget:
#
#     came_from = {
#         (1, 0): (0, 0),
#         (0, 1): (0, 0),
#     }
#
#     g_costs = {
#         (0, 0): 0.0,
#         (1, 0): 1.0,
#         (0, 1): 1.0,
#     }
#
# Ezután az új node-ok bekerülnek az open_list-be az open_list.append(...) sorral.
# Mindkettő f-költsége 3.0:
#
#     open_list = [
#         (3.0, 1.0, (1, 0)),
#         (3.0, 1.0, (0, 1)),
#     ]
#
# Ezután létrejön a search_steps első eleme. Ez csak akkor történik meg, ha a
# return_details értéke True. A program egy szótárban elmenti az imént lezajlott
# feldolgozási kört:
#
#     search_steps[0] = {
#         "current": (0, 0),
#         "neighbors": [(1, 0), (0, 1)],
#         "current_g": 0.0,
#         "current_h": 3.0,
#         "current_f": 3.0,
#         "neighbor_scores": [...],
#     }
#
# A current azt mutatja, melyik cellát dolgoztuk fel. A neighbors az elérhető
# szomszédokat tartalmazza. A current_g, current_h és current_f az aktuális
# cella költségei. A neighbor_scores külön leírja, hogy a program mit számolt
# ki mindkét szomszédra, és elfogadta-e őket.
#
# Ezután a program a már frissített open_list-ből létrehozza a valid_open_nodes
# listát, majd a priority_queue-t. Ez nem egy új keresési lista, hanem az
# open_list megjelenítéshez átalakított változata:
#
#     priority_queue = [
#         {"position": (1, 0), "g": 1.0, "h": 2.0, "f": 3.0},
#         {"position": (0, 1), "g": 1.0, "h": 2.0, "f": 3.0},
#     ]
#
# A priority_queue azokat a node-okat mutatja, amelyek már bekerültek az
# open_list-be, de még nem kerültek feldolgozásra. Az f-költség szerint vannak
# rendezve, ezért ebből látható, hogy a következő körben melyik node lehet a
# következő kiválasztott elem. A priority_queue és a next_position adatait a
# program ugyanabba a search_steps[0] szótárba írja bele.
#
# 4. A következő cella kiválasztása és feldolgozása
#
# Az előző lépés végén az open_list két node-ot tartalmazott. Mindkét node
# f = 3.0 és g = 1.0 értékű volt. A min(open_list) kiválasztja közülük a
# következő node-ot. Azonos f és g esetén a tuple további elemei alapján
# történik a rendezés, ezért a példában a (0, 1) cella kerül sorra:
#
#     best_node = (3.0, 1.0, (0, 1))
#     open_list = [(3.0, 1.0, (1, 0))]
#
# A (0, 1) cella ekkor kikerül a várakozó listából, és bekerül az
# expanded_nodes listába:
#
#     expanded_nodes = [(0, 0), (0, 1)]
#
# Ezután a program lekéri a (0, 1) szabad szomszédait. Ezek a térkép és a
# get_neighbors irány-sorrendje alapján:
#
#     (1, 1), (0, 2), (0, 0)
#
# A for ciklus ezeket egymás után vizsgálja. A (1, 1) és a (0, 2) cellát most
# találja meg először, ezért a g_costs még nem tartalmaz hozzájuk értéket. Az
# új út mindkét cellához olcsóbbnak számít a kezdeti végtelen értéknél, ezért
# accepted = True lesz, és mindkét node bekerül az open_list-be.
#
# A (0, 0) cellát viszont már korábban feldolgoztuk. A jelenlegi cellából oda
# vezető új út költsége 2.0 lenne, de a g_costs szerint a startcellához már
# 0.0 költséggel eljutottunk. Ezért az új út nem jobb:
#
#     (0, 0): új g = 2.0, régi g = 0.0 -> accepted = False
#
# Emiatt a (0, 0) node-hoz nem frissül a came_from vagy a g_costs, és nem kerül
# újra az open_list-be. A két elfogadott szomszéd viszont bekerül az adatokba:
#
#     came_from[(1, 1)] = (0, 1)
#     came_from[(0, 2)] = (0, 1)
#     g_costs[(1, 1)] = 2.0
#     g_costs[(0, 2)] = 2.0
#
# A két új node bekerül az open_list-be. A feldolgozás állapota bekerül a
# search_steps második elemébe.
#
# 5. Olyan node feldolgozása, amely nem lesz a végső út része
#
# A következő kiválasztott cella (1, 0). Ez is bekerül az expanded_nodes listába:
#
#     expanded_nodes = [(0, 0), (0, 1), (1, 0)]
#
# Innen a (1, 1) cellához vezető új út költsége szintén 2.0 lenne. Mivel a
# g_costs már tartalmazza a (1, 1): 2.0 értéket, az új jelölt nem jobb:
#
#     új g = 2.0, ismert g = 2.0 -> accepted = False
#
# Ez a lépés bekerül a search_steps listába, de (1, 0) végül nem kerül bele
# a path listába. Ez mutatja a különbséget a keresés közben feldolgozott és a
# végső útvonalhoz tartozó cellák között.
#
# 6. A cél elérhetővé válik az open_list-ben
#
# A (0, 2) cella feldolgozásakor a cél (1, 2) szomszédként megjelenik:
#
#     új g = 3.0
#     h = 0.0
#     f = 3.0
#
# Mivel a célhoz eddig nem tartozott g_costs érték, a program elfogadja:
#
#     came_from[(1, 2)] = (0, 2)
#     g_costs[(1, 2)] = 3.0
#
# A cél bekerül az open_list-be, de ekkor még nincs benne az expanded_nodes-ban.
# Először várakozó node, és csak akkor lesz expanded node, amikor kivesszük.
#
# 7. A priority_queue és a valid_open_nodes szerepe
#
# A program az open_list-ből létrehozza a valid_open_nodes listát. Ez kiszűri
# azokat a régi bejegyzéseket, amelyekhez időközben olcsóbb útvonalat találtunk.
# A priority_queue ezt követően megjelenítéshez használható szótárakat készít:
#
#     {
#         "position": (1, 2),
#         "g": 3.0,
#         "h": 0.0,
#         "f": 3.0,
#     }
#
# Ez az adat bekerül az aktuális search_steps elembe. Így a search_steps nemcsak
# azt tárolja, hogy melyik cellát dolgoztuk fel, hanem az adott kör végén azt is,
# hogy mely node-ok várakoznak még, és melyik lesz várhatóan a következő.
#
# 8. A cél feldolgozása és a végső eredmény
#
# A cél kiválasztásakor először bekerül az expanded_nodes listába:
#
#     expanded_nodes = [
#         (0, 0), (0, 1), (1, 0), (0, 2), (1, 1), (1, 2)
#     ]
#
# Ezután a program észreveszi, hogy current_position == goal, ezért nem keres
# további szomszédokat. A came_from szótárból visszafelé felépíti az útvonalat:
#
#     (1, 2) <- (0, 2) <- (0, 1) <- (0, 0)
#
# A visszafelé kapott sorrendet megfordítja, ezért a végső path:
#
#     path = [(0, 0), (0, 1), (0, 2), (1, 2)]
#
# A visszaadott részletes eredmény szerkezete:
#
#     {
#         "path": path,
#         "expanded_nodes": expanded_nodes,
#         "search_steps": search_steps,
#     }
#
# Rövid adatáramlás:
#
#     szomszéd
#       -> g, h, f kiszámítása
#       -> jobb út esetén came_from és g_costs frissítése
#       -> node hozzáadása az open_list-hez
#       -> régi node-ok kiszűrése valid_open_nodes segítségével
#       -> állapot mentése a search_steps-ben
#       -> legjobb node kiválasztása
#       -> cél esetén path felépítése a came_from alapján
````````

### `Projekt/Python_szimulacio/codes_diploma/astar_project/astar_variants.py`

````````python
"""Egyszerűen cserélhető heurisztikák az A* összehasonlításához."""

import math


def manhattan(position, goal):
	"""Távolság csak vízszintes és függőleges mozgáshoz."""
	return abs(position[0] - goal[0]) + abs(position[1] - goal[1])


def euclidean(position, goal):
	"""Légvonalbeli távolság."""
	row_distance = abs(position[0] - goal[0])
	column_distance = abs(position[1] - goal[1])
	return math.sqrt(row_distance ** 2 + column_distance ** 2)


def chebyshev(position, goal):
	"""A két koordinátakülönbség közül a nagyobb."""
	return max(abs(position[0] - goal[0]), abs(position[1] - goal[1]))


def octile(position, goal):
	"""Jó becslés egyenes és sqrt(2) költségű átlós mozgáshoz."""
	row_distance = abs(position[0] - goal[0])
	column_distance = abs(position[1] - goal[1])
	straight = max(row_distance, column_distance)
	diagonal = min(row_distance, column_distance)
	return straight + (math.sqrt(2) - 1) * diagonal


HEURISTICS = {
	"manhattan": manhattan,
	"euclidean": euclidean,
	"chebyshev": chebyshev,
	"octile": octile,
}


def get_heuristic(name):
	"""Visszaadja a névhez tartozó heurisztikát."""
	try:
		return HEURISTICS[name]
	except KeyError as error:
		raise ValueError(f"Ismeretlen heurisztika: {name}") from error
````````

### `Projekt/Python_szimulacio/codes_diploma/astar_project/grid_map.py`

````````python
"""Egyszeru racsterkep az A* algoritmushoz."""

import math


class GridMap:
    """Negyzetes cellakbol allo, ketdimenzios terkep."""

    def __init__(
        self,
        width,
        height,
        resolution=0.1,
        origin_x=0.0,
        origin_y=0.0,
        unknown=False,
    ):
        if width <= 0 or height <= 0:
            raise ValueError("A terkep merete legyen pozitiv.")
        if resolution <= 0:
            raise ValueError("A felbontas legyen pozitiv.")

        self.width = width
        self.height = height
        self.resolution = resolution
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.grid = []

        initial_value = 2 if unknown else 0
        for _ in range(height):
            self.grid.append([initial_value] * width)

    def is_inside(self, row, column):
        """Megadja, hogy a cella a terkepen belul van-e."""
        return 0 <= row < self.height and 0 <= column < self.width

    def is_free(self, row, column):
        """Megadja, hogy a cella szabad-e."""
        return self.is_inside(row, column) and self.grid[row][column] == 0

    def world_to_grid(self, x, y):
        """Vilagkoordinatat (meterben) racskoordinatava alakit."""
        column = math.floor((x - self.origin_x) / self.resolution)
        row = math.floor((y - self.origin_y) / self.resolution)
        return row, column

    def grid_to_world(self, row, column):
        """A cella kozepontjat visszaadja vilagkoordinataban."""
        x = self.origin_x + (column + 0.5) * self.resolution
        y = self.origin_y + (row + 0.5) * self.resolution
        return x, y

    def add_obstacle(self, row, column):
        """Akadalykent megjelol egy cellat."""
        if not self.is_inside(row, column):
            raise ValueError("Az akadaly a terkepen kivul van.")
        self.grid[row][column] = 1

    def remove_obstacle(self, row, column):
        """Szabad cellava tesz egy cellat."""
        if not self.is_inside(row, column):
            raise ValueError("A cella a terkepen kivul van.")
        self.grid[row][column] = 0

    def mark_free(self, row, column):
        """A robot altal megvizsgalt cellat szabadnak jelol."""
        if not self.is_inside(row, column):
            raise ValueError("A cella a terkepen kivul van.")
        self.grid[row][column] = 0

    def add_obstacle_world(self, x, y, radius=0.0):
        """Vilagkoordinatas akadalyat egy vagy tobb cellaba ir."""
        center_row, center_column = self.world_to_grid(x, y)
        cell_radius = int(radius / self.resolution) + 1

        for row in range(center_row - cell_radius, center_row + cell_radius + 1):
            for column in range(
                center_column - cell_radius,
                center_column + cell_radius + 1,
            ):
                if not self.is_inside(row, column):
                    continue
                cell_x, cell_y = self.grid_to_world(row, column)
                distance = ((cell_x - x) ** 2 + (cell_y - y) ** 2) ** 0.5
                if distance <= radius + self.resolution:
                    self.add_obstacle(row, column)

    def update_from_obstacles(self, obstacles):
        """Szimulacios akadalyobjektumokbol frissiti a terkepet.

        Az objektumoknak ``x``, ``y`` es opcionisan ``radius`` attributummal
        kell rendelkezniuk, ahogy a DWA Obstacle osztályának.
        """
        for obstacle in obstacles:
            radius = getattr(obstacle, "radius", 0.0)
            self.add_obstacle_world(obstacle.x, obstacle.y, radius)

    def inflate_obstacles(self, radius):
        """Biztonsagi tavolsaggal kitagitja az akadalycellakat."""
        if radius < 0:
            raise ValueError("A biztonsagi sugar nem lehet negativ.")
        if radius == 0:
            return

        obstacle_cells = [
            (row, column)
            for row in range(self.height)
            for column in range(self.width)
            if self.grid[row][column] == 1
        ]
        cell_radius = math.ceil(radius / self.resolution)

        for obstacle_row, obstacle_column in obstacle_cells:
            for row in range(
                obstacle_row - cell_radius,
                obstacle_row + cell_radius + 1,
            ):
                for column in range(
                    obstacle_column - cell_radius,
                    obstacle_column + cell_radius + 1,
                ):
                    if self.is_inside(row, column):
                        self.grid[row][column] = 1

    def get_neighbors(self, row, column, diagonal=False):
        """Visszaadja a szabad szomszedos cellakat."""
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        if diagonal:
            directions += [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        neighbors = []
        for row_change, column_change in directions:
            new_row = row + row_change
            new_column = column + column_change
            if self.is_free(new_row, new_column):
                is_diagonal = row_change != 0 and column_change != 0
                if is_diagonal:
                    if not self.is_free(row, new_column):
                        continue
                    if not self.is_free(new_row, column):
                        continue
                neighbors.append((new_row, new_column))

        return neighbors
````````

### `Projekt/Python_szimulacio/codes_diploma/astar_project/path_smoothing.py`

````````python
"""Egyszeru, akadalybiztos masodfoku Bezier-utvonalsimitas."""

import math


def _bezier_point(start_point, control_point, end_point, parameter):    #bemenet start pont, kontrollpont, vegpont, parameter
	"""Egy pontot szamol a harom kontrollponttal megadott gorben."""
	weight = 1 - parameter  # 
	return (
		weight ** 2 * start_point[0]
		+ 2 * weight * parameter * control_point[0]
		+ parameter ** 2 * end_point[0],
		weight ** 2 * start_point[1]
		+ 2 * weight * parameter * control_point[1]
		+ parameter ** 2 * end_point[1],
	)


def _remove_straight_points(path):
	"""Az egyenes szakaszok koztes pontjait eltavolitja."""
	if len(path) < 3:
		return list(path)

	turning_points = [path[0]]
	for point_index in range(1, len(path) - 1):
		previous_point = path[point_index - 1]
		current_point = path[point_index]
		next_point = path[point_index + 1]
		incoming_row = current_point[0] - previous_point[0]
		incoming_column = current_point[1] - previous_point[1]
		outgoing_row = next_point[0] - current_point[0]
		outgoing_column = next_point[1] - current_point[1]

		# A kereszt-szorzat nulla, ha a harom pont egy egyenesre esik.
		if incoming_row * outgoing_column != incoming_column * outgoing_row:
			turning_points.append(current_point)

	turning_points.append(path[-1])
	return turning_points


def _curve_points(start_point, control_point, end_point, sample_count):
	"""Mintapontokat keszit egy kanyarodasi Bezier-szakaszbol."""
	if sample_count <= 0:
		raise ValueError("A Bezier-mintak szama legyen pozitiv.")

	return [
		_bezier_point(
			start_point,
			control_point,
			end_point,
			sample_index / sample_count,
		)
		for sample_index in range(sample_count + 1)
	]


def _cut_point(control_point, neighbor_point, max_distance):
	"""A kontrollponttol legfeljebb max_distance tavolsagra vag."""
	delta_row = neighbor_point[0] - control_point[0]
	delta_column = neighbor_point[1] - control_point[1]
	distance = math.hypot(delta_row, delta_column)
	if distance == 0 or distance <= max_distance:
		return neighbor_point
	ratio = max_distance / distance
	return (
		control_point[0] + delta_row * ratio,
		control_point[1] + delta_column * ratio,
	)


def bezier_curve_points(path, samples_per_segment=10, max_cut_distance=None):
	"""Folytonos pontokat keszit az utvonal valodi kanyarai korul."""
	turning_points = _remove_straight_points(path)
	if len(turning_points) < 3:
		return list(path)

	curve = [turning_points[0]]
	for point_index in range(1, len(turning_points) - 1):
		previous_point = turning_points[point_index - 1]
		control_point = turning_points[point_index]
		next_point = turning_points[point_index + 1]

		# A gorbe a szomszedos elek felezopontjai kozott halad.
		if max_cut_distance is None:
			start_point = (
				(previous_point[0] + control_point[0]) / 2,
				(previous_point[1] + control_point[1]) / 2,
			)
			end_point = (
				(control_point[0] + next_point[0]) / 2,
				(control_point[1] + next_point[1]) / 2,
			)
		else:
			start_point = _cut_point(control_point, previous_point, max_cut_distance)
			end_point = _cut_point(control_point, next_point, max_cut_distance)
		if point_index == 1:
			start_point = turning_points[0]
		if point_index == len(turning_points) - 2:
			end_point = turning_points[-1]

		segment_points = _curve_points(
			start_point,
			control_point,
			end_point,
			samples_per_segment,
		)
		curve.extend(segment_points[1:])

	curve.append(turning_points[-1])
	return curve


def _is_path_safe(grid_map, path, diagonal=False):
	"""A folytonos gorbe kerekitett cellait es lepeskapcsolatait ellenorzi."""
	if not path:
		return True

	rounded_cells = [
		(round(path[0][0]), round(path[0][1]))
	]
	for start_point, end_point in zip(path, path[1:]):
		step_count = max(
			1,
			math.ceil(max(abs(end_point[0] - start_point[0]), abs(end_point[1] - start_point[1]))),
		)
		if len(path) == 2 and step_count > 1:
			return False
		for step_index in range(1, step_count + 1):
			ratio = step_index / step_count
			row = start_point[0] + ratio * (end_point[0] - start_point[0])
			column = start_point[1] + ratio * (end_point[1] - start_point[1])
			cell = (round(row), round(column))
			if cell != rounded_cells[-1]:
				rounded_cells.append(cell)

	if not all(grid_map.is_free(*cell) for cell in rounded_cells):
		return False

	return all(
		current_cell == next_cell
		or next_cell in grid_map.get_neighbors(*current_cell, diagonal)
		for current_cell, next_cell in zip(rounded_cells, rounded_cells[1:])
	)


def _has_direction_reversal(path):
	"""Megkeresi, hogy a gorbe egymas utan visszafordul-e."""
	for previous, current, following in zip(path, path[1:], path[2:]):
		incoming = (current[0] - previous[0], current[1] - previous[1])
		outgoing = (following[0] - current[0], following[1] - current[1])
		if incoming[0] * outgoing[0] + incoming[1] * outgoing[1] < -1e-9:
			return True
	return False


def smooth_path_bezier(grid_map, path, samples_per_curve=8, diagonal=False, max_cut_distance=None):
	"""Simiti a kanyarokon, veszely eseten az eredeti utat adja vissza."""
	if len(path) < 3:
		return list(path)

	turning_points = _remove_straight_points(path)
	if len(turning_points) < 3:
		return list(path)

	if max_cut_distance is None:
		max_cut_distance = 0.5 * grid_map.resolution
	cut_distance_cells = max_cut_distance / grid_map.resolution
	smoothed_path = bezier_curve_points(path, samples_per_curve, cut_distance_cells)
	if _is_path_safe(grid_map, smoothed_path, diagonal) and not _has_direction_reversal(smoothed_path):
		return smoothed_path
	return list(path)


def smooth_path(grid_map, path, diagonal=False, samples_per_curve=8, max_cut_distance=None):
	"""A projekt korabbi hivoinak megtartott belepesi pont."""
	return smooth_path_bezier(
		grid_map,
		path,
		samples_per_curve=samples_per_curve,
		diagonal=diagonal,
		max_cut_distance=max_cut_distance,
	)


r"""Vizsgáljuk meg a kódot **függvényről függvényre, sorról sorra**, részletesen kitérve az összes paraméterre, belső változóra és a mögöttes logikára.

---

### 1. `_bezier_point(start_point, control_point, end_point, parameter)`

Ez a függvény felelős a másodfokú Bézier-görbe egyetlen koordinátájának kiszámításáért egy adott $t$ paraméterhelyen.

* **Paraméterek:**
* `start_point`: Egy `(x, y)` vagy `(row, column)` koordinátapár, amely a Bézier-szakasz kezdőpontját ($P_0$) jelenti.
* `control_point`: Egy koordinátapár, amely a kontrollpontot ($P_1$, azaz maga a sarokpont) adja meg, ami felé a görbe "hajlik".
* `end_point`: Egy koordinátapár, amely a Bézier-szakasz végpontját ($P_2$) jelenti.
* `parameter`: Egy lebegőpontos szám ($t$), amely $0.0$ és $1.0$ között mozog ($0$ a szakasz eleje, $1$ a vége).


* **Belső változók:**
* `weight`: Kiszámítja a `1 - parameter` értéket (ez a $(1-t)$ tényező a képletben).


* **Működés:**
* Behelyettesíti az értékeket a másodfokú Bézier-képletbe külön az $x$ és $y$ koordinátára:
$\text{koordináta} = (1-t)^2 \cdot P_{0} + 2(1-t)t \cdot P_{1} + t^2 \cdot P_{2}$.
* Visszatér egy új, simított `(x, y)` ponttal (ami már lebegőpontos tizedesjegyeket is tartalmazhat).



---

### 2. `_remove_straight_points(path)`

Az A* által adott útvonal sok felesleges, egymás melletti pontot tartalmaz egyenes szakaszokon. Ez a függvény kiszűri őket, hogy csak a sarkok maradjanak.

* **Paraméterek:**
* `path`: Az eredeti rácspontok listája (pl. `[(0,0), (0,1), (0,2), (1,3), ...]`).


* **Belső változók:**
* `turning_points`: Egy lista, amely kezdetben csak a kezdőpontot (`path[0]`) tartalmazza, ide gyűjtjük majd a sarkokat.
* `point_index`: A ciklus futóindexe, amivel egyesével haladunk végig a belső pontokon.
* `previous_point`, `current_point`, `next_point`: Egy hármas ablak ($m-1, m, m+1$) a szomszédos csomópontok vizsgálatához.
* `incoming_row`, `incoming_column`: Az érkező vektor komponensei (`current` minus `previous`).
* `outgoing_row`, `outgoing_column`: A távozó vektor komponensei (`next` minus `current`).


* **Működés:**
* Két vektoriális irányt hasonlít össze kereszt-szorzattal (`incoming_row * outgoing_column != incoming_column * outgoing_row`).
* Ha a kereszt-szorzat nem nulla, az azt jelenti, hogy az irány megváltozott (vagyis a pont egy kanyar / sarok). Ekkor bekerül a `turning_points`-ba. Ha nulla, az azt jelenti, hogy a pont egy egyenes része, így a kód figyelmen kívül hagyja (kidobja).
* Végül hozzáadja a célpontot (`path[-1]`) is, majd visszatér a sarkok listájával.



---

### 3. `_curve_points(start_point, control_point, end_point, sample_count)`

Egy adott kanyar szakaszhoz tartozó összes mintapontot generálja le a Bézier-képlet ismételt meghívásával.

* **Paraméterek:**
* `start_point`: A kanyar kezdőpontja.
* `control_point`: A kanyar kontrollpontja (sarok).
* `end_point`: A kanyar végpontja.
* `sample_count`: Egész szám, amely megadja, hogy hány darab kis lépésre (mintára) bontsa fel a kanyar ívét.


* **Belső változók:**
* `sample_index`: A ciklusban $0$-tól `sample_count`-ig számoló index.


* **Működés:**
* Ellenőrzi, hogy a `sample_count` pozitív-e (ha nem, `ValueError`-t dob).
* Egy listagenerátorral végigfut a lépéseken, kiszámolja a $t = \text{sample\_index} / \text{sample\_count}$ arányt, meghívja a `_bezier_point`-ot, és összegyűjti az ív pontjait egy listába.



---

### 4. `bezier_curve_points(path, samples_per_segment=10)`

Ez szervezi össze a teljes útvonal simítását a sarkok és a kanyarok között.

* **Paraméterek:**
* `path`: Az eredeti A* útvonal.
* `samples_per_segment`: Hány mintapontot készítsen egy-egy kanyarhoz (alapértelmezésben `10`).


* **Belső változók:**
* `turning_points`: A `_remove_straight_points(path)` által megtisztított sarkok listája.
* `curve`: Az épülő, simított útvonalat tároló lista, amely a kezdőponttal indul.
* `point_index`: A sarkokon végigiteráló index.
* `previous_point`, `control_point`, `next_point`: A soron következő sarok és a szomszédai.
* `start_point`, `end_point`: A Bézier-ív tényleges kezdő- és végpontja. *Megjegyzés:* Ezeket a kód a szomszédos élek **felezőpontjainál** veszi fel, kivéve a teljes út elejét és végét, ahol rögzítetten a valódi kezdő/végpontot használja.
* `segment_points`: Az aktuális kanyarhoz generált pontok listája.


* **Működés:**
* Végigmegy a sarkokon, kiszámolja a felezőpontok alapján a Bézier-ívek határait, generálja a pontokat a `_curve_points`-szal, majd hozzáfűzi a `curve` listához (ügyelve arra, hogy a csatlakozási pontok ne duplázódjanak meg a `segment_points[1:]` szeleteléssel).



---

### 5. `_is_path_safe(grid_map, path, diagonal=False)`

Ez a legfontosabb **biztonsági védőháló**, ami garantálja, hogy a robot ne ütközzön neki semminek a simítás miatt.

* **Paraméterek:**
* `grid_map`: A térkép objektum (amelyben az akadályok helye van tárolva).
* `path`: A simított, lebegőpontos koordinátákat tartalmazó útvonal.
* `diagonal`: Logikai érték (`True` / `False`), ami engedélyezi-e az átlós rácslépéseket.


* **Belső változók:**
* `rounded_cells`: Mivel a Bézier-görbe tizedesjegyeket ad (pl. `(1.23, 4.56)`), ez a lista **egész rácscellákra kerekíti** (`round()`) az összes pontot, hogy illeszkedjenek a diszkrét rácstérképre.
* `current_cell`, `next_cell`: Az egymást követő cellák a `zip()` iterációban.


* **Működés:**
1. Ellenőrzi, hogy a kerekített útvonal **minden egyes cellája szabad-e** (`grid_map.is_free(*cell)`). Ha bárhol akadályba ütközne, azonnal `False`-lal visszatér.
2. Ellenőrzi a lépéskapcsolatokat is: a `grid_map.get_neighbors(...)` segítségével megnézi, hogy az egymást követő pontok valóban szomszédos, szabályos lépések-e a rácson (így a robot nem tud "átugrani" egy falat vagy illegális ugrást tenni). Ha minden rendben, `True`-t ad vissza.



---

### 6. `smooth_path_bezier(grid_map, path, samples_per_curve=8, diagonal=False)`

A fő vezérlőfüggvény, ami összehozza a generálást és a biztonsági ellenőrzést.

* **Paraméterek:**
* `grid_map`: A térkép objektum.
* `path`: Az eredeti A* útvonal.
* `samples_per_curve`: A kanyarok finomsága (alapértelmezett: `8` mintapont kanyaroonként).
* `diagonal`: Átlós mozgás engedélyezése.


* **Belső változók:**
* `turning_points`: A kiszűrt sarkok listája.
* `smoothed_path`: A `bezier_curve_points` által legyártott simított útvonal.


* **Működés:**
* Ha az útvonal túl rövid (< 3 pont), simítás nélkül visszaadja.
* Lefuttatja a Bézier-simítást (`smoothed_path`).
* Meghívja az `_is_path_safe`-et. **Ha a simított út biztonságos, akkor a simított utat adja vissza. Ha viszont a kanyar miatt a robot túl közel menne egy falhoz (vagyis nem biztonságos), akkor a kód eldobja az egészet, és az eredeti, garantáltan biztonságos A* útvonalat adja vissza.**



---

### 7. `smooth_path(grid_map, path, diagonal=False, samples_per_curve=8)`

* **Paraméterek:** Ugyanazok, mint az előző függvénynél.
* **Működés:** Ez egy **kompatibilitási burkolófüggvény (wrapper)**. Ha a projekted más moduljai korábban a `smooth_path` nevet hívták meg, ez a függvény változatlanul továbbítja az összes paramétert a `smooth_path_bezier`-nek, így nem kell átírnod a többi fájlodban a függvényhívásokat.
    """
````````

### `Projekt/Python_szimulacio/codes_diploma/DWA+A.py`

````````python
"""A* globális útvonal és DWA lokális vezérlés integrációja."""

from __future__ import annotations  # Típusannotációk késleltetett kiértékelése (előre hivatkozható típusok)
import math  # Matematikai műveletekhez (hypot, gyökvonás, trigonometria)
from typing import Any, Dict, List, Optional, Sequence, Tuple

# Külső projektmodulok importálása a tervezéshez és konfigurációhoz
from codes_diploma.astar_project.astar_baseline import astar_search  # Diszkrét A* kereső algoritmus
from codes_diploma.astar_project.path_smoothing import smooth_path  # Bézier-alapú saroklekerekítő algoritmus
from codes_diploma.DWA import optimisation, pairstochoose  # DWA sebességtér mintavételezés és költségoptimalizálás
from codes_diploma.robot import Goal, robotconfig  # Célpont reprezentáció és robot fizikai paraméterei
from typing import Tuple  # Típusjelölések a tiszta C++-os kódképhez

# Típusaliasok a C++ 'using' vagy 'typedef' mintájára
Point2D = Tuple[float, float]  # Folytonos világkoordináta: (x, y) méterben
GridCoord = Tuple[int, int]  # Diszkrét térképkoordináta: (sor, oszlop) cellaindexben


class AStarDWAPlanner:
    """Kétszintű hibrid útvonaltervező és mozgásvezérlő osztály."""

    def __init__(
        self,
        grid_map: Any,  # Bemeneti foglaltsági rácstérkép
        config: Optional[Any] = None,  # Robot dinamikai és geometriai korlátai
        diagonal: bool = True,  # Engedélyezi-e a 8-irányú (átlós) mozgást az A*-ban
        waypoint_tolerance: float = 0.2,  # Alapértelmezett elfogadási sugár egy ponthoz [m]
        waypoint_spacing: float = 0.2,  # Waypointok közötti egyenletes távolság az újramintavételezéskor [m]
    ) -> None:
        self.grid_map = grid_map  # Térkép elmentése a koordináta-transzformációkhoz
        self.config = config if config is not None else robotconfig()  # Konfiguráció inicializálása
        self.diagonal: bool = diagonal  # Átlós szomszédok engedélyezésének mentése
        self.waypoint_tolerance: float = waypoint_tolerance  # Névleges toleranciasugár rögzítése
        self.waypoint_spacing: float = waypoint_spacing  # Újramintavételezési lépésköz rögzítése

        self.path: List[Point2D] = []  # Végleges, aktívan követett folytonos útvonal pontjai
        self.astar_path: List[Point2D] = []  # Nyers, töréspontos A* világkoordináták listája
        self.bezier_path: List[Point2D] = []  # Saroklekerekített, simított Bézier pontok listája
        self.waypoints: List[Point2D] = []  # Egyenletesen diszkretizált célpontok láncolata
        self.waypoint_index: int = 0  # Az aktuálisan követett referencia waypoint sorszáma

    def _current_tolerance(self, state: Any) -> float:
        """Kiszámítja az adaptív toleranciát a célhoz mért távolság alapján."""
        if not self.waypoints:  # Ha nincs betöltve útvonal
            return self.waypoint_tolerance  # Az alapértelmezett tűréssel tér vissza

        goal_x, goal_y = self.waypoints[-1]  # A legutolsó pont (globális végcél) koordinátái
        goal_distance: float = math.hypot(goal_x - state.x, goal_y - state.y)  # Robot-végcél távolság

        # 0.05m és waypoint_tolerance közé szorított, távolságarányos dinamikus tűrés
        return max(0.05, min(self.waypoint_tolerance, goal_distance * 0.2))

    @staticmethod
    def _create_waypoints(path: Sequence[Point2D], spacing: float = 0.2) -> List[Point2D]:
        """A nyers/simított görbét egyenlő ívhosszúságú szakaszokra osztja fel."""
        if not path:  # Üres útvonal esetén
            return []  # Üres listát ad vissza

        waypoints: List[Point2D] = [path[0]]  # A kezdőpont mindig bekerül első waypointként
        remaining_distance: float = spacing  # A következő pont lehelyezéséig hátralévő távolság
        segment_start: Point2D = path[0]  # A vizsgált útszakasz kezdőkoordinátája

        for segment_end in path[1:]:  # Végiglépked az útvonal egymást követő pontjain
            dx: float = segment_end[0] - segment_start[0]  # Szakasz X irányú hossza
            dy: float = segment_end[1] - segment_start[1]  # Szakasz Y irányú hossza
            segment_length: float = math.hypot(dx, dy)  # Két pont közötti euklideszi távolság

            if segment_length == 0.0:  # Ha a két egymást követő pont egybeesik
                continue  # Átugorjuk a felesleges nullosztást

            while segment_length >= remaining_distance:  # Ha a szakasz hosszabb a szükséges távnál
                ratio: float = remaining_distance / segment_length  # Interpolációs arány [0.0, 1.0]
                point: Point2D = (  # Beszúrt új pont kiszámítása lineáris arányosítással
                    segment_start[0] + ratio * dx,  # Új pont X koordinátája
                    segment_start[1] + ratio * dy,  # Új pont Y koordinátája
                )
                waypoints.append(point)  # Pont hozzáadása a diszkrét lánchoz

                segment_start = point  # A szakasz új kezdőpontja az imént beszúrt pont lesz
                dx = segment_end[0] - segment_start[0]  # Hátralévő szakasz X távolságának frissítése
                dy = segment_end[1] - segment_start[1]  # Hátralévő szakasz Y távolságának frissítése
                segment_length = math.hypot(dx, dy)  # Hátralévő szakasz hosszának újraszámolása
                remaining_distance = spacing  # Visszaállítjuk a teljes lépésközt a következő ponthoz

            remaining_distance -= segment_length  # Levonjuk a szakaszból megmaradt tört távolságot
            segment_start = segment_end  # Átlépünk a következő szakaszra

        if waypoints[-1] != path[-1]:  # Ha a lépésközök miatt a legvégső pont kimaradt volna
            waypoints.append(path[-1])  # Explicit hozzáadjuk a pontos célpontot

        return waypoints  # Visszaadjuk a kiszámított, egyenletes pontlistát

    def _update_pruned_lookahead_target(self, state: Any) -> Tuple[Point2D, int]:
        """Elvégzi a szakasz-metszést (pruning) és kijelöli az előretekintő célpontot."""
        search_window: int = 25  # Keresési ablak mérete (ennyi pontot vizsgál előre a robot előtt)
        end_search: int = min(len(self.waypoints), self.waypoint_index + search_window)  # Keresés felső indexe

        min_dist: float = float("inf")  # Legkisebb távolság kezdeti értéke végtelenre állítva
        closest_idx: int = self.waypoint_index  # Legközelebbi pont indexének tárolója

        for i in range(self.waypoint_index, end_search):  # Ciklus az előretekintési ablakon
            dist: float = math.hypot(self.waypoints[i][0] - state.x, self.waypoints[i][1] - state.y)  # Távolság mérése
            if dist < min_dist:  # Ha találtunk közelebbi pontot a robot pillanatnyi helyéhez
                min_dist = dist  # Elmentjük az új minimális távolságot
                closest_idx = i  # Elmentjük a legközelebbi pont sorszámát

        self.waypoint_index = max(self.waypoint_index, closest_idx)  # Monotonitás: index nem léphet vissza

        # Adaptív előretekintési távolság a pillanatnyi transzlációs sebesség (v) alapján: [0.35m - 0.80m]
        lookahead_distance: float = max(0.35, min(0.80, abs(state.v) * 1.2))

        accumulated_dist: float = 0.0  # Görbe mentén kumulált ívhossz összegzője
        target_idx: int = self.waypoint_index  # A kijelölt előretekintési pont indexe

        for i in range(self.waypoint_index, len(self.waypoints) - 1):  # Ívhossz összegzése a metszett indextől
            p1: Point2D = self.waypoints[i]  # Szakasz kezdőpontja
            p2: Point2D = self.waypoints[i + 1]  # Szakasz végpontja
            accumulated_dist += math.hypot(p2[0] - p1[0], p2[1] - p1[1])  # Távolság hozzáadása az ívhosszhoz
            if accumulated_dist >= lookahead_distance:  # Ha elértük a sebességfüggő előretekintést
                target_idx = i + 1  # Kijelöljük ezt a pontot közvetlen célpontnak
                break  # Megvan a pont, kilépünk a ciklusból
        else:
            target_idx = len(self.waypoints) - 1  # Ha elfogyott a pálya, a legutolsó pontra állunk rá

        return self.waypoints[target_idx], target_idx  # Visszaadjuk a koordinátát és annak indexét

    def plan_global(
        self,
        start_world: Point2D,  # Start pozíció világkoordinátában (x, y) [m]
        goal_world: Point2D,  # Cél pozíció világkoordinátában (x, y) [m]
        heuristic: Optional[Any] = None,  # Egyedi A* heurisztika függvény (ha nincs, euklideszi)
        smooth: bool = True,  # Engedélyezze-e a Bézier íves simítást
        samples_per_curve: int = 8,  # Görbénkénti mintavételi pontok száma a simításnál
        max_cut_distance: Optional[float] = None,  # Saroklevágás maximális megengedett távolsága
    ) -> Optional[Tuple[Point2D, ...]]:
        """Globális A* keresés, saroksimítás és waypoint lánc generálása."""
        start_grid: GridCoord = self.grid_map.world_to_grid(*start_world)  # Start átváltása rácskoordinátára
        goal_grid: GridCoord = self.grid_map.world_to_grid(*goal_world)  # Cél átváltása rácskoordinátára

        raw_path: Optional[List[GridCoord]] = astar_search(  # A* útvonalkeresés futtatása a rácson
            self.grid_map,  # Bemeneti térkép
            start_grid,  # Kezdőcella
            goal_grid,  # Célcella
            diagonal=self.diagonal,  # 8-irányú szomszédság vizsgálata
            heuristic=heuristic,  # Heurisztika átadása
        )

        if raw_path is None:  # Ha nincs járható út a start és a cél között
            self.path.clear()  # Végleges út ürítése
            self.astar_path.clear()  # Nyers A* út ürítése
            self.bezier_path.clear()  # Simított út ürítése
            self.waypoints.clear()  # Diszkrét pontok ürítése
            self.waypoint_index = 0  # Index nullázása
            return None  # Tervezési hiba jelzése

        # A* cellaindexek visszaváltása méter alapú világkoordinátákra
        self.astar_path = [self.grid_map.grid_to_world(r, c) for r, c in raw_path]

        if smooth:  # Ha kértünk saroklekerekítést
            if max_cut_distance is None:  # Ha nincs explicit beállítva vágási limit
                max_cut_distance = 0.5 * self.grid_map.resolution  # Fél cellányi felbontást engedünk vágni

            smoothed_raw_path = smooth_path(  # Bézier simítás végrehajtása
                self.grid_map,  # Térkép az ütközésmentes ívekhez
                raw_path,  # Nyers rácsútvonal
                diagonal=self.diagonal,  # Átlós mozgás figyelembevétele
                samples_per_curve=samples_per_curve,  # Ívminták sűrűsége
                max_cut_distance=max_cut_distance,  # Maximális sarokvágási távolság
            )
            # Simított rácspontok transzformálása világkoordinátákra
            self.bezier_path = [self.grid_map.grid_to_world(r, c) for r, c in smoothed_raw_path]
        else:
            self.bezier_path = list(self.astar_path)  # Simítás nélkül az A* út marad

        self.path = list(self.bezier_path)  # Aktív trajektória frissítése
        self.waypoints = self._create_waypoints(self.path, self.waypoint_spacing)  # Egyenletes újramintavétel
        self.waypoint_index = min(1, len(self.waypoints) - 1)  # Az első aktív waypoint

        return tuple(self.path)  # Útvonal visszaadása konstans tuple formátumban

    def plan_local(self, state: Any, obstacles: Sequence[Any] = ()) -> Optional[Dict[str, Any]]:
        """Egy vezérlési ciklust hajt végre: célpontot frissít és DWA parancsot generál."""
        if not self.waypoints:  # Ha nincs követhető waypoint generálva
            return None  # Nincs feladat, visszatérés

        if self.reached_goal(state):  # Ha a robot beért a legvégső cél toleranciakörébe
            return {
                "waypoint": self.waypoints[-1],  # Elért utolsó pont
                "target": self.waypoints[-1],  # Célként rögzített utolsó pont
                "best_pair": [0.0, 0.0, 0.0, 0.0],  # Nulla sebesség: robot megállítása [v, w, ...]
                "safe_pairs": [],  # Nincsenek további vizsgált ágak
                "all_pairs": [],  # Nincsenek további vizsgált ágak
                "finished": True,  # Sikeres célba érés flag-je
            }

        current = self.waypoints[self.waypoint_index]
        current_tolerance = self._current_tolerance(state)
        if self.waypoint_index < len(self.waypoints) - 1:
            next_point = self.waypoints[self.waypoint_index + 1]
            to_current = (current[0] - state.x, current[1] - state.y)
            next_direction = (
                next_point[0] - current[0],
                next_point[1] - current[1],
            )
            passed_waypoint = (
                to_current[0] * next_direction[0]
                + to_current[1] * next_direction[1]
                < 0
            )
            if (
                math.hypot(current[0] - state.x, current[1] - state.y)
                <= current_tolerance
                or passed_waypoint
            ) and abs(state.v) <= 0.3:
                self.waypoint_index += 1

        target = self.waypoints[self.waypoint_index]
        is_final_waypoint: bool = self.waypoint_index == len(self.waypoints) - 1
        slow_down_distance: float = 0.5 if is_final_waypoint else 0.35  # Végcélnál korábban kezdünk lassítani

        # Lassítás engedélyezése ha konfigurálva van, vagy ha a pálya legvégére értünk
        enable_slowdown: bool = (
            getattr(self.config, "enable_waypoint_slowdown", False) or is_final_waypoint
        )

        goal = Goal(  # DWA lokális célpont objektum példányosítása
            target[0],  # Cél X koordinátája
            target[1],  # Cél Y koordinátája
            self.waypoint_tolerance,  # Célhoz tartozó hibatűrés
            slow_down=enable_slowdown,  # Sebességcsökkentési kényszer bekapcsolása
            slow_down_distance=slow_down_distance,  # Lassítási zóna sugara
        )

        # DWA sebességtér kiértékelése: optimális sebességpár és ütközésmentes alternatívák
        best_pair, safe_pairs = optimisation(self.config, state, goal, obstacles)
        all_pairs = pairstochoose(self.config, state)  # Az összes kinematikailag lehetséges ablak-mintavétel

        return {
            "waypoint": self.waypoints[self.waypoint_index],  # Aktív referencia-waypoint
            "target": target,  # DWA által közvetlenül célzott előretekintési pont
            "best_pair": best_pair,  # Kiválasztott optimális beavatkozójel: [v, w, ...]
            "safe_pairs": safe_pairs,  # Ütközésmentes pályák halmaza (megjelenítéshez/naplózáshoz)
            "all_pairs": all_pairs,  # Összes dinamikai ablakba eső sebességpár
            "finished": self.reached_goal(state),  # Végcél elérési állapotának visszajelzése
        }

    def reached_goal(self, state: Any) -> bool:
        """Megvizsgálja, hogy a robot elérte-e a globális végcélt a dinamikus tolerancián belül."""
        if not self.waypoints:  # Ha nincs útvonal
            return False  # Nem érhettünk célba

        goal_x, goal_y = self.waypoints[-1]  # Globális cél X és Y pozíciója
        dist_to_goal: float = math.hypot(goal_x - state.x, goal_y - state.y)  # Aktuális távolság a célig
        return dist_to_goal <= self._current_tolerance(state)  # Távolság összevetése a szűkített toleranciával
````````

### `Projekt/Python_szimulacio/codes_diploma/DWA.py`

````````python
"""Dinamikus ablakos lokális útvonaltervezés (Dynamic Window Approach - DWA)."""

import math
import numpy as np
from .robot import get_robot_kinematics, robotstate, update


"""
Kiszámítja a megtett utat az ív mentén az első ütközésig.
Ha nincs ütközés a predict_time alatt, egy nagy értéket ad vissza.
"""
def get_dist_on_trajectory(state, config, w_L, w_R, obstacle_list):
    temp_robot = robotstate(x=state.x, y=state.y, irany=state.irany, w_L=state.w_L, w_R=state.w_R)
    accumulated_dist = 0.0
    v_actual, _ = get_robot_kinematics(w_L, w_R, config)
    
    # --- SZENZOR PARAMÉTEREK ---
    max_sensor_dist = 3.0  # 3 méterig lát el a LiDAR
    fov_angle = math.radians(180)  # 180 fokos látószög elöl
    
    for t in np.arange(0, config.predict_time, config.dt):
        for obs in obstacle_list:
            # 1. Szenzor szűrés: Csak azt látja, ami közel van
            dist_now = math.hypot(state.x - obs.x, state.y - obs.y)
            if dist_now > max_sensor_dist:
                continue
                
            # 2. FOV szűrés: Csak azt látja, ami előtte van (+-90 fok)
            angle_to_obs = math.atan2(obs.y - state.y, obs.x - state.x)
            diff_angle = math.atan2(
                math.sin(angle_to_obs - state.irany),
                math.cos(angle_to_obs - state.irany)
            )
            if abs(diff_angle) > fov_angle / 2:
                continue

            # 3. DINAMIKUS PREDIKCIÓ: Hol lesz az akadály 't' idő múlva?
            obs_future_x = obs.x + obs.vx * t
            obs_future_y = obs.y + obs.vy * t
            
            dist_centers = math.hypot(temp_robot.x - obs_future_x, temp_robot.y - obs_future_y)
            
            # 4. KÜLÖNVÁLASZTOTT INFLÁCIÓ: Statikus fal mellett szűk ráhagyás, mozgónál teljes
            is_static = (obs.vx == 0.0 and obs.vy == 0.0)
            if is_static:
                collision_threshold = obs.radius + config.rob_radius + getattr(config, "static_safety_margin", 0.01)
            else:
                collision_threshold = config.rob_radius + obs.radius + config.safety_margin
            
            if dist_centers <= collision_threshold:
                return accumulated_dist 
        
        # Állapotfrissítés az ív mentén
        update(temp_robot, config, w_L, w_R, config.dt)
        accumulated_dist += abs(v_actual) * config.dt
                
    return 10.0


#############xx FÉKEZÉSI FELTÉTELEK ###############
def AdmissableVelocity(robotconfig, w_L, w_R, state, obstacle_list):
    """
    Ellenőrzi, hogy a robot meg tud-e állni az adott íven az ütközés előtt.
    """
    # 1. Kiszámítjuk a távolságot az ív mentén az ütközésig
    dist_to_obs = get_dist_on_trajectory(state, robotconfig, w_L, w_R, obstacle_list)
    
    # 2. Megkapjuk a lineáris sebességet (v)
    v, _ = get_robot_kinematics(w_L, w_R, robotconfig)
    
    # Fékezési feltétel: |v| <= sqrt(2 * a_max * dist)
    if abs(v) <= math.sqrt(2 * robotconfig.a_max * dist_to_obs):
        return True
    return False


"""        
Összes választható v,w pár kiszámolása kerekekből számítva
"""
def pairstochoose(robotconfig, robotstate):

    w_dot_max = robotconfig.a_max / robotconfig.r_kerek         # w_dot = a / r
   
    w_L_min_actual = max(robotconfig.w_kerek_min, robotstate.w_L - w_dot_max * robotconfig.dt)
    w_L_max_actual = min(robotconfig.w_kerek_max, robotstate.w_L + w_dot_max * robotconfig.dt)

    w_R_min_actual = max(robotconfig.w_kerek_min, robotstate.w_R - w_dot_max * robotconfig.dt)
    w_R_max_actual = min(robotconfig.w_kerek_max, robotstate.w_R + w_dot_max * robotconfig.dt)
   
    w_L_samples = np.arange(w_L_min_actual, w_L_max_actual + robotconfig.w_kerek_resolution, robotconfig.w_kerek_resolution)
    w_R_samples = np.arange(w_R_min_actual, w_R_max_actual + robotconfig.w_kerek_resolution, robotconfig.w_kerek_resolution)

    all_pairs = []
    for w_L in w_L_samples:
        for w_R in w_R_samples:
            v, w = get_robot_kinematics(w_L, w_R, robotconfig)

            all_pairs.append([v, w, w_L, w_R])
    return all_pairs


########################Összes lehetséges választható pálya eltárolása ami biztonságos megállást biztosít#######################x

def safepairs(robotconfig, state, obstacle_list):
    """
    Eredő keresési tér (Vr = Vs ∩ Vd ∩ Va):
    Kiszűri azokat a sebességpárokat, amelyek kielégítik a megállási feltételt,
    és kiszűri a tolató pályákat (hacsak nincs kifejezetten engedélyezve a tolatás).
    """
    allow_reverse = getattr(robotconfig, "allow_reverse", False)
    
    admissible_list = []  # Ebben csak a "jó" párok lesznek
    
    for pair in pairstochoose(robotconfig, state):
        v = pair[0]
        w_L = pair[2]
        w_R = pair[3]
        
        # Előremeneti kényszer: ne válasszon tolatást vészmegoldásként
        if not allow_reverse and v < 0.0:
            continue
            
        if AdmissableVelocity(robotconfig, w_L, w_R, state, obstacle_list):
            admissible_list.append(pair)
                
    return admissible_list


################################################

############# optimalizáció #####################
def optimisation(robotconfig, state, goal, obstacle_list):
    # 1. Biztonságos sebességpárok lekérése
    safe_list = safepairs(robotconfig, state, obstacle_list)
    
    # Ha nincs biztonságos út (ÜRES A LISTA -> DEADLOCK)
    if not safe_list:
        # Visszaadunk egy speciális jelzést (None), hogy a főciklus tudja: Recovery kell
        return None, []

    best_score = -float('inf')
    best_pair = None
    
    dist_to_goal = math.hypot(goal.x - state.x, goal.y - state.y)
    v_max_robot = robotconfig.w_kerek_max * robotconfig.r_kerek
    
    # 2. Adaptív predikció: célhoz közeledve vagy éles szögeltérés esetén dinamikusan rövidül
    adaptive_predict_time = robotconfig.predict_time
    heading_to_goal = math.atan2(goal.y - state.y, goal.x - state.x)
    heading_error = abs(
        math.atan2(
            math.sin(heading_to_goal - state.irany),
            math.cos(heading_to_goal - state.irany),
        )
    )
    
    if dist_to_goal < 1.0:
        adaptive_predict_time = max(0.5, dist_to_goal * 2.0)
    
    alfa = robotconfig.Alfa      # Célra tartás súlya
    beta = robotconfig.Beta      # Akadálykerülés súlya
    gamma = robotconfig.Gamma    # Sebességszabályozás súlya

    for v, w, w_L, w_R in safe_list:  
        # Gyors szimuláció a jövőbeli állapot becsléséhez az adaptív időablak végéig
        temp_robot = robotstate(x=state.x, y=state.y, irany=state.irany, w_L=state.w_L, w_R=state.w_R)
        for _ in np.arange(0, adaptive_predict_time, robotconfig.dt):
            update(temp_robot, robotconfig, w_L, w_R, robotconfig.dt)
        
        # --- PONTOZÁSI LOGIKA ---

        # A: Heading score (Irányhiba normalizálva 0 és 1 közé, atan2 periodicitás-kezeléssel)
        angle_to_goal = getattr(goal, "heading", None)
        if angle_to_goal is None:
            angle_to_goal = math.atan2(goal.y - temp_robot.y, goal.x - temp_robot.x)
            
        error_angle = math.atan2(
            math.sin(angle_to_goal - temp_robot.irany), 
            math.cos(angle_to_goal - temp_robot.irany)
        )
        score_heading = (math.pi - abs(error_angle)) / math.pi
        
        # B: Dist score (Akadályoktól való távolság az ív mentén)
        score_dist = get_dist_on_trajectory(state, robotconfig, w_L, w_R, obstacle_list)
        
        # C: Velocity score (Szabad haladás esetén maximális tempó, cél közelében dinamikus lebegtetés)
        slow_down_distance = getattr(goal, "slow_down_distance", 0.8)
        if not getattr(goal, "slow_down", True) and dist_to_goal > slow_down_distance:
            score_vel = v / v_max_robot
        else:
            # Nem engedi a célsebességet 0-ra fulladni, dinamikusabban húz a cél felé
            v_target = min(v_max_robot, max(0.08, dist_to_goal * 1.4))
            score_vel = 1.0 - (abs(v_target - v) / v_max_robot)

        # Végső pontszám kiszámítása a költségfüggvény súlyaival
        score = (alfa * score_heading + 
                 beta * score_dist + 
                 gamma * score_vel)

        if score > best_score:
            best_score = score
            best_pair = [v, w, w_L, w_R]

    return best_pair, safe_list
````````

### `Projekt/Python_szimulacio/codes_diploma/robot.py`

````````python
"""Differenciális meghajtású robotmodell."""

import math

import numpy as np


def get_robot_kinematics(w_L, w_R, config):
	"""Keréksebességből lineáris és szögsebességet számol."""
	v = ((w_L + w_R) / 2) * config.r_kerek
	w = ((w_R - w_L) / (2 * config.b)) * config.r_kerek
	return v, w


class Obstacle:
	def __init__(self, x, y, radius=0.1, vx=0.0, vy=0.0):
		self.x = x
		self.y = y
		self.radius = radius
		self.vx = vx
		self.vy = vy

	def move(self, dt):
		self.x += self.vx * dt
		self.y += self.vy * dt


class Goal:
	def __init__(self, x, y, tolerance=0.15, slow_down=True, slow_down_distance=0.8, heading=None):
		self.x = x
		self.y = y
		self.tolerance = tolerance
		self.slow_down = slow_down
		self.slow_down_distance = slow_down_distance
		self.heading = heading


class robotconfig:
	def __init__(robot):
		robot.r_kerek = 0.033
		robot.b = 0.08
		robot.w_kerek_max = 15
		robot.a_max = 2
		robot.w_kerek_min = -robot.w_kerek_max
		robot.w_kerek_resolution = 1
		robot.allow_reverse = False
		robot.dt = 0.1
		robot.predict_time = 3
		robot.rob_radius = robot.b + 0.02
		robot.safety_margin = 0.15
		robot.static_safety_margin = 0.01  # Új paraméter a statikus falak melletti tűréshez
		robot.Alfa = 5
		robot.Beta = 2
		robot.Gamma = 3
		robot.enable_waypoint_slowdown = False


class robotstate:
	def __init__(robot, x=0, y=0, v=0, w=0, irany=0, w_L=0, w_R=0):
		robot.x = x
		robot.y = y
		robot.v = v
		robot.w = w
		robot.irany = irany
		robot.w_L = w_L
		robot.w_R = w_R


def update(robot, config, w_L_target, w_R_target, dt):
	"""Frissíti a robotot a gyorsuláskorlátozás és a kinematika alapján."""
	max_w_dot = config.a_max / config.r_kerek
	w_L_new = robot.w_L + np.clip(
		w_L_target - robot.w_L,
		-max_w_dot * dt,
		max_w_dot * dt,
	)
	w_R_new = robot.w_R + np.clip(
		w_R_target - robot.w_R,
		-max_w_dot * dt,
		max_w_dot * dt,
	)
	v, w = get_robot_kinematics(w_L_new, w_R_new, config)
	theta_0 = robot.irany

	if abs(w) > 1e-6:
		robot.x += (v / w) * (math.sin(theta_0 + w * dt) - math.sin(theta_0))
		robot.y += -(v / w) * (math.cos(theta_0 + w * dt) - math.cos(theta_0))
	else:
		robot.x += v * math.cos(theta_0) * dt
		robot.y += v * math.sin(theta_0) * dt

	robot.irany += w * dt
	robot.v = v
	robot.w = w
	robot.w_L = w_L_new
	robot.w_R = w_R_new

	return np.array([robot.x, robot.y, robot.irany, robot.v, robot.w, robot.w_L, robot.w_R])
````````

### `Projekt/Python_szimulacio/codes_diploma/simulation.py`

````````python
"""A* + DWA szimulacio az onlabos palyamegjelenitessel es a palyak vegi fekezessel."""

import importlib.util
import math
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

import matplotlib

matplotlib.use("TkAgg")

from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle, Rectangle
import matplotlib.pyplot as plt

from codes_diploma.astar_project.astar_baseline import astar_search
from codes_diploma.astar_project.astar_variants import get_heuristic
from codes_diploma.astar_project.grid_map import GridMap
from codes_diploma.DWA import AdmissableVelocity, get_dist_on_trajectory
from codes_diploma.robot import Obstacle, robotconfig, robotstate, update


def load_planner_class():
    """Betolti a pluszjelet tartalmazo DWA+A.py modult."""
    file_path = Path(__file__).with_name("DWA+A.py")
    spec = importlib.util.spec_from_file_location("dwa_a_module", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.AStarDWAPlanner


def parse_cell(value):
    """Szoveges cellakoordinatat konvertal egesz parra."""
    row, column = (int(part.strip()) for part in value.split(","))
    return row, column


def create_scene(
    width=30,
    height=20,
    resolution=0.2,
    start_cell=(2, 2),
    goal_cell=(17, 27),
    inflation_radius=0.11,
):
    """Letrehozza az A* es DWA kozos terkepet es akadalyait."""
    grid_map = GridMap(width=width, height=height, resolution=resolution)
    vertical_column = min(10, width - 2)
    horizontal_row = min(12, height - 2)
    static_cells = []

    for row in range(2, max(2, height - 2)):
        if row not in range(7, 13):
            static_cells.append((row, vertical_column))
    for column in range(12, max(12, width - 2)):
        if column not in range(19, 25):
            static_cells.append((horizontal_row, column))

    for cell in static_cells:
        if grid_map.is_inside(*cell) and cell not in (start_cell, goal_cell):
            grid_map.add_obstacle(*cell)
    grid_map.inflate_obstacles(inflation_radius)

    start = grid_map.grid_to_world(*start_cell)
    goal = grid_map.grid_to_world(*goal_cell)
    state = robotstate(x=start[0], y=start[1], irany=0.0)
    static_obstacles = [
        Obstacle(*grid_map.grid_to_world(*cell), radius=0.12)
        for cell in static_cells
    ]
    dynamic_obstacles = [
        Obstacle(2.4, 0.4, radius=0.18, vx=0.0, vy=0.20),
        Obstacle(6.8, 2.1, radius=0.18, vx=-0.25, vy=0.0),
    ]
    return (
        grid_map,
        start_cell,
        goal_cell,
        start,
        goal,
        state,
        static_obstacles,
        dynamic_obstacles,
    )


def compute_onlab_trajectories(state, config, all_pairs, best_pair, obstacles):
    """Kiszamolja a josolt palyakat es azok vegen a fekezesi szakaszokat az onlab alapjan."""
    unsafe_paths = []
    unsafe_brakes = []

    safe_paths = []
    safe_brakes = []

    best_path = ([], [])
    best_brake = ([], [])

    predict_steps = max(1, int(round(config.predict_time / config.dt)))

    for v, w, w_L, w_R in all_pairs:
        # Csak elorehaladast vizsgalunk, ha a hatramenet tiltott
        if not getattr(config, "allow_reverse", False) and v < 0:
            continue

        is_best = False
        if best_pair is not None:
            if math.isclose(w_L, best_pair[2], abs_tol=1e-3) and math.isclose(
                w_R, best_pair[3], abs_tol=1e-3
            ):
                is_best = True

        is_safe = AdmissableVelocity(config, w_L, w_R, state, obstacles)
        dist_to_coll = get_dist_on_trajectory(state, config, w_L, w_R, obstacles)

        # 1. Jósolt szakasz (Trajectory rollout)
        ghost = robotstate(
            x=state.x, y=state.y, irany=state.irany, w_L=state.w_L, w_R=state.w_R
        )
        path_points = [(ghost.x, ghost.y)]
        for _ in range(predict_steps):
            update(ghost, config, w_L, w_R, config.dt)
            path_points.append((ghost.x, ghost.y))

        # 2. Fékezési szakasz a jósolt szakasz legvégétől indítva (önlabos képlet)
        t_stop = abs(v) / config.a_max if abs(v) > 0.0 else 0.0
        brake_robot = robotstate(
            x=ghost.x, y=ghost.y, irany=ghost.irany, w_L=w_L, w_R=w_R
        )
        brake_points = [(brake_robot.x, brake_robot.y)]
        brake_steps = (
            int(math.ceil(t_stop / config.dt)) if t_stop > 0.0 else 0
        )

        for step_idx in range(brake_steps):
            t = step_idx * config.dt
            factor = max(0.0, 1.0 - (t / t_stop)) if t_stop > 0.0 else 0.0
            update(brake_robot, config, w_L * factor, w_R * factor, config.dt)
            brake_points.append((brake_robot.x, brake_robot.y))

        # 3. Szétválogatás
        if is_best:
            px, py = zip(*path_points)
            bx, by = zip(*brake_points)
            best_path = (list(px), list(py))
            best_brake = (list(bx), list(by))
        elif dist_to_coll < (abs(v) * config.predict_time) or not is_safe:
            unsafe_paths.append(path_points)
            unsafe_brakes.append(brake_points)
        else:
            safe_paths.append(path_points)
            safe_brakes.append(brake_points)

    return (
        unsafe_paths,
        unsafe_brakes,
        safe_paths,
        safe_brakes,
        best_path,
        best_brake,
    )


def create_simulation(
    width=30,
    height=20,
    resolution=0.2,
    start_cell=(2, 2),
    goal_cell=(17, 27),
    diagonal=True,
    heuristic_name="euclidean",
    inflation_radius=0.1,
    smooth=True,
    samples_per_curve=8,
    alpha=5.0,
    beta=2.0,
    gamma=3.0,
    waypoint_slowdown=False,
    show_original_astar=False,
    max_steps=600,
    auto_play=True,
    show=False,
):
    planner_class = load_planner_class()
    (
        grid_map,
        start_cell,
        goal_cell,
        start,
        goal,
        state,
        static_obstacles,
        dynamic_obstacles,
    ) = create_scene(
        width, height, resolution, start_cell, goal_cell, inflation_radius
    )
    heuristic = get_heuristic(heuristic_name)
    astar_result = astar_search(
        grid_map,
        start_cell,
        goal_cell,
        diagonal=diagonal,
        heuristic=heuristic,
        return_details=True,
    )
    if astar_result["path"] is None:
        raise RuntimeError("Az A* nem talalt utvonalat a beallitott terkepen.")

    config = robotconfig()
    config.Alfa = alpha
    config.Beta = beta
    config.Gamma = gamma
    config.enable_waypoint_slowdown = waypoint_slowdown
    planner = planner_class(grid_map, config=config, diagonal=diagonal)
    path = planner.plan_global(
        start,
        goal,
        heuristic=heuristic,
        smooth=smooth,
        samples_per_curve=samples_per_curve,
    )
    expanded_world = [
        grid_map.grid_to_world(*cell) for cell in astar_result["expanded_nodes"]
    ]
    path_world = list(path)
    planning_frames = max(1, len(expanded_world))
    movement_start = planning_frames + 1
    total_frames = movement_start + max_steps

    figure, (info_ax, map_ax) = plt.subplots(
        1, 2, figsize=(15, 8), gridspec_kw={"width_ratios": (1, 3)}
    )
    figure.subplots_adjust(bottom=0.13, right=0.82, wspace=0.08)
    info_ax.set_axis_off()
    info_ax.set_title("A* + DWA allapot")
    priority_text = info_ax.text(
        0.02, 0.95, "", va="top", family="monospace", fontsize=8
    )

    for row in range(grid_map.height + 1):
        map_ax.axhline(
            row * resolution,
            color="#78909c",
            linewidth=0.65,
            alpha=0.75,
            zorder=0,
        )
    for column in range(grid_map.width + 1):
        map_ax.axvline(
            column * resolution,
            color="#78909c",
            linewidth=0.65,
            alpha=0.75,
            zorder=0,
        )

    raw_obstacle_cells = set()
    vertical_column = min(10, width - 2)
    horizontal_row = min(12, height - 2)
    for row in range(2, max(2, height - 2)):
        if row not in range(7, 13):
            raw_obstacle_cells.add((row, vertical_column))
    for column in range(12, max(12, width - 2)):
        if column not in range(19, 25):
            raw_obstacle_cells.add((horizontal_row, column))

    inflation_rectangles = []
    for row in range(grid_map.height):
        for column in range(grid_map.width):
            if grid_map.grid[row][column] == 1:
                rect = Rectangle(
                    (column * resolution, row * resolution),
                    resolution,
                    resolution,
                    color="#455a64",
                    zorder=1,
                )
                map_ax.add_patch(rect)
                if (row, column) not in raw_obstacle_cells:
                    inflation_rectangles.append(rect)

    astar_world = list(planner.astar_path)
    astar_x, astar_y = zip(*astar_world)
    path_x, path_y = zip(*path_world)
    waypoint_x, waypoint_y = zip(*planner.waypoints)

    # 1. Bézier útvonal: zorder=4, de alpha=0.55-tel áttetsző, hogy ne takarja el az A*-ot
    map_ax.plot(
        path_x,
        path_y,
        "-",
        color="#2e7d32",
        linewidth=3.5,
        alpha=0.55,
        label="Bezier utvonal",
        zorder=4,
    )

# Vékony, finom szaggatott vonal apró csomóponti pontokkal a Bézier felett
    (astar_line,) = map_ax.plot(
        astar_x,
        astar_y,
        linestyle="--",
        dashes=(3, 2),        # Sűrűbb, rövidebb szaggatás a finomabb megjelenéshez
        marker="o",
        markersize=2.0,       # Apró, finom pontok
        color="#0a22a7",      # Élénk narancs a jó kontrasztért
        linewidth=1.0,        # Vékony vonalvastagság (korábbi 1.8 helyett)
        alpha=0.9,
        label="Eredeti A* racsutvonal",
        zorder=7,
    )
    astar_line.set_visible(show_original_astar)
    map_ax.scatter(
        waypoint_x,
        waypoint_y,
        s=14,
        color="#e53935",
        edgecolors="#bdef48",
        linewidths=0.5,
        label="Bezier DWA pontok",
        zorder=6,
    )
    explored = map_ax.scatter(
        [], [], s=18, color="#90caf9", alpha=0.45, label="A* vizsgalt cellak", zorder=3
    )
    current_cell = map_ax.scatter(
        [],
        [],
        s=110,
        color="#ff9800",
        edgecolors="#e65100",
        label="A* aktualis pont",
        zorder=5,
    )
    waypoint = map_ax.scatter(
        [],
        [],
        s=150,
        marker="*",
        color="#fdd835",
        edgecolors="#f57f17",
        label="DWA waypoint",
        zorder=7,
    )

    # Összes pálya és fékezési szakaszok az önlabos megjelenítés szerint
    unsafe_collection = LineCollection(
        [],
        colors="red",
        linewidths=0.8,
        alpha=0.25,
        zorder=4,
        label="Nem biztonsagos palya (piros)",
    )
    map_ax.add_collection(unsafe_collection)

    safe_collection = LineCollection(
        [],
        colors="gray",
        linewidths=0.8,
        alpha=0.25,
        zorder=4,
        label="Biztonsagos palya (szurke)",
    )
    map_ax.add_collection(safe_collection)

    brakes_collection = LineCollection(
        [],
        colors="red",
        linewidths=0.8,
        alpha=0.35,
        zorder=4,
        label="Fekezesi szakasz (palya vegen)",
    )
    map_ax.add_collection(brakes_collection)

    (best_line,) = map_ax.plot(
        [],
        [],
        color="lime",
        linewidth=3.5,
        label="Valasztott legjobb (lime)",
        zorder=8,
    )
    (best_brake_line,) = map_ax.plot(
        [],
        [],
        color="red",
        linewidth=2.5,
        linestyle="--",
        label="Valasztott fekezese",
        zorder=9,
    )

    robot = Circle(
        start,
        config.rob_radius,
        fill=False,
        color="#1565c0",
        linewidth=2,
        label="Robot",
        zorder=10,
    )
    map_ax.add_patch(robot)
    goal_patch = Circle(
        goal,
        config.rob_radius * 0.6,
        fill=False,
        color="#2e7d32",
        linewidth=2,
        label="Cel",
        zorder=6,
    )
    map_ax.add_patch(goal_patch)
    (trail_line,) = map_ax.plot(
        [start[0]],
        [start[1]],
        color="#1565c0",
        linewidth=2,
        label="Robot nyoma",
        zorder=4,
    )
    status = map_ax.text(
        0.02,
        0.98,
        "A* tervezes",
        transform=map_ax.transAxes,
        va="top",
        zorder=11,
    )

    all_obstacles = static_obstacles + dynamic_obstacles
    obstacle_patches = [
        Circle(
            (obstacle.x, obstacle.y),
            obstacle.radius,
            color="#d32f2f",
            alpha=0.65,
            zorder=5,
        )
        for obstacle in all_obstacles
    ]
    for patch in obstacle_patches:
        map_ax.add_patch(patch)

    map_ax.set_xlim(0, width * resolution)
    map_ax.set_ylim(0, height * resolution)
    map_ax.set_aspect("equal")
    map_ax.set_xlabel("x [m]")
    map_ax.set_ylabel("y [m]")
    map_ax.set_title("A* racs, DWA palyak es a palyak vegi fekezes")
    map_ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), fontsize=8)

    trail_x = [state.x]
    trail_y = [state.y]
    last_movement_frame = -1
    last_result = None

    def priority_description(frame):
        if frame >= len(astar_result["search_steps"]):
            return "A* kesz\n\nDWA fazis\nmozgo akadalyak"
        step = astar_result["search_steps"][frame]
        return (
            f"A* lepes: {frame + 1}\n"
            f"aktualis: {step['current']}\n\n"
            f"prioritas\npozicio       f\n"
            + "\n".join(
                f"{item['position']!s:12s} {item['f']:6.2f}"
                for item in step.get("priority_queue", [])[:8]
            )
        )

    def advance_robot_one_step():
        nonlocal last_result
        for obstacle in dynamic_obstacles:
            obstacle.move(config.dt)
        last_result = planner.plan_local(state, all_obstacles)
        best_pair = (
            last_result["best_pair"] if last_result is not None else None
        )
        if best_pair is None:
            update(state, config, 0.0, 0.0, config.dt)
        else:
            update(state, config, best_pair[2], best_pair[3], config.dt)
        trail_x.append(state.x)
        trail_y.append(state.y)

    def update_frame(frame):
        nonlocal last_movement_frame
        if frame < planning_frames:
            explored.set_offsets(expanded_world[: frame + 1])
            current_cell.set_offsets([expanded_world[frame]])
            waypoint.set_offsets([[math.nan, math.nan]])
            priority_text.set_text(priority_description(frame))
            status.set_text(f"A* tervezes: {frame + 1}/{planning_frames}")
            return

        if frame == movement_start - 1:
            for rect in inflation_rectangles:
                rect.set_visible(False)
            explored.set_offsets(expanded_world)
            current_cell.set_offsets([[math.nan, math.nan]])
            priority_text.set_text(
                priority_description(len(astar_result["search_steps"]))
            )
            status.set_text("A* kesz - DWA mozgas indul")
            return

        movement_frame = min(frame - movement_start, max_steps - 1)
        while last_movement_frame < movement_frame:
            advance_robot_one_step()
            last_movement_frame += 1

        if last_result is not None:
            active_waypoint = last_result["waypoint"]
            target = last_result["target"]
            best_pair = last_result.get("best_pair", None)
            all_pairs = last_result.get("all_pairs", [])
            waypoint.set_offsets([active_waypoint])
        else:
            active_waypoint = None
            target = None
            best_pair = None
            all_pairs = []

        (
            unsafe_p,
            unsafe_b,
            safe_p,
            safe_b,
            best_p,
            best_b,
        ) = compute_onlab_trajectories(
            state, config, all_pairs, best_pair, all_obstacles
        )

        unsafe_collection.set_segments(unsafe_p)
        safe_collection.set_segments(safe_p)
        brakes_collection.set_segments(unsafe_b + safe_b)

        best_line.set_data(best_p[0], best_p[1])
        best_brake_line.set_data(best_b[0], best_b[1])

        trail_line.set_data(trail_x, trail_y)
        robot.center = (state.x, state.y)
        for patch, obstacle in zip(obstacle_patches, all_obstacles):
            patch.center = (obstacle.x, obstacle.y)

        priority_text.set_text(
            f"DWA allapot\n"
            f"robot: ({state.x:.2f}, {state.y:.2f})\n"
            f"sebesseg: {state.v:.2f} m/s\n"
            f"osszes palya: {len(all_pairs)} db\n"
            f"veszelyes (piros): {len(unsafe_p)} db\n"
            f"biztonsagos (szurke): {len(safe_p)} db\n"
            f"waypointok: {len(planner.waypoints)}\n"
            f"aktualis: {active_waypoint}\n"
            f"DWA cel: {target}"
        )
        status.set_text(
            "Cel elerve"
            if planner.reached_goal(state)
            else f"DWA mozgas: {movement_frame + 1}/{max_steps}"
        )

    animation = FuncAnimation(
        figure,
        update_frame,
        frames=total_frames,
        interval=80,
        repeat=False,
        blit=False,
    )
    figure._simulation_animation = animation
    if show:
        plt.show(block=True)
    return figure, animation


def run_simulation():
    """Elinditja a beallitasi ablakot."""
    window = tk.Tk()
    window.title("A* + DWA beallitasok")
    window.resizable(False, False)
    frame = ttk.Frame(window, padding=16)
    frame.grid()
    fields = {
        "width": ("Szelesseg cellaban", "30"),
        "height": ("Magassag cellaban", "20"),
        "resolution": ("Felbontas [m]", "0.2"),
        "start": ("Start (sor,oszlop)", "2,2"),
        "goal": ("Cel (sor,oszlop)", "17,27"),
        "inflation": ("Akadalyinflacio [m]", "0.11"),
        "alpha": ("Alfa - iranykovetes", "5"),
        "beta": ("Beta - akadalybiztonsag", "2"),
        "gamma": ("Gamma - sebesseg", "3"),
    }
    entries = {}
    for row, (name, (label, value)) in enumerate(fields.items()):
        ttk.Label(frame, text=label).grid(
            row=row, column=0, sticky="w", padx=(0, 12), pady=4
        )
        entry = ttk.Entry(frame, width=18)
        entry.insert(0, value)
        entry.grid(row=row, column=1, pady=4)
        entries[name] = entry

    diagonal = tk.BooleanVar(value=True)
    smooth = tk.BooleanVar(value=True)
    waypoint_slowdown = tk.BooleanVar(value=False)
    show_original_astar = tk.BooleanVar(value=False)
    heuristic = tk.StringVar(value="euclidean")

    tk.Checkbutton(frame, text="Atlos mozgas", variable=diagonal).grid(
        row=9, column=0, columnspan=2, sticky="w"
    )
    tk.Checkbutton(frame, text="Bezier utvonal simitasa", variable=smooth).grid(
        row=10, column=0, columnspan=2, sticky="w"
    )
    tk.Checkbutton(
        frame, text="Waypoint lassitas", variable=waypoint_slowdown
    ).grid(row=11, column=0, columnspan=2, sticky="w")
    tk.Checkbutton(
        frame, text="Eredeti A* utvonal", variable=show_original_astar
    ).grid(row=12, column=0, columnspan=2, sticky="w")
    tk.Label(frame, text="A* heurisztika").grid(
        row=13, column=0, sticky="w", pady=4
    )
    heuristic_box = ttk.Combobox(
        frame,
        textvariable=heuristic,
        values=("manhattan", "euclidean", "chebyshev", "octile"),
        state="readonly",
        width=16,
    )
    heuristic_box.grid(row=13, column=1, pady=4)

    def start():
        try:
            settings = {name: entry.get() for name, entry in entries.items()}
            width = int(settings["width"])
            height = int(settings["height"])
            resolution = float(settings["resolution"])
            inflation = float(settings["inflation"])
            alpha = float(settings["alpha"])
            beta = float(settings["beta"])
            gamma = float(settings["gamma"])
            start_cell = parse_cell(settings["start"])
            goal_cell = parse_cell(settings["goal"])
            if not (width > 2 and height > 2 and resolution > 0 and inflation >= 0):
                raise ValueError(
                    "A terkep merete es a felbontas legyen pozitiv."
                )
            if min(alpha, beta, gamma) < 0 or alpha + beta + gamma == 0:
                raise ValueError(
                    "A sullyok legyenek nem negativak, es legalabb egy legyen pozitiv."
                )
            if not (0 <= start_cell[0] < height and 0 <= start_cell[1] < width):
                raise ValueError("A start legyen a terkepen belul.")
            if not (0 <= goal_cell[0] < height and 0 <= goal_cell[1] < width):
                raise ValueError("A cel legyen a terkepen belul.")
            window.destroy()
            create_simulation(
                width,
                height,
                resolution,
                start_cell,
                goal_cell,
                diagonal.get(),
                heuristic.get(),
                inflation,
                smooth=smooth.get(),
                alpha=alpha,
                beta=beta,
                gamma=gamma,
                waypoint_slowdown=waypoint_slowdown.get(),
                show_original_astar=show_original_astar.get(),
                auto_play=True,
                show=True,
            )
        except (TypeError, ValueError, RuntimeError) as error:
            messagebox.showerror("Hibas beallitas", str(error), parent=window)

    tk.Button(frame, text="Szimulacio inditasa", command=start).grid(
        row=14, column=0, columnspan=2, sticky="ew", pady=(12, 0)
    )
    window.mainloop()


if __name__ == "__main__":
    run_simulation()
````````

### `Projekt/Python_szimulacio/codes_diploma/sulyvizsgalat/dwa_weight_sweep.csv`

````````csv
scenario,alpha,beta,gamma,predict_time,safety_margin,reached,sim_time_s,path_m,avg_speed_mps,min_clearance_m,collision_steps,collision,no_command_steps
S1,2,0,1,3,0.15,True,23.9,6.18,0.259,-0.268,15,True,51
S1,2,0,3,3,0.15,True,23.6,6.18,0.262,-0.274,26,True,52
S1,2,0,5,3,0.15,True,23.5,6.26,0.266,-0.273,20,True,52
S1,2,2,1,3,0.15,True,25.2,6.49,0.258,0.075,0,False,12
S1,2,2,3,3,0.15,True,27.3,9.45,0.346,0.025,0,False,0
S1,2,2,5,3,0.15,False,40.0,17.43,0.436,0.024,0,False,0
S1,2,6,1,3,0.15,True,25.2,6.49,0.258,0.075,0,False,12
S1,2,6,3,3,0.15,True,27.3,9.45,0.346,0.025,0,False,0
S1,2,6,5,3,0.15,False,40.0,17.43,0.436,0.024,0,False,0
S1,5,0,1,3,0.15,True,24.5,6.17,0.252,-0.275,16,True,50
S1,5,0,3,3,0.15,True,23.7,6.18,0.261,-0.268,15,True,51
S1,5,0,5,3,0.15,True,23.7,6.18,0.261,-0.266,18,True,52
S1,5,2,1,3,0.15,True,27.4,6.45,0.235,0.077,0,False,12
S1,5,2,3,2,0.15,True,25.6,6.27,0.245,-0.216,35,True,51
S1,5,2,3,3,0.1,True,24.9,6.4,0.257,0.028,0,False,11
S1,5,2,3,3,0.15,True,25.6,6.48,0.253,0.108,0,False,10
S1,5,2,3,3,0.2,True,25.7,6.65,0.259,0.119,0,False,12
S1,5,2,3,3,0.25,True,28.2,6.71,0.238,0.05,0,False,56
S1,5,2,3,4,0.15,True,24.0,6.49,0.27,0.126,0,False,6
S1,5,2,5,3,0.15,True,25.4,6.66,0.262,-0.05,16,True,46
S1,5,6,1,3,0.15,True,27.4,6.45,0.235,0.077,0,False,12
S1,5,6,3,3,0.15,True,25.6,6.48,0.253,0.108,0,False,10
S1,5,6,5,3,0.15,True,25.4,6.66,0.262,-0.05,16,True,46
S1,8,0,1,3,0.15,True,24.5,6.17,0.252,-0.269,15,True,45
S1,8,0,3,3,0.15,True,24.0,6.17,0.257,-0.261,20,True,51
S1,8,0,5,3,0.15,True,23.8,6.18,0.26,-0.273,16,True,51
S1,8,2,1,3,0.15,True,27.3,6.53,0.239,0.085,0,False,11
S1,8,2,3,3,0.15,True,27.1,6.46,0.238,0.062,0,False,14
S1,8,2,5,3,0.15,True,25.2,6.51,0.258,0.067,0,False,12
S1,8,6,1,3,0.15,True,27.3,6.53,0.239,0.085,0,False,11
S1,8,6,3,3,0.15,True,27.1,6.46,0.238,0.062,0,False,14
S1,8,6,5,3,0.15,True,25.2,6.51,0.258,0.067,0,False,12
S2,2,0,1,3,0.15,True,25.8,6.18,0.24,-0.27,18,True,68
S2,2,0,3,3,0.15,True,25.6,6.18,0.241,-0.28,30,True,71
S2,2,0,5,3,0.15,True,25.5,6.26,0.245,-0.273,23,True,71
S2,2,2,1,3,0.15,True,25.7,6.51,0.253,0.069,0,False,13
S2,2,2,3,3,0.15,True,25.8,7.64,0.296,-0.222,20,True,27
S2,2,2,5,3,0.15,False,40.0,16.5,0.413,0.027,0,False,0
S2,2,6,1,3,0.15,True,25.7,6.51,0.253,0.069,0,False,13
S2,2,6,3,3,0.15,True,25.9,8.51,0.329,0.013,0,False,6
S2,2,6,5,3,0.15,False,40.0,16.5,0.413,0.027,0,False,0
S2,5,0,1,3,0.15,True,26.2,6.17,0.236,-0.272,18,True,66
S2,5,0,3,3,0.15,True,25.8,6.18,0.24,-0.271,18,True,68
S2,5,0,5,3,0.15,True,25.5,6.18,0.242,-0.269,21,True,69
S2,5,2,1,3,0.15,True,27.5,6.48,0.236,0.098,0,False,11
S2,5,2,3,2,0.15,True,26.6,6.49,0.244,-0.077,20,True,54
S2,5,2,3,3,0.1,True,25.1,6.47,0.258,0.053,0,False,9
S2,5,2,3,3,0.15,True,25.4,6.46,0.254,0.05,0,False,12
S2,5,2,3,3,0.2,True,26.7,6.45,0.241,0.034,0,False,20
S2,5,2,3,3,0.25,True,28.2,6.71,0.238,0.05,0,False,56
S2,5,2,3,4,0.15,True,24.9,6.51,0.262,0.132,0,False,5
S2,5,2,5,3,0.15,True,25.0,6.58,0.263,-0.05,16,True,47
S2,5,6,1,3,0.15,True,27.5,6.48,0.236,0.098,0,False,11
S2,5,6,3,3,0.15,True,25.4,6.46,0.254,0.05,0,False,12
S2,5,6,5,3,0.15,True,25.0,6.58,0.263,-0.05,16,True,47
S2,8,0,1,3,0.15,True,26.4,6.17,0.234,-0.275,20,True,63
S2,8,0,3,3,0.15,True,25.7,6.18,0.24,-0.275,24,True,66
S2,8,0,5,3,0.15,True,25.9,6.18,0.239,-0.276,21,True,70
S2,8,2,1,3,0.15,True,27.5,6.53,0.237,0.089,0,False,11
S2,8,2,3,3,0.15,True,27.1,6.45,0.238,0.074,0,False,13
S2,8,2,5,3,0.15,True,25.5,6.47,0.254,0.048,0,False,13
S2,8,6,1,3,0.15,True,27.5,6.53,0.237,0.089,0,False,11
S2,8,6,3,3,0.15,True,27.1,6.45,0.238,0.074,0,False,13
S2,8,6,5,3,0.15,True,25.5,6.47,0.254,0.048,0,False,13
````````

### `Projekt/Python_szimulacio/codes_diploma/sulyvizsgalat/dwa_weight_sweep.py`

````````python
"""DWA parameter-sweep a Python szimulacios kornyezeten (headless).

Az ido a SZIMULALT ido (lepesszam * dt), ezert nem fugg a gep sebessegetol.
Futtatas (a Python_szimulacio mappabol): python codes_diploma/sulyvizsgalat/dwa_weight_sweep.py [probe]
"""
import csv
import math
import os
import sys
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import matplotlib

matplotlib.use("Agg")

from codes_diploma.astar_project.astar_variants import get_heuristic
from codes_diploma.robot import Obstacle, robotconfig, update
from codes_diploma.simulation import create_scene, load_planner_class

OUT_DIR = Path(__file__).resolve().parent
MAX_STEPS = 400  # 40 s szimulalt ido

# S1: az alap pálya, szembejövő mozgó akadály; S2: ehhez egy keresztező akadály is
SCENARIOS = {
    "S1": [],
    "S2": [(3.4, 0.2, 0.0, 0.14)],
}


def run_case(args):
    scenario, params = args
    (grid_map, _, _, start, goal, state, statics, dynamics) = create_scene(
        30, 20, 0.2, (2, 2), (17, 27), 0.1
    )
    for x, y, vx, vy in SCENARIOS[scenario]:
        dynamics.append(Obstacle(x, y, radius=0.18, vx=vx, vy=vy))
    config = robotconfig()
    config.Alfa, config.Beta, config.Gamma = params["alpha"], params["beta"], params["gamma"]
    config.predict_time = params["predict_time"]
    config.safety_margin = params["safety_margin"]
    planner = load_planner_class()(grid_map, config=config, diagonal=True)
    planner.plan_global(start, goal, heuristic=get_heuristic("euclidean"),
                        smooth=True, samples_per_curve=8)
    obstacles = statics + dynamics
    length, min_clear, collisions, no_command = 0.0, math.inf, 0, 0
    previous = (state.x, state.y)
    reached = False
    for step in range(MAX_STEPS):
        for obstacle in dynamics:
            obstacle.move(config.dt)
        result = planner.plan_local(state, obstacles)
        best = result["best_pair"] if result is not None else None
        if best is None:
            no_command += 1
            update(state, config, 0.0, 0.0, config.dt)
        else:
            update(state, config, best[2], best[3], config.dt)
        length += math.hypot(state.x - previous[0], state.y - previous[1])
        previous = (state.x, state.y)
        clearance = min(math.hypot(state.x - o.x, state.y - o.y) - o.radius - config.rob_radius
                        for o in obstacles)
        min_clear = min(min_clear, clearance)
        if clearance < 0:
            collisions += 1
        if planner.reached_goal(state):
            reached = True
            break
    sim_time = (step + 1) * config.dt
    return {
        "scenario": scenario, **params, "reached": reached,
        "sim_time_s": round(sim_time, 1), "path_m": round(length, 2),
        "avg_speed_mps": round(length / sim_time, 3),
        "min_clearance_m": round(min_clear, 3), "collision_steps": collisions,
        "collision": collisions > 0, "no_command_steps": no_command,
    }


BASE = {"alpha": 5, "beta": 2, "gamma": 3, "predict_time": 3, "safety_margin": 0.15}


def build_jobs():
    jobs = []
    for scenario in SCENARIOS:
        for a in (2, 5, 8):
            for b in (0, 2, 6):
                for g in (1, 3, 5):
                    jobs.append((scenario, {**BASE, "alpha": a, "beta": b, "gamma": g}))
        for predict_time in (2, 4):
            jobs.append((scenario, {**BASE, "predict_time": predict_time}))
        for margin in (0.10, 0.20, 0.25):
            jobs.append((scenario, {**BASE, "safety_margin": margin}))
    return jobs


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "probe":
        jobs = [(s, {**BASE, "beta": b}) for s in SCENARIOS for b in (0, 20)]
    else:
        jobs = build_jobs()
    print(len(jobs), "eset", flush=True)
    OUT_DIR.mkdir(exist_ok=True)
    rows = []
    with Pool(max(1, (os.cpu_count() or 2) - 1)) as pool:
        for row in pool.imap_unordered(run_case, jobs):
            rows.append(row)
            print(row, flush=True)
    rows.sort(key=lambda r: (r["scenario"], r["alpha"], r["beta"], r["gamma"],
                             r["predict_time"], r["safety_margin"]))
    name = "probe.csv" if len(sys.argv) > 1 else "dwa_weight_sweep.csv"
    with open(OUT_DIR / name, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
````````

### `Projekt/Python_szimulacio/README.md`

````````markdown
# Python 2D szimuláció (A* + DWA)

Matematikai (nem ROS-os) szimuláció: az A* tervezi az utat, a DWA vezeti a robotot, a mozgó akadályokat kikerülve. Python 3, a `numpy` és a `matplotlib` kell hozzá (a grafikus ablakhoz `tkinter`).

## Mappák
```
Python_szimulacio/
└── codes_diploma/
    ├── simulation.py        indító és animáció
    ├── DWA+A.py             A* és DWA összekapcsolása (waypointok)
    ├── DWA.py               DWA algoritmus (pontozás)
    ├── robot.py             robotmodell és paraméterek
    ├── astar_project/       A* keresés, heurisztikák, rácstérkép, útvonalsimítás
    └── sulyvizsgalat/       DWA súlyvizsgálat (szkript + eredmény CSV)
```

## Indítás
Terminálban (PowerShell), ebből a mappából (`Python_szimulacio`):
```
cd "<útvonal>\Projekt\Python_szimulacio"
pip install numpy matplotlib
$env:PYTHONIOENCODING="utf-8"
python -m codes_diploma.simulation
```
1. Először egy **„A* + DWA beallitasok"** ablak jelenik meg (méret, start, cél, α/β/γ súlyok). Ez a tálcán/más ablak mögött is lehet.
2. Az alapértékek jók, kattints a **„Szimulacio inditasa"** gombra.
3. Megnyílik az animáció (A* útvonal, DWA pályák, mozgó akadályok), és automatikusan lejátszik.

Az ablak bezárásával a program leáll.

## Súlyvizsgálat (opcionális, ~1,5 óra)
```
python codes_diploma\sulyvizsgalat\dwa_weight_sweep.py
```
Az eredmény a `codes_diploma\sulyvizsgalat\dwa_weight_sweep.csv` fájlba kerül.
````````

### `Projekt/README.md`

````````markdown
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
````````
