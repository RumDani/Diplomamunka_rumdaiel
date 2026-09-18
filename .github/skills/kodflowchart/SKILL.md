---
name: kodflowchart
description: "Use when the user asks for a flowchart, pseudo-flowchart, function call map, code relationship diagram, execution order, or a continuously updated visual explanation of the A* project."
---

# A* projekt-flowchart és kapcsolati térkép

## Cél

Tedd átláthatóvá, hogy az A*-fejlesztésben melyik modul és függvény mikor kapcsolódik a többihez, milyen adatot kap, és mit ad tovább. A projekt aktuális ábráját Graphviz `.gv` diagramként vezesd.

## Forrásfájlok

A jelenlegi A* folyamat ellenőrzéséhez mindig olvasd el:

- `codes_diploma/astar_project/astar_baseline.py`
- `codes_diploma/astar_project/grid_map.py`
- `codes_diploma/astar_project/astar_simulation.py`
- a közvetlen teszteket a `codes_diploma/astar_project/tests/` alatt
- szükség esetén az `ASTAR_FEJLESZTESI_TERV.md` fájlt
- csak az `astar_project` A*-hoz tartozó forrásfájlokat és teszteket

## Munkamenet

1. Olvasd el az aktuális fájlokat, mielőtt az ábrát módosítod.
2. Keresd meg a belépési függvényt és a tényleges hívásokat.
3. Írd le a normál végrehajtási sorrendet.
4. Jelöld a fontos döntési pontokat: validáció, ciklus, cél elérése, sikertelen keresés, jobb útvonal.
5. Jelöld a fontos adatok útját, például `open_nodes`, `came_from` és `g_costs`.
6. Csak a jelenleg megvalósított kódot ábrázold; tervezett vagy üres modul ne kerüljön bele.
7. Ha a fejlesztés során új A* függvény vagy modul ténylegesen elkészül, frissítsd az ábrát ugyanabban a munkamenetben.

## Mentés

A tartós, szebben megjeleníthető A* Graphviz ábra helye:

```text
codes_diploma/ASTAR_PROJEKT_FOLYAMATBRA.gv
```

A hosszabb függvénymagyarázatok helye:

```text
codes_diploma/KODMAGYARAZATOK.md
```

A Graphviz diagramot `.gv`-t támogató VS Code-bővítménnyel vagy a Graphviz `dot` programjával lehet SVG/PNG formátumba renderelni. Ez az egyetlen elsődleges A* folyamatábra; külön ASCII/Markdown-flowchartot nem kell fenntartani.

A flowchart és a kódmagyarázat egymást egészítse ki: az ábra a sorrendet és kapcsolatokat, a magyarázat a részletes működést írja le.

## Egyszerűségi szabályok

- Graphviz-dobozokat és klasztereket használj, hogy a fejlesztési fázisok és a függvényhívások elkülönüljenek.
- Egy doboz egy logikai lépést jelentsen.
- A függvényneveket és az adatstruktúrákat pontosan írd.
- Minden ág mellett legyen rövid jelentés, például `igen`, `nem`, `nincs út`.
- Ne használj túl sok technikai rövidítést.
- A diagram után adj rövid, szöveges hívási láncot is.
- A szaggatott kapcsolatokat csak belső, segéd- vagy indirekt hívások jelölésére használd; nem megvalósított kódot ne ábrázolj.

## Frissítési ellenőrzés

Módosítás után ellenőrizd:

- a flowchart belépési függvénye létezik-e;
- minden ábrázolt hívás megtalálható-e a kódban;
- a hívási sorrend megfelel-e a vezérlésnek;
- a visszatérési pontok és hibás ágak szerepelnek-e;
- az adatstruktúrák nevei egyeznek-e a kóddal.
- az A* diagram minden modulja és függvénye ténylegesen megvalósított kódhoz tartozik-e.

A flowchartot ne tekintsd automatikusan generáltnak. Kódváltozás után a dokumentumot a módosítást végző munkamenetben kell ellenőrizni és frissíteni.
