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
    -> lokális akadályrács
    -> A* (Grid cellák)
    -> következő waypoint
    -> DWA sebességvizsgálat
    -> /cmd_vel
```

A `/goal_pose` üzenet új világkoordinátás célt állít be. Az A* útvonalat a
`/astar_path` `nav_msgs/Path` topicon teszi közzé. A robot számára a lényeges
interfész tehát: `LaserScan`, `Odometry`, `PoseStamped`, `Twist` és `Path`.

### 12.3. Fontos paraméterek és koordináták

Az `astar_dwa_controller/config/rosbot.yaml` tartalmazza a topic-neveket,
a célt, a `map_size` értéket, a `resolution` cellaméretet és a
`robot_radius` biztonsági sugarat. A C++ node lokális, négyzetes rácsot épít
a robot körül. A rácskoordináta:

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

A DWA a `v = 0...0.4 m/s` és `omega = -1.2...1.2 rad/s` mintapárokat
vizsgálja. Minden pár 15 darab, egyenként `0.1 s` hosszú előrelépéssel
szimulálódik. Ütközés esetén a pár kiesik. A pontszám:

```text
score = -goal_distance - 0.25 * |heading_error| + 0.15 * v
```

Ha egy jelölt 1 m-re van a céltól, a szögeltérés `0.2 rad`, a sebesség
`0.4 m/s`, akkor a pontszám `-1 - 0.25*0.2 + 0.15*0.4 =
-1 - 0.05 + 0.06 = -0.99`. A nagyobb pontszámú biztonságos pár
kerül a `/cmd_vel` üzenetbe.

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
