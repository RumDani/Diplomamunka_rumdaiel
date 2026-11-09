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
