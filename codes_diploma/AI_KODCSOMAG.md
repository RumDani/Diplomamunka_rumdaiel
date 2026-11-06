# AI-kódcsomag - aktuális forrássnapshot

Generálás dátuma: 2026-11-06

Ez a dokumentum a `cpp-rethink` ág forrásainak gépileg összeállított pillanatképe. A projekt tényleges forrásfájljai az alábbi fejezetcímekben megadott útvonalakon az irányadók. A Pythonos A* + DWA szimuláció külön megvalósítás; a Gazebo-integráció aktív ROS 2 vezérlője C++.

A snapshot 54 követett forrás-, konfigurációs és tesztfájlt tartalmaz: 45 aktív `codes_diploma` fájlt és 9 külön jelölt `Önlab` archív fájlt. Kihagyja a virtuális környezetet, a build/install/log könyvtárakat, a binárisokat, az eredményábrákat és a futási naplókat. Az archív kód nem része az aktív Gazebo launch-nak. A dokumentáció forrásai: `ros2_astar_dwa_gazebo/README.md`, `KODMAGYARAZATOK.md` és `DOLGOZAT_KOD_AUDIT.md`.

## Aktuális architektúra - ellenőrzött források alapján

- A Gazebo `simulation.launch.py` indítja a szimulációt, a ROS-Gazebo bridge-et, az `astar_dwa_node` C++ vezérlőt és a szimulációs mozgóakadály-node-ot.
- A C++ vezérlő fogadja az `/odom`, `/scan` és `/goal_pose` adatokat, A*-útvonalat tervez, a DWA-val lokális sebességparancsot választ, és `/cmd_vel` üzenetet ad ki.
- A világpozíciós odometria `/odom` néven érkezik; a kerék-odometria diagnosztikai célra `/gazebo/wheel_odom` néven marad elérhető.
- A C++ node a forrás szerint `odom -> base_link -> base_scan` TF-transzformációkat küld. A valós idejű helyességet Gazebo-futással kell ellenőrizni; ez a snapshot önmagában nem futási bizonyíték.
- A Pythonos Matplotlib-szimuláció és az `astar_project` könyvtár nem a ROS2/Gazebo launch vezérlője, a két megvalósítás eredményeit külön kell kezelni.

## Diplomamunka - Gazebo-fejezet ötletek

1. Ismertesd a szimulációs architektúrát, a launch által indított folyamatokat, a ROS topicokat és az adatfolyamot a LiDAR-bemenettől a `/cmd_vel` kimenetig.
2. Mutasd be az `odom -> base_link -> base_scan` TF-láncot és az `rqt_graph` szerepét. A TF geometriai koordináta-kapcsolatokat, az rqt_graph node- és topic-kapcsolatokat mutat.
3. Fogalmazz meg mérési tervet a világpozíciós és kerék-odometria összevetésére: azonos időbélyegeken mért pozícióhiba, eltérés akadálykontaktus után, valamint a célkoordinátához viszonyított végső hiba. Csak mérés után közölj számokat.
4. Különítsd el a statikus, globális térképet és a LiDAR-ból származó lokális DWA-akadályinformációt. Írd le, hogy a jelenlegi implementáció milyen adatot használ, és mi nincs megvalósítva, például a globális térkép automatikus frissítése LiDAR-ból.
5. Javasolt értékelési mutatók: célbaérési arány, útvonalhossz, futási idő, minimális akadálytávolság, célhiba és sikertelen/újratervezett esetek. Az összehasonlításhoz rögzített pályák, azonos célok, több ismétlés és dokumentált paraméterek kellenek.
6. Tárgyald a szimuláció és a valós robot közötti különbségeket: LiDAR-keret és kalibráció, odometria, késleltetés, QoS, kerékparaméterek, fizikai korlátok, vészfékezés és fokozatos tesztelés.

### Diplomamunkaszöveg készítésére használható prompt

> Készíts magyar nyelvű, diplomamunkába illeszthető fejezetet a projekt ROS 2 Jazzy- és Gazebo Sim-integrációjáról. Először ellenőrizd az aktuális `simulation.launch.py`, `astar_dwa_node.cpp`, `gazebo_odometry_world.py`, `rosbot.yaml`, RViz-konfiguráció és README tartalmát. Írd le a node-ok felelősségét, az `/odom`, `/gazebo/wheel_odom`, `/scan`, `/goal_pose` és `/cmd_vel` adatfolyamát, az `odom -> base_link -> base_scan` TF-láncot, a globális A* és lokális DWA szerepét, valamint a statikus térkép és a LiDAR-alapú akadálykezelés határait. Válaszd szét a kódból bizonyítható tényeket, a még le nem futtatott teszteket és a javasolt további méréseket. Ne találj ki mérési eredményt, teljesítményt vagy valós roboton igazolt működést. Javasolj reprodukálható Gazebo-kísérleti tervet célbaérési aránnyal, útvonalhosszal, futási idővel, minimális akadálytávolsággal és végső célhibával; mindegyikhez írd le a szükséges naplózást és az ismétlés feltételeit. A fejezet végére adj rövid korlátok és szimuláció-valós robot átvihetőségi részt. A hivatkozásokat hiteles ROS 2/Gazebo-dokumentációval és ellenőrzött szakirodalommal támaszd alá; ne tulajdoníts a projektnek olyan modult, amely nincs a jelenlegi kódban.

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

### codes_diploma/ros2_astar_dwa_gazebo/src/astar_dwa_controller/CMakeLists.txt

~~~~~text
cmake_minimum_required(VERSION 3.8)
project(astar_dwa_controller)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(visualization_msgs REQUIRED)
find_package(tf2_ros REQUIRED)

add_executable(astar_dwa_node src/astar_dwa_node.cpp)
ament_target_dependencies(astar_dwa_node rclcpp geometry_msgs nav_msgs sensor_msgs visualization_msgs tf2_ros)

install(TARGETS astar_dwa_node DESTINATION lib/${PROJECT_NAME})
install(DIRECTORY config launch rviz DESTINATION share/${PROJECT_NAME})
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
  <depend>rclcpp</depend>
  <depend>geometry_msgs</depend>
  <depend>nav_msgs</depend>
  <depend>sensor_msgs</depend>
  <depend>visualization_msgs</depend>
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
      Name: Known occupancy map
      Enabled: true
      Topic:
        Depth: 1
        Durability Policy: Transient Local
        History Policy: Keep Last
        Reliability Policy: Reliable
        Value: /astar_map
      Alpha: 0.45
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
    Fixed Frame: odom
    Frame Rate: 30
  Name: root
  Tools:
    - Class: rviz_default_plugins/Interact
    - Class: rviz_default_plugins/MoveCamera
    - Class: rviz_default_plugins/Select
    - Class: rviz_default_plugins/SetGoal
      Topic: /goal_pose
  Views:
    Current:
      Class: rviz_default_plugins/TopDownOrtho
      Name: Top view
      Angle: 0
      Scale: 3.5
      Target Frame: odom
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
    RCLCPP_INFO(get_logger(), "A* + DWA: cpp-world-pose (Gazebo tenyleges vilagpozicio)");
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

    const auto statics = planning_obstacles();
    const double now_s = now().seconds();
    const double dt = now_s - last_track_time_;
    std::vector<Track> new_tracks;
    for (const auto & cl : clusters) {
      double cx = 0.0, cy = 0.0;
      for (auto k : cl) { cx += pts[k].x; cy += pts[k].y; }
      cx /= static_cast<double>(cl.size());
      cy /= static_cast<double>(cl.size());
      const double extent = distance(pts[cl.front()].x, pts[cl.front()].y,
                                     pts[cl.back()].x, pts[cl.back()].y);
      bool near_static = false;
      for (const auto & s : statics)
        if (distance(cx, cy, s.x, s.y) < s.radius + 0.25) { near_static = true; break; }
      double vx = 0.0, vy = 0.0;
      if (!near_static && extent < 0.6 && dt > 0.02 && dt < 0.5) {
        const Track * best = nullptr;
        double best_d = 0.35;
        for (const auto & t : tracks_) {
          const double d = distance(cx, cy, t.x, t.y);
          if (d < best_d) { best_d = d; best = &t; }
        }
        if (best) {
          vx = 0.6 * best->vx + 0.4 * (cx - best->x) / dt;
          vy = 0.6 * best->vy + 0.4 * (cy - best->y) / dt;
          const double sp = std::hypot(vx, vy);
          if (sp < 0.06) { vx = 0.0; vy = 0.0; }
          else if (sp > 0.6) { vx *= 0.6 / sp; vy *= 0.6 / sp; }
        }
      }
      new_tracks.push_back({cx, cy, vx, vy});
      for (auto k : cl) { pts[k].vx = vx; pts[k].vy = vy; }
    }
    tracks_ = new_tracks;
    last_track_time_ = now_s;
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
    if (rejoin_active_) {
      // Include the reference and braking commands exactly, not only the sampling lattice.
      left_samples.push_back(std::clamp(
        (reference.first - reference.second * wheel_base_) / wheel_radius_, left_min, left_max));
      right_samples.push_back(std::clamp(
        (reference.first + reference.second * wheel_base_) / wheel_radius_, right_min, right_max));
      left_samples.push_back(std::clamp(0.0, left_min, left_max));
      right_samples.push_back(std::clamp(0.0, right_min, right_max));
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
    const Obstacle * nearest = nullptr;
    double nd = 1.2;
    for (const auto & o : sensed) {
      const double d = distance(pose_.x, pose_.y, o.x, o.y);
      if (d < nd) { nd = d; nearest = &o; }
    }
    if (nearest) {
      const double side = angle_error(
        std::atan2(nearest->y - pose_.y, nearest->x - pose_.x) - pose_.yaw);
      if (std::abs(side) > 0.15) recovery_dir_ = side > 0.0 ? -1 : 1;
    }
    return {0.0, recovery_dir_ * 0.6 * max_angular_velocity_};
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
    for (const auto & o : sensed_obstacles)
      nearest_obstacle = std::min(nearest_obstacle, distance(pose_.x, pose_.y, o.x, o.y));

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
      "utvonal_elteres=%.3f m, cmd=(%.2f, %.2f)",
      goal_x_, goal_y_, target_x, target_y, path.size(), nearest_obstacle,
      path_error, velocity.first, velocity.second);
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
  double sensed_until_{0.0};
  int recovery_dir_{1};
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
#include <limits>
#include <utility>
#include <vector>

namespace path_tracking {
using Path = std::vector<std::pair<double, double>>;

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

### codes_diploma/ros2_astar_dwa_gazebo/src/astar_dwa_controller/test/test_path_tracking.cpp

~~~~~cpp
#include "../src/path_tracking.hpp"

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
      std::cout << "Path tracking regression checks passed\n";
}
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
from launch.actions import DeclareLaunchArgument, ExecuteProcess, OpaqueFunction, SetEnvironmentVariable
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def start_simulation(context):
    package_share = get_package_share_directory("dwa_gazebo_sim")
    controller_share = get_package_share_directory("astar_dwa_controller")
    model_root = os.path.join(get_package_share_directory("turtlebot3_gazebo"), "models")
    model_file = os.path.join(model_root, "turtlebot3_waffle", "model.sdf")
    world_file = os.path.join(package_share, "worlds", "dwa_world.sdf")
    model = ET.parse(model_file).getroot()
    drive = model.find(".//plugin[@name='gz::sim::systems::DiffDrive']")
    laser = model.find(".//sensor[@type='gpu_lidar']")
    collision = model.find(".//link[@name='base_link']/collision")
    if drive is None or laser is None or collision is None:
        raise RuntimeError("Installed TurtleBot Waffle model is missing DiffDrive, LiDAR or body geometry")
    from dwa_gazebo_sim.gazebo_odometry_world import add_world_pose_odometry
    runtime_world = add_world_pose_odometry(world_file, model_file)
    body_pose = [float(value) for value in collision.findtext("pose", "0 0 0 0 0 0").split()]
    body_size = [float(value) for value in collision.findtext("geometry/box/size").split()]
    robot_radius = math.hypot(abs(body_pose[0]) + body_size[0] / 2,
                              abs(body_pose[1]) + body_size[1] / 2)
    laser_pose = [float(value) for value in laser.findtext("pose", "0 0 0 0 0 0").split()]
    return [
        SetEnvironmentVariable("GZ_SIM_RESOURCE_PATH", os.pathsep.join(
            [model_root, os.environ.get("GZ_SIM_RESOURCE_PATH", "")])),
        ExecuteProcess(cmd=["gz", "sim", "-r", "-v", LaunchConfiguration("verbose"), runtime_world],
                       output="screen"),
        Node(
            package="ros_gz_bridge", executable="parameter_bridge", output="screen",
            arguments=[
                "/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist",
                "/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry",
                "/world_pose_odom@nav_msgs/msg/Odometry[gz.msgs.Odometry",
                "/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan",
                "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
                "/world/dwa_world/set_pose@ros_gz_interfaces/srv/SetEntityPose",
            ],
            remappings=[("/odom", "/gazebo/wheel_odom"),
                        ("/world_pose_odom", "/odom")],
            parameters=[{"use_sim_time": True}],
        ),
        Node(
            package="astar_dwa_controller", executable="astar_dwa_node", name="astar_dwa_node",
            output="screen",
            parameters=[
                os.path.join(controller_share, "config", "rosbot.yaml"),
                {"use_sim_time": True,
                 "initial_pose_x": 0.0, "initial_pose_y": 0.0,
                 "robot_radius": robot_radius,
                 "wheel_radius": float(drive.findtext("wheel_radius")),
                 "wheel_base": float(drive.findtext("wheel_separation")) / 2.0,
                 "scan_offset_x": laser_pose[0],
                 "scan_offset_y": laser_pose[1],
                 "scan_offset_z": laser_pose[2],
                 "acceleration_limit": float(drive.findtext("max_linear_acceleration", "1.0")),
                 "max_linear_velocity": 0.22,
                 "gazebo_world": "dwa_world"},
            ],
        ),
        Node(package="dwa_gazebo_sim", executable="moving_obstacle_node", output="screen",
             parameters=[{"use_sim_time": True}]),
    ]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument("verbose", default_value="4"),
        DeclareLaunchArgument("software_rendering", default_value="true"),
        SetEnvironmentVariable("LIBGL_ALWAYS_SOFTWARE", "1",
                               condition=IfCondition(LaunchConfiguration("software_rendering"))),
        SetEnvironmentVariable("ROS_AUTOMATIC_DISCOVERY_RANGE", "LOCALHOST"),
        OpaqueFunction(function=start_simulation),
    ])
~~~~~

### codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/launch/visualization.launch.py

~~~~~python
from launch import LaunchDescription
from launch.actions import SetEnvironmentVariable
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
        SetEnvironmentVariable("ROS_AUTOMATIC_DISCOVERY_RANGE", "LOCALHOST"),
        SetEnvironmentVariable("QT_QPA_PLATFORM", "xcb"),
        SetEnvironmentVariable("QT_X11_NO_MITSHM", "1"),
        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            output="screen",
            arguments=["-d", rviz_config, "-f", "odom"],
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
        (os.path.join("share", package_name, "launch"), glob("launch/*.py")),
        (os.path.join("share", package_name, "config"), glob("config/*")),
        (os.path.join("share", package_name, "worlds"), glob("worlds/*.sdf")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    entry_points={
        "console_scripts": [
            "moving_obstacle_node = dwa_gazebo_sim.moving_obstacle_node:main",
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
      <pose>6.8 2.1 0.45 0 0 0</pose>
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

## Archivált Önlab-források

Ezek a fájlok a régi laborág pillanatképei, nem a cpp-rethink Gazebo launch részei.

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

