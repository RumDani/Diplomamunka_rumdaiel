# A* útvonaltervezés fejlesztési terve

## 0. A dokumentum célja

Ez a dokumentum a szakdolgozati fejlesztés gyakorlati terve. A cél egy olyan Python-alapú kísérleti környezet létrehozása, amelyben az A* algoritmus alap- és továbbfejlesztett változatai azonos feltételek mellett vizsgálhatók.

A későbbi cél az A* globális útvonaltervező és a DWA lokális vezérlő összekapcsolása, majd az eredmény ROS2/Gazebo környezetben történő kipróbálása.

A fejlesztés fő sorrendje:

```text
Rácsos térkép
    -> klasszikus A*
    -> továbbfejlesztett A* változatok
    -> útvonal-simítás
    -> mérési és összehasonlítási rendszer
    -> A* + DWA Python-szimuláció
    -> ROS2 integráció
    -> SBA* külön kutatási ág
```

---

## 1. Kiindulási állapot

### 1.1. Meglévő Python DWA-szimuláció

A `DWA_py.py` már tartalmazza:

- differenciális hajtású robotmodell;
- keréksebességből számított `v` és `w` értékeket;
- gyorsuláskorlátozást;
- statikus és mozgó akadályokat;
- biztonságos sebességpárok keresését;
- trajektória-előrejelzést;
- ütközésvizsgálatot;
- grafikus megjelenítést;
- paramétersöprést és CSV-mentést.

Ez jó alap a későbbi DWA-mérésekhez.

### 1.2. Meglévő ROS2 DWA

A ROS2-es DWA-csomópont jelenleg:

- LiDAR-adatokat olvas;
- odometriát és TF-transzformációt használ;
- célpozíciót fogad;
- `cmd_vel` üzenetet publikál.

A Python-szimulációhoz képest azonban még egyszerűsített:

- csak kevés sebességértéket vizsgál;
- nem teljes dinamikus ablakot használ;
- rövid trajektóriák helyett lényegében egy előre jelzett pozíciót ellenőriz;
- nincs globális A* útvonal;
- nincs waypoint- vagy kulcspont-követés.

Ezért az A* fejlesztést először külön Python-modulban kell megvalósítani.

---

## 2. Végső rendszerarchitektúra

A tervezett rendszer három fő részből áll.

```text
Occupancy Grid / statikus térkép
              |
              v
       Globális A* tervező
              |
              v
       Teljes globális útvonal
              |
              v
       Kulcspont-kiválasztás
              |
              v
       Lokális DWA tervező
              |
              v
             cmd_vel
```

### 2.1. A* feladata

Az A* a statikus vagy lassan változó térképen megkeresi a kezdőpont és a célpont közötti útvonalat.

Az A* nem feladata:

- a robotsebesség közvetlen vezérlése;
- a dinamikus akadályok pillanatnyi elkerülése;
- a `cmd_vel` kiadása;
- a differenciális hajtás teljes szimulációja.

### 2.2. DWA feladata

A DWA a globális útvonal egy következő kulcspontját követi, miközben:

- figyelembe veszi a robot aktuális sebességét;
- sebességpárokat vagy `(v, w)` párokat vizsgál;
- rövid trajektóriákat szimulál;
- ellenőrzi az akadályokat;
- betartja a gyorsulási és fékezési korlátokat.

---

## 3. Javasolt projektstruktúra

Az A* kísérleti kódot a `codes_diploma` mappán belül külön alkönyvtárban érdemes tartani.

```text
codes_diploma/
    tudasbazis.MD
    DWA+A.py
    ASTAR_FEJLESZTESI_TERV.md
    astar_project/
        __init__.py
        grid_map.py
        astar_baseline.py
        astar_variants.py
        path_smoothing.py
        scenarios.py
        metrics.py
        experiments.py
        plots.py
        run_experiment.py
        tests/
            test_grid_map.py
            test_astar_baseline.py
            test_path_smoothing.py
        results/
            raw/
            figures/
            tables/
```

A fájlok feladata:

| Fájl | Feladat |
|---|---|
| `grid_map.py` | Rácstérkép, cellák, akadályok és robot-infláció |
| `astar_baseline.py` | Klasszikus A* |
| `astar_variants.py` | EA*, EBA*, EBHA*, EBHSA* változatok |
| `path_smoothing.py` | Kollineáris szűrés és inflection bypass |
| `scenarios.py` | Tesztpályák előállítása |
| `metrics.py` | Útvonal- és teljesítménymutatók |
| `experiments.py` | Ismételt futtatások és paramétersöprések |
| `plots.py` | Térképek, útvonalak és összehasonlító ábrák |
| `run_experiment.py` | Parancssoros belépési pont |
| `tests/` | Automatikus ellenőrzések |

---

## 4. Fejlesztési fázisok

## Fázis 1: Rácsos térképmodell

### Feladatok

1. 2D tömb alapú occupancy grid létrehozása.
2. Szabad és foglalt cellák kezelése.
3. Kezdő- és célpont validálása.
4. Pályák kirajzolása.
5. Robot- és akadályméret figyelembevétele.

A robotot nem szabad egyetlen matematikai pontként kezelni, ha ütközésbiztonságot szeretnénk vizsgálni. Az akadályokat ki kell tágítani:

$$
r_{inflated} = r_{robot} + r_{obstacle} + r_{safety}
$$

### Ellenőrzés

- A kezdő- és célcella szabad.
- A térkép megjelenik.
- A robot-infláció után sem kerül a kezdő vagy célcella akadályba.

---

## Fázis 2: Klasszikus A*

A referenciaalgoritmus értékelőfüggvénye:

$$
f(n) = g(n) + h(n)
$$

ahol:

- `g(n)` a kezdőponttól az aktuális csomópontig megtett költség;
- `h(n)` az aktuális csomópont és a cél közötti heurisztikus becslés;
- `f(n)` a prioritási érték.

### Elsőként implementálandó változatok

1. 4-szomszédos keresés + Manhattan-heurisztika.
2. 8-szomszédos keresés + diagonális költség.
3. 8-szomszédos keresés + Euklideszi heurisztika.

### Fontos adatok

Minden csomópontnál tárolni kell:

```text
position
parent
g_cost
h_cost
f_cost
```

A prioritási sorhoz min-heap használata javasolt.

### Ellenőrzés

- Egyszerű, akadálymentes pályán megtalálja az útvonalat.
- Akadály esetén kerülőutat keres.
- Elérhetetlen cél esetén szabályosan jelez.
- A visszafejtett útvonal szomszédos cellákból áll.

---

## Fázis 3: Alapmérési rendszer

Minden futásból legalább az alábbi adatokat kell menteni:

| Metrika | Jelentés |
|---|---|
| `success` | Elérte-e a célpontot |
| `planning_time_ms` | Tervezési idő |
| `expanded_nodes` | Kibővített csomópontok száma |
| `visited_nodes` | Megvizsgált csomópontok száma |
| `path_length` | Útvonal hossza |
| `path_nodes` | Útvonal csomópontjainak száma |
| `turn_count` | Irányváltások száma |
| `max_turn_angle` | Legnagyobb irányváltozás |
| `map_id` | Tesztpálya azonosítója |
| `algorithm` | Használt algoritmus |

Az eredményeket CSV vagy Parquet formátumban kell menteni. A megjelenítéshez PNG és SVG ábrák készíthetők.

### Ellenőrzés

Ugyanazt a térképet legalább ötször kell lefuttatni, és ellenőrizni kell, hogy determinisztikus algoritmusnál az eredmények megegyeznek-e.

---

## Fázis 4: EA* - Enhanced A*

Az EA* elnevezést csak akkor szabad végleges szakirodalmi névként használni, ha hozzá tartozik konkrét publikáció és pontos definíció.

A jelenlegi kísérleti tervben az EA* a klasszikus A* továbbfejlesztett változata lehet:

- célirányos szomszédságvizsgálat;
- redundáns irányok elhagyása;
- javított heurisztika;
- sarokvágás elleni védelem;
- opcionális dinamikus heurisztikasúly.

A tudástárban szereplő exponenciális súlyozás:

$$
P = \frac{|x_n-x_g|+|y_n-y_g|}{|x_s-x_g|+|y_s-y_g|}
$$

$$
f(n) = g(n) + e^P h(n)
$$

Ezt külön konfigurációként kell vizsgálni, mert a súlyozott heurisztika gyorsíthatja a keresést, de nem feltétlenül őrzi meg a klasszikus A* optimális útvonalgaranciáját.

### Mérendő hatás

- csökken-e a kibővített csomópontok száma;
- csökken-e a tervezési idő;
- változik-e az útvonalhossz;
- nő-e a kanyarszám vagy csökken-e.

---

## Fázis 5: EBA* - kétirányú változat

Az EBA* munkadefiníciója:

- keresés a kezdőpontból és a célpontból egyszerre;
- a két keresési front találkozásakor útvonal-összekapcsolás;
- a klasszikus A* és az EA* eredményeivel való összehasonlítás.

A kétirányú keresésnél külön ellenőrizni kell:

- valóban találkozik-e a két front;
- helyesen történik-e a szülőmutatók összefűzése;
- az összekötött útvonal nem tartalmaz-e érvénytelen átmenetet;
- a megállási feltétel nem rontja-e az útvonal optimalitását.

### Mérendő hatás

- keresési idő;
- két irányban kibővített csomópontok száma;
- útvonalhossz;
- memóriaigény;
- sikertelen esetek aránya.

---

## Fázis 6: EBHA* - heurisztikával továbbfejlesztett kétirányú A*

Az EBHA* munkadefiníciója:

```text
EA* jellegű heurisztika
    + kétirányú keresés
    + irányfüggő vagy dinamikus prioritás
```

A heurisztika változtatásait külön kell kapcsolhatóvá tenni. Nem célszerű egyszerre beépíteni a szomszédságcsökkentést, a dinamikus súlyozást és a kétirányú keresést, mert akkor nem lesz megállapítható, melyik módosítás okozza az eredményt.

Javasolt kísérleti sorrend:

```text
A*
A* + dinamikus heurisztika
A* + szomszédságoptimalizálás
EBA*
EBHA*
```

---

## Fázis 7: EBHSA* - simítással kiegészített változat

Az EBHSA* munkadefiníciója:

```text
EBHA*
    + kollineáris pontok törlése
    + akadálymentes inflection bypass
```

A simítást külön utófeldolgozásként kell megvalósítani, nem közvetlenül a keresési ciklusban.

### Kollineáris pont törlése

Ha három egymást követő pont azonos irányban fekszik, a középső pont törölhető.

### Inflection bypass

Ha két töréspont közvetlenül összeköthető akadálymentesen, és a közvetlen szakasz rövidebb, mint az eredeti részút, akkor a köztes pontok eltávolíthatók.

### Kötelező biztonsági feltétel

A simítás után minden új szakaszt újra ütközésvizsgálattal kell ellenőrizni.

---

## 5. Tesztpályák

Legalább az alábbi pályákat kell létrehozni:

1. akadálymentes tér;
2. egyetlen akadály;
3. több akadály;
4. U alakú akadály;
5. szűk folyosó;
6. zsákutca;
7. több azonos hosszúságú kerülőút;
8. sűrű akadálymező;
9. dinamikus akadályokat tartalmazó pálya a későbbi DWA-vizsgálathoz.

Minden algoritmust ugyanazon térképeken kell futtatni, azonos kezdő- és célponttal.

---

## 6. Kísérleti mátrix

A minimális összehasonlítás:

```text
A*
EA*
EBA*
EBHA*
EBHSA*
```

A későbbi hibrid összehasonlítás:

```text
A* + DWA
EA* + DWA
EBA* + DWA
EBHA* + DWA
EBHSA* + DWA
```

Minden kombináció esetén azonos legyen:

- térkép;
- kezdőpont;
- célpont;
- robotméret;
- biztonsági margó;
- DWA sebességkorlátja;
- DWA előretekintési ideje;
- akadálylista;
- mérési időszak.

---

## 7. A* és DWA összekapcsolása

A globális A* útvonalat a DWA nem teljes egészében, hanem kulcspontokon keresztül követi.

Egy waypoint akkor teljesített, ha:

$$
\sqrt{(x-x_w)^2+(y-y_w)^2} < \varepsilon_w
$$

A vezérlési ciklus logikája:

```text
1. Robotpozíció frissítése
2. Aktuális waypoint kiválasztása
3. DWA sebességpárok generálása
4. Trajektóriák szimulációja
5. Ütközés- és fékezési feltételek ellenőrzése
6. Legjobb trajektória kiválasztása
7. cmd_vel kiadása
8. Waypoint teljesítésének ellenőrzése
9. Szükség esetén globális újratervezés
```

Globális újratervezés szükséges lehet, ha:

- a térkép megváltozik;
- a célpont elérhetetlenné válik;
- a DWA tartósan holtpontba kerül;
- a robot jelentősen eltér a globális útvonaltól.

---

## 8. DWA továbbfejlesztése az A* után

A Python DWA-szimulációban megtartandó elemek:

- differenciális hajtásmodell;
- keréksebességből számított mozgás;
- gyorsuláskorlátozás;
- fékezési feltétel;
- trajektória-rollout;
- mozgó akadályok előrejelzése;
- paramétersweep.

A későbbi integrációhoz módosítani kell:

- a célpontot az aktuális waypoint adja;
- a heading pontszám a globális útvonal irányát is vegye figyelembe;
- legyen útvonaltól való oldaltávolság-pontszám;
- a DWA ne menjen a globális útvonal biztonsági sávján kívülre, ha ez nem szükséges.

---

## 9. SBA* későbbi kutatási ágként

Az SBA* nem az első implementáció része. Külön modulban készüljön, mert eltérő problémát old meg:

- folytonos állapottér;
- mintavételezés;
- lokális elérhetőség;
- `STEER` művelet;
- folytonos ütközésvizsgálat;
- új csomópont valószínűségi értékelése;
- sűrűségi és szűkületi állapotok.

A javasolt sorrend:

```text
klasszikus A*
    -> továbbfejlesztett diszkrét A*
    -> A* + DWA
    -> SBA* külön Python-szimuláció
    -> SBA* és lokális vezérlő integrációja
```

---

## 10. Szakdolgozati kutatási kérdések

1. Csökkenti-e a továbbfejlesztett szomszédságvizsgálat a kibővített csomópontok számát?
2. Csökkenti-e a dinamikus heurisztika a tervezési időt?
3. Milyen hatással van a heurisztika módosítása az útvonal optimális hosszára?
4. Javítja-e a kétirányú keresés a nagyobb térképeken a futási időt?
5. Csökkenti-e az útvonal-simítás a kanyarszámot és az irányváltozások összegét?
6. Javítja-e az EBHSA* útvonala a DWA követési stabilitását?
7. Melyik globális A* változat adja a legjobb kompromisszumot útvonalhossz, tervezési idő és DWA-követhetőség között?
8. Hogyan változik a teljesítmény statikus és dinamikus akadályok mellett?

---

## 11. Javasolt első konkrét munkamenet

### Első lépés

Készítsd el a `GridMap` osztályt:

- szélesség;
- magasság;
- cellaméret;
- akadálycellák;
- kezdőpont;
- célpont;
- cella szabad/akadály lekérdezése.

### Második lépés

Implementáld a klasszikus A*-t Manhattan-heurisztikával.

### Harmadik lépés

Készíts egy egyszerű ábrát, amelyen látható:

- akadályok;
- kezdőpont;
- célpont;
- kibővített csomópontok;
- végső útvonal.

### Negyedik lépés

Adj hozzá mérési adatokat:

- futási idő;
- kibővített csomópontok;
- útvonalhossz;
- kanyarszám.

### Ötödik lépés

Csak ezután kezdd el az EA* első módosítását.

---

## 12. Források és forráskezelés

A rövidítések használata előtt minden algoritmushoz fel kell venni:

- teljes algoritmusnév;
- szerzők;
- év;
- DOI vagy stabil URL;
- pontos pszeudokód;
- módosított képlet;
- optimális vagy közelítő jelleg;
- saját implementációs eltérések.

Fontos kiinduló források:

- Hart, Nilsson és Raphael: *A Formal Basis for the Heuristic Determination of Minimum Cost Paths*, DOI: `10.1109/TSSC.1968.300136`.
- Liu, Wang, Wu és Wei: *Mobile Robot Path Planning Based on Kinematically Constrained A-Star Algorithm and DWA Fusion Algorithm*, DOI: `10.3390/math11214552`.
- Fox, Burgard és Thrun: *The Dynamic Window Approach to Collision Avoidance*, DOI: `10.1109/100.580977`.

Az `EA*`, `EBA*`, `EBHA*` és `EBHSA*` rövidítésekhez külön, ellenőrzött bibliográfiai forrást kell rögzíteni, vagy világosan saját kísérleti elnevezésként kell megadni őket.

---

## 13. Elkészültnek tekinthető mérföldkövek

### Mérföldkő 1

A klasszikus A* legalább három pályán helyes útvonalat ad.

### Mérföldkő 2

Az A* eredményei automatikusan CSV-be menthetők.

### Mérföldkő 3

Az EA*, EBA*, EBHA* és EBHSA* ugyanazzal a mérési rendszerrel futtatható.

### Mérföldkő 4

Az útvonal-simítás után minden szakasz ütközésmentes marad.

### Mérföldkő 5

A Python DWA egy A* által generált waypoint-listát követ.

### Mérföldkő 6

Az A*–DWA rendszer dinamikus akadályos szimulációban is mérhető.

### Mérföldkő 7

A legjobb változat ROS2/Gazebo környezetben is futtatható.

---

## 14. Rövid döntési szabályok fejlesztés közben

- Először mindig legyen működő referencia-A*.
- Egyszerre csak egy algoritmikus módosítást vezess be.
- Minden változat ugyanazon pályákon fusson.
- A gyorsabb algoritmus nem automatikusan jobb algoritmus.
- Az útvonalhossz és a tervezési idő mellett a kanyarszámot is mérni kell.
- A simítás csak új ütközésvizsgálat után fogadható el.
- A globális A* és a lokális DWA felelősségét külön kell tartani.
- Az SBA* csak a diszkrét A* validációja után következzen.
