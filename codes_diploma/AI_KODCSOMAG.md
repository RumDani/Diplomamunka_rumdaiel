# AI-kódcsomag - aktuális forrássnapshot

Generálás dátuma: 2026-11-06

Ez a dokumentum a `cpp-rethink` ág jelenlegi munkafájának forrássnapshotja. Nem egy futással igazolt kiadás. A Gazebo `simulation.launch.py` kizárólag a C++ `astar_dwa_node` vezérlőt indítja. A build forrása `reference_controller.cpp`, tervezőmagja `reference_planner.hpp`; a régi `astar_dwa_node.cpp` már nem a buildelt implementáció.

A snapshot a követett forrás-, konfigurációs, csomagolási és tesztfájlok aktuális lemezes tartalmát tartalmazza. Kihagyja a virtuális környezetet, a build/install/log könyvtárakat, a binárisokat, az eredményábrákat és a futási naplókat. Az `Önlab` fájlok archívak; a C++ és legacy ROS fájlok jelenléte sem jelenti, hogy az aktív launch használja őket. A régebbi kódmagyarázatok frissítése halasztott; az alábbi állapotjelentést kell figyelembe venni.

## Aktuális architektúra - ellenőrzött források alapján

- A `simulation.launch.py` Gazebót, ROS-Gazebo bridge-et, SLAM Toolboxot, a C++ `astar_dwa_node` vezérlőt, továbbá `python_simulation_node` és `lidar_obstacle_node` segédfolyamatokat indít.
- A C++ mag az eredeti Python A*+DWA alapján tartalmazza a globális A*-ot, ellenőrzött Bézier-simítást, 0,2 m-es waypointokat, az adaptív toleranciát és az eredeti DWA fékút-szűrését, mozgóakadály-predikcióját, valamint irány/távolság/sebesség pontozását.
- Python navigációs backend nincs: `python_planner_node.py`, `python_dwa.py`, a tervezőbetöltő és a backend-kapcsolók törölve. Python csak a launch, szimulációs segédfeladatok és LiDAR-követés oldalán maradt. Az eredeti Matplotlib-források változatlan referenciák, nem a Gazebo vezérlője.
- A SLAM `/map` térképet ad a globális A*-hoz. A lokális akadályadat útja: `/scan` -> LiDAR-követő -> `/tracked_obstacles` -> DWA -> `/cmd_vel`.
- A robot állapota kerék-odometriából és TF-ből származik. Lánc: `map -> odom -> base_footprint -> base_link -> base_scan`. Az adapter a spawneltolást egyszer adja hozzá a nyers kerék-odometriához.
- A `/gazebo/ground_truth_odom` kizárólag diagnosztikára és a Gazebo útvonalrajzának illesztésére szolgál, nem navigációra.
- Mapping, térképmentés és mentett térképes lokalizáció rendelkezésre áll. Azonos koordinátakeretű térképfrissítés megőrzi a waypointokat; nem cél a folyamatos globális újratervezés.

## Átadási Állapot És Korlátok

- Kiinduló, korábban pusholt állapot: `d8bfb61`, ág: `cpp-rethink`. Az alábbi snapshot már az ezt követő C++-átállást tartalmazza.
- VÉGLEGES CÉL: az eredeti, Matplotlibben a felhasználó szerint jól működő Python `DWA+A.py` A* + DWA megvalósítás ötleteinek és döntési logikájának átültetése C++ / ROS 2 / fizikai Gazebo környezetbe. A felhasználó a szimulációban kizárólag C++ navigációs vezérlőt kér. A DWA válassza a kitérő mozgást, majd folytatódjon az eredeti waypointkövetés. Külön kézzel kijelölt oldalsó kerülőcél és új kerülési algoritmus nem kell, ilyen nincs az aktív C++ magban.
- Az eredeti `robot.py`, `DWA.py`, `DWA+A.py`, `simulation.py`, az `astar_project` és a védett A* folyamatábra nem módosítható e javításokhoz. Csak a ROS/Gazebo integráció változzon. Teszteket csak kérésre kell indítani; a felhasználó másik gépen tesztel. Dokumentációs és ábrafrissítések a kódcsomag kivételével halasztottak.
- Legújabb regressziós bizonyíték: az `a3b2a57` próbában a robot már a találkozás előtt lelassul. Egy sorban `admissible=118 forward_pairs=103 reject_dynamic=0`, mégis `cmd=(0.006,0.071)`: ekkor a pontozás választ közel álló mozgást, nem a biztonsági szűrés kényszeríti ki. Csak később fogy el minden jelölt a közeledő akadály miatt. Külön hiba: a lokalizált y kb. 1,75 m-ről 4,33 m-re ugrik, miközben a tényleges robot y kb. 1,76 m. A 8-as távolságsúly/1 m-es puha cél hangolása nem hozott javulást, visszavontuk. Teljes, sikeres kitérés-visszatérés-célbaérés továbbra sincs igazolva.
- A korábbi NumPy-backend és annak eltérő pontozási/kerülési próbálkozásai törölve. A C++ mag nem tartalmazza a régi C++ külön visszatérési üzemmódját és pályabüntetéseit sem. A LiDAR-segédfolyamat felületi pontillesztéses sebességbecslése megmaradt; pontossága nincs fizikai méréssel igazolva.
- Az eredeti Pythonhoz képest tudatos fizikai eltérés: a kerékminták nem léphetik túl a kerékhatárt, míg a NumPy arange végpontja túlcsúszhatott. A C++ és Python numerikus azonosságát nem ellenőriztük; azonos adatokon összehasonlítás szükséges.
- Legújabb szimulációs hangolás: a szembejövő `moving_obstacle_2` pályája y=2,1 m helyett y=1,7 m. A y=2,4 m-nél kezdődő vízszintes fal és a 0,18 m sugarú akadály közti felületi rés így 0,12 m helyett 0,52 m. A falak változatlanok. Az aktív Gazebo-segédnode szembejövő akadálysebessége 0,25-ről 0,26 m/s-ra nőtt, tehát 4%-kal gyorsabb.
- Visszaállított puha távolságpontozás: a `dynamic_clearance_distance` alapértéke ismét 0,6 m, a `dynamic_clearance_weight` alapértéke ismét 4,0. A merev ütközési sugár változatlan. Az előre jelzett mozgóakadály-ütközés továbbra is kizárja a jelöltet, nulla robotsebességnél is; a statikus fékút-szűrés és a waypoint/pruning logika megmarad. A súlyozás nem hozhat vissza kizárt jelöltet.
- Új célközeledési pontszám: a DWA a predikció eleji és végi lokális céltávolság különbségét elosztja a maximális lineáris sebesség és a pontozási horizont szorzatával, majd -1 és 1 közé korlátozza. Ez dimenzió nélküli érték: állva 0, közeledve pozitív, távolodva negatív; a meglévő `Alfa` súllyal hozzáadódik az irányponthoz. Például 0,35 m-ről 0,28 m-re közeledésnél, 0,26 m/s maximummal és 0,7 s horizonttal a pontszám 0,07/(0,26*0,7), kb. 0,385; az 5-ös súllyal kb. 1,92 pont. Ez nem kikényszerített előremenet, csak az összes biztonsági szűrésen átment jelöltek pontozása. Új naplómezők: `score_progress`, `score_dynamic`, `score_distance`, mind a kiválasztott jelölt súlyozott komponensei. Futási igazolás még nincs.
- Sűrűbb kerékmintavétel: az új `wheel_resolution` launch-argumentum a C++ `w_kerek_resolution` paramétert adja, alapértéke 0,5 rad/s a korábbi 1,0 helyett. Több görbületi/sebességjelölt kerül ugyanabba a dinamikus ablakba. A robot 0,26 m/s-os sebességhatára, gyorsulása, 3 másodperces predikciója és a biztonsági zóna változatlan. A sűrűbb mintázás több számítást jelent; a célgépen a `compute_ms` és `planner_deadline` figyelendő. A meglévő C++ ellenőrzőfájlhoz hozzáadtuk a régi minták megtartását és a fizikai kerékhatárokat ellenőrző eseteket, de ezeket nem futtattuk.
- A 360 fokos, 3 méteres LiDAR-ellenőrzés megmarad. A célfüggvényben ismét a `6a38f98` változat méter alapú akadály-ívhossz pontszáma szerepel; a 10-zel osztott normalizálást visszavontuk. Ezért a pontszámok eltérő skálájának ismert kockázata jelenleg fennmarad. A `DIAG_CONFIG` jelölése `schema=cpp-dwa-7 lidar_fov=360 pruning=25`, és kiírja a `dynamic_clearance_weight`, `dynamic_clearance_distance`, `wheel_resolution` értékeket is.
- Szűkített visszatérés új célpont nélkül: először a mozgó akadályok és a robot aktuális sebességének egyenletes továbbhaladásából várható ütközési veszélyt nézzük a predikciós horizonton. Ilyen veszélynél nincs waypoint-irányhibából eredő sebességkorlátozás, a korábbi DWA-pontozás választhat kitérőt. Külön lassítás/helyben forduló minta csak 90 foknál nagyobb waypoint-irányhibánál és ilyen veszély hiányában van. A fékezési korlát és minden jelölt ütközésszűrése megmarad, nincs kikényszerített előremenet. A globális útvonal és a waypointok sorrendje változatlan. Új naplómezők: `avoidance_priority`, `reorient`, továbbá a radiánban mért `goal_heading_error`.
- Dinamikus pruning és lookahead már aktív: a `path_tracking::prune_lookahead` a jelenlegi waypoint előtti szakasztól legfeljebb 25 waypointtal előre keres elérhető, legközelebbi szakaszprojekciót. Az aktív index nem lép vissza, és egy ciklusban több elhagyott pontot is kihagyhat. A DWA célja a projekciótól előrefelé, a megmaradt pálya ívhosszán kijelölt pont; nem külön kézzel választott kerülőcél. A névleges lookahead 0,35 m plusz a sebesség abszolút értékének 1,2-szerese, legfeljebb 0,80 m. Például állva 0,35 m, 0,25 m/s-nál 0,65 m. Az eredeti Python előretekintési segédfüggvényétől ez eltér, hogy a lassabb fizikai robot sebessége is ténylegesen befolyásolja a távolságot.
- Pruning-biztonság: a robot és a projekció, illetve a lookahead-cél közti egyenes összeköttetést az inflált térképen ellenőrizzük; falon vagy ismeretlen cellán át nem választunk új visszacsatlakozást. Blokkolt lookahead esetén a távolság felezhető, 0,05 m-ig vizsgálva, végül az elérhető projekció használható. Ha nincs elérhető projekció, nem történik pruning, az addigi waypoint marad; a DWA ütközésszűrése ekkor is aktív. A mozgó akadályok vizsgálata továbbra is a DWA feladata. A globális út és a waypointlista nem változik. Lejárt számításnál a pruning indexét az adapter visszaállítja.
- Új pruning-naplómezők: `pruned`, `lookahead`, `target_index`; a `target` és `goal_heading_error` már a tényleges lookahead-célra vonatkozik. A meglévő `test_path_tracking.cpp` új esetei több pont elhagyását, monotonitást, sebességfüggést, blokkolt összeköttetést és végcélra korlátozást fednek le. Ezeket a felhasználó kérésének megfelelően nem futtattuk; helyi C++/ROS build és Gazebo-próba sem történt.
- A LiDAR-illesztés visszaállt a `6a38f98` állapotra: közeli felületi pontok mediáneltolása, legalább két egyezés, az eredeti sebességsimítás. A kölcsönös párosítást, 50%-os átfedési küszöböt és a sebességtartást visszavontuk. A visszaállítás fájltartalmát Gittel összehasonlítottuk. A zajos becslések ismert kockázata fennmarad; ennek külön vizsgálatához friss futási adatok szükségesek.
- A C++ adapter mért keréksebességből indul, pontos szenzoridőbélyeghez kér TF-et, késő transzformációhoz korlátos üzenetsorokat tart, az akadályokat a robotállapot idejére igazítja. Friss adatok és számítási határidő nélkül megáll. Ugyanabban a map koordinátakeretben érkező új térkép nem indít új globális tervezést.
- Lokalizációs regresszió visszavétele: a felhasználó pontosítása szerint RVizben a térkép és a LiDAR-pontok csúsznak el egymáson, nem a Gazebo-útvonal rajzolásával van az aktuális probléma. A korábban lokalizációhoz bevezetett nullás mozgásküszöböt visszavontuk; a launch mindkét módban `minimum_travel_distance=0.1`, `minimum_travel_heading=0.1` értéket és `check_min_dist_and_heading_precisely=True` beállítást ad át. Ez az upstream kapuban a kellő forgást is elfogadja scan-feldolgozáshoz, miközben álló odometria mellett nem kér minden scanhez újraillesztést. A meglévő időkorlát 0,1 s. A `DIAG_SLAM_CONFIG` kiírja a `scan_motion_threshold=0.1` értéket. A Gazebo-rajzoló kódját és a DWA-t ebben a javításban nem változtattuk. A nullás küszöb hozzájárulása az elcsúszáshoz hipotézis, nem bizonyított kizárólagos ok.
- Lokalizációs korlát: a visszaállított mozgásküszöb ismét megakadályozhatja a scan-feldolgozást kerékforgás nélküli fizikai eltoláskor; ezt ez a módosítás nem oldja meg. Az upstream kapu forrása: https://github.com/SteveMacenski/slam_toolbox/blob/ros2/src/slam_toolbox_common.cpp . A célgépen telepített verzió paramétertámogatását és a tényleges térkép–LiDAR illesztést újraindítás után ellenőrizni kell. Az elcsúszott futási állapottal ne írják felül a jó mentett térképet. Nincs navigációs ground truth visszacsatolás, és ez a beállítás nem oldja meg önmagában a DWA jelöltelfogyását.
- Lokalizációs ugrásvédő: aktív követésnél két elfogadott odometriai időbélyeg közti lokalizált elmozdulást a maximális robotsebesség és az eltelt idő alapján ellenőrizzük. A megengedett ugrás a nagyobbik érték 0,5 m és a maximális sebességgel megtett út plusz 0,2 m közül. Ezt meghaladó ugrásnál a node nullás motorparancsot küld, megszakítja az aktív feladatot és törli annak útvonalát; `DIAG_LOCALIZATION` és `reason=localization_jump` jelzi. A lokalizáció ellenőrzése után új cél szükséges; ez nem javítja meg önmagában a scan matchinget. A meglévő szimulációs segédnode az inaktív állapot hatására az akadálymenetet is leállítja, ezért ez a megszakítás nem értékelhető sikeres kitérésnek.
- Viselkedést nem módosító DWA-diagnosztika: `reject_velocity`, `reject_dynamic`, `reject_braking` a kizárási okokat számolja; ezek és az `admissible` összege adja a `pairs` értékét. A `reject_dynamic_now` a dinamikus kizárások azon része, amely már t=0-nál, a mozgó akadály biztonsági zónáján belül történik; ez nem feltétlenül fizikai érintkezés. A `forward_pairs` a megengedett, 0,01 m/s feletti jelöltek száma. A `moving_points` és `max_obstacle_speed` a DWA-nak átadott akadálybecslést mutatja. A biztonsági szűréseket és a pontozást e diagnosztikai csomag nem lazítja.
- A fizikai illesztés bemenete nem a Matplotlib pontos akadálymodellje: LiDAR-felületi pontok, becsült akadálysebesség, kerék-odometria és késleltetett TF érkezik. A megállás okát friss `DIAG_CONTROL cpp`, `DIAG_LIDAR`, `DIAG_TF_CPP` adatokkal kell elkülöníteni; lehet elégtelen sebességbecslés, üres megengedett jelölthalmaz, célfüggvény vagy késleltetés. Az új javítások eredményessége még nincs futással igazolva.
- Következő munka: C++/ROS build és Gazebo-futtatás a célgépen; `DIAG_CONFIG backend=cpp-python-reference`, `DIAG_CONTROL cpp`, `DIAG_TF_CPP` és `DIAG_LIDAR` naplók értékelése. Ne helyettesítsd a hibakeresést vak előremenettel, akadályadatok elhagyásával vagy biztonsági időkorlátok kikapcsolásával.
- Helyi ROS/Gazebo-futás és numerikus összehasonlítás nem történt. A korábbi editor- és szintaxisellenőrzés nem bizonyítja a helyes akadálykerülést.

## Diplomamunka - Gazebo-fejezet ötletek

1. Ismertesd a szimulációs architektúrát, a launch által indított folyamatokat, a ROS topicokat és az adatfolyamot a LiDAR-bemenettől a `/cmd_vel` kimenetig.
2. Mutasd be az `odom -> base_link -> base_scan` TF-láncot és az `rqt_graph` szerepét. A TF geometriai koordináta-kapcsolatokat, az rqt_graph node- és topic-kapcsolatokat mutat.
3. Fogalmazz meg mérési tervet a világpozíciós és kerék-odometria összevetésére: azonos időbélyegeken mért pozícióhiba, eltérés akadálykontaktus után, valamint a célkoordinátához viszonyított végső hiba. Csak mérés után közölj számokat.
4. Különítsd el a statikus, globális térképet és a LiDAR-ból származó lokális DWA-akadályinformációt. Írd le, hogy a jelenlegi implementáció milyen adatot használ, és mi nincs megvalósítva, például a globális térkép automatikus frissítése LiDAR-ból.
5. Javasolt értékelési mutatók: célbaérési arány, útvonalhossz, futási idő, minimális akadálytávolság, célhiba és sikertelen/újratervezett esetek. Az összehasonlításhoz rögzített pályák, azonos célok, több ismétlés és dokumentált paraméterek kellenek.
6. Tárgyald a szimuláció és a valós robot közötti különbségeket: LiDAR-keret és kalibráció, odometria, késleltetés, QoS, kerékparaméterek, fizikai korlátok, vészfékezés és fokozatos tesztelés.

### Diplomamunkaszöveg készítésére használható prompt

> A fenti átadási állapotból és a beillesztett aktuális forrásokból dolgozz. A navigáció csak C++; a megmaradt Python segédnode-okat ne keverd össze egy Python vezérlővel. Az eredeti Python A*+DWA változatlan viselkedési referencia. Különítsd el a kódból bizonyítható tényeket, a felhasználói hibajelentést és az ellenőrizetlen hipotéziseket. Ne állítsd működőnek a szembejövő akadály kerülését futási bizonyíték nélkül. Csak a ROS/Gazebo fájlokat módosítsd, az eredeti Python-fájlokat ne.

A teljes Gazebo-indítási sorrend és a TF/rqt terminálparancsok a `ros2_astar_dwa_gazebo/README.md` fájlban találhatók.

## Aktuális forrásfájlok

### codes_diploma/astar_project/__init__.py

~~~~~python

~~~~~

### codes_diploma/astar_project/astar_baseline.py

~~~~~python
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

~~~~~

### codes_diploma/astar_project/astar_simulation.py

~~~~~python
"""Egyszeru matplotlib szimulacio az A* utvonal bemutatasahoz."""

import math
import tkinter as tk
from tkinter import messagebox, ttk

import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from matplotlib.widgets import Button

from .astar_baseline import astar_search
from .astar_variants import get_heuristic
from .grid_map import GridMap
from .path_smoothing import bezier_curve_points, smooth_path


def create_demo_map(
    width=30,
    height=20,
    resolution=0.2,
    robot_radius=0.08,
    start=(2, 2),
    goal=(17, 27),
):
    """Letrehoz egy ismert, statikus akadalyokat tartalmazo terkepet."""
    grid_map = GridMap(width=width, height=height, resolution=resolution)
    vertical_column = min(10, width - 2)
    horizontal_row = min(12, height - 2)
    vertical_wall = [
        (row, vertical_column)
        for row in range(2, max(2, height - 2))
        if row not in range(7, 13)
    ]
    horizontal_wall = [
        (horizontal_row, column)
        for column in range(12, max(12, width - 2))
        if column not in range(19, 25)
    ]
    for row, column in vertical_wall + horizontal_wall:
        if grid_map.is_inside(row, column) and (row, column) not in (start, goal):
            grid_map.add_obstacle(row, column)
    grid_map.inflate_obstacles(robot_radius)
    return grid_map, start, goal


def _parse_position(value):
    """Egy 'sor,oszlop' szoveget racskoordinatava alakit."""
    row, column = (int(part.strip()) for part in value.split(","))
    return row, column


def _read_settings(fields, diagonal, heuristic):
    """Beolvassa es ellenorzi a beallitasi ablak ertekeit."""
    get_value = lambda field: field.get() if hasattr(field, "get") else field.text
    heuristic_name = heuristic.get() if hasattr(heuristic, "get") else heuristic.value_selected
    diagonal_value = diagonal.get() if hasattr(diagonal, "get") else diagonal.get_status()[0]
    settings = {
        "width": int(get_value(fields["width"])),
        "height": int(get_value(fields["height"])),
        "resolution": float(get_value(fields["resolution"])),
        "robot_radius": float(get_value(fields["robot_radius"])),
        "start": _parse_position(get_value(fields["start"])),
        "goal": _parse_position(get_value(fields["goal"])),
        "diagonal": diagonal_value,
        "smooth_path": fields["smooth_path"].get(),
        "auto_play": fields["auto_play"].get(),
        "heuristic": get_heuristic(heuristic_name),
    }
    if settings["width"] < 3 or settings["height"] < 3:
        raise ValueError("A terkep legalabb 3 x 3 meretu legyen.")
    if settings["resolution"] <= 0 or settings["robot_radius"] < 0:
        raise ValueError("A felbontas pozitiv, a robotmeret nem negativ legyen.")
    return settings


def _create_settings_window(on_apply):
    """Letrehozza az A* bemeneti ertekeinek feluletet."""
    window = tk.Tk()
    window.title("A* beallitasok")
    window.resizable(False, False)
    main = ttk.Frame(window, padding=20)
    main.grid()
    ttk.Label(main, text="A* szimulacio", font=("Segoe UI", 16, "bold")).grid(
        row=0, column=0, columnspan=2, sticky="w", pady=(0, 16)
    )

    values = {
        "width": ("Szelesseg", "30"),
        "height": ("Magassag", "20"),
        "resolution": ("Felbontas [m]", "0.2"),
        "robot_radius": ("Robot sugar [m]", "0.08"),
        "start": ("Start (sor,oszlop)", "2,2"),
        "goal": ("Cel (sor,oszlop)", "17,27"),
    }
    fields = {}
    for index, (name, (label, value)) in enumerate(values.items()):
        row = index + 1
        ttk.Label(main, text=label).grid(row=row, column=0, sticky="w", padx=(0, 20), pady=5)
        field = ttk.Entry(main, width=24)
        field.insert(0, value)
        field.grid(row=row, column=1, sticky="ew", pady=5)
        fields[name] = field

    diagonal = tk.BooleanVar(value=True)
    ttk.Checkbutton(main, text="Atlos mozgas engedelyezese", variable=diagonal).grid(
        row=7, column=0, columnspan=2, sticky="w", pady=(12, 5)
    )
    ttk.Label(main, text="Heurisztika").grid(row=8, column=0, sticky="w", pady=5)
    heuristic = ttk.Combobox(
        main,
        values=["manhattan", "euclidean", "chebyshev", "octile"],
        state="readonly",
        width=21,
    )
    heuristic.set("euclidean")
    heuristic.grid(row=8, column=1, sticky="ew", pady=5)

    smooth_path_value = tk.BooleanVar(value=True)
    ttk.Checkbutton(
        main,
        text="Utvonal simitasa",
        variable=smooth_path_value,
    ).grid(row=9, column=0, columnspan=2, sticky="w", pady=5)
    fields["smooth_path"] = smooth_path_value

    auto_play_value = tk.BooleanVar(value=True)
    tk.Checkbutton(
        main,
        text="Automatikus lejatszas",
        variable=auto_play_value,
    ).grid(row=10, column=0, columnspan=2, sticky="w", pady=5)
    fields["auto_play"] = auto_play_value

    def apply_settings():
        try:
            settings = _read_settings(fields, diagonal, heuristic)
            window.destroy()
            on_apply(settings)
            plt.show()
        except (TypeError, ValueError, RuntimeError) as error:
            messagebox.showerror("Hibas beallitas", str(error), parent=window)

    ttk.Button(main, text="Szimulacio inditasa", command=apply_settings).grid(
        row=11, column=0, columnspan=2, sticky="ew", pady=(16, 0)
    )
    return window


def _safe_curve(grid_map, curve, diagonal):
    cells = [grid_map.world_to_grid(x, y) for x, y in curve]
    return all(
        grid_map.is_free(*cell)
        for cell in cells
    ) and all(
        current_next == current
        or current_next in grid_map.get_neighbors(*current, diagonal)
        for current, current_next in zip(cells, cells[1:])
    )


def create_robot_trajectory(
    grid_map, path, steps_per_cell=4, smooth=False, diagonal=False
):
    """Az A* cellautvonalabol koztes pontokat keszit az animaciohoz."""
    if not path:
        return []

    world_path = [grid_map.grid_to_world(row, column) for row, column in path]
    if smooth:
        curve = bezier_curve_points(world_path, samples_per_segment=20)
        if _safe_curve(grid_map, curve, diagonal):
            return curve

    trajectory = [world_path[0]]
    for start, end in zip(world_path, world_path[1:]):
        for step in range(1, steps_per_cell + 1):
            ratio = step / steps_per_cell
            trajectory.append(
                (
                    start[0] + ratio * (end[0] - start[0]),
                    start[1] + ratio * (end[1] - start[1]),
                )
            )
    return trajectory


def draw_map(ax, grid_map, start, goal):
    """Kirajzolja a terkepet es a start-cel pontokat."""
    for row in range(grid_map.height):
        for column in range(grid_map.width):
            if grid_map.grid[row][column] != 1:
                continue
            ax.add_patch(
                Rectangle(
                    (column * grid_map.resolution, row * grid_map.resolution),
                    grid_map.resolution,
                    grid_map.resolution,
                    facecolor="#444444",
                    edgecolor="white",
                    linewidth=0.3,
                )
            )

    start_x, start_y = grid_map.grid_to_world(*start)
    goal_x, goal_y = grid_map.grid_to_world(*goal)
    ax.scatter(start_x, start_y, color="#16803c", s=70, label="Start", zorder=4)
    ax.scatter(goal_x, goal_y, color="#c62828", s=70, label="Cel", zorder=4)
    ax.set_xlim(0, grid_map.width * grid_map.resolution)
    ax.set_ylim(0, grid_map.height * grid_map.resolution)
    ax.set_aspect("equal")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_xticks(
        [
            grid_map.origin_x + column * grid_map.resolution
            for column in range(grid_map.width + 1)
        ],
        minor=True,
    )
    ax.set_yticks(
        [
            grid_map.origin_y + row * grid_map.resolution
            for row in range(grid_map.height + 1)
        ],
        minor=True,
    )
    ax.grid(True, which="minor", color="#9e9e9e", alpha=0.5, linewidth=0.5)
    ax.grid(True, which="major", alpha=0.2)


def _priority_text(search_steps, frame):
    """Rovid szoveges tablazat az aktualis prioritasi sorrol."""
    if frame >= len(search_steps):
        return "A* kesz\n\nA robot koveti\na kivalasztott utvonalat."

    step = search_steps[frame]
    lines = [
        f"Lepes: {frame + 1}",
        f"Aktualis: {step['current']}",
        "",
        "pozicio       g     h     f",
    ]
    for index, item in enumerate(step.get("priority_queue", [])[:8], start=1):
        lines.append(
            f"{index:2d}. {str(item['position']):9s} "
            f"{item['g']:5.1f} {item['h']:5.1f} {item['f']:5.1f}"
        )
    if len(lines) == 4:
        lines.append("(ures prioritasi sor)")
    return "\n".join(lines)


def plot_simulation(
    grid_map,
    path,
    trajectory,
    start,
    goal,
    expanded_nodes=None,
    search_steps=None,
    original_path=None,
    robot_radius=0.08,
    planning_interval=200,
    movement_interval=50,
    auto_play=False,
    show=True,
    smoothed=False,
):
    """A* es robotmozgasi abra kezi vagy automatikus lejatszassal."""
    expanded_nodes = expanded_nodes or []
    search_steps = search_steps or []
    figure, (priority_ax, map_ax) = plt.subplots(
        1, 2, figsize=(13, 6), gridspec_kw={"width_ratios": (1.35, 2.4)}
    )
    figure.subplots_adjust(bottom=0.14, right=0.82, wspace=0.12)

    priority_ax.set_title("Prioritasi sor")
    priority_ax.set_axis_off()
    priority_ax.text(
        0.02,
        0.98,
        "A* prioritasi keplet",
        va="top",
        fontsize=10,
        fontweight="bold",
        color="#263238",
    )
    priority_ax.text(
        0.02,
        0.88,
        "f(n) = g(n) + h(n)\n\n"
        "g: eddigi ut koltsege\n"
        "h: becsult tavolsag a celig\n"
        "f: teljes prioritasi ertek\n\n"
        "Euklideszi h(n):\n"
        "h(n) = sqrt(dr^2 + dc^2)\n"
        "dr = |goal_row - row|\n"
        "dc = |goal_col - col|\n\n"
        "Pelda: dr=15, dc=25\n"
        "h(n) = sqrt(15^2 + 25^2) = 29.15\n\n"
        "Egyenes = 1.0 | Atlos = 1.41\n"
        "resolution = 0.2 m | robot = 0.08 m",
        va="top",
        family="monospace",
        fontsize=8,
        color="#263238",
        linespacing=1.35,
    )
    priority_text = priority_ax.text(
        0.02,
        0.31,
        "",
        va="top",
        family="monospace",
        fontsize=7.5,
        color="#004d40",
        linespacing=1.25,
    )
    draw_map(map_ax, grid_map, start, goal)
    map_ax.set_title("A* utvonal es Bezier-simitas")

    expanded_world = [grid_map.grid_to_world(*cell) for cell in expanded_nodes]
    path_world = [grid_map.grid_to_world(*cell) for cell in path]
    original_world = [
        grid_map.grid_to_world(*cell) for cell in (original_path or path)
    ]
    display_path = trajectory if smoothed else path_world
    path_x, path_y = zip(*display_path)
    original_x, original_y = zip(*original_world)
    original_line, = map_ax.plot(
        original_x,
        original_y,
        ":",
        color="#9e9e9e",
        linewidth=2,
        label="Eredeti A* utvonal",
        visible=False,
        zorder=2,
    )
    path_line, = map_ax.plot(
        path_x,
        path_y,
        "-",
        color="#ef8a8a",
        linewidth=2.0,
        alpha=0.8,
        label="Bezier-simitott utvonal",
        visible=False,
        zorder=3,
    )
    explored = map_ax.scatter(
        [], [], s=28, color="#90caf9", alpha=0.6, label="Vizsgalt cellak"
    )
    current_search = map_ax.scatter(
        [], [], s=90, color="#ff9800", edgecolors="#e65100",
        label="C: aktualis cella", zorder=5
    )
    robot = Circle(
        (math.nan, math.nan), robot_radius, color="#e65100", label="Robot", zorder=6
    )
    map_ax.add_patch(robot)
    trail, = map_ax.plot([], [], color="#f57c00", linewidth=2, label="Robot nyoma")
    status = map_ax.text(0.02, 0.98, "Indulas", transform=map_ax.transAxes, va="top")
    map_ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), borderaxespad=0)

    trajectory_x = [point[0] for point in trajectory]
    trajectory_y = [point[1] for point in trajectory]
    planning_frames = len(expanded_world)
    movement_start = planning_frames + 1
    total_frames = movement_start + len(trajectory)
    current_frame = 0

    def update(frame):
        nonlocal current_frame
        current_frame = frame
        if frame < planning_frames:
            explored.set_offsets(expanded_world[: frame + 1])
            current_search.set_offsets([expanded_world[frame]])
            priority_text.set_text(_priority_text(search_steps, frame))
            status.set_text(f"A* tervezes: {frame + 1}/{planning_frames}")
            path_line.set_visible(False)
            original_line.set_visible(False)
            robot.center = (math.nan, math.nan)
            trail.set_data([], [])
        elif frame == movement_start - 1:
            explored.set_offsets(expanded_world or [[math.nan, math.nan]])
            current_search.set_offsets([[math.nan, math.nan]])
            priority_text.set_text(_priority_text(search_steps, len(search_steps)))
            status.set_text("A* kesz - robotmozgas indul")
            original_line.set_visible(True)
            path_line.set_visible(True)
            robot.center = (math.nan, math.nan)
            trail.set_data([], [])
        else:
            movement_frame = min(frame - movement_start, len(trajectory) - 1)
            explored.set_offsets(expanded_world or [[math.nan, math.nan]])
            current_search.set_offsets([[math.nan, math.nan]])
            priority_text.set_text(_priority_text(search_steps, len(search_steps)))
            original_line.set_visible(True)
            path_line.set_visible(True)
            robot.center = (trajectory_x[movement_frame], trajectory_y[movement_frame])
            trail.set_data(trajectory_x[: movement_frame + 1], trajectory_y[: movement_frame + 1])
            status.set_text(
                "Cel elerve" if movement_frame == len(trajectory) - 1
                else f"Robotmozgas: {movement_frame + 1}/{len(trajectory)}"
            )
        return (
            explored,
            current_search,
            original_line,
            path_line,
            robot,
            trail,
            status,
            priority_text,
        )

    robot_animation = animation.FuncAnimation(
        figure,
        update,
        frames=total_frames,
        interval=planning_interval,
        repeat=False,
        blit=False,
    )

    if not auto_play and robot_animation.event_source is not None:
        robot_animation.event_source.stop()
        update(0)

    next_button = Button(figure.add_axes((0.68, 0.035, 0.13, 0.06)), "Kovetkezo")
    reset_button = Button(figure.add_axes((0.83, 0.035, 0.13, 0.06)), "Ujrakezdes")

    def next_frame(_event=None):
        nonlocal current_frame
        current_frame = min(current_frame + 1, total_frames - 1)
        update(current_frame)
        figure.canvas.draw_idle()

    def reset_simulation(_event=None):
        nonlocal current_frame
        current_frame = 0
        update(current_frame)
        figure.canvas.draw_idle()

    next_button.on_clicked(next_frame)
    reset_button.on_clicked(reset_simulation)
    figure._astar_animation = robot_animation
    figure._astar_controls = (next_button, reset_button)
    figure._astar_next_frame = next_frame
    figure._astar_reset = reset_simulation
    figure.canvas.mpl_connect(
        "key_press_event",
        lambda event: next_frame() if event.key in ("right", " ") else None,
    )
    if show:
        plt.show()
    return figure, robot_animation


def _run_simulation(settings, show=True):
    """A megadott beallitasokkal lefuttatja a szimulaciot."""
    grid_map, start, goal = create_demo_map(
        width=settings["width"],
        height=settings["height"],
        resolution=settings["resolution"],
        robot_radius=settings["robot_radius"],
        start=settings["start"],
        goal=settings["goal"],
    )
    result = astar_search(
        grid_map,
        start,
        goal,
        diagonal=settings["diagonal"],
        heuristic=settings["heuristic"],
        return_details=True,
    )
    if result["path"] is None:
        raise RuntimeError("A demo terkepen nincs elerheto utvonal.")
    original_path = result["path"]
    path = original_path
    if settings["smooth_path"]:
        path = smooth_path(grid_map, path, settings["diagonal"])
    trajectory = create_robot_trajectory(
        grid_map,
        path,
        smooth=settings["smooth_path"],
        diagonal=settings["diagonal"],
    )
    return plot_simulation(
        grid_map,
        path,
        trajectory,
        start,
        goal,
        expanded_nodes=result["expanded_nodes"],
        search_steps=result["search_steps"],
        original_path=original_path,
        auto_play=settings["auto_play"],
        show=show,
        smoothed=settings["smooth_path"],
    )


def run_simulation(show=True):
    """Beallitasi ablakot nyit, majd elinditja az A* szimulaciot."""
    simulation_figure = [None]

    def apply_settings(settings):
        if simulation_figure[0] is not None:
            plt.close(simulation_figure[0])
        simulation_figure[0], _ = _run_simulation(settings, show=False)

    settings_figure = _create_settings_window(apply_settings)
    if show:
        settings_figure.mainloop()
    return settings_figure


if __name__ == "__main__":
    run_simulation()
~~~~~

### codes_diploma/astar_project/astar_variants.py

~~~~~python
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


~~~~~

### codes_diploma/astar_project/compose_simulation_obstacle_avoidance.py

~~~~~python
"""Harom szimulacios kepkocka egyetlen, beillesztheto abrahoz."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from PIL import Image


FRAME_DIRECTORY = Path(__file__).resolve().parent / "results" / "figures"
FRAME_NAMES = (
    "simulation_02_frame_0100.png",
    "simulation_03_frame_0250.png",
    "simulation_04_frame_0500.png",
)
CROP_BOX = (570, 235, 1810, 1035)


def main():
    figure, axes = plt.subplots(1, 3, figsize=(18, 6), dpi=180)
    figure.subplots_adjust(wspace=0.03, left=0, right=1, top=1, bottom=0)

    for axis, filename in zip(axes, FRAME_NAMES):
        image_path = FRAME_DIRECTORY / filename
        if not image_path.exists():
            raise FileNotFoundError(f"Hianyzo szimulacios kepkocka: {image_path}")
        with Image.open(image_path) as source_image:
            grid_image = source_image.crop(CROP_BOX)
        axis.imshow(grid_image)
        axis.axis("off")

    output_path = FRAME_DIRECTORY / "simulation_obstacle_avoidance_sequence.png"
    figure.savefig(output_path, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    print(f"Abra mentve: {output_path}")


if __name__ == "__main__":
    main()

~~~~~

### codes_diploma/astar_project/experiments.py

~~~~~python
"""Reprodukálható A* összehasonlító kísérletek."""

import csv
import math
from pathlib import Path

from .astar_baseline import astar_search
from .astar_variants import HEURISTICS, get_heuristic
from .grid_map import GridMap


def _path_cost(path):
    """Kiszámítja a rácsútvonal költségét egyenes/átlós lépésekkel."""
    if not path:
        return None
    return sum(
        math.hypot(current[0] - previous[0], current[1] - previous[1])
        for previous, current in zip(path, path[1:])
    )


def build_experiment_scenarios():
    """Visszaadja azonos méretű, reprodukálható tesztpályákat.

    A pályák között van szabad tér, átjárót tartalmazó akadálypálya,
    sarokvágást tiltó eset és olyan pálya is, ahol átlós mozgás nélkül
    nincs megoldás.
    """
    scenarios = {}

    original_map = GridMap(width=30, height=20, resolution=0.2)
    vertical_column = 10
    horizontal_row = 12
    for row in range(2, 18):
        if row not in range(7, 13):
            original_map.add_obstacle(row, vertical_column)
    for column in range(12, 28):
        if column not in range(19, 25):
            original_map.add_obstacle(horizontal_row, column)
    scenarios["original_simulation"] = (original_map, (2, 2), (17, 27))

    compact_map = GridMap(width=10, height=7)
    for row in range(7):
        if row not in (2, 3):
            compact_map.add_obstacle(row, 3)
    for column in range(4, 9):
        if column not in (6, 7):
            compact_map.add_obstacle(4, column)
    scenarios["compact_corridor"] = (compact_map, (0, 0), (6, 9))

    corner_map = GridMap(width=5, height=5)
    corner_map.add_obstacle(1, 2)
    corner_map.add_obstacle(2, 1)
    scenarios["corner_cutting"] = (corner_map, (1, 1), (3, 3))

    diagonal_only_map = GridMap(width=3, height=3)
    diagonal_only_map.add_obstacle(0, 1)
    diagonal_only_map.add_obstacle(1, 0)
    diagonal_only_map.add_obstacle(1, 2)
    diagonal_only_map.add_obstacle(2, 1)
    scenarios["diagonal_only"] = (diagonal_only_map, (0, 0), (2, 2))

    return scenarios


def compare_heuristics(grid_map, start, goal, diagonal, heuristic_names=None):
    """Összeveti a heurisztikákat egyetlen pályán.

    A visszatérési lista minden eleme tartalmazza a heurisztika nevét,
    a talált útvonalat, annak költségét, a kibővített csomópontok számát
    és azt, hogy sikerült-e célt elérni.
    """
    names = list(heuristic_names or HEURISTICS)
    rows = []
    for name in names:
        heuristic = get_heuristic(name)
        result = astar_search(
            grid_map,
            start,
            goal,
            diagonal=diagonal,
            heuristic=heuristic,
            return_details=True,
        )
        path = result["path"]
        rows.append(
            {
                "heuristic": name,
                "diagonal": diagonal,
                "success": path is not None,
                "path_cost": _path_cost(path),
                "path_length": len(path) if path is not None else None,
                "expanded_nodes": len(result["expanded_nodes"]),
                "path": path,
            }
        )
    return rows


def run_scenario_comparison(heuristic_names=None):
    """Minden pályát lefuttat átlós és nem átlós módban."""
    rows = []
    for scenario_name, (grid_map, start, goal) in build_experiment_scenarios().items():
        for diagonal in (False, True):
            for row in compare_heuristics(
                grid_map, start, goal, diagonal, heuristic_names
            ):
                rows.append({"scenario": scenario_name, **row})
    return rows


def write_results(rows, output_path):
    """CSV-be menti a kísérleti eredményeket, útvonal nélkül."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "scenario",
        "heuristic",
        "diagonal",
        "success",
        "path_cost",
        "path_length",
        "expanded_nodes",
    ]
    with output_path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row[field] for field in fields})

~~~~~

### codes_diploma/astar_project/generate_comparison_figures.py

~~~~~python
"""Pontokkal es vonalstilusokkal jelolt heurisztika-abra generalasa."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from .astar_baseline import astar_search
from .astar_variants import HEURISTICS, get_heuristic
from .experiments import _path_cost, build_experiment_scenarios


COLORS = {
    "manhattan": "#0072B2",
    "euclidean": "#E69F00",
    "chebyshev": "#009E73",
    "octile": "#CC79A7",
}


def _draw_scenario(grid_map, start, goal, output_path):
    figure, axes = plt.subplots(1, 2, figsize=(17, 8), dpi=180)
    for axis, diagonal, title in (
        (axes[0], False, "Négyirányú mozgás"),
        (axes[1], True, "Átlós mozgás is engedélyezett"),
    ):
        for row in range(grid_map.height):
            for column in range(grid_map.width):
                if grid_map.grid[row][column] == 1:
                    axis.add_patch(
                        Rectangle(
                            (column * grid_map.resolution, row * grid_map.resolution),
                            grid_map.resolution,
                            grid_map.resolution,
                            facecolor="#455A64",
                            edgecolor="none",
                            zorder=1,
                        )
                    )
        for row in range(grid_map.height + 1):
            axis.axhline(
                row * grid_map.resolution,
                color="#78909C",
                linewidth=0.65,
                alpha=0.75,
                zorder=0,
            )
        for column in range(grid_map.width + 1):
            axis.axvline(
                column * grid_map.resolution,
                color="#78909C",
                linewidth=0.65,
                alpha=0.75,
                zorder=0,
            )
        for heuristic_name in HEURISTICS:
            color = COLORS[heuristic_name]
            result = astar_search(
                grid_map,
                start,
                goal,
                diagonal=diagonal,
                heuristic=get_heuristic(heuristic_name),
                return_details=True,
            )
            path = result["path"]
            if path is None:
                continue
            world_path = [
                grid_map.grid_to_world(row, column)
                for row, column in path
            ]
            path_x = [x for x, _ in world_path]
            path_y = [y for _, y in world_path]
            cost = _path_cost(path)
            label = f"{heuristic_name.title()}: {cost:.2f}"
            line, = axis.plot(
                path_x,
                path_y,
                color=color,
                linestyle="--",
                dashes=(3, 2),
                marker="o",
                markersize=2.4,
                markeredgewidth=0.45,
                markeredgecolor="white",
                linewidth=1.8,
                alpha=0.92,
                label=label,
                zorder=4,
            )

        start_x, start_y = grid_map.grid_to_world(*start)
        goal_x, goal_y = grid_map.grid_to_world(*goal)
        axis.scatter(
            [start_x], [start_y], s=90, marker="o",
            facecolor="#00A651", edgecolor="white", linewidth=2, zorder=5,
        )
        axis.scatter(
            [goal_x], [goal_y], s=110, marker="*",
            facecolor="#E31B23", edgecolor="white", linewidth=1.5, zorder=5,
        )
        axis.text(
            start_x, start_y, "S", color="white", ha="center",
            va="center", weight="bold", zorder=6,
        )
        axis.text(
            goal_x, goal_y, "G", color="white", ha="center",
            va="center", weight="bold", zorder=6,
        )
        axis.set_title(title, fontsize=15, weight="bold")
        axis.set_xlabel("x [m]")
        axis.set_ylabel("y [m]")
        axis.set_xlim(0, grid_map.width * grid_map.resolution)
        axis.set_ylim(0, grid_map.height * grid_map.resolution)
        axis.set_aspect("equal")
        axis.legend(
            loc="lower left",
            fontsize=8,
            framealpha=0.92,
            title="Heurisztika: költség",
        )

    figure.suptitle(
        "A* heurisztikák az eredeti szimulációs térképen",
        fontsize=18,
        weight="bold",
    )
    figure.tight_layout(rect=(0, 0.10, 1, 0.94))
    figure.savefig(output_path, bbox_inches="tight")
    plt.close(figure)


def main():
    output_directory = (
        Path(__file__).resolve().parent / "results" / "figures"
    )
    output_directory.mkdir(parents=True, exist_ok=True)
    original_map, start, goal = build_experiment_scenarios()[
        "original_simulation"
    ]
    _draw_scenario(
        original_map,
        start,
        goal,
        output_directory / "heuristics_original_simulation.png",
    )
    print(f"Abraak mentve: {output_directory}")


if __name__ == "__main__":
    main()

~~~~~

### codes_diploma/astar_project/generate_simulation_heuristic_comparison.py

~~~~~python
"""A valodi A*+DWA szimulacios terkep osszehasonlito abrazolasa."""

import importlib.util
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.patheffects as patheffects
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from .astar_variants import HEURISTICS, get_heuristic
from .experiments import _path_cost
from .. import simulation


COLORS = {
    "manhattan": "#0057B8",
    "euclidean": "#F28E00",
    "chebyshev": "#009E73",
    "octile": "#D81B60",
}

LINESTYLES = {
    "manhattan": "-",
    "euclidean": "--",
    "chebyshev": "-.",
    "octile": ":",
}


def _load_planner_class():
    file_path = Path(simulation.__file__).with_name("DWA+A.py")
    spec = importlib.util.spec_from_file_location("dwa_a_comparison", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.AStarDWAPlanner


def _draw_map(axis, grid_map):
    for row in range(grid_map.height):
        for column in range(grid_map.width):
            if grid_map.grid[row][column] == 1:
                axis.add_patch(
                    Rectangle(
                        (
                            column * grid_map.resolution,
                            row * grid_map.resolution,
                        ),
                        grid_map.resolution,
                        grid_map.resolution,
                        facecolor="#455A64",
                        edgecolor="none",
                        zorder=1,
                    )
                )
    for row in range(grid_map.height + 1):
        axis.axhline(
            row * grid_map.resolution,
            color="#78909C",
            linewidth=0.65,
            alpha=0.75,
            zorder=0,
        )
    for column in range(grid_map.width + 1):
        axis.axvline(
            column * grid_map.resolution,
            color="#78909C",
            linewidth=0.65,
            alpha=0.75,
            zorder=0,
        )


def _draw_paths(axis, grid_map, start_cell, goal_cell, diagonal):
    for heuristic_name in HEURISTICS:
        _draw_path(
            axis,
            grid_map,
            start_cell,
            goal_cell,
            diagonal,
            heuristic_name,
        )


def _draw_path(axis, grid_map, start_cell, goal_cell, diagonal, heuristic_name):
    planner_class = _load_planner_class()
    start = grid_map.grid_to_world(*start_cell)
    goal = grid_map.grid_to_world(*goal_cell)
    heuristic = get_heuristic(heuristic_name)
    planner = planner_class(
        grid_map,
        config=simulation.robotconfig(),
        diagonal=diagonal,
    )
    path = planner.plan_global(
        start,
        goal,
        heuristic=heuristic,
        smooth=False,
    )
    if path:
        path_x, path_y = zip(*path)
        grid_path = [grid_map.world_to_grid(x, y) for x, y in path]
        cost = _path_cost(grid_path)
        axis.plot(
            path_x,
            path_y,
            color=COLORS[heuristic_name],
            linestyle=LINESTYLES[heuristic_name],
            linewidth=2.8,
            alpha=1.0,
            marker="o",
            markersize=2.8,
            markeredgewidth=0.7,
            markeredgecolor="#FFFFFF",
            label=f"{heuristic_name.title()}: {cost:.2f}",
            zorder=4,
            path_effects=[
                patheffects.Stroke(linewidth=5.0, foreground="#FFFFFF"),
                patheffects.Normal(),
            ],
        )


def main():
    grid_map, start_cell, goal_cell, *_ = simulation.create_scene(
        width=30,
        height=20,
        resolution=0.2,
        start_cell=(2, 2),
        goal_cell=(17, 27),
        inflation_radius=0.1,
    )
    matplotlib.use("Agg", force=True)
    figure, axes = plt.subplots(1, 2, figsize=(17, 8), dpi=180)
    for axis, diagonal, title in (
        (axes[0], False, "Négyirányú A* + DWA"),
        (axes[1], True, "Átlós A* + DWA"),
    ):
        _draw_map(axis, grid_map)
        _draw_paths(axis, grid_map, start_cell, goal_cell, diagonal)
        start_x, start_y = grid_map.grid_to_world(*start_cell)
        goal_x, goal_y = grid_map.grid_to_world(*goal_cell)
        axis.scatter(
            [start_x],
            [start_y],
            s=90,
            color="#00A651",
            edgecolors="white",
            linewidths=1.5,
            zorder=6,
        )
        axis.scatter(
            [goal_x],
            [goal_y],
            s=110,
            marker="*",
            color="#E31B23",
            edgecolors="white",
            linewidths=1.2,
            zorder=6,
        )
        axis.set_title(title, fontsize=15, weight="bold")
        axis.set_xlabel("x [m]")
        axis.set_ylabel("y [m]")
        axis.set_xlim(0, grid_map.width * grid_map.resolution)
        axis.set_ylim(0, grid_map.height * grid_map.resolution)
        axis.set_aspect("equal")
        axis.legend(
            loc="upper center",
            bbox_to_anchor=(0.5, -0.10),
            ncol=2,
            fontsize=8,
            framealpha=0.92,
            title="Heurisztika: költség",
        )

    figure.suptitle(
        "A*+DWA útvonalak az eredeti, inflált szimulációs térképen",
        fontsize=18,
        weight="bold",
    )
    figure.tight_layout(rect=(0, 0.06, 1, 0.94))
    output_path = (
        Path(__file__).resolve().parent
        / "results"
        / "figures"
        / "simulation_heuristic_comparison.png"
    )
    figure.savefig(output_path, bbox_inches="tight")
    plt.close(figure)
    print(f"Abra mentve: {output_path}")


if __name__ == "__main__":
    main()

~~~~~

### codes_diploma/astar_project/grid_map.py

~~~~~python
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

~~~~~

### codes_diploma/astar_project/metrics.py

~~~~~python
"""Path quality and experiment performance metrics."""

~~~~~

### codes_diploma/astar_project/path_smoothing.py

~~~~~python
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
~~~~~

### codes_diploma/astar_project/plots.py

~~~~~python
"""Plotting helpers for maps, paths, and comparisons."""

~~~~~

### codes_diploma/astar_project/run_experiment.py

~~~~~python
"""Parancssori belépési pont az A* összehasonlító kísérletekhez."""

from pathlib import Path

from .experiments import run_scenario_comparison, write_results


if __name__ == "__main__":
    output = (
        Path(__file__).resolve().parent
        / "results"
        / "tables"
        / "heuristic_comparison.csv"
    )
    rows = run_scenario_comparison()
    write_results(rows, output)
    print(f"{len(rows)} eredmény mentve: {output}")

~~~~~

### codes_diploma/astar_project/scenarios.py

~~~~~python
"""Reproducible map and planning scenarios."""

~~~~~

### codes_diploma/astar_project/tests/test_astar_baseline.py

~~~~~python
"""A klasszikus A* alapviselkedésének tesztjei."""

import math
import unittest

from codes_diploma.astar_project.astar_baseline import astar_search
from codes_diploma.astar_project.astar_variants import (
	chebyshev,
	euclidean,
	get_heuristic,
	manhattan,
	octile,
)
from codes_diploma.astar_project.grid_map import GridMap


class TestAstarSearch(unittest.TestCase):
	def test_heuristics_can_be_selected(self):
		self.assertEqual(manhattan((0, 0), (2, 3)), 5)
		self.assertAlmostEqual(euclidean((0, 0), (2, 3)), math.sqrt(13))
		self.assertEqual(chebyshev((0, 0), (2, 3)), 3)
		self.assertAlmostEqual(octile((0, 0), (2, 3)), 3 + 2 * (math.sqrt(2) - 1))
		self.assertIs(get_heuristic("octile"), octile)

	def test_custom_heuristic_can_be_passed(self):
		grid_map = GridMap(width=4, height=1)

		path = astar_search(
			grid_map,
			(0, 0),
			(0, 3),
			heuristic=lambda position, goal: 0,
		)

		self.assertEqual(path, [(0, 0), (0, 1), (0, 2), (0, 3)])

	def test_finds_straight_path(self):
		grid_map = GridMap(width=4, height=1)

		path = astar_search(grid_map, (0, 0), (0, 3))

		self.assertEqual(path, [(0, 0), (0, 1), (0, 2), (0, 3)])

	def test_avoids_obstacle(self):
		grid_map = GridMap(width=5, height=3)
		grid_map.add_obstacle(1, 2)

		path = astar_search(grid_map, (1, 0), (1, 4))

		self.assertIsNotNone(path)
		self.assertNotIn((1, 2), path)
		self.assertEqual(path[0], (1, 0))
		self.assertEqual(path[-1], (1, 4))

	def test_returns_none_when_goal_is_unreachable(self):
		grid_map = GridMap(width=3, height=3)
		for row, column in ((0, 1), (1, 0), (1, 2), (2, 1)):
			grid_map.add_obstacle(row, column)

		path = astar_search(grid_map, (0, 0), (2, 2))

		self.assertIsNone(path)

	def test_diagonal_motion_uses_diagonal_neighbors(self):
		grid_map = GridMap(width=3, height=3)

		path = astar_search(grid_map, (0, 0), (2, 2), diagonal=True)

		self.assertEqual(path, [(0, 0), (1, 1), (2, 2)])

	def test_detailed_result_contains_neighbors_for_each_search_step(self):
		grid_map = GridMap(width=3, height=1)

		result = astar_search(
			grid_map,
			(0, 0),
			(0, 2),
			return_details=True,
		)

		self.assertEqual(result["search_steps"][0]["current"], (0, 0))
		self.assertEqual(result["search_steps"][0]["neighbors"], [(0, 1)])
		self.assertEqual(result["search_steps"][0]["neighbor_scores"][0]["g"], 1.0)
		self.assertEqual(result["search_steps"][0]["neighbor_scores"][0]["h"], 1.0)
		self.assertEqual(result["search_steps"][0]["neighbor_scores"][0]["f"], 2.0)
		self.assertEqual(result["search_steps"][0]["next_position"], (0, 1))
		self.assertEqual(result["search_steps"][0]["priority_queue"][0]["position"], (0, 1))
		self.assertEqual(result["search_steps"][0]["priority_queue"][0]["f"], 2.0)

	def test_rejects_blocked_start_or_goal(self):
		grid_map = GridMap(width=2, height=2)
		grid_map.add_obstacle(0, 0)

		with self.assertRaises(ValueError):
			astar_search(grid_map, (0, 0), (1, 1))


if __name__ == "__main__":
	unittest.main()

~~~~~

### codes_diploma/astar_project/tests/test_astar_simulation.py

~~~~~python
"""Teszt a statikus A* matplotlib szimulaciohoz."""

import unittest

from codes_diploma.astar_project.astar_baseline import astar_search
from codes_diploma.astar_project.astar_simulation import (
    _parse_position,
    create_demo_map,
    create_robot_trajectory,
    plot_simulation,
)
from codes_diploma.astar_project.path_smoothing import bezier_curve_points


class TestAstarSimulation(unittest.TestCase):
    def test_position_input_is_read_as_row_and_column(self):
        self.assertEqual(_parse_position(" 2, 17 "), (2, 17))

    def test_demo_map_has_a_valid_static_path(self):
        grid_map, start, goal = create_demo_map()

        path = astar_search(grid_map, start, goal, diagonal=True)

        self.assertIsNotNone(path)
        self.assertEqual(path[0], start)
        self.assertEqual(path[-1], goal)
        self.assertTrue(all(grid_map.is_free(row, column) for row, column in path))

    def test_demo_path_creates_continuous_smoothing_points(self):
        grid_map, start, goal = create_demo_map()
        path = astar_search(grid_map, start, goal, diagonal=True)

        curve = bezier_curve_points(path)

        self.assertEqual(curve[0], path[0])
        self.assertEqual(curve[-1], path[-1])
        self.assertNotEqual(curve, path)

    def test_robot_trajectory_starts_and_ends_at_path_points(self):
        grid_map, start, goal = create_demo_map()
        path = astar_search(grid_map, start, goal)

        trajectory = create_robot_trajectory(grid_map, path, steps_per_cell=4)

        self.assertEqual(trajectory[0], grid_map.grid_to_world(*start))
        self.assertEqual(trajectory[-1], grid_map.grid_to_world(*goal))
        self.assertEqual(len(trajectory), 1 + (len(path) - 1) * 4)

    def test_plot_simulation_can_be_created_without_showing_window(self):
        grid_map, start, goal = create_demo_map()
        path = astar_search(grid_map, start, goal)
        trajectory = create_robot_trajectory(grid_map, path)

        figure, robot_animation = plot_simulation(
            grid_map,
            path,
            trajectory,
            start,
            goal,
            show=False,
        )

        self.assertIsNotNone(figure)
        self.assertIsNotNone(robot_animation)
        figure.clf()

    def test_plot_uses_smoothed_trajectory_when_enabled(self):
        grid_map = create_demo_map(width=5, height=5)[0]
        path = [(0, 0), (0, 2), (2, 2)]
        trajectory = create_robot_trajectory(
            grid_map, path, smooth=True, diagonal=True
        )

        figure, _ = plot_simulation(
            grid_map,
            path,
            trajectory,
            path[0],
            path[-1],
            show=False,
            smoothed=True,
        )

        smoothed_line = next(
            line
            for line in figure.axes[1].lines
            if line.get_label() == "Bezier-simitott utvonal"
        )
        self.assertEqual(list(zip(*smoothed_line.get_data())), trajectory)
        figure.clf()

    def test_next_button_advances_the_current_search_cell(self):
        grid_map, start, goal = create_demo_map()
        result = astar_search(
            grid_map,
            start,
            goal,
            diagonal=True,
            return_details=True,
        )
        trajectory = create_robot_trajectory(grid_map, result["path"])

        figure, _ = plot_simulation(
            grid_map,
            result["path"],
            trajectory,
            start,
            goal,
            expanded_nodes=result["expanded_nodes"],
            search_steps=result["search_steps"],
            show=False,
        )

        map_axes = figure.axes[1]
        current_search = next(
            artist
            for artist in map_axes.collections
            if artist.get_label() == "C: aktualis cella"
        )
        first_position = tuple(current_search.get_offsets()[0])
        figure._astar_next_frame()
        second_position = tuple(current_search.get_offsets()[0])

        self.assertNotEqual(first_position, second_position)
        figure.clf()


if __name__ == "__main__":
    unittest.main()

~~~~~

### codes_diploma/astar_project/tests/test_dwa_a.py

~~~~~python
"""A DWA+A.py A*–DWA illesztésének tesztjei."""

import importlib.util
import pathlib
import unittest

from codes_diploma.astar_project.grid_map import GridMap
from codes_diploma.robot import robotconfig, robotstate


def point_to_path_distance(point, path):
	minimum = float("inf")
	for start, end in zip(path, path[1:]):
		dx = end[0] - start[0]
		dy = end[1] - start[1]
		length_squared = dx * dx + dy * dy
		if length_squared == 0:
			projection = start
		else:
			ratio = max(0.0, min(1.0, ((point[0] - start[0]) * dx + (point[1] - start[1]) * dy) / length_squared))
			projection = (start[0] + ratio * dx, start[1] + ratio * dy)
		minimum = min(minimum, ((point[0] - projection[0]) ** 2 + (point[1] - projection[1]) ** 2) ** 0.5)
	return minimum


def load_planner_class():
	file_path = pathlib.Path(__file__).parents[2] / "DWA+A.py"
	spec = importlib.util.spec_from_file_location("dwa_a_module", file_path)
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module.AStarDWAPlanner


class TestDwaA(unittest.TestCase):
	def test_astar_path_becomes_waypoints_and_dwa_pair(self):
		planner_class = load_planner_class()
		grid_map = GridMap(width=5, height=1, resolution=1.0)
		planner = planner_class(grid_map, config=robotconfig(), diagonal=False)

		path = planner.plan_global((0.1, 0.1), (4.1, 0.1))
		result = planner.plan_local(robotstate(x=0.5, y=0.5))

		self.assertEqual(len(path), 5)
		self.assertIn(result["target"], planner.waypoints)
		self.assertEqual(result["target"], planner.waypoints[planner.waypoint_index])
		self.assertEqual(len(result["best_pair"]), 4)
		self.assertTrue(all(
			point_to_path_distance(point, planner.bezier_path) < 1e-9
			for point in planner.waypoints
		))

	def test_waypoint_changes_only_after_reaching_active_point(self):
		planner_class = load_planner_class()
		grid_map = GridMap(width=5, height=1, resolution=1.0)
		planner = planner_class(grid_map, config=robotconfig(), diagonal=False, waypoint_tolerance=0.1)
		planner.plan_global((0.1, 0.1), (4.1, 0.1), smooth=False)

		planner.plan_local(robotstate(x=0.5, y=0.5))
		self.assertEqual(planner.waypoint_index, 1)

		active_waypoint = planner.waypoints[planner.waypoint_index]
		planner.plan_local(robotstate(x=active_waypoint[0], y=active_waypoint[1]))
		self.assertEqual(planner.waypoint_index, 2)

	def test_goal_returns_stop_command(self):
		planner_class = load_planner_class()
		grid_map = GridMap(width=3, height=1, resolution=1.0)
		planner = planner_class(grid_map, config=robotconfig(), diagonal=False)
		planner.plan_global((0.1, 0.1), (2.1, 0.1), smooth=False)

		goal = planner.waypoints[-1]
		result = planner.plan_local(robotstate(x=goal[0], y=goal[1]))

		self.assertTrue(result["finished"])
		self.assertEqual(result["best_pair"], [0.0, 0.0, 0.0, 0.0])


if __name__ == "__main__":
	unittest.main()
~~~~~

### codes_diploma/astar_project/tests/test_dynamic_obstacle_crossing.py

~~~~~python
"""Deterministikus teszt oldalrol keresztezo mozgo akadallyal."""

import unittest

from codes_diploma.DWA import optimisation
from codes_diploma.robot import Goal, Obstacle, robotconfig, robotstate


class TestDynamicObstacleCrossing(unittest.TestCase):
	def test_dwa_reacts_to_crossing_obstacle(self):
		config = robotconfig()
		state = robotstate(x=0.5, y=0.0, irany=0.0)
		goal = Goal(3.0, 0.0)

		clear_pair, _ = optimisation(config, state, goal, [])
		crossing_obstacle = Obstacle(1.5, -0.5, radius=0.15, vx=0.0, vy=0.2)
		obstacle_pair, safe_pairs = optimisation(config, state, goal, [crossing_obstacle])

		self.assertIsNotNone(clear_pair)
		self.assertIsNotNone(obstacle_pair)
		self.assertTrue(safe_pairs)
		self.assertLess(obstacle_pair[0], clear_pair[0])
		self.assertGreaterEqual(obstacle_pair[0], 0.0)


if __name__ == "__main__":
	unittest.main()
~~~~~

### codes_diploma/astar_project/tests/test_experiments.py

~~~~~python
"""Az A* heurisztika- és mozgásmód-összehasonlítás tesztjei."""

import unittest

from codes_diploma.astar_project.experiments import (
    build_experiment_scenarios,
    compare_heuristics,
    run_scenario_comparison,
)


class TestExperiments(unittest.TestCase):
    def test_all_heuristics_are_compared_in_both_motion_modes(self):
        rows = run_scenario_comparison()

        self.assertEqual(len(rows), 4 * 2 * 4)
        self.assertEqual(
            {row["heuristic"] for row in rows},
            {"manhattan", "euclidean", "chebyshev", "octile"},
        )
        self.assertEqual({row["diagonal"] for row in rows}, {False, True})

    def test_non_diagonal_mode_rejects_diagonal_only_map(self):
        grid_map, start, goal = build_experiment_scenarios()["diagonal_only"]

        rows = compare_heuristics(grid_map, start, goal, diagonal=False)

        self.assertTrue(all(not row["success"] for row in rows))

    def test_corner_cutting_is_not_used_when_diagonal_is_enabled(self):
        grid_map, start, goal = build_experiment_scenarios()["corner_cutting"]

        rows = compare_heuristics(grid_map, start, goal, diagonal=True)

        self.assertTrue(all(row["success"] for row in rows))
        for row in rows:
            self.assertNotIn((2, 2), row["path"])


if __name__ == "__main__":
    unittest.main()

~~~~~

### codes_diploma/astar_project/tests/test_grid_map.py

~~~~~python
"""A GridMap alapmuveleteinek tesztjei."""

import unittest

from codes_diploma.astar_project.grid_map import GridMap


class TestGridMap(unittest.TestCase):
	def test_diagonal_corner_cutting_is_rejected(self):
		grid_map = GridMap(width=3, height=3)
		grid_map.add_obstacle(0, 1)
		grid_map.add_obstacle(1, 0)

		neighbors = grid_map.get_neighbors(0, 0, diagonal=True)

		self.assertNotIn((1, 1), neighbors)

	def test_inflate_obstacles_marks_nearby_cells(self):
		grid_map = GridMap(width=5, height=5, resolution=0.1)
		grid_map.add_obstacle(2, 2)

		grid_map.inflate_obstacles(0.1)

		self.assertEqual(grid_map.grid[1][1], 1)
		self.assertEqual(grid_map.grid[3][3], 1)
		self.assertTrue(grid_map.is_free(0, 0))


if __name__ == "__main__":
	unittest.main()

~~~~~

### codes_diploma/astar_project/tests/test_path_smoothing.py

~~~~~python
"""Az utvonal-simitas tesztjei."""

import unittest

from codes_diploma.astar_project.grid_map import GridMap
from codes_diploma.astar_project.path_smoothing import (
	_is_path_safe,
	_cut_point,
	bezier_curve_points,
	smooth_path,
)


class TestPathSmoothing(unittest.TestCase):
	def test_keeps_a_straight_path_unchanged(self):
		grid_map = GridMap(width=5, height=1)
		path = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]

		self.assertEqual(smooth_path(grid_map, path), path)

	def test_creates_a_bezier_path_between_turning_points(self):
		grid_map = GridMap(width=5, height=5)

		path = smooth_path(grid_map, [(0, 0), (0, 2), (2, 2)], diagonal=True)

		self.assertEqual(path[0], (0, 0))
		self.assertEqual(path[-1], (2, 2))
		self.assertTrue(
			all(
				grid_map.is_free(round(row), round(column))
				for row, column in path
			)
		)

	def test_uses_all_points_in_a_dynamic_order_curve(self):
		grid_map = GridMap(width=5, height=5)
		path = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]

		smoothed_path = smooth_path(grid_map, path, diagonal=True)
		curve = bezier_curve_points(path, samples_per_segment=15)

		self.assertEqual(smoothed_path[0], path[0])
		self.assertEqual(smoothed_path[-1], path[-1])
		self.assertGreater(len(curve), len(path))
		self.assertNotEqual(curve[1], path[1])

	def test_keeps_a_path_around_an_obstacle(self):
		grid_map = GridMap(width=5, height=3)
		grid_map.add_obstacle(1, 2)
		path = [(1, 0), (0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (1, 4)]

		result = smooth_path(grid_map, path)

		self.assertEqual(result[0], path[0])
		self.assertEqual(result[-1], path[-1])
		self.assertNotIn((1, 2), result)

	def test_rejects_non_neighbor_jump(self):
		grid_map = GridMap(width=5, height=1)

		self.assertFalse(_is_path_safe(grid_map, [(0, 0), (0, 2)]))

	def test_bezier_cut_point_respects_maximum_distance(self):
		cut_point = _cut_point((0.0, 2.0), (0.0, 0.0), 1.5)

		self.assertAlmostEqual(cut_point[0], 0.0)
		self.assertAlmostEqual(cut_point[1], 0.5)


if __name__ == "__main__":
	unittest.main()

~~~~~

### codes_diploma/astar_project/tests/test_robot_and_dwa.py

~~~~~python
"""A robot.py és a DWA.py célzott tesztjei."""

import unittest

from codes_diploma.DWA import optimisation
from codes_diploma.robot import Obstacle, Goal, get_robot_kinematics, robotconfig, robotstate


class TestRobotAndDWA(unittest.TestCase):
	def test_robot_kinematics(self):
		config = robotconfig()
		linear, angular = get_robot_kinematics(10.0, 10.0, config)

		self.assertAlmostEqual(linear, 0.33)
		self.assertAlmostEqual(angular, 0.0)

	def test_original_parameters_are_preserved(self):
		config = robotconfig()

		self.assertEqual(config.r_kerek, 0.033)
		self.assertEqual(config.b, 0.08)
		self.assertEqual(config.w_kerek_max, 15)
		self.assertEqual(config.a_max, 2)
		self.assertEqual(config.dt, 0.1)
		self.assertEqual(config.predict_time, 3)
		self.assertEqual(config.rob_radius, 0.1)

	def test_dwa_returns_original_pair_format(self):
		best_pair, safe_pairs = optimisation(
			robotconfig(),
			robotstate(),
			Goal(2.0, 0.0),
			[],
		)

		self.assertIsNotNone(best_pair)
		self.assertTrue(safe_pairs)
		self.assertEqual(len(best_pair), 4)

	def test_moving_obstacle(self):
		obstacle = Obstacle(1.0, 2.0, radius=0.1, vx=0.5)

		obstacle.move(2.0)

		self.assertEqual((obstacle.x, obstacle.y), (2.0, 2.0))


if __name__ == "__main__":
	 unittest.main()
~~~~~

### codes_diploma/astar_project/tests/test_simulation.py

~~~~~python
"""A grafikus szimulacio grafika nelkuli tesztjei."""

import unittest

from codes_diploma.simulation import create_scene


class TestSimulation(unittest.TestCase):
	def test_scene_contains_static_and_moving_obstacles(self):
		grid_map, start_cell, goal_cell, start, goal, state, static_obstacles, dynamic_obstacles = create_scene()

		self.assertIsNotNone(grid_map)
		self.assertNotEqual(start, goal)
		self.assertTrue(static_obstacles)
		self.assertTrue(dynamic_obstacles)
		self.assertTrue(dynamic_obstacles[0].vx != 0.0 or dynamic_obstacles[0].vy != 0.0)


if __name__ == "__main__":
	unittest.main()
~~~~~

### codes_diploma/DWA.py

~~~~~python
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
~~~~~

### codes_diploma/DWA+A.py

~~~~~python
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
~~~~~

### codes_diploma/robot.py

~~~~~python
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
~~~~~

### codes_diploma/ros2_astar_dwa_gazebo/gazebo_topdown.config

~~~~~text
<?xml version="1.0"?>

<window>
  <width>1200</width>
  <height>800</height>
  <style material_theme="Light" material_primary="DeepOrange" material_accent="LightBlue" />
</window>

<plugin filename="MinimalScene" name="3D View">
  <gz-gui>
    <title>3D View</title>
    <property type="bool" key="showTitleBar">false</property>
    <property type="string" key="state">docked</property>
  </gz-gui>
  <engine>ogre2</engine>
  <scene>scene</scene>
  <ambient_light>0.6 0.6 0.6</ambient_light>
  <background_color>0.12 0.14 0.18</background_color>
  <camera_pose>4 2.5 8 0 1.5708 0</camera_pose>
</plugin>

<plugin filename="WorldControl" name="World control">
  <gz-gui>
    <title>World control</title>
    <property type="bool" key="showTitleBar">false</property>
    <property type="bool" key="resizable">false</property>
    <property type="double" key="height">72</property>
    <property type="string" key="state">floating</property>
    <anchors target="3D View">
      <line own="left" target="left" />
      <line own="bottom" target="bottom" />
    </anchors>
  </gz-gui>
  <play_pause>true</play_pause>
  <step>true</step>
  <start_paused>false</start_paused>
  <use_event>true</use_event>
</plugin>

<plugin filename="WorldStats" name="World stats">
  <gz-gui>
    <title>World stats</title>
    <property type="bool" key="showTitleBar">false</property>
    <property type="bool" key="resizable">false</property>
    <property type="double" key="height">80</property>
    <property type="double" key="width">260</property>
    <property type="string" key="state">floating</property>
    <anchors target="3D View">
      <line own="right" target="right" />
      <line own="bottom" target="bottom" />
    </anchors>
  </gz-gui>
  <sim_time>true</sim_time>
  <real_time>true</real_time>
  <real_time_factor>true</real_time_factor>
  <iterations>true</iterations>
</plugin>

<plugin filename="Screenshot" name="Screenshot">
  <gz-gui>
    <property key="resizable" type="bool">false</property>
    <property key="x" type="double">250</property>
    <property key="y" type="double">50</property>
    <property key="width" type="double">50</property>
    <property key="height" type="double">50</property>
    <property key="state" type="string">floating</property>
    <property key="showTitleBar" type="bool">false</property>
    <property key="cardBackground" type="string">#777777</property>
  </gz-gui>
</plugin>

~~~~~

### codes_diploma/ros2_astar_dwa_gazebo/README.md

~~~~~text
# Indítás három fázisban

**Először: előkészítés → 1. feltérképezés → 2. mentés → teljes leállítás → 3. mentett térképes indítás.**
Később csak az előkészítés és a **3. fázis** kell; ne fussanak párhuzamosan régi szimulációk.

## Előkészítés

**VS Code PowerShell: frissítés** – a pull a követett távoli ágból frissít, a merge önmagában nem tölt le semmit.

```powershell
Set-Location "C:\Users\Rum Dániel\Desktop\Diplomamunka"
git fetch --all
git switch cpp-rethink
git pull --ff-only
git log -1 --oneline
```

**WSL: build, csak kódfrissítés után** – a forrás frissítése nem építi újra a futó programot.

```bash
cd "/mnt/c/Users/Rum Dániel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo"
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src --rosdistro jazzy -r -y
ls -l src/dwa_gazebo_sim/config/slam.yaml
colcon build --symlink-install --packages-select astar_dwa_controller dwa_gazebo_sim
source install/setup.bash
ros2 pkg prefix dwa_gazebo_sim
ls -l "$(ros2 pkg prefix dwa_gazebo_sim)/share/dwa_gazebo_sim/config/slam.yaml"
```

**Ha `No such file .../config/slam.yaml` jelenik meg:** ez a csomag telepítési konfigurációja, nem a `~/maps/palya` mentés.
Ha már a `src/...` fájl hiányzik, előbb frissítsd a megfelelő klónt; ha csak az installból hiányzik, buildeld újra a fenti két csomagot.
Csak sikeres build és a második `ls` által megtalált fájl után indítsd a 3. fázist; az üzenetben a `ros2 pkg prefix` a most buildelt workspace-re mutasson.
A mentett térképet emiatt nem kell újraépíteni vagy felülírni; ha a fájl továbbra is hiányzik, a teljes buildkimenetet küldd vissza.

**Ha a build egy már törölt `robot_controller.launch.py` fájlt akar másolni:** régi generált symlink maradt a buildben; állítsd le a futásokat, frissítsd a kódot, majd új WSL-terminálban:

```bash
cd "/mnt/c/Users/Rum Dániel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo"
source /opt/ros/jazzy/setup.bash
if [ -d build/dwa_gazebo_sim ]; then mv -- build/dwa_gazebo_sim "build/dwa_gazebo_sim_backup_$(date +%Y%m%d_%H%M%S)"; fi
colcon build --symlink-install --packages-select astar_dwa_controller dwa_gazebo_sim
source install/setup.bash
ls -l "$(ros2 pkg prefix dwa_gazebo_sim)/share/dwa_gazebo_sim/config/slam.yaml"
```

Az átnevezés csak az érintett csomag generált buildjét teszi félre, a forrást és a `~/maps` mentést nem módosítja; ne hozd vissza a törölt launch-fájlt.
Csak sikeres build és megtalált `slam.yaml` után folytasd a **3. fázissal**, nem kell újra feltérképezni.

**Minden új WSL-terminál elején ezt futtasd**, a `~` mappából is működik:

```bash
source /opt/ros/jazzy/setup.bash
cd "/mnt/c/Users/Rum Dániel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo"
source install/setup.bash
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
export DISPLAY=:0
export QT_QPA_PLATFORM=xcb
export QT_X11_NO_MITSHM=1
export XDG_RUNTIME_DIR=/tmp/gazebo-runtime
mkdir -p "$XDG_RUNTIME_DIR" results/diagnostics
chmod 700 "$XDG_RUNTIME_DIR"
```

Másik gépen az útvonalat cseréld a sajátodra, az idézőjeleket megtartva; hiba esetén állj meg.

## Tiszta újraindítás hiba után

1. Állítsd meg a robotot, majd Ctrl+C-vel zárd be a teleopot/plannert, az RViz-t és végül a Gazebo–SLAM futást.
2. Nyiss új WSL-terminált, és futtasd a fenti **Minden új WSL-terminál elején** blokkot.
3. Az alábbi paranccsal indíts új feltérképezést; ez az 1. fázis A termináljának indítása helyett használandó, ne indíts két szimulációt.

```bash
ros2 daemon stop
ros2 daemon start
ros2 launch dwa_gazebo_sim simulation.launch.py slam_mode:=mapping start_planner:=false map_resolution:=0.10 2>&1 | tee "results/diagnostics/mapping_$(date +%Y%m%d_%H%M%S).log"
```

Ezután az 1. fázis **B és C termináljával** folytasd: RViz, majd kézi mozgatás.
A daemon újraindítása nem állítja le a régi node-okat és nem hoz létre hiányzó TF-et; ezért szükséges előtte a Ctrl+C-s leállítás.
A `queue is full` nem megtelt tárhely: hiányzó/késő TF miatt is betelhet a mérések várakozási sora.
Ha friss indítás után is `odom ... does not exist` vagy tartós TF-hiba látszik, ne ments és ne indíts lokalizációt; küldd a `mapping_*.log` fájlt a `DIAG_TF`, `DIAG_ODOM` és SLAM sorokkal.

## 1. Feltérképezés

**A terminál: Gazebo + új SLAM-térkép** – a planner még nem vezérli a robotot.

```bash
ros2 launch dwa_gazebo_sim simulation.launch.py slam_mode:=mapping start_planner:=false map_resolution:=0.10 2>&1 | tee "results/diagnostics/mapping_$(date +%Y%m%d_%H%M%S).log"
```

**B terminál: RViz** – itt látod a feltérképezett területet; Fixed Frame: `map`.

```bash
ros2 launch dwa_gazebo_sim visualization.launch.py
```

**C terminál: kézi mozgatás** – az aktív teleop terminál billentyűivel lassan járd körbe a pályát.

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p speed:=0.15 -p turn:=0.5
```

**A térképnek az RViz-ben látszania és bővülnie kell.** Ha üres a nézet, `tf_missing`, `waiting_map` vagy tartós `queue is full` látszik, ne ments és ne indíts lokalizációt.

## 2. Mentés

**C terminál:** állítsd meg a robotot, majd Ctrl+C-vel zárd be a teleopot; az A és B terminál maradjon futva.

Először ellenőrizd, hogy valóban érkezik térkép:

```bash
ros2 lifecycle get /slam_toolbox
timeout 10s ros2 topic echo --once /map --field info
```

Elvárt: `active`, valamint pozitív `width` és `height`; ha nincs adat vagy hibát kapsz, állj meg és küldd az A terminál naplóját.

Ha már létezik régi `~/maps/palya` mentés, előbb másold el:

```bash
cp -a "$HOME/maps" "$HOME/maps_backup_$(date +%Y%m%d_%H%M%S)"
```

Ezután mentsd a térképképet:

```bash
mkdir -p "$HOME/maps"
MAP="$HOME/maps/palya"
ros2 run nav2_map_server map_saver_cli -f "$MAP" --ros-args -p save_map_timeout:=10.0
```

**Csak sikeres térképképmentés után** mentsd a folytatható SLAM-állapotot ugyanebben a terminálban:

```bash
ros2 service call /slam_toolbox/serialize_map slam_toolbox/srv/SerializePoseGraph "{filename: '$MAP'}"
ls -lh "$MAP"*
```

Eredmény: `.yaml` + térképkép és `.posegraph` + `.data`; a későbbi indítás a két utóbbit használja.
A serialize `result: 0` csak sikeres fájlkiírást jelent, nem bizonyít használható térképet.
**Sikeres mentés után állítsd le az A és B terminál futását is Ctrl+C-vel.**

## 3. Indítás a mentett térképpel

**A terminál: új Gazebo a kezdőhelyről + mentett térképes lokalizáció** – nem kell újra kézzel feltérképezni.

```bash
ros2 launch dwa_gazebo_sim simulation.launch.py slam_mode:=localization map_file:="$HOME/maps/palya" initial_x:=0.8 initial_y:=0.8 initial_yaw:=0.0 2>&1 | tee "results/diagnostics/localization_$(date +%Y%m%d_%H%M%S).log"
```

**B terminál: RViz és céladás** – megjeleníti a mentett térképet és a globális utat.

```bash
ros2 launch dwa_gazebo_sim visualization.launch.py
```

1. Ellenőrizd a robot térképbeli helyét; szükség esetén **2D Pose Estimate**-tel jelöld a helyét és irányát.
2. **2D Goal Pose:** ismert szabad helyen kattints, húzd meg az irányt, majd engedd el.
3. A robot az A*-út waypointjait követi DWA-val; ne indíts mellé teleopot vagy második plannert.

Az `initial_x/y/yaw` a mentett térképben adott becslés, nem a Gazebo robotjának áthelyezése; a példa nem garantálja a helyes lokalizációt.
A `map_file` kiterjesztés nélküli előtag: ugyanahhoz a mentéshez tartozó `.posegraph` és `.data` kell.
Az út RViz-ben és Gazebóban ugyanabból a `/astar_path`-ból rajzolódik; a Gazebo-illesztés csak vizualizáció, nem vezérlési visszacsatolás.

## Új térkép vagy felülírás

Állíts le minden futást, majd ismételd az **1. és 2. fázist**, a régi mentés biztonsági másolatával; ezután a **3. fázissal** indulj.
Lokalizációs módban a mentett térkép nem frissül automatikusan; a fájl felülírása nem cseréli le egy már futó node térképét.

## Csak hibakereséshez

Küldd vissza a `results/diagnostics/mapping_*.log` vagy `localization_*.log` fájlt az indulástól a hibáig; RViz-problémánál képernyőképet is.
Külön előkészített WSL-terminálban a következő parancsokat egyesével futtasd, a folyamatos kimenetet Ctrl+C-vel zárd le:

```bash
ros2 lifecycle get /slam_toolbox
ros2 run tf2_ros tf2_echo odom base_scan
ros2 run tf2_ros tf2_echo map odom
```

**Jelenlegi korlát:** a felhasználói naplóban az `odom` frame hiánya miatt nem épült térkép; a teljes ROS/Gazebo működés még nincs igazolva, a leírás átrendezése ezt nem javítja meg.

## TF-fa és rqt_graph – külön terminálokban

A Gazebo és a SLAM maradjon futva; minden alábbi eszközhöz új WSL-terminált nyiss, és először ezt futtasd:

```bash
source /opt/ros/jazzy/setup.bash
cd "/mnt/c/Users/Rum Dániel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo"
source install/setup.bash
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
export DISPLAY=:0
export QT_QPA_PLATFORM=xcb
export QT_X11_NO_MITSHM=1
export XDG_RUNTIME_DIR=/tmp/gazebo-runtime
mkdir -p "$XDG_RUNTIME_DIR" results/diagnostics
chmod 700 "$XDG_RUNTIME_DIR"
```

### TF-fa rajzolása és megnyitása

A koordinátakeretek geometriai kapcsolatait PDF-be menti és megnyitja.

```bash
cd results/diagnostics
ros2 run tf2_tools view_frames --output frames
xdg-open frames.pdf
```

### Élő TF-adatok

A robot térképbeli becsült helyzetét mutatja; néhány sor után Ctrl+C-vel állítható le.

```bash
ros2 run tf2_ros tf2_echo map base_link
```

Ha hibát jelez, külön-külön ellenőrizd a láncot, a parancsok között Ctrl+C-vel:

```bash
ros2 run tf2_ros tf2_echo odom base_scan
ros2 run tf2_ros tf2_echo map odom
```

### rqt_graph megnyitása

A ROS node-ok és topicok adatkapcsolatait rajzolja ki; ez nem a geometriai TF-fa.

```bash
ros2 run rqt_graph rqt_graph
```

Ha hiányzik valamelyik eszköz: `sudo apt install ros-jazzy-tf2-tools ros-jazzy-rqt-graph graphviz xdg-utils`.
~~~~~

### codes_diploma/ros2_astar_dwa_gazebo/src/astar_dwa_controller/CMakeLists.txt

~~~~~text
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
install(DIRECTORY config launch rviz DESTINATION share/${PROJECT_NAME})
ament_get_python_install_dir(PYTHON_INSTALL_DIR)
set(PYTHON_REFERENCE_SOURCE "${CMAKE_CURRENT_SOURCE_DIR}/../../..")
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

~~~~~

### codes_diploma/ros2_astar_dwa_gazebo/src/astar_dwa_controller/config/rosbot.yaml

~~~~~yaml
astar_dwa_node:
  ros__parameters:
    cmd_vel_topic: /cmd_vel
    odom_topic: /odom
    scan_topic: /scan
    goal_topic: /goal_pose
    path_topic: /astar_path
    goal_x: 0.0
    goal_y: 0.0
    known_obstacle_x: [2.1, 2.1, 2.1, 2.1, 2.1,  2.1, 2.1, 2.1, 2.1, 2.1,  2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0,  5.4, 5.6, 5.8, 6.0, 6.2, 6.4, 6.6, 6.8, 7.0, 7.2, 7.4, 7.6, 7.8, 8.0]
    known_obstacle_y: [0.5, 0.7, 0.9, 1.1, 1.3,  2.7, 2.9, 3.1, 3.3, 3.5,  2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5,  2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5]
    known_obstacle_radius: [0.10, 0.10, 0.10, 0.10, 0.10,  0.10, 0.10, 0.10, 0.10, 0.10,  0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10,  0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10]
    map_size: 8.2
    map_height: 5.2
    map_origin_x: -0.1
    map_origin_y: -0.1
    initial_pose_x: 0.0
    initial_pose_y: 0.0
    scan_offset_x: -0.064
    scan_offset_y: 0.0
    scan_offset_z: 0.121
    resolution: 0.20
    robot_radius: 0.24  # Megnövelve, hogy a robot hátulja is biztonságban legyen kikerüléskor!
    safety_margin: 0.10
    static_safety_margin: 0.04
    planning_margin: 0.15
    lookahead_distance: 0.40
    control_period: 0.10
    max_linear_velocity: 0.22  # Kicsit visszavéve a maximális sebességet a stabilabb kikerülésért
    max_angular_velocity: 1.00
    wheel_radius: 0.033
    wheel_base: 0.08
    wheel_max: 15.0
    wheel_resolution: 0.5
    acceleration_limit: 1.8
    predict_time: 2.0        # Biztonságosabb, hosszabb előrejelzési ablak
    min_ttc: 0.8
    gazebo_path_debug: true
    gazebo_world: dwa_world
    alpha: 5.0
    beta: 3.0
    gamma: 2.0
    path_distance_bias: 6.0
    goal_distance_bias: 2.0
    path_return_bias: 8.0
    path_return_tolerance: 0.10

~~~~~

### codes_diploma/ros2_astar_dwa_gazebo/src/astar_dwa_controller/launch/controller.launch.py

~~~~~python
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    package_share = get_package_share_directory("astar_dwa_controller")
    return LaunchDescription([
        Node(
            package="astar_dwa_controller",
            executable="astar_dwa_node",
            name="astar_dwa_node",
            output="screen",
            parameters=[
                os.path.join(package_share, "config", "rosbot.yaml"),
                {"use_sim_time": True},
            ],
        )
    ])

~~~~~

### codes_diploma/ros2_astar_dwa_gazebo/src/astar_dwa_controller/package.xml

~~~~~xml
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

~~~~~

### codes_diploma/ros2_astar_dwa_gazebo/src/astar_dwa_controller/rviz/astar_dwa.rviz

~~~~~yaml
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
        Depth: 5
        Durability Policy: Volatile
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

~~~~~

### codes_diploma/ros2_astar_dwa_gazebo/src/astar_dwa_controller/src/astar_dwa_node.cpp

~~~~~cpp
#include <algorithm>
#include <atomic>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <sstream>
#include <thread>
#include <functional>
#include <limits>
#include <memory>
#include <queue>
#include <string>
#include <utility>
#include <vector>

#include "geometry_msgs/msg/pose_stamped.hpp"
#include "geometry_msgs/msg/transform_stamped.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include "nav_msgs/msg/occupancy_grid.hpp"
#include "nav_msgs/msg/path.hpp"
#include "rclcpp/rclcpp.hpp"
#include "rclcpp/create_timer.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"
#include "tf2_ros/transform_broadcaster.h"
#include "visualization_msgs/msg/marker_array.hpp"
#include "path_tracking.hpp"

namespace {
struct Obstacle { double x, y, radius, vx{0.0}, vy{0.0}; };
struct Track { double x, y, vx, vy; };
struct Pose { double x{0.0}, y{0.0}, yaw{0.0}; };
double angle_error(double value) { return std::atan2(std::sin(value), std::cos(value)); }
double distance(double ax, double ay, double bx, double by) {
  return std::hypot(ax - bx, ay - by);
}
}  // namespace

class AStarDwaNode final : public rclcpp::Node {
public:
  AStarDwaNode() : Node("astar_dwa_node") {
    cmd_topic_ = declare_parameter("cmd_vel_topic", std::string("/cmd_vel"));
    odom_topic_ = declare_parameter("odom_topic", std::string("/odom"));
    scan_topic_ = declare_parameter("scan_topic", std::string("/scan"));
    goal_topic_ = declare_parameter("goal_topic", std::string("/goal_pose"));
    path_topic_ = declare_parameter("path_topic", std::string("/astar_path"));
    goal_x_ = declare_parameter("goal_x", 0.0);
    goal_y_ = declare_parameter("goal_y", 0.0);
    map_size_ = declare_parameter("map_size", 8.2);
    map_height_ = declare_parameter("map_height", 5.2);
    map_origin_x_ = declare_parameter("map_origin_x", 0.0);
    map_origin_y_ = declare_parameter("map_origin_y", 0.0);
    initial_pose_x_ = declare_parameter("initial_pose_x", 0.0);
    initial_pose_y_ = declare_parameter("initial_pose_y", 0.0);
    scan_offset_x_ = declare_parameter("scan_offset_x", 0.0);
    scan_offset_y_ = declare_parameter("scan_offset_y", 0.0);
    scan_offset_z_ = declare_parameter("scan_offset_z", 0.16);
    resolution_ = declare_parameter("resolution", 0.20);
    robot_radius_ = declare_parameter("robot_radius", 0.22);
    max_linear_velocity_ = declare_parameter("max_linear_velocity", 0.26);
    max_angular_velocity_ = declare_parameter("max_angular_velocity", 1.0);
    wheel_radius_ = declare_parameter("wheel_radius", 0.033);
    wheel_base_ = declare_parameter("wheel_base", 0.08);
    wheel_max_ = declare_parameter("wheel_max", 15.0);
    wheel_resolution_ = declare_parameter("wheel_resolution", 0.5);
    acceleration_limit_ = declare_parameter("acceleration_limit", 2.0);
    predict_time_ = declare_parameter("predict_time", 2.5);
    safety_margin_ = declare_parameter("safety_margin", 0.08);
    min_ttc_ = declare_parameter("min_ttc", 1.0);
    static_safety_margin_ = declare_parameter("static_safety_margin", 0.03);
    lookahead_distance_ = declare_parameter("lookahead_distance", 0.25);
    planning_margin_ = declare_parameter("planning_margin", 0.30);
    gazebo_path_debug_ = declare_parameter("gazebo_path_debug", true);
    gazebo_world_ = declare_parameter("gazebo_world", std::string("dwa_world"));
    alpha_ = declare_parameter("alpha", 5.0);
    beta_ = declare_parameter("beta", 2.0);
    gamma_ = declare_parameter("gamma", 3.0);
    path_distance_bias_ = declare_parameter("path_distance_bias", 6.0);
    goal_distance_bias_ = declare_parameter("goal_distance_bias", 2.0);
    path_return_bias_ = declare_parameter("path_return_bias", 8.0);
    path_return_tolerance_ = declare_parameter("path_return_tolerance", 0.10);
    known_obstacle_x_ = declare_parameter("known_obstacle_x", std::vector<double>{});
    known_obstacle_y_ = declare_parameter("known_obstacle_y", std::vector<double>{});
    known_obstacle_radius_ = declare_parameter("known_obstacle_radius", std::vector<double>{});
    const double period = declare_parameter("control_period", 0.10);
    dt_ = period;
    cmd_pub_ = create_publisher<geometry_msgs::msg::Twist>(cmd_topic_, 10);
    path_pub_ = create_publisher<nav_msgs::msg::Path>(path_topic_, 10);
    map_pub_ = create_publisher<nav_msgs::msg::OccupancyGrid>(
      "/astar_map", rclcpp::QoS(1).transient_local().reliable());
    marker_pub_ = create_publisher<visualization_msgs::msg::MarkerArray>("/astar_dwa_markers", 10);
    tf_broadcaster_ = std::make_unique<tf2_ros::TransformBroadcaster>(*this);
    odom_sub_ = create_subscription<nav_msgs::msg::Odometry>(
      odom_topic_, 10, [this](nav_msgs::msg::Odometry::ConstSharedPtr msg) { odom(msg); });
    scan_sub_ = create_subscription<sensor_msgs::msg::LaserScan>(
      scan_topic_, 10, [this](sensor_msgs::msg::LaserScan::ConstSharedPtr msg) { scan(msg); });
    goal_sub_ = create_subscription<geometry_msgs::msg::PoseStamped>(
      goal_topic_, 10, [this](geometry_msgs::msg::PoseStamped::ConstSharedPtr msg) {
        goal_x_ = msg->pose.position.x; goal_y_ = msg->pose.position.y;
        has_goal_ = true;
        blocked_cycles_ = 0;
        returning_to_path_ = false;
        rejoin_active_ = false;
        need_replan_ = true;
        RCLCPP_INFO(get_logger(), "Uj cel: x=%.2f m, y=%.2f m", goal_x_, goal_y_); });
    timer_ = rclcpp::create_timer(
      this, get_clock(), rclcpp::Duration::from_seconds(period), [this]() { control(); });
    RCLCPP_INFO(get_logger(), "A* + DWA: cpp-world-pose-scan-tracking-v2");
  }

  ~AStarDwaNode() override {
    if (debug_thread_.joinable()) debug_thread_.join();
  }

private:
  std::string build_path_sdf(const std::vector<std::pair<double, double>> & path) const {
    std::ostringstream s;
    s.precision(4);
    s << std::fixed;
    s << "<?xml version=\"1.0\"?>\n<sdf version=\"1.8\">\n<model name=\"debug_path\">\n"
         "<static>true</static>\n<link name=\"link\">\n";
    for (std::size_t i = 0; i < path.size(); ++i) {
      s << "<visual name=\"wp_" << i << "\"><pose>" << path[i].first << " " << path[i].second
        << " 0.04 0 0 0</pose><cast_shadows>false</cast_shadows><geometry><sphere><radius>0.035"
           "</radius></sphere></geometry><material><ambient>0.1 0.9 0.2 1</ambient>"
           "<diffuse>0.1 0.9 0.2 1</diffuse></material></visual>\n";
      if (i + 1 < path.size()) {
        const double dx = path[i + 1].first - path[i].first;
        const double dy = path[i + 1].second - path[i].second;
        const double len = std::hypot(dx, dy);
        if (len < 1e-3) continue;
        s << "<visual name=\"seg_" << i << "\"><pose>" << (path[i].first + dx / 2.0) << " "
          << (path[i].second + dy / 2.0) << " 0.03 0 0 " << std::atan2(dy, dx)
          << "</pose><cast_shadows>false</cast_shadows><geometry><box><size>" << len
          << " 0.035 0.01</size></box></geometry><material><ambient>0.1 0.4 1 1</ambient>"
             "<diffuse>0.1 0.4 1 1</diffuse></material></visual>\n";
      }
    }
    s << "</link>\n</model>\n</sdf>\n";
    return s.str();
  }

  void update_gazebo_path(const std::vector<std::pair<double, double>> & path) {
    if (!gazebo_path_debug_ || path.size() < 2 || debug_busy_) return;
    const double now_s = now().seconds();
    if (now_s - last_debug_time_ < 1.5) return;
    bool changed = last_debug_path_.size() < 2 ||
      std::abs(static_cast<int>(path.size()) - static_cast<int>(last_debug_path_.size())) > 2;
    if (!changed) {
      const auto & a = path.back();
      const auto & b = last_debug_path_.back();
      changed = distance(a.first, a.second, b.first, b.second) > 0.1;
    }
    if (!changed) return;
    last_debug_time_ = now_s;
    last_debug_path_ = path;
    const std::string sdf = build_path_sdf(path);
    const std::string world = gazebo_world_;
    if (debug_thread_.joinable()) debug_thread_.join();
    debug_busy_ = true;
    debug_thread_ = std::thread([this, sdf, world]() {
      const std::string file = "/tmp/astar_debug_path.sdf";
      {
        std::ofstream out(file);
        out << sdf;
      }
      const std::string cmd =
        "gz service -s /world/" + world + "/remove --reqtype gz.msgs.Entity "
        "--reptype gz.msgs.Boolean --timeout 1000 --req 'name: \"debug_path\" type: MODEL' "
        ">/dev/null 2>&1; "
        "gz service -s /world/" + world + "/create --reqtype gz.msgs.EntityFactory "
        "--reptype gz.msgs.Boolean --timeout 3000 --req 'sdf_filename: \"" + file + "\"' "
        ">/dev/null 2>&1";
      const int rc = std::system(cmd.c_str());
      (void)rc;
      debug_busy_ = false;
    });
  }

  void odom(const nav_msgs::msg::Odometry::ConstSharedPtr msg) {
    const auto & q = msg->pose.pose.orientation;
    pose_.x = msg->pose.pose.position.x + initial_pose_x_;
    pose_.y = msg->pose.pose.position.y + initial_pose_y_;
    pose_.yaw = std::atan2(2.0 * (q.w * q.z + q.x * q.y),
                           1.0 - 2.0 * (q.y * q.y + q.z * q.z));
    geometry_msgs::msg::TransformStamped transform;
    transform.header.stamp = msg->header.stamp;
    transform.header.frame_id = "odom";
    transform.child_frame_id = "base_link";
    transform.transform.translation.x = pose_.x;
    transform.transform.translation.y = pose_.y;
    transform.transform.rotation = q;
    tf_broadcaster_->sendTransform(transform);
    transform.header.frame_id = "base_link";
    transform.child_frame_id = "base_scan";
    transform.transform.translation.x = scan_offset_x_;
    transform.transform.translation.y = scan_offset_y_;
    transform.transform.translation.z = scan_offset_z_;
    transform.transform.rotation.x = 0.0;
    transform.transform.rotation.y = 0.0;
    transform.transform.rotation.z = 0.0;
    transform.transform.rotation.w = 1.0;
    tf_broadcaster_->sendTransform(transform);
    last_odom_time_ = rclcpp::Time(msg->header.stamp).seconds();
    have_odom_ = true;
  }

  void scan(const sensor_msgs::msg::LaserScan::ConstSharedPtr msg) {
    scan_ = msg;
    have_scan_ = true;
  }

  int map_width() const {
    return std::max(3, static_cast<int>(std::ceil(map_size_ / resolution_)));
  }
  int map_height() const {
    return std::max(3, static_cast<int>(std::ceil(map_height_ / resolution_)));
  }

  std::vector<Obstacle> planning_obstacles() const {
    std::vector<Obstacle> result;
    const std::size_t count = std::min(
      {known_obstacle_x_.size(), known_obstacle_y_.size(), known_obstacle_radius_.size()});
    for (std::size_t i = 0; i < count; ++i)
      result.push_back({known_obstacle_x_[i], known_obstacle_y_[i], known_obstacle_radius_[i]});
    return result;
  }

  bool line_free(double ax, double ay, double bx, double by,
                 const std::vector<Obstacle> & statics) const {
    const double len = distance(ax, ay, bx, by);
    const int n = std::max(1, static_cast<int>(std::ceil(len / 0.05)));
    for (int k = 0; k <= n; ++k) {
      const double t = static_cast<double>(k) / n;
      const double x = ax + (bx - ax) * t, y = ay + (by - ay) * t;
      for (const auto & o : statics)
        if (distance(x, y, o.x, o.y) < o.radius + robot_radius_ - 0.02) return false;
    }
    return true;
  }

  std::vector<Obstacle> obstacles() {
    std::vector<Obstacle> pts;
    std::vector<std::size_t> scan_index;
    if (!scan_) return pts;
    const double scan_time = rclcpp::Time(scan_->header.stamp).seconds();
    if (have_tracked_scan_ && scan_time == last_track_time_) return sensed_cache_;
    constexpr double max_dist = 3.0;
    constexpr double half_fov = 1.57079632679;
    for (std::size_t i = 0; i < scan_->ranges.size(); ++i) {
      const double r = scan_->ranges[i];
      if (!std::isfinite(r) || r < scan_->range_min || r > scan_->range_max) continue;
      const double rel = scan_->angle_min + static_cast<double>(i) * scan_->angle_increment;
      if (r > max_dist || std::abs(angle_error(rel)) > half_fov) continue;
      const double a = pose_.yaw + rel;
      const double sensor_x = pose_.x + scan_offset_x_ * std::cos(pose_.yaw) -
        scan_offset_y_ * std::sin(pose_.yaw);
      const double sensor_y = pose_.y + scan_offset_x_ * std::sin(pose_.yaw) +
        scan_offset_y_ * std::cos(pose_.yaw);
      pts.push_back({sensor_x + r * std::cos(a), sensor_y + r * std::sin(a), 0.0});
      scan_index.push_back(i);
    }

    std::vector<std::vector<std::size_t>> clusters;
    for (std::size_t k = 0; k < pts.size(); ++k) {
      bool join = false;
      if (!clusters.empty()) {
        const std::size_t last = clusters.back().back();
        join = (scan_index[k] - scan_index[last] <= 2) &&
               distance(pts[k].x, pts[k].y, pts[last].x, pts[last].y) < 0.15;
      }
      if (join) clusters.back().push_back(k); else clusters.push_back({k});
    }

    const double dt = scan_time - last_track_time_;
    std::vector<Track> new_tracks;
    std::vector<bool> used(tracks_.size(), false);
    for (const auto & cl : clusters) {
      double cx = 0.0, cy = 0.0;
      for (auto k : cl) { cx += pts[k].x; cy += pts[k].y; }
      cx /= static_cast<double>(cl.size());
      cy /= static_cast<double>(cl.size());
      double vx = 0.0, vy = 0.0;
      if (have_tracked_scan_ && cl.size() >= 2 && dt > 0.02 && dt < 0.5) {
        std::size_t best_index = tracks_.size();
        double best_d = 0.35;
        for (std::size_t index = 0; index < tracks_.size(); ++index) {
          if (used[index]) continue;
          const auto & track = tracks_[index];
          const double d = distance(cx, cy, track.x + track.vx * dt,
                                   track.y + track.vy * dt);
          if (d < best_d) { best_d = d; best_index = index; }
        }
        if (best_index < tracks_.size()) {
          used[best_index] = true;
          const auto & best = tracks_[best_index];
          vx = 0.6 * best.vx + 0.4 * (cx - best.x) / dt;
          vy = 0.6 * best.vy + 0.4 * (cy - best.y) / dt;
          const double sp = std::hypot(vx, vy);
          if (sp < 0.06) { vx = 0.0; vy = 0.0; }
          else if (sp > 0.6) { vx *= 0.6 / sp; vy *= 0.6 / sp; }
        }
      }
      new_tracks.push_back({cx, cy, vx, vy});
      for (auto k : cl) { pts[k].vx = vx; pts[k].vy = vy; }
    }
    tracks_ = new_tracks;
    last_track_time_ = scan_time;
    have_tracked_scan_ = true;
    return pts;
  }

  // ---------------------------------------------------------------------- A*
  std::vector<std::pair<double, double>> astar(
    const std::vector<Obstacle> & sensed_obstacles, bool use_sensed) const {
    const int width = map_width();
    const int height = map_height();
    const double ox = map_origin_x_, oy = map_origin_y_;
    std::vector<bool> blocked(static_cast<std::size_t>(width) * height, false);
    auto inside = [width, height](int r, int c) { return r >= 0 && c >= 0 && r < height && c < width; };
    auto index = [width](int r, int c) { return r * width + c; };
    auto cell = [resolution = resolution_, ox, oy](double x, double y) {
      return std::pair<int, int>{static_cast<int>(std::floor((y - oy) / resolution)),
                                 static_cast<int>(std::floor((x - ox) / resolution))};
    };
    auto world = [resolution = resolution_, ox, oy](int r, int c) {
      return std::pair<double, double>{ox + (c + 0.5) * resolution, oy + (r + 0.5) * resolution};
    };

    auto inflate = [&](const Obstacle & obstacle) {
      const auto center = cell(obstacle.x, obstacle.y);
      const double inflation = robot_radius_ + obstacle.radius + planning_margin_;
      const int radius = static_cast<int>(std::ceil(inflation / resolution_));
      for (int r = center.first - radius; r <= center.first + radius; ++r)
        for (int c = center.second - radius; c <= center.second + radius; ++c)
          if (inside(r, c)) {
            const auto p = world(r, c);
            if (distance(p.first, p.second, obstacle.x, obstacle.y) <= inflation)
              blocked[index(r, c)] = true;
          }
    };

    const auto statics = planning_obstacles();
    for (const auto & obstacle : statics) inflate(obstacle);
    if (use_sensed) {
      for (const auto & o : sensed_obstacles) {
        if (distance(pose_.x, pose_.y, o.x, o.y) < 0.35) continue;
        bool known = false;
        for (const auto & s : statics)
          if (distance(o.x, o.y, s.x, s.y) < s.radius + 0.25) { known = true; break; }
        if (known) continue;
        inflate({o.x, o.y, 0.05});
      }
    }

    const double boundary_margin = robot_radius_ + safety_margin_;
    for (int r = 0; r < height; ++r)
      for (int c = 0; c < width; ++c) {
        const auto p = world(r, c);
        if (p.first < ox + boundary_margin || p.first > ox + map_size_ - boundary_margin ||
            p.second < oy + boundary_margin || p.second > oy + map_height_ - boundary_margin)
          blocked[index(r, c)] = true;
      }

    const auto start = cell(pose_.x, pose_.y);
    const auto target = cell(goal_x_, goal_y_);
    if (!inside(start.first, start.second) || !inside(target.first, target.second) ||
        blocked[index(target.first, target.second)]) {
      RCLCPP_WARN_THROTTLE(
        get_logger(), *get_clock(), 5000,
        "A* ervenytelen kezdo/celcella: start=(%d,%d), cel=(%d,%d)",
        start.first, start.second, target.first, target.second);
      return {};
    }
    blocked[index(start.first, start.second)] = false;
    for (int dr = -1; dr <= 1; ++dr)
      for (int dc = -1; dc <= 1; ++dc) {
        const int rr = start.first + dr, cc = start.second + dc;
        if (!inside(rr, cc)) continue;
        const auto p = world(rr, cc);
        bool hard = false;
        for (const auto & o : statics)
          if (distance(p.first, p.second, o.x, o.y) < o.radius + 0.12) { hard = true; break; }
        if (!hard) blocked[index(rr, cc)] = false;
      }

    struct Entry {
      double f, g; int r, c;
      bool operator>(const Entry & other) const { return f > other.f; }
    };
    std::priority_queue<Entry, std::vector<Entry>, std::greater<Entry>> open;
    const std::size_t total = static_cast<std::size_t>(width) * height;
    std::vector<double> cost(total, std::numeric_limits<double>::infinity());
    std::vector<int> parent(total, -1);
    auto heuristic = [&target](int r, int c) { return std::hypot(target.first - r, target.second - c); };
    open.push({heuristic(start.first, start.second), 0.0, start.first, start.second});
    cost[index(start.first, start.second)] = 0.0;
    const int directions[8][2] = {{1,0},{-1,0},{0,1},{0,-1},{1,1},{1,-1},{-1,1},{-1,-1}};
    while (!open.empty()) {
      const auto current = open.top(); open.pop();
      if (current.g > cost[index(current.r, current.c)]) continue;
      if (current.r == target.first && current.c == target.second) break;
      for (const auto & d : directions) {
        const int nr = current.r + d[0], nc = current.c + d[1];
        if (!inside(nr, nc) || blocked[index(nr, nc)]) continue;
        if (d[0] && d[1] && (blocked[index(current.r, nc)] || blocked[index(nr, current.c)])) continue;
        const double ng = current.g + ((d[0] && d[1]) ? std::sqrt(2.0) : 1.0);
        if (ng < cost[index(nr, nc)]) {
          cost[index(nr, nc)] = ng;
          parent[index(nr, nc)] = index(current.r, current.c);
          open.push({ng + heuristic(nr, nc), ng, nr, nc});
        }
      }
    }
    std::vector<std::pair<double, double>> path;
    int current = index(target.first, target.second);
    const int start_index = index(start.first, start.second);
    if (current != start_index && parent[current] < 0) return path;
    while (current >= 0) {
      path.push_back(world(current / width, current % width));
      if (current == start_index) break;
      current = parent[current];
    }
    std::reverse(path.begin(), path.end());
    if (!path.empty()) path.back() = {goal_x_, goal_y_};
    return path;
  }

  void publish_map() {
    nav_msgs::msg::OccupancyGrid map;
    map.header.frame_id = "odom";
    map.header.stamp = now();
    map.info.resolution = static_cast<float>(resolution_);
    map.info.width = static_cast<std::uint32_t>(map_width());
    map.info.height = static_cast<std::uint32_t>(map_height());
    map.info.origin.position.x = map_origin_x_;
    map.info.origin.position.y = map_origin_y_;
    map.info.origin.orientation.w = 1.0;
    map.data.assign(map.info.width * map.info.height, 0);
    const int width = static_cast<int>(map.info.width);
    const int height = static_cast<int>(map.info.height);
    for (const auto & obstacle : planning_obstacles()) {
      const double inflation = obstacle.radius + robot_radius_ + planning_margin_;
      const int radius = static_cast<int>(std::ceil(inflation / resolution_));
      const int cc = static_cast<int>(std::floor((obstacle.x - map_origin_x_) / resolution_));
      const int cr = static_cast<int>(std::floor((obstacle.y - map_origin_y_) / resolution_));
      for (int r = cr - radius; r <= cr + radius; ++r)
        for (int c = cc - radius; c <= cc + radius; ++c)
          if (r >= 0 && c >= 0 && r < height && c < width) {
            const double px = map_origin_x_ + (c + 0.5) * resolution_;
            const double py = map_origin_y_ + (r + 0.5) * resolution_;
            if (distance(px, py, obstacle.x, obstacle.y) <= inflation)
              map.data[static_cast<std::size_t>(r) * width + c] = 100;
          }
    }
    map_pub_->publish(map);
  }

  // --------------------------------------------------------------------- DWA
  std::pair<double, double> wheel_kinematics(double left, double right) const {
    const double velocity = ((left + right) / 2.0) * wheel_radius_;
    const double angular = ((right - left) / (2.0 * wheel_base_)) * wheel_radius_;
    return {velocity, angular};
  }

  std::pair<double, double> dwa(double target_x, double target_y,
                                std::size_t target_index,
                                const std::vector<Obstacle> & sensed) {
    const double wa = acceleration_limit_ / wheel_radius_;
    const double left_min = std::max(-wheel_max_, wheel_left_ - wa * dt_);
    const double left_max = std::min(wheel_max_, wheel_left_ + wa * dt_);
    const double right_min = std::max(-wheel_max_, wheel_right_ - wa * dt_);
    const double right_max = std::min(wheel_max_, wheel_right_ + wa * dt_);
    const double clearance_limit = robot_radius_ + safety_margin_;
    const double goal_dist = distance(pose_.x, pose_.y, target_x, target_y);
    const std::size_t first = waypoint_index_ > 0 ? waypoint_index_ - 1 : 0;
    const std::size_t last = std::min(target_index + 1, current_path_.size() - 1);
    const double initial_path_error = path_tracking::distance_to_path(
      current_path_, first, last, pose_.x, pose_.y);
    if (avoiding_obstacle_) returning_to_path_ = false;
    else if (rejoin_active_) returning_to_path_ = true;
    else if (initial_path_error <= path_return_tolerance_) returning_to_path_ = false;
    else if (initial_path_error > 2.0 * path_return_tolerance_) returning_to_path_ = true;
    const double horizon = returning_to_path_ || avoiding_obstacle_ ? predict_time_ :
      std::clamp(goal_dist * 2.0, 0.8, predict_time_);
    const double max_travel = max_linear_velocity_ * horizon;
    const double return_heading = std::atan2(target_y - pose_.y, target_x - pose_.x);
    const auto statics = planning_obstacles();
    std::vector<double> static_init_clear(statics.size(), 0.0);
    for (std::size_t index = 0; index < statics.size(); ++index) {
      static_init_clear[index] = distance(pose_.x, pose_.y, statics[index].x, statics[index].y) -
        (robot_radius_ + static_safety_margin_ + statics[index].radius);
    }

    std::vector<double> init_clear(sensed.size(), 0.0);
    for (std::size_t j = 0; j < sensed.size(); ++j) {
      const bool mv = std::hypot(sensed[j].vx, sensed[j].vy) > 0.0;
      init_clear[j] = distance(pose_.x, pose_.y, sensed[j].x, sensed[j].y) -
                      (robot_radius_ + (mv ? safety_margin_ : static_safety_margin_) + sensed[j].radius);
    }
    const auto reference = path_tracking::rejoin_command(
      goal_dist, angle_error(return_heading - pose_.yaw),
      max_linear_velocity_, max_angular_velocity_);
    bool rejoin_control = rejoin_active_ && line_free(pose_.x, pose_.y, target_x, target_y, statics);
    const path_tracking::Path connector{{pose_.x, pose_.y}, {target_x, target_y}};
    for (const auto & obstacle : sensed) {
      if (!rejoin_control) break;
      const bool moving = std::hypot(obstacle.vx, obstacle.vy) > 0.0;
      const double clearance = robot_radius_ + obstacle.radius +
        (moving ? safety_margin_ : static_safety_margin_);
      for (double time = 0.0; time <= horizon; time += dt_) {
        if (path_tracking::distance_to_path(connector, 0, 1,
              obstacle.x + obstacle.vx * time, obstacle.y + obstacle.vy * time) <= clearance) {
          rejoin_control = false;
          break;
        }
      }
    }
    std::vector<double> left_samples, right_samples;
    for (double left = left_min; left <= left_max + 1e-9; left += wheel_resolution_)
      left_samples.push_back(left);
    for (double right = right_min; right <= right_max + 1e-9; right += wheel_resolution_)
      right_samples.push_back(right);
    left_samples.push_back(std::clamp(wheel_left_, left_min, left_max));
    right_samples.push_back(std::clamp(wheel_right_, right_min, right_max));
    left_samples.push_back(std::clamp(0.0, left_min, left_max));
    right_samples.push_back(std::clamp(0.0, right_min, right_max));
    if (rejoin_active_) {
      // Include the reference and braking commands exactly, not only the sampling lattice.
      left_samples.push_back(std::clamp(
        (reference.first - reference.second * wheel_base_) / wheel_radius_, left_min, left_max));
      right_samples.push_back(std::clamp(
        (reference.first + reference.second * wheel_base_) / wheel_radius_, right_min, right_max));
    }
    double best_score = -std::numeric_limits<double>::infinity();
    double best_left = 0.0, best_right = 0.0;
    double best_path_error = initial_path_error;
    bool best_returning = false;
    bool found = false;
    std::size_t n_test = 0, n_vel = 0, n_ttc = 0, n_brake = 0;
    std::size_t n_collision = 0, n_returning = 0;

    for (double left : left_samples) {
      for (double right : right_samples) {
        ++n_test;
        const auto cand = wheel_kinematics(left, right);
        if (cand.first < 0.0 || cand.first > max_linear_velocity_ ||
            std::abs(cand.second) > max_angular_velocity_) {
          ++n_vel;
          continue;
        }

        double x = pose_.x, y = pose_.y, yaw = pose_.yaw;
        double sl = wheel_left_, sr = wheel_right_;
        double arc = 0.0, collision_dist = 10.0, min_clear = 3.0;
        bool hit = false;
        int steps = 0;
        for (double t = 0.0; t < horizon; t += dt_, ++steps) {
          sl += std::clamp(left - sl, -wa * dt_, wa * dt_);
          sr += std::clamp(right - sr, -wa * dt_, wa * dt_);
          const auto s = wheel_kinematics(sl, sr);
          if (std::abs(s.second) > 1e-6) {
            x += (s.first / s.second) * (std::sin(yaw + s.second * dt_) - std::sin(yaw));
            y -= (s.first / s.second) * (std::cos(yaw + s.second * dt_) - std::cos(yaw));
          } else {
            x += s.first * std::cos(yaw) * dt_;
            y += s.first * std::sin(yaw) * dt_;
          }
          yaw += s.second * dt_;
          arc += std::abs(s.first) * dt_;
          const double tt = (steps + 1) * dt_;

          if (x < map_origin_x_ + clearance_limit ||
              x > map_origin_x_ + map_size_ - clearance_limit ||
              y < map_origin_y_ + clearance_limit ||
              y > map_origin_y_ + map_height_ - clearance_limit) {
            collision_dist = arc;
            hit = true;
            break;
          }
          for (std::size_t index = 0; index < statics.size(); ++index) {
            const auto & obstacle = statics[index];
            const double clear = distance(x, y, obstacle.x, obstacle.y) -
              (robot_radius_ + static_safety_margin_ + obstacle.radius);
            min_clear = std::min(min_clear, clear);
            if (clear <= 0.0 && clear < static_init_clear[index] - 0.005) {
              collision_dist = arc;
              hit = true;
              break;
            }
          }
          if (hit) break;
          for (std::size_t j = 0; j < sensed.size(); ++j) {
            const auto & o = sensed[j];
            const double ox = o.x + o.vx * tt;
            const double oy = o.y + o.vy * tt;
            const bool moving = std::hypot(o.vx, o.vy) > 0.0;
            const double margin = moving ? safety_margin_ : static_safety_margin_;
            const double clear = distance(x, y, ox, oy) - (robot_radius_ + margin + o.radius);
            min_clear = std::min(min_clear, clear);
            if (clear <= 0.0 && clear < init_clear[j] - 0.005) {
              collision_dist = arc;
              hit = true;
              break;
            }
          }
          if (hit) break;
        }

        if (cand.first > std::sqrt(2.0 * acceleration_limit_ * collision_dist) + 1e-9) {
          ++n_brake;
          continue;
        }
        if (hit && cand.first > 1e-3 && collision_dist < cand.first * min_ttc_) {
          ++n_ttc;
          continue;
        }
        if (hit) {
          ++n_collision;
          continue;
        }

        const double goal_heading = returning_to_path_ || avoiding_obstacle_ ? return_heading :
          std::atan2(target_y - y, target_x - x);
        const double heading_score = (M_PI - std::abs(angle_error(goal_heading - yaw))) / M_PI;
        const double clear_score = std::clamp(min_clear / 1.0, 0.0, 1.0);
        const double v_target = std::min(max_linear_velocity_, std::max(0.08, goal_dist * 1.4));
        const double vel_score = 1.0 - std::abs(v_target - cand.first) / max_linear_velocity_;
        const double tracking_cost = path_tracking::tracking_cost(
          current_path_, first, last, x, y, target_x, target_y,
          avoiding_obstacle_ ? 0.0 : path_distance_bias_, goal_distance_bias_);
        const double final_path_error = path_tracking::distance_to_path(current_path_, first, last, x, y);
        const double progress = path_tracking::return_progress(
          initial_path_error, final_path_error, max_travel);
        const bool returning = returning_to_path_ && path_tracking::is_returning(
          initial_path_error, final_path_error, path_return_tolerance_, max_travel);
        if (returning) ++n_returning;
        const double score = rejoin_control ? -path_tracking::command_error(
          cand.first, cand.second, reference, max_linear_velocity_, max_angular_velocity_) :
          alpha_ * heading_score + beta_ * clear_score + gamma_ * vel_score -
          tracking_cost + (returning_to_path_ ? path_return_bias_ * progress : 0.0);
        // A clear rejoin uses the current steering command, not a repeatedly postponed endpoint.
        if (!found || (rejoin_control ? score > best_score :
            path_tracking::prefer_candidate(returning, score, best_returning, best_score))) {
          best_score = score;
          best_left = left;
          best_right = right;
          best_returning = returning;
          best_path_error = final_path_error;
          found = true;
        }
      }
    }
    RCLCPP_INFO_THROTTLE(
      get_logger(), *get_clock(), 2000,
      "DWA: teszt=%zu sebesseg=%zu fekezes=%zu ttc=%zu utkozes=%zu elfogadott=%s "
      "visszateres=%s visszatero_jelolt=%zu valasztott_visszatero=%s elteres=%.3f->%.3f m "
      "rogzitett_cel=%s cel_index=%zu iranykovetes=%s referencia=(%.3f,%.3f) kerules=%s",
      n_test, n_vel, n_brake, n_ttc, n_collision, found ? "igen" : "nem",
      returning_to_path_ ? "igen" : "nem", n_returning, best_returning ? "igen" : "nem",
      initial_path_error, best_path_error, rejoin_active_ ? "igen" : "nem", target_index,
      rejoin_control ? "igen" : "nem", reference.first, reference.second,
      avoiding_obstacle_ ? "igen" : "nem");

    if (found) {
      blocked_cycles_ = 0;
      wheel_left_ = best_left;
      wheel_right_ = best_right;
      return wheel_kinematics(wheel_left_, wheel_right_);
    }

    RCLCPP_WARN_THROTTLE(
      get_logger(), *get_clock(), 2000,
      "DWA: nincs elfogadhato jelolt (fekezes=%zu ttc=%zu), blokkolt ciklusok=%d",
      n_brake, n_ttc, blocked_cycles_ + 1);
    ++blocked_cycles_;
    wheel_left_ = 0.0;
    wheel_right_ = 0.0;
    return {0.0, 0.0};
  }

  // ------------------------------------------------------------ vizualizacio
  visualization_msgs::msg::Marker make_marker(
    int id, int type, double x, double y, double z,
    double scale, float r, float g, float b) const {
    visualization_msgs::msg::Marker marker;
    marker.header.frame_id = "odom";
    marker.header.stamp = now();
    marker.ns = "astar_dwa";
    marker.id = id;
    marker.type = type;
    marker.action = visualization_msgs::msg::Marker::ADD;
    marker.pose.position.x = x;
    marker.pose.position.y = y;
    marker.pose.position.z = z;
    marker.pose.orientation.w = 1.0;
    marker.scale.x = scale;
    marker.scale.y = scale;
    marker.scale.z = scale;
    marker.color.r = r;
    marker.color.g = g;
    marker.color.b = b;
    marker.color.a = 0.9;
    marker.lifetime = rclcpp::Duration::from_seconds(0.4);
    return marker;
  }

  void publish_debug(const std::vector<std::pair<double, double>> & path,
                     double target_x, double target_y,
                     double velocity, double angular_velocity) {
    visualization_msgs::msg::MarkerArray markers;
    markers.markers.push_back(make_marker(
      0, visualization_msgs::msg::Marker::SPHERE, target_x, target_y, 0.35, 0.45, 0.1, 1.0, 0.2));
    auto goal_ring = make_marker(3, visualization_msgs::msg::Marker::CYLINDER,
                                 target_x, target_y, 0.03, 1.0, 0.1, 1.0, 0.2);
    goal_ring.scale.z = 0.04;
    goal_ring.color.a = 0.75;
    markers.markers.push_back(goal_ring);
    auto goal_text = make_marker(4, visualization_msgs::msg::Marker::TEXT_VIEW_FACING,
                                 target_x, target_y, 0.85, 0.1, 0.1, 1.0, 0.2);
    goal_text.text = "CEL";
    goal_text.scale.z = 0.28;
    goal_text.color.a = 1.0;
    markers.markers.push_back(goal_text);
    auto path_marker = make_marker(1, visualization_msgs::msg::Marker::LINE_STRIP,
                                   0.0, 0.0, 0.18, 0.1, 0.1, 1.0, 0.2);
    path_marker.points.clear();
    for (const auto & point : path) {
      geometry_msgs::msg::Point p;
      p.x = point.first; p.y = point.second; p.z = 0.08;
      path_marker.points.push_back(p);
    }
    markers.markers.push_back(path_marker);
    int id = 10;
    for (const auto & obstacle : planning_obstacles()) {
      auto marker = make_marker(id++, visualization_msgs::msg::Marker::CYLINDER,
                                obstacle.x, obstacle.y, 0.45,
                                obstacle.radius * 2.0, 0.9, 0.15, 0.1);
      marker.scale.z = 0.9;
      markers.markers.push_back(marker);
      auto safety = make_marker(id++, visualization_msgs::msg::Marker::CYLINDER,
                                obstacle.x, obstacle.y, 0.02,
                                2.0 * (obstacle.radius + robot_radius_ + planning_margin_),
                                1.0, 0.35, 0.05);
      safety.scale.z = 0.02;
      safety.color.a = 0.25;
      markers.markers.push_back(safety);
    }
    int sensed_id = 1000;
    for (const auto & obstacle : sensed_cache_) {
      const bool moving = std::hypot(obstacle.vx, obstacle.vy) > 0.0;
      auto marker = make_marker(sensed_id++, visualization_msgs::msg::Marker::SPHERE,
                                obstacle.x, obstacle.y, 0.16, 0.10,
                                moving ? 1.0f : 1.0f, moving ? 0.1f : 0.75f, moving ? 0.1f : 0.05f);
      marker.color.a = 0.85;
      markers.markers.push_back(marker);
    }
    auto trajectory = make_marker(2, visualization_msgs::msg::Marker::LINE_STRIP,
                                  0.0, 0.0, 0.22, 0.09, 0.2, 0.6, 1.0);
    trajectory.points.clear();
    double x = pose_.x, y = pose_.y, yaw = pose_.yaw;
    for (int step = 0; step < 15; ++step) {
      x += velocity * std::cos(yaw) * 0.1;
      y += velocity * std::sin(yaw) * 0.1;
      yaw += angular_velocity * 0.1;
      geometry_msgs::msg::Point p;
      p.x = x; p.y = y; p.z = 0.12;
      trajectory.points.push_back(p);
    }
    markers.markers.push_back(trajectory);
    auto robot = make_marker(5, visualization_msgs::msg::Marker::CYLINDER,
                             pose_.x, pose_.y, 0.04, 2.0 * robot_radius_, 0.2, 0.7, 1.0);
    robot.scale.z = 0.05;
    robot.color.a = 0.35;
    markers.markers.push_back(robot);
    auto heading = make_marker(6, visualization_msgs::msg::Marker::ARROW,
                               pose_.x, pose_.y, 0.28, 0.08, 0.2, 0.7, 1.0);
    heading.points.clear();
    geometry_msgs::msg::Point start, end;
    start.x = pose_.x; start.y = pose_.y; start.z = 0.28;
    end.x = pose_.x + 0.55 * std::cos(pose_.yaw);
    end.y = pose_.y + 0.55 * std::sin(pose_.yaw); end.z = 0.28;
    heading.points = {start, end};
    heading.scale.x = 0.08; heading.scale.y = 0.14; heading.scale.z = 0.14;
    markers.markers.push_back(heading);
    marker_pub_->publish(markers);
  }

  // ---------------------------------------------------------------- vezerles
  void stop_robot() {
    last_linear_velocity_ = 0.0;
    last_angular_velocity_ = 0.0;
    wheel_left_ = 0.0;
    wheel_right_ = 0.0;
    cmd_pub_->publish(geometry_msgs::msg::Twist{});
  }

  void control() {
    if (!have_odom_) return;
    publish_map();
    if (!have_scan_) {
      publish_debug({}, pose_.x, pose_.y, 0.0, 0.0);
      return;
    }
    const double sensor_time = std::min(last_odom_time_,
      rclcpp::Time(scan_->header.stamp).seconds());
    if (now().seconds() - sensor_time > std::max(0.5, 3.0 * dt_)) {
      stop_robot();
      RCLCPP_WARN_THROTTLE(get_logger(), *get_clock(), 2000,
                           "Elavult odometria vagy scan; a robot megall.");
      return;
    }
    sensed_cache_ = obstacles();
    const auto & sensed_obstacles = sensed_cache_;
    if (!has_goal_) {
      cmd_pub_->publish(geometry_msgs::msg::Twist{});
      publish_debug({}, pose_.x, pose_.y, 0.0, 0.0);
      return;
    }

    if (current_path_.empty() || need_replan_ ||
        (!rejoin_active_ && waypoint_index_ < current_path_.size() &&
         distance(pose_.x, pose_.y, current_path_[waypoint_index_].first,
                  current_path_[waypoint_index_].second) > 1.2)) {
      auto new_path = astar({}, false);
      if (!new_path.empty() || current_path_.empty()) {
        current_path_ = std::move(new_path);
        waypoint_index_ = 0;
        rejoin_active_ = false;
        returning_to_path_ = false;
      }
      need_replan_ = false;
      last_replan_time_ = now().seconds();
      RCLCPP_INFO(get_logger(), "A* (statikus terkep) utvonal: %zu pont", current_path_.size());
    }
    const auto path = current_path_;

    nav_msgs::msg::Path path_msg;
    path_msg.header.frame_id = "odom";
    path_msg.header.stamp = now();
    for (const auto & point : path) {
      geometry_msgs::msg::PoseStamped pose;
      pose.header = path_msg.header;
      pose.pose.position.x = point.first;
      pose.pose.position.y = point.second;
      pose.pose.orientation.w = 1.0;
      path_msg.poses.push_back(pose);
    }
    path_pub_->publish(path_msg);
    update_gazebo_path(path);

    geometry_msgs::msg::Twist command;
    if (path.empty()) {
      stop_robot();
      RCLCPP_WARN_THROTTLE(get_logger(), *get_clock(), 5000,
                           "Az A* nem talalt elerheto utvonalat; a robot megall.");
      publish_debug({}, goal_x_, goal_y_, 0.0, 0.0);
      return;
    }
    if (distance(pose_.x, pose_.y, goal_x_, goal_y_) < 0.3) {
      stop_robot();
      return;
    }
    const double boundary_margin = robot_radius_ + safety_margin_;
    if (pose_.x < map_origin_x_ + boundary_margin ||
        pose_.x > map_origin_x_ + map_size_ - boundary_margin ||
        pose_.y < map_origin_y_ + boundary_margin ||
        pose_.y > map_origin_y_ + map_height_ - boundary_margin) {
      stop_robot();
      RCLCPP_WARN_THROTTLE(get_logger(), *get_clock(), 5000,
                           "A robot a palya biztonsagi hataran kivul van; sebesseg nullazva.");
      publish_debug(path, pose_.x, pose_.y, 0.0, 0.0);
      return;
    }

    const auto statics = planning_obstacles();
    bool obstacle_threat = false;
    for (const auto & obstacle : sensed_obstacles) {
      const double speed = std::hypot(obstacle.vx, obstacle.vy);
      bool known_static = false;
      if (speed < 0.06) {
        for (const auto & wall : statics) {
          if (distance(obstacle.x, obstacle.y, wall.x, wall.y) < wall.radius + 0.08) {
            known_static = true;
            break;
          }
        }
      }
      if (known_static) continue;
      const double clearance = robot_radius_ + safety_margin_ + obstacle.radius;
      if (path_tracking::collision_course(
          obstacle.x - pose_.x, obstacle.y - pose_.y,
          obstacle.vx - max_linear_velocity_ * std::cos(pose_.yaw),
          obstacle.vy - max_linear_velocity_ * std::sin(pose_.yaw),
          clearance, predict_time_)) {
        obstacle_threat = true;
        break;
      }
    }
    if (obstacle_threat) last_obstacle_threat_time_ = now().seconds();
    avoiding_obstacle_ = now().seconds() - last_obstacle_threat_time_ < 0.6;
    if (avoiding_obstacle_) {
      rejoin_active_ = false;
      returning_to_path_ = false;
    }
    if (rejoin_active_ && (distance(pose_.x, pose_.y,
        path[rejoin_index_].first, path[rejoin_index_].second) <= path_return_tolerance_ ||
        path_tracking::distance_to_path(path, waypoint_index_ > 0 ? waypoint_index_ - 1 : 0,
          std::min(rejoin_index_ + 1, path.size() - 1), pose_.x, pose_.y) <= path_return_tolerance_)) {
      rejoin_active_ = false;
      returning_to_path_ = false;
    }
    {
      const std::size_t window_end = std::min(path.size(), waypoint_index_ + 8);
      double best_d = std::numeric_limits<double>::infinity();
      std::size_t closest = waypoint_index_;
      bool found_visible = false;
      for (std::size_t i = waypoint_index_; i < window_end; ++i) {
        if (!line_free(pose_.x, pose_.y, path[i].first, path[i].second, statics)) continue;
        const double d = distance(pose_.x, pose_.y, path[i].first, path[i].second);
        if (d < best_d) { best_d = d; closest = i; found_visible = true; }
      }
      if (found_visible) {
        if (!rejoin_active_) {
          waypoint_index_ = std::max(waypoint_index_, closest);
          const double lateral_error = path_tracking::distance_to_path(
            path, closest > 0 ? closest - 1 : 0, std::min(closest + 1, path.size() - 1),
            pose_.x, pose_.y);
          if (!avoiding_obstacle_ && lateral_error > 2.0 * path_return_tolerance_) {
            rejoin_active_ = true;
            rejoin_index_ = closest;
          }
        }
      } else if (now().seconds() - last_replan_time_ > 1.0) {
        need_replan_ = true;
      }
    }
    std::size_t target_index = rejoin_active_ ? rejoin_index_ : path.size() - 1;
    if (!rejoin_active_) {
      double accumulated = 0.0;
      for (std::size_t i = waypoint_index_; i + 1 < path.size(); ++i) {
        accumulated += distance(path[i].first, path[i].second, path[i + 1].first, path[i + 1].second);
        if (accumulated >= lookahead_distance_) { target_index = i + 1; break; }
      }
      while (target_index > waypoint_index_ &&
             !line_free(pose_.x, pose_.y, path[target_index].first, path[target_index].second,
                        statics))
        --target_index;
    }
    double target_x = path[target_index].first, target_y = path[target_index].second;

    double nearest_obstacle = std::numeric_limits<double>::infinity();
    const Obstacle * nearest_sensed = nullptr;
    std::size_t moving_points = 0;
    for (const auto & obstacle : sensed_obstacles) {
      if (std::hypot(obstacle.vx, obstacle.vy) > 0.0) ++moving_points;
      const double obstacle_distance = distance(pose_.x, pose_.y, obstacle.x, obstacle.y);
      if (obstacle_distance < nearest_obstacle) {
        nearest_obstacle = obstacle_distance;
        nearest_sensed = &obstacle;
      }
    }

    const double target_heading = std::atan2(target_y - pose_.y, target_x - pose_.x);
    const double heading_error = angle_error(target_heading - pose_.yaw);
    if (!rejoin_active_ && std::abs(heading_error) > 0.95 && nearest_obstacle > 0.85) {
      wheel_left_ = 0.0;
      wheel_right_ = 0.0;
      command.angular.z = std::clamp(heading_error, -max_angular_velocity_, max_angular_velocity_);
      publish_debug(path, target_x, target_y, 0.0, command.angular.z);
      cmd_pub_->publish(command);
      return;
    }

    const auto velocity = dwa(target_x, target_y, target_index, sensed_obstacles);
    const double path_error = path_tracking::distance_to_path(
      path, waypoint_index_ > 0 ? waypoint_index_ - 1 : 0,
      std::min(target_index + 1, path.size() - 1), pose_.x, pose_.y);
    RCLCPP_INFO_THROTTLE(
      get_logger(), *get_clock(), 2000,
      "Vezerles: cel=(%.2f, %.2f), waypoint=(%.2f, %.2f), ut=%zu pont, akadaly_tav=%.2f, "
      "utvonal_elteres=%.3f m, cmd=(%.2f, %.2f), sim_t=%.3f scan_kor=%.3f s "
      "lidar_pont=%zu mozgo_pont=%zu kozeli_v=(%.3f,%.3f) m/s",
      goal_x_, goal_y_, target_x, target_y, path.size(), nearest_obstacle,
      path_error, velocity.first, velocity.second, now().seconds(),
      (now() - rclcpp::Time(scan_->header.stamp, get_clock()->get_clock_type())).seconds(),
      sensed_obstacles.size(), moving_points,
      nearest_sensed ? nearest_sensed->vx : 0.0,
      nearest_sensed ? nearest_sensed->vy : 0.0);
    command.linear.x = std::clamp(velocity.first, 0.0, max_linear_velocity_);
    command.angular.z = std::clamp(velocity.second, -max_angular_velocity_, max_angular_velocity_);
    last_linear_velocity_ = command.linear.x;
    last_angular_velocity_ = command.angular.z;
    publish_debug(path, target_x, target_y, command.linear.x, command.angular.z);
    cmd_pub_->publish(command);
  }

  // ------------------------------------------------------------------- tagok
  std::string cmd_topic_, odom_topic_, scan_topic_, goal_topic_, path_topic_;
  double goal_x_{0.0}, goal_y_{0.0}, map_size_{8.2}, map_height_{5.2};
  double map_origin_x_{0.0}, map_origin_y_{0.0};
  double initial_pose_x_{0.0}, initial_pose_y_{0.0};
  double scan_offset_x_{0.0}, scan_offset_y_{0.0}, scan_offset_z_{0.16};
  double resolution_{0.2}, robot_radius_{0.22};
  double max_linear_velocity_{0.26}, max_angular_velocity_{1.0};
  std::vector<double> known_obstacle_x_, known_obstacle_y_, known_obstacle_radius_;
  Pose pose_;
  sensor_msgs::msg::LaserScan::ConstSharedPtr scan_;
  bool have_odom_{false}, have_scan_{false}, has_goal_{false};
  double last_odom_time_{0.0};
  double wheel_radius_{0.033}, wheel_base_{0.08}, wheel_max_{15.0};
  double wheel_resolution_{0.5}, acceleration_limit_{2.0};
  double predict_time_{2.5}, safety_margin_{0.08}, min_ttc_{1.0};
  double alpha_{5.0}, beta_{2.0}, gamma_{3.0}, dt_{0.1};
  double path_distance_bias_{6.0}, goal_distance_bias_{2.0};
  double path_return_bias_{8.0}, path_return_tolerance_{0.10};
  bool returning_to_path_{false};
  bool rejoin_active_{false};
  std::size_t rejoin_index_{0};
  bool avoiding_obstacle_{false};
  double last_obstacle_threat_time_{-100.0};
  double wheel_left_{0.0}, wheel_right_{0.0};
  double last_linear_velocity_{0.0}, last_angular_velocity_{0.0};
  std::vector<Track> tracks_;
  std::vector<Obstacle> sensed_cache_;
  double last_track_time_{0.0};
  bool have_tracked_scan_{false};
  double sensed_until_{0.0};
  int blocked_cycles_{0};
  double static_safety_margin_{0.03};
  double planning_margin_{0.30};
  double lookahead_distance_{0.25};
  double last_replan_time_{-100.0};
  std::vector<std::pair<double, double>> current_path_;
  std::size_t waypoint_index_{0};
  bool need_replan_{true};
  bool gazebo_path_debug_{true};
  std::string gazebo_world_{"dwa_world"};
  std::vector<std::pair<double, double>> last_debug_path_;
  double last_debug_time_{-100.0};
  std::atomic<bool> debug_busy_{false};
  std::thread debug_thread_;
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr cmd_pub_;
  rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr path_pub_;
  rclcpp::Publisher<nav_msgs::msg::OccupancyGrid>::SharedPtr map_pub_;
  rclcpp::Publisher<visualization_msgs::msg::MarkerArray>::SharedPtr marker_pub_;
  std::unique_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster_;
  rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr odom_sub_;
  rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr scan_sub_;
  rclcpp::Subscription<geometry_msgs::msg::PoseStamped>::SharedPtr goal_sub_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char ** argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<AStarDwaNode>());
  rclcpp::shutdown();
  return 0;
}
~~~~~

### codes_diploma/ros2_astar_dwa_gazebo/src/astar_dwa_controller/src/path_tracking.hpp

~~~~~cpp
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
    if (distance >= nearest || !reachable(projected)) continue;
    nearest = distance;
    found = true;
    segment = index;
    result.projection = projected;
    result.waypoint = std::max(current, index + (fraction > 1e-9 ? 1 : 0));
  }
  if (!found) return result;
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
  for (double lookahead = result.lookahead; lookahead >= 0.05; lookahead *= 0.5) {
    const auto candidate = along_path(lookahead);
    if (!reachable(candidate.first)) continue;
    result.target = candidate.first;
    result.target_index = candidate.second;
    result.lookahead = lookahead;
    return result;
  }
  result.target = result.projection;
  result.target_index = result.waypoint;
  result.lookahead = 0.0;
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
~~~~~

### codes_diploma/ros2_astar_dwa_gazebo/src/astar_dwa_controller/src/reference_controller.cpp

~~~~~cpp
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
      "DIAG_CONFIG backend=cpp-python-reference schema=cpp-dwa-7 lidar_fov=360 pruning=25 dt=%.3f horizon=%.3f radius=%.3f "
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
    for (std::size_t index = 0; index < message->data.size(); ++index)
      grid_.blocked[index] = message->data[index] < 0 ? 2 : message->data[index] >= 65 ? 1 : 0;
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
      const double heading = yaw(conversion.rotation);
      try {
        if (!message.data.empty()) {
          sensor_msgs::PointCloud2ConstIterator<float> point_x(message, "x"), point_y(message, "y"),
            radius(message, "radius"), velocity_x(message, "vx"), velocity_y(message, "vy");
          for (; point_x != point_x.end(); ++point_x, ++point_y, ++radius, ++velocity_x, ++velocity_y) {
            if (!std::isfinite(*point_x) || !std::isfinite(*point_y) || !std::isfinite(*radius) ||
                !std::isfinite(*velocity_x) || !std::isfinite(*velocity_y) || *radius < 0.0) continue;
            const auto position = project(*point_x, *point_y, conversion);
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
    message.header.stamp = now();
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
                        tracking.target == waypoints_.back(), obstacles);
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
      "score_progress=%.3f score_dynamic=%.3f score_distance=%.3f "
      "cmd=(%.3f,%.3f) avoidance_priority=%d reorient=%d goal_heading_error=%.3f odom_age=%.3f obstacle_age=%.3f compute_ms=%.2f",
      result.found ? "command" : "braking_no_pair", state_.x, state_.y, state_.yaw,
      state_.velocity, state_.angular, waypoint_, waypoints_.size(), waypoint_ - previous_waypoint,
      tracking.lookahead, tracking.target_index, tracking.target.first, tracking.target.second,
      obstacles.size(), result.candidates, result.admissible,
      result.rejected_velocity, result.rejected_dynamic, result.rejected_dynamic_now, result.rejected_braking,
      result.forward_pairs, moving_points, max_obstacle_speed,
      result.score_progress, result.score_dynamic, result.score_distance,
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
~~~~~

### codes_diploma/ros2_astar_dwa_gazebo/src/astar_dwa_controller/src/reference_planner.hpp

~~~~~cpp
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
	bool found{false};
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

inline Result optimise(const Config & config, const State & state, Point goal,
											 bool final_waypoint, const std::vector<Obstacle> & sensed) {
	std::vector<Obstacle> visible;
	for (const auto & obstacle : sensed) {
		if (std::hypot(obstacle.x - state.x, obstacle.y - state.y) <= 3.0)
			visible.push_back(obstacle);
	}
	const double goal_distance = std::hypot(goal.first - state.x, goal.second - state.y);
	const double horizon = goal_distance < 1.0 ? std::max(0.5, goal_distance * 2.0) : config.predict_time;
	const double maximum_velocity = config.wheel_max * config.wheel_radius;
	const double heading_error = angle_error(std::atan2(goal.second - state.y, goal.first - state.x) - state.yaw);
	bool approaching_obstacle = false;
	for (const auto & obstacle : visible) {
		if (obstacle.vx == 0.0 && obstacle.vy == 0.0) continue;
		if (path_tracking::collision_course(obstacle.x - state.x, obstacle.y - state.y,
				obstacle.vx - state.velocity * std::cos(state.yaw),
				obstacle.vy - state.velocity * std::sin(state.yaw),
				config.radius + obstacle.radius + config.safety_margin, config.predict_time)) {
			approaching_obstacle = true;
			break;
		}
	}
	const bool reorient = std::abs(heading_error) > pi / 2.0 && !approaching_obstacle;
	const double target_speed = reorient ? 0.0 : maximum_velocity;
	const double velocity_limit = reorient ? std::max(0.0, state.velocity - config.acceleration * config.dt) : maximum_velocity;
	auto left_samples = wheel_samples(state.left, config);
	auto right_samples = wheel_samples(state.right, config);
	const double rotation_lower = std::max(left_samples.front(), -right_samples.back());
	const double rotation_upper = std::min(left_samples.back(), -right_samples.front());
	if (reorient && rotation_lower <= rotation_upper) {
		const double rotation_left = std::clamp(-heading_error * config.half_axle / config.wheel_radius,
			rotation_lower, rotation_upper);
		left_samples.push_back(rotation_left);
		right_samples.push_back(-rotation_left);
	}
	const bool slowdown = config.waypoint_slowdown || final_waypoint;
	const double slowdown_distance = final_waypoint ? 0.5 : 0.35;
	double best_score = -std::numeric_limits<double>::infinity();
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
			const double progress_score = std::clamp(
				(goal_distance - predicted_goal_distance) / (maximum_velocity * horizon), -1.0, 1.0);
			const double target_velocity = std::min(target_speed, std::max(0.08, goal_distance * 1.4));
			const double velocity_score = !slowdown && goal_distance > slowdown_distance ?
				command.velocity / maximum_velocity :
				1.0 - std::abs(target_velocity - command.velocity) / maximum_velocity;
			const double dynamic_score = std::isfinite(trajectory.dynamic_clearance) ?
				std::clamp(trajectory.dynamic_clearance / config.dynamic_clearance_distance, 0.0, 1.0) : 0.0;
			const double score = config.alpha * (heading_score + progress_score) + config.beta * trajectory.distance +
				config.gamma * velocity_score + config.dynamic_clearance_weight * dynamic_score;
			if (score > best_score) {
				best_score = score;
				result.command = command;
				result.found = true;
				result.score_progress = config.alpha * progress_score;
				result.score_dynamic = config.dynamic_clearance_weight * dynamic_score;
				result.score_distance = config.beta * trajectory.distance;
			}
		}
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
~~~~~

### codes_diploma/ros2_astar_dwa_gazebo/src/astar_dwa_controller/test/test_path_tracking.cpp

~~~~~cpp
#include "../src/path_tracking.hpp"
#include "../src/reference_planner.hpp"

#include <iostream>
#include <stdexcept>

void require(bool condition, const char * message) {
  if (!condition) throw std::runtime_error(message);
}

void near(double actual, double expected, const char * message) {
  require(std::abs(actual - expected) < 1e-9, message);
}

int main() {
  using path_tracking::distance_to_path;
  using path_tracking::tracking_cost;
  const path_tracking::Path straight{{0.0, 0.0}, {1.0, 0.0}, {2.0, 0.0}};
  near(distance_to_path(straight, 0, 2, 0.5, 0.0), 0.0, "Use segments, not vertices");
  near(distance_to_path(straight, 0, 2, 0.5, 0.4), 0.4, "Measure lateral offset");
  near(distance_to_path(straight, 0, 2, -0.3, 0.4), 0.5, "Clamp segment projection");
  const path_tracking::Path repeated{{0.0, 0.0}, {0.0, 0.0}, {1.0, 0.0}};
  near(distance_to_path(repeated, 0, 2, 0.5, 0.2), 0.2, "Handle duplicate points");
  near(distance_to_path({{1.0, 1.0}}, 0, 0, 1.3, 1.4), 0.5, "Handle single point");
  require(std::isinf(distance_to_path({}, 0, 0, 0.0, 0.0)), "Empty path is not trackable");
  const path_tracking::Path corner{{0.0, 0.0}, {1.0, 0.0}, {1.0, 1.0}};
  near(distance_to_path(corner, 0, 2, 1.3, 0.6), 0.3, "Follow a corner");
  const path_tracking::Path hairpin{{0.0, 0.0}, {2.0, 0.0}, {2.0, 0.5}, {0.0, 0.5}};
  near(distance_to_path(hairpin, 0, 1, 0.5, 0.5), 0.5, "Do not reward a future return branch");

  const double parallel_cost = tracking_cost(straight, 0, 2, 0.8, 0.4, 1.0, 0.0, 6.0, 2.0);
  const double returning_cost = tracking_cost(straight, 0, 2, 0.75, 0.1, 1.0, 0.0, 6.0, 2.0);
  require(returning_cost < parallel_cost, "Prefer return over parallel offset");
  const double parallel_score = 5.0 * 0.95 + 2.0 * 0.8 + 3.0 - parallel_cost;
  const double returning_score = 5.0 * 0.9 + 2.0 * 0.6 + 3.0 - returning_cost;
  require(returning_score > parallel_score, "Return must overcome moderate clearance preference");
  require(tracking_cost(straight, 0, 2, 0.9, 0.0, 1.0, 0.0, 6.0, 2.0) <
          tracking_cost(straight, 0, 2, 0.2, 0.0, 1.0, 0.0, 6.0, 2.0),
          "Reward approaching target, not merely aligning yaw");
  near(tracking_cost(straight, 0, 2, 0.8, 0.4, 1.0, 0.0, 0.0, 0.0), 0.0,
       "Zero biases preserve legacy scoring");
    near(path_tracking::return_progress(0.4, 0.4, 0.44), 0.0,
         "Parallel travel has no lateral progress");
    require(path_tracking::is_returning(0.4, 0.35, 0.1, 0.44),
      "A five-centimeter return is meaningful within this horizon");
    require(!path_tracking::is_returning(0.4, 0.399, 0.1, 0.44),
      "Numerical-scale improvement is not a return");
    require(path_tracking::is_returning(0.11, 0.10, 0.1, 0.44),
      "Reaching the tolerance counts as returning");
    require(path_tracking::prefer_candidate(true, -10.0, false, 100.0),
      "A safe meaningful return beats any parallel reward");
    require(!path_tracking::prefer_candidate(false, 100.0, true, -10.0),
      "Parallel motion cannot displace an existing safe return");
    require(path_tracking::prefer_candidate(false, 2.0, false, 1.0),
      "Without a return candidate normal avoidance remains available");
    require(path_tracking::prefer_candidate(true, 2.0, true, 1.0),
      "Use scores within the returning candidate class");
    const auto left_rejoin = path_tracking::rejoin_command(0.4, 1.4, 0.22, 1.0);
    near(left_rejoin.first, 0.0, "Turn before driving across the path");
    near(left_rejoin.second, 1.0, "Steer toward the fixed waypoint now");
    const auto right_rejoin = path_tracking::rejoin_command(0.4, -1.4, 0.22, 1.0);
    near(right_rejoin.second, -1.0, "Handle the opposite detour side");
    require(path_tracking::command_error(0.0, 1.0, left_rejoin, 0.22, 1.0) <
      path_tracking::command_error(0.22, 0.0, left_rejoin, 0.22, 1.0),
      "Immediate steering must beat parallel forward motion");
      near(path_tracking::rejoin_command(0.05, 0.0, 0.22, 1.0).first, 0.075,
         "Slow down when approaching the fixed waypoint");
      require(path_tracking::rejoin_command(0.4, 0.7, 0.22, 1.0).first > 0.1,
        "A moderate heading error must allow a moving return arc");
      require(path_tracking::collision_course(0.8, 0.0, -0.42, 0.0, 0.34, 2.0),
        "A head-on obstacle must keep avoidance active");
      require(!path_tracking::collision_course(-0.5, 0.0, -0.42, 0.0, 0.34, 2.0),
        "A passed receding obstacle must release avoidance");
      require(!path_tracking::collision_course(0.5, 0.6, -0.42, 0.0, 0.34, 2.0),
        "A safe lateral pass must not suppress path rejoin");
      require(path_tracking::collision_course(0.4, 0.6, -0.2, -0.3, 0.34, 2.0),
        "A crossing obstacle must still be detected");
      require(!path_tracking::collision_course(0.5, 0.0, 0.0, 0.0, 0.34, 2.0),
        "Constant safe separation is not a closing threat");
      path_tracking::Path dense;
      for (int index = 0; index <= 30; ++index) dense.emplace_back(index * 0.2, 0.0);
      const auto reachable = [](const std::pair<double, double> &) { return true; };
      const auto pruned = path_tracking::prune_lookahead(dense, 1, 1.1, 0.4, 0.0, reachable);
      require(pruned.waypoint == 6, "Prune multiple passed points after a detour");
      near(pruned.projection.first, 1.1, "Project onto the nearest forward segment");
      near(pruned.target.first, 1.45, "Look ahead along arc length from the projection");
      const auto faster = path_tracking::prune_lookahead(dense, 1, 1.1, 0.4, 0.25, reachable);
      near(faster.lookahead, 0.65, "Increase lookahead with actual TurtleBot speeds");
      near(faster.target.first, 1.75, "Move the DWA target forward with speed");
      require(path_tracking::prune_lookahead(dense, 8, 1.1, 0.4, 0.0, reachable).waypoint >= 8,
        "Never move the pruning index backward");
      const auto obstructed = path_tracking::prune_lookahead(dense, 1, 1.1, 0.4, 0.25,
        [](const std::pair<double, double> & point) { return point.first <= 1.7; });
      near(obstructed.lookahead, 0.325, "Shorten a blocked lookahead connector");
      near(obstructed.target.first, 1.425, "Use only a reachable forward target");
      const auto blocked = path_tracking::prune_lookahead(dense, 1, 1.1, 0.4, 0.0,
        [](const std::pair<double, double> &) { return false; });
      require(blocked.waypoint == 1, "Do not prune across an unreachable connector");
      const auto finish = path_tracking::prune_lookahead(dense, 29, 5.95, 0.0, 0.25, reachable);
      require(finish.target == dense.back(), "Clamp lookahead to the final goal");
      reference_planner::Config sampling_config;
      for (double measured : {0.0, sampling_config.wheel_max}) {
        sampling_config.wheel_resolution = 0.5;
        const auto fine_samples = reference_planner::wheel_samples(measured, sampling_config);
        sampling_config.wheel_resolution = 1.0;
        const auto coarse_samples = reference_planner::wheel_samples(measured, sampling_config);
        require(fine_samples.size() > coarse_samples.size(), "Finer wheel lattice offers more arcs");
        for (double coarse : coarse_samples)
          require(std::any_of(fine_samples.begin(), fine_samples.end(), [coarse](double fine) {
            return std::abs(fine - coarse) < 1e-9;
          }), "Retain the previous wheel candidates");
        for (double sample : fine_samples)
          require(std::abs(sample) <= sampling_config.wheel_max + 1e-9, "Respect physical wheel limits");
      }
      std::cout << "Path tracking regression checks passed\n";
}
~~~~~

### codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/config/gazebo_topdown.config

~~~~~text
<?xml version="1.0"?>
<window>
  <width>1200</width>
  <height>800</height>
  <style material_theme="Light" material_primary="DeepOrange" material_accent="LightBlue" />
</window>

<plugin filename="MinimalScene" name="3D View">
  <gz-gui>
    <title>3D View</title>
    <property type="bool" key="showTitleBar">false</property>
    <property type="string" key="state">docked</property>
  </gz-gui>
  <engine>ogre2</engine>
  <scene>scene</scene>
  <ambient_light>0.6 0.6 0.6</ambient_light>
  <background_color>0.12 0.14 0.18</background_color>
  <camera_pose>4 2.5 8 0 1.5708 0</camera_pose>
</plugin>

<plugin filename="WorldControl" name="World control">
  <gz-gui>
    <title>World control</title>
    <property type="bool" key="resizable">false</property>
    <property type="double" key="height">72</property>
    <property type="string" key="state">floating</property>
  </gz-gui>
  <play_pause>true</play_pause>
  <step>true</step>
  <start_paused>false</start_paused>
  <use_event>true</use_event>
</plugin>

<plugin filename="WorldStats" name="World stats">
  <gz-gui>
    <title>World stats</title>
    <property type="bool" key="resizable">false</property>
    <property type="double" key="height">80</property>
    <property type="double" key="width">260</width>
    <property type="string" key="state">floating</property>
  </gz-gui>
  <sim_time>true</sim_time>
  <real_time>true</real_time>
  <real_time_factor>true</real_time_factor>
  <iterations>true</iterations>
</plugin>

~~~~~

### codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/config/slam.yaml

~~~~~yaml
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
~~~~~

### codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/dwa_gazebo_sim/__init__.py

~~~~~python

~~~~~

### codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/dwa_gazebo_sim/gazebo_odometry_world.py

~~~~~python
"""Create a runtime copy of the TurtleBot world with world-pose odometry."""

import copy
import tempfile
import xml.etree.ElementTree as ET


def add_world_pose_odometry(world_file, model_file):
    world_tree = ET.parse(world_file)
    world = world_tree.getroot().find("world")
    model_root = ET.parse(model_file).getroot().find("model")
    include = None if world is None else world.find("include")
    if world is None or include is None or model_root is None:
        raise ValueError("Expected a world with an included TurtleBot model")

    robot = copy.deepcopy(model_root)
    robot.set("name", include.findtext("name", "turtlebot3_waffle"))
    pose = robot.find("pose")
    if pose is None:
        pose = ET.SubElement(robot, "pose")
    pose.text = include.findtext("pose", "0 0 0 0 0 0")
    if robot.find("plugin[@name='gz::sim::systems::DiffDrive']") is None:
        raise ValueError("TurtleBot model is missing the DiffDrive plugin")

    odometry = ET.SubElement(
        robot, "plugin", filename="gz-sim-odometry-publisher-system",
        name="gz::sim::systems::OdometryPublisher",
    )
    for key, value in {
        "odom_frame": "odom",
        "robot_base_frame": "base_link",
        "odom_topic": "/world_pose_odom",
        "tf_topic": "/gazebo/world_pose_tf",
        "dimensions": 2,
        "odom_publish_frequency": 50,
        "gaussian_noise": 0,
    }.items():
        ET.SubElement(odometry, key).text = str(value)

    world.remove(include)
    world.append(robot)
    with tempfile.NamedTemporaryFile(suffix=".sdf", prefix="turtlebot_world_pose_", delete=False) as handle:
        world_tree.write(handle, encoding="utf-8", xml_declaration=True)
        return handle.name
~~~~~

### codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/dwa_gazebo_sim/gazebo_path_node.py

~~~~~python
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
~~~~~

### codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/dwa_gazebo_sim/lidar_obstacle_node.py

~~~~~python
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
                f"motion_fits={motion_fits} "
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
~~~~~

### codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/dwa_gazebo_sim/moving_obstacle_node.py

~~~~~python
import rclpy
from geometry_msgs.msg import Pose, PoseStamped
from rclpy.node import Node
from ros_gz_interfaces.srv import SetEntityPose
from std_msgs.msg import Bool


class MovingObstacle(Node):
    def __init__(self):
        super().__init__("moving_obstacle")
        self.client = self.create_client(
            SetEntityPose, "/world/dwa_world/set_pose"
        )
        self.obstacles = [
            ("moving_obstacle_1", 2.4, 0.4, 0.0, 0.20),
            ("moving_obstacle_2", 6.8, 2.1, -0.25, 0.0),
        ]
        self.time = 0.0
        self.obstacle_index = 0
        self.request_in_flight = False
        self.service_wait_logged = False
        self.sim_active = False
        self.goal_received = False
        self.create_subscription(Bool, "/sim_active", self.sim_active_callback, 10)
        self.create_subscription(PoseStamped, "/goal_pose", self.goal_callback, 10)
        self.timer = self.create_timer(0.10, self.update)

    def sim_active_callback(self, message):
        self.sim_active = bool(message.data)

    def goal_callback(self, _message):
        self.goal_received = True

    def update(self):
        if not self.goal_received:
            return

        dt = 0.10
        self.time += dt
        if not self.client.service_is_ready():
            if not self.service_wait_logged:
                self.get_logger().warning(
                    "A Gazebo set_pose szolgaltatas meg nem erheto el."
                )
                self.service_wait_logged = True
            return
        self.service_wait_logged = False
        if self.request_in_flight:
            return

        self.request_in_flight = True
        name, x, y, vx, vy = self.obstacles[self.obstacle_index]
        request = SetEntityPose.Request()
        request.entity.name = name
        request.entity.type = request.entity.MODEL
        request.pose = Pose()
        request.pose.position.x = x + vx * self.time
        request.pose.position.y = y + vy * self.time
        request.pose.position.z = 0.45
        request.pose.orientation.w = 1.0
        future = self.client.call_async(request)
        future.add_done_callback(self._handle_pose_response)

    def _handle_pose_response(self, future):
        try:
            response = future.result()
        except Exception as error:
            self.get_logger().warning(f"A Gazebo poziciofrissitese sikertelen: {error}")
        else:
            if not response.success:
                self.get_logger().warning(
                    "A Gazebo nem fogadta el a mozgó akadály pozíciófrissítését."
                )
        self.obstacle_index = (self.obstacle_index + 1) % len(self.obstacles)
        self.request_in_flight = False


def main(args=None):
    rclpy.init(args=args)
    node = MovingObstacle()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()

~~~~~

### codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/dwa_gazebo_sim/python_reference.py

~~~~~python
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
~~~~~

### codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/dwa_gazebo_sim/python_simulation_node.py

~~~~~python
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
        crossing_enabled = node.declare_parameter("enable_crossing_obstacle", False).value
        obstacle_specs = [(f"moving_obstacle_{index + 1}", obstacle)
                  for index, obstacle in enumerate(self.obstacles)
                  if crossing_enabled or index == 1]
        self.obstacles = [obstacle for _, obstacle in obstacle_specs]
        self.obstacle_names = [name for name, _ in obstacle_specs]
        self.oncoming_start_x = float(node.declare_parameter("oncoming_start_x", 2.4).value)
        if not math.isfinite(self.oncoming_start_x):
            raise ValueError("oncoming_start_x must be finite")
        self.robot_odom_x = None
        self.oncoming_started = False
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
            f"DIAG_SCENARIO crossing_enabled={crossing_enabled} "
            f"moving_models={[name for name, _ in obstacle_specs]} "
            f"oncoming_start_x={self.oncoming_start_x}")

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
        for name, obstacle, publisher in zip(self.obstacle_names, self.obstacles, self.obstacle_commands):
            moving = self.active and (name != "moving_obstacle_2" or self.oncoming_started)
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
~~~~~

### codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/dwa_gazebo_sim/python_world.py

~~~~~python
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
~~~~~

### codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/launch/bridge_and_controller.launch.py

~~~~~python
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
import os


def generate_launch_description():
    controller_share = get_package_share_directory("astar_dwa_controller")
    return LaunchDescription([
        Node(
            package="ros_gz_bridge",
            executable="parameter_bridge",
            arguments=[
                "/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist",
                "/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry",
                "/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan",
                "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
                "/world/dwa_world/set_pose@ros_gz_interfaces/srv/SetEntityPose",
            ],
            parameters=[{"use_sim_time": True}],
        ),
        Node(
            package="astar_dwa_controller",
            executable="astar_dwa_node",
            parameters=[
                os.path.join(controller_share, "config", "rosbot.yaml"),
                {"use_sim_time": True},
            ],
        ),
        Node(
            package="dwa_gazebo_sim",
            executable="moving_obstacle_node",
            parameters=[{"use_sim_time": True}],
        ),
    ])

~~~~~

### codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/launch/simulation.launch.py

~~~~~python
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
    scan_motion_threshold = 0.1
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
                     "minimum_travel_distance": scan_motion_threshold,
                     "minimum_travel_heading": scan_motion_threshold,
                     "check_min_dist_and_heading_precisely": True,
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
                         "laser_pose": laser_pose[:3], "base_link_z": base_pose[2],
                         "odom_child_frame": drive.findtext("child_frame_id", "base_footprint")}],
        ),
        LogInfo(msg=f"DIAG_SLAM_CONFIG executable={slam_executable} mode={slam_mode} "
                    f"map_file={map_file!r} initial_pose={initial_pose} "
                    f"resolution={map_resolution} scan_motion_threshold={scan_motion_threshold} params_file={slam_config}",
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
        DeclareLaunchArgument("enable_crossing_obstacle", default_value="false", choices=["true", "false"],
                      description="Include the crossing obstacle; false keeps only the oncoming obstacle"),
        DeclareLaunchArgument("enable_camera", default_value="false", choices=["true", "false"],
                      description="Enable unused camera rendering in the runtime TurtleBot model"),
        DeclareLaunchArgument("oncoming_start_x", default_value="2.4",
                      description="Start the oncoming obstacle after the robot reaches this odom x in metres"),
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

~~~~~

### codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/launch/visualization.launch.py

~~~~~python
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

~~~~~

### codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/package.xml

~~~~~xml
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

~~~~~

### codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/resource/dwa_gazebo_sim

~~~~~text

~~~~~

### codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/setup.cfg

~~~~~text
[develop]
script_dir=$base/lib/dwa_gazebo_sim
[install]
install_scripts=$base/lib/dwa_gazebo_sim

~~~~~

### codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/setup.py

~~~~~python
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
            "launch/bridge_and_controller.launch.py",
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
            "moving_obstacle_node = dwa_gazebo_sim.moving_obstacle_node:main",
            "python_simulation_node = dwa_gazebo_sim.python_simulation_node:main",
            "lidar_obstacle_node = dwa_gazebo_sim.lidar_obstacle_node:main",
        ],
    },
)

~~~~~

### codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/worlds/dwa_world.sdf

~~~~~xml
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
      <pose>6.8 1.7 0.45 0 0 0</pose>
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

~~~~~

### codes_diploma/simulation.py

~~~~~python
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

~~~~~

### Önlab/DWA_py.py

~~~~~python
import matplotlib.pyplot as plt     # kirajzolásra- szimuláció           --> cmd:pip install matplotlib numpy
import math                         # matematikai műveletekre pl.:pi

import numpy as np      #gyorsabb számolás miatt --> ez C-ben írodott

import pandas as pd
import time
"""
get_robot_kinematics : a kerékadatokból v,w párokat számol --> differenciális meghajtású robot elmélete
"""
def get_robot_kinematics(w_L, w_R, config):
    v = ((w_L + w_R) / 2) * config.r_kerek
    w = ((w_R - w_L) / (2 * config.b)) * config.r_kerek
    return v, w

"""
Akadály osztály
"""
class Obstacle:
    def __init__(self, x, y, radius=0.1, vx=0.0, vy=0.0):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = vx  # sebesség x irányban
        self.vy = vy  # sebesség y irányban

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt


"""        
Akadályok példányosítása
"""
obstacle_list = [
    
    Obstacle(1.5, 1.0, radius=0.4),
    Obstacle(2.5, 1.2, radius=0.4),
    Obstacle(3.5, 0.8, radius=0.4),
    Obstacle(2.0, 4.0, radius=0.4),
    Obstacle(3.0, 4.2, radius=0.4),
    Obstacle(4.0, 3.8, radius=0.4),
    Obstacle(5.0, 2.5, radius=0.6),
    Obstacle(2.5, -1.0, radius=0.3, vx=0.0, vy=0.3),
    Obstacle(5.0, 6.0, radius=0.25, vx=0.0, vy=-0.5),
    Obstacle(3.5, 2.8, radius=0.2, vx=0.6, vy=0.0),
    Obstacle(6.0, 1.5, radius=0.2, vx=-0.4, vy=0.1),
    Obstacle(1.2, 5.5, radius=0.15),
    Obstacle(6.8, 4.5, radius=0.2),
    Obstacle(7.2, 2.0, radius=0.15),
    
    ]
    
"""""
    Obstacle(0.6, 0.25, radius=0.15),
    Obstacle(1.5, 0.5, radius=0.15),  
    Obstacle(2.0, -0.2, radius=0.08),
    Obstacle(0.8, 1.2, radius=0.2),
    Obstacle(2.5, 1.0, radius=0.1),
    Obstacle(1.0, 2.5, radius=0.15),
    Obstacle(3.0, 0.5, radius=0.3),
    Obstacle(4.5, 1.5, radius=0.2),
    Obstacle(2.0, 3.5, radius=0.25),
    Obstacle(5.5, 3.5, radius=0.3),
    Obstacle(4.0, 4.5, radius=0.2),
    Obstacle(6.5, 2.0, radius=0.2),
    Obstacle(2.5, 1.5, 0.25, vx=0.2, vy=0.1),  # Mozgó
    Obstacle(4.5, 1.5, 0.2, vx=-0.15, vy=0.3), # Mozgó
    Obstacle(3.0, 3.0, 0.25, vx=0.3, vy=-0.2), # Mozgó
    Obstacle(3.5, 0.0, radius=0.6, vx=0.0, vy=0.4)
    """


"""
Cél kitűzése
"""
class Goal:
    def __init__(self, x, y, tolerance=0.15):
        self.x = x
        self.y = y
        self.tolerance = tolerance

"""
Kiszámítja a megtett utat az ív mentén az első ütközésig.
Ha nincs ütközés a predict_time alatt, egy nagy értéket ad vissza.
"""
def get_dist_on_trajectory(state, config, w_L, w_R, obstacle_list):
    temp_robot = robotstate(x=state.x, y=state.y, irany=state.irany, w_L=state.w_L, w_R=state.w_R)
    accumulated_dist = 0.0
    v_actual, _ = get_robot_kinematics(w_L, w_R, config)
    
    # --- SZENZOR PARAMÉTEREK ---
    max_sensor_dist = 3.0  # 3 méterig lát el a Lidar
    fov_angle = math.radians(180) # 180 fokos látószög elöl
    
    for t in np.arange(0, config.predict_time, config.dt):
        for obs in obstacle_list:
            # 1. Szenzor szűrés: Csak azt látja, ami közel van
            dist_now = math.hypot(state.x - obs.x, state.y - obs.y)
            if dist_now > max_sensor_dist:
                continue
                
            # 2. FOV szűrés: Csak azt látja, ami előtte van (+-90 fok)
            angle_to_obs = math.atan2(obs.y - state.y, obs.x - state.x)
            diff_angle = math.atan2(math.sin(angle_to_obs - state.irany), math.cos(angle_to_obs - state.irany))
            if abs(diff_angle) > fov_angle / 2:
                continue

            # 3. DINAMIKUS PREDIKCIÓ: Hol lesz az akadály 't' idő múlva?
            obs_future_x = obs.x + obs.vx * t
            obs_future_y = obs.y + obs.vy * t
            
            dist_centers = math.hypot(temp_robot.x - obs_future_x, temp_robot.y - obs_future_y)
            
            if dist_centers <= (config.rob_radius + obs.radius + config.safety_margin):
                return accumulated_dist 
        
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
    
    #Ez a képlet le van vezetve --> admissable velocity lap
    if abs(v) <= math.sqrt(2 * robotconfig.a_max * dist_to_obs):
        return True
    return False
   
############################################################
"""#Differenciális meghajtású robot esetén"""
class robotconfig:
    def __init__(robot):
        # feltételezem hogy a negativ és poziti sebességek megegyeznek v_max = v_min és w_max=w_min --> ezeket kiszámolom a kerekek adataibol és a robot konfigurációjából/ felépítéséből
        robot.r_kerek = 0.033   #[m]
        robot.b = 0.08 #[m]
        robot.w_kerek_max = 15 #rad/s
        robot.a_max = 2 # [m/s^2] gyorsulás
       
        robot.w_kerek_min = -robot.w_kerek_max
       
        # Felbontások a mintavételezéshez (most a kerék szögsebességére vonatkozóan)
        robot.w_kerek_resolution = 1 # [rad/s] A kerék szögsebesség mintavételezési finomsága.
       
        #DWA időparaméterek
        robot.dt = 0.1 # [s] --> időléspés (felbontás)
        robot.predict_time = 3 # [s] --> mennyi időre lásson előre
   
        #robot-alakja--> legyen kör az egyszerűség kedvéért
        robot.rob_radius = robot.b + 0.02 #[m]
        
        robot.safety_margin = 0.15
       
        ########Optimalizáció###########
       
        #G(v,w)= Alfa*heading(v,w)+Beta*dist(v,w)+Gamma*vel(v,w)
        robot.Alfa = 3  #célra tarás súlya  2
        robot.Beta = 3 # Akadály kerülés súlya  2
        robot.Gamma = 7 #Sebesség súlya 5
       
"""
Robot jelenlegi állapotának eltárolása
"""
class robotstate:
    def __init__(robot, x=0, y=0, v=0, w=0, irany = 0, w_L=0, w_R=0):  #default konstruktor
        robot.x = x
        robot.y = y
        robot.v = v
        robot.w = w
        robot.irany = irany
        robot.w_L = w_L
        robot.w_R = w_R

"""
Robot állapotának frissítése
"""
def update(robot, config, w_L_target, w_R_target, dt):
    # Gyorsulás korlátozása
    max_w_dot = config.a_max / config.r_kerek  # max kerék szögsebesség változás
    
    # Korlátozzuk, hogy mennyit változhat a keréksebesség ennyi idő alatt
    w_L_new = robot.w_L + np.clip(w_L_target - robot.w_L, -max_w_dot * dt, max_w_dot * dt)
    w_R_new = robot.w_R + np.clip(w_R_target - robot.w_R, -max_w_dot * dt, max_w_dot * dt)
    
    # Most számoljuk a kinematikát a KORLÁTOZOTT sebességgel
    v, w = get_robot_kinematics(w_L_new, w_R_new, config)
    
    # Pozíció frissítés (ugyanaz, mint előbb)
    theta_0 = robot.irany
    
    if(abs(w) > 1e-6):  # kis küszöb a nullához
        robot.x += (v/w) * (math.sin(theta_0 + w*dt) - math.sin(theta_0))
        robot.y += - (v/w) * (math.cos(theta_0 + w*dt) - math.cos(theta_0))
    else:
        robot.x += v * math.cos(theta_0) * dt
        robot.y += v * math.sin(theta_0) * dt
    
    robot.irany += w * dt
    robot.v = v
    robot.w = w
    robot.w_L = w_L_new
    robot.w_R = w_R_new
    
    return np.array([robot.x, robot.y, robot.irany, robot.v, robot.w, robot.w_L, robot.w_R])

"""        
Összes választható v,w pár kiszámolása kerekekből számítva
"""
def pairstochoose (robotconfig, robotstate):

    w_dot_max = robotconfig.a_max / robotconfig.r_kerek         #w=a/r
   
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

########################Összes lehetséges válaztható pálya eltárolása ami biztonságos megállást biztosít, ez frissüljön minden egyes döntáshozásnál#######################x

def safepairs (robotconfig, state, obstacle_list):
    w_dot_max = robotconfig.a_max / robotconfig.r_kerek
    
    # Dinamikus ablak kiszámítása (mint a pairstochoose-ban)
    w_L_min_actual = max(robotconfig.w_kerek_min, state.w_L - w_dot_max * robotconfig.dt)
    w_L_max_actual = min(robotconfig.w_kerek_max, state.w_L + w_dot_max * robotconfig.dt)

    w_R_min_actual = max(robotconfig.w_kerek_min, state.w_R - w_dot_max * robotconfig.dt)
    w_R_max_actual = min(robotconfig.w_kerek_max, state.w_R + w_dot_max * robotconfig.dt)
    
    w_L_samples = np.arange(w_L_min_actual, w_L_max_actual + robotconfig.w_kerek_resolution, robotconfig.w_kerek_resolution)
    w_R_samples = np.arange(w_R_min_actual, w_R_max_actual + robotconfig.w_kerek_resolution, robotconfig.w_kerek_resolution)

    admissible_list = [] # Ebben csak a "jó" párok lesznek
    
    for w_L in w_L_samples:
        for w_R in w_R_samples:
            if AdmissableVelocity(robotconfig, w_L, w_R, state, obstacle_list):
                v, w = get_robot_kinematics(w_L, w_R, robotconfig)
                admissible_list.append([v, w, w_L, w_R])
                
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
    
    # 2. Adaptív predikció: közelebb rövidebb időre nézünk előre a precizitásért
    adaptive_predict_time = robotconfig.predict_time
    if dist_to_goal < 1.0:
        adaptive_predict_time = max(0.5, dist_to_goal * 2.0)

    alfa = robotconfig.Alfa    # Célra tartás (pl. 2.0)
    beta = robotconfig.Beta    # Akadálykerülés (pl. 1.0)
    gamma = robotconfig.Gamma          # Sebességszabályozás súlya (magasabb, hogy hallgasson a lassításra)

    for v, w, w_L, w_R in safe_list:  
        # Gyors szimuláció a jövőbeli állapot becsléséhez
        temp_robot = robotstate(x=state.x, y=state.y, irany=state.irany, w_L=state.w_L, w_R=state.w_R)
        for _ in np.arange(0, adaptive_predict_time, robotconfig.dt):
            update(temp_robot, robotconfig, w_L, w_R, robotconfig.dt)
        
        # --- PONTOZÁSI LOGIKA ---

        # A: Heading score (Irányhiba normalizálva 0 és 1 közé)
        angle_to_goal = math.atan2(goal.y - temp_robot.y, goal.x - temp_robot.x)
        error_angle = math.atan2(math.sin(angle_to_goal - temp_robot.irany), 
                                 math.cos(angle_to_goal - temp_robot.irany))
        score_heading = (math.pi - abs(error_angle)) / math.pi
        
        # B: Dist score (Akadályoktól való távolság)
        score_dist = get_dist_on_trajectory(state, robotconfig, w_L, w_R, obstacle_list)
        
        # C: Velocity score (Folytonos lassulási görbe)
        if dist_to_goal > 0.8:
            # Messze: egyszerűen jutalmazzuk a sebességet (0.0 - 1.0)
            score_vel = v / v_max_robot
        else:
            # Közel: v_target követése. v_target = távolság (pl. 0.5m-nél 0.5m/s az ideális)
            # A pontszám 1.0 ha tökéletesen tartja a lassulást, és csökken ha eltér tőle.
            v_target = max(0.0, dist_to_goal) 
            score_vel = 1.0 - (abs(v_target - v) / v_max_robot)

        # Végső pontszám kiszámítása
        score = (alfa * score_heading + 
                 beta * score_dist + 
                 gamma * score_vel)

        if score > best_score:
            best_score = score
            best_pair = [v, w, w_L, w_R]

    return best_pair, safe_list

"""
szimulációs rész
"""
def plot_all_trajectories(state, config, all_pairs, best_pair, goal, obstacles):
    # Ha sweep módban vagyunk, ne csináljon semmit
    if not plt.get_fignums(): 
        return
    
    plt.clf()
    ax = plt.gca()
    
    # Beállítjuk a keretet, hogy ne mozogjon a robot után
    ax.set_xlim(-1.0, 8.5) 
    ax.set_ylim(-1.0, 6.5)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True, linestyle='--', alpha=0.5)

    # 1. Cél és Akadályok rajzolása
    ax.plot(goal.x, goal.y, "gx", markersize=12, mew=3, label="Cél")
    for obs in obstacles:
        ax.add_patch(plt.Circle((obs.x, obs.y), obs.radius, color="red", alpha=0.3))
    
    # 2. Összes lehetséges pálya végigpörgetése
    for v, w, w_L, w_R in all_pairs:
        # PONTOS ELLENŐRZÉS: Ez-e a kiválasztott legjobb páros?
        is_best = False
        if best_pair is not None:
            if math.isclose(w_L, best_pair[2], abs_tol=1e-3) and \
               math.isclose(w_R, best_pair[3], abs_tol=1e-3):
                is_best = True

        is_safe = AdmissableVelocity(config, w_L, w_R, state, obstacles)
        dist_to_coll = get_dist_on_trajectory(state, config, w_L, w_R, obstacles)
        
        # --- SZÍNMEGHATÁROZÁS ---
        if dist_to_coll < (abs(v) * config.predict_time) or not is_safe:
            path_color = "red"    # Ütközésveszély = Piros
        elif is_best:
            path_color = "lime"   # Választott legjobb = Élénkzöld
        elif v > 0:
            path_color = "gray"   # Többi biztonságos előre = Szürke (halvány)
        else:
            path_color = "blue"   # Hátramenet = Kék (ha v < 0)

        # Megjelenítési beállítások: a legjobb út legyen legfelül és legvastagabb
        z_ord = 10 if is_best else 1
        alpha_val = 1.0 if is_best else 0.15
        lw_val = 3.5 if is_best else 0.8

        # --- JÓSOLT SZAKASZ (Trajectory rollout) ---
        ghost = robotstate(x=state.x, y=state.y, irany=state.irany, w_L=state.w_L, w_R=state.w_R)
        path_x, path_y = [ghost.x], [ghost.y]

        # Predikciós szimuláció
        for _ in np.arange(0, config.predict_time, config.dt):
            update(ghost, config, w_L, w_R, config.dt)
            path_x.append(ghost.x)
            path_y.append(ghost.y)
        
        ax.plot(path_x, path_y, color=path_color, alpha=alpha_val, linewidth=lw_val, zorder=z_ord)

        # --- FÉKEZÉSI SZAKASZ (A vonalak végén lévő ív) ---
        t_stop = abs(v) / config.a_max if abs(v) > 0 else 0
        brake_robot = robotstate(x=ghost.x, y=ghost.y, irany=ghost.irany, w_L=w_L, w_R=w_R)
        brake_x, brake_y = [brake_robot.x], [brake_robot.y]
        
        for t in np.arange(0, t_stop, config.dt):
            factor = max(0, 1.0 - (t / t_stop)) if t_stop > 0 else 0
            update(brake_robot, config, w_L * factor, w_R * factor, config.dt)
            brake_x.append(brake_robot.x)
            brake_y.append(brake_robot.y)
            
        # A fékezési szakasz mindig piros marad
        ax.plot(brake_x, brake_y, color="red", alpha=alpha_val * 0.7, linewidth=lw_val * 0.7, zorder=z_ord)

    # 3. A Robot és az aktuális megtett út nyomvonala (trail) rajzolása
    ax.add_patch(plt.Circle((state.x, state.y), config.rob_radius, color="blue", fill=False, lw=2))
    plt.arrow(state.x, state.y, config.rob_radius * math.cos(state.irany),
              config.rob_radius * math.sin(state.irany), head_width=0.05, fc='b', ec='b')

    plt.title(f"DWA Szimuláció - v: {state.v:.2f} m/s")
    plt.draw()
    plt.pause(0.01)
    

def start_original_simulation():
    conf = robotconfig()
    state = robotstate(x=0, y=0, irany=0, w_L=0, w_R=0)
    goal = Goal(x=7.0, y=5.0)
    
    plt.ion()
    plt.figure(figsize=(10, 8))

    # Állapotjelző a deadlockhoz
    is_recovering = False

    for step in range(1200): # Kicsit több lépés, mert a forgás idő
        for obs in obstacle_list:
            obs.move(conf.dt)

        best, all_pairs = optimisation(conf, state, goal, obstacle_list)
        
        # --- DEADLOCK KEZELÉS ---
        if best is None:
            is_recovering = True
            # Forgás egy helyben: ellentétes irányú keréksebességek
            # A w_kerek_max felével forgunk, hogy biztonságos legyen
            recovery_w_L = -conf.w_kerek_max * 0.3
            recovery_w_R = conf.w_kerek_max * 0.3
            
            update(state, conf, recovery_w_L, recovery_w_R, conf.dt)
            print(f"Lépés {step}: DEADLOCK! Helyben forgás...")
        else:
            is_recovering = False
            update(state, conf, best[2], best[3], conf.dt)

        # Megjelenítés
        if step % 3 == 0:
            # Ha recovery van, üres listát adunk a rajzolónak
            plot_all_trajectories(state, conf, all_pairs if best else [], best, goal, obstacle_list)
        
        if math.hypot(state.x - goal.x, state.y - goal.y) < goal.tolerance:
            print("Célba ért!")
            break

    plt.ioff()
    plt.show()
    
##################xTÁBLÁZATOS############################

def run_single_test(a, b, g):
    """
    Részletes szimulációs futás adathalászathoz.
    """
    conf = robotconfig()
    conf.Alfa = a
    conf.Beta = b
    conf.Gamma = g
    
    state = robotstate(x=0, y=0, irany=0, w_L=0, w_R=0)
    goal = Goal(x=7.0, y=5.0)
    
    # Frissített akadálylista a standard teszthez
    current_obs_list = [
        
        Obstacle(1.5, 1.0, radius=0.4), Obstacle(2.5, 1.2, radius=0.4),
        Obstacle(3.5, 0.8, radius=0.4), Obstacle(2.0, 4.0, radius=0.4),
        Obstacle(3.0, 4.2, radius=0.4), Obstacle(4.0, 3.8, radius=0.4),
        Obstacle(5.0, 2.5, radius=0.6),
        Obstacle(2.5, -1.0, radius=0.3, vx=0.0, vy=0.3),
        Obstacle(5.0, 6.0, radius=0.25, vx=0.0, vy=-0.5),
        Obstacle(3.5, 2.8, radius=0.2, vx=0.6, vy=0.0)
        
    ]

    min_dist = float('inf')
    collision = False
    total_v = 0.0
    step_count = 0
    max_steps = 600 

    for step in range(max_steps):
        for obs in current_obs_list: obs.move(conf.dt)

        for obs in current_obs_list:
            d = math.hypot(state.x - obs.x, state.y - obs.y) - (conf.rob_radius + obs.radius)
            if d < min_dist: min_dist = d
            if d <= 0:
                collision = True
                break
        if collision: break

        best, _ = optimisation(conf, state, goal, current_obs_list)
        
        if best:
            update(state, conf, best[2], best[3], conf.dt)
        else:
            update(state, conf, 0, 0, conf.dt)
            
        total_v += state.v
        step_count = step
        
        if math.hypot(state.x - goal.x, state.y - goal.y) < goal.tolerance:
            avg_v = total_v / (step_count + 1)
            return [a, b, g, "SIKER", False, round(min_dist, 3), step_count, round(avg_v, 3)]

    avg_v = total_v / (step_count + 1) if step_count > 0 else 0
    eredmeny = "ÜTKÖZÉS" if collision else "TIMEOUT"
    return [a, b, g, eredmeny, collision, round(min_dist, 3), step_count, round(avg_v, 3)]

def start_sweep():
    """
    Paraméter sweep 0-tól 10-ig minden egész értékre.
    Összesen 11 * 11 * 11 = 1331 futtatás.
    """
    import numpy as np
    sweep_results = []
    
    # Tartomány definiálása (0, 1, 2 ... 10)
    vals = np.arange(0, 11, 1) 
    total_runs = len(vals)**3
    
    print(f"--- RÉSZLETES SWEEP INDÍTÁSA ---")
    print(f"Tartomány: 0-10 | Kombinációk: {total_runs}")
    print("Ez eltarthat egy ideig, kérlek várj...")
    
    start_time = time.time()
    count = 0

    for a in vals:
        for b in vals:
            for g in vals:
                res = run_single_test(a, b, g)
                sweep_results.append(res)
                count += 1
                
                # Haladási napló minden 50. futás után
                if count % 50 == 0:
                    percent = round((count / total_runs) * 100, 1)
                    print(f"Haladás: {percent}% ({count}/{total_runs})")

    # Táblázat összeállítása
    columns = ["Alpha", "Beta", "Gamma", "Eredmény", "Ütközés", "Min_Távolság", "Lépésszám", "Átlag_Sebesség"]
    df = pd.DataFrame(sweep_results, columns=columns)
    
    # Fájl mentése (letölthető CSV)
    filename = "dwa_sweep_eredmenyek_10.csv"
    df.to_csv(filename, index=False)
    
    total_duration = round((time.time() - start_time) / 60, 2)
    print(f"\n--- SWEEP KÉSZ ---")
    print(f"Futási idő: {total_duration} perc")
    print(f"Fájl elmentve: {filename}")
    
    # Megmutatjuk a legjobb 10 sikeres futamot sebesség szerint rendezve
    print("\nLegjobb 10 konfiguráció (Sikeres, leggyorsabb szerint):")
    success_df = df[df["Eredmény"] == "SIKER"].sort_values(by="Lépésszám", ascending=True)
    print(success_df.head(10).to_string(index=False))


# --- INNEN TUDSZ VÁLTANI ---
if __name__ == "__main__":
    # 1. SWEEP MÓD (táblázat):
    #start_sweep()

    # 2. EREDETI MÓD (grafika) - Ha ezt akarod, vedd ki a '#' jelet alóla:
    start_original_simulation()
~~~~~

### Önlab/ros2_ws/readme.txt

~~~~~text
# --- TERMINÁL 1: Gazebo ---
export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:/opt/ros/jazzy/share/turtlebot3_gazebo/models
export LIBGL_ALWAYS_SOFTWARE=1
gz sim -v 4 ~/ros2_ws/src/my_gazebo_worlds/worlds/dwa_test.sdf

# --- TERMINÁL 2: Bridge + DWA (launch fájllal) ---
cd ~/ros2_ws
source install/setup.bash
ros2 launch dwa_planner dwa_launch.py

# --- TERMINÁL 3: SLAM Toolbox ---
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=True

# --- TERMINÁL 4: RViz2 ---
rviz2


🎯 RViz beállítások (egyszer elég elmenteni):
Állítsd be a Fixed Frame-et map-re

Add hozzá a Map display-t (/map topic)

Add hozzá a TF display-t
~~~~~

### Önlab/ros2_ws/src/dwa_planner/dwa_planner/__init__.py

~~~~~python

~~~~~

### Önlab/ros2_ws/src/dwa_planner/dwa_planner/dwa_node.py

~~~~~python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, PoseStamped
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import math
import numpy as np
from tf2_ros import TransformListener, Buffer
from tf2_geometry_msgs import do_transform_point
from geometry_msgs.msg import PointStamped

class DWANode(Node):
    def __init__(self):
        super().__init__('dwa_node')
        # Publikálók
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.filtered_scan_pub = self.create_publisher(LaserScan, '/scan_filtered', 10)

        # Feliratkozók
        self.create_subscription(LaserScan, '/scan', self.scan_cb, 10)
        self.create_subscription(Odometry, '/odom', self.odom_cb, 10)
        self.create_subscription(PoseStamped, '/goal_pose', self.goal_cb, 10)
        
        self.x, self.y, self.yaw = 0.0, 0.0, 0.0
        self.obstacles = []
        self.goal_x, self.goal_y = None, None
        
        # TF2 a SLAM-hez
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.map_x, self.map_y, self.map_yaw = 0.0, 0.0, 0.0
        self.use_slam = False
        
        # Timer-ek
        self.create_timer(0.05, self.update_robot_pose)
        self.create_timer(0.1, self.control_loop)
        
        self.get_logger().info("--- DWA NODE ELINDULT ---")

    def update_robot_pose(self):
        """Lekéri a robot pozícióját a map keretben (SLAM-tól)"""
        try:
            # Ellenőrizzük, hogy létezik-e a transzformáció
            if self.tf_buffer.can_transform('map', 'base_footprint', rclpy.time.Time()):
                transform = self.tf_buffer.lookup_transform('map', 'base_footprint', rclpy.time.Time())
                self.map_x = transform.transform.translation.x
                self.map_y = transform.transform.translation.y
                q = transform.transform.rotation
                self.map_yaw = math.atan2(2*(q.w*q.z + q.x*q.y), 1-2*(q.y*q.y + q.z*q.z))
                self.use_slam = True
            else:
                self.use_slam = False
        except Exception as e:
            self.use_slam = False
            pass

    def goal_cb(self, msg):
        self.goal_x, self.goal_y = msg.pose.position.x, msg.pose.position.y
        self.get_logger().info(f'Új cél: ({self.goal_x}, {self.goal_y})')

    def odom_cb(self, msg):
        self.x, self.y = msg.pose.pose.position.x, msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        self.yaw = math.atan2(2*(q.w*q.z + q.x*q.y), 1-2*(q.y*q.y + q.z*q.z))

    def scan_cb(self, msg):
        self.obstacles = []
        filtered_msg = msg
        new_ranges = list(msg.ranges)

        for i, r in enumerate(new_ranges):
            if 0.25 < r < 3.0 and not math.isinf(r):
                # A DWA belső számításához az akadályokat a robot aktuális pozíciójához viszonyítva tároljuk
                angle = msg.angle_min + i * msg.angle_increment + self.yaw
                ox = self.x + r * math.cos(angle)
                oy = self.y + r * math.sin(angle)
                self.obstacles.append([ox, oy])
            else:
                new_ranges[i] = float('inf')

        filtered_msg.ranges = new_ranges
        self.filtered_scan_pub.publish(filtered_msg)

    def control_loop(self):
        if self.goal_x is None: 
            return
        
        # Használjuk a SLAM pozíciót, ha van
        if self.use_slam:
            current_x = self.map_x
            current_y = self.map_y
            current_yaw = self.map_yaw
        else:
            current_x = self.x
            current_y = self.y
            current_yaw = self.yaw
        
        dist_to_goal = math.hypot(self.goal_x - current_x, self.goal_y - current_y)
        if dist_to_goal < 0.2:
            self.cmd_pub.publish(Twist())
            self.goal_x = None
            self.get_logger().info("CELBA ERTEM!")
            return

        best_v, best_w, max_score = 0.0, 0.0, -1e9
        
        for v in [0.2, 0.3]:  # Több sebesség opció
            for w in np.linspace(-0.8, 0.8, 11):
                new_yaw = current_yaw + w * 1.0
                px = current_x + v * math.cos(new_yaw) * 1.0
                py = current_y + v * math.sin(new_yaw) * 1.0
                
                safe = True
                for ox, oy in self.obstacles:
                    if math.hypot(px - ox, py - oy) < 0.4:
                        safe = False
                        break
                
                if safe:
                    score = -math.hypot(self.goal_x - px, self.goal_y - py)
                    if score > max_score:
                        max_score, best_v, best_w = score, v, w

        msg = Twist()
        msg.linear.x = float(best_v)
        msg.angular.z = float(best_w)
        self.cmd_pub.publish(msg)

def main():
    rclpy.init()
    rclpy.spin(DWANode())
    rclpy.shutdown()

if __name__ == '__main__':
    main()
~~~~~

### Önlab/ros2_ws/src/dwa_planner/launch/dwa_launch.py

~~~~~python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=[
                '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
                '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
                '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
                '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
                '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V'
            ],
            parameters=[{'use_sim_time': True}],
        ),
        Node(
            package='dwa_planner',
            executable='dwa_node',
            parameters=[{'use_sim_time': True}],
        ),
    ])
~~~~~

### Önlab/ros2_ws/src/dwa_planner/package.xml

~~~~~xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>dwa_planner</name>
  <version>0.0.0</version>
  <description>TODO: Package description</description>
  <maintainer email="rumdaniel@todo.todo">rumdaniel</maintainer>
  <license>TODO: License declaration</license>
	<depend>visualization_msgs</depend>
  <depend>rclpy</depend>
  <depend>geometry_msgs</depend>
  <depend>nav_msgs</depend>
  <depend>tf2_ros</depend>
  <depend>tf2</depend>
  <depend>tf2_geometry_msgs</depend>

  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>

~~~~~

### Önlab/ros2_ws/src/dwa_planner/setup.cfg

~~~~~text
[develop]
script_dir=$base/lib/dwa_planner
[install]
install_scripts=$base/lib/dwa_planner

~~~~~

### Önlab/ros2_ws/src/dwa_planner/setup.py

~~~~~python
from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'dwa_planner'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'dwa_node = dwa_planner.dwa_node:main'
        ],
    },
)
~~~~~

### Önlab/ros2_ws/src/my_gazebo_worlds/worlds/dwa_test.sdf

~~~~~xml
<?xml version="1.0" ?>
<sdf version="1.8">
    <world name="dwa_world">
        <physics name="1ms" type="ignored">
            <max_step_size>0.001</max_step_size>
        </physics>
        <plugin filename="gz-sim-physics-system" name="gz::sim::systems::Physics"/>
        <plugin filename="gz-sim-sensors-system" name="gz::sim::systems::Sensors">
            <render_engine>ogre2</render_engine>
        </plugin>
        <plugin filename="gz-sim-user-commands-system" name="gz::sim::systems::UserCommands"/>
        <plugin filename="gz-sim-scene-broadcaster-system" name="gz::sim::systems::SceneBroadcaster"/>

        <light type="directional" name="sun">
            <cast_shadows>true</cast_shadows>
            <pose>0 0 10 0 0 0</pose>
            <direction>-0.5 0.1 -0.9</direction>
        </light>

        <model name="ground_plane">
            <static>true</static>
            <link name="link">
                <collision name="c">
                    <geometry><plane><normal>0 0 1</normal></plane></geometry>
                </collision>
                <visual name="v">
                    <geometry><plane><normal>0 0 1</normal></plane></geometry>
                    <material><ambient>0.8 0.8 0.8 1</ambient><diffuse>0.8 0.8 0.8 1</diffuse></material>
                </visual>
            </link>
        </model>

        <model name="obs1">
            <pose>2.0 0.5 0.5 0 0 0</pose>
            <link name="l">
                <collision name="c"><geometry><box><size>0.5 0.5 1</size></box></geometry></collision>
                <visual name="v"><geometry><box><size>0.5 0.5 1</size></box></geometry></visual>
            </link>
        </model>

        <model name="obs2">
            <pose>3.5 -0.5 0.5 0 0 0</pose>
            <link name="l">
                <collision name="c"><geometry><box><size>0.5 0.5 1</size></box></geometry></collision>
                <visual name="v"><geometry><box><size>0.5 0.5 1</size></box></geometry></visual>
            </link>
        </model>

        <include>
            <uri>model://turtlebot3_waffle</uri>
            <name>turtlebot3_waffle</name>
            <pose>0 0 0.05 0 0 0</pose> </include>
    </world>
</sdf>

~~~~~

