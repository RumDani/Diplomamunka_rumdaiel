---
name: kodmagyarazat
description: "Use when the user asks for a detailed Hungarian explanation of code, algorithms, classes, functions, parameters, coordinate systems, resolution, data structures, or requests that explanations be saved and kept updated."
---

# Egyszerű A* kódmagyarázat és fejlesztési folyamat

## Cél

Magyarázd el a kódot magyarul, egyszerűen és konkrét példákkal. Mindig a jelenlegi fájlt olvasd el először; ne magyarázz feltételezett vagy régi kódot.

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
5. Csak sikeres ellenőrzés után lépj tovább a következő fázisra.

## Magyarázat tartalma

Térj ki ezekre, amikor relevánsak:

- a fájl, osztály és függvény célja;
- paraméterek, visszatérési értékek és hibák;
- adatszerkezetek és az A* adatfolyam;
- `g`, `h`, `f`, heurisztika és szomszédság;
- rácskoordináta `(row, column)` és világkoordináta `(x, y)`;
- `resolution`, cellaméret, origó és koordináta-átalakítás;
- legalább egy kis, végigszámolt példa.

Ne csak soronként fordítsd le a kódot: először a működési elképzelést, utána a fontos részleteket magyarázd el.

## Tudásbázis használata

Az `codes_diploma/tudasbazis.MD` ötlet- és háttérforrásként használható. Segíthet heurisztikák, szomszédsági szabályok, útvonal-simítási módszerek és SBA* irányok megértésében.

A tudásbázis nem helyettesíti a jelenlegi kódot, a szakirodalmi ellenőrzést vagy a tesztet. Az onnan származó ötletet külön, kis lépésben vezesd be; ne állítsd működőnek vagy bizonyítottnak addig, amíg a kód és a tesztek ezt nem igazolják. A DWA-s anyagokat csak akkor használd, ha az aktuális feladat kifejezetten az A* és DWA kapcsolatáról szól.

## Magyarázatok mentése és frissítése

A tartós magyarázatokat a `codes_diploma/KODMAGYARAZATOK.md` fájlba írd.

Működést érintő kódmódosítás után ellenőrizd az érintett magyarázatot, és frissítsd, ha elavult. Formázási vagy működést nem érintő változás miatt nem kell új magyarázatot írni.

## Stílus

- Magyarul, világosan és felesleges bonyolítás nélkül fogalmazz.
- Használj rövid kódrészleteket és konkrét számolást.
- Tüntesd fel a mértékegységeket.
- Ne állíts olyat, amit a jelenlegi kód, teszt vagy ellenőrzött forrás nem támaszt alá.
