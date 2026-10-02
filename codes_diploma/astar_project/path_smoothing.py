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