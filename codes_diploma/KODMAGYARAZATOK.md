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
astar_search(
    grid_map, start, goal, diagonal=False, return_details=False, heuristic=None
)
```

Paraméterek:

- `grid_map`: a `GridMap` példánya, amely megmondja, mely cellák szabadok.
- `start`: kezdőcella `(row, column)` formában.
- `goal`: célcella `(row, column)` formában.
- `diagonal`: ha `False`, csak a négy főirány használható; ha `True`, az átlós irányok is engedélyezettek.
- `return_details`: ha `False`, csak az útvonalat adja vissza; ha `True`, az útvonal mellett a tervezés közben kibővített cellákat is visszaadja.
- `heuristic`: opcionális, `(position, goal)` paraméterű saját heurisztika. Ha nincs megadva, a `diagonal` értéke alapján Manhattan- vagy Euklideszi-becslés fut.

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

Az egyszerűbb tanulási változat egy sima `open_list` listát használ. A lista elemei:

```python
(f_cost, g_cost, position)
```

Az első érték az `f_cost`, ez alapján keressük meg a következő cellát. A `g_cost` az eddig megtett út költsége, a `position` pedig a cella koordinátája. A kiválasztás így történik:

```python
best_node = min(open_list)
open_list.remove(best_node)
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
            "priority_queue": [
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
mindegyikből lesz következő feldolgozott cella. A szomszédok költségét
összehasonlítja, majd a prioritási sorból a legjobb `f = g + h` értékű cellát
választja ki.

Például a `(0, 0)` cellából a szabad szomszédok lehetnek `(0, 1)` és `(1, 0)`.
Mindkettő megjelenik a `neighbor_scores` adatai között. Ha `(0, 1)` kapja a
kedvezőbb prioritást, akkor ez lesz a következő feldolgozott cella, míg
`(1, 0)` várakozó jelöltként maradhat a `priority_queue` adataiban.

A `priority_queue` ugyanezen lépés után a még várakozó, érvényes jelölteket
tárolja `f` szerint rendezve. A szimuláció bal oldali panelje ezt a listát
mutatja. A lista első eleme az a cella, amelyet az A* a következő körben
kiválasztana. A lista minden kézi `Kovetkezo` lépésnél frissül, ezért a térkép
és a prioritási sorrend együtt magyarázza az útvonal kialakulását.

A szimuláció a prioritási panelen kiírja a `neighbor_scores` és a
`priority_queue` alapján megjelenített súlyokat:

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

Átlós keresésnél az alapimplementáció egyszerű Euklideszi heurisztikát használ:

$$
h(n) = \sqrt{(row_n-row_g)^2 + (column_n-column_g)^2}
$$

Ez légvonalbeli becslést ad az aktuális cellától a célig. Nem számol az akadályokkal,
ezért az akadályok miatt ténylegesen szükséges út nem lehet rövidebb ennél.
Az átlós mozgás tényleges költsége ettől függetlenül `sqrt(2)` marad.

Az `astar_variants.py` további, összehasonlítható függvényeket tartalmaz:

- `manhattan`: vízszintes és függőleges mozgáshoz;
- `euclidean`: légvonalbeli becslés;
- `chebyshev`: az eltérő koordináták közül a nagyobbik;
- `octile`: egyenes és `sqrt(2)` költségű átlós mozgáshoz.

A kiválasztott heurisztika az `astar_search(..., heuristic=...)` paraméterrel adható át.
Például: `astar_search(grid_map, start, goal, diagonal=True, heuristic=octile)`.
Saját függvényhez elég a `(position, goal)` paramétereket fogadó függvény, például
`lambda position, goal: 0`.

## 6. A bemenetek módosítása a felületen

A `astar_simulation.py` Tkinter beállítási ablaka a `Szimulacio inditasa` gombbal
indítja el a szimulációt. Itt módosítható a térkép szélessége és magassága, a
`resolution`, a robot sugara, a start- és célcella, az átlós mozgás, valamint a
heurisztika. Az automatikus lejátszás alapértelmezés szerint be van kapcsolva,
így a tervezés és a robot mozgása kattintás nélkül végigfut; kikapcsolva a
`Kovetkezo` gombbal lehet léptetni.
A start és a cél formátuma `sor,oszlop`, például `2,17`.

Az `Utvonal simitasa` kapcsoló alapértelmezés szerint be van kapcsolva. Bekapcsolt
állapotban az A* útvonalát a
`path_smoothing.py` dolgozza fel. A jelenlegi megoldás megkeresi a közel
derékszögű kanyarokat, a valódi kanyarokhoz másodfokú Bézier-görbét készít,
majd a mintapontokat kerekítve ütközés és szomszédság szempontjából ellenőrzi.
Ha a görbe nem biztonságos, az eredeti A* útvonal marad meg.

## 7. A mozgási költség

Az `_movement_cost` két szomszédos cella között számol:

- egyenes lépés költsége: `1.0`;
- átlós lépés költsége: `sqrt(2)`.

Ha `resolution=0.1`, akkor ezek a cellalépések fizikailag 0,1 méteres, illetve körülbelül 0,1414 méteres mozgást jelentenek. Az alapimplementáció költségei azonban cellaegységekben maradnak.

## 8. A keresési ciklus

1. A kezdőcella bekerül a prioritási sorba.
2. A legkisebb prioritású cellát kivesszük.
3. Ha ez a cél, a `came_from` kapcsolatokból visszaépítjük az utat.
4. Egyébként lekérjük a szabad szomszédokat a `GridMap.get_neighbors` segítségével.
5. Minden szomszédra kiszámoljuk az új `g` költséget.
6. Ha ez jobb, mint a korábban ismert költség, frissítjük a szülőt és a prioritást.
7. Ha az `open_list` lista kiürül cél elérése nélkül, nincs út.

Az elavult lista-bejegyzéseket ez a feltétel hagyja figyelmen kívül:

```python
if current_g > g_costs[current]:
    continue
```

Erre azért van szükség, mert egy cellához később jobb út is érkezhet, miközben a régi bejegyzés még bent marad a listában. Ez a megoldás tanulási célból egyszerűbb, de nagy térképen lassabb lehet, mert a `min(open_list)` minden körben végignézi a listát.

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
- a beépített és egyedi heurisztikák kiválasztását;
- a részletes `search_steps` és `priority_queue` adatok létrejöttét;
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

Ezután a függvény két egymást követő cellaközéppont között `steps_per_cell` köztes pontot készít. Alapértelmezésben `steps_per_cell=4`, ezért `resolution=0.2` esetén egy egyenes cellalépés 0,2 méter, egy szimulációs lépés pedig körülbelül 0,05 méter.

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

Ez egy szándékosan rövid, kétpaneles megjelenítő, amely a DWA-szimuláció egyszerű működéséhez hasonlóan egyetlen fő animációs ciklusban frissíti az ábrát:

1. a bal oldalon az aktuális prioritási sort mutatja `g`, `h`, `f` értékekkel;
2. ugyanitt kiírja a prioritási függvényt: $f(n)=g(n)+h(n)$, ahol `g(n)` az eddigi út költsége, `h(n)` a célhoz tartozó becslés, `f(n)` pedig a teljes prioritási érték;
3. átlós keresésnél a könnyebben értelmezhető Euklideszi heurisztikát használja: `h(n) = sqrt(dr^2 + dc^2)`, ahol `dr` és `dc` az aktuális cella és a cél sor-, illetve oszlopkülönbsége;
4. ugyanitt láthatók a lépésköltségek: egyenes lépés `1,0`, átlós lépés `sqrt(2)`, valamint a demo-paraméterek;
5. a jobb oldalon kirajzolja az akadályokat, a vizsgált cellákat, az aktuális keresési cellát, a startot és a célt;
6. a tervezés végén megjeleníti az eredeti és szükség esetén a Bézier-simított útvonalat;
7. a robot a kiválasztott trajektóriát és annak nyomát animálja;
8. az automatikus lejátszás mellett a `Kovetkezo` és `Ujrakezdes` gomb, illetve a jobb nyíl kézi vezérlést ad.

A prioritási panel a tényleges `priority_queue` tartalmát mutatja, legfeljebb
nyolc várakozó elemmel. A térképen a halvány pontok a feldolgozott
`expanded_nodes` cellák, a narancssárga jelölő az aktuális keresési cella, a
robot pedig csak a tervezési szakasz után jelenik meg. A kód nem használ külön
`X`, `N` vagy `O` szöveges cellajelöléseket.

Jelölések:

- `C`: az animáció adott pillanatában ezt a cellát dolgozza fel az A*;
- a halvány pontok: az A* által már vizsgált cellák;
- a kék szaggatott vonal: a végső, visszaépített útvonal.

A `show=False` használható teszteléskor, így az ábra létrejön, de nem nyílik meg grafikus ablak. A szimuláció kézi léptetésű, ezért a keresés és a robotmozgás egyaránt könnyen követhető. A megjelenítő nem modellez sebességet, gyorsulást vagy valódi robotkinematikát; a célja az A* működésének szemléltetése.

## 7. `run_simulation`

```python
run_simulation()
```

Ez a szimuláció belépési pontja:

```text
beállítási ablak
    -> create_demo_map
    -> astar_search(diagonal=..., heuristic=..., return_details=True)
    -> expanded_nodes megjelenitese
    -> smooth_path (ha engedélyezett)
    -> create_robot_trajectory
    -> plot_simulation
```

A tényleges belépési sorrendben a `run_simulation()` először a Tkinter
beállítási ablakot nyitja meg. Az alkalmazott értékekből a `_run_simulation()`
létrehozza a demo térképet, kiválasztja a heurisztikát, lefuttatja az A*-ot,
opcionálisan simít, majd létrehozza a trajektóriát és az animációt.

A fájl közvetlen futtatása:

```text
python -m codes_diploma.astar_project.astar_simulation
```

## 8. Mit mutat és mit nem mutat?

Mutatja:

- az ismert statikus rácstérképet;
- az A* által vizsgált cellákat (`expanded_nodes`) és az aktuális keresési cellát;
- az aktuális prioritási sor részletes adatait (`g`, `h`, `f`);
- az akadálykerülő A* globális útvonalat;
- az eredeti és a ténylegesen használt útvonalat, ha a simítás engedélyezett;
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

---

# `astar_project/path_smoothing.py`

## A jelenlegi kód

```python
def _bezier_point(start_point, control_point, end_point, parameter):
    """Egy pontot számol egy másodfokú Bézier-görbén."""


def _remove_straight_points(path):
    """Eltávolítja az egyenes szakaszok köztes pontjait."""


def bezier_curve_points(path, samples_per_segment=10):
    """Folytonos pontokat készít a valódi kanyarok körül."""


def _is_path_safe(grid_map, path, diagonal=False):
    """Kerekített cellákon ellenőrzi az akadályt és a szomszédságot."""


def smooth_path_bezier(grid_map, path, samples_per_curve=8, diagonal=False):
    """Biztonságos másodfokú Bézier-simítást készít."""


def smooth_path(grid_map, path, diagonal=False, samples_per_curve=8):
    """Kompatibilis belépési pont a Bézier-simításhoz."""
```

## 1. A fájl célja

Ez a modul az A* által készített rácsos útvonalat próbálja kevésbé tördeltté
tenni. Nem keres új utat, és nem módosítja az A* `g`, `h` vagy `f` költségeit.
Utófeldolgozásként működik:

```text
A* útvonal
    -> egyenes köztes pontok eltávolítása
    -> három kontrollpont meghatározása minden kanyarnál
    -> másodfokú Bézier-pontok mintavétele
    -> ellenőrzéshez cellákra kerekítés
    -> rácsos akadály- és szomszédsági ellenőrzés
    -> elfogadott simított út vagy eredeti útvonal
```

## 2. Az útvonal adatai

Az A* útvonala `(row, column)` párok listája. Például:

```python
[(0, 0), (0, 1), (0, 2), (1, 2)]
```

Ez azt jelenti, hogy a robot két cellát vízszintesen halad, majd egy sort
lefelé fordul. A rácskoordináta nem méterben megadott világkoordináta. Ha a
`GridMap` `resolution` értéke `0.2`, akkor egy rácslépés `0.2 m`.

## 3. A másodfokú Bézier-matematika

Egy kanyarhoz három pontot használunk:

- `P0`: a kanyar kezdőpontja;
- `P1`: az eredeti A* kanyarcellája, vagyis a kontrollpont;
- `P2`: a kanyar végpontja.

A képlet:

$$
B(t)=(1-t)^2P_0+2(1-t)tP_1+t^2P_2,
\qquad 0\leq t\leq 1.
$$

A `t` értéke `0` és `1` között változik. A görbe a `P0` pontból indul, a
`P2` pontba érkezik, és a `P1` kontrollpont felé hajlik.

### Konkrét számolási példa

Legyen:

```text
P0 = (0, 0)
P1 = (0, 2)
P2 = (2, 2)
t  = 0,5
```

Ekkor a sorérték:

```text
(1 - 0,5)^2 * 0 + 2 * (1 - 0,5) * 0,5 * 0 + 0,5^2 * 2
= 0,5
```

Az oszlopérték:

```text
(1 - 0,5)^2 * 0 + 2 * (1 - 0,5) * 0,5 * 2 + 0,5^2 * 2
= 1,5
```

A görbe mintapontja tehát `(0,5; 1,5)`. Ez folytonos koordináta, amelyet a
megjelenítő megtart, a biztonsági ellenőrzés viszont egész rácscellára kerekít.

## 4. A fontos függvények

### `_bezier_point(start_point, control_point, end_point, parameter)`

A másodfokú Bézier-képletet alkalmazza egyetlen `t` értékre. A `weight` a
`1 - t`, ezért a három pont súlya fokozatosan változik a görbe mentén.

### `_remove_straight_points(path)`

A három egymást követő pontból képzett irányvektorok kereszt-szorzatát vizsgálja.
Ha az érték nulla, a pontok egy egyenesre esnek, ezért a középső pontot nem kell
simítani. Így egyenes útvonalnál nem keletkezik felesleges görbe.

### `bezier_curve_points(path, samples_per_segment=10)`

Először eltávolítja az egyenes szakaszok köztes pontjait, majd minden valódi
kanyarhoz három pontot választ. A szomszédos élek felezőpontjai adják a `P0`
és `P2` kezdő- és végpontot, az eredeti kanyarcellája pedig a `P1` kontrollpont.
Az eredmény folytonos, lebegőpontos rácskoordinátákból áll.

### `_is_path_safe(grid_map, path, diagonal=False)`

Egész cellákra kerekíti a görbe pontjait, majd ellenőrzi, hogy minden cella
szabad-e, és minden egymást követő cella a `GridMap` engedélyezett szomszédja-e.
Így az akadályba lógó görbe és a tiltott átlós sarokvágás elutasításra kerül.

### `smooth_path_bezier(grid_map, path, samples_per_curve=8, diagonal=False)`

A rácstérképpel együtt meghívja a folytonos Bézier-simítást, majd biztonsági
ellenőrzést végez. Ha a simítás veszélyes, az eredeti A* útvonalat adja vissza.

### `smooth_path(grid_map, path, diagonal=False, samples_per_curve=8)`

Kompatibilis belépési pont, amely a `smooth_path_bezier` függvényt hívja.
Azért maradt meg, mert az `astar_simulation.py` és a korábbi hívók ezt a nevet
használják.

### `bezier_curve_points(path, samples_per_segment=10)`

Ez a függvény folytonos, lebegőpontos Bézier-pontokat készít. A szimuláció ezt
használja a robot trajektóriájához.

## 5. Kapcsolat a szimulációval

Az `astar_simulation.py` simítás nélkül az eredeti A* cellautat használja.
Simításkor a `smooth_path()` biztonsági ellenőrzéssel folytonos Bézier-pontokat
ad vissza, amelyeket a `create_robot_trajectory()` világkoordinátára alakít.
Ha a biztonsági ellenőrzés elutasítja a görbét, az eredeti A* útvonal marad.
A `plot_simulation()` `smoothed=True` jelzője ilyenkor a Bézier-vonalat a
folytonos robottrajektóriából rajzolja, ezért a megjelenített út nem esik vissza
az eredeti rácsos vonalra akkor sem, ha a kerekített cellalista változatlan marad.
A piros vonal mindig a ténylegesen használt, biztonságos trajektóriát mutatja.

Az automatikus lejátszás alapértelmezett időzítése `250 ms` a tervezési
képkockáknál és `60 ms` a robotmozgásnál. A nem simított mozgás cellánként négy
köztes mintapontot kap; a simított mozgás szakaszonként húsz Bézier-mintát
használ, hogy a görbe rácsos ellenőrzése ne ugorjon át cellákat.

## 6. Tesztelés és korlátok

A `test_path_smoothing.py` ellenőrzi, hogy:

- a Bézier-simítás eltérhet az eredeti törött úttól;
- az egyenes útvonal változatlan marad;
- akadály mellett az útvonal nem kerülhet tiltott cellába;
- a kezdő- és végpont megmarad.

Futtatás:

```text
python -m unittest codes_diploma.astar_project.tests.test_path_smoothing -v
```

Szűk folyosóban vagy akadály sarkánál a görbe elutasítható. Ilyenkor a modul
nem erőlteti a simítást, hanem az eredeti A* útvonalat tartja meg.

---

# A közös robotmag és az A*–DWA első integrációja

## 1. A fájlok célja

A `codes_diploma/robot.py` a robotmodellt, a `codes_diploma/DWA.py` a lokális DWA-t, a `codes_diploma/DWA+A.py` pedig az A* és a DWA kapcsolatát tartalmazza.

## 2. Adatfolyam és fontos adatok

Az A* bemenete `GridMap`, valamint a start- és célpont világkoordinátája. A `DWA+A.py` az `astar_search()` eredményét waypointlistává alakítja, majd a `robotstate` és `Obstacle` lista alapján meghívja az `optimisation()` függvényt. A kimenet az eredeti `[v, w, w_L, w_R]` forma.

`robotstate` mezői: `x`, `y`, `v`, `w`, `irany`, `w_L` és `w_R`. Az `Obstacle` kör alakú; a `vx` és `vy` mezők az egyenletes mozgás sebességét jelentik. A `move(dt)` frissíti az akadály helyét.

## 3. Robotparaméterek és kinematika

Az alapértelmezett `robotconfig` keréksugara `0,033 m`, tengelytávja `0,08 m`, maximális keréksebessége `15 rad/s`, időlépése `0,1 s`, előretekintése `3 s`, robotrádiusza `0,10 m`, biztonsági margója pedig `0,15 m`.

A differenciális hajtás összefüggései:

$$
v = r\frac{\omega_L + \omega_R}{2},
\qquad
\omega = r\frac{\omega_R - \omega_L}{b}
$$

Itt `r` a kerék sugara méterben, `b` a tengelytáv méterben, `omega_L` és `omega_R` a kerekek radián/másodperc egységű szögsebességei, `v` a robot lineáris sebessége méter/másodpercben, `omega` pedig a fordulási sebesség radián/másodpercben. Például `10 rad/s` azonos keréksebességnél:

$$
v = 0{,}033\frac{10+10}{2} = 0{,}33\ \mathrm{m/s},
\qquad
\omega = 0{,}033\frac{10-10}{0{,}08} = 0\ \mathrm{rad/s}
$$

Ez egyenes haladást jelent. Az `update()` az eredeti képlettel korlátozza a keréksebesség változását: egy `0,1 s` időlépésben legfeljebb `(2 / 0,033) * 0,1` radián/másodperc változás engedélyezett.

## 4. A DWA döntési menete

A `pairstochoose()` és a `safepairs()` az aktuális keréksebesség körül dinamikus ablakot képez. A `safepairs()` csak előrehaladó (`v >= 0`) párokat engedélyez. Az `optimisation()` a köztes waypointok előtt bátran halad, és csak az utolsó `0,2 m`-en igazítja a sebességet; a végső célpontnál a lassítási zóna `0,5 m`.

Egy `0,10 m` sugarú robot, egy `0,20 m` sugarú akadály és `0,15 m` margója akkor ütközik, ha a középpontok távolsága legfeljebb `0,10 + 0,20 + 0,15 = 0,45 m`. A mozgó akadálynál a távolságvizsgálat az adott predikciós időpontra számolt pozíciót használja.

Az eredeti logika szerint a `get_dist_on_trajectory()` csak a robot szenzorhatárán belüli (`3 m`) és a robot előtti `180` fokos látómezőben lévő akadályokat vizsgálja. A mozgó akadály pozíciója `x + vx * t`, illetve `y + vy * t` alapján változik. Az `AdmissableVelocity()` ezután a megállíthatóságot is ellenőrzi:

$$
|v| \leq \sqrt{2 a_{max} d}
$$

`v` a pillanatnyi lineáris sebesség, `a_max = 2,0 m/s^2` a lassulási korlát, `d` pedig az első ütközésig számított távolság. Például `d = 0,5 m` esetén a megengedett sebesség legfeljebb `sqrt(2 * 2,0 * 0,5) = 1,41 m/s`. Ha egy trajektória nem teljesíti ezt, a DWA elutasítja.

Az érvényes sebességpárok pontszáma az aktuális `Alfa = 5`, `Beta = 2`, `Gamma = 3` súlyokat használja: a célirányt, az ütközésig megtett távolságot és a sebességet kombinálja. A robot hátramenete a szimulációban tiltott. Ha nincs biztonságos pár, az `optimisation()` `(None, [])` értéket ad vissza.

## 5. A* és DWA kapcsolata

Az A* nem ad ki közvetlenül `cmd_vel` üzenetet. A `DWA+A.py` mindig az aktuális
aktív waypointot adja a DWA-nak. A következő waypoint csak akkor válik aktívvá,
ha a robot `0,20 m`-es helyzettűrésen belülre ér és a sebessége legfeljebb
`0,30 m/s`. A köztes pontoknál a befogási zóna kicsi, a végső célpontnál
viszont `0,5 m`-es lassítási zóna működik.

## 6. Biztonsági korlátok és jelenlegi határ

Az A* térkép statikus; a mozgó akadályt a jelenlegi prototípus csak a DWA lokális predikciójában kezeli. A LiDAR-pontfelhőből körakadály-listát készítő ROS2-adapter, a zajszűrés, a teljes fékezési teszt és a globális újratervezés még külön feladat. A robotmodell és a DWA-modul ezért közvetlenül nem importál ROS2- vagy Matplotlib-csomagot.

## 7. Tesztelés

Az alábbi tesztek ellenőrzik a közös robotmagot, a kinematikát, a gyorsuláskorlátot, a mozgó akadály előrejelzését, a DWA ütközéselutasítását és az A* waypoint-kimenetét:

```text
python -m unittest codes_diploma.astar_project.tests.test_robot_and_dwa codes_diploma.astar_project.tests.test_dwa_a
```

## 8. Egyszerű újrahasználat

Az A* és a DWA minimális használata:

```python
from codes_diploma.astar_project.grid_map import GridMap
from codes_diploma.DWA import optimisation
from codes_diploma.robot import Goal, Obstacle, robotconfig, robotstate

config = robotconfig()
state = robotstate(x=0.5, y=0.5)
grid_map = GridMap(width=20, height=20, resolution=0.1)
goal = Goal(1.5, 1.5)

result, safe_pairs = optimisation(config, state, goal, [Obstacle(1.0, 0.8, radius=0.15)])

if result is not None:
    linear_speed = result[0]
    angular_speed = result[1]
```

ROS2-ben a `linear_speed` értéke kerülhet a `Twist.linear.x`, az
`angular_speed` pedig a `Twist.angular.z` mezőbe. A ROS2-node feladata az
odometriából létrehozott `robotstate`, a LiDAR-ból létrehozott `Obstacle` lista
és a `Twist` publikálása.

Az új fájlok röviden:

- `robot.py`: robotállapot, kinematika és akadályok;
- `DWA.py`: DWA-sebességpárok, biztonság és pontozás;
- `DWA+A.py`: A* waypoint és DWA összekötése;
- `test_robot_and_dwa.py`, `test_dwa_a.py`: a két egység tesztjei.

Az A*–DWA teljes folyamatát a `DWA+A.py` osztálya kezeli. A `best_pair` formája
`[v, w, w_L, w_R]`; a ROS2-node a `v` és `w` értékeket `Twist.linear.x` és
`Twist.angular.z` mezőbe írhatja.

## 10. A szimulációs felület A* szerinti megjelenítése

A `codes_diploma/simulation.py` a meglévő A* szimuláció felépítését követi,
de a robotmozgást DWA-val egészíti ki. A bal oldali információs panel az A*
aktuális celláját és a prioritási sor rövid részletét mutatja. A térképen:

- a vékony vonalak a rácscellák határai;
- a sötét cellák a statikus akadályok;
- a kék pontok az A* által már vizsgált cellák;
- a narancssárga pont az A* aktuális keresési pontja;
- a sárga csillag a DWA aktuális waypointja;
- a fekete szaggatott vonal az A* globális útvonala;
- a narancssárga vonal a DWA lokális előrejelzett trajektóriája;
- a piros körök a statikus és mozgó akadályok;
- a kék vonal a robot eddigi nyomvonala.

A program indításakor az A* szimulációjához hasonló beállítási ablak jelenik
meg. Megadható a rács szélessége, magassága, felbontása, start- és célcellája,
az átlós mozgás, valamint az automatikus lejátszás. A beállított start- és
célcella rácskoordináta, például `(2, 2)`, amely a `0,2 m` felbontású térképen
a cella középpontján keresztül világkoordinátává alakul.

A szimuláció két vizuális fázisból áll. Először az A* keresés lépései jelennek
meg egymás után. Ezután minden animációs időlépésben a mozgó akadályok
frissülnek, a DWA kiválasztja a `best_pair` értéket, a `robot.py` `update()`
függvénye mozgatja a robotot, végül a rajz frissül. A globális A* és Bézier-
útvonal minden megjelenítési pontját kis piros pont jelöli; ezek a pontok a
teljes animáció alatt láthatók. A vezérlés ettől külön ritkított waypoint-listát
használ.

Az aktív waypoint-index monoton növekszik: a DWA nem választhat ki újra korábbi
útvonalpontot, és nem ugorhat át előre pontokat. Egy waypoint csak akkor vált,
ha a robot `0,20 m`-en belülre ért és a sebessége legfeljebb `0,30 m/s`. A végső waypoint elérésekor a
`plan_local()` `[0, 0, 0, 0]` parancsot ad vissza, ezért a célba ért robot nem
kap újabb mozgási utasítást.

Az indítóablakban beállítható a rács szélessége, magassága, felbontása,
akadályinflációja, start- és célcellája, továbbá az A* heurisztikája
(`manhattan`, `euclidean`, `chebyshev`, `octile`), az átlós mozgás, az
automatikus lejátszás, valamint az `Alfa`, `Beta` és `Gamma` DWA-súlyok.
Külön kapcsolóval engedélyezhető vagy kikapcsolható a waypoint-lassítás.

A Bézier-simítás kanyarainál a kontrollponttól mért vágási távolság legfeljebb
`3 * resolution` méter. Így például `0,20 m` felbontásnál legfeljebb `0,60 m`
vágás engedélyezett. Ha a görbe akadályt érintene, a biztonsági ellenőrzés az
eredeti A* útvonalat tartja meg.

## 9. Egyszerű A*–DWA szimuláció

A `codes_diploma/simulation.py` külön megjelenítési réteg. Nem tartalmaz új
útvonaltervezési vagy DWA-algoritmust, hanem a `robot.py`, a `DWA.py` és a
`DWA+A.py` függvényeit hívja meg.

A `create_scene()` létrehoz egy rácstérképet, statikus akadályokat, két mozgó
akadályt, robotállapotot és célt. A `create_simulation()` ezután A* útvonalat
keres, Matplotlib-ábrát készít, és minden animációs lépésben ezt a sorrendet
hajtja végre:

```text
mozgó akadályok frissítése
    -> aktuális waypoint kiválasztása
    -> DWA best_pair kiválasztása
    -> robot.py: update()
    -> robot, akadályok és trajektóriák kirajzolása
```

A `best_pair` formája `[v, w, w_L, w_R]`. Ha a DWA nem ad biztonságos párt,
a szimuláció nullás keréksebességgel frissíti a robotot. A narancssárga vonal
a kiválasztott keréksebesség-pár rövid előrejelzett trajektóriája, a kék vonal
pedig a robot eddigi nyomvonala.

### Futtatás

A projekt gyökeréből:

```text
python -m codes_diploma.simulation
```

## 11. A jelenlegi vegso A*--Bezier--DWA rendszer reszletes magyarazata

### 11.1. A rendszer szerepei

A rendszer negy kulon felelossegi szintet tartalmaz:

1. A `GridMap` a vilagot racsos cellakra osztja.
2. Az A* a statikus racson globalis utvonalat keres.
3. A `path_smoothing.py` a racsos ut kanyarait biztonsagos Bezier-gorbevel
     simitja.
4. A DWA rovid, lokalis mozgasparancsot valaszt a robot aktualis allapotabol,
     az akadalyokbol es az aktualis utvonalpontbol.

A fo adatfolyam:

```text
GridMap
    -> astar_search()
    -> astar_path
    -> smooth_path_bezier()
    -> bezier_path
    -> _create_waypoints()
    -> aktualis waypoint
    -> DWA optimisation()
    -> [v, w, w_L, w_R]
    -> robot.update()
```

### 11.2. `robot.py`: a robot fizikai modellje

A `robotconfig` tarolja a differencialis meghajtasu robot adatait:

- `r_kerek = 0,033 m`: a kerek sugara;
- `b = 0,08 m`: a ket kerek tengelyiranyu tavolsaga;
- `w_kerek_max = 15 rad/s`: maximalis kerekszogsebesseg;
- `a_max = 2 m/s^2`: gyorsulasi/lassulasi korlat;
- `dt = 0,1 s`: egy vezerlesi lepes idotartama;
- `predict_time = 3 s`: DWA eloretekintesi ideje;
- `rob_radius = 0,10 m`: a robot kor sugaru kozelitese;
- `safety_margin = 0,15 m`: biztonsagi tavolsag;
- `Alfa = 5`, `Beta = 2`, `Gamma = 3`: a DWA pontozasi sulya;
- `allow_reverse = False`: a szimulacioban a hatramenet tiltott.

A differencialis kerekkinematika:

$$
v = r\frac{\omega_L+\omega_R}{2}
$$

$$
\omega = r\frac{\omega_R-\omega_L}{2b}
$$

`r` a kerek sugara, `b` a tengelytav, `omega_L` es `omega_R` a bal es jobb
kerek szogsebessege, `v` a robot linearis sebessege, `omega` pedig a robot
szogsebessege.

Pelda az aktualis parameterekkel, azonos `10 rad/s` kerekszogsebessegnel:

$$
v = 0{,}033\frac{10+10}{2}=0{,}33\ \mathrm{m/s}
$$

$$
\omega = 0{,}033\frac{10-10}{2\cdot0{,}08}=0\ \mathrm{rad/s}
$$

Ez egyenes haladast jelent, mert a ket kerek azonos sebesseggel forog.

Az `update()` eloszor korlatozza a celzott kerekszogsebesseg valtozasat, majd
az aktualis `v` es `omega` ertekekkel frissiti a robot helyzetet. Nem egyetlen
ponttal ugrik a kovetkezo koordinatara, hanem a korpalyas kinematikai keplettel
szamolja ki az uj `x`, `y` es `irany` erteket.

### 11.3. Mozgo akadalyok

Az `Obstacle` adatai:

```python
Obstacle(x, y, radius, vx, vy)
```

Az `x`, `y` a kozepont, a `radius` a kor sugara, a `vx`, `vy` pedig a
vilagkoordinatas sebesseg komponensei. A szimulacios ciklus minden `dt` utan
meghivja az akadaly `move(dt)` metodusat:

$$
x_{uj}=x_{regi}+v_x\cdot dt
$$

$$
y_{uj}=y_{regi}+v_y\cdot dt
$$

Pelda: `v_y=0,25 m/s` es `dt=0,1 s` esetben az akadaly minden ciklusban
`0,025 m`-rel mozog felfele.

### 11.4. `DWA.py`: dinamikus ablak es biztonsag

A `pairstochoose()` az aktualis kerekszogsebessegek korul mintakat general.
Az ablak szelesseget az `a_max / r_kerek` kerekszoggyorsulas es a `dt` ido
hatarozza meg.

Az `AdmissableVelocity()` minden jelolt parnal meghivja a
`get_dist_on_trajectory()` metodust. Ez a kovetkezoket vizsgalja:

- legfeljebb `3 m` szenzortavolsag;
- a robot elotti `180 fokos` latomezo;
- a mozgo akadaly elore jelzett pozicioja;
- a robot, az akadaly es a biztonsagi sav egyuttes sugara.

Az elso utkozesig szamolt tavolsag legyen `d`. A megallithatosagi feltetel:

$$
|v|\leq\sqrt{2a_{max}d}
$$

Peldaul `a_max=2 m/s^2` es `d=0,5 m` eseten:

$$
|v|\leq\sqrt{2\cdot2\cdot0{,}5}=1{,}41\ \mathrm{m/s}
$$

Az ennel gyorsabb jelolt par kiesik a `safepairs()` listabol.

Az `optimisation()` a megmaradt parokat heading, akadalybiztonsag es sebesseg
alapjan pontozza. A cel kozeli lassitas csak az aktualis konfiguracio szerint
kapcsolhato; a vegso cel elerese ettol fuggetlenul explicit nullas parancsot
ad.

### 11.5. `path_smoothing.py`: a Bezier-utvonal

Az A* racspontjai torott vonalat alkotnak. A `_remove_straight_points()` az
egyenes reszek felesleges pontjait kiszedi, a valodi kanyarokat megtartja.

A masodfoku Bezier-keplet:

$$
B(t)=(1-t)^2P_0+2(1-t)tP_1+t^2P_2,
\qquad 0\leq t\leq1
$$

`P_0` a kanyar kezdopontja, `P_1` a kontrollpont, `P_2` a kanyar vegpontja.
Peldaul `t=0,5` eseten a kontrollpont a gorbe kozepere gyakorol hatast, de a
gorbe nem feltetlenul megy at pontosan a kontrollponton.

A kontrollponttol valo vagas alapertelmezetten `0,5 * resolution` meretu. A
`_is_path_safe()` a gorbe koztes pontjait cellakra bontja, ellenorzi a szabad
cellakat es a szomszedsagi kapcsolatokat. A `_has_direction_reversal()` a
lokalis visszafordulast tiltja. Ha barmelyik biztonsagi ellenorzes sikertelen,
a modul az eredeti A* utat adja vissza.

Ezert a Bezier-utvonal ketfele lehet:

- biztonsagos esetben folytonos, simitott gorbe;
- szuk vagy veszelyes kanyarban az eredeti, torott A* ut.

### 11.6. `DWA+A.py`: waypoint-allapotgep

Az `AStarDWAPlanner.plan_global()` eltarolja az `astar_path` es a
`bezier_path` listat, majd a simitott utbol vezerlesi waypointokat keszit.
Az aktiv index a `waypoint_index`.

Az aktiv waypoint csak akkor lep tovabb, ha:

1. a robot a dinamikus waypoint-turesen belul van;
2. a robot sebessege eleg kicsi;
3. vagy a skalarszorzas alapjan mar elhaladt a waypoint mellett.

Ez megakadályozza, hogy a DWA egy mar elhagyott ponthoz visszaforduljon.
Az `optimisation()` bemeneti celja az aktiv waypoint, nem egy kulon, elugro
racskoordinata.

### 11.7. `simulation.py`: grafikus szimulacio

A szimulacios ciklus sorrendje:

```text
1. A* vizsgalt cellak megjelenitese
2. statikus es mozgo akadalyak letrehozasa
3. mozgó akadalyak frissitese
4. aktiv waypoint es DWA cel meghatarozasa
5. DWA best_pair kivalsztasa
6. robot.update()
7. robotnyom, Bézier-ut, pontok es akadalyak kirajzolasa
```

A megjelenites jelolesei:

- vilagos kek pontok: A* altal vizsgalt cellak;
- zold vonal: Bézier-utvonal;
- kis piros pontok: DWA vezerlesi waypointok;
- sarga csillag: aktualis aktiv waypoint;
- narancssarga vonal: DWA rovid lokalis trajektoria;
- piros korok: statikus es mozgo akadalyak;
- kek kor: robot.

A program inditasa:

```text
python -m codes_diploma.simulation
```

Az ablakban a racs, a resolution, az akadalyinflacio, az A* heurisztika,
az Alfa/Beta/Gamma sullyok, a Bezier-simitas es a waypoint-lassitas is
allithato.

### 11.8. Teszteles

A teljes tesztcsomag parancsa:

```text
python -m unittest discover -s codes_diploma/astar_project/tests -p "test_*.py"
```

A tesztek ellenorzik az A* alapot, a racterkepet, a Bezier-biztonsagot, a
robotkinematikat, a DWA-t, az A*--DWA kapcsolatot, a mozgó akadalyat es a
szimulacios jelenetet. A legutobbi teljes ellenorzes eredmenye: `32 teszt
sikeres`.

A megjelenítés automatikusan elindul és legfeljebb `600` animációs lépést
futtat. A szimulációhoz nem kell ROS2; a Matplotlib és NumPy telepítése
szükséges.

## 12. ROS 2 / Gazebo robotfüggetlen C++ A* + DWA integráció

### 12.1. A csomag célja

Az új `ros2_astar_dwa_gazebo/src/astar_dwa_controller` csomag a korábbi
Python prototípustól független, C++17 alapú ROS 2 vezérlő. A
[astar_dwa_node.cpp](./ros2_astar_dwa_gazebo/src/astar_dwa_controller/src/astar_dwa_node.cpp)
nem tartalmaz TurtleBot3- vagy ROSbot-specifikus meghajtási kódot. Szabványos
ROS üzeneteket fogad és küld, ezért a robotmodell később topic-paraméterekkel
cserélhető.

### 12.2. Adatfolyam

```text
/scan + /odom
    -> obstacles(): világkoordinátás LiDAR-pontok, sebességbecslés
ismert statikus akadályok + /odom + /goal_pose
    -> astar(): statikus Grid cellák -> világkoordinátás útvonal
    -> control(): látható waypoint és előretekintési cél
    -> dwa(): LiDAR-alapú sebességvizsgálat és útvonalközelségi pontozás
    -> /cmd_vel
```

A `/goal_pose` üzenet új világkoordinátás célt állít be. Az A* útvonalat a
`/astar_path` `nav_msgs/Path` topicon teszi közzé. A robot számára a lényeges
interfész tehát: `LaserScan`, `Odometry`, `PoseStamped`, `Twist` és `Path`.

### 12.3. Fontos paraméterek és koordináták

Az `astar_dwa_controller/config/rosbot.yaml` tartalmazza a topic-neveket,
a célt, a `map_size` értéket, a `resolution` cellaméretet és a
`robot_radius` biztonsági sugarat. A C++ node rögzített, téglalap alakú rácsot
épít a konfigurált térképorigótól. A rácskoordináta:

```text
row = floor((y - origin_y) / resolution)
column = floor((x - origin_x) / resolution)
```

Például `resolution = 0.20 m`, `origin_y = -6.0 m`, `y = 0.4 m` esetén
`row = floor(6.4 / 0.2) = 32`. A cellaközéppont visszaalakítása:
`y = origin_y + (row + 0.5) * resolution`, ezért a 32-es sor középpontja
`-6 + 32.5 * 0.2 = 0.5 m`.

### 12.4. A* és DWA működése

Az A* prioritási sort használ. A `g` az eddigi cellaköltség, a `h` az
egyenes vonalú becslés a célig, az `f = g + h` pedig a kiválasztási érték.
Egy átlós lépés költsége `sqrt(2)`, egyenes lépésé `1`. Például egy két
egyenes és egy átlós lépés költsége `1 + 1 + 1.414 = 3.414` cellaköltség.
Átlós sarokvágás csak akkor engedélyezett, ha a két oldalsó cella is szabad.

A DWA kerék-szögsebességeket mintavételez a gyorsuláskorlátos dinamikus
ablakban. A YAML szerint az előremeneti sebesség felső határa `0.26 m/s`,
a szögsebességé `1.0 rad/s`. Az előrejelzés `0.1 s` lépéssel, a helyi
célpont távolságától függő, `0.8...2.5 s` időtávon fut. Ütközés észlelésekor
a fékezhetőség és az ütközésig hátralévő idő feltétele dönti el az elfogadást;
nem minden későbbi ütközés jelent automatikus kiesést.

A pontozás célirány-, szabad tér- és sebességtagot, továbbá a globális
útvonaltól és a helyi céltól mért távolság büntetését tartalmazza. A jelenlegi
képletet, a változók egységeit és a behelyettesítési példát a dokumentum végén
a 14. fejezet részletezi. A legnagyobb pontszámú elfogadott jelölt adja a
`/cmd_vel` parancsot; elfogadható jelölt nélkül helyben elfordulás következik.

### 12.5. ROSbot átültethetőség

A ROSbot saját bringupja biztosítja a motorvezérlést, odometriát és LiDAR-t.
Az algoritmus nem nyúl közvetlenül a motorokhoz. Ha a ROSbot például
`/rosbot/scan`, `/rosbot/odom` és `/rosbot/cmd_vel` topicokat használ, a
paraméterekkel ezek adhatók meg; a C++ forrás nem változik. A Gazebo-világ
robotmodellje jelenleg TurtleBot3, ezért a ROSbot modellcsere külön
szimulációs konfigurációs lépés, nem algoritmusmódosítás.

### 12.6. Ellenőrzés

Windows alatt a ROS fejlécek hiányában a Python launch-fájlok szintaxisa
ellenőrizhető. A tényleges C++ fordítás WSL-ben történik:

```bash
cd ~/projects/ros2_astar_dwa_gazebo
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
```

### 12.7. Ismert térkép, LiDAR és megjelenítés

Az `astar_dwa_node` kizárólag az előre ismert statikus térképet használja.
Az `known_obstacle_x`, `known_obstacle_y` és
`known_obstacle_radius` paraméterekből építi fel az A* statikus térképét.
Ez a szimulációban azt jelenti, hogy a piros és narancssárga statikus
akadályok helye előre ismert. A DWA ettől még a `/scan` aktuális mérését
használja, így az előre nem ismert vagy mozgó akadályokra is reagál.

Az automatikus `lidar_map` és `frontier` módok eltávolítva, ezért a LiDAR
csak a DWA pillanatnyi akadályvizsgálatához használatos.

A `visualization.launch.py` RViz2-konfigurációja az `odom` fix keretben
megjeleníti a TF-fa koordinátáit, a narancssárga `/scan` pontokat, a kék
odometriát és a zöld `/astar_path` útvonalat. Ez a megjelenítés nem avatkozik
be a vezérlésbe: ugyanazok a szabványos ROS topicok használhatók Gazebo-ban
és a valódi ROSboton.

### 12.8. Mozgó akadály szimuláció

A `moving_obstacle_node.py` a Gazebo `SetEntityPose` szolgáltatásán keresztül
mozgatja a `moving_obstacle` nevű kék hengert. A pozíció:

```text
x = 3.0 m
y = 1.8 m + 1.2 m * sin(0.6 * t)
```

ahol `t` másodpercben mért szimulációs idő. Például `t = 0` esetén
`y = 1.8 m`, `t = 1` esetén pedig körülbelül
`1.8 + 1.2 * 0.565 = 2.478 m`. A henger a LiDAR-ban megjelenik, és a DWA
ütközésvizsgálata a következő előrejelzett pontoknál figyelembe veszi.

### 12.9. RViz-hibakeresés és a látható működés

Az RViz konfiguráció fix koordinátakerete `odom`, nem `map`. A jelenlegi
Gazebo-változatban nincs SLAM vagy térképkiszolgáló, ezért `map` TF nem
létezik; a `Fixed Frame: map` hiba emiatt helyes hibajelzés. A
`visualization.launch.py` az `astar_dwa.rviz` konfigurációt és az `odom`
fix frame-et tölti be.

Az `astar_dwa_node` minden vezérlési ciklusban közzéteszi az
`/astar_dwa_markers` `visualization_msgs/MarkerArray` üzenetet:

- zöld gömb: aktuális A* cél/waypoint;
- zöld vonal: A* útvonal;
- piros hengerek: ismert statikus akadályok;
- kék vonal: a kiválasztott DWA sebességpár 15 lépéses előrejelzése.

Az odometriából a node dinamikusan publikálja az `odom -> base_link`, majd a
`base_link -> base_scan` TF-et. Ez teszi lehetővé, hogy az RViz a `/scan`
LiDAR-pontokat az `odom` fix frame-be transzformálja. A valós ROSboton ezt a
TF-et célszerű a robot saját bringupjára bízni; a vezérlő topic- és frame
paraméterezése mellett a szabványos interfész változatlan marad.

## 13. RViz-es célkijelölés és OccupancyGrid térkép

### A fájlok célja

Az `astar_dwa_node.cpp` most az `/astar_map` `nav_msgs/OccupancyGrid` topicot
is publikálja. Ez a `known_map` módban a statikus akadályokat, a robot
ráhagyásával inflált tiltott cellákat és a térkép szélét mutatja. Az
`astar_dwa.rviz` ehhez hozzáadja a `Known occupancy map` displayt, valamint a
`SetGoal` eszközt, amely a `/goal_pose` topicon küld célt.

### Adatfolyam és célkijelölés

Az RViz `2D Goal Pose` eszköz kattintásból és az egér húzásának irányából
`PoseStamped` üzenetet készít. A node a pozíció `x` és `y` mezőjét eltárolja
`goal_x_` és `goal_y_` értékként, naplózza az új célt, majd a következő
vezérlési ciklusban újra lefuttatja az A*-t. Például egy `(4.0, 2.0)` cél az
`odom` koordinátarendszerben a térkép origójától 4 méterre keletre és 2 méterre
északra van; a node ezt a világkoordinátát cellává alakítja.

### Térkép és koordináta-átalakítás

Az OccupancyGrid origója `(-map_size/2, -map_size/2)`, a cellaméret
`resolution`. Egy `(x, y) = (4.0, 2.0)` pont `resolution = 0.20 m` és
`map_size = 16 m` mellett:

```text
column = floor((4.0 + 8.0) / 0.20) = 60
row    = floor((2.0 + 8.0) / 0.20) = 50
```

Ez azt jelenti, hogy a pont a 80x80 cellás térkép 60. oszlopába és 50. sorába
kerül. Az akadályok körül a kód
`ceil((obstacle.radius + robot_radius) / resolution)` sugarú körben 100-as
értékű, foglalt cellákat állít be; a többi ismert szabad cella 0.

### Látható működés

A célmarker most gömbből, célfeliratból és síkbeli céljelből áll. Az A* vonal
vastagabb, a DWA előrejelzett vonala külön kék magasságban fut, továbbá a
robot footprintje és haladási nyila is látható. A `/astar_map` tartós
QoS-szal készül, ezért az RViz későbbi csatlakozásakor is megkapja az egyszer
publikált statikus térképet. A node az odom első beérkezése után, majd minden
vezérlési ciklusban meghívja a `publish_map()` függvényt. A `known_map` mód
akadálylistája nem függ a LiDAR első üzenetétől, ezért a térkép akkor is
nem üres, ha a szenzoradat néhány pillanattal később érkezik.

Az RViz célüzenete nem Gazebo-topic. A `/goal_pose` a vezérlő node bemenete;
az új cél alapján az A* útvonal újraszámolódik, majd a DWA a Gazebo felé a
`/cmd_vel` topicot használja. Ha még nincs LiDAR, a node már akkor is közzéteszi
a célmarkert, de sebességparancsot csak érvényes szenzoradat után ad.

### Korlátok és ellenőrzés

Az RViz-ből érkező cél az `odom` keretben legyen. A statikus térkép nem
tartalmazza a mozgó kék akadályt, mert annak aktuális helyét a LiDAR és a DWA
kezeli. Ellenőrizhető:

```bash
ros2 topic echo /astar_map --once
ros2 topic echo /goal_pose --once
```

Az RViz `TF` display tengelyei korábban piros X-tengelyeket és nyilakat
rajzoltak a `base_link` és `base_scan` keretekhez. Ezek vizualizációs elemek,
nem akadályok és nem A*-útvonalak; a projekt konfigurációjában a nyilak,
tengelyek és frame-nevek most ki vannak kapcsolva a tisztább nézet érdekében.

## 14. LiDAR-alapú felhalmozott térkép

### A fájl célja

Az `astar_dwa_node.cpp` `planning_source` paramétere két működést választ:
`known_map` esetén a YAML-ben megadott statikus akadályokból készül a tervezési
térkép; `lidar_map` esetén a node a LiDAR-mérésekből fokozatosan felépített
`OccupancyGrid`-et használja. Ez a mód a korábbi ismerttérképes megoldást nem
törli, csak alternatív forrást ad az A* számára.

### Adatfolyam

Az `scan()` eltárolja az új `LaserScan` üzenetet, majd `lidar_map` vagy
`frontier` módban
meghívja az `update_lidar_map()` függvényt. Ez a robot aktuális
`pose_` értékével az `odom` keretbe alakítja a LiDAR-sugarakat. A
`mark_lidar_ray()` a robot cellájától a mérési végpontig halad:

- a köztes cellák értéke `0`, vagyis szabad;
- érvényes akadálymérésnél a végpont értéke `100`, vagyis foglalt;
- `inf` vagy tartományon kívüli mérésnél a `range_max` végpontja nem lesz
  foglalt, csak a sugár köztes cellái lesznek szabadok;
- a korábbi cellaértékek megmaradnak, így a térkép összeadja a több
  pozícióból érkező megfigyeléseket.

Az `astar()` a `planning_obstacles()` eredményét használja. `lidar_map`
módban a `lidar_map_obstacles()` minden `100`-as cellából akadálypontot
képez, majd az A* a robot sugarával és a cella félméretével inflálja az
akadály környezetét. A DWA ettől külön továbbra is az aktuális, nyers
`obstacles()` LiDAR-pontokat használja. A lokális DWA csak a robot előtti
180 fokos és legfeljebb 3 méteres mérési tartományt használja, így a falak
és akadályok mögötti 360 fokos pontfelhő nem kényszeríti indokolatlan
megállásra vagy helyben forgásra.

### Rács, koordináták és képlet

A térkép négyzetes, oldala `map_size` méter, cellamérete `resolution` méter,
origója az `odom` rendszerben `(-map_size/2, -map_size/2)`. A
`map_cell(x, y, row, column)` képlete:

```text
column = floor((x + map_size / 2) / resolution)
row    = floor((y + map_size / 2) / resolution)
```

Itt `x` és `y` méterben mért világkoordináta, `row` és `column` egész
cellaindex. Például `map_size = 16 m`, `resolution = 0.20 m` és
`(x, y) = (4.0, 2.0)` esetén:

```text
column = floor((4.0 + 8.0) / 0.20) = floor(60.0) = 60
row    = floor((2.0 + 8.0) / 0.20) = floor(50.0) = 50
```

Ez a 80x80 cellás térkép `(50, 60)` cellája. Ha a robot
`(0, 0)` ponton áll, és egy sugár `2.0 m` távolságban, `0` radián szögben
akadályt mér, akkor a végpont `(2.0, 0.0)`, amelynek cellája:

```text
column = floor((2.0 + 8.0) / 0.20) = 50
row    = floor((0.0 + 8.0) / 0.20) = 40
```

A `mark_lidar_ray()` a robot cellájától a `(40, 50)` végpontig a diszkrét
vonal celláit jelöli szabadnak, majd a `(40, 50)` cellát foglaltra állítja.

### Megjelenítés és használat

Az `publish_map()` `lidar_map` módban közvetlenül ezt a rácsot publikálja
`/astar_map` néven. Az `OccupancyGrid` jelentése:

- `-1`: még nem látott / ismeretlen;
- `0`: LiDAR-sugár által szabadnak látott cella;
- `100`: LiDAR-mérés végpontja, feltételezett akadály.

A mód a launch paraméterével kapcsolható, a YAML alapértelmezése mellett:

```bash
ros2 launch dwa_gazebo_sim simulation.launch.py planning_source:=lidar_map
```

Ezután újra kell fordítani a workspace-t, majd a teljes
`simulation.launch.py` indítással lehet futtatni. `known_map` módban az
OccupancyGrid továbbra is a YAML statikus akadályait és a biztonsági
inflációt mutatja.

### Biztonsági korlátok

Ez a megoldás LiDAR-odometriai térkép, nem teljes SLAM. Az `odom` driftje a
térképben is megjelenhet, nincs loop closure és nincs map->odom korrekció.
A cellán kívüli sugarakat a node elutasítja. Az ismeretlen cellákat a jelenlegi egyszerű
szimulációs A* nem tiltja le, ezért a robot a cél felé haladva fedezhet fel
új területet; valódi biztonságkritikus navigációhoz az ismeretlen cellákat
blokkolni vagy Nav2/SLAM Toolbox megoldással kezelni kell.

### Ellenőrzés

A C++ változtatás WSL-ben fordítható és indítható:

```bash
cd "/mnt/c/Users/Rum Dániel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo"
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source install/setup.bash
ros2 launch dwa_gazebo_sim simulation.launch.py
```

Futás közben a térkép ellenőrzése:

```bash
ros2 topic echo /astar_map --once
```

Az üzenetben a `data` tömbben kell megjelenniük a `-1`, `0` és `100`
értékeknek; `known_map` módban a `-1` érték nem része az előre ismert
statikus térképnek.

## 15. Frontier-alapú automatikus feltérképezés

### Működés

Az új `planning_source: frontier` mód nem használ előre megadott célt. A
vezérlő induló állapota és alapértelmezett célkoordinátája `(0, 0)`, de a cél
nem aktív, ezért `known_map` és `lidar_map` módban is csak `/goal_pose`
üzenet után indul a robot. Frontier módban a node a felhalmozott LiDAR-rács
alapján automatikusan aktivál célt.

Frontier célcellának azt az ismert szabad cellát tekinti, amely:

- legalább egy 8-szomszédja még ismeretlen (`-1`);
- legalább `0.6 m` távolságra van a robottól.

A `select_frontier_goal()` a feltételeknek megfelelő szabad cellák közül a
legközelebbit választja. Ezt a világkoordinátás cellaközéppontot az A* céljaként állítja be,
majd a DWA a következő waypoint felé mozgatja a robotot. A frontier elérése
után a cél deaktiválódik, és a következő vezérlési ciklus új frontiert keres.
Ha nincs több ilyen cella, a node nulla sebességet publikál és megáll.

Ha a frontier célhoz az aktuális, inflált LiDAR-térképen az A* nem talál
útvonalat, a cél nem törlődik azonnal. A node megtartja a kiválasztott
frontiert, és korlátozott recovery-forgatást indít. A haladásfigyelő akkor is
recovery-t indít, ha több másodpercig nincs legalább `0.10 m` odometriai
elmozdulás. A forgatás legfeljebb `2.5 s`, utána új A* útvonal készül. A cél
így nem kerül törlésre, és a vezérlés nem keveri össze a DWA által választott
nullasebességet a sikeres célbaéréssel.

A LiDAR-térkép ray-castinget használ. Valós, érvényes végpontnál a sugár
köztes cellái szabadak, a végpont foglalt; `inf` vagy tartományon kívüli
mérésnél a sugár a `range_max` határig csak szabad cellákat jelöl. Így a
nyitott előre irány nem marad tévesen teljesen ismeretlen, és a frontier
kereső ténylegesen tud elérhető célcellát találni.

A Gazebo-fizika stabilitása érdekében a DWA kimenete sebességrámpán halad:
a lineáris sebesség legfeljebb `0.20 m/s`, a szögsebesség legfeljebb
`0.8 rad/s`, egy 0,1 másodperces ciklusban pedig a változás legfeljebb
`0.04 m/s` és `0.20 rad/s`. Üres A* útvonal esetén a node nulla sebességet
publikál és megáll.

### Adatfolyam és példa

```text
LiDAR -> lidar_map -> szabad/ismeretlen határ keresése
                         -> frontier cél
                         -> A* -> DWA -> /cmd_vel
                                      |
                                      +-> új LiDAR-mérés
```

Ha a robot `(0, 0)` helyen van, `resolution = 0.20 m`, és egy szabad cella
középpontja `(1.1, 0.3)`, akkor a frontier cél ez a világpont lesz. Az A*
ezt a célcellát használja; amikor a robot `0.3 m`-nél közelebb ér, a cél
lezárul, és új határcella kiválasztása indul.

### Korlátok

Ez a frontier-mód egyszerű odometria-alapú feltérképezés. Az `odom` driftje
eltolhatja a korábbi méréseket, és nincs loop closure. Az ismeretlen cellákat
az egyszerű A* átjárhatónak kezeli, miközben a frontier kiválasztása csak
ismert szabad cellára esik. Valós, biztonságkritikus roboton az ismeretlen
cellákat konzervatívan blokkolni, illetve SLAM Toolbox/Nav2 rendszert használni
célszerű.

### Indítás és ellenőrzés

```bash
ros2 launch dwa_gazebo_sim simulation.launch.py planning_source:=frontier
```

A naplóban az automatikusan kiválasztott cél ilyen formában jelenik meg:

```text
Uj frontier cel: x=..., y=... m
```

---

# `simulation.py` – 1.1 Szimulációs eredmények és forgatókönyvek

## 1. A fájl célja

A `simulation.py` az A* globális útvonaltervezést és a DWA lokális mozgástervezést
egy közös, kétdimenziós jelenetben mutatja be. A szimuláció nem csak a végső
útvonalat rajzolja ki: az A* keresés közben megjeleníti a vizsgált cellákat és
a prioritási sort, a DWA szakaszban pedig a lehetséges pályákat, a mozgó
akadályokat, a waypointot és a fékezési szakaszokat is.

Az alapbeállításokkal a térkép `30 x 20` cellás, a felbontás `0,2 m/cella`,
ezért a megjelenített terület `6,0 m x 4,0 m`. A kezdőcella `(2, 2)`, a
célcella `(17, 27)`, ahol a koordináta formája `(sor, oszlop)`. A világban
ezek középpontjai rendre `(0,5 m, 0,5 m)` és `(5,5 m, 3,5 m)`.

## 2. Adatfolyam

Az `create_scene()` elkészíti a rácstérképet, a statikus akadályokat, a két
mozgó akadályt és a robot kezdeti állapotát. Az akadályinfláció után az
`astar_search()` megkeresi a globális útvonalat. Ezt az `AStarDWAPlanner`
Bezier-simítással waypointokká alakítja. Az animáció első része az A* keresés
lépéseit, a második része pedig a DWA ciklusait futtatja:

```text
create_scene -> A* keresés -> Bezier útvonal és waypointok
             -> mozgó akadályok -> DWA pályajelöltek -> robotfrissítés
```

A `compute_onlab_trajectories()` minden DWA sebességpárhoz előre kiszámítja a
jósolt pályát, majd a pálya végéről indított fékezési szakaszt. A pálya piros,
ha ütközésveszélyes vagy a megálláshoz szükséges távolság nem elegendő; a
biztonságos pályák szürkék, a kiválasztott pálya zöld.

## 3. Fontos függvények és adatok

- `load_planner_class()`: betölti a `DWA+A.py` fájlban lévő
  `AStarDWAPlanner` osztályt.
- `parse_cell(value)`: a `"sor,oszlop"` szöveget egész koordinátapárrá alakítja.
- `create_scene(...)`: a rácsot és az akadályokat hozza létre.
- `create_simulation(...)`: elvégzi a tervezést, felépíti a Matplotlib-ábrát,
  majd visszaadja a `figure` és `FuncAnimation` objektumot.
- `compute_onlab_trajectories(...)`: a DWA jelöltek biztonságát és fékezési
  útját számolja.
- `update_frame(frame)`: A* vagy DWA állapot szerint frissíti az ábrát.
- `run_simulation()`: a Tkinter beállítóablakot indítja el.

Az ábra bal oldali információs panelje az A* lépését és prioritási értékeit,
illetve a DWA fázisban a robot helyzetét, sebességét, az összes, veszélyes és
biztonságos pályák darabszámát mutatja. A jobb oldali térképen a sötét cellák
az inflált akadályterületet, a piros körök a dinamikus vagy statikus akadályokat,
a világoszöld vonal a simított útvonalat, a kék nyomvonal pedig a robot tényleges
mozgását jelzi.

## 4. A képek értelmezése

Az alapbeállításokkal mentett képkockák a
`codes_diploma/astar_project/results/figures/` mappában találhatók.

1. `simulation_01_frame_0000.png`: az A* keresés első lépése. A bal oldali
   panelen az aktuális cella `(2, 2)`, a prioritási sorban pedig az `f` értékek
   láthatók. A világoskék pontok a már kibővített A* cellákat jelölik.
2. `simulation_02_frame_0100.png`: az A* keresés késői szakasza. A statikus
   akadályok közötti átjárók és az infláció miatt tiltott biztonsági zónák
   szemléltetik, hogy a robot nem matematikai pontként tervez útvonalat.
3. `simulation_03_frame_0250.png`: a DWA mozgás közbeni állapota. A robot
   körül sok piros és szürke jelölt pálya látható; a piros jelöltek veszélyesek,
   a szürke jelöltek a pillanatnyilag megengedett alternatívák. A vastag zöld
   görbe az aktuálisan választott pályát, a csillag a waypointot jelöli.
4. `simulation_04_frame_0500.png`: a robot a középső akadályrendszer után
   közelít a felső átjáróhoz. Ez jó kép az akadálykerülés és a waypoint-követés
   együttes bemutatására.
5. `simulation_05_frame_0650.png`: késői DWA állapot, amikor a robot már a cél
   előtti szakaszon halad. A kék nyomvonal és a zöld globális útvonal közötti
   eltérés a lokális korrekciót szemlélteti.
6. `simulation_06_frame_0725.png`: végállapot. A panelen `Cel elerve`, a
   sebesség `0,00 m/s`, a robot pedig a cél körül áll. Ez a legjobb összefoglaló
   kép a sikeres útvonaltervezés és végrehajtás bemutatására.

## 5. Konkrét számolási példa

Az alapbeállításban a célcella `(17, 27)`, a felbontás `0,2 m`, az origó
`(0,0)`. A célpont világkoordinátája:

```text
x = (27 + 0,5) * 0,2 m = 5,5 m
y = (17 + 0,5) * 0,2 m = 3,5 m
```

Az animációban a tervezési fázis 125 képkockából áll. A DWA mozgás ezért a
`movement_start = 126` képkockánál kezdődik, és legfeljebb 600 mozgási lépést
kap. A `frame = 250` kép így a `250 - 126 = 124`-edik mozgási állapot környékét
mutatja, nem egy újratervezett globális A* útvonalat.

## 6. Korlátok és indítás

A közvetlen

```text
python -m codes_diploma.simulation
```

indítás a Tkinter beállítóablakot és utána a blokkoló Matplotlib-ablakot nyitja
meg, ezért parancssori futtatásban az ablak bezárásáig nem ad vissza promptot.
Képek mentéséhez a `create_simulation(..., show=False)` visszaadott ábrájának
képkockái menthetők. A jelenlegi képek az `euclidean` heurisztikával,
átlós mozgással, `0,11 m` inflációval és Bezier-simítással készültek.

A vizsgálat nem jelent statisztikai összehasonlítást: egy rögzített jelenet
egy futását dokumentálja. Több forgatókönyvhöz külön kell változtatni például
a kezdő- és célcellát, az inflációt, a heurisztikát, a simítást vagy a DWA
`alpha`, `beta`, `gamma` súlyait, majd azonos módon menteni és összevetni a
képeket és a mérőszámokat.

## 7. Ellenőrzés

Lefutott a kért `python -m codes_diploma.simulation` parancs; a grafikus
ablakos működés miatt a folyamatot a képernyőmentésre szolgáló vezérelt futás
egészítette ki. A vezérelt futás hat képet mentett a
`codes_diploma/astar_project/results/figures/` mappába, összesen 726 animációs
képkockával. A képeken ellenőrizhető az A* tervezési szakasz, a DWA jelölt
pályái, a fékezési megjelenítés és a cél elérése.

---

# `experiments.py` és `run_experiment.py` – heurisztika- és mozgásmód-vizsgálat

## 1. A vizsgálat célja

Az összehasonlító mérés négy heurisztikát vizsgál azonos pályákon:
Manhattan, Euklideszi, Chebyshev és octile. Minden pálya két módban fut:
átlós mozgással (`diagonal=True`) és csak négy főirányú mozgással
(`diagonal=False`). Így külön látható a heurisztika hatása, valamint az,
hogy az átlós lépés megengedése vagy tiltása megváltoztatja-e a megoldhatóságot.

## 2. Pályák és adatfolyam

A `build_experiment_scenarios()` négy rögzített pályát készít:

- `original_simulation`: az eredeti `simulation.py` 30×20 cellás fal- és
  átjáróelrendezése, start `(2,2)` és cél `(17,27)` ponttal;
- `compact_corridor`: ennek kisebb, 10×7 cellás szemléltető változata;
- `corner_cutting`: saroknál elhelyezett akadályok, ahol a közös sarok
  átvágását a `GridMap.get_neighbors()` tiltja;
- `diagonal_only`: kereszt alakú akadály, amelyben a start és a cél között
  csak egy nem engedélyezett átlós átkelés lenne.

Az `original_simulation` pálya az eredeti szimuláció fal- és átjáróelrendezését
használja. A `compact_corridor` ennek kisebb, 10×7 cellás változata. A képek
elsődleges eredménye az eredeti térképen készült; az inflációt és a DWA
mozgó akadályait ez az A* összehasonlítás külön nem tartalmazza.

A `run_scenario_comparison()` minden pályát mindkét mozgásmódban, azon belül
mind a négy heurisztikával lefuttat. A `compare_heuristics()` az A* részletes
eredményéből a következőket menti: sikeresség, útvonal költsége, útvonalhossz,
vizsgált csomópontok száma és maga az útvonal. A `write_results()` az útvonal
kivételével CSV-be írja az összehasonlítható mérőszámokat.

## 3. Eredmények

Az eredményfájl:

`codes_diploma/astar_project/results/tables/heuristic_comparison.csv`

Összesen 32 sor készült: 4 pálya × 2 mozgásmód × 4 heurisztika.

Az `original_simulation` pályán főirányú mozgásnál minden heurisztika 40,00
költségű utat talált. Átlós mozgásnál a Manhattan költsége 32,38, az
Euklideszi, Chebyshev és octile változatoké 31,21 lett. Ez a különbség nem
heurisztikai hiba, hanem az engedélyezett mozgások és a heurisztika együttese.

A `compact_corridor` pályán az átjárók miatt minden konfiguráció talált utat.
Főirányú módban a költség `15,0`, átlós módban `12,0711` lett. Az
`diagonal_only` pályán viszont mind a négy heurisztika helyesen `success=False`
eredményt adott nem átlós és átlós módban is: a cél körüli akadályok miatt a
tiltott sarokátvágással sem lehet szabályos útvonalat létrehozni.

## 4. Sarokvágás kezelése

Átlós mozgás esetén sem elég azt ellenőrizni, hogy az átlós célcella szabad-e.
A `GridMap.get_neighbors()` a két köztes oldalsó cellát is megvizsgálja. Ha
például `(1,1)` cellából a `(2,2)` cellába lépne a robot, akkor a `(1,2)` és
`(2,1)` cellának is szabadnak kell lennie. Ha valamelyik akadály, az átlós
szomszédot elutasítja. Ez akadályozza meg, hogy a robot két akadály közös
sarkán fizikailag átvágjon.

A `corner_cutting` teszt ezt ellenőrzi: a talált út nem tartalmazza a
tiltott `(2,2)` sarokátvágási cellát. A teszt ugyanakkor azt is ellenőrzi,
hogy a pálya kerülő úton továbbra is megoldható marad.

## 5. Konkrét költségpélda

Az eredeti szimulációs pályán a start `(2,2)`, a cél `(17,27)`. Főirányú
módban 40 egyenes lépés szükséges. Átlós mozgásnál a start és a cél
koordinátakülönbsége `15` sor és `25` oszlop, ezért az ideális, akadályt nem
keresztező geometriai alsó becslés 15 átlós és 10 egyenes lépés:

```text
15 * sqrt(2) + 10 * 1
= 15 * 1,41421356 + 10
= 31,2132
```

Az eredeti falak miatt a tényleges út ennél hosszabb lehet. A mérésben a
Manhattan változat 32,38, a másik három heurisztika 31,21 költséget adott;
ez azt is megmutatja, hogy a Manhattan heurisztika átlós költség mellett nem
ugyanolyan természetes választás, mint az octile vagy az Euklideszi heurisztika.

Az egyenes lépés költsége 1 cella, az átlós lépés költsége
`sqrt(2) ≈ 1,4142` cella. A heurisztika a kibővített csomópontok számát
befolyásolhatja, de szabályos, megengedett mozgásoknál nem vezethet
olcsóbb útvonalhoz az optimálisnál.

## 6. Indítás és tesztelés

Az összehasonlítás indítása:

```text
python -m codes_diploma.astar_project.run_experiment
```

A célzott tesztek:

```text
python -m unittest codes_diploma.astar_project.tests.test_experiments codes_diploma.astar_project.tests.test_astar_baseline codes_diploma.astar_project.tests.test_grid_map -v
```

A futtatás eredménye: 13 teszt sikeres. A tesztek ellenőrzik mind a négy
heurisztika és mindkét mozgásmód lefutását, a nem átlós módban elutasított
megoldhatatlan pályát és a sarokvágás tiltását.

## 7. Az egységes, kontrasztos összehasonlító ábrák

Az aktuális ábrák ismét egyetlen térképen jelenítik meg mind a négy heurisztika útvonalát. A heurisztikákat nagy kontrasztú színek különböztetik meg: Manhattan kék, Euklideszi narancssárga, Chebyshev zöld, Octile lila. A folytonos vonal az átlós mozgás tiltását, a szaggatott vonal az átlós mozgás engedélyezését jelenti. Az útvonalak vastagok, fehér kontúrt kapnak, ezért a szomszédos vagy egymást fedő szakaszok is jobban elkülönülnek. A kezdőpont zöld `S`, a célpont piros `G` jelölést kapott.

Az ábrákat a `python -m codes_diploma.astar_project.generate_comparison_figures` parancs generálja újra. A program minden forgatókönyvhöz egy képet ment a `codes_diploma/astar_project/results/figures/` könyvtárba.

### 7.1. Eredeti szimulációs térkép

**Kép:** `heuristics_original_simulation.png`

**Képaláírás:** *A négy A* heurisztika útvonalainak összehasonlítása az eredeti szimulációs térképen.*

**Beilleszthető szöveg:**
Az ábra ugyanazon, 30×20 cellás térképen mutatja be a Manhattan, Euklideszi, Chebyshev és Octile heurisztika által talált útvonalakat. A szín a heurisztikát, a vonal típusa pedig a mozgási módot jelöli. Így egyetlen térképen látható, hogy az átlós lépések engedélyezése rövidebb útvonalakat eredményezhet, miközben az akadályok megkerülésének szabályai minden változatban érvényben maradnak.

### 7.2. Kisebb, átjárós ellenőrző pálya

**Kép:** `heuristics_compact_corridor.png`

**Képaláírás:** *Heurisztika-összehasonlítás kisebb, átjárókat tartalmazó rácstérképen.*

**Beilleszthető szöveg:**
A kisebb ellenőrző pálya egy függőleges és egy vízszintes akadályfalon kialakított átjárókat tartalmaz. Az ábra azt szemlélteti, hogy az összes vizsgált heurisztika képes megtalálni a falak közötti szabályos útvonalat, az átlós mozgás pedig csökkenti az útvonal geometriai költségét.

### 7.3. Sarokvágási vizsgálat

**Kép:** `heuristics_corner_cutting.png`

**Képaláírás:** *A sarokvágás elleni szomszédvizsgálat hatása átlós mozgásnál.*

**Beilleszthető szöveg:**
Az átlós mozgás engedélyezése mellett az algoritmus nem léphet át két akadály közös sarkán. A szomszédvizsgálat a két köztes oldalsó cellát is ellenőrzi, ezért a megtalált útvonal szabályos kerülőutat használ.

### 7.4. Megoldhatatlan pálya

**Kép:** `heuristics_diagonal_only.png`

**Képaláírás:** *Megoldhatatlan rácspálya felismerése két mozgási módban.*

**Beilleszthető szöveg:**
A kereszt alakú akadályrendszer elzárja a kezdő- és a célcellát. Egyik heurisztika sem tud szabályos útvonalat létrehozni, ezért az algoritmus mindkét mozgási módban helyesen jelzi a `NO PATH` eredményt. Ez megerősíti, hogy a heurisztika a keresés sorrendjét befolyásolja, az akadály- és szomszédsági szabályokat nem írja felül.
## 7. K?tpaneles, szimul?ci?s st?lus? ?sszehasonl?t? ?bra

Az aktu?lis k?p az eredeti `python -m codes_diploma.simulation` t?rk?prajzol?si
st?lus?hoz igazodik. A t?rk?p k?t egym?s melletti panelen l?that?: balra a
n?gyir?ny?, jobbra az ?tl?s mozg?st is enged?lyez? A* keres?s eredm?nye. Mindk?t
panelen egyszerre szerepel a Manhattan, Euklideszi, Chebyshev ?s Octile
heurisztika. Az akad?lyok sz?rk?s t?glalapok, a cellahat?rok finom r?csvonalak,
az ?tvonal pedig v?kony, szaggatott vonal apr? csom?ponti jel?l?sekkel. Ez a
jel?l?s k?zelebb ?ll a szimul?ci? eredeti A* ?tvonal-megjelen?t?s?hez, ?s nem
takarja el az akad?lyokat vagy a t?bbi ?tvonalat.

**K?p:** `heuristics_original_simulation.png`

**K?pal??r?s:** *A n?gy A* heurisztika ?sszehasonl?t?sa az eredeti szimul?ci?s
t?rk?pen: balra a n?gyir?ny?, jobbra az ?tl?s mozg?st is enged?lyez? eset.*

**Beilleszthet? sz?veg:**
Az ?bra az eredeti szimul?ci? t?rk?pelrendez?s?t ?s megjelen?t?si logik?j?t
k?veti. A bal oldali panelen csak a n?gy f?ir?ny, a jobb oldali panelen pedig
az ?tl?s szomsz?dcell?k is haszn?lhat?k. Az ?tvonalakat a sz?nek k?l?n?tik el,
a v?kony szaggatott vonal ?s az apr? csom?ponti jel?l?s pedig az A* r?cs?tvonal
alakj?t mutatja. A vil?gkoordin?t?s tengelyek miatt az ?bra a szimul?ci?ban
l?that? t?rk?phez hasonl?an ?rtelmezhet?.


## 8. Val?di szimul?ci?s t?rk?pen v?gzett heurisztika-?sszehasonl?t?s

A `simulation_heuristic_comparison.py` k?l?n ?sszehasonl?t? ?br?t k?sz?t az
alap szimul?ci? t?rk?p?p?t?s?t felhaszn?lva. A `simulation.create_scene()`
hozza l?tre a 30?20 cell?s t?rk?pet, majd az `inflation_radius=0.1` param?terrel
a `GridMap.inflate_obstacles()` biztons?gi z?n?val kib?v?ti az akad?lyokat. Ez
fontos k?l?nbs?g a puszt?n nyers akad?lycell?kat rajzol? k?s?rleti ?br?khoz
k?pest: az ?tvonaltervez?s a robot k?r?li tiltott r?hagy?st is figyelembe veszi.

A program mind a n?gy heurisztik?hoz l?trehozza az `AStarDWAPlanner` p?ld?ny?t,
majd a `plan_global()` f?ggv?nyt futtatja egyszer n?gyir?ny? ?s egyszer ?tl?s
mozg?ssal. Az ?gy kapott, nem sim?tott A* glob?lis ?tvonalakat egy k?z?s, k?t paneles ?br?n jelen?ti meg. A bal panel a n?gyir?ny?, a jobb panel az ?tl?s mozg?s eredm?nye; mindk?t panelen egyszerre l?that? mind a n?gy heurisztika. Az akad?lyok ?s a biztons?gi z?na v?ltozatlanul az alap szimul?ci?b?l sz?rmaznak, a heurisztik?kat pedig csak elt?r? sz?nek k?l?nb?ztetik meg. A panelenk?nti jelmagyar?zat az ?tvonal-k?lts?get jel?li.

**Kimeneti k?p:** `astar_project/results/figures/simulation_heuristic_comparison.png`

**?jragener?l?s:**

```text
python -m codes_diploma.astar_project.generate_simulation_heuristic_comparison
```

A friss?tett v?ltozatban a n?gy heurisztika kontrasztos sz?neket kapott. A t?rk?p ?s az ?tvonalak geometri?ja nem v?ltozott, ?gy a megjelen?t?s csak az elk?l?n?thet?s?get jav?tja.

Ez az ?bra a megl?v? `heuristics_original_simulation.png` k?pet nem ?rja fel?l;
a k?t k?p elt?r? c?lt szolg?l. A megl?v? k?p a kor?bbi vizu?lis ?sszehasonl?t?
st?lust ?rzi meg, az ?j k?p viszont az alap szimul?ci? t?nyleges, infl?lt
GridMap-j?re ?s A*+DWA ?tvonaltervez?j?re ?p?l.
## 6. Ind?t?s ?s tesztel?s

Az ?sszehasonl?t?s ind?t?sa:

```text
python -m codes_diploma.astar_project.run_experiment
```

A c?lzott tesztek:

```text
python -m unittest codes_diploma.astar_project.tests.test_experiments codes_diploma.astar_project.tests.test_astar_baseline codes_diploma.astar_project.tests.test_grid_map -v
```

A k?s?rleti tesztek ellen?rzik a n?gy heurisztika ?s a k?t mozg?si m?d lefut?s?t, a sarokv?g?s tilt?s?t ?s a megoldhatatlan p?lya kezel?s?t.

## 7. A `simulation_heuristic_comparison.png` ?bra le?r?sa

**K?p:** `astar_project/results/figures/simulation_heuristic_comparison.png`

**K?pal??r?s:** *A n?gy A* heurisztika ?sszehasonl?t?sa az eredeti, akad?lyinfl?ci?val kib?v?tett szimul?ci?s t?rk?pen: balra a n?gyir?ny?, jobbra az ?tl?s mozg?s.*

**Beilleszthet? sz?veg:**

Az ?bra az alap szimul?ci? `create_scene()` f?ggv?ny?vel l?trehozott, 30?20 cell?s t?rk?pet haszn?lja. A t?rk?p akad?lyai az `inflation_radius=0.1` param?terrel vannak kib?v?tve, ez?rt a sz?rke akad?lyter?let a robot sz?m?ra fenntartott biztons?gi z?n?t is tartalmazza.

A bal oldali panelen az A* csak fel, le, balra ?s jobbra l?phet. A jobb oldali panelen az ?tl?s szomsz?dcella is enged?lyezett. Mindk?t panelen ugyanaz a n?gy heurisztika fut le az `AStarDWAPlanner.plan_global()` f?ggv?nyen kereszt?l, sim?t?s n?lk?l. A k?t panel ugyanazon szimul?ci?s t?rk?pen hasonl?tja ?ssze a mozg?si szab?lyokat.

A heurisztik?k sz?nei:

- Manhattan: k?k;
- Euklideszi: narancss?rga;
- Chebyshev: z?ld;
- Octile: magenta.

A panelenk?nti jelmagyar?zat az adott ?tvonal k?lts?g?t mutatja. A geometriai ?tvonalak a t?nyleges, infl?lt `GridMap`-b?l sz?rmaznak; a sz?nek csak az ?tvonalak vizu?lis elk?l?n?t?s?t szolg?lj?k.

**?jragener?l?s:**

```text
python -m codes_diploma.astar_project.generate_simulation_heuristic_comparison
```

A kor?bbi `heuristics_original_simulation.png` k?pet meghagytam, de a szakdolgozati le?r?s ehhez az ?j, biztons?gi z?n?t is tartalmaz? `simulation_heuristic_comparison.png` k?phez tartozik.
## 8. ROS 2 A* + DWA akadályinfláció és útvonalhiba

Az `astar_dwa_node.cpp` az odometriából, a célból és a statikus akadályokból
A* rácstérképet készít, majd a DWA-val sebességet küld a `/cmd_vel` témára.
A mostani javítás az akadályinflációt érinti: a korábbi négyzetes tiltás
lezárhatta a fizikailag átjárható réseket.

A paraméterek szerint a rács felbontása `resolution=0.20 m`, a robot sugara
`robot_radius=0.28 m`. Egy 0,35 m sugarú akadálynál a biztonsági sugár:

```text
0,35 m + 0,28 m = 0,63 m
```

Az új kód a cellaközéppont és az akadályközéppont euklideszi távolságát méri:

```text
d = sqrt((x_c - x_o)^2 + (y_c - y_o)^2)
```

ahol `x_c,y_c` a cellaközéppont, `x_o,y_o` az akadály középpontja méterben.
Csak a `d <= 0,63 m` feltételnek megfelelő cellák lesznek blokkoltak.
Korábban a teljes négyzetes rácsblokk tiltott volt, így két akadály között
összeérhettek a biztonsági zónák.

Például 1,80 m középponttávolság és két 0,63 m-es biztonsági sugár esetén:

```text
1,80 m - 2 * 0,63 m = 0,54 m
```

marad geometriai szabad távolság. A kör alakú infláció ezért kevésbé
konzervatív, miközben a robot sugarát továbbra is figyelembe veszi.

Ha a kezdő- vagy célcella kívül esik a térképen, vagy blokkolt, a node most
diagnosztikai figyelmeztetést ír ki a `start=(row,column)`, `goal=(row,column)`,
`start_blocked` és `goal_blocked` értékekkel. Ez megmutatja, hogy érvénytelen
cella vagy ténylegesen megszakadt A* kapcsolat okozza-e az üres útvonalat.

A DWA külön réteg: az A* útvonal megtalálása után a LiDAR-pontok alapján még
megállíthatja a robotot, ha minden kipróbált sebességpálya ütközne. A javítás
az A* statikus térképét teszi pontosabbá, a lokális LiDAR-viselkedést nem
rejti el.

Ellenőrzés:

```bash
colcon build --symlink-install --packages-select astar_dwa_controller
```

Ezután az `/astar_path`, `/astar_map` és `/astar_dwa_markers` témákon lehet
ellenőrizni, hogy a két akadály közötti útvonal létrejön-e.
## 9. A ROS 2 A* + DWA tesztelési vizualizációja és sebességkorlátja

Az `astar_dwa_node.cpp` vezérlője két külön feladatot végez. Az A* a statikus
akadályokból útvonalat készít, a DWA pedig a LiDAR alapján kiválasztja a
következő sebességpárt. A tesztelés áttekinthetőbb lett az RViz
`/astar_dwa_markers` témáján:

- zöld vonal: A* útvonal;
- kék vonal: az aktuálisan kiválasztott DWA-előrejelzés;
- piros hengerek: ismert statikus akadályok;
- halványsárga lapok: statikus akadály plusz robot-sugár biztonsági zónája;
- sárga pontok: a LiDAR által éppen érzékelt akadálypontok;
- kék áttetsző henger és nyíl: robotpozíció és haladási irány.

A maximális lineáris sebesség most paraméterezett. A `rosbot.yaml`
`max_linear_velocity=0.32 m/s` értéke azt jelenti, hogy a kiadott
`Twist.linear.x` nem lehet nagyobb 0,32 m/s-nél. A korábbi kód ezt 0,20 m/s-ra
korlátozta, miközben a DWA 0,40 m/s-ig vizsgált sebességeket. A
`max_angular_velocity=1.00 rad/s` az elfordulási sebesség felső határa.

A vezérlő ciklusa 0,10 s. Az új lineáris gyorsítási lépés legfeljebb 0,08 m/s
ciklusonként, vagyis ideális esetben:

```text
0,32 m/s / 0,08 m/s = 4 ciklus
4 * 0,10 s = 0,40 s
```

alatt éri el a maximális értéket. Ez nem gyorsítja fel a veszélyes helyzeteket:
az ütközésvizsgálat minden DWA-jelölt pályán továbbra is lefut.

Az RViz-es vizsgálat menete:

1. `/astar_path`: van-e globális útvonal;
2. `/astar_map`: a statikus biztonsági zónák helye;
3. sárga LiDAR-pontok: lát-e a robot váratlan akadályt;
4. kék DWA-vonal: a lokális vezérlő merre tervezi a következő 1,5 másodpercet.

Ha zöld útvonal van, de a kék vonal rövid vagy a robot áll, akkor a DWA
LiDAR-biztonsági ellenőrzése állította meg. Ha zöld útvonal sincs, akkor az
A* statikus térképét vagy a célt kell ellenőrizni.

## 10. A Gazebo mozgó akadály működése és javítása

### A fájlok célja

A mozgó akadály működését három fájl együtt adja:

- `worlds/dwa_world.sdf`: a `moving_obstacle` Gazebo-modellje;
- `dwa_gazebo_sim/moving_obstacle_node.py`: a modell új pozícióját számítja;
- `launch/bridge_and_controller.launch.py`: ROS 2 service bridge-et indít a
  Gazebo `/world/dwa_world/set_pose` szolgáltatásához.

### Adatfolyam

Az akadály kezdeti világkoordinátája `(x, y, z) = (3.0, 1.8, 0.45) m`.
A `moving_obstacle_node` 0,05 másodpercenként frissítési ciklust futtat. A
pozíció y-koordinátája:

```text
y(t) = 1,8 + 1,2 * sin(0,6 * t) m
```

Itt `t` a node által követett idő másodpercben, a `1,8 m` a középvonal, a
`1,2 m` a kitérés amplitúdója, a `0,6 1/s` pedig a szögsebesség jellegű
szorzó. Például `t = 0 s` esetén:

```text
y(0) = 1,8 + 1,2 * sin(0) = 1,8 m
```

`t = 2 s` esetén `0,6 * 2 = 1,2`, ezért
`y(2) ≈ 1,8 + 1,2 * 0,932 ≈ 2,92 m`. Az x-koordináta végig `3,0 m`,
tehát az akadály függőleges irányban mozog.

### Mi akadályozta a mozgást?

Korábban a world fájlban ez szerepelt:

```xml
<static>true</static>
```

Ez azt jelentette, hogy a Gazebo a modellt statikus objektumként kezelte.
Ezt `<static>false</static>` értékre módosítottam. Ezen kívül a node ugyan
meghívta a service klienst, de a launch fájl nem bridge-elte a
`SetEntityPose` szolgáltatást. Most ez is bekerült:

```text
/world/dwa_world/set_pose@ros_gz_interfaces/srv/SetEntityPose
```

Ez a kapcsolat továbbítja a ROS 2 service-kérést a Gazebo transport felé.

### A node biztonságos frissítése

A node a `request_in_flight` állapottal biztosítja, hogy ne küldjön új
pozíciókérést addig, amíg az előző válasz meg nem érkezett. Így a 20 Hz-es
timer nem halmozza fel a Gazebo service-kéréseket. A válasz `success` mezőjét
ellenőrzi, és sikertelen frissítésnél figyelmeztetést ír a ROS 2 naplóba.

### Ellenőrzés

A módosítás után lefutott:

```bash
colcon build --symlink-install --packages-select dwa_gazebo_sim
python3 -m py_compile moving_obstacle_node.py
```

A futási ellenőrzés során a Gazebo pose-adatában a `moving_obstacle` y-értéke
változott, például `2,8703 m`, majd `2,8536 m`, később `2,8359 m` lett. Ez
igazolja, hogy az akadály már nem csak a node-ban számolja a pályát, hanem a
Gazebo-modell tényleges pozíciója is frissül.

## 11. A mozgó akadály kezelése az A* + DWA C++ vezérlőben

### A fájl célja

Az `astar_dwa_node.cpp` a ROS 2 vezérlőben két külön feladatot kapcsol össze:
az A* egy rövid, globális útvonalat keres, a DWA pedig a következő útvonalpont
felé választ sebességet. A korábbi működésben az A* csak a YAML-ben megadott
statikus akadályokat használta. A mozgó akadályt ugyan látta a LiDAR, de az A*
útvonala nem változott, ezért az útvonal a dinamikus akadályon keresztül is
vezethetett.

### Adatfolyam és módosítás

A vezérlési ciklus az `obstacles()` függvénnyel a `/scan` LaserScan mérési
pontjait világkoordinátára alakítja, és csak a robot előtti, legfeljebb 3,0 m-es
tartományt tartja meg. Az aktuális LiDAR-akadályokat a lokális DWA használja; a globális A* rács
továbbra is a statikus akadálymodellt használja, a Python-szimulátor logikájával
összhangban.

### Fontos függvények

- `obstacles()`: a LiDAR-pontokat szűri és `Obstacle{x, y, radius}` adatokká
  alakítja;
- `astar(const std::vector<Obstacle>& sensed_obstacles, bool use_sensed)`:
    a `control()` jelenleg `astar({}, false)` formában hívja, tehát csak a
    statikus térképből építi a rácsot; a LiDAR-listát a lokális DWA kezeli;
- `dwa(target_x, target_y, target_index, sensed)`: előrehaladó és helyben
    forduló keréksebességpárokat vizsgál, a negatív lineáris sebességet kizárja;
    az elfogadott jelölteket útvonalközelséggel is pontozza;
- `control()`: egy ciklusban egyszer gyűjti a LiDAR-akadályokat, újratervez,
  kiválasztja a waypointot, majd publikálja a `/cmd_vel` üzenetet.

### DWA biztonsági változás

A DWA előremenő és helyben forduló jelölteket vizsgál, `0.1 s` lépéssel,
a helyi cél távolságától függő `0.8...2.5 s` időtávon. A LiDAR-pontok sugara
`0 m`; a robot sugara `0.22 m`, a statikus tartalék `0.03 m`, a mozgó
akadályoké `0.08 m`. Például álló ponttól `0.36 m` távolságban a szabad tér
`0.36 - (0.22 + 0.03 + 0) = 0.11 m`: először a test és a tartalék együttes
sugarát számoljuk ki, majd ezt levonjuk a középpontok távolságából. Ebben a
példában nincs ütközés. Mozgó pontnál ugyanott `0.06 m` maradna.

Az ütközésjelzés a kezdeti szabad távolsághoz is viszonyít, így a már
biztonsági margón belül lévő robot nem minden mozdulatát tiltja le. Az
elfogadást ezután a fékezhetőség és a `min_ttc` feltétel dönti el. Ha nincs
elfogadott minta, a DWA nulla lineáris sebességgel az akadálytól elfelé fordul;
a forgásirányt a `recovery_dir_` őrzi. Ez nem tolatás és nem célirányú forgás.

### Miért oldja meg az elakadást?

Ha a mozgó akadály a globális A* útvonalra kerül, a DWA a lokális
előrejelzésben kerüli ki vagy fékezi le. A LiDAR minden mérési pontját nem
szabad külön A* akadályként inflálni, mert egy fizikai akadály sok sűrű pontot
ad, és a cellák körüli zónák tévesen teljes átjárókat zárhatnak le.

### Ellenőrzés

A csomag ROS2-környezetben ellenőrizhető az alábbi paranccsal:

```bash
source /opt/ros/jazzy/setup.bash
cd ros2_astar_dwa_gazebo
colcon build --packages-select astar_dwa_controller --symlink-install
```

A korábbi build eredménye nem igazolja az új pontozás Gazebo-beli működését.
Az RViz-ben az `/astar_path`, a sárga LiDAR-pontok
és a kék DWA-trajektória együttesét kell figyelni. Ha a robot mégsem halad,
a vezérlő naplójában az `Az A* nem talált elérhető útvonalat` üzenet
különválasztja a valódi útvonalhiányt a DWA biztonsági megállásától.

## 12. A ROS/Gazebo térkép és a Python-szimulátor összehangolása

A ROS/Gazebo változat most a Python `simulation.py` alapértelmezett térképét
használja referenciaként. A rács 30 oszlopból és 20 sorból áll, a
`resolution=0,2 m`, ezért a tervezési terület 6,0 m széles és 4,0 m magas.
A rács origója `(0,0) m`, így a `(2,2)` kezdőcella középpontja:

```text
x = (2 + 0,5) * 0,2 = 0,5 m
y = (2 + 0,5) * 0,2 = 0,5 m
```

A `(17,27)` célcella középpontja ugyanígy `(5,5; 3,5) m`. A függőleges
akadálysor a 10. oszlopban, a 7-12. sorok között nyitott réssel, a vízszintes
akadálysor pedig a 12. sorban, a 19-24. oszlopok közötti nyitott réssel
szerepel. A Gazebo SDF-ben ezek összefüggő, 0,2 m vastag falszakaszokként
jelennek meg; ez a cellák fizikai megfelelője.

### A két mozgó akadály

A Python-szimulátorban szereplő akadályok ROS oldali kezdőpozíciója és
sebessége:

```text
moving_obstacle_1: (2,4; 0,4) m + (0; 0,20) m/s * t
moving_obstacle_2: (6,8; 2,1) m + (-0,25; 0) m/s * t
```

Például 5 másodpercnél az első akadály helye
`(2,4; 1,4) m`, a másodiké pedig `(5,55; 2,1) m`. A
`moving_obstacle_node.py` ezeket a pozíciókat a
`/world/dwa_world/set_pose` szolgáltatáson keresztül adja át a Gazebónak.
Egyszerre csak egy service-kérés van függőben, ezért az akadályfrissítés nem
halmozódik fel.

### A DWA működési egyezése

Az `astar_dwa_node.cpp` DWA-része a Python `robotconfig` fő paramétereit
használja: keréksugár `0,033 m`, keréktávolság `0,08 m`, maximális
keréksebesség `15 rad/s`, keréksebesség-lépés `1 rad/s`, gyorsulási korlát
`2 m/s²`, `dt=0,1 s`, előrejelzési idő `3 s`, biztonsági ráhagyás `0,15 m`,
valamint `Alfa=5`, `Beta=2`, `Gamma=3`.

Egy bal és jobb keréksebességből a Python- és ROS-kód azonos módon számolja:

```text
v = ((w_L + w_R) / 2) * r
w = ((w_R - w_L) / (2 * b)) * r
```

Például `w_L=w_R=10 rad/s` esetén `v=0,33 m/s`, `w=0 rad/s`, tehát a robot
egyenesen halad. A ROS DWA a dinamikus ablakban ezeket a keréksebességeket
vizsgálja, a pályát 0,1 s-os lépésekben integrálja, és az ütközésig mért
távolság alapján alkalmazza a Python-féle megállíthatósági feltételt:

```text
|v| <= sqrt(2 * a_max * distance_to_obstacle)
```

Ez a dokumentáció és az `ASTAR_PROJEKT_FOLYAMATBRA.gv` az új,
keréksebesség-alapú ROS DWA-hívási sorrendet tükrözi.

---

# `astar_dwa_node.cpp` – ROS odometria, cél és A* útvonal ellenőrzése

## 1. A fájl célja

Az `astar_dwa_node.cpp` a ROS 2 és Gazebo közötti vezérlőcsomópont. Az
`/odom` és `/scan` adataiból felépíti a robot aktuális állapotát és a
pillanatnyi akadályképet, az RViz `/goal_pose` üzenetéből célt vesz át, majd
A*-útvonalat és DWA-sebességet publikál `/astar_path` és `/cmd_vel` témákon.

## 2. Odometriai kezdőeltolás

A TurtleBot Gazebo odometria-pluginja a robot spawnhelyéhez képest lokális
koordinátát ad vissza, miközben a modell `(0.8, 0.8)` méteren spawnol. Ezért a
konfigurációban `initial_pose_x = 0.8 m` és `initial_pose_y = 0.8 m`. Az `odom()`
ezt a világkoordinátára állító offsetet adja hozzá:

```cpp
pose_.x = msg->pose.pose.position.x + initial_pose_x_;
pose_.y = msg->pose.pose.position.y + initial_pose_y_;
```

A Gazebo-odom `(0, 0)` mérés így a tervezőben `(0.8, 0.8)` világpozícióvá
válik. `resolution = 0.2 m/cella` mellett ez:

```text
column = floor(0.8 / 0.2) = 4
row    = floor(0.8 / 0.2) = 4
```

tehát a Python-szimulátor kezdőcellája `(4, 4)`, nem egy kétszeresen eltolt
pozíció.

## 3. Cél- és útvonal-adatfolyam

Az RViz `2D Goal Pose` eszköze `geometry_msgs/msg/PoseStamped` üzenetet küld
`/goal_pose` témán. A node a világkoordinátás `x` és `y` értéket eltárolja,
majd a vezérlési ciklusban a jelenlegi pozícióból és a célból cellát készít.
Az A* eredménye `nav_msgs/msg/Path` formában jelenik meg `/astar_path`-on;
az útvonal pontjai az `odom` frame-ben, 0,2 méteres cellaközéppontokként
szerepelnek. A következő waypointot a DWA lokális vezérlése követi, amely a
`/cmd_vel` Twist üzenetet publikálja.

## 4. Biztonsági feltételek

Odometria nélkül a vezérlő nem tervez. Érvénytelen vagy foglalt kezdő- illetve
célcella esetén az A* figyelmeztetést ír, üres útvonalat publikál és nulla
sebességgel állítja meg a robotot. Ezért a `/astar_path` topic megléte önmagában
nem elég: az üzenet `poses` tömbjének is tartalmaznia kell útvonalpontokat.

## 5. Ellenőrzött futás

A javítás ellenőrzéséhez a következő parancs futott:

```bash
colcon build --packages-select astar_dwa_controller --symlink-install
```

A build sikeres volt. Tiszta Gazebo- és bridge-indítás után a `/goal_pose`
cél `(5.50, 3.50)` értékkel érkezett meg, a node `ut=27 pont` útvonalat írt
a naplóba, és az `/astar_path` üzenet 27, a célhoz vezető pontot tartalmazott.

---

# Pályahatár-védelem és a Gazebo-pálya nagyítása

A korábbi `6,0 m x 4,0 m` térkép csak az A* cellakeresésének határa volt. A DWA
előrejelzése azonban kizárólag a LiDAR által érzékelt akadályokat vizsgálta,
ezért a pálya szélén nem volt olyan feltétel, amely a sebességjelöltet
elutasította volna. A Gazebo-világban sem volt fizikai határfal.

Az aktuális pálya `8,0 m x 5,0 m`, `0,2 m/cella` felbontással, vagyis
`40 x 25` cellás. A robot kezdőpontja `(0,8 m, 0,8 m)`, amelynek cellája:

```text
column = floor(0.8 / 0.2) = 4
row    = floor(0.8 / 0.2) = 4
```

A DWA most minden előrejelzett pontnál ellenőrzi a
`robot_radius + safety_margin = 0,28 + 0,15 = 0,43 m` biztonsági sávot.
Ez azt jelenti, hogy a robot középpontja nem közelítheti meg a pálya szélét
`0,43 m`-nél jobban. Például az alsó határnál a megengedett tartomány kezdete
`y = 0,43 m`; az ennél kisebb `y` értéket eredményező DWA-jelöltet a node
veszélyesnek jelöli és nem választja ki.

A világfájl négy statikus falat is tartalmaz a `0..8 m` és `0..5 m` terület
körül. Így a vizuális pálya és a tervező rácsa ugyanazt a koordinátatartományt
használja. Ha a robot már a biztonsági határon kívül van, a vezérlő nulla
`/cmd_vel` értéket küld, és figyelmeztetést ír a naplóba.

A ROS- és Python-DWA közötti fontos különbség, hogy a ROS-vezérlő a
keréksebesség-jelöltekből számított `v` és `w` értékeket publikálja. Ha a
jelölt túllépi a publikált sebességhatárt, a korábbi kód csak a végső Twist
üzenetet vágta le. Például egy `w = 1,86 rad/s` jelöltből `1,0 rad/s` került
ki a topicra, miközben a belső kerékállapot továbbra is az `1,86` értékű
jelöltet követte. Ez eltérést okozott a tervezett és a tényleges mozgás között.
Az aktuális kód már a DWA pontozása előtt elutasítja azokat a jelölteket,
amelyek `v > 0,32 m/s` vagy `|w| > 1,0 rad/s` értéket adnak.

Ha a LiDAR-biztonsági feltétel, a pályahatár vagy a sebességkorlát miatt egyetlen
előremeneti jelölt sem marad, a node ezt külön kezeli. A korábbi keréksebesség
helyett lenullázza a kerékállapotot, és a cél irányába legfeljebb
`1,0 rad/s` helyben forgást ad vissza. Így a robot nem marad csendben nulla
sebességen egy régi vagy érvénytelen DWA-állapot miatt.

---

# Iránybaállítás a körkörös mozgás elkerülésére

A vezérlő a következő waypoint és a robot aktuális `pose_.yaw` értéke alapján
irányhibát számol:

```text
heading_error = wrap(atan2(target_y - pose_y, target_x - pose_x) - yaw)
```

Az `atan2` a cél felé mutató szöget adja radiánban, a `yaw` a robot jelenlegi
irányultsága, a `wrap` pedig `[-pi, pi]` tartományba hozza a különbséget.
Például ha a célirány `1,2 rad`, a robot iránya `-0,2 rad`, akkor a hiba
`1,4 rad`, ezért a robot először helyben fordul, nem pedig előremenetben
köröz.

Az aktuális vezérlőben nincs külön `0,6 rad` feletti teljes megállási ág. A
heading-score, az akadálypredikció és a fékezhetőségi feltétel együtt dönti el,
hogy a DWA helyben forduljon, vagy lassú íves előremenetet válasszon. Ez azért
fontos a rés előtt, mert a korábbi külön ág minden nagyobb irányhibánál
`linear.x=0` értéket küldött, és a robot megtorpanhatott. A módosított logban
például `cmd=(0.15, 0.62)`, majd `cmd=(0.32, 0.21)` látható, ami előremeneti
befordulást jelent.

## 13. C++ DWA frissítés a Python referencia alapján

Az aktuális `dwa()` trajektória közben kumulálja az ívhosszt. Ha a pálya később
ér akadályt, a jelölt nem esik ki automatikusan: a `collision_dist` adja az
ütközésig megtett úthosszt méterben. A fékezhetőségi ellenőrzésben a sebesség
nem haladhatja meg a kétszeres gyorsulás és az úthossz szorzatának négyzetgyökét.
Például `2 m/s²` lassulásnál, `0.01 m` úthosszból a sebességhatár
`sqrt(2 * 2 * 0.01) = 0.2 m/s`. A `0.26 m/s` jelölt ekkor kiesik.
A külön `min_ttc` vizsgálat az ütközésig szükséges minimális időt ellenőrzi.

Az adaptív időtáv `clamp(goal_dist * 2.0, 0.8, predict_time_)`: a helyi
célpont méterben mért távolságát egy `2 s/m` tényező szorozza, majd a kód
`0.8 s` és a konfigurált `2.5 s` közé szorítja. `0.3 m` céltávolságnál
`0.6 s` adódna, ezért `0.8 s` lesz az időtáv. A sebességpont célsebességhez
viszonyít, az új útvonalközelségi tag ettől különálló büntetés.

Az A* akadályinflációjában a robot sugara, az akadály sugara és a
`planning_margin` szerepel. A `control()` alapértéken `0.25 m` ívhosszú
előretekintést használ; a diszkrét pontok miatt a kiválasztott waypoint ennél
távolabb is lehet. A `line_free()` a statikus akadályokon átvezető közvetlen
célpontot visszalépteti. A jelenlegi `obstacles()` a statikus falpontokat is
megtartja a DWA számára; a fal közelsége a sebességbecslést tiltja, nem a
pontok ütközésvizsgálatát.

Ellenőrzés:

```text
colcon build --packages-select astar_dwa_controller dwa_gazebo_sim --symlink-install
```

## 14. Visszatérés az A* útvonalra akadálykerülés után

### A vezérlő célja és a hiba oka

Az `astar_dwa_node.cpp` továbbra is a ROS2-integráció vezérlője. A módosítás a
lokális DWA pontozását érinti, nem az A* keresést és nem a Python-szimulátort.
A korábbi célirány-pont azt mérte, hogy az előrejelzés végén a robot orra
mennyire néz a helyi cél felé. Nem mérte külön, milyen messze marad az eredeti
útvonaltól, vagy ténylegesen közelebb kerül-e a célponthoz. Az akadálytávolság
és a sebesség jutalma ezért előnyben részesíthetett egy oldalra eltolt ívet.
Ez kódszinten igazolható hiányosság; a konkrét Gazebo-futás teljes ok-okozati
bizonyításához új szimulációs próba szükséges.

### Adatfolyam, függvények és adatok

A `control()` a `current_path_` világkoordinátás pontpárlistát követi. A
`waypoint_index_` csak előre halad: nyolc ponton belül a legközelebbi látható
waypointot keresi. Ezután az útvonal ívhosszán választ előretekintési célpontot,
és a `line_free()` segítségével ellenőrzi annak statikus láthatóságát.

A hívás most `dwa(target_x, target_y, target_index, sensed)`: az első két
paraméter a cél méterben megadott világkoordinátája, a harmadik az útvonalon
elfoglalt indexe, a negyedik az aktuális LiDAR-akadálylista. Visszatérése a
lineáris és szögsebesség párja, `m/s` és `rad/s` egységben. A jelöltek
dinamikus ablakát, gyorsuláskorlátját, fékezhetőségét és ütközési idővizsgálatát
a módosítás nem változtatja meg.

Az elfogadott rollout `(x, y)` végpontjára a `path_tracking::tracking_cost()`
büntetést számol. A vizsgált útvonaldarab a jelenlegi waypoint előtti ponttól
az előretekintési célpont utáni pontig tart, az útvonal határaihoz igazítva.
Így nem egy tetszőleges, későbbi útvonalág közelsége ad jutalmat, és a kerülés
utáni eltolás nem válik új referencia-egyenessé.

### Pontozás és számpélda

```text
score = alpha * heading_score + beta * clear_score + gamma * vel_score
    - path_distance_bias * path_distance
    - goal_distance_bias * target_distance
```

A `score` dimenzió nélküli összehasonlító érték, a nagyobb a jobb. A
`heading_score` a rollout végén a célirány és a robot iránya közötti abszolút
szöghibát vonja le a pi értékéből, majd pi-vel oszt; egysége nincs. A
`clear_score` a legkisebb megmaradt biztonsági távolságot `1 m`-hez viszonyítja
és 0 és 1 közé szorítja. A `vel_score` a jelölt sebesség és a célsebesség
abszolút különbségét osztja a maximális lineáris sebességgel, majd ezt kivonja
egyből. Az `alpha=5`, `beta=2`, `gamma=3` dimenzió nélküli súlyok.

A `path_distance` a végpont és a helyi A* vonallánc legkisebb távolsága
méterben. A `target_distance` a végpont és a helyi cél távolsága méterben.
A két új paraméter `path_distance_bias=6.0` és `goal_distance_bias=2.0`,
pontszám/méter értelmű súly. Először a három jutalmat összeadjuk, majd az
útvonaltól és a céltól mért súlyozott távolságokat levonjuk.

Konkrét példa: az útvonal az x tengelyen fut, a helyi cél `(1.0, 0.0) m`.
Egy párhuzamos jelölt végpontja `(0.8, 0.4) m`: az útvonalhibája `0.4 m`,
célhibája `sqrt(0.2² + 0.4²) = 0.4472 m`. Büntetése
`6 * 0.4 + 2 * 0.4472 = 3.2944` pont. Egy visszatérő jelölt vége
`(0.75, 0.1) m`: a két távolság `0.1 m` és `sqrt(0.25² + 0.1²) = 0.2693 m`,
ezért büntetése `6 * 0.1 + 2 * 0.2693 = 1.1385` pont.

Ha a párhuzamos jelölt három részpontja `(0.95, 0.8, 1.0)`, a visszatérőé
`(0.9, 0.6, 1.0)`, a régi jutalmuk `9.35`, illetve `8.70` pont. A régi
pontozás a párhuzamosat választaná. Az új értékek `6.0556` és `7.5615` pont:
ugyanilyen feltételek mellett a visszatérő jelölt nyer. Ezek tesztbemenetek,
nem Gazebo-ból mért trajektóriák.

### Biztonsági korlátok és megfigyelés

Az útvonalközelség puha büntetés, nem tiltott folyosó: az akadálykerüléshez
szükséges eltérés továbbra is lehetséges. Az új tag csak a meglévő biztonsági
vizsgálatokon átjutott jelöltek sorrendjét változtatja. Ez nem jelent új,
szigorú ütközésmentességi garanciát, hiszen a jelenlegi DWA a későbbi ütközést
a fékezhetőség alapján is elfogadhatja. Túl nagy útvonalsúly szűk helyen
ronthatja a kerülést, ezért a súlyokat csak méréssel érdemes tovább emelni.

A `Vezerles` napló új `utvonal_elteres` mezője az aktuális robotpozíció
távolsága a vizsgált útvonaldarabtól, méterben. Ez az érték a normál DWA-ágon
jelenik meg, nem a külön helyben forgató vagy megállító ágakon. Kerülés közben
nőhet, utána viszont az útvonalra visszatérő robotnál csökkennie kell.
Üres útvonalnál a `control()` megállítja a robotot, nem hívja a DWA-t.

### Kapcsolat és tesztelés

A hívási lánc: `control()` -> `dwa()` -> `path_tracking::tracking_cost()` ->
`path_tracking::distance_to_path()` -> legjobb jelölt -> `/cmd_vel`.
Az ábra ROS2-blokkja ugyanezt mutatja. A YAML tárolja az új súlyokat;
a node az indulásakor olvassa be őket, ezért módosítás után újra kell indítani.
Mindkét súly nullázásával az új büntetés kikapcsolható összehasonlító futáshoz.

ROS2-környezetben, a `ros2_astar_dwa_gazebo` könyvtárból:

```bash
colcon build --packages-select astar_dwa_controller --symlink-install --cmake-args -DBUILD_TESTING=ON
colcon test --packages-select astar_dwa_controller --event-handlers console_direct+
colcon test-result --verbose
```

A teljes node fordítása és a Gazebo/RViz célbaérési próba ebben a
Windows-munkamenetben nem igazolható: ROS2 és telepített WSL nem érhető el.
A regressziós teszt a geometriai függvényeket és a pontozási példákat méri,
nem a teljes robot zárt hurkú mozgását.

A helyi hordozható C++ fordítóval megkísérelt ellenőrzésből nem született
sikeres tesztfutási eredmény. A felhasználó kérésére további teszt nem fut;
a ROS2-fordítást, a regressziós tesztet és a Gazebo-próbát ő végzi el.

## 15. Útvonaltávolság számítása: path_tracking.hpp

### Cél, bemenet és kimenet

A `ros2_astar_dwa_gazebo/src/astar_dwa_controller/src/path_tracking.hpp`
ROS2-től független C++17 segédfájl. A `Path` a világkoordinátás `(x, y)`
pontpárok vektora. A `distance_to_path(path, first, last, x, y)` a megadott,
inkluzív indextartomány vonalláncától mért legkisebb távolságot adja méterben.
A `tracking_cost(path, first, last, x, y, target_x, target_y,
path_distance_bias, goal_distance_bias)` a két súlyozott távolság összegét adja,
amelyet a DWA levon a jutalompontszámból. A paraméterek a 14. fejezetben
bemutatott rollout-végpontot, helyi célt és súlyokat jelentik.

### Szakaszra vetítés hétköznapi példával

Nemcsak a waypointok távolságát mérjük: az összekötő vonalra ejtett
merőleges talppont is számít. Képzelj el egy kifeszített zsinórt két szög
között: a robot távolságát a zsinór legközelebbi pontjától kell mérni,
nem feltétlenül valamelyik szögtől.

Minden szakasz két végpontja `start` és `end`, méterben. A `dx` és `dy` a
két végpont koordinátakülönbsége, a `length_squared` ezek négyzetösszege,
négyzetméterben. A `fraction` a kezdőponttól a vizsgált pontig tartó vektornak
a szakaszirányra vett skalárszorzata, osztva a szakaszhossz négyzetével;
dimenzió nélküli arány. Ezt a kód 0 és 1 közé szorítja, hogy a véges
szakaszt, ne a végtelen egyenest mérje. A kapott aránnyal a kezdőponttól
a szakasz mentén haladunk, majd e talppont és a vizsgált `(x, y)` pont
euklideszi távolságát számítjuk.

Például `(0,0)` és `(1,0) m` között, `(0.5,0.4) m` végpontra `dx=1 m`,
`dy=0 m`, `length_squared=1 m²`, a skalárszorzat `0.5 m²`. Az arány `0.5`,
tehát a talppont `(0.5,0) m`, a távolság `0.4 m`. Csak a waypointokhoz mérve
hibásan `sqrt(0.5² + 0.4²) = 0.6403 m` adódna. A `(-0.3,0.4) m` pontnál
az arány negatív lenne, ezért 0-ra szorítjuk, és a szakasz kezdőpontjához
mérjük a `0.5 m` távolságot.

### Szélső esetek és tesztelés

Azonos szakaszvégpontoknál a vetítési arány 0, így nincs nullával osztás.
Egypontos útvonalnál ponttávolságot kapunk. A kód a túl nagy indexeket az
útvonal végéhez igazítja. Üres útvonalra a távolság pozitív végtelen; a
vezérlő ezt az esetet korábban kezeli, így nem pontoz ilyen pályát.

A `test/test_path_tracking.cpp` ellenőrzi az egyenes és kanyarodó szakaszt,
az ismételt és egyetlen pontot, az üres listát, a végpontra szorított vetítést,
a vizsgált tartományból kizárt későbbi visszatérő ágat, a visszatérés és a
párhuzamos haladás összehasonlítását, a cél megközelítését és a nullázott
súlyokkal kikapcsolt büntetést. Sikertelen állításnál kivétellel és nem nulla
kilépési kóddal áll le. A `CMakeLists.txt` `BUILD_TESTING` esetén önálló
`test_path_tracking` futtatható programként fordítja, és `path_tracking`
néven regisztrálja a CTest-ben; külön ROS2- vagy tesztkönyvtár nem kell a
teszt forrásának közvetlen C++17 fordításához.
