"""Klasszikus A* útvonaltervezés rácstérképen."""

import math


def _heuristic(position, goal, diagonal):
	"""Heurisztikus becslést ad a pozíció és a cél között."""
	row, column = position
	goal_row, goal_column = goal
	row_distance = abs(goal_row - row)
	column_distance = abs(goal_column - column)

	if diagonal:
		diagonal_steps = min(row_distance, column_distance)
		straight_steps = max(row_distance, column_distance) - diagonal_steps
		return diagonal_steps * math.sqrt(2) + straight_steps

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
	"""Megkeresi a legkisebb költségű utat a start és a cél között.

	A pozíciók rácskoordináták, formájuk ``(row, column)``. Ha nincs
	elérhető út, a függvény ``None`` értéket ad vissza. A
	``return_details=True`` mód a keresés közben kibővített cellákat is
	visszaadja a szimuláció és a szemléltetés számára, valamint a kiválasztott
	cellákhoz tartozó szomszédjelölteket.
	"""
	if not grid_map.is_inside(*start) or not grid_map.is_inside(*goal):
		raise ValueError("A start és a cél a térképen belül legyen.")
	if not grid_map.is_free(*start) or not grid_map.is_free(*goal):
		raise ValueError("A start és a cél szabad cella legyen.")

	open_nodes = []
	start_priority = _heuristic(start, goal, diagonal)
	open_nodes.append((start_priority, 0.0, start))

	came_from = {}
	g_costs = {start: 0.0}
	expanded_nodes = []
	search_steps = []

	while open_nodes:
		best_node = min(open_nodes)
		open_nodes.remove(best_node)
		best_priority = best_node[0]
		current_g_cost = best_node[1]
		current_position = best_node[2]

		if current_g_cost > g_costs[current_position]:
			continue

		expanded_nodes.append(current_position)

		if current_position == goal:
			path = _reconstruct_path(came_from, current_position)
			if return_details:
				return {
					"path": path,
					"expanded_nodes": expanded_nodes,
					"search_steps": search_steps,
				}
			return path

		neighbors = grid_map.get_neighbors(
			current_position[0], current_position[1], diagonal
		)
		neighbor_scores = []
		for neighbor in neighbors:
			movement_cost = _movement_cost(current_position, neighbor)
			candidate_g_cost = current_g_cost + movement_cost
			candidate_h_cost = _heuristic(neighbor, goal, diagonal)
			neighbor_scores.append(
				{
					"position": neighbor,
					"g": candidate_g_cost,
					"h": candidate_h_cost,
					"f": candidate_g_cost + candidate_h_cost,
					"accepted": candidate_g_cost < g_costs.get(neighbor, math.inf),
				}
			)
		search_steps.append(
			{
				"current": current_position,
				"neighbors": neighbors,
				"current_g": current_g_cost,
				"current_h": _heuristic(current_position, goal, diagonal),
				"current_f": current_g_cost
				+ _heuristic(current_position, goal, diagonal),
				"neighbor_scores": neighbor_scores,
			}
		)

		for neighbor in neighbors:
			movement_cost = _movement_cost(current_position, neighbor)
			new_g_cost = current_g_cost + movement_cost

			if new_g_cost >= g_costs.get(neighbor, math.inf):
				continue

			came_from[neighbor] = current_position
			g_costs[neighbor] = new_g_cost
			h_cost = _heuristic(neighbor, goal, diagonal)
			f_cost = new_g_cost + h_cost
			open_nodes.append((f_cost, new_g_cost, neighbor))

		valid_open_nodes = [
			entry
			for entry in open_nodes
			if entry[1] <= g_costs.get(entry[2], math.inf)
		]
		if valid_open_nodes:
			search_steps[-1]["next_position"] = min(valid_open_nodes)[2]
		else:
			search_steps[-1]["next_position"] = None

	if return_details:
		return {
			"path": None,
			"expanded_nodes": expanded_nodes,
			"search_steps": search_steps,
		}

	return None
