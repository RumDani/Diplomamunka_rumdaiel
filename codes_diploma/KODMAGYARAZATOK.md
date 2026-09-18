# Kódmagyarázatok

Ez a dokumentum a diplomamunka kódjának részletes, magyar nyelvű magyarázatait gyűjti.

## Frissítési szabály

Ha a kód működése, paraméterei, adatszerkezete vagy algoritmusa megváltozik, a hozzá tartozó magyarázatot is ellenőrizni és szükség esetén frissíteni kell. A magyarázatnak mindig a jelenlegi kódot kell leírnia.

Az A*-fejlesztés aktuális függvényhívási és modulkapcsolati Graphviz-ábrája az [ASTAR_PROJEKT_FOLYAMATBRA.gv](ASTAR_PROJEKT_FOLYAMATBRA.gv) fájlban található. Hívási sorrend vagy fontos adatkapcsolat változásakor azt is frissíteni kell.

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
astar_search(grid_map, start, goal, diagonal=False, return_details=False)
```

Paraméterek:

- `grid_map`: a `GridMap` példánya, amely megmondja, mely cellák szabadok.
- `start`: kezdőcella `(row, column)` formában.
- `goal`: célcella `(row, column)` formában.
- `diagonal`: ha `False`, csak a négy főirány használható; ha `True`, az átlós irányok is engedélyezettek.
- `return_details`: ha `False`, csak az útvonalat adja vissza; ha `True`, az útvonal mellett a tervezés közben kibővített cellákat is visszaadja.

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

Az egyszerűbb tanulási változat egy sima `open_nodes` listát használ. A lista elemei:

```python
(f_cost, g_cost, position)
```

Az első érték az `f_cost`, ez alapján keressük meg a következő cellát. A `g_cost` az eddig megtett út költsége, a `position` pedig a cella koordinátája. A kiválasztás így történik:

```python
best_node = min(open_nodes)
open_nodes.remove(best_node)
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
        },
    ],
}
```

Az `expanded_nodes` a tervezés megfigyeléséhez kell. A cellák sorrendben kerülnek bele, amikor az A* ténylegesen kiválasztja és feldolgozza őket. A matplotlib szimuláció ezeket világoskék pontokként vagy cellaközéppontokként jeleníti meg.

Az új `search_steps` minden feldolgozott aktuális cellához eltárolja a
`GridMap.get_neighbors()` által visszaadott szomszédokat. Ez fontos különbség:
az A* egy aktuális cella összes engedélyezett szomszédját megvizsgálja, de nem
mindegyikből lesz következő `X` cella. A szomszédok költségét összehasonlítja,
majd a prioritási sorból a legjobb `f = g + h` értékű cellát választja ki.

Például a `(0, 0)` cellából a szabad szomszédok lehetnek `(0, 1)` és `(1, 0)`.
Mindkettő `N` jelölést kap a szimulációban. Ha `(0, 1)` kapja a kedvezőbb
prioritást, akkor ez lesz a következő `C`, később pedig `X`; `(1, 0)` nem tűnik
el, csak várakozó jelöltként marad a prioritási sorban. Ezért az animációban
az `N` karikák mutatják a helyi döntési lehetőségeket, az `X` pontok pedig a
tényleges feldolgozási sorrendet.

A szimuláció a súlyokat is kiírja az `N` jelölések mellett:

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

Átlós keresésnél a heurisztika az átlós lépéseket `sqrt(2)` költséggel veszi figyelembe:

```text
h = átlós lépések * sqrt(2) + egyenes lépések
```

Ez illeszkedik ahhoz, hogy az átlós cellalépés tényleges költsége is `sqrt(2)`.

## 6. A mozgási költség

Az `_movement_cost` két szomszédos cella között számol:

- egyenes lépés költsége: `1.0`;
- átlós lépés költsége: `sqrt(2)`.

Ha `resolution=0.1`, akkor ezek a cellalépések fizikailag 0,1 méteres, illetve körülbelül 0,1414 méteres mozgást jelentenek. Az alapimplementáció költségei azonban cellaegységekben maradnak.

## 7. A keresési ciklus

1. A kezdőcella bekerül a prioritási sorba.
2. A legkisebb prioritású cellát kivesszük.
3. Ha ez a cél, a `came_from` kapcsolatokból visszaépítjük az utat.
4. Egyébként lekérjük a szabad szomszédokat a `GridMap.get_neighbors` segítségével.
5. Minden szomszédra kiszámoljuk az új `g` költséget.
6. Ha ez jobb, mint a korábban ismert költség, frissítjük a szülőt és a prioritást.
7. Ha az `open_nodes` lista kiürül cél elérése nélkül, nincs út.

Az elavult lista-bejegyzéseket ez a feltétel hagyja figyelmen kívül:

```python
if current_g > g_costs[current]:
    continue
```

Erre azért van szükség, mert egy cellához később jobb út is érkezhet, miközben a régi bejegyzés még bent marad a listában. Ez a megoldás tanulási célból egyszerűbb, de nagy térképen lassabb lehet, mert a `min(open_nodes)` minden körben végignézi a listát.

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

Ezután a függvény két egymást követő cellaközéppont között `steps_per_cell` köztes pontot készít. Ha `resolution=0.2` és `steps_per_cell=8`, akkor egy egyenes cellalépés 0,2 méter, egy szimulációs lépés pedig körülbelül 0,025 méter.

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

Ez kapcsolja össze a térképet, az útvonalat és a robotot:

1. létrehozza a matplotlib ábrát;
2. kirajzolja a statikus akadályokat és a teljes cellarácsot;
3. halvány világoskék pontokkal megmutatja az A* által már vizsgált (`X`) cellákat;
4. türkiz karikákkal és `N` betűvel megmutatja az aktuális cella szomszédjelöltjeit;
5. az `N` jelöléseknél kiírja a jelölt `g`, `h` és `f` súlyát;
6. vékony türkiz vonalakkal összeköti az aktuális cellát a szomszédjelöltekkel;
7. lila vonallal összeköti a vizsgálati sorrend cellaközéppontjait;
8. narancssárga ponttal és `C` betűvel kiemeli az A* éppen vizsgált celláját;
9. a végső útvonalat kék vonallal és `O` betűvel csak a tervezési szakasz végén jeleníti meg;
10. rövid szünetet tart, hogy a tervezés eredménye megfigyelhető legyen;
11. ezután narancssárga körként mozgatja a robotot, és rajzolja a robot nyomát;
12. a cél elérésekor kiírja, hogy `A* utvonal kesz - cel elerve`.

A szimuláció automatikusan fut, `650 ms` képkockánként. Így a keresési lépések
egymás után maguktól megjelennek. A régi `X` cellák csak halvány pontként
maradnak a térképen, a részletes súlyok pedig csak az aktuális `N` szomszédoknál
láthatók, hogy az ábra ne legyen túlzsúfolt.

A betűk jelentése a képen:

- `X`: az A* ezt a cellát már kivette a prioritási sorból és megvizsgálta; a képen ez szándékosan pontként jelenik meg, hogy ne legyen minden régi cellán külön felirat;
- `C`: az animáció adott pillanatában ezt a cellát dolgozza fel az A*;
- `N`: az aktuális cellából elérhető szomszédjelölt;
- `O`: ez a cella a végső, visszaépített útvonal része.

Ezért az `X` cellákat összekötő vonal nem a robot útvonala. Ez a keresés sorrendjét mutatja,
amely kanyaroghat és sok olyan cellát is érinthet, amely végül nem kerül bele az `O` útvonalba.

A `show=False` használható teszteléskor, így az ábra létrejön, de nem nyílik meg grafikus ablak. A szimuláció szándékosan lassú, hogy külön megfigyelhető legyen az A* keresése és a robot későbbi mozgása.

## 7. `run_simulation`

```python
run_simulation()
```

Ez a szimuláció belépési pontja:

```text
create_demo_map
    -> astar_search(diagonal=True, return_details=True)
    -> expanded_nodes megjelenitese
    -> create_robot_trajectory
    -> plot_simulation
```

A fájl közvetlen futtatása:

```text
python -m codes_diploma.astar_project.astar_simulation
```

## 8. Mit mutat és mit nem mutat?

Mutatja:

- az ismert statikus rácstérképet;
- az A* által vizsgált cellák állapotát (`X`), sorrendjét és aktuális celláját (`C`);
- az aktuális cella tényleges szomszédjelöltjeit (`N`);
- az akadálykerülő A* globális útvonalat;
- a végső útvonal celláit (`O`);
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
