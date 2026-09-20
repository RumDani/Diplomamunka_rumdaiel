"""Klasszikus A* útvonaltervezés rácstérképen."""

import math


def _heuristic(position, goal, diagonal):
	"""Heurisztikus becslést ad a pozíció és a cél között."""
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

	if row_change == 1 and column_change == 1:
		return math.sqrt(2)
	return 1.0


def _reconstruct_path(came_from, current):
	"""A célcellától visszalépve összeállítja a startig vezető utat."""
	path_from_goal = [current]

	while current in came_from:
		previous_position = came_from[current]
		path_from_goal.append(previous_position)
		current = previous_position

	path_from_goal.reverse()
	return path_from_goal


def astar_search(grid_map, start, goal, diagonal=False, return_details=False):
	"""Megkeresi a legkisebb költségű utat a start és a cél között."""
 
	if not grid_map.is_inside(*start) or not grid_map.is_inside(*goal):
		raise ValueError("A start és a cél a térképen belül legyen.")
	if not grid_map.is_free(*start) or not grid_map.is_free(*goal):
		raise ValueError("A start és a cél szabad cella legyen.")

	open_list = [(_heuristic(start, goal, diagonal), 0.0, start)]	#heurisztika értéke, g költség, pozíció

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
			h_cost = _heuristic(neighbor, goal, diagonal)	#h költség a szomszédokhoz
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

		
		current_h_cost = _heuristic(current_position, goal, diagonal)	# a jelenlegi pozíció h költsége
		search_steps.append(
			{
				"current": current_position,
				"neighbors": neighbors,
				"current_g": current_g_cost,
				"current_h": current_h_cost,
				"current_f": current_g_cost + current_h_cost,
				"neighbor_scores": neighbor_scores,
			}
		)

		valid_open_nodes = [
			entry
			for entry in open_list
			if entry[1] <= g_costs.get(entry[2], math.inf)
		]
		priority_queue = [
			{
				"position": position,
				"g": cost,
				"h": priority - cost,
				"f": priority,
			}
			for priority, cost, position in sorted(valid_open_nodes)
		]
		search_steps[-1]["priority_queue"] = priority_queue
		search_steps[-1]["next_position"] = (
			min(valid_open_nodes)[2] if valid_open_nodes else None
		)

	if return_details:
		return {
			"path": None,
			"expanded_nodes": expanded_nodes,
			"search_steps": search_steps,
		}

	return None


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
# Az adatok működési sorrendje röviden:
#
#     szomszédos cella
#       -> g, h és f költség kiszámítása
#       -> (f, g, position) hozzáadása az open_list-hez
#       -> jobb út esetén g_costs frissítése
#       -> elavult node-ok kiszűrése valid_open_nodes segítségével
#       -> priority_queue létrehozása az áttekinthető megjelenítéshez
