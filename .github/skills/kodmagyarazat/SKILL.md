---
name: kodmagyarazat
description: "Use for every detailed Hungarian code explanation, algorithm explanation, code-change explanation, class/function explanation, parameter or data-structure explanation, coordinate/resolution explanation, or request to save and keep explanations updated."
---

# Egyszerű, követhető kódmagyarázat és fejlesztési folyamat

## Cél

Magyarázd el a kódot magyarul, egyszerűen, de ne túl tömören. Mindig a jelenlegi
fájlt olvasd el először; ne magyarázz feltételezett vagy régi kódot.

Ez a forma minden kódra érvényes, nem csak az A* modulokra. A magyarázat célja,
hogy az olvasó a kódot később önállóan is követni tudja, ne csak rövid
függvénylistát kapjon.
## Kötelező fejlesztési sorrend

A projekt alapértelmezett sorrendje:

```text
rácstérkép
-> klasszikus A*
-> alapmérések és tesztek
-> A* változatok
-> útvonal-simítás
-> kísérletek és összehasonlítás
-> későbbi SBA* vagy integrációs ág
```

Új kódot ebbe a sorrendbe illesztve tervezz és magyarázz. Először legyen működő és tesztelt alap, csak utána jöjjön optimalizálás vagy új algoritmus.

Ha a feladat eltér ettől a sorrendtől:

1. azonosítsd, melyik fejlesztési fázist érinti;
2. módosítsd a fejlesztési tervet, ha a sorrend tartósan megváltozik;
3. a változást írd le röviden az `ASTAR_FEJLESZTESI_TERV.md` fájlban;
4. az eltérést ne rejtsd el, hanem jelezd a magyarázatban és az ellenőrzésben.

## Munkamenet

1. Olvasd el a módosított fájlt és a közvetlen teszteket vagy használatokat.
2. Mondd ki röviden, mi a fájl feladata és mi változik.
3. Végezd el a legkisebb szükséges kódmódosítást.
4. Futtass célzott tesztet vagy más gyors ellenőrzést.
5. A lezárás előtt mindig végezz konzisztencia-auditot: vesd össze a jelenlegi kód tényleges függvényneveit, paramétereit, visszatérési értékeit, adatfolyamát, algoritmusát és megjelenítését a `codes_diploma/KODMAGYARAZATOK.md` érintett fejezeteivel és az `ASTAR_PROJEKT_FOLYAMATBRA.gv` ábrával.
6. Keresd meg és javítsd az elavult, törölt vagy nem bizonyított állításokat; külön ellenőrizd a hívási sorrendet, a döntési ágakat, a képleteket, a konkrét számolási példákat és a tesztparancsokat.
7. A frissített magyarázat és folyamatábra csak akkor tekinthető késznek, ha minden állítás visszavezethető a jelenlegi kódra vagy egy lefuttatott célzott tesztre. Ha egy eltérés nem javítható a jelenlegi munkamenetben, jelezd külön a lezárásban.
8. Csak sikeres kód- és dokumentációs ellenőrzés után lépj tovább a következő fázisra.

### Kötelező kód–magyarázat ellenőrzés

Ezt az ellenőrzést minden részletes magyar kódmagyarázat, kódmódosítás és
magyarázat-frissítés végén el kell végezni, akkor is, ha a kód nem változott.

- A magyarázatban szereplő minden nyilvános és fontos belső függvénynév,
	paraméter és visszatérési forma egyezzen a jelenlegi fájllal.
- A leírt algoritmus, képlet, koordináta-átalakítás, alapértelmezett érték és
	hibakezelés egyezzen a jelenlegi végrehajtással.
- A magyarázatban szereplő összes matematikai képletet külön bontsd fel: nevezd
	meg minden változó jelentését és mértékegységét, magyarázd el a műveletek
	sorrendjét közérthetően, és adj hozzá legalább egy konkrét behelyettesítési
	példát. Képlet nem maradhat csak leírva vagy megnevezve magyarázat nélkül.
- A magyarázat ne tartalmazzon olyan felületi elemet, jelölést, gombot,
	animációs állapotot vagy modult, amelyet a jelenlegi kód már nem használ.
- A folyamatábra hívási sorrendjét és kapcsolatait is vesd össze a kóddal;
	hívási sorrend, döntési ág vagy fontos adatkapcsolat eltérése esetén frissítsd.
- Futtasd a legszűkebb érintett tesztet, majd ha több modul vagy dokumentum
	érintett, a teljes releváns tesztcsomagot is.
- A lezárásban röviden rögzítsd, mit ellenőriztél, milyen parancs futott le, és
	maradt-e ismert eltérés vagy figyelmeztetés.

## Magyarázat tartalma

Minden tartós kódmagyarázatot az alábbi sorrendben építs fel:

1. **A fájl célja:** milyen problémát old meg és hol helyezkedik el a programban.
2. **Adatfolyam:** mi érkezik bemenetként, mi történik vele, és mi lesz a kimenet.
3. **Fontos adatok:** listák, szótárak, objektumok, rácsok, koordináták vagy állapotok.
4. **Függvények és osztályok:** cél, paraméterek, visszatérési érték és hibakezelés.
5. **Algoritmus vagy matematika:** a képletet és a döntési logikát hétköznapi nyelven is írd le.
6. **Konkrét számolási példa:** kis, végigszámolt bemenettel mutasd meg a működést.
7. **Biztonsági feltételek és korlátok:** mikor utasít el adatot, mikor tér vissza alapállapotba, és miért.
8. **Kapcsolat és tesztelés:** melyik modul hívja, mitől függ, és milyen teszt ellenőrzi.

Ezek mellett térj ki, amikor releváns:
- paraméterek, visszatérési értékek és hibák;
- adatszerkezetek és az A* adatfolyam;
- `g`, `h`, `f`, heurisztika és szomszédság;
- rácskoordináta `(row, column)` és világkoordináta `(x, y)`;
- `resolution`, cellaméret, origó és koordináta-átalakítás;
- legalább egy kis, végigszámolt példa;
- a tényleges jelenlegi kód és az esetleges vizuális megjelenítés közötti különbség.

Ne csak soronként fordítsd le a kódot. Először adj működési képet, utána bontsd
ki a fontos részeket. A magyarázat legyen tagolt címsorokkal és rövid
kódrészletekkel, de ne legyen felsorolásból álló, nehezen olvasható kivonat.

Ne csak soronként fordítsd le a kódot: először a működési elképzelést, utána a fontos részleteket magyarázd el.

## Tudásbázis használata

Az `codes_diploma/tudasbazis.MD` ötlet- és háttérforrásként használható. Segíthet heurisztikák, szomszédsági szabályok, útvonal-simítási módszerek és SBA* irányok megértésében.

A tudásbázis nem helyettesíti a jelenlegi kódot, a szakirodalmi ellenőrzést vagy a tesztet. Az onnan származó ötletet külön, kis lépésben vezesd be; ne állítsd működőnek vagy bizonyítottnak addig, amíg a kód és a tesztek ezt nem igazolják. A DWA-s anyagokat csak akkor használd, ha az aktuális feladat kifejezetten az A* és DWA kapcsolatáról szól.

## Magyarázatok mentése és frissítése

A tartós magyarázatokat a `codes_diploma/KODMAGYARAZATOK.md` fájl végére írd,
új, számozott fejezetként. Így az új magyarázat nem keveredik össze a korábbi
fájlmagyarázatokkal.

Minden módosított vagy részletesen bemutatott fájlhez készíts külön, közvetlenül
a kódhoz tartozó magyarázati fejezetet. A fejezetben a jelenlegi kód alatt,
olvasható sorrendben szerepeljen a fájl célja, az adatfolyam, a függvények,
az algoritmus vagy képlet, egy konkrét számolási példa, a biztonsági korlátok
és a tesztelés. Ne elégedj meg egy rövid összefoglalóval.

Kódmódosítás után ezt ugyanabban a munkamenetben kell elvégezni. A lezárás
előtti ellenőrzőlista:

- a magyarázat a jelenlegi kód függvényneveit használja;
- nincs benne régi vagy már törölt algoritmus;
- van legalább egy konkrét számolási példa;
- le van írva a bemenet, a kimenet és a hibás/veszélyes eset kezelése;
- szerepel a célzott teszt parancsa és eredménye;
- a magyarázat a `KODMAGYARAZATOK.md` végén külön fejezetként megkereshető.

Működést érintő kódmódosítás után ellenőrizd az érintett magyarázatot, és frissítsd, ha elavult. Formázási vagy működést nem érintő változás miatt nem kell új magyarázatot írni.

Ha több, egymással összefüggő fájl változik, a magyarázatban külön nevezd meg
a hívási sorrendet és azt, hogy melyik fájlban dől el a viselkedés. Ne írj olyan
magyarázatot, amelyet a jelenlegi fájl vagy egy célzott teszt nem támaszt alá.
## Stílus

- Magyarul, világosan és felesleges bonyolítás nélkül fogalmazz.
- Használj rövid kódrészleteket és konkrét számolást.
- Tüntesd fel a mértékegységeket.
- Ne állíts olyat, amit a jelenlegi kód, teszt vagy ellenőrzött forrás nem támaszt alá.
