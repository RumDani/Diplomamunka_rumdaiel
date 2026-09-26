"""Rovid, akadalybiztos masodfoku Bezier-utvonalsimitas."""


def _bezier_point(start, control, end, t):
	weight = 1 - t
	return (
		weight ** 2 * start[0] + 2 * weight * t * control[0] + t ** 2 * end[0],
		weight ** 2 * start[1] + 2 * weight * t * control[1] + t ** 2 * end[1],
	)


def _remove_straight_points(path):
	if len(path) < 3:
		return list(path)

	# Az egyenes szakaszok köztes cellái nem adnak új irányinformációt.
	result = [path[0]]
	for index in range(1, len(path) - 1):
		first, middle, last = path[index - 1:index + 2]
		row_a = middle[0] - first[0]
		column_a = middle[1] - first[1]
		row_b = last[0] - middle[0]
		column_b = last[1] - middle[1]
		if row_a * column_b != column_a * row_b:
			result.append(path[index])
	result.append(path[-1])
	return result


def _curve_points(start, control, end, steps, round_points):
	# Ugyanaz a Bezier-ciklus szolgál a rácsos ellenőrzéshez és a megjelenítéshez.
	points = []
	for index in range(steps + 1):
		t = index / steps
		point = _bezier_point(start, control, end, t)
		if round_points:
			point = (round(point[0]), round(point[1]))
		if not points or point != points[-1]:
			points.append(point)
	return points


def bezier_curve_points(path, samples_per_segment=10):
	if len(path) < 3:
		return list(path)

	curve = [path[0]]
	for index in range(1, len(path) - 1):
		previous = path[index - 1]
		current = path[index]
		next_point = path[index + 1]
		start = path[0] if index == 1 else (
			(previous[0] + current[0]) / 2,
			(previous[1] + current[1]) / 2,
		)
		end = path[-1] if index == len(path) - 2 else (
			(current[0] + next_point[0]) / 2,
			(current[1] + next_point[1]) / 2,
		)
		points = _curve_points(
			start, current, end,
			samples_per_segment, False
		)
		curve.extend(points[1:])
	curve.append(path[-1])
	return curve


def _valid_path(grid_map, path, diagonal):
	"""Ellenorzi a Bezierbol kapott racsutvonalat."""
	# Először a cellákat, utána a cellák közötti lépéseket ellenőrizzük.
	for cell in path:
		if not grid_map.is_free(*cell):
			return False

	for current, next_cell in zip(path, path[1:]):
		neighbors = grid_map.get_neighbors(*current, diagonal)
		if next_cell not in neighbors:
			return False
	return True


def smooth_path(grid_map, path, diagonal=False):
	"""Bezier-gorbebol keszit simabb, tovabbra is biztonsagos utat."""
	if len(path) < 3:
		return list(path)

	# Sikertelen ellenőrzéskor a hívó mindig a változatlan A* útvonalat kapja.
	path = _remove_straight_points(path)
	result = [path[0]]
	for index in range(1, len(path) - 1):
		row_span = abs(path[index + 1][0] - path[index - 1][0])
		column_span = abs(path[index + 1][1] - path[index - 1][1])
		steps = max(2, 2 * max(row_span, column_span))
		curve = _curve_points(
			path[index - 1], path[index], path[index + 1], steps, True
		)
		result.extend(point for point in curve[1:] if point != result[-1])

	if result[-1] != path[-1]:
		result.append(path[-1])
	return result if _valid_path(grid_map, result, diagonal) else list(path)


# -----------------------------------------------------------------------------
# A FÁJL RÖVID MAGYARÁZATA
#
# A modul egy A* útvonalat kap, amely (sor, oszlop) rácscellák listája.
# Először a _remove_straight_points törli az egyenes szakaszok köztes pontjait.
# Ezután a smooth_path minden megmaradt hárompontos szakaszra alkalmazza a
# másodfokú Bezier-képletet:
#
#     B(t) = (1-t)^2 * P0 + 2 * (1-t) * t * P1 + t^2 * P2
#
# Itt P0 a kezdőpont, P1 a kontrollpont, P2 a végpont, t pedig 0 es 1 kozott
# valtozik. Peldaul P0=(0,0), P1=(0,2), P2=(2,2), t=0.5 eseten B(t)=(0.5,1.5).
#
# A _curve_points ezeket a pontokat mintazza. A smooth_path a biztonsagi
# ellenorzeshez egesz racspontokra kerekiti oket, majd a _valid_path ellenorzi,
# hogy minden cella szabad-e, es minden lepes engedelyezett szomszedsagi lepes-e.
# Ha barmelyik cella foglalt vagy a lepes ervenytelen, az eredeti A* utvonalat
# adja vissza. Emiatt ez a modul nem engedelyezhet veszelyes simitott utat.
#
# A bezier_curve_points kulon, folytonos pontokat keszit. Robotmozgasra csak
# kulon biztonsagi ellenorzessel hasznalhato, mert ellenorzes nelkul a gorbe
# akadalyba hajolhat.
# -----------------------------------------------------------------------------
