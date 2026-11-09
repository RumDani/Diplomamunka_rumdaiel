# A* heurisztikák.
"""Egyszerűen cserélhető heurisztikák az A* összehasonlításához."""

import math


# Manhattan-távolság.
def manhattan(position, goal):
	"""Távolság csak vízszintes és függőleges mozgáshoz."""
	return abs(position[0] - goal[0]) + abs(position[1] - goal[1])


# Euklideszi távolság.
def euclidean(position, goal):
	"""Légvonalbeli távolság."""
	row_distance = abs(position[0] - goal[0])
	column_distance = abs(position[1] - goal[1])
	return math.sqrt(row_distance ** 2 + column_distance ** 2)


# Csebisev-távolság.
def chebyshev(position, goal):
	"""A két koordinátakülönbség közül a nagyobb."""
	return max(abs(position[0] - goal[0]), abs(position[1] - goal[1]))


# Oktilis távolság (8 irányú mozgás).
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


# Heurisztika kiválasztása név alapján.
def get_heuristic(name):
	"""Visszaadja a névhez tartozó heurisztikát."""
	try:
		return HEURISTICS[name]
	except KeyError as error:
		raise ValueError(f"Ismeretlen heurisztika: {name}") from error

