# Diplomamunka és kód teljes összevetése

**Ellenőrzés dátuma:** 2026-11-06
**Összevetett dolgozat:** `Rum Dániel Diplomamunka.docx`  
**Összevetett kód:** `codes_diploma/` Python-projektje és a `ros2_astar_dwa_gazebo/` forráscsomagja

## 1. Rövid összesítés

A dolgozat és a kód több fontos ponton egyezik: a rácsos A* keresés, a `resolution` alapú koordináta-átalakítás, a Bézier-útvonalsimítás, a Pythonos DWA, a differenciálhajtású robotmodell, valamint az A* + DWA szimuláció ténylegesen megtalálható a projektben.

A dolgozat azonban jelen állapotában nem tekinthető teljesen kódhűnek. A legfontosabb eltérések:

- a megvalósított Python A* klasszikus A*, nem az összes dolgozatban vagy háttéranyagban említett továbbfejlesztett A* vagy SBA*;
- a mérési és benchmark-eredményekhez nem található kész mérési futtató, metrikagyűjtés vagy eredményfájl;
- a robotkinematikai fejezetből hiányzik a keréksebesség gyorsuláskorlátozása;
- a robotkinematikai (31) és (32) képleteknél a deriváltjelölés szükséges;
- a Pythonos referencia-szimuláció és a C++ ROS2/Gazebo vezérlő két külön megvalósítás; az egyik viselkedése nem bizonyítja automatikusan a másikét;
- a dokumentumban szereplő algoritmusneveket és mérési számokat csak akkor szabad saját megvalósításként vagy saját eredményként bemutatni, ha külön kóddal és reprodukálható futással is igazolhatók.

## 2. Státuszjelölések

| Státusz | Jelentés |
|---|---|
| **Egyezik** | A dolgozat állítása és a jelenlegi kód közvetlenül összhangban van. |
| **Részben egyezik** | Az alapötlet vagy a fő működés létezik, de a dolgozat túl tág, más paramétert használ, vagy fontos korlátozást nem említ. |
| **Eltér** | A dolgozat konkrét állítása nem felel meg a tényleges implementációnak. |
| **Nincs implementálva** | A dolgozatban vagy a projekttervben szereplő elemhez nem található működő kód. |
| **Nem igazolható** | A dolgozat állítása mérési eredményre vagy külső bizonyítékra hivatkozik, de ehhez nincs reprodukálható helyi futtatás vagy eredményfájl. |

## 3. Rácstérkép és koordináták

| Dolgozati állítás vagy témakör | Kód bizonyítéka | Státusz | Szükséges teendő |
|---|---|---|---|
| A környezet cellákból álló rácstérkép. | [`grid_map.py`](codes_diploma/astar_project/grid_map.py): `GridMap`, `grid`, `width`, `height`. | **Egyezik** | Nincs alapvető javítás. |
| A `resolution` a cella fizikai mérete. | [`grid_map.py`](codes_diploma/astar_project/grid_map.py): `world_to_grid()` és `grid_to_world()`. | **Egyezik** | Írd le, hogy a `grid_to_world()` a cellaközéppontot adja vissza. |
| A világkoordináta és rácskoordináta között átalakítás történik. | `world_to_grid()` `floor()`-t használ, `grid_to_world()` pedig `(column + 0.5) * resolution` és `(row + 0.5) * resolution` alakot. | **Egyezik** | A sor–oszlop sorrendet külön jelöld: `(row, column)`, világban `(x, y)`. |
| Az akadályok inflációval figyelembe veszik a robot méretét. | `GridMap.inflate_obstacles(radius)` cellákra kerekített biztonsági zónát készít. | **Részben egyezik** | Ne írd pontos körgeometriának: a jelenlegi megoldás cellaalapú, négyzetes kiterjesztést alkalmaz. |
| Diagonális mozgásnál nincs sarokvágás akadály mellett. | `get_neighbors()` csak akkor enged átlós cellát, ha a két ortogonális szomszéd is szabad. | **Egyezik** | Nincs alapvető javítás. |
| Ismeretlen cellák kezelése szerepelhet a térképen. | `GridMap(unknown=True)` kezdeti értéke `2`, de az A* csak `grid == 0` cellát tekint szabadnak. | **Részben egyezik** | A dolgozatban tisztázd, hogy az ismeretlen cella jelenleg nem járható, nem külön SLAM- vagy bizonytalansági modell. |

## 4. Klasszikus A*

| Dolgozati állítás vagy témakör | Kód bizonyítéka | Státusz | Szükséges teendő |
|---|---|---|---|
| Az A* költségfüggvénye `f(n) = g(n) + h(n)`. | [`astar_baseline.py`](codes_diploma/astar_project/astar_baseline.py): `f_cost = new_g_cost + h_cost`. | **Egyezik** | Nincs javítás. |
| A keresés a legkisebb `f` értékű csomópontot választja. | `open_list` lista, `min(open_list)`. | **Egyezik** | A dolgozatban ne prioritási kupacként írd, mert a kód egyszerű listát használ. |
| A mozgási költség egyenes lépésnél 1, átlónál `sqrt(2)`. | `_movement_cost()` euklideszi cellaköltséget számít. | **Egyezik** | Nincs javítás. |
| 4- és 8-szomszédos keresés támogatott. | `astar_search(..., diagonal=False/True)` és `GridMap.get_neighbors()`. | **Egyezik** | Nincs javítás. |
| Az alapértelmezett heurisztika 4-szomszédnál Manhattan, átlós keresésnél Euklideszi. | `_heuristic()` az átadott `diagonal` alapján választ. | **Egyezik** | Írd hozzá, hogy egyedi heurisztika függvény is átadható. |
| Manhattan, Euklideszi, Chebyshev és Octile heurisztika működik. | [`astar_variants.py`](codes_diploma/astar_project/astar_variants.py): mind a négy függvény és `get_heuristic()`. | **Egyezik** | Az egyes heurisztikák alkalmazási feltételét pontosítsd. |
| Az A* továbbfejlesztett, dinamikusan súlyozott heurisztikát használ. | A jelenlegi `astar_baseline.py` nem tartalmaz dinamikus súlyozást; csak átadott heurisztikát hív. | **Eltér** | Ha ilyen állítás szerepel a dolgozatban, nevezd jövőbeli vagy tervezett fejlesztésnek, vagy implementáld és teszteld külön. |
| 5-szomszédságú A* működik. | A kódban 4 vagy 8 irány van, ötödik irány nincs. | **Nincs implementálva** | A dolgozatból törlendő saját implementációként, vagy külön meg kell valósítani. |
| EA*, EBA*, EBHA*, EBHSA* változatok működnek. | Az `astar_variants.py` csak heurisztikákat tartalmaz, ilyen keresőváltozatokat nem. | **Nincs implementálva** | A dolgozatban csak irodalmi háttérként vagy jövőbeli munkaként szerepeljen. |
| Az A* hibás start- vagy célcella esetén hibát jelez, elérhetetlen cél esetén `None`-t ad. | `astar_search()` `ValueError`-t dob érvénytelen vagy foglalt végpontnál; sikertelen keresésnél `None` vagy részletes szótár tér vissza. | **Egyezik** | Nincs javítás. |

## 5. Útvonalsimítás és waypointok

| Dolgozati állítás vagy témakör | Kód bizonyítéka | Státusz | Szükséges teendő |
|---|---|---|---|
| Az A* törött vonalas útvonala simítható. | [`path_smoothing.py`](codes_diploma/astar_project/path_smoothing.py), `smooth_path_bezier()`. | **Egyezik** | Ne általános „optimális simításként”, hanem Bézier-alapú geometriai utófeldolgozásként nevezd. |
| Másodfokú Bézier-görbe készül. | `_bezier_point()` képlete és `bezier_curve_points()`. | **Egyezik** | Nincs alapvető javítás. |
| Az egyenes szakasz köztes pontjai eltávolíthatók. | `_remove_straight_points()` kereszt-szorzattal azonosítja a kanyarokat. | **Egyezik** | Nincs javítás. |
| A simított görbe akadálybiztos. | `_is_path_safe()` a pontokat cellákra kerekíti, majd szabad cellát és megengedett szomszédságot ellenőriz. | **Részben egyezik** | Írd le, hogy a biztonsági ellenőrzés diszkrét, kerekített cellákon történik, nem folytonos geometriai görbe–akadály metszésvizsgálattal. |
| A sarokvágás alapértéke legfeljebb egy teljes cella vagy `3 * resolution`. | `smooth_path_bezier()` és `AStarDWAPlanner.plan_global()` alapértéke `0.5 * grid_map.resolution`. | **Eltér** | A dolgozatban a tényleges alapértéket, `0.5 * resolution`-t használd. |
| A görbe irányváltását a kód elutasítja. | `_has_direction_reversal()` és az eredeti útvonalra visszaállás. | **Egyezik** | Nincs javítás. |
| A simítás biztosan lerövidíti vagy optimalizálja az utat. | A kód csak simít, nem számol összehasonlító útminőségi optimumot. | **Nem igazolható** | „Simább” vagy „folytonosabb” útvonalként írd, ne bizonyítottan optimális vagy rövidebb útvonalként. |
| A simított útból egyenletes waypointlánc készül. | [`DWA+A.py`](codes_diploma/DWA+A.py): `_create_waypoints()` `0.2 m` alapértelmezett ívhossz-lépéssel. | **Egyezik** | A waypointot különítsd el a Bézier-mintaponttól. |

## 6. DWA és differenciálhajtású robotmodell

| Dolgozati állítás vagy témakör | Kód bizonyítéka | Státusz | Szükséges teendő |
|---|---|---|---|
| A DWA sebességpárokat dinamikus ablakban keresi. | [`DWA.py`](codes_diploma/DWA.py): `pairstochoose()` az aktuális keréksebesség körüli gyorsulási ablakból mintavételez. | **Egyezik** | A dolgozatban jelezd, hogy a mintavétel kerék-szögsebességpárokon történik. |
| A kerék kerületi sebessége `v_L = r * omega_L`, `v_R = r * omega_R`. | [`robot.py`](codes_diploma/robot.py): `get_robot_kinematics()`. | **Egyezik** | Nincs javítás. |
| A robot lineáris sebessége a két keréksebesség átlaga. | `v = ((w_L + w_R) / 2) * r_kerek`. | **Egyezik** | Nincs javítás. |
| A robot szögsebessége `omega = (v_R - v_L) / (2b)`. | Kódban `w = ((w_R - w_L) / (2 * config.b)) * config.r_kerek`; `b = 0.08 m`. | **Egyezik** | `2b` legyen a teljes keréktávolság, `b` a fél tengelytáv. |
| A (31)–(32) összefüggések a pozíció sebességkomponensei. | A dolgozatban a deriváltjel hiányzik; a kód állapotot frissít. | **Részben egyezik** | Használd: `dot{x} = v cos(theta)`, `dot{y} = v sin(theta)`. |
| Egyenes haladásnál a robot az aktuális irány mentén mozdul. | `update()` $ w == 0 ` ág: `x += v*cos(theta)*dt`, `y += v*sin(theta)*dt`. | **Egyezik** | Megjegyzendő a kódban használt `abs(w) <= 1e-6` küszöb. |
| Íves mozgásnál köríves integrálás történik. | `update()` $ abs(w) > 1e-6 ` ág zárt alakú szinuszos/koszinuszos képleteket használ. | **Egyezik** | „Numerikus integrálás” helyett „zárt alakú köríves integrálás” a pontosabb megfogalmazás. |
| A célzott keréksebesség közvetlenül megvalósul. | `update()` előbb `np.clip()`-pel korlátozza a kerék-szögsebesség változását. | **Eltér** | A dolgozatba vedd fel: `max_w_dot = a_max / r_kerek`, majd a célérték korlátozása. |
| A robotparaméterek a dolgozatban szereplő értékek. | `robotconfig()`: `r_kerek=0.033`, `b=0.08`, `w_kerek_max=15`, `a_max=2`, `dt=0.1`, `predict_time=3`. | **Egyezik** | Ezeket a mértékegységekkel együtt add meg. |
| A DWA tetszőleges hátramenetet használhat. | `allow_reverse=False`; a negatív `v` értékű párokat a DWA kihagyja. | **Részben egyezik** | A dolgozatban írd le, hogy a jelenlegi alapbeállítás előremenetet enged. |
| A DWA ütközésvizsgálata a mozgó akadály jövőbeli pozícióját is figyelembe veszi. | `get_dist_on_trajectory()` `x + vx*t`, `y + vy*t` alapján ellenőriz. | **Egyezik** | Írd hozzá a 3 m-es érzékelési távolságot és 180 fokos elülső látómezőt. |
| A megállási feltétel `|v| <= sqrt(2*a_max*d)`. | `AdmissableVelocity()` ezt a feltételt használja. | **Egyezik** | Nincs javítás. |
| A DWA súlyai a szakirodalmi értékek. | A Python `robotconfig()` alapértékei `Alfa=5`, `Beta=2`, `Gamma=3`; a jelenlegi kód nem a háttéranyagban szereplő `15,37,0.02` értékeket használja. | **Eltér** | A dolgozatban a tényleges kísérleti konfigurációt add meg, vagy nevezd külön szakirodalmi összehasonlításnak. |

## 7. A* + DWA Python-szimuláció

| Dolgozati állítás vagy témakör | Kód bizonyítéka | Státusz | Szükséges teendő |
|---|---|---|---|
| A globális A* és lokális DWA együttműködik. | [`DWA+A.py`](codes_diploma/DWA+A.py): `plan_global()` A*-t futtat, `plan_local()` DWA-parancsot választ. | **Egyezik** | Nincs alapvető javítás. |
| Az A* statikus térképen dolgozik, a DWA kezeli a lokális akadályokat. | [`simulation.py`](codes_diploma/simulation.py): statikus falak a `GridMap`-ben, külön mozgó akadálylista a DWA-hoz. | **Egyezik** | A globális térkép dinamikus újratervezésének hiányát említsd meg. |
| A waypointok követése adaptív előretekintést használ. | `DWA+A.py`: `_update_pruned_lookahead_target()`, `0.35–0.80 m` közé szorított lookahead. | **Egyezik** | A pontos határokat add meg, ne általános „adaptív” állítás maradjon. |
| A végső cél elérése fix, minden helyzetben azonos tolerancia. | `reached_goal()` és `_current_tolerance()` dinamikusan `0.05–0.2 m` között számol. | **Eltér** | A dolgozatban dinamikus toleranciát írj. |
| A rendszer globálisan újratervez, ha mozgó akadály kerül az útra. | A `plan_local()` az aktuális útvonal waypointjait követi; új A* keresés nincs minden akadálymozgás után. | **Nincs implementálva** | Ne állíts globális dinamikus újratervezést, csak lokális DWA-elkerülést. |
| A szimuláció megjeleníti a biztonságos és veszélyes pályákat, valamint a fékezési szakaszokat. | `simulation.py`: `compute_onlab_trajectories()` és Matplotlib `LineCollection` objektumok. | **Egyezik** | Nincs javítás. |
| A simítás alapértelmezett vágása `0.5 * resolution`. | `AStarDWAPlanner.plan_global()` és `smooth_path_bezier()`. | **Egyezik** | Nincs javítás. |

## 8. Tisztán A*-os szimuláció

| Dolgozati állítás vagy témakör | Kód bizonyítéka | Státusz | Szükséges teendő |
|---|---|---|---|
| Az A* demonstráció statikus térképen fut. | [`astar_simulation.py`](codes_diploma/astar_project/astar_simulation.py): `create_demo_map()`, `plot_simulation()`. | **Egyezik** | Nincs javítás. |
| Ez a demonstráció teljes fizikai robotmodellt használ. | A modul a cellaútvonalból interpolált vagy Bézier-pontokat készít; nem hívja a `robot.update()` kinematikai frissítését. | **Eltér** | A dolgozatban különítsd el az A* vizualizációt az A* + DWA fizikai szimulációtól. |
| A tisztán A*-os modul sebességet, gyorsulást és mozgó akadályt vizsgál. | A `create_robot_trajectory()` csak geometriai pontokat generál. | **Nincs implementálva** | Ezt ne tulajdonítsd az `astar_simulation.py` modulnak. |

## 9. Mérési rendszer és eredmények

| Dolgozati állítás vagy témakör | Kód bizonyítéka | Státusz | Szükséges teendő |
|---|---|---|---|
| A projekt automatikusan útvonalhosszt, kanyarszámot és futási időt mér. | [`metrics.py`](codes_diploma/astar_project/metrics.py) jelenleg csak moduldokumentációt tartalmaz. | **Nincs implementálva** | A dolgozat mérési módszerét vagy kódoldalon kell megvalósítani, vagy kézi/előzetes eredményként kell jelölni. |
| A projekt több forgatókönyvet automatikusan lefuttat. | [`experiments.py`](codes_diploma/astar_project/experiments.py) jelenleg nem tartalmaz futtatási logikát. | **Nincs implementálva** | Ne állíts automatikus paraméter-söprést. |
| A parancssori kísérletfuttató kész. | [`run_experiment.py`](codes_diploma/astar_project/run_experiment.py) explicit módon `Experiment runner is not implemented yet.` üzenettel áll le. | **Eltér** | A dolgozatban kész mérési infrastruktúraként nem szerepelhet. |
| A mérési eredmények reprodukálhatók a `results` mappából. | A `results/raw`, `figures`, `tables` mappákban nincs futtatott eredményadatokra utaló kész eredménykészlet. | **Nem igazolható** | A dolgozatban minden számhoz add meg a futtató szkriptet, paramétereket és eredményfájlt. |
| A tudásbázisban szereplő benchmarkok saját kísérleti eredmények. | [`tudasbazis.MD`](codes_diploma/tudasbazis.MD) irodalmi/tervezési háttérszöveg; a helyi mérési pipeline hiányzik. | **Nem igazolható** | A `-6.24%`, `-75%`, idő- és útvonalhosszértékeket ne nevezd saját mérésnek bizonyíték nélkül. |

## 10. ROS2 és Gazebo

| Dolgozati állítás vagy témakör | Kód bizonyítéka | Státusz | Szükséges teendő |
|---|---|---|---|
| ROS2 + Gazebo szimuláció TurtleBot3 Waffle robottal működik. | [`dwa_world.sdf`](codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/worlds/dwa_world.sdf), launch- és csomagfájlok. | **Egyezik** | A futtatási környezetet, ROS2-disztribúciót és Gazebo-verziót pontosítsd. |
| A ROS2-ben A* globális útvonal és DWA lokális vezérlés működik. | Az alapértelmezett `cpp-rethink` launch a C++ [`astar_dwa_node.cpp`](codes_diploma/ros2_astar_dwa_gazebo/src/astar_dwa_controller/src/astar_dwa_node.cpp) node-ot indítja. | **Részben egyezik** | A Python Matplotlib-szimuláció és a C++ ROS2/Gazebo vezérlő külön implementáció; viselkedésazonosságuk nincs igazolva. |
| A ROS2-es DWA a Python DWA teljes változata. | A C++ node saját keréksebesség-mintavételezést és pontozást tartalmaz. | **Eltér** | A Python-algoritmust és C++ ROS2-megvalósítást külön rendszerként írd le; a C++ nem közvetlen Python-port. |
| A LiDAR-adatok alapján lokális akadálytérkép készül. | A C++ `obstacles()` a `/scan` pontokat világkoordinátára alakítja és a DWA lokális ütközésvizsgálatának adja; a statikus A* rácsot a `rosbot.yaml` pontlistái adják. | **Eltér** | Ne írd, hogy a LiDAR frissíti a globális A* térképet: az aktuális C++ launchban a LiDAR a lokális DWA-bemenet. |
| A mozgó akadályt a globális A* elkerüli. | `moving_obstacle_node.py` mozgatja az akadályt, de a statikus globális térkép nem minden ciklusban tervez újra. | **Nincs implementálva** | Lokális akadályelkerülésként írd le, ne globális dinamikus újratervezésként. |
| A ROS2/Gazebo futásból mérési eredmények származnak. | Forráskód és launch fájlok vannak, de a dolgozati eredményekhez kötött automatikus adatgyűjtés nem azonosítható. | **Nem igazolható** | A mérési naplókat, rosbaget vagy kiértékelő szkriptet csatolni kellene. |

## 11. Fogalmi és szöveges eltérések

| Hely vagy állítás | Jelenlegi probléma | Javítás |
|---|---|---|
| DWA bevezetője | A dolgozat egyik részében „szinkronhajtású robot” szerepel, miközben a saját modell differenciálhajtású. | Cseréld „differenciálhajtású robot”-ra. |
| Robotkinematika (31)–(32) | A képletekben az `x` és `y` deriváltjele hiányzik. | `dot{x}` és `dot{y}` jelölést használj. |
| Robotkinematika (30) | A `b` és `2b` jelentése csak akkor helyes, ha `b` fél tengelytáv. | Írd le: `2b` teljes keréktávolság, `b` fél tengelytáv. |
| Robotállapot frissítése | A dolgozat csak a kinematikai képleteket írja le, az aktuális keréksebességek gyorsuláskorlátozását nem. | Vedd fel az `a_max / r` alapú keréksebesség-korlátot. |
| Integrálás megnevezése | A kód íves mozgásnál zárt alakú köríves megoldást használ. | „Zárt alakú köríves integrálás” legyen a pontos megfogalmazás. |
| A* változatok | A háttéranyagban vagy tervben szereplő algoritmusokat a működő Python kód nem tartalmazza. | Válaszd külön: szakirodalmi háttér, terv, megvalósított algoritmus. |
| Mérési eredmények | A számokhoz nincs azonosítható helyi mérési pipeline és eredményfájl. | Minden szám mellé futtatási paraméter, kód, dátum és eredményfájl szükséges. |

## 12. Ellenőrzött tesztek és ellenőrzési korlátok

A robot- és DWA-mag célzott tesztje sikeresen lefutott:

```text
python -m unittest codes_diploma.astar_project.tests.test_robot_and_dwa
Ran 4 tests in 0.336s
OK
```

A dolgozat és a kód összevetése során ellenőrzött fő források:

- [`robot.py`](codes_diploma/robot.py)
- [`DWA.py`](codes_diploma/DWA.py)
- [`DWA+A.py`](codes_diploma/DWA+A.py)
- [`simulation.py`](codes_diploma/simulation.py)
- [`grid_map.py`](codes_diploma/astar_project/grid_map.py)
- [`astar_baseline.py`](codes_diploma/astar_project/astar_baseline.py)
- [`astar_variants.py`](codes_diploma/astar_project/astar_variants.py)
- [`path_smoothing.py`](codes_diploma/astar_project/path_smoothing.py)
- [`astar_simulation.py`](codes_diploma/astar_project/astar_simulation.py)
- [`metrics.py`](codes_diploma/astar_project/metrics.py)
- [`experiments.py`](codes_diploma/astar_project/experiments.py)
- [`run_experiment.py`](codes_diploma/astar_project/run_experiment.py)
- [`astar_dwa_node.cpp`](codes_diploma/ros2_astar_dwa_gazebo/src/astar_dwa_controller/src/astar_dwa_node.cpp)
- [`moving_obstacle_node.py`](codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/dwa_gazebo_sim/moving_obstacle_node.py)
- [`gazebo_odometry_world.py`](codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/dwa_gazebo_sim/gazebo_odometry_world.py)
- [`simulation.launch.py`](codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/launch/simulation.launch.py)
- [`rosbot.yaml`](codes_diploma/ros2_astar_dwa_gazebo/src/astar_dwa_controller/config/rosbot.yaml)
- [`README.md`](codes_diploma/ros2_astar_dwa_gazebo/README.md)

A `cpp-rethink` ágon a korábbi duplikált Python ROS-planner fájlok törölve
lettek. Ez nem érinti a `codes_diploma/simulation.py` és a Python A*/DWA
referencia működését.

A DOCX képletei Word OMML matematikai objektumként szerepelnek; a robotkinematikai fejezet (27)–(37) képleteinek szerkezete külön ki lett olvasva. A teljes dolgozat vizuális tördelése, ábraaláírásai és minden külső szakirodalmi hivatkozás tartalmi hitelessége ebből a kód-auditból nem bizonyítható.

## 13. Javítási sorrend

1. A dolgozatban javítsd a robotkinematikai jelöléseket és egészítsd ki a gyorsuláskorlátozással.
2. Válaszd külön a működő klasszikus A* és a csak tervezett/tárgyalt A* változatokat.
3. A mérési eredményeket csak reprodukálható futtatás után hagyd saját eredményként.
4. A Pythonos és ROS2-es DWA implementációt külön rendszerként írd le.
5. A tisztán A*-os demonstrációt különítsd el az A* + DWA fizikai szimulációtól.
6. A dolgozat végén vagy a mellékletben add meg a konkrét futtatási parancsokat, paramétereket és teszteredményeket.

## 14. Ctrl+F keresőlista a dolgozathoz

Az alábbi kifejezéseket másold be a Word keresőjébe. A találat után ellenőrizd a
mellette megadott állítást, képletet vagy fejezetet.

| Keresendő pontos szövegrészlet | Hol található / mit ellenőrizz | Javítás vagy megjegyzés |
|---|---|---|
| `szinkronhajtású mobilrobot` | DWA elméleti bevezetése | A saját modell differenciálhajtású, ezért ezt cseréld `differenciálhajtású mobilrobot` kifejezésre. |
| `A megvalósításom és a dolgozatom második lényeges eleme` | DWA fejezet eleje | Ez a DWA-rész kezdőmondata; ellenőrizd ugyanebben a bekezdésben a robot típusát és a sebességtér definícióját. |
| `A kinematikai korlátokat a szinkronhajtású robot sebességterének` | DWA fejezet | A „szinkronhajtású” megnevezés itt is hibás a jelenlegi robotmodellhez képest. |
| `Mivel a robot jelentős tehetetlenséggel rendelkezik` | Dinamikus ablak és gyorsulási korlát | Ez a szöveg a DWA dinamikus ablakát írja le. Egészítsd ki azzal, hogy a `robot.py` az állapotfrissítésben is korlátozza a kerék-szögsebesség változását. |
| `Ahogyan a kódomban is megvalósítottam` | A DWA dinamikus ablakának magyarázata | Ellenőrizd, hogy a hivatkozott képlet tényleg a `pairstochoose()` és nem csak elméleti sebességtér működését írja-e le. |
| `A megvalósított rendszerben az A* algoritmus felel` | A* és DWA fúziója | Ez a rész jól illeszkedik a `DWA+A.py` működéséhez; ellenőrizd, hogy a globális újratervezés hiánya szerepel-e. |
| `Bézier-görbékkel simítunk` | A* és DWA fúziója | Egyezik a `path_smoothing.py` és `DWA+A.py` működésével. Ne nevezd optimális simításnak. |
| `másodfokú Bézier-görbékkel simítom` | Útvonalsimítás fejezete | Egyezik; a következő mondatokban keresd a kerekített cellákon végzett biztonsági ellenőrzést is. |
| `A rendszer rácscellákra kerekíti a görbe pontjait` | Bézier-simítás biztonsági ellenőrzése | Egyezik a `_is_path_safe()` működésével, de ez diszkrét ellenőrzés, nem folytonos görbe–akadály metszésvizsgálat. |
| `Ha az ív nem biztonságos` | Bézier-simítás fallback ága | Egyezik: a kód ilyenkor az eredeti A* útvonalat adja vissza. |
| `create_waypoints függvény végzi` | Waypoint-újramintavételezés | A dolgozatban ellenőrizd a pontos lépésközt: a kód alapértéke `0.2 m`. |
| `pontosan` és `méterenként helyez el` | A `create_waypoints` mondatának környezete | Csak akkor maradjon így, ha az egyenlő ívhosszú waypoint-generálásról van szó; a Bézier-mintapontok nem ugyanazok, mint a waypointok. |
| `Path Pruning (Útvonal-metszés)` | Pályakövetési fejezet | Egyezik a `_update_pruned_lookahead_target()` függvénnyel; keresd a `25` elemű keresési ablak és a `0.35–0.80 m` lookahead értéket. |
| `legközelebbi pont keresését a megelőző ciklus indexétől` | Path pruning rész | Egyezik a kóddal, mert a waypoint-index nem lép vissza. |
| `A szimuláció alapját a differenciálhajtású robot matematikai modellje adja` | Robotkinematikai fejezet eleje | A fejezet megfelelő kiindulás; innen keresd a (27)–(37) képleteket. |
| `Ahol a 2b paraméter a két hajtott kerék közötti tengelytávolságot jelöli` | A (30) képlet után | Ez csak akkor pontos, ha `b` fél tengelytáv. A kódban `b = 0.08 m`, ezért a teljes keréktávolság `2b = 0.16 m`. |
| `a szögsebesség nulla` | Egyenes vonalú mozgás leírása | Ellenőrizd, hogy a képlet mellett szerepel-e a kódbeli küszöb: `abs(w) <= 1e-6`, nem csak az elméleti `w = 0`. |
| `az állapotfrissítés numerikus integrálással valósul meg` | A (31)–(32) képletek előtti bekezdés | Íves mozgásnál pontosabb: `zárt alakú köríves integrálás`. |
| `A robot új állapotának` | A (33)–(35) képletek bevezetése | Itt ellenőrizd a változókat: `x`, `y`, `theta`, `v`, `w` és `dt`. |
| `Amennyiben a szögsebesség nem nulla` | A (36)–(37) köríves képletek bevezetése | Egyezik a kód `abs(w) > 1e-6` ágával. |
| `Ez a matematikai megközelítés biztosítja` | Robotkinematikai fejezet zárómondata | A mondat maradhat, de érdemes hozzátenni, hogy ez ideális, csúszásmentes kinematikai modell. |
| `A szimulációs eredmények és forgatókönyvek vizsgálata` | Eredményfejezet címe | Ellenőrizd minden táblázat és ábra mögött a futtatott kódot, paramétert és eredményfájlt. |
| `A szimulációk igazolják` | A heurisztikák vagy eredmények értékelése | Minden ilyen mondathoz kell helyi mérési eredmény; a jelenlegi `metrics.py` és `run_experiment.py` nem szolgáltat kész benchmark-pipeline-t. |
| `legmagasabb számítási hatékonyságot` | Heurisztika-összegzés | Csak mérési táblázattal és azonos forgatókönyvekkel igazolható; elméleti állításként óvatosabban fogalmazd. |
| `ROS 2 szoftverarchitektúra és Gazebo szimulációs környezet` | ROS2/Gazebo fejezet címe | Az indított launch fájlt és a ténylegesen használt C++ vagy Python node-ot nevezd meg. |
| `ROS 2 csomópont-architektúra és kommunikációs interfészek` | ROS2 alfejezet | Ellenőrizd a topicneveket és azt, hogy a dolgozat ne állítsa a Python DWA teljes ROS2-portját. |
| `Gazebo 3D fizikai szimuláció` | Gazebo alfejezet | A világ és a robotmodell jelen van, de automatikus mérési eredmény csak naplóval vagy kiértékelő szkripttel bizonyítható. |
