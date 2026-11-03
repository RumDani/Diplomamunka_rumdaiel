# AI-kodcsomag - aktualis projektforras

Generalt datum: 2026-11-01 13:45
Ez a fajl a jelenlegi forraskodot, ROS 2/Gazebo konfiguraciokat, teszteket es dokumentaciokat tartalmazza. A build/install/log/.venv/cache es binaris fajlok kimaradnak.

### .github/copilot-instructions.md

```markdown
# Projekt-specifikus Copilot-instructions

## KĂłdmagyarĂˇzatok

- A felhasznĂˇlĂł kĂ©rĂ©sĂ©re kĂ©szĂ­ts rĂ©szletes, magyar nyelvĹ± kĂłdmagyarĂˇzatot.
- A magyarĂˇzatban tĂ©rj ki a fĂˇjl cĂ©ljĂˇra, a fontos osztĂˇlyokra Ă©s fĂĽggvĂ©nyekre, a paramĂ©terekre, az adatszerkezetekre, a koordinĂˇtĂˇkra, az algoritmus logikĂˇjĂˇra Ă©s legalĂˇbb egy konkrĂ©t szĂˇmolĂˇsi pĂ©ldĂˇra.
- A `resolution`, koordinĂˇta-ĂˇtalakĂ­tĂˇs Ă©s rĂˇcsindexelĂ©s jellegĹ± fogalmakat hĂ©tkĂ¶znapi elkĂ©pzelĂ©ssel Ă©s konkrĂ©t pĂ©ldĂˇval is magyarĂˇzd.
- A tartĂłs magyarĂˇzatokat a `codes_diploma/KODMAGYARAZATOK.md` fĂˇjlban kell gyĹ±jteni.
- Az A*-fejlesztĂ©s szĂ©p, vizuĂˇlisan renderelhetĹ‘ Graphviz-flowchartjĂˇt a `codes_diploma/ASTAR_PROJEKT_FOLYAMATBRA.gv` fĂˇjlban kell vezetni.
- KĂłdmĂłdosĂ­tĂˇs utĂˇn ellenĹ‘rizd, hogy az Ă©rintett magyarĂˇzat tovĂˇbbra is megfelel-e az aktuĂˇlis kĂłdnak; mĹ±kĂ¶dĂ©st Ă©rintĹ‘ vĂˇltozĂˇs esetĂ©n frissĂ­tsd a dokumentumot ugyanabban a munkamenetben.
- Ha vĂˇltozik a hĂ­vĂˇsi sorrend, egy fĂĽggvĂ©ny kapcsolata, egy dĂ¶ntĂ©si Ăˇg, egy fontos adatstruktĂşra, egy A* modul vagy a fejlesztĂ©si fĂˇzis, ugyanabban a munkamenetben frissĂ­tsd az `ASTAR_PROJEKT_FOLYAMATBRA.gv` fĂˇjlt is.
- Ne Ă­rj magyarĂˇzatot olyan kĂłdrĂłl, amelyet nem ellenĹ‘riztĂ©l a jelenlegi fĂˇjlban.
```

### .github/skills/kodflowchart/SKILL.md

```markdown
---
name: kodflowchart
description: "Use when the user asks for a flowchart, pseudo-flowchart, function call map, code relationship diagram, execution order, or a continuously updated visual explanation of the A* project."
---

# A* projekt-flowchart Ă©s kapcsolati tĂ©rkĂ©p

## CĂ©l

Tedd ĂˇtlĂˇthatĂłvĂˇ, hogy az A*-fejlesztĂ©sben melyik modul Ă©s fĂĽggvĂ©ny mikor kapcsolĂłdik a tĂ¶bbihez, milyen adatot kap, Ă©s mit ad tovĂˇbb. A projekt aktuĂˇlis ĂˇbrĂˇjĂˇt Graphviz `.gv` diagramkĂ©nt vezesd.

## ForrĂˇsfĂˇjlok

A jelenlegi A* folyamat ellenĹ‘rzĂ©sĂ©hez mindig olvasd el:

- `codes_diploma/astar_project/astar_baseline.py`
- `codes_diploma/astar_project/grid_map.py`
- `codes_diploma/astar_project/astar_simulation.py`
- a kĂ¶zvetlen teszteket a `codes_diploma/astar_project/tests/` alatt
- szĂĽksĂ©g esetĂ©n az `ASTAR_FEJLESZTESI_TERV.md` fĂˇjlt
- csak az `astar_project` A*-hoz tartozĂł forrĂˇsfĂˇjlokat Ă©s teszteket

## Munkamenet

1. Olvasd el az aktuĂˇlis fĂˇjlokat, mielĹ‘tt az ĂˇbrĂˇt mĂłdosĂ­tod.
2. Keresd meg a belĂ©pĂ©si fĂĽggvĂ©nyt Ă©s a tĂ©nyleges hĂ­vĂˇsokat.
3. ĂŤrd le a normĂˇl vĂ©grehajtĂˇsi sorrendet.
4. JelĂ¶ld a fontos dĂ¶ntĂ©si pontokat: validĂˇciĂł, ciklus, cĂ©l elĂ©rĂ©se, sikertelen keresĂ©s, jobb Ăştvonal.
5. JelĂ¶ld a fontos adatok ĂştjĂˇt, pĂ©ldĂˇul `open_nodes`, `came_from` Ă©s `g_costs`.
6. Csak a jelenleg megvalĂłsĂ­tott kĂłdot ĂˇbrĂˇzold; tervezett vagy ĂĽres modul ne kerĂĽljĂ¶n bele.
7. Ha a fejlesztĂ©s sorĂˇn Ăşj A* fĂĽggvĂ©ny vagy modul tĂ©nylegesen elkĂ©szĂĽl, frissĂ­tsd az ĂˇbrĂˇt ugyanabban a munkamenetben.

## MentĂ©s

A tartĂłs, szebben megjelenĂ­thetĹ‘ A* Graphviz Ăˇbra helye:

```text
codes_diploma/ASTAR_PROJEKT_FOLYAMATBRA.gv
```

A hosszabb fĂĽggvĂ©nymagyarĂˇzatok helye:

```text
codes_diploma/KODMAGYARAZATOK.md
```

A Graphviz diagramot `.gv`-t tĂˇmogatĂł VS Code-bĹ‘vĂ­tmĂ©nnyel vagy a Graphviz `dot` programjĂˇval lehet SVG/PNG formĂˇtumba renderelni. Ez az egyetlen elsĹ‘dleges A* folyamatĂˇbra; kĂĽlĂ¶n ASCII/Markdown-flowchartot nem kell fenntartani.

A flowchart Ă©s a kĂłdmagyarĂˇzat egymĂˇst egĂ©szĂ­tse ki: az Ăˇbra a sorrendet Ă©s kapcsolatokat, a magyarĂˇzat a rĂ©szletes mĹ±kĂ¶dĂ©st Ă­rja le.

## EgyszerĹ±sĂ©gi szabĂˇlyok

- Graphviz-dobozokat Ă©s klasztereket hasznĂˇlj, hogy a fejlesztĂ©si fĂˇzisok Ă©s a fĂĽggvĂ©nyhĂ­vĂˇsok elkĂĽlĂ¶nĂĽljenek.
- Egy doboz egy logikai lĂ©pĂ©st jelentsen.
- A fĂĽggvĂ©nyneveket Ă©s az adatstruktĂşrĂˇkat pontosan Ă­rd.
- Minden Ăˇg mellett legyen rĂ¶vid jelentĂ©s, pĂ©ldĂˇul `igen`, `nem`, `nincs Ăşt`.
- Ne hasznĂˇlj tĂşl sok technikai rĂ¶vidĂ­tĂ©st.
- A diagram utĂˇn adj rĂ¶vid, szĂ¶veges hĂ­vĂˇsi lĂˇncot is.
- A szaggatott kapcsolatokat csak belsĹ‘, segĂ©d- vagy indirekt hĂ­vĂˇsok jelĂ¶lĂ©sĂ©re hasznĂˇld; nem megvalĂłsĂ­tott kĂłdot ne ĂˇbrĂˇzolj.

## FrissĂ­tĂ©si ellenĹ‘rzĂ©s

MĂłdosĂ­tĂˇs utĂˇn ellenĹ‘rizd:

- a flowchart belĂ©pĂ©si fĂĽggvĂ©nye lĂ©tezik-e;
- minden ĂˇbrĂˇzolt hĂ­vĂˇs megtalĂˇlhatĂł-e a kĂłdban;
- a hĂ­vĂˇsi sorrend megfelel-e a vezĂ©rlĂ©snek;
- a visszatĂ©rĂ©si pontok Ă©s hibĂˇs Ăˇgak szerepelnek-e;
- az adatstruktĂşrĂˇk nevei egyeznek-e a kĂłddal.
- az A* diagram minden modulja Ă©s fĂĽggvĂ©nye tĂ©nylegesen megvalĂłsĂ­tott kĂłdhoz tartozik-e.

A flowchartot ne tekintsd automatikusan generĂˇltnak. KĂłdvĂˇltozĂˇs utĂˇn a dokumentumot a mĂłdosĂ­tĂˇst vĂ©gzĹ‘ munkamenetben kell ellenĹ‘rizni Ă©s frissĂ­teni.
```

### .github/skills/kodmagyarazat/SKILL.md

```markdown
---
name: kodmagyarazat
description: "Use for every detailed Hungarian code explanation, algorithm explanation, code-change explanation, class/function explanation, parameter or data-structure explanation, coordinate/resolution explanation, or request to save and keep explanations updated."
---

# EgyszerĹ±, kĂ¶vethetĹ‘ kĂłdmagyarĂˇzat Ă©s fejlesztĂ©si folyamat

## CĂ©l

MagyarĂˇzd el a kĂłdot magyarul, egyszerĹ±en, de ne tĂşl tĂ¶mĂ¶ren. Mindig a jelenlegi
fĂˇjlt olvasd el elĹ‘szĂ¶r; ne magyarĂˇzz feltĂ©telezett vagy rĂ©gi kĂłdot.

Ez a forma minden kĂłdra Ă©rvĂ©nyes, nem csak az A* modulokra. A magyarĂˇzat cĂ©lja,
hogy az olvasĂł a kĂłdot kĂ©sĹ‘bb Ă¶nĂˇllĂłan is kĂ¶vetni tudja, ne csak rĂ¶vid
fĂĽggvĂ©nylistĂˇt kapjon.
## KĂ¶telezĹ‘ fejlesztĂ©si sorrend

A projekt alapĂ©rtelmezett sorrendje:

```text
rĂˇcstĂ©rkĂ©p
-> klasszikus A*
-> alapmĂ©rĂ©sek Ă©s tesztek
-> A* vĂˇltozatok
-> Ăştvonal-simĂ­tĂˇs
-> kĂ­sĂ©rletek Ă©s Ă¶sszehasonlĂ­tĂˇs
-> kĂ©sĹ‘bbi SBA* vagy integrĂˇciĂłs Ăˇg
```

Ăšj kĂłdot ebbe a sorrendbe illesztve tervezz Ă©s magyarĂˇzz. ElĹ‘szĂ¶r legyen mĹ±kĂ¶dĹ‘ Ă©s tesztelt alap, csak utĂˇna jĂ¶jjĂ¶n optimalizĂˇlĂˇs vagy Ăşj algoritmus.

Ha a feladat eltĂ©r ettĹ‘l a sorrendtĹ‘l:

1. azonosĂ­tsd, melyik fejlesztĂ©si fĂˇzist Ă©rinti;
2. mĂłdosĂ­tsd a fejlesztĂ©si tervet, ha a sorrend tartĂłsan megvĂˇltozik;
3. a vĂˇltozĂˇst Ă­rd le rĂ¶viden az `ASTAR_FEJLESZTESI_TERV.md` fĂˇjlban;
4. az eltĂ©rĂ©st ne rejtsd el, hanem jelezd a magyarĂˇzatban Ă©s az ellenĹ‘rzĂ©sben.

## Munkamenet

1. Olvasd el a mĂłdosĂ­tott fĂˇjlt Ă©s a kĂ¶zvetlen teszteket vagy hasznĂˇlatokat.
2. Mondd ki rĂ¶viden, mi a fĂˇjl feladata Ă©s mi vĂˇltozik.
3. VĂ©gezd el a legkisebb szĂĽksĂ©ges kĂłdmĂłdosĂ­tĂˇst.
4. Futtass cĂ©lzott tesztet vagy mĂˇs gyors ellenĹ‘rzĂ©st.
5. A lezĂˇrĂˇs elĹ‘tt mindig vĂ©gezz konzisztencia-auditot: vesd Ă¶ssze a jelenlegi kĂłd tĂ©nyleges fĂĽggvĂ©nyneveit, paramĂ©tereit, visszatĂ©rĂ©si Ă©rtĂ©keit, adatfolyamĂˇt, algoritmusĂˇt Ă©s megjelenĂ­tĂ©sĂ©t a `codes_diploma/KODMAGYARAZATOK.md` Ă©rintett fejezeteivel Ă©s az `ASTAR_PROJEKT_FOLYAMATBRA.gv` ĂˇbrĂˇval.
6. Keresd meg Ă©s javĂ­tsd az elavult, tĂ¶rĂ¶lt vagy nem bizonyĂ­tott ĂˇllĂ­tĂˇsokat; kĂĽlĂ¶n ellenĹ‘rizd a hĂ­vĂˇsi sorrendet, a dĂ¶ntĂ©si Ăˇgakat, a kĂ©pleteket, a konkrĂ©t szĂˇmolĂˇsi pĂ©ldĂˇkat Ă©s a tesztparancsokat.
7. A frissĂ­tett magyarĂˇzat Ă©s folyamatĂˇbra csak akkor tekinthetĹ‘ kĂ©sznek, ha minden ĂˇllĂ­tĂˇs visszavezethetĹ‘ a jelenlegi kĂłdra vagy egy lefuttatott cĂ©lzott tesztre. Ha egy eltĂ©rĂ©s nem javĂ­thatĂł a jelenlegi munkamenetben, jelezd kĂĽlĂ¶n a lezĂˇrĂˇsban.
8. Csak sikeres kĂłd- Ă©s dokumentĂˇciĂłs ellenĹ‘rzĂ©s utĂˇn lĂ©pj tovĂˇbb a kĂ¶vetkezĹ‘ fĂˇzisra.

### KĂ¶telezĹ‘ kĂłdâ€“magyarĂˇzat ellenĹ‘rzĂ©s

Ezt az ellenĹ‘rzĂ©st minden rĂ©szletes magyar kĂłdmagyarĂˇzat, kĂłdmĂłdosĂ­tĂˇs Ă©s
magyarĂˇzat-frissĂ­tĂ©s vĂ©gĂ©n el kell vĂ©gezni, akkor is, ha a kĂłd nem vĂˇltozott.

- A magyarĂˇzatban szereplĹ‘ minden nyilvĂˇnos Ă©s fontos belsĹ‘ fĂĽggvĂ©nynĂ©v,
	paramĂ©ter Ă©s visszatĂ©rĂ©si forma egyezzen a jelenlegi fĂˇjllal.
- A leĂ­rt algoritmus, kĂ©plet, koordinĂˇta-ĂˇtalakĂ­tĂˇs, alapĂ©rtelmezett Ă©rtĂ©k Ă©s
	hibakezelĂ©s egyezzen a jelenlegi vĂ©grehajtĂˇssal.
- A magyarĂˇzatban szereplĹ‘ Ă¶sszes matematikai kĂ©pletet kĂĽlĂ¶n bontsd fel: nevezd
	meg minden vĂˇltozĂł jelentĂ©sĂ©t Ă©s mĂ©rtĂ©kegysĂ©gĂ©t, magyarĂˇzd el a mĹ±veletek
	sorrendjĂ©t kĂ¶zĂ©rthetĹ‘en, Ă©s adj hozzĂˇ legalĂˇbb egy konkrĂ©t behelyettesĂ­tĂ©si
	pĂ©ldĂˇt. KĂ©plet nem maradhat csak leĂ­rva vagy megnevezve magyarĂˇzat nĂ©lkĂĽl.
- A magyarĂˇzat ne tartalmazzon olyan felĂĽleti elemet, jelĂ¶lĂ©st, gombot,
	animĂˇciĂłs Ăˇllapotot vagy modult, amelyet a jelenlegi kĂłd mĂˇr nem hasznĂˇl.
- A folyamatĂˇbra hĂ­vĂˇsi sorrendjĂ©t Ă©s kapcsolatait is vesd Ă¶ssze a kĂłddal;
	hĂ­vĂˇsi sorrend, dĂ¶ntĂ©si Ăˇg vagy fontos adatkapcsolat eltĂ©rĂ©se esetĂ©n frissĂ­tsd.
- Futtasd a legszĹ±kebb Ă©rintett tesztet, majd ha tĂ¶bb modul vagy dokumentum
	Ă©rintett, a teljes relevĂˇns tesztcsomagot is.
- A lezĂˇrĂˇsban rĂ¶viden rĂ¶gzĂ­tsd, mit ellenĹ‘riztĂ©l, milyen parancs futott le, Ă©s
	maradt-e ismert eltĂ©rĂ©s vagy figyelmeztetĂ©s.

## MagyarĂˇzat tartalma

Minden tartĂłs kĂłdmagyarĂˇzatot az alĂˇbbi sorrendben Ă©pĂ­ts fel:

1. **A fĂˇjl cĂ©lja:** milyen problĂ©mĂˇt old meg Ă©s hol helyezkedik el a programban.
2. **Adatfolyam:** mi Ă©rkezik bemenetkĂ©nt, mi tĂ¶rtĂ©nik vele, Ă©s mi lesz a kimenet.
3. **Fontos adatok:** listĂˇk, szĂłtĂˇrak, objektumok, rĂˇcsok, koordinĂˇtĂˇk vagy Ăˇllapotok.
4. **FĂĽggvĂ©nyek Ă©s osztĂˇlyok:** cĂ©l, paramĂ©terek, visszatĂ©rĂ©si Ă©rtĂ©k Ă©s hibakezelĂ©s.
5. **Algoritmus vagy matematika:** a kĂ©pletet Ă©s a dĂ¶ntĂ©si logikĂˇt hĂ©tkĂ¶znapi nyelven is Ă­rd le.
6. **KonkrĂ©t szĂˇmolĂˇsi pĂ©lda:** kis, vĂ©gigszĂˇmolt bemenettel mutasd meg a mĹ±kĂ¶dĂ©st.
7. **BiztonsĂˇgi feltĂ©telek Ă©s korlĂˇtok:** mikor utasĂ­t el adatot, mikor tĂ©r vissza alapĂˇllapotba, Ă©s miĂ©rt.
8. **Kapcsolat Ă©s tesztelĂ©s:** melyik modul hĂ­vja, mitĹ‘l fĂĽgg, Ă©s milyen teszt ellenĹ‘rzi.

Ezek mellett tĂ©rj ki, amikor relevĂˇns:
- paramĂ©terek, visszatĂ©rĂ©si Ă©rtĂ©kek Ă©s hibĂˇk;
- adatszerkezetek Ă©s az A* adatfolyam;
- `g`, `h`, `f`, heurisztika Ă©s szomszĂ©dsĂˇg;
- rĂˇcskoordinĂˇta `(row, column)` Ă©s vilĂˇgkoordinĂˇta `(x, y)`;
- `resolution`, cellamĂ©ret, origĂł Ă©s koordinĂˇta-ĂˇtalakĂ­tĂˇs;
- legalĂˇbb egy kis, vĂ©gigszĂˇmolt pĂ©lda;
- a tĂ©nyleges jelenlegi kĂłd Ă©s az esetleges vizuĂˇlis megjelenĂ­tĂ©s kĂ¶zĂ¶tti kĂĽlĂ¶nbsĂ©g.

Ne csak soronkĂ©nt fordĂ­tsd le a kĂłdot. ElĹ‘szĂ¶r adj mĹ±kĂ¶dĂ©si kĂ©pet, utĂˇna bontsd
ki a fontos rĂ©szeket. A magyarĂˇzat legyen tagolt cĂ­msorokkal Ă©s rĂ¶vid
kĂłdrĂ©szletekkel, de ne legyen felsorolĂˇsbĂłl ĂˇllĂł, nehezen olvashatĂł kivonat.

Ne csak soronkĂ©nt fordĂ­tsd le a kĂłdot: elĹ‘szĂ¶r a mĹ±kĂ¶dĂ©si elkĂ©pzelĂ©st, utĂˇna a fontos rĂ©szleteket magyarĂˇzd el.

## TudĂˇsbĂˇzis hasznĂˇlata

Az `codes_diploma/tudasbazis.MD` Ă¶tlet- Ă©s hĂˇttĂ©rforrĂˇskĂ©nt hasznĂˇlhatĂł. SegĂ­thet heurisztikĂˇk, szomszĂ©dsĂˇgi szabĂˇlyok, Ăştvonal-simĂ­tĂˇsi mĂłdszerek Ă©s SBA* irĂˇnyok megĂ©rtĂ©sĂ©ben.

A tudĂˇsbĂˇzis nem helyettesĂ­ti a jelenlegi kĂłdot, a szakirodalmi ellenĹ‘rzĂ©st vagy a tesztet. Az onnan szĂˇrmazĂł Ă¶tletet kĂĽlĂ¶n, kis lĂ©pĂ©sben vezesd be; ne ĂˇllĂ­tsd mĹ±kĂ¶dĹ‘nek vagy bizonyĂ­tottnak addig, amĂ­g a kĂłd Ă©s a tesztek ezt nem igazoljĂˇk. A DWA-s anyagokat csak akkor hasznĂˇld, ha az aktuĂˇlis feladat kifejezetten az A* Ă©s DWA kapcsolatĂˇrĂłl szĂłl.

## MagyarĂˇzatok mentĂ©se Ă©s frissĂ­tĂ©se

A tartĂłs magyarĂˇzatokat a `codes_diploma/KODMAGYARAZATOK.md` fĂˇjl vĂ©gĂ©re Ă­rd,
Ăşj, szĂˇmozott fejezetkĂ©nt. ĂŤgy az Ăşj magyarĂˇzat nem keveredik Ă¶ssze a korĂˇbbi
fĂˇjlmagyarĂˇzatokkal.

Minden mĂłdosĂ­tott vagy rĂ©szletesen bemutatott fĂˇjlhez kĂ©szĂ­ts kĂĽlĂ¶n, kĂ¶zvetlenĂĽl
a kĂłdhoz tartozĂł magyarĂˇzati fejezetet. A fejezetben a jelenlegi kĂłd alatt,
olvashatĂł sorrendben szerepeljen a fĂˇjl cĂ©lja, az adatfolyam, a fĂĽggvĂ©nyek,
az algoritmus vagy kĂ©plet, egy konkrĂ©t szĂˇmolĂˇsi pĂ©lda, a biztonsĂˇgi korlĂˇtok
Ă©s a tesztelĂ©s. Ne elĂ©gedj meg egy rĂ¶vid Ă¶sszefoglalĂłval.

KĂłdmĂłdosĂ­tĂˇs utĂˇn ezt ugyanabban a munkamenetben kell elvĂ©gezni. A lezĂˇrĂˇs
elĹ‘tti ellenĹ‘rzĹ‘lista:

- a magyarĂˇzat a jelenlegi kĂłd fĂĽggvĂ©nyneveit hasznĂˇlja;
- nincs benne rĂ©gi vagy mĂˇr tĂ¶rĂ¶lt algoritmus;
- van legalĂˇbb egy konkrĂ©t szĂˇmolĂˇsi pĂ©lda;
- le van Ă­rva a bemenet, a kimenet Ă©s a hibĂˇs/veszĂ©lyes eset kezelĂ©se;
- szerepel a cĂ©lzott teszt parancsa Ă©s eredmĂ©nye;
- a magyarĂˇzat a `KODMAGYARAZATOK.md` vĂ©gĂ©n kĂĽlĂ¶n fejezetkĂ©nt megkereshetĹ‘.

MĹ±kĂ¶dĂ©st Ă©rintĹ‘ kĂłdmĂłdosĂ­tĂˇs utĂˇn ellenĹ‘rizd az Ă©rintett magyarĂˇzatot, Ă©s frissĂ­tsd, ha elavult. FormĂˇzĂˇsi vagy mĹ±kĂ¶dĂ©st nem Ă©rintĹ‘ vĂˇltozĂˇs miatt nem kell Ăşj magyarĂˇzatot Ă­rni.

Ha tĂ¶bb, egymĂˇssal Ă¶sszefĂĽggĹ‘ fĂˇjl vĂˇltozik, a magyarĂˇzatban kĂĽlĂ¶n nevezd meg
a hĂ­vĂˇsi sorrendet Ă©s azt, hogy melyik fĂˇjlban dĹ‘l el a viselkedĂ©s. Ne Ă­rj olyan
magyarĂˇzatot, amelyet a jelenlegi fĂˇjl vagy egy cĂ©lzott teszt nem tĂˇmaszt alĂˇ.
## StĂ­lus

- Magyarul, vilĂˇgosan Ă©s felesleges bonyolĂ­tĂˇs nĂ©lkĂĽl fogalmazz.
- HasznĂˇlj rĂ¶vid kĂłdrĂ©szleteket Ă©s konkrĂ©t szĂˇmolĂˇst.
- TĂĽntesd fel a mĂ©rtĂ©kegysĂ©geket.
- Ne ĂˇllĂ­ts olyat, amit a jelenlegi kĂłd, teszt vagy ellenĹ‘rzĂ¶tt forrĂˇs nem tĂˇmaszt alĂˇ.
```

### codes_diploma/ASTAR_FEJLESZTESI_TERV.md

```markdown
# A* ĂştvonaltervezĂ©s fejlesztĂ©si terve

## 0. A dokumentum cĂ©lja

Ez a dokumentum a szakdolgozati fejlesztĂ©s gyakorlati terve. A cĂ©l egy olyan Python-alapĂş kĂ­sĂ©rleti kĂ¶rnyezet lĂ©trehozĂˇsa, amelyben az A* algoritmus alap- Ă©s tovĂˇbbfejlesztett vĂˇltozatai azonos feltĂ©telek mellett vizsgĂˇlhatĂłk.

A kĂ©sĹ‘bbi cĂ©l az A* globĂˇlis ĂştvonaltervezĹ‘ Ă©s a DWA lokĂˇlis vezĂ©rlĹ‘ Ă¶sszekapcsolĂˇsa, majd az eredmĂ©ny ROS2/Gazebo kĂ¶rnyezetben tĂ¶rtĂ©nĹ‘ kiprĂłbĂˇlĂˇsa.

A fejlesztĂ©s fĹ‘ sorrendje:

```text
RĂˇcsos tĂ©rkĂ©p
    -> klasszikus A*
    -> ismert statikus tĂ©rkĂ©pes matplotlib-szimulĂˇciĂł
    -> tovĂˇbbfejlesztett A* vĂˇltozatok
    -> Ăştvonal-simĂ­tĂˇs
    -> mĂ©rĂ©si Ă©s Ă¶sszehasonlĂ­tĂˇsi rendszer
    -> A* + DWA Python-szimulĂˇciĂł
    -> ROS2 integrĂˇciĂł
    -> SBA* kĂĽlĂ¶n kutatĂˇsi Ăˇg
```

---

## 1. KiindulĂˇsi Ăˇllapot

### 1.1. MeglĂ©vĹ‘ Python DWA-szimulĂˇciĂł

A korĂˇbbi DWA-szimulĂˇciĂł mĂˇr tartalmazza:

- differenciĂˇlis hajtĂˇsĂş robotmodell;
- kerĂ©ksebessĂ©gbĹ‘l szĂˇmĂ­tott `v` Ă©s `w` Ă©rtĂ©keket;
- gyorsulĂˇskorlĂˇtozĂˇst;
- statikus Ă©s mozgĂł akadĂˇlyokat;
- biztonsĂˇgos sebessĂ©gpĂˇrok keresĂ©sĂ©t;
- trajektĂłria-elĹ‘rejelzĂ©st;
- ĂĽtkĂ¶zĂ©svizsgĂˇlatot;
- grafikus megjelenĂ­tĂ©st;
- paramĂ©tersĂ¶prĂ©st Ă©s CSV-mentĂ©st.

Ez jĂł alap a kĂ©sĹ‘bbi DWA-mĂ©rĂ©sekhez.

### 1.2. MeglĂ©vĹ‘ ROS2 DWA

A ROS2-es DWA-csomĂłpont jelenleg:

- LiDAR-adatokat olvas;
- odometriĂˇt Ă©s TF-transzformĂˇciĂłt hasznĂˇl;
- cĂ©lpozĂ­ciĂłt fogad;
- `cmd_vel` ĂĽzenetet publikĂˇl.

A Python-szimulĂˇciĂłhoz kĂ©pest azonban mĂ©g egyszerĹ±sĂ­tett:

- csak kevĂ©s sebessĂ©gĂ©rtĂ©ket vizsgĂˇl;
- nem teljes dinamikus ablakot hasznĂˇl;
- rĂ¶vid trajektĂłriĂˇk helyett lĂ©nyegĂ©ben egy elĹ‘re jelzett pozĂ­ciĂłt ellenĹ‘riz;
- nincs globĂˇlis A* Ăştvonal;
- nincs waypoint- vagy kulcspont-kĂ¶vetĂ©s.

EzĂ©rt az A* fejlesztĂ©st elĹ‘szĂ¶r kĂĽlĂ¶n Python-modulban kell megvalĂłsĂ­tani.

---

## 2. VĂ©gsĹ‘ rendszerarchitektĂşra

A tervezett rendszer hĂˇrom fĹ‘ rĂ©szbĹ‘l Ăˇll.

```text
Occupancy Grid / statikus tĂ©rkĂ©p
              |
              v
       GlobĂˇlis A* tervezĹ‘
              |
              v
       Teljes globĂˇlis Ăştvonal
              |
              v
       Kulcspont-kivĂˇlasztĂˇs
              |
              v
       LokĂˇlis DWA tervezĹ‘
              |
              v
             cmd_vel
```

### 2.1. A* feladata

Az A* a statikus vagy lassan vĂˇltozĂł tĂ©rkĂ©pen megkeresi a kezdĹ‘pont Ă©s a cĂ©lpont kĂ¶zĂ¶tti Ăştvonalat.

Az A* nem feladata:

- a robotsebessĂ©g kĂ¶zvetlen vezĂ©rlĂ©se;
- a dinamikus akadĂˇlyok pillanatnyi elkerĂĽlĂ©se;
- a `cmd_vel` kiadĂˇsa;
- a differenciĂˇlis hajtĂˇs teljes szimulĂˇciĂłja.

### 2.2. DWA feladata

A DWA a globĂˇlis Ăştvonal egy kĂ¶vetkezĹ‘ kulcspontjĂˇt kĂ¶veti, mikĂ¶zben:

- figyelembe veszi a robot aktuĂˇlis sebessĂ©gĂ©t;
- sebessĂ©gpĂˇrokat vagy `(v, w)` pĂˇrokat vizsgĂˇl;
- rĂ¶vid trajektĂłriĂˇkat szimulĂˇl;
- ellenĹ‘rzi az akadĂˇlyokat;
- betartja a gyorsulĂˇsi Ă©s fĂ©kezĂ©si korlĂˇtokat.

---

## 3. Javasolt projektstruktĂşra

Az A* kĂ­sĂ©rleti kĂłdot a `codes_diploma` mappĂˇn belĂĽl kĂĽlĂ¶n alkĂ¶nyvtĂˇrban Ă©rdemes tartani.

```text
codes_diploma/
    tudasbazis.MD
    DWA+A.py
    ASTAR_FEJLESZTESI_TERV.md
    astar_project/
        __init__.py
        grid_map.py
        astar_baseline.py
        astar_simulation.py
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
            test_astar_simulation.py
            test_path_smoothing.py
        results/
            raw/
            figures/
            tables/
```

A fĂˇjlok feladata:

| FĂˇjl | Feladat |
|---|---|
| `grid_map.py` | RĂˇcstĂ©rkĂ©p, cellĂˇk, akadĂˇlyok Ă©s robot-inflĂˇciĂł |
| `astar_baseline.py` | Klasszikus A* |
| `astar_simulation.py` | Ismert statikus tĂ©rkĂ©pes matplotlib-szimulĂˇciĂł |
| `astar_variants.py` | EA*, EBA*, EBHA*, EBHSA* vĂˇltozatok |
| `path_smoothing.py` | MĂˇsodfokĂş BĂ©zier-simĂ­tĂˇs rĂˇcsos akadĂˇlyellenĹ‘rzĂ©ssel |
| `scenarios.py` | TesztpĂˇlyĂˇk elĹ‘ĂˇllĂ­tĂˇsa |
| `metrics.py` | Ăštvonal- Ă©s teljesĂ­tmĂ©nymutatĂłk |
| `experiments.py` | IsmĂ©telt futtatĂˇsok Ă©s paramĂ©tersĂ¶prĂ©sek |
| `plots.py` | TĂ©rkĂ©pek, Ăştvonalak Ă©s Ă¶sszehasonlĂ­tĂł ĂˇbrĂˇk |
| `run_experiment.py` | Parancssoros belĂ©pĂ©si pont |
| `tests/` | Automatikus ellenĹ‘rzĂ©sek |

---

## 4. FejlesztĂ©si fĂˇzisok

## FĂˇzis 1: RĂˇcsos tĂ©rkĂ©pmodell

### Feladatok

1. 2D tĂ¶mb alapĂş occupancy grid lĂ©trehozĂˇsa.
2. Szabad Ă©s foglalt cellĂˇk kezelĂ©se.
3. KezdĹ‘- Ă©s cĂ©lpont validĂˇlĂˇsa.
4. PĂˇlyĂˇk kirajzolĂˇsa.
5. Robot- Ă©s akadĂˇlymĂ©ret figyelembevĂ©tele.

A robotot nem szabad egyetlen matematikai pontkĂ©nt kezelni, ha ĂĽtkĂ¶zĂ©sbiztonsĂˇgot szeretnĂ©nk vizsgĂˇlni. Az akadĂˇlyokat ki kell tĂˇgĂ­tani:

$$
r_{inflated} = r_{robot} + r_{obstacle} + r_{safety}
$$

### EllenĹ‘rzĂ©s

- A kezdĹ‘- Ă©s cĂ©lcella szabad.
- A tĂ©rkĂ©p megjelenik.
- A robot-inflĂˇciĂł utĂˇn sem kerĂĽl a kezdĹ‘ vagy cĂ©lcella akadĂˇlyba.

---

## FĂˇzis 2: Klasszikus A*

### Jelenlegi Ăˇllapot

Az elsĹ‘ referenciaimplementĂˇciĂł elkĂ©szĂĽlt az `astar_project/astar_baseline.py` fĂˇjlban. Az `astar_search` 4-szomszĂ©dos keresĂ©st Manhattan-heurisztikĂˇval, valamint opcionĂˇlis 8-szomszĂ©dos keresĂ©st diagonĂˇlis kĂ¶ltsĂ©ggel tĂˇmogat. A mĹ±kĂ¶dĂ©st cĂ©lzott `unittest` tesztek ellenĹ‘rzik: egyenes Ăşt, akadĂˇlykerĂĽlĂ©s, elĂ©rhetetlen cĂ©l, ĂˇtlĂłs mozgĂˇs Ă©s Ă©rvĂ©nytelen kezdĹ‘cella.

Ez mĂ©g a klasszikus referenciafĂˇzis rĂ©sze; tovĂˇbbfejlesztett heurisztika, irĂˇnyszĹ±rĂ©s Ă©s Ăştvonal-simĂ­tĂˇs csak ennek stabil ellenĹ‘rzĂ©se utĂˇn kĂ¶vetkezhet.

A referenciaalgoritmus Ă©rtĂ©kelĹ‘fĂĽggvĂ©nye:

$$
f(n) = g(n) + h(n)
$$

ahol:

- `g(n)` a kezdĹ‘ponttĂłl az aktuĂˇlis csomĂłpontig megtett kĂ¶ltsĂ©g;
- `h(n)` az aktuĂˇlis csomĂłpont Ă©s a cĂ©l kĂ¶zĂ¶tti heurisztikus becslĂ©s;
- `f(n)` a prioritĂˇsi Ă©rtĂ©k.

### ElsĹ‘kĂ©nt implementĂˇlandĂł vĂˇltozatok

1. 4-szomszĂ©dos keresĂ©s + Manhattan-heurisztika.
2. 8-szomszĂ©dos keresĂ©s + diagonĂˇlis kĂ¶ltsĂ©g.
3. 8-szomszĂ©dos keresĂ©s + Euklideszi heurisztika.

### Fontos adatok

Minden csomĂłpontnĂˇl tĂˇrolni kell:

```text
position
parent
g_cost
h_cost
f_cost
```

A prioritĂˇsi sorhoz min-heap hasznĂˇlata javasolt.

### EllenĹ‘rzĂ©s

- EgyszerĹ±, akadĂˇlymentes pĂˇlyĂˇn megtalĂˇlja az Ăştvonalat.
- AkadĂˇly esetĂ©n kerĂĽlĹ‘utat keres.
- ElĂ©rhetetlen cĂ©l esetĂ©n szabĂˇlyosan jelez.
- A visszafejtett Ăştvonal szomszĂ©dos cellĂˇkbĂłl Ăˇll.

## FĂˇzis 2.5: Ismert statikus tĂ©rkĂ©pes matplotlib-szimulĂˇciĂł

### CĂ©l

A klasszikus A* utĂˇn egy egyszerĹ±, vizuĂˇlisan ellenĹ‘rizhetĹ‘ szimulĂˇciĂł kĂ¶vetkezik. A szimulĂˇciĂł ismert, statikus rĂˇcstĂ©rkĂ©pet hasznĂˇl: az akadĂˇlyok mĂˇr a tervezĂ©s elĹ‘tt benne vannak a `GridMap` objektumban.

### MegvalĂłsĂ­tott fĂˇjl

Az `astar_project/astar_simulation.py`:

- lĂ©trehoz egy demo rĂˇcstĂ©rkĂ©pet statikus akadĂˇlyokkal;
- meghĂ­vja a klasszikus `astar_search` fĂĽggvĂ©nyt;
- a robotot egyszerĹ±, `0,08 m` sugarĂş kĂ¶rkĂ©nt jelenĂ­ti meg;
- a robot sugarĂˇval kitĂˇgĂ­tott akadĂˇlytĂ©rkĂ©pen tervezi az A* Ăştvonalat;
- az A* cellaĂştvonalĂˇt vilĂˇgkoordinĂˇtĂˇs cellakĂ¶zĂ©ppontokkĂˇ alakĂ­tja;
- ĂˇtlĂłs A* keresĂ©st hasznĂˇl, ezĂ©rt az akadĂˇlymentes rĂ©szeken nem csak derĂ©kszĂ¶gben tud haladni;
- megĹ‘rzi Ă©s animĂˇlja az A* Ăˇltal kibĹ‘vĂ­tett cellĂˇk sorrendjĂ©t;
- a szomszĂ©dos cellakĂ¶zĂ©ppontok kĂ¶zĂ¶tt egyszerĹ± robottrajektĂłriĂˇt kĂ©szĂ­t;
- matplotlibben kirajzolja a tĂ©rkĂ©pet, akadĂˇlyokat, A* Ăştvonalat Ă©s a robot nyomĂˇt;
- animĂˇlja a robot pontjĂˇt a tervezett Ăştvonalon.

Ez mĂ©g nem DWA Ă©s nem teljes fizikai robotmodell. A robot itt egyszerĹ± kĂ¶r alakĂş testkĂ©nt mozog a mĂˇr ismert globĂˇlis Ăştvonalon. A megjelenĂ­tĂ©s elĹ‘szĂ¶r a tervezĂ©si folyamatot, utĂˇna a robot mozgĂˇsĂˇt mutatja. Ez szĂˇndĂ©kos alapĂˇllapot: elĹ‘szĂ¶r azt ellenĹ‘rizzĂĽk, hogy a tĂ©rkĂ©p, az akadĂˇlyinflĂˇciĂł, az A* Ăştvonal, a vizsgĂˇlt cellĂˇk Ă©s a vizuĂˇlis mozgĂˇs egymĂˇssal helyesen kapcsolĂłdik-e.

### FuttatĂˇs

```text
python -m codes_diploma.astar_project.astar_simulation
```

### EllenĹ‘rzĂ©s

- A demo tĂ©rkĂ©pen lĂ©tezik Ăşt a start Ă©s a cĂ©l kĂ¶zĂ¶tt.
- Az Ăştvonal elsĹ‘ cellĂˇja a start, utolsĂł cellĂˇja a cĂ©l.
- Az Ăştvonal csak szabad cellĂˇkbĂłl Ăˇll.
- A robottrajektĂłria a start vilĂˇgkoordinĂˇtĂˇjĂˇrĂłl indul Ă©s a cĂ©l vilĂˇgkoordinĂˇtĂˇjĂˇn vĂ©gzĹ‘dik.
- A matplotlib Ăˇbra ablak lĂ©trehozhatĂł akkor is, ha a teszt nem jelenĂ­t meg ablakot.

---

## FĂˇzis 3: AlapmĂ©rĂ©si rendszer

Minden futĂˇsbĂłl legalĂˇbb az alĂˇbbi adatokat kell menteni:

| Metrika | JelentĂ©s |
|---|---|
| `success` | ElĂ©rte-e a cĂ©lpontot |
| `planning_time_ms` | TervezĂ©si idĹ‘ |
| `expanded_nodes` | KibĹ‘vĂ­tett csomĂłpontok szĂˇma |
| `visited_nodes` | MegvizsgĂˇlt csomĂłpontok szĂˇma |
| `path_length` | Ăštvonal hossza |
| `path_nodes` | Ăštvonal csomĂłpontjainak szĂˇma |
| `turn_count` | IrĂˇnyvĂˇltĂˇsok szĂˇma |
| `max_turn_angle` | Legnagyobb irĂˇnyvĂˇltozĂˇs |
| `map_id` | TesztpĂˇlya azonosĂ­tĂłja |
| `algorithm` | HasznĂˇlt algoritmus |

Az eredmĂ©nyeket CSV vagy Parquet formĂˇtumban kell menteni. A megjelenĂ­tĂ©shez PNG Ă©s SVG ĂˇbrĂˇk kĂ©szĂ­thetĹ‘k.

### EllenĹ‘rzĂ©s

Ugyanazt a tĂ©rkĂ©pet legalĂˇbb Ă¶tszĂ¶r kell lefuttatni, Ă©s ellenĹ‘rizni kell, hogy determinisztikus algoritmusnĂˇl az eredmĂ©nyek megegyeznek-e.

---

## FĂˇzis 4: EA* - Enhanced A*

Az EA* elnevezĂ©st csak akkor szabad vĂ©gleges szakirodalmi nĂ©vkĂ©nt hasznĂˇlni, ha hozzĂˇ tartozik konkrĂ©t publikĂˇciĂł Ă©s pontos definĂ­ciĂł.

A jelenlegi kĂ­sĂ©rleti tervben az EA* a klasszikus A* tovĂˇbbfejlesztett vĂˇltozata lehet:

- cĂ©lirĂˇnyos szomszĂ©dsĂˇgvizsgĂˇlat;
- redundĂˇns irĂˇnyok elhagyĂˇsa;
- javĂ­tott heurisztika;
- sarokvĂˇgĂˇs elleni vĂ©delem;
- opcionĂˇlis dinamikus heurisztikasĂşly.

A tudĂˇstĂˇrban szereplĹ‘ exponenciĂˇlis sĂşlyozĂˇs:

$$
P = \frac{|x_n-x_g|+|y_n-y_g|}{|x_s-x_g|+|y_s-y_g|}
$$

$$
f(n) = g(n) + e^P h(n)
$$

Ezt kĂĽlĂ¶n konfigurĂˇciĂłkĂ©nt kell vizsgĂˇlni, mert a sĂşlyozott heurisztika gyorsĂ­thatja a keresĂ©st, de nem feltĂ©tlenĂĽl Ĺ‘rzi meg a klasszikus A* optimĂˇlis ĂştvonalgaranciĂˇjĂˇt.

### MĂ©rendĹ‘ hatĂˇs

- csĂ¶kken-e a kibĹ‘vĂ­tett csomĂłpontok szĂˇma;
- csĂ¶kken-e a tervezĂ©si idĹ‘;
- vĂˇltozik-e az Ăştvonalhossz;
- nĹ‘-e a kanyarszĂˇm vagy csĂ¶kken-e.

---

## FĂˇzis 5: EBA* - kĂ©tirĂˇnyĂş vĂˇltozat

Az EBA* munkadefinĂ­ciĂłja:

- keresĂ©s a kezdĹ‘pontbĂłl Ă©s a cĂ©lpontbĂłl egyszerre;
- a kĂ©t keresĂ©si front talĂˇlkozĂˇsakor Ăştvonal-Ă¶sszekapcsolĂˇs;
- a klasszikus A* Ă©s az EA* eredmĂ©nyeivel valĂł Ă¶sszehasonlĂ­tĂˇs.

A kĂ©tirĂˇnyĂş keresĂ©snĂ©l kĂĽlĂ¶n ellenĹ‘rizni kell:

- valĂłban talĂˇlkozik-e a kĂ©t front;
- helyesen tĂ¶rtĂ©nik-e a szĂĽlĹ‘mutatĂłk Ă¶sszefĹ±zĂ©se;
- az Ă¶sszekĂ¶tĂ¶tt Ăştvonal nem tartalmaz-e Ă©rvĂ©nytelen Ăˇtmenetet;
- a megĂˇllĂˇsi feltĂ©tel nem rontja-e az Ăştvonal optimalitĂˇsĂˇt.

### MĂ©rendĹ‘ hatĂˇs

- keresĂ©si idĹ‘;
- kĂ©t irĂˇnyban kibĹ‘vĂ­tett csomĂłpontok szĂˇma;
- Ăştvonalhossz;
- memĂłriaigĂ©ny;
- sikertelen esetek arĂˇnya.

---

## FĂˇzis 6: EBHA* - heurisztikĂˇval tovĂˇbbfejlesztett kĂ©tirĂˇnyĂş A*

Az EBHA* munkadefinĂ­ciĂłja:

```text
EA* jellegĹ± heurisztika
    + kĂ©tirĂˇnyĂş keresĂ©s
    + irĂˇnyfĂĽggĹ‘ vagy dinamikus prioritĂˇs
```

A heurisztika vĂˇltoztatĂˇsait kĂĽlĂ¶n kell kapcsolhatĂłvĂˇ tenni. Nem cĂ©lszerĹ± egyszerre beĂ©pĂ­teni a szomszĂ©dsĂˇgcsĂ¶kkentĂ©st, a dinamikus sĂşlyozĂˇst Ă©s a kĂ©tirĂˇnyĂş keresĂ©st, mert akkor nem lesz megĂˇllapĂ­thatĂł, melyik mĂłdosĂ­tĂˇs okozza az eredmĂ©nyt.

Javasolt kĂ­sĂ©rleti sorrend:

```text
A*
A* + dinamikus heurisztika
A* + szomszĂ©dsĂˇgoptimalizĂˇlĂˇs
EBA*
EBHA*
```

---

## FĂˇzis 7: EBHSA* - simĂ­tĂˇssal kiegĂ©szĂ­tett vĂˇltozat

Az EBHSA* munkadefinĂ­ciĂłja:

```text
EBHA*
    + kollineĂˇris pontok tĂ¶rlĂ©se
    + akadĂˇlymentes inflection bypass
```

A simĂ­tĂˇst kĂĽlĂ¶n utĂłfeldolgozĂˇskĂ©nt kell megvalĂłsĂ­tani, nem kĂ¶zvetlenĂĽl a keresĂ©si ciklusban.

### KollineĂˇris pont tĂ¶rlĂ©se

Ha hĂˇrom egymĂˇst kĂ¶vetĹ‘ pont azonos irĂˇnyban fekszik, a kĂ¶zĂ©psĹ‘ pont tĂ¶rĂ¶lhetĹ‘.

### Inflection bypass

Ha kĂ©t tĂ¶rĂ©spont kĂ¶zvetlenĂĽl Ă¶sszekĂ¶thetĹ‘ akadĂˇlymentesen, Ă©s a kĂ¶zvetlen szakasz rĂ¶videbb, mint az eredeti rĂ©szĂşt, akkor a kĂ¶ztes pontok eltĂˇvolĂ­thatĂłk.

### KĂ¶telezĹ‘ biztonsĂˇgi feltĂ©tel

A simĂ­tĂˇs utĂˇn minden Ăşj szakaszt Ăşjra ĂĽtkĂ¶zĂ©svizsgĂˇlattal kell ellenĹ‘rizni.

---

## 5. TesztpĂˇlyĂˇk

LegalĂˇbb az alĂˇbbi pĂˇlyĂˇkat kell lĂ©trehozni:

1. akadĂˇlymentes tĂ©r;
2. egyetlen akadĂˇly;
3. tĂ¶bb akadĂˇly;
4. U alakĂş akadĂˇly;
5. szĹ±k folyosĂł;
6. zsĂˇkutca;
7. tĂ¶bb azonos hosszĂşsĂˇgĂş kerĂĽlĹ‘Ăşt;
8. sĹ±rĹ± akadĂˇlymezĹ‘;
9. dinamikus akadĂˇlyokat tartalmazĂł pĂˇlya a kĂ©sĹ‘bbi DWA-vizsgĂˇlathoz.

Minden algoritmust ugyanazon tĂ©rkĂ©peken kell futtatni, azonos kezdĹ‘- Ă©s cĂ©lponttal.

---

## 6. KĂ­sĂ©rleti mĂˇtrix

A minimĂˇlis Ă¶sszehasonlĂ­tĂˇs:

```text
A*
EA*
EBA*
EBHA*
EBHSA*
```

A kĂ©sĹ‘bbi hibrid Ă¶sszehasonlĂ­tĂˇs:

```text
A* + DWA
EA* + DWA
EBA* + DWA
EBHA* + DWA
EBHSA* + DWA
```

Minden kombinĂˇciĂł esetĂ©n azonos legyen:

- tĂ©rkĂ©p;
- kezdĹ‘pont;
- cĂ©lpont;
- robotmĂ©ret;
- biztonsĂˇgi margĂł;
- DWA sebessĂ©gkorlĂˇtja;
- DWA elĹ‘retekintĂ©si ideje;
- akadĂˇlylista;
- mĂ©rĂ©si idĹ‘szak.

---

## 7. A* Ă©s DWA Ă¶sszekapcsolĂˇsa

A globĂˇlis A* Ăştvonalat a DWA nem teljes egĂ©szĂ©ben, hanem kulcspontokon keresztĂĽl kĂ¶veti.

Egy waypoint akkor teljesĂ­tett, ha:

$$
\sqrt{(x-x_w)^2+(y-y_w)^2} < \varepsilon_w
$$

A vezĂ©rlĂ©si ciklus logikĂˇja:

```text
1. RobotpozĂ­ciĂł frissĂ­tĂ©se
2. AktuĂˇlis waypoint kivĂˇlasztĂˇsa
3. DWA sebessĂ©gpĂˇrok generĂˇlĂˇsa
4. TrajektĂłriĂˇk szimulĂˇciĂłja
5. ĂśtkĂ¶zĂ©s- Ă©s fĂ©kezĂ©si feltĂ©telek ellenĹ‘rzĂ©se
6. Legjobb trajektĂłria kivĂˇlasztĂˇsa
7. cmd_vel kiadĂˇsa
8. Waypoint teljesĂ­tĂ©sĂ©nek ellenĹ‘rzĂ©se
9. SzĂĽksĂ©g esetĂ©n globĂˇlis ĂşjratervezĂ©s
```

GlobĂˇlis ĂşjratervezĂ©s szĂĽksĂ©ges lehet, ha:

- a tĂ©rkĂ©p megvĂˇltozik;
- a cĂ©lpont elĂ©rhetetlennĂ© vĂˇlik;
- a DWA tartĂłsan holtpontba kerĂĽl;
- a robot jelentĹ‘sen eltĂ©r a globĂˇlis ĂştvonaltĂłl.

---

## 8. DWA tovĂˇbbfejlesztĂ©se az A* utĂˇn

### 8.1. ElkĂ©szĂĽlt elsĹ‘ robotmag

Az elsĹ‘ integrĂˇciĂłs lĂ©pĂ©sben a robotra vonatkozĂł, ROS2-tĹ‘l Ă©s MatplotlibtĹ‘l
fĂĽggetlen rĂ©szek kĂ©t jĂłl elkĂĽlĂ¶nĂ­tett fĂˇjlba kerĂĽltek:

| Modul | FelelĹ‘ssĂ©g |
|---|---|
| `robot.py` | robotĂˇllapot, robotparamĂ©terek, kinematika, akadĂˇly Ă©s ĂˇllapotfrissĂ­tĂ©s |
| `DWA.py` | dinamikus ablak, szenzoros akadĂˇlyvizsgĂˇlat, fĂ©kezĂ©si feltĂ©tel Ă©s pontozĂˇs |
| `DWA+A.py` | A* rĂˇcsĂştvonal, legfeljebb `3 * resolution` BĂ©zier-simĂ­tĂˇs, waypoint-kĂ¶vetĂ©s Ă©s DWA-vezĂ©rlĂ©s |
| `simulation.py` | A* mintĂˇjĂş Matplotlib animĂˇciĂł lĂˇthatĂł rĂˇcscellĂˇkkal, waypointokkal Ă©s statikus/mozgĂł akadĂˇlyokkal |

A robotmag az eredeti, mĂˇr hasznĂˇlt neveket tartja meg: `robotstate`,
`robotconfig`, `Obstacle`, `Goal`, `update`, `safepairs` Ă©s `optimisation`.
A ROS2-node kĂ©sĹ‘bb ezeket tĂ¶lti fel odometriĂˇbĂłl Ă©s LiDAR-bĂłl, majd a `best_pair` Ă©rtĂ©keit Ă­rja
`geometry_msgs/Twist` ĂĽzenetbe.

A jelenlegi hĂ­vĂˇsi sorrend:

```text
GridMap + start/goal vilĂˇgkoordinĂˇta
        -> AStarDWAPlanner.plan_global()
        -> astar_search()
        -> rĂˇcsĂştvonal -> vilĂˇgkoordinĂˇtĂˇs waypointok
        -> AStarDWAPlanner.plan_local() a DWA+A.py fĂˇjlban
        -> Goal(aktuĂˇlis waypoint)
        -> optimisation(config, state, goal, obstacles)
        -> best_pair = [v, w, w_L, w_R]
```

Az elsĹ‘ prototĂ­pus mĂˇr fogad egyenletesen mozgĂł akadĂˇlyt is (`vx`, `vy`), de
az akadĂˇlyok pĂˇlyĂˇrĂłl valĂł ki- Ă©s belĂ©pĂ©sĂ©t, a LiDAR-zaj kezelĂ©sĂ©t Ă©s a
globĂˇlis ĂşjratervezĂ©st mĂ©g kĂĽlĂ¶n fĂˇzisban kell megvalĂłsĂ­tani. A mozgĂł akadĂˇly
elĹ‘rejelzĂ©se nem teszi a globĂˇlis A* tĂ©rkĂ©pet dinamikussĂˇ; az A* tovĂˇbbra is
statikus vagy pillanatfelvĂ©telkĂ©nt frissĂ­tett rĂˇcson dolgozik.

### 8.2. RobotparamĂ©terek elsĹ‘ konfigurĂˇciĂłja

Az alapĂ©rtĂ©kek a meglĂ©vĹ‘ Matplotlib DWA robotmodelljĂ©nek Ă©rtĂ©keit kĂ¶vetik:

| ParamĂ©ter | AlapĂ©rtĂ©k | MĂ©rtĂ©kegysĂ©g |
|---|---:|---|
| `wheel_radius` | `0.033` | m |
| `axle_track` | `0.08` | m |
| `max_wheel_speed` | `15` | rad/s |
| `max_wheel_acceleration` | `2 / 0.033` | rad/sÂ˛ |
| `control_period` | `0.1` | s |
| `prediction_horizon` | `3.0` | s |
| `robot_radius` | `0.10` | m |
| `safety_margin` | `0.15` | m |

PĂ©ldĂˇul azonos, `10 rad/s` kerĂ©ksebessĂ©gnĂ©l a lineĂˇris sebessĂ©g:

$$
v = r\frac{\omega_L+\omega_R}{2}
    = 0{,}033\frac{10+10}{2}
    = 0{,}33\ \mathrm{m/s}
$$

Itt `r` a kerĂ©k sugara, `omega_L` Ă©s `omega_R` a bal Ă©s jobb kerĂ©k
szĂ¶gsebessĂ©ge. Mivel a kĂ©t kerĂ©k egyformĂˇn forog, az `omega` szĂ¶gsebessĂ©g
nulla, tehĂˇt a robot egyenes vonalban halad.

### 8.3. EllenĹ‘rzĂ©s

Az Ăşj robotmag tesztjei:

```text
python -m unittest codes_diploma.astar_project.tests.test_robot_and_dwa codes_diploma.astar_project.tests.test_dwa_a
```

Ezek ellenĹ‘rzik az eredeti robotparamĂ©tereket, a kinematikĂˇt, a mozgĂł akadĂˇly
kezelĂ©sĂ©t, az `optimisation()` kimenetĂ©t Ă©s az A* Ăştvonal waypointokkĂˇ
alakĂ­tĂˇsĂˇt.

A Python DWA-szimulĂˇciĂłban megtartandĂł elemek:

- differenciĂˇlis hajtĂˇsmodell;
- kerĂ©ksebessĂ©gbĹ‘l szĂˇmĂ­tott mozgĂˇs;
- gyorsulĂˇskorlĂˇtozĂˇs;
- fĂ©kezĂ©si feltĂ©tel;
- trajektĂłria-rollout;
- mozgĂł akadĂˇlyok elĹ‘rejelzĂ©se;
- paramĂ©tersweep.

A kĂ©sĹ‘bbi integrĂˇciĂłhoz mĂłdosĂ­tani kell:

- a cĂ©lpontot az aktuĂˇlis waypoint adja;
- a heading pontszĂˇm a globĂˇlis Ăştvonal irĂˇnyĂˇt is vegye figyelembe;
- legyen ĂştvonaltĂłl valĂł oldaltĂˇvolsĂˇg-pontszĂˇm;
- a DWA ne menjen a globĂˇlis Ăştvonal biztonsĂˇgi sĂˇvjĂˇn kĂ­vĂĽlre, ha ez nem szĂĽksĂ©ges.

---

## 9. SBA* kĂ©sĹ‘bbi kutatĂˇsi ĂˇgkĂ©nt

Az SBA* nem az elsĹ‘ implementĂˇciĂł rĂ©sze. KĂĽlĂ¶n modulban kĂ©szĂĽljĂ¶n, mert eltĂ©rĹ‘ problĂ©mĂˇt old meg:

- folytonos ĂˇllapottĂ©r;
- mintavĂ©telezĂ©s;
- lokĂˇlis elĂ©rhetĹ‘sĂ©g;
- `STEER` mĹ±velet;
- folytonos ĂĽtkĂ¶zĂ©svizsgĂˇlat;
- Ăşj csomĂłpont valĂłszĂ­nĹ±sĂ©gi Ă©rtĂ©kelĂ©se;
- sĹ±rĹ±sĂ©gi Ă©s szĹ±kĂĽleti Ăˇllapotok.

A javasolt sorrend:

```text
klasszikus A*
    -> tovĂˇbbfejlesztett diszkrĂ©t A*
    -> A* + DWA
    -> SBA* kĂĽlĂ¶n Python-szimulĂˇciĂł
    -> SBA* Ă©s lokĂˇlis vezĂ©rlĹ‘ integrĂˇciĂłja
```

---

## 10. Szakdolgozati kutatĂˇsi kĂ©rdĂ©sek

1. CsĂ¶kkenti-e a tovĂˇbbfejlesztett szomszĂ©dsĂˇgvizsgĂˇlat a kibĹ‘vĂ­tett csomĂłpontok szĂˇmĂˇt?
2. CsĂ¶kkenti-e a dinamikus heurisztika a tervezĂ©si idĹ‘t?
3. Milyen hatĂˇssal van a heurisztika mĂłdosĂ­tĂˇsa az Ăştvonal optimĂˇlis hosszĂˇra?
4. JavĂ­tja-e a kĂ©tirĂˇnyĂş keresĂ©s a nagyobb tĂ©rkĂ©peken a futĂˇsi idĹ‘t?
5. CsĂ¶kkenti-e az Ăştvonal-simĂ­tĂˇs a kanyarszĂˇmot Ă©s az irĂˇnyvĂˇltozĂˇsok Ă¶sszegĂ©t?
6. JavĂ­tja-e az EBHSA* Ăştvonala a DWA kĂ¶vetĂ©si stabilitĂˇsĂˇt?
7. Melyik globĂˇlis A* vĂˇltozat adja a legjobb kompromisszumot Ăştvonalhossz, tervezĂ©si idĹ‘ Ă©s DWA-kĂ¶vethetĹ‘sĂ©g kĂ¶zĂ¶tt?
8. Hogyan vĂˇltozik a teljesĂ­tmĂ©ny statikus Ă©s dinamikus akadĂˇlyok mellett?

---

## 11. Javasolt elsĹ‘ konkrĂ©t munkamenet

### ElsĹ‘ lĂ©pĂ©s

KĂ©szĂ­tsd el a `GridMap` osztĂˇlyt:

- szĂ©lessĂ©g;
- magassĂˇg;
- cellamĂ©ret;
- akadĂˇlycellĂˇk;
- kezdĹ‘pont;
- cĂ©lpont;
- cella szabad/akadĂˇly lekĂ©rdezĂ©se.

### MĂˇsodik lĂ©pĂ©s

ImplementĂˇld a klasszikus A*-t Manhattan-heurisztikĂˇval.

### Harmadik lĂ©pĂ©s

KĂ©szĂ­ts egy egyszerĹ± ĂˇbrĂˇt, amelyen lĂˇthatĂł:

- akadĂˇlyok;
- kezdĹ‘pont;
- cĂ©lpont;
- kibĹ‘vĂ­tett csomĂłpontok;
- vĂ©gsĹ‘ Ăştvonal.

### Negyedik lĂ©pĂ©s

Adj hozzĂˇ mĂ©rĂ©si adatokat:

- futĂˇsi idĹ‘;
- kibĹ‘vĂ­tett csomĂłpontok;
- Ăştvonalhossz;
- kanyarszĂˇm.

### Ă–tĂ¶dik lĂ©pĂ©s

Csak ezutĂˇn kezdd el az EA* elsĹ‘ mĂłdosĂ­tĂˇsĂˇt.

---

## 12. ForrĂˇsok Ă©s forrĂˇskezelĂ©s

A rĂ¶vidĂ­tĂ©sek hasznĂˇlata elĹ‘tt minden algoritmushoz fel kell venni:

- teljes algoritmusnĂ©v;
- szerzĹ‘k;
- Ă©v;
- DOI vagy stabil URL;
- pontos pszeudokĂłd;
- mĂłdosĂ­tott kĂ©plet;
- optimĂˇlis vagy kĂ¶zelĂ­tĹ‘ jelleg;
- sajĂˇt implementĂˇciĂłs eltĂ©rĂ©sek.

Fontos kiindulĂł forrĂˇsok:

- Hart, Nilsson Ă©s Raphael: *A Formal Basis for the Heuristic Determination of Minimum Cost Paths*, DOI: `10.1109/TSSC.1968.300136`.
- Liu, Wang, Wu Ă©s Wei: *Mobile Robot Path Planning Based on Kinematically Constrained A-Star Algorithm and DWA Fusion Algorithm*, DOI: `10.3390/math11214552`.
- Fox, Burgard Ă©s Thrun: *The Dynamic Window Approach to Collision Avoidance*, DOI: `10.1109/100.580977`.

Az `EA*`, `EBA*`, `EBHA*` Ă©s `EBHSA*` rĂ¶vidĂ­tĂ©sekhez kĂĽlĂ¶n, ellenĹ‘rzĂ¶tt bibliogrĂˇfiai forrĂˇst kell rĂ¶gzĂ­teni, vagy vilĂˇgosan sajĂˇt kĂ­sĂ©rleti elnevezĂ©skĂ©nt kell megadni Ĺ‘ket.

---

## 13. ElkĂ©szĂĽltnek tekinthetĹ‘ mĂ©rfĂ¶ldkĂ¶vek

### MĂ©rfĂ¶ldkĹ‘ 1

A klasszikus A* legalĂˇbb hĂˇrom pĂˇlyĂˇn helyes Ăştvonalat ad.

### MĂ©rfĂ¶ldkĹ‘ 2

Az A* eredmĂ©nyei automatikusan CSV-be menthetĹ‘k.

### MĂ©rfĂ¶ldkĹ‘ 3

Az EA*, EBA*, EBHA* Ă©s EBHSA* ugyanazzal a mĂ©rĂ©si rendszerrel futtathatĂł.

### MĂ©rfĂ¶ldkĹ‘ 4

Az Ăştvonal-simĂ­tĂˇs utĂˇn minden szakasz ĂĽtkĂ¶zĂ©smentes marad.

### MĂ©rfĂ¶ldkĹ‘ 5

A Python DWA egy A* Ăˇltal generĂˇlt waypoint-listĂˇt kĂ¶vet.

### MĂ©rfĂ¶ldkĹ‘ 6

Az A*â€“DWA rendszer dinamikus akadĂˇlyos szimulĂˇciĂłban is mĂ©rhetĹ‘.

### MĂ©rfĂ¶ldkĹ‘ 7

A legjobb vĂˇltozat ROS2/Gazebo kĂ¶rnyezetben is futtathatĂł.

---

## 14. RĂ¶vid dĂ¶ntĂ©si szabĂˇlyok fejlesztĂ©s kĂ¶zben

- ElĹ‘szĂ¶r mindig legyen mĹ±kĂ¶dĹ‘ referencia-A*.
- Egyszerre csak egy algoritmikus mĂłdosĂ­tĂˇst vezess be.
- Minden vĂˇltozat ugyanazon pĂˇlyĂˇkon fusson.
- A gyorsabb algoritmus nem automatikusan jobb algoritmus.
- Az Ăştvonalhossz Ă©s a tervezĂ©si idĹ‘ mellett a kanyarszĂˇmot is mĂ©rni kell.
- A simĂ­tĂˇs csak Ăşj ĂĽtkĂ¶zĂ©svizsgĂˇlat utĂˇn fogadhatĂł el.
- A globĂˇlis A* Ă©s a lokĂˇlis DWA felelĹ‘ssĂ©gĂ©t kĂĽlĂ¶n kell tartani.
- Az SBA* csak a diszkrĂ©t A* validĂˇciĂłja utĂˇn kĂ¶vetkezzen.
```

### codes_diploma/astar_project/__init__.py

```python
```

### codes_diploma/astar_project/astar_baseline.py

```python
"""Klasszikus A* ĂştvonaltervezĂ©s rĂˇcstĂ©rkĂ©pen."""

import math


def _heuristic(position, goal, diagonal, heuristic=None):
	"""Heurisztikus becslĂ©st ad a pozĂ­ciĂł Ă©s a cĂ©l kĂ¶zĂ¶tt."""
	if heuristic is not None:
		return heuristic(position, goal)

	row, column = position
	goal_row, goal_column = goal
	row_distance = abs(goal_row - row)
	column_distance = abs(goal_column - column)

	if diagonal:
		return math.sqrt(row_distance ** 2 + column_distance ** 2)

	return row_distance + column_distance


def _movement_cost(current, neighbor):
	"""Megadja kĂ©t szomszĂ©dos cella mozgĂˇsi kĂ¶ltsĂ©gĂ©t."""
	row_change = abs(neighbor[0] - current[0])
	column_change = abs(neighbor[1] - current[1])
	return math.sqrt(row_change ** 2 + column_change ** 2)


def _reconstruct_path(came_from, current):
	"""A cĂ©lcellĂˇtĂłl visszalĂ©pve Ă¶sszeĂˇllĂ­tja a startig vezetĹ‘ utat."""
	path_from_goal = [current]

	while current in came_from:
		previous_position = came_from[current]
		path_from_goal.append(previous_position)
		current = previous_position

	path_from_goal.reverse()
	return path_from_goal


def astar_search(
	grid_map,
	start,
	goal,
	diagonal=False,
	return_details=False,
	heuristic=None,
):
	"""Megkeresi a legkisebb kĂ¶ltsĂ©gĹ± utat a start Ă©s a cĂ©l kĂ¶zĂ¶tt."""
 
	if not grid_map.is_inside(*start) or not grid_map.is_inside(*goal):
		raise ValueError("A start Ă©s a cĂ©l a tĂ©rkĂ©pen belĂĽl legyen.")
	if not grid_map.is_free(*start) or not grid_map.is_free(*goal):
		raise ValueError("A start Ă©s a cĂ©l szabad cella legyen.")

	open_list = [(_heuristic(start, goal, diagonal, heuristic), 0.0, start)]	#heurisztika Ă©rtĂ©ke, g kĂ¶ltsĂ©g, pozĂ­ciĂł

	came_from = {}	#lista a szĂĽlĹ‘ pozĂ­ciĂłkhoz
	g_costs = {start: 0.0}	#az egyes pozĂ­ciĂłkhoz tartozĂł g kĂ¶ltsĂ©gek
	expanded_nodes = []	#csomĂłpontokhoz tartozĂł lista, a hozzĂˇfĂ©rhetĹ‘ csomopontokhoz
	search_steps = []	#a lĂ©pĂ©seket tarolja a kereses folyaman

	while open_list:	#amig van open stĂˇtuszban csomĂłpont addig csinĂˇlja
		best_node = min(open_list)	#legjobb node kivĂˇlasztĂˇsa f kĂ¶ltsĂ©g alapjĂˇn
		open_list.remove(best_node)	#kiveszi a legjobb nodeot
		current_g_cost = best_node[1]	#g kĂ¶ltsĂ©g a legjobb nodehoz
		current_position = best_node[2]	#pozĂ­ciĂł a legjobb nodehoz

		if current_g_cost > g_costs[current_position]:	#ha a g kĂ¶ltsĂ©g nagyobb mint a tĂˇrolt g kĂ¶ltsĂ©g akkor nem kell tovĂˇbb vizsgĂˇlni
			continue

		expanded_nodes.append(current_position)	# mĂˇr feldolgozott csomĂłpontokhoz hozzĂˇadja a jelenlegi pozĂ­ciĂłt

		if current_position == goal:
			path = _reconstruct_path(came_from, current_position)
			if return_details:
				return {
					"path": path,
					"expanded_nodes": expanded_nodes,
					"search_steps": search_steps,
				}
			return path

		neighbors = grid_map.get_neighbors(current_position[0], current_position[1], diagonal)	 #szomszĂ©dos cellĂˇk lekĂ©rĂ©se a grid_mapbĹ‘l, ahol [0] a sor, [1] az oszlop
		neighbor_scores = []	#a szomszĂ©dos cellĂˇkhoz tartozĂł f, g, h kĂ¶ltsĂ©gek
		for neighbor in neighbors:	#a szomszĂ©dos cellĂˇkhoz tartozĂł f, g, h kĂ¶ltsĂ©gek kiszĂˇmĂ­tĂˇsa
			movement_cost = _movement_cost(current_position, neighbor)	#mozgĂˇs kĂ¶ltsĂ©ge a jelenlegi Ă©s a szomszĂ©dos pozĂ­ciĂł kĂ¶zĂ¶tt
			new_g_cost = current_g_cost + movement_cost	#g kĂ¶ltsĂ©g a szomszĂ©dokhoz
			h_cost = _heuristic(neighbor, goal, diagonal, heuristic)	#h kĂ¶ltsĂ©g a szomszĂ©dokhoz
			f_cost = new_g_cost + h_cost	#f kĂ¶ltsĂ©g a szomszĂ©dokhoz
			accepted = new_g_cost < g_costs.get(neighbor, math.inf)	#ha a szomszĂ©dos cella g kĂ¶ltsĂ©ge kisebb mint a tĂˇrolt g kĂ¶ltsĂ©g akkor elfogadja a szomszĂ©dos cellĂˇt

			if return_details:
				neighbor_scores.append(	
					{
						"position": neighbor,
						"g": new_g_cost,
						"h": h_cost,
						"f": new_g_cost + h_cost,
						"accepted": accepted,
					}
				)

			if not accepted:
				continue

			came_from[neighbor] = current_position	#a szomszĂ©dos cella szĂĽlĹ‘ pozĂ­ciĂłja a jelenlegi pozĂ­ciĂł
			g_costs[neighbor] = new_g_cost	#szomszĂ©dos cella g kĂ¶ltsĂ©ge a jelenlegi g kĂ¶ltsĂ©g + mozgĂˇs kĂ¶ltsĂ©g
			f_cost = new_g_cost + h_cost	#szomszĂ©dos cella f kĂ¶ltsĂ©ge a jelenlegi g kĂ¶ltsĂ©g + h kĂ¶ltsĂ©g
			open_list.append((f_cost, new_g_cost, neighbor))	#szomszĂ©dos cella hozzĂˇadĂˇsa az open listĂˇhoz a f kĂ¶ltsĂ©g, g kĂ¶ltsĂ©g Ă©s pozĂ­ciĂł alapjĂˇn

		if not return_details:
			continue

		
		current_h_cost = _heuristic(current_position, goal, diagonal, heuristic)	# a jelenlegi pozĂ­ciĂł h kĂ¶ltsĂ©ge
		search_steps.append(	#hozzĂˇadja a keresĂ©si lĂ©pĂ©sekhez a jelenlegi pozĂ­ciĂłt, szomszĂ©dos cellĂˇkat, g kĂ¶ltsĂ©get, h kĂ¶ltsĂ©get, f kĂ¶ltsĂ©get Ă©s szomszĂ©dos cellĂˇkhoz tartozĂł f, g, h kĂ¶ltsĂ©geket
			{
				"current": current_position,
				"neighbors": neighbors,
				"current_g": current_g_cost,
				"current_h": current_h_cost,
				"current_f": current_g_cost + current_h_cost,
				"neighbor_scores": neighbor_scores,
			}
		)

		valid_open_nodes = []
		for entry in open_list:
			stored_g_cost = entry[1]
			position = entry[2]
			best_known_g_cost = g_costs.get(position, math.inf)

			if stored_g_cost <= best_known_g_cost:
				valid_open_nodes.append(entry)

		# Az Ă©rvĂ©nyes tuple-Ă¶kbĹ‘l olvashatĂł szĂłtĂˇrakat kĂ©szĂ­tĂĽnk a megjelenĂ­tĂ©shez.
		priority_queue = [
			{
				"position": position,  # A vĂˇrakozĂł node cellakoordinĂˇtĂˇja.
				"g": cost,  # A starttĂłl eddig vezetĹ‘ Ăşt kĂ¶ltsĂ©ge.
				"h": priority - cost,  # A cellĂˇtĂłl a cĂ©lig becsĂĽlt kĂ¶ltsĂ©g: h = f - g.
				"f": priority,  # A teljes becsĂĽlt kĂ¶ltsĂ©g: f = g + h.
			}
			# A sorted tuple-jeibĹ‘l rendre az f, g Ă©s pozĂ­ciĂł Ă©rtĂ©keket vesszĂĽk ki.
			for priority, cost, position in sorted(valid_open_nodes)
		]
		search_steps[-1]["priority_queue"] = priority_queue  # A -1 az utolsĂł keresĂ©si lĂ©pĂ©st jelenti.
		search_steps[-1]["next_position"] = (min(valid_open_nodes)[2] if valid_open_nodes else None)  # A legkisebb f-kĂ¶ltsĂ©gĹ± kĂ¶vetkezĹ‘ pozĂ­ciĂł, vagy None.

	if return_details:
		return {
			"path": None,
			"expanded_nodes": expanded_nodes,
			"search_steps": search_steps,
		}

	return None


# A priority_queue blokk mĹ±kĂ¶dĂ©se rĂ©szletesen:
#
# 1. A valid_open_nodes elemei tuple-Ă¶k:
#
#        (f_kĂ¶ltsĂ©g, g_kĂ¶ltsĂ©g, pozĂ­ciĂł)
#
#    PĂ©ldĂˇul:
#
#        [
#            (7.0, 3.0, (2, 4)),
#            (6.0, 4.0, (1, 5)),
#        ]
#
# 2. A sorted(valid_open_nodes) rendezi ezeket a tuple-Ă¶ket. ElsĹ‘kĂ©nt az
#    f-kĂ¶ltsĂ©get hasonlĂ­tja Ă¶ssze, ezĂ©rt a kisebb f-kĂ¶ltsĂ©gĹ± node kerĂĽl elĹ‘re.
#    Ebben a pĂ©ldĂˇban a (6.0, 4.0, (1, 5)) node lesz az elsĹ‘.
#
# 3. A list comprehension minden tuple-bĹ‘l egy szĂłtĂˇrat kĂ©szĂ­t. Ez azĂ©rt
#    hasznos, mert a szĂłtĂˇr kulcsai alapjĂˇn kĂ©sĹ‘bb kĂ¶nnyebb megjelenĂ­teni Ă©s
#    Ă©rtelmezni az adatokat:
#
#        {
#            "position": (1, 5),
#            "g": 4.0,
#            "h": 2.0,
#            "f": 6.0,
#        }
#
#    A for ciklus vĂˇltozĂłi a tuple elemeit jelentik:
#    - priority: az entry[0], vagyis az f-kĂ¶ltsĂ©g;
#    - cost: az entry[1], vagyis a g-kĂ¶ltsĂ©g;
#    - position: az entry[2], vagyis a cella pozĂ­ciĂłja.
#
# 4. A h-kĂ¶ltsĂ©get a kĂłd nem tĂˇrolta kĂĽlĂ¶n a valid_open_nodes tuple-ben.
#    Mivel f = g + h, ezĂ©rt vissza lehet szĂˇmolni:
#
#        h = f - g
#        h = priority - cost
#
#    A pĂ©ldĂˇban:
#
#        h = 6.0 - 4.0 = 2.0
#
# 5. A search_steps[-1] az utolsĂłkĂ©nt lĂ©trehozott keresĂ©si lĂ©pĂ©s szĂłtĂˇra.
#    A priority_queue kulcs alĂˇ bekerĂĽl az aktuĂˇlis kĂ¶rben mĂ©g vĂˇrakozĂł node-ok
#    listĂˇja, Ă­gy ezt a szimulĂˇciĂł kĂ©sĹ‘bb meg tudja jelenĂ­teni.
#
# 6. A next_position meghatĂˇrozĂˇsa:
#
#        min(valid_open_nodes)[2]
#
#    A min kivĂˇlasztja a legkisebb tuple-t, tehĂˇt elsĹ‘sorban a legkisebb
#    f-kĂ¶ltsĂ©gĹ± node-ot. A [2] ezutĂˇn csak a pozĂ­ciĂłt veszi ki belĹ‘le.
#    Ha nincs Ă©rvĂ©nyes vĂˇrakozĂł node, akkor a feltĂ©teles kifejezĂ©s None Ă©rtĂ©ket
#    ad vissza:
#
#        next_position = (1, 5)
#        vagy
#        next_position = None
#
# 7. A return_details kapcsolĂł dĂ¶nti el, hogy ezek a rĂ©szletes adatok
#    visszakerĂĽlnek-e a hĂ­vĂł kĂłdhoz. Ha True, az eredmĂ©ny egy szĂłtĂˇr:
#
#        {
#            "path": ...,             # megtalĂˇlt Ăşt vagy None
#            "expanded_nodes": ...,   # mĂˇr feldolgozott cellĂˇk
#            "search_steps": ...,     # a keresĂ©s minden rĂ©szletes lĂ©pĂ©se
#        }
#
#    Ha return_details False, a fĂĽggvĂ©ny csak az Ăştvonalat vagy sikertelen
#    keresĂ©s esetĂ©n None Ă©rtĂ©ket ad vissza, a rĂ©szletes megjelenĂ­tĂ©si adatokra
#    nincs szĂĽksĂ©g.


# ---------------------------------------------------------------------------
# ADATSTRUKTĂšRAI ĂTTEKINTĂ‰S AZ A* ALGORITMUSHOZ
# ---------------------------------------------------------------------------
# Ebben a megvalĂłsĂ­tĂˇsban a "node" nem kĂĽlĂ¶n osztĂˇly vagy objektum, hanem
# egy tuple, amely hĂˇrom adatot tartalmaz:
#
#     (f_kĂ¶ltsĂ©g, g_kĂ¶ltsĂ©g, pozĂ­ciĂł)
#
# PĂ©lda egy node-ra:
#
#     (7.0, 3.0, (2, 4))
#
# A tuple elemei:
# - entry[0] = f-kĂ¶ltsĂ©g = g-kĂ¶ltsĂ©g + h-kĂ¶ltsĂ©g.
#   Ezt hasznĂˇlja az A* annak eldĂ¶ntĂ©sĂ©re, melyik node legyen a kĂ¶vetkezĹ‘.
# - entry[1] = g-kĂ¶ltsĂ©g, vagyis a startcellĂˇtĂłl az adott cellĂˇig megtett Ăşt
#   eddigi kĂ¶ltsĂ©ge.
# - entry[2] = position, vagyis a cella (sor, oszlop) koordinĂˇtĂˇja.
#
# A pĂ©ldĂˇban:
# - f = 7.0;
# - g = 3.0;
# - h = f - g = 7.0 - 3.0 = 4.0;
# - position = (2, 4), tehĂˇt a cella a 2. sorban Ă©s a 4. oszlopban van.
#
# A fontosabb A* adatszerkezetek felĂ©pĂ­tĂ©se:
#
# 1. open_list
#    Azokat a node-okat tartalmazza, amelyeket az algoritmus mĂ©g nem dolgozott
#    fel teljesen. Egy lista pĂ©ldĂˇul Ă­gy nĂ©zhet ki:
#
#        [
#            (7.0, 3.0, (2, 4)),
#            (6.5, 4.5, (1, 5)),
#        ]
#
#    Az elsĹ‘ elem az f-kĂ¶ltsĂ©g, a mĂˇsodik a g-kĂ¶ltsĂ©g, a harmadik a pozĂ­ciĂł.
#    A min(open_list) a legkisebb tuple-t vĂˇlasztja ki, ezĂ©rt elsĹ‘sorban az
#    f-kĂ¶ltsĂ©g alapjĂˇn keresĂĽnk, egyezĂ©s esetĂ©n pedig a tovĂˇbbi tuple-elemek
#    alapjĂˇn dĂ¶nt a Python.
#
# 2. g_costs
#    Egy szĂłtĂˇr, amely minden mĂˇr felfedezett cellĂˇhoz eltĂˇrolja az eddig
#    ismert legjobb g-kĂ¶ltsĂ©get:
#
#        {
#            (2, 4): 3.0,
#            (1, 5): 4.5,
#        }
#
#    A (2, 4): 3.0 azt jelenti, hogy a startcellĂˇtĂłl a (2, 4) cellĂˇig jelenleg
#    ismert legolcsĂłbb Ăşt kĂ¶ltsĂ©ge 3.0.
#
# 3. came_from
#    A cellĂˇk szĂĽlĹ‘cellĂˇjĂˇt tĂˇrolja. Ez kell ahhoz, hogy a cĂ©l elĂ©rĂ©sekor az
#    algoritmus vissza tudja Ă©pĂ­teni az Ăştvonalat:
#
#        {
#            (2, 4): (2, 3),
#            (2, 3): (1, 3),
#        }
#
#    Ez azt jelenti, hogy a (2, 4) cellĂˇba a (2, 3) cellĂˇbĂłl Ă©rkeztĂĽnk.
#
# 4. valid_open_nodes
#    Az open_list megtisztĂ­tott vĂˇltozata. Ugyanaz a cella tĂ¶bb alkalommal is
#    bekerĂĽlhet az open_list-be, ha kĂ©sĹ‘bb olcsĂłbb Ăşton talĂˇljuk meg. A rĂ©gi,
#    drĂˇgĂˇbb node ilyenkor elavult. A szĹ±rĂ©s csak azt tartja meg, amelynek a
#    g-kĂ¶ltsĂ©ge mĂ©g megfelel a g_costs szĂłtĂˇrban tĂˇrolt legjobb Ă©rtĂ©knek.
#
#    PĂ©lda:
#
#        open_list: [(8.0, 5.0, (2, 4)), (7.0, 3.0, (2, 4))]
#        g_costs:   {(2, 4): 3.0}
#
#    A g = 5.0 Ă©rtĂ©kĹ± rĂ©gi node kiesik, a g = 3.0 Ă©rtĂ©kĹ± aktuĂˇlis node marad.
#
# 5. priority_queue
#    A valid_open_nodes elemeit kĂ¶nnyebben olvashatĂł szĂłtĂˇrakkĂˇ alakĂ­tja:
#
#        {
#            "position": (2, 4),
#            "g": 3.0,
#            "h": 4.0,
#            "f": 7.0,
#        }
#
#    Itt a h-kĂ¶ltsĂ©g kĂĽlĂ¶n is megjelenik, amely az open_list tuple-jĂˇban nem
#    szerepel kĂ¶zvetlenĂĽl, mert kiszĂˇmĂ­thatĂł az f - g kĂ©plettel.
#
# 6. search_steps
#    A search_steps egy lista, amely a keresĂ©s kĂ¶zben lĂ©trejĂ¶vĹ‘ lĂ©pĂ©seket
#    tĂˇrolja. Egy listaelem egy olyan szĂłtĂˇr, amely egyetlen feldolgozott
#    aktuĂˇlis cella teljes ĂˇllapotĂˇt Ă­rja le.
#
#    Egy search_steps elem felĂ©pĂ­tĂ©se:
#
#        {
#            "current": (2, 3),
#            "neighbors": [(1, 3), (2, 4)],
#            "current_g": 2.0,
#            "current_h": 4.0,
#            "current_f": 6.0,
#            "neighbor_scores": [
#                {
#                    "position": (1, 3),
#                    "g": 3.0,
#                    "h": 3.0,
#                    "f": 6.0,
#                    "accepted": True,
#                }
#            ],
#            "priority_queue": [
#                {
#                    "position": (1, 3),
#                    "g": 3.0,
#                    "h": 3.0,
#                    "f": 6.0,
#                }
#            ],
#            "next_position": (1, 3),
#        }
#
#    A mezĹ‘k jelentĂ©se:
#    - current: az a cella, amelyet az A* algoritmus ebben a kĂ¶rben feldolgoz.
#    - neighbors: a current cella szabad Ă©s elĂ©rhetĹ‘ szomszĂ©dai.
#    - current_g: a startcellĂˇtĂłl a current cellĂˇig ismert Ăşt kĂ¶ltsĂ©ge.
#    - current_h: a current cellĂˇtĂłl a cĂ©lig becsĂĽlt kĂ¶ltsĂ©g.
#    - current_f: current_g + current_h; ezt hasznĂˇlja az A* a rangsorolĂˇshoz.
#    - neighbor_scores: minden szomszĂ©dhoz kiszĂˇmĂ­tott g, h Ă©s f Ă©rtĂ©kek listĂˇja.
#    - accepted: True, ha a szomszĂ©dhoz talĂˇlt Ăşj Ăşt olcsĂłbb a korĂˇbbinĂˇl,
#      ezĂ©rt a szomszĂ©d bekerĂĽlhet az open_list-be.
#    - priority_queue: az adott kĂ¶r utĂˇn Ă©rvĂ©nyes, mĂ©g feldolgozĂˇsra vĂˇrĂł
#      node-ok kĂ¶nnyebben olvashatĂł formĂˇban.
#    - next_position: az a kĂ¶vetkezĹ‘ cella, amelyet az A* a legkisebb f alapjĂˇn
#      vĂˇrhatĂłan kivĂˇlaszt. Ha nincs tĂ¶bb node, az Ă©rtĂ©ke None.
#
#    A search_steps lista Ă­gy Ă©pĂĽl fel:
#
#        search_steps = [
#            elsĹ‘ keresĂ©si lĂ©pĂ©s szĂłtĂˇra,
#            mĂˇsodik keresĂ©si lĂ©pĂ©s szĂłtĂˇra,
#            harmadik keresĂ©si lĂ©pĂ©s szĂłtĂˇra,
#            ...,
#        ]
#
#    A ciklus minden feldolgozott current cella utĂˇn lĂ©trehoz egy Ăşj szĂłtĂˇrat,
#    majd a priority_queue Ă©s a next_position adatait ugyanebbe a szĂłtĂˇrba
#    Ă­rja bele. EzutĂˇn a szĂłtĂˇr bekerĂĽl a search_steps lista vĂ©gĂ©re.
#
#    PĂ©ldĂˇul:
#
#        search_steps[0]
#
#    a keresĂ©s elsĹ‘ feldolgozĂˇsi kĂ¶rĂ©nek adatait jelenti, mĂ­g a
#
#        search_steps[1]
#
#    a mĂˇsodik kĂ¶r adatait. A szimulĂˇciĂł ezt hasznĂˇlja arra, hogy a keresĂ©st
#    lĂ©pĂ©senkĂ©nt, animĂˇciĂłs kĂ©pkockĂˇk formĂˇjĂˇban meg tudja jelenĂ­teni.
#
# Az adatok mĹ±kĂ¶dĂ©si sorrendje rĂ¶viden:
#
#     szomszĂ©dos cella
#       -> g, h Ă©s f kĂ¶ltsĂ©g kiszĂˇmĂ­tĂˇsa
#       -> (f, g, position) hozzĂˇadĂˇsa az open_list-hez
#       -> jobb Ăşt esetĂ©n g_costs frissĂ­tĂ©se
#       -> elavult node-ok kiszĹ±rĂ©se valid_open_nodes segĂ­tsĂ©gĂ©vel
#       -> priority_queue lĂ©trehozĂˇsa az ĂˇttekinthetĹ‘ megjelenĂ­tĂ©shez


# ---------------------------------------------------------------------------
# A valid_open_nodes szĹ±rĂ©sĂ©nek rĂ©szletes magyarĂˇzata
# ---------------------------------------------------------------------------
#
# A programban az open_list elemei hĂˇrom adatot tartalmazĂł tuple-Ă¶k:
#
#     (f_kĂ¶ltsĂ©g, g_kĂ¶ltsĂ©g, pozĂ­ciĂł)
#
# PĂ©ldĂˇul:
#
#     (8.0, 5.0, (2, 4))
#
# Ez azt jelenti, hogy a (2, 4) cellĂˇhoz a startcellĂˇtĂłl eddig ismert Ăşt
# kĂ¶ltsĂ©ge 5.0. Az f-kĂ¶ltsĂ©g 8.0, amely a g- Ă©s h-kĂ¶ltsĂ©g Ă¶sszege:
#
#     f = g + h
#
# A kĂłd az open_list minden elemĂ©t egyenkĂ©nt megvizsgĂˇlja:
#
#     valid_open_nodes = []
#     for entry in open_list:
#         stored_g_cost = entry[1]
#         position = entry[2]
#         best_known_g_cost = g_costs.get(position, math.inf)
#
#         if stored_g_cost <= best_known_g_cost:
#             valid_open_nodes.append(entry)
#
# Az entry az open_list egyik tuple-je. Az entry[1] az ebben a tuple-ben
# tĂˇrolt g-kĂ¶ltsĂ©g, az entry[2] pedig a cella pozĂ­ciĂłja.
#
# A g_costs szĂłtĂˇr minden mĂˇr felfedezett cellĂˇhoz eltĂˇrolja a jelenleg
# ismert legjobb g-kĂ¶ltsĂ©get. PĂ©ldĂˇul:
#
#     g_costs = {
#         (2, 4): 3.0
#     }
#
# Ez azt jelenti, hogy a (2, 4) cellĂˇhoz jelenleg ismert legolcsĂłbb Ăşt kĂ¶ltsĂ©ge
# 3.0.
#
# Ugyanaz a cella tĂ¶bbszĂ¶r is bekerĂĽlhet az open_list-be. Ez akkor tĂ¶rtĂ©nik,
# ha az A* elĹ‘szĂ¶r egy drĂˇgĂˇbb, majd kĂ©sĹ‘bb egy olcsĂłbb Ăştvonalat talĂˇl hozzĂˇ.
# PĂ©ldĂˇul:
#
#     open_list = [
#         (8.0, 5.0, (2, 4)),
#         (6.0, 3.0, (2, 4)),
#     ]
#
#     g_costs = {
#         (2, 4): 3.0
#     }
#
# Az elsĹ‘ bejegyzĂ©s elavult, mert a benne lĂ©vĹ‘ g-kĂ¶ltsĂ©g 5.0, mikĂ¶zben mĂˇr
# ismert egy 3.0 kĂ¶ltsĂ©gĹ± Ăşt ugyanahhoz a cellĂˇhoz:
#
#     5.0 <= 3.0  -> False
#
# EzĂ©rt ez az elem nem kerĂĽl bele a valid_open_nodes listĂˇba.
#
# A mĂˇsodik bejegyzĂ©s Ă©rvĂ©nyes, mert az Ăˇltala tĂˇrolt g-kĂ¶ltsĂ©g megegyezik
# a jelenleg ismert legjobb Ă©rtĂ©kkel:
#
#     3.0 <= 3.0  -> True
#
# EzĂ©rt bekerĂĽl a valid_open_nodes listĂˇba.
#
# A valid_open_nodes tehĂˇt az open_list megtisztĂ­tott vĂˇltozata: csak azok a
# bejegyzĂ©sek maradnak benne, amelyek mĂ©g a cellĂˇhoz ismert legjobb Ăştvonalat
# kĂ©pviselik. Az eredeti open_list ettĹ‘l nem vĂˇltozik, a program csak egy Ăşj
# listĂˇt kĂ©szĂ­t a mĂ©g Ă©rvĂ©nyes elemekbĹ‘l.
#
# Ez a szĹ±rt lista a priority_queue lĂ©trehozĂˇsĂˇhoz Ă©s a megjelenĂ­tĂ©shez kell.
# A priority_queue mĂˇr olvashatĂł szĂłtĂˇrakkĂˇ alakĂ­tja ezeket az elemeket, Ă©s
# kĂĽlĂ¶n megjelenĂ­ti a cella pozĂ­ciĂłjĂˇt, valamint a g, h Ă©s f kĂ¶ltsĂ©geket.


# ---------------------------------------------------------------------------
# 				Az A* teljes mĹ±kĂ¶dĂ©sĂ©nek rĂ¶vid, vĂ©gigkĂ¶vetett pĂ©ldĂˇja
# ---------------------------------------------------------------------------
#
# PĂ©lda:
#
#     rĂˇcsmĂ©ret: 3 oszlop x 2 sor
#     start:     (0, 0)
#     cĂ©l:       (1, 2)
#     akadĂˇly:   nincs
#     diagonal:  False
#
# A cellĂˇkat (sor, oszlop) formĂˇban jelĂ¶ljĂĽk. ĂtlĂłs mozgĂˇs nĂ©lkĂĽl egy lĂ©pĂ©s
# kĂ¶ltsĂ©ge 1. A Manhattan-heurisztika kĂ©plete:
#
#     h = abs(cĂ©l_sor - sor) + abs(cĂ©l_oszlop - oszlop)
#
# 1. KezdĹ‘Ăˇllapot
#
# Az algoritmus lĂ©trehozza az ĂĽres adatszerkezeteket, majd a startcellĂˇt
# beteszi az open_list-be:
#
#     open_list = [(3.0, 0.0, (0, 0))]
#     g_costs = {(0, 0): 0.0}
#     came_from = {}
#     expanded_nodes = []
#     search_steps = []
#
# A startcellĂˇnĂˇl g = 0.0, a cĂ©lig becsĂĽlt h = 3.0, ezĂ©rt f = g + h = 3.0.
#
# 2. A startcellĂˇt kivĂˇlasztjuk, majd kivesszĂĽk az open_list-bĹ‘l
#
# IndulĂˇskor az open_list-ben mĂ©g csak a startcellĂˇhoz tartozĂł node van:
#
#     open_list = [(3.0, 0.0, (0, 0))]
#
# Ez a node nem a semmibĹ‘l kerĂĽlt a listĂˇba: az algoritmus a keresĂ©s elejĂ©n
# kĂ©szĂ­ti el a startcellĂˇbĂłl. A tuple elemei rendre az f-kĂ¶ltsĂ©g, a g-kĂ¶ltsĂ©g
# Ă©s a pozĂ­ciĂł. A startnĂˇl g = 0.0, mert mĂ©g nem tettĂĽnk meg lĂ©pĂ©st.
#
# A min(open_list) kivĂˇlasztja a legkisebb f-kĂ¶ltsĂ©gĹ± node-ot. Ezt a node-ot
# a program eltĂˇvolĂ­tja az open_list-bĹ‘l, majd current_position nĂ©ven kezdi
# feldolgozni:
#
#     best_node = (3.0, 0.0, (0, 0))
#     open_list = []
#     current_position = (0, 0)
#
# EzutĂˇn a startcellĂˇt feldolgozott cellakĂ©nt eltĂˇroljuk:
#
#     expanded_nodes = [(0, 0)]
#
# 3. A start szomszĂ©dainak felderĂ­tĂ©se Ă©s az open_list feltĂ¶ltĂ©se
#
# A program ezutĂˇn lekĂ©ri a current_position, vagyis (0, 0) szabad szomszĂ©dait:
#
#     (1, 0) Ă©s (0, 1)
#
# Ezek mĂ©g nem voltak benne az open_list-ben. A for ciklus mindkĂ©t szomszĂ©dra
# kiszĂˇmĂ­tja a mozgĂˇsi kĂ¶ltsĂ©get, az Ăşj g-kĂ¶ltsĂ©get, a h-kĂ¶ltsĂ©get Ă©s az
# f-kĂ¶ltsĂ©get. MindkĂ©t cellĂˇhoz 1.0 kĂ¶ltsĂ©ggel jutunk el, majd a program
# eltĂˇrolja a szĂĽlĹ‘t Ă©s a legjobb ismert g-kĂ¶ltsĂ©get:
#
#     came_from = {
#         (1, 0): (0, 0),
#         (0, 1): (0, 0),
#     }
#
#     g_costs = {
#         (0, 0): 0.0,
#         (1, 0): 1.0,
#         (0, 1): 1.0,
#     }
#
# EzutĂˇn az Ăşj node-ok bekerĂĽlnek az open_list-be az open_list.append(...) sorral.
# MindkettĹ‘ f-kĂ¶ltsĂ©ge 3.0:
#
#     open_list = [
#         (3.0, 1.0, (1, 0)),
#         (3.0, 1.0, (0, 1)),
#     ]
#
# EzutĂˇn lĂ©trejĂ¶n a search_steps elsĹ‘ eleme. Ez csak akkor tĂ¶rtĂ©nik meg, ha a
# return_details Ă©rtĂ©ke True. A program egy szĂłtĂˇrban elmenti az imĂ©nt lezajlott
# feldolgozĂˇsi kĂ¶rt:
#
#     search_steps[0] = {
#         "current": (0, 0),
#         "neighbors": [(1, 0), (0, 1)],
#         "current_g": 0.0,
#         "current_h": 3.0,
#         "current_f": 3.0,
#         "neighbor_scores": [...],
#     }
#
# A current azt mutatja, melyik cellĂˇt dolgoztuk fel. A neighbors az elĂ©rhetĹ‘
# szomszĂ©dokat tartalmazza. A current_g, current_h Ă©s current_f az aktuĂˇlis
# cella kĂ¶ltsĂ©gei. A neighbor_scores kĂĽlĂ¶n leĂ­rja, hogy a program mit szĂˇmolt
# ki mindkĂ©t szomszĂ©dra, Ă©s elfogadta-e Ĺ‘ket.
#
# EzutĂˇn a program a mĂˇr frissĂ­tett open_list-bĹ‘l lĂ©trehozza a valid_open_nodes
# listĂˇt, majd a priority_queue-t. Ez nem egy Ăşj keresĂ©si lista, hanem az
# open_list megjelenĂ­tĂ©shez ĂˇtalakĂ­tott vĂˇltozata:
#
#     priority_queue = [
#         {"position": (1, 0), "g": 1.0, "h": 2.0, "f": 3.0},
#         {"position": (0, 1), "g": 1.0, "h": 2.0, "f": 3.0},
#     ]
#
# A priority_queue azokat a node-okat mutatja, amelyek mĂˇr bekerĂĽltek az
# open_list-be, de mĂ©g nem kerĂĽltek feldolgozĂˇsra. Az f-kĂ¶ltsĂ©g szerint vannak
# rendezve, ezĂ©rt ebbĹ‘l lĂˇthatĂł, hogy a kĂ¶vetkezĹ‘ kĂ¶rben melyik node lehet a
# kĂ¶vetkezĹ‘ kivĂˇlasztott elem. A priority_queue Ă©s a next_position adatait a
# program ugyanabba a search_steps[0] szĂłtĂˇrba Ă­rja bele.
#
# 4. A kĂ¶vetkezĹ‘ cella kivĂˇlasztĂˇsa Ă©s feldolgozĂˇsa
#
# Az elĹ‘zĹ‘ lĂ©pĂ©s vĂ©gĂ©n az open_list kĂ©t node-ot tartalmazott. MindkĂ©t node
# f = 3.0 Ă©s g = 1.0 Ă©rtĂ©kĹ± volt. A min(open_list) kivĂˇlasztja kĂ¶zĂĽlĂĽk a
# kĂ¶vetkezĹ‘ node-ot. Azonos f Ă©s g esetĂ©n a tuple tovĂˇbbi elemei alapjĂˇn
# tĂ¶rtĂ©nik a rendezĂ©s, ezĂ©rt a pĂ©ldĂˇban a (0, 1) cella kerĂĽl sorra:
#
#     best_node = (3.0, 1.0, (0, 1))
#     open_list = [(3.0, 1.0, (1, 0))]
#
# A (0, 1) cella ekkor kikerĂĽl a vĂˇrakozĂł listĂˇbĂłl, Ă©s bekerĂĽl az
# expanded_nodes listĂˇba:
#
#     expanded_nodes = [(0, 0), (0, 1)]
#
# EzutĂˇn a program lekĂ©ri a (0, 1) szabad szomszĂ©dait. Ezek a tĂ©rkĂ©p Ă©s a
# get_neighbors irĂˇny-sorrendje alapjĂˇn:
#
#     (1, 1), (0, 2), (0, 0)
#
# A for ciklus ezeket egymĂˇs utĂˇn vizsgĂˇlja. A (1, 1) Ă©s a (0, 2) cellĂˇt most
# talĂˇlja meg elĹ‘szĂ¶r, ezĂ©rt a g_costs mĂ©g nem tartalmaz hozzĂˇjuk Ă©rtĂ©ket. Az
# Ăşj Ăşt mindkĂ©t cellĂˇhoz olcsĂłbbnak szĂˇmĂ­t a kezdeti vĂ©gtelen Ă©rtĂ©knĂ©l, ezĂ©rt
# accepted = True lesz, Ă©s mindkĂ©t node bekerĂĽl az open_list-be.
#
# A (0, 0) cellĂˇt viszont mĂˇr korĂˇbban feldolgoztuk. A jelenlegi cellĂˇbĂłl oda
# vezetĹ‘ Ăşj Ăşt kĂ¶ltsĂ©ge 2.0 lenne, de a g_costs szerint a startcellĂˇhoz mĂˇr
# 0.0 kĂ¶ltsĂ©ggel eljutottunk. EzĂ©rt az Ăşj Ăşt nem jobb:
#
#     (0, 0): Ăşj g = 2.0, rĂ©gi g = 0.0 -> accepted = False
#
# Emiatt a (0, 0) node-hoz nem frissĂĽl a came_from vagy a g_costs, Ă©s nem kerĂĽl
# Ăşjra az open_list-be. A kĂ©t elfogadott szomszĂ©d viszont bekerĂĽl az adatokba:
#
#     came_from[(1, 1)] = (0, 1)
#     came_from[(0, 2)] = (0, 1)
#     g_costs[(1, 1)] = 2.0
#     g_costs[(0, 2)] = 2.0
#
# A kĂ©t Ăşj node bekerĂĽl az open_list-be. A feldolgozĂˇs Ăˇllapota bekerĂĽl a
# search_steps mĂˇsodik elemĂ©be.
#
# 5. Olyan node feldolgozĂˇsa, amely nem lesz a vĂ©gsĹ‘ Ăşt rĂ©sze
#
# A kĂ¶vetkezĹ‘ kivĂˇlasztott cella (1, 0). Ez is bekerĂĽl az expanded_nodes listĂˇba:
#
#     expanded_nodes = [(0, 0), (0, 1), (1, 0)]
#
# Innen a (1, 1) cellĂˇhoz vezetĹ‘ Ăşj Ăşt kĂ¶ltsĂ©ge szintĂ©n 2.0 lenne. Mivel a
# g_costs mĂˇr tartalmazza a (1, 1): 2.0 Ă©rtĂ©ket, az Ăşj jelĂ¶lt nem jobb:
#
#     Ăşj g = 2.0, ismert g = 2.0 -> accepted = False
#
# Ez a lĂ©pĂ©s bekerĂĽl a search_steps listĂˇba, de (1, 0) vĂ©gĂĽl nem kerĂĽl bele
# a path listĂˇba. Ez mutatja a kĂĽlĂ¶nbsĂ©get a keresĂ©s kĂ¶zben feldolgozott Ă©s a
# vĂ©gsĹ‘ Ăştvonalhoz tartozĂł cellĂˇk kĂ¶zĂ¶tt.
#
# 6. A cĂ©l elĂ©rhetĹ‘vĂ© vĂˇlik az open_list-ben
#
# A (0, 2) cella feldolgozĂˇsakor a cĂ©l (1, 2) szomszĂ©dkĂ©nt megjelenik:
#
#     Ăşj g = 3.0
#     h = 0.0
#     f = 3.0
#
# Mivel a cĂ©lhoz eddig nem tartozott g_costs Ă©rtĂ©k, a program elfogadja:
#
#     came_from[(1, 2)] = (0, 2)
#     g_costs[(1, 2)] = 3.0
#
# A cĂ©l bekerĂĽl az open_list-be, de ekkor mĂ©g nincs benne az expanded_nodes-ban.
# ElĹ‘szĂ¶r vĂˇrakozĂł node, Ă©s csak akkor lesz expanded node, amikor kivesszĂĽk.
#
# 7. A priority_queue Ă©s a valid_open_nodes szerepe
#
# A program az open_list-bĹ‘l lĂ©trehozza a valid_open_nodes listĂˇt. Ez kiszĹ±ri
# azokat a rĂ©gi bejegyzĂ©seket, amelyekhez idĹ‘kĂ¶zben olcsĂłbb Ăştvonalat talĂˇltunk.
# A priority_queue ezt kĂ¶vetĹ‘en megjelenĂ­tĂ©shez hasznĂˇlhatĂł szĂłtĂˇrakat kĂ©szĂ­t:
#
#     {
#         "position": (1, 2),
#         "g": 3.0,
#         "h": 0.0,
#         "f": 3.0,
#     }
#
# Ez az adat bekerĂĽl az aktuĂˇlis search_steps elembe. ĂŤgy a search_steps nemcsak
# azt tĂˇrolja, hogy melyik cellĂˇt dolgoztuk fel, hanem az adott kĂ¶r vĂ©gĂ©n azt is,
# hogy mely node-ok vĂˇrakoznak mĂ©g, Ă©s melyik lesz vĂˇrhatĂłan a kĂ¶vetkezĹ‘.
#
# 8. A cĂ©l feldolgozĂˇsa Ă©s a vĂ©gsĹ‘ eredmĂ©ny
#
# A cĂ©l kivĂˇlasztĂˇsakor elĹ‘szĂ¶r bekerĂĽl az expanded_nodes listĂˇba:
#
#     expanded_nodes = [
#         (0, 0), (0, 1), (1, 0), (0, 2), (1, 1), (1, 2)
#     ]
#
# EzutĂˇn a program Ă©szreveszi, hogy current_position == goal, ezĂ©rt nem keres
# tovĂˇbbi szomszĂ©dokat. A came_from szĂłtĂˇrbĂłl visszafelĂ© felĂ©pĂ­ti az Ăştvonalat:
#
#     (1, 2) <- (0, 2) <- (0, 1) <- (0, 0)
#
# A visszafelĂ© kapott sorrendet megfordĂ­tja, ezĂ©rt a vĂ©gsĹ‘ path:
#
#     path = [(0, 0), (0, 1), (0, 2), (1, 2)]
#
# A visszaadott rĂ©szletes eredmĂ©ny szerkezete:
#
#     {
#         "path": path,
#         "expanded_nodes": expanded_nodes,
#         "search_steps": search_steps,
#     }
#
# RĂ¶vid adatĂˇramlĂˇs:
#
#     szomszĂ©d
#       -> g, h, f kiszĂˇmĂ­tĂˇsa
#       -> jobb Ăşt esetĂ©n came_from Ă©s g_costs frissĂ­tĂ©se
#       -> node hozzĂˇadĂˇsa az open_list-hez
#       -> rĂ©gi node-ok kiszĹ±rĂ©se valid_open_nodes segĂ­tsĂ©gĂ©vel
#       -> Ăˇllapot mentĂ©se a search_steps-ben
#       -> legjobb node kivĂˇlasztĂˇsa
#       -> cĂ©l esetĂ©n path felĂ©pĂ­tĂ©se a came_from alapjĂˇn
```

### codes_diploma/astar_project/astar_simulation.py

```python
"""Egyszeru matplotlib szimulacio az A* utvonal bemutatasahoz."""

import math
import tkinter as tk
from tkinter import messagebox, ttk

import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from matplotlib.widgets import Button

from .astar_baseline import astar_search
from .astar_variants import get_heuristic
from .grid_map import GridMap
from .path_smoothing import bezier_curve_points, smooth_path


def create_demo_map(
    width=30,
    height=20,
    resolution=0.2,
    robot_radius=0.08,
    start=(2, 2),
    goal=(17, 27),
):
    """Letrehoz egy ismert, statikus akadalyokat tartalmazo terkepet."""
    grid_map = GridMap(width=width, height=height, resolution=resolution)
    vertical_column = min(10, width - 2)
    horizontal_row = min(12, height - 2)
    vertical_wall = [
        (row, vertical_column)
        for row in range(2, max(2, height - 2))
        if row not in range(7, 13)
    ]
    horizontal_wall = [
        (horizontal_row, column)
        for column in range(12, max(12, width - 2))
        if column not in range(19, 25)
    ]
    for row, column in vertical_wall + horizontal_wall:
        if grid_map.is_inside(row, column) and (row, column) not in (start, goal):
            grid_map.add_obstacle(row, column)
    grid_map.inflate_obstacles(robot_radius)
    return grid_map, start, goal


def _parse_position(value):
    """Egy 'sor,oszlop' szoveget racskoordinatava alakit."""
    row, column = (int(part.strip()) for part in value.split(","))
    return row, column


def _read_settings(fields, diagonal, heuristic):
    """Beolvassa es ellenorzi a beallitasi ablak ertekeit."""
    get_value = lambda field: field.get() if hasattr(field, "get") else field.text
    heuristic_name = heuristic.get() if hasattr(heuristic, "get") else heuristic.value_selected
    diagonal_value = diagonal.get() if hasattr(diagonal, "get") else diagonal.get_status()[0]
    settings = {
        "width": int(get_value(fields["width"])),
        "height": int(get_value(fields["height"])),
        "resolution": float(get_value(fields["resolution"])),
        "robot_radius": float(get_value(fields["robot_radius"])),
        "start": _parse_position(get_value(fields["start"])),
        "goal": _parse_position(get_value(fields["goal"])),
        "diagonal": diagonal_value,
        "smooth_path": fields["smooth_path"].get(),
        "auto_play": fields["auto_play"].get(),
        "heuristic": get_heuristic(heuristic_name),
    }
    if settings["width"] < 3 or settings["height"] < 3:
        raise ValueError("A terkep legalabb 3 x 3 meretu legyen.")
    if settings["resolution"] <= 0 or settings["robot_radius"] < 0:
        raise ValueError("A felbontas pozitiv, a robotmeret nem negativ legyen.")
    return settings


def _create_settings_window(on_apply):
    """Letrehozza az A* bemeneti ertekeinek feluletet."""
    window = tk.Tk()
    window.title("A* beallitasok")
    window.resizable(False, False)
    main = ttk.Frame(window, padding=20)
    main.grid()
    ttk.Label(main, text="A* szimulacio", font=("Segoe UI", 16, "bold")).grid(
        row=0, column=0, columnspan=2, sticky="w", pady=(0, 16)
    )

    values = {
        "width": ("Szelesseg", "30"),
        "height": ("Magassag", "20"),
        "resolution": ("Felbontas [m]", "0.2"),
        "robot_radius": ("Robot sugar [m]", "0.08"),
        "start": ("Start (sor,oszlop)", "2,2"),
        "goal": ("Cel (sor,oszlop)", "17,27"),
    }
    fields = {}
    for index, (name, (label, value)) in enumerate(values.items()):
        row = index + 1
        ttk.Label(main, text=label).grid(row=row, column=0, sticky="w", padx=(0, 20), pady=5)
        field = ttk.Entry(main, width=24)
        field.insert(0, value)
        field.grid(row=row, column=1, sticky="ew", pady=5)
        fields[name] = field

    diagonal = tk.BooleanVar(value=True)
    ttk.Checkbutton(main, text="Atlos mozgas engedelyezese", variable=diagonal).grid(
        row=7, column=0, columnspan=2, sticky="w", pady=(12, 5)
    )
    ttk.Label(main, text="Heurisztika").grid(row=8, column=0, sticky="w", pady=5)
    heuristic = ttk.Combobox(
        main,
        values=["manhattan", "euclidean", "chebyshev", "octile"],
        state="readonly",
        width=21,
    )
    heuristic.set("euclidean")
    heuristic.grid(row=8, column=1, sticky="ew", pady=5)

    smooth_path_value = tk.BooleanVar(value=True)
    ttk.Checkbutton(
        main,
        text="Utvonal simitasa",
        variable=smooth_path_value,
    ).grid(row=9, column=0, columnspan=2, sticky="w", pady=5)
    fields["smooth_path"] = smooth_path_value

    auto_play_value = tk.BooleanVar(value=True)
    tk.Checkbutton(
        main,
        text="Automatikus lejatszas",
        variable=auto_play_value,
    ).grid(row=10, column=0, columnspan=2, sticky="w", pady=5)
    fields["auto_play"] = auto_play_value

    def apply_settings():
        try:
            settings = _read_settings(fields, diagonal, heuristic)
            window.destroy()
            on_apply(settings)
            plt.show()
        except (TypeError, ValueError, RuntimeError) as error:
            messagebox.showerror("Hibas beallitas", str(error), parent=window)

    ttk.Button(main, text="Szimulacio inditasa", command=apply_settings).grid(
        row=11, column=0, columnspan=2, sticky="ew", pady=(16, 0)
    )
    return window


def _safe_curve(grid_map, curve, diagonal):
    cells = [grid_map.world_to_grid(x, y) for x, y in curve]
    return all(
        grid_map.is_free(*cell)
        for cell in cells
    ) and all(
        current_next == current
        or current_next in grid_map.get_neighbors(*current, diagonal)
        for current, current_next in zip(cells, cells[1:])
    )


def create_robot_trajectory(
    grid_map, path, steps_per_cell=4, smooth=False, diagonal=False
):
    """Az A* cellautvonalabol koztes pontokat keszit az animaciohoz."""
    if not path:
        return []

    world_path = [grid_map.grid_to_world(row, column) for row, column in path]
    if smooth:
        curve = bezier_curve_points(world_path, samples_per_segment=20)
        if _safe_curve(grid_map, curve, diagonal):
            return curve

    trajectory = [world_path[0]]
    for start, end in zip(world_path, world_path[1:]):
        for step in range(1, steps_per_cell + 1):
            ratio = step / steps_per_cell
            trajectory.append(
                (
                    start[0] + ratio * (end[0] - start[0]),
                    start[1] + ratio * (end[1] - start[1]),
                )
            )
    return trajectory


def draw_map(ax, grid_map, start, goal):
    """Kirajzolja a terkepet es a start-cel pontokat."""
    for row in range(grid_map.height):
        for column in range(grid_map.width):
            if grid_map.grid[row][column] != 1:
                continue
            ax.add_patch(
                Rectangle(
                    (column * grid_map.resolution, row * grid_map.resolution),
                    grid_map.resolution,
                    grid_map.resolution,
                    facecolor="#444444",
                    edgecolor="white",
                    linewidth=0.3,
                )
            )

    start_x, start_y = grid_map.grid_to_world(*start)
    goal_x, goal_y = grid_map.grid_to_world(*goal)
    ax.scatter(start_x, start_y, color="#16803c", s=70, label="Start", zorder=4)
    ax.scatter(goal_x, goal_y, color="#c62828", s=70, label="Cel", zorder=4)
    ax.set_xlim(0, grid_map.width * grid_map.resolution)
    ax.set_ylim(0, grid_map.height * grid_map.resolution)
    ax.set_aspect("equal")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_xticks(
        [
            grid_map.origin_x + column * grid_map.resolution
            for column in range(grid_map.width + 1)
        ],
        minor=True,
    )
    ax.set_yticks(
        [
            grid_map.origin_y + row * grid_map.resolution
            for row in range(grid_map.height + 1)
        ],
        minor=True,
    )
    ax.grid(True, which="minor", color="#9e9e9e", alpha=0.5, linewidth=0.5)
    ax.grid(True, which="major", alpha=0.2)


def _priority_text(search_steps, frame):
    """Rovid szoveges tablazat az aktualis prioritasi sorrol."""
    if frame >= len(search_steps):
        return "A* kesz\n\nA robot koveti\na kivalasztott utvonalat."

    step = search_steps[frame]
    lines = [
        f"Lepes: {frame + 1}",
        f"Aktualis: {step['current']}",
        "",
        "pozicio       g     h     f",
    ]
    for index, item in enumerate(step.get("priority_queue", [])[:8], start=1):
        lines.append(
            f"{index:2d}. {str(item['position']):9s} "
            f"{item['g']:5.1f} {item['h']:5.1f} {item['f']:5.1f}"
        )
    if len(lines) == 4:
        lines.append("(ures prioritasi sor)")
    return "\n".join(lines)


def plot_simulation(
    grid_map,
    path,
    trajectory,
    start,
    goal,
    expanded_nodes=None,
    search_steps=None,
    original_path=None,
    robot_radius=0.08,
    planning_interval=200,
    movement_interval=50,
    auto_play=False,
    show=True,
    smoothed=False,
):
    """A* es robotmozgasi abra kezi vagy automatikus lejatszassal."""
    expanded_nodes = expanded_nodes or []
    search_steps = search_steps or []
    figure, (priority_ax, map_ax) = plt.subplots(
        1, 2, figsize=(13, 6), gridspec_kw={"width_ratios": (1.35, 2.4)}
    )
    figure.subplots_adjust(bottom=0.14, right=0.82, wspace=0.12)

    priority_ax.set_title("Prioritasi sor")
    priority_ax.set_axis_off()
    priority_ax.text(
        0.02,
        0.98,
        "A* prioritasi keplet",
        va="top",
        fontsize=10,
        fontweight="bold",
        color="#263238",
    )
    priority_ax.text(
        0.02,
        0.88,
        "f(n) = g(n) + h(n)\n\n"
        "g: eddigi ut koltsege\n"
        "h: becsult tavolsag a celig\n"
        "f: teljes prioritasi ertek\n\n"
        "Euklideszi h(n):\n"
        "h(n) = sqrt(dr^2 + dc^2)\n"
        "dr = |goal_row - row|\n"
        "dc = |goal_col - col|\n\n"
        "Pelda: dr=15, dc=25\n"
        "h(n) = sqrt(15^2 + 25^2) = 29.15\n\n"
        "Egyenes = 1.0 | Atlos = 1.41\n"
        "resolution = 0.2 m | robot = 0.08 m",
        va="top",
        family="monospace",
        fontsize=8,
        color="#263238",
        linespacing=1.35,
    )
    priority_text = priority_ax.text(
        0.02,
        0.31,
        "",
        va="top",
        family="monospace",
        fontsize=7.5,
        color="#004d40",
        linespacing=1.25,
    )
    draw_map(map_ax, grid_map, start, goal)
    map_ax.set_title("A* utvonal es Bezier-simitas")

    expanded_world = [grid_map.grid_to_world(*cell) for cell in expanded_nodes]
    path_world = [grid_map.grid_to_world(*cell) for cell in path]
    original_world = [
        grid_map.grid_to_world(*cell) for cell in (original_path or path)
    ]
    display_path = trajectory if smoothed else path_world
    path_x, path_y = zip(*display_path)
    original_x, original_y = zip(*original_world)
    original_line, = map_ax.plot(
        original_x,
        original_y,
        ":",
        color="#9e9e9e",
        linewidth=2,
        label="Eredeti A* utvonal",
        visible=False,
        zorder=2,
    )
    path_line, = map_ax.plot(
        path_x,
        path_y,
        "-",
        color="#ef8a8a",
        linewidth=2.0,
        alpha=0.8,
        label="Bezier-simitott utvonal",
        visible=False,
        zorder=3,
    )
    explored = map_ax.scatter(
        [], [], s=28, color="#90caf9", alpha=0.6, label="Vizsgalt cellak"
    )
    current_search = map_ax.scatter(
        [], [], s=90, color="#ff9800", edgecolors="#e65100",
        label="C: aktualis cella", zorder=5
    )
    robot = Circle(
        (math.nan, math.nan), robot_radius, color="#e65100", label="Robot", zorder=6
    )
    map_ax.add_patch(robot)
    trail, = map_ax.plot([], [], color="#f57c00", linewidth=2, label="Robot nyoma")
    status = map_ax.text(0.02, 0.98, "Indulas", transform=map_ax.transAxes, va="top")
    map_ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), borderaxespad=0)

    trajectory_x = [point[0] for point in trajectory]
    trajectory_y = [point[1] for point in trajectory]
    planning_frames = len(expanded_world)
    movement_start = planning_frames + 1
    total_frames = movement_start + len(trajectory)
    current_frame = 0

    def update(frame):
        nonlocal current_frame
        current_frame = frame
        if frame < planning_frames:
            explored.set_offsets(expanded_world[: frame + 1])
            current_search.set_offsets([expanded_world[frame]])
            priority_text.set_text(_priority_text(search_steps, frame))
            status.set_text(f"A* tervezes: {frame + 1}/{planning_frames}")
            path_line.set_visible(False)
            original_line.set_visible(False)
            robot.center = (math.nan, math.nan)
            trail.set_data([], [])
        elif frame == movement_start - 1:
            explored.set_offsets(expanded_world or [[math.nan, math.nan]])
            current_search.set_offsets([[math.nan, math.nan]])
            priority_text.set_text(_priority_text(search_steps, len(search_steps)))
            status.set_text("A* kesz - robotmozgas indul")
            original_line.set_visible(True)
            path_line.set_visible(True)
            robot.center = (math.nan, math.nan)
            trail.set_data([], [])
        else:
            movement_frame = min(frame - movement_start, len(trajectory) - 1)
            explored.set_offsets(expanded_world or [[math.nan, math.nan]])
            current_search.set_offsets([[math.nan, math.nan]])
            priority_text.set_text(_priority_text(search_steps, len(search_steps)))
            original_line.set_visible(True)
            path_line.set_visible(True)
            robot.center = (trajectory_x[movement_frame], trajectory_y[movement_frame])
            trail.set_data(trajectory_x[: movement_frame + 1], trajectory_y[: movement_frame + 1])
            status.set_text(
                "Cel elerve" if movement_frame == len(trajectory) - 1
                else f"Robotmozgas: {movement_frame + 1}/{len(trajectory)}"
            )
        return (
            explored,
            current_search,
            original_line,
            path_line,
            robot,
            trail,
            status,
            priority_text,
        )

    robot_animation = animation.FuncAnimation(
        figure,
        update,
        frames=total_frames,
        interval=planning_interval,
        repeat=False,
        blit=False,
    )

    if not auto_play and robot_animation.event_source is not None:
        robot_animation.event_source.stop()
        update(0)

    next_button = Button(figure.add_axes((0.68, 0.035, 0.13, 0.06)), "Kovetkezo")
    reset_button = Button(figure.add_axes((0.83, 0.035, 0.13, 0.06)), "Ujrakezdes")

    def next_frame(_event=None):
        nonlocal current_frame
        current_frame = min(current_frame + 1, total_frames - 1)
        update(current_frame)
        figure.canvas.draw_idle()

    def reset_simulation(_event=None):
        nonlocal current_frame
        current_frame = 0
        update(current_frame)
        figure.canvas.draw_idle()

    next_button.on_clicked(next_frame)
    reset_button.on_clicked(reset_simulation)
    figure._astar_animation = robot_animation
    figure._astar_controls = (next_button, reset_button)
    figure._astar_next_frame = next_frame
    figure._astar_reset = reset_simulation
    figure.canvas.mpl_connect(
        "key_press_event",
        lambda event: next_frame() if event.key in ("right", " ") else None,
    )
    if show:
        plt.show()
    return figure, robot_animation


def _run_simulation(settings, show=True):
    """A megadott beallitasokkal lefuttatja a szimulaciot."""
    grid_map, start, goal = create_demo_map(
        width=settings["width"],
        height=settings["height"],
        resolution=settings["resolution"],
        robot_radius=settings["robot_radius"],
        start=settings["start"],
        goal=settings["goal"],
    )
    result = astar_search(
        grid_map,
        start,
        goal,
        diagonal=settings["diagonal"],
        heuristic=settings["heuristic"],
        return_details=True,
    )
    if result["path"] is None:
        raise RuntimeError("A demo terkepen nincs elerheto utvonal.")
    original_path = result["path"]
    path = original_path
    if settings["smooth_path"]:
        path = smooth_path(grid_map, path, settings["diagonal"])
    trajectory = create_robot_trajectory(
        grid_map,
        path,
        smooth=settings["smooth_path"],
        diagonal=settings["diagonal"],
    )
    return plot_simulation(
        grid_map,
        path,
        trajectory,
        start,
        goal,
        expanded_nodes=result["expanded_nodes"],
        search_steps=result["search_steps"],
        original_path=original_path,
        auto_play=settings["auto_play"],
        show=show,
        smoothed=settings["smooth_path"],
    )


def run_simulation(show=True):
    """Beallitasi ablakot nyit, majd elinditja az A* szimulaciot."""
    simulation_figure = [None]

    def apply_settings(settings):
        if simulation_figure[0] is not None:
            plt.close(simulation_figure[0])
        simulation_figure[0], _ = _run_simulation(settings, show=False)

    settings_figure = _create_settings_window(apply_settings)
    if show:
        settings_figure.mainloop()
    return settings_figure


if __name__ == "__main__":
    run_simulation()
```

### codes_diploma/astar_project/astar_variants.py

```python
"""EgyszerĹ±en cserĂ©lhetĹ‘ heurisztikĂˇk az A* Ă¶sszehasonlĂ­tĂˇsĂˇhoz."""

import math


def manhattan(position, goal):
	"""TĂˇvolsĂˇg csak vĂ­zszintes Ă©s fĂĽggĹ‘leges mozgĂˇshoz."""
	return abs(position[0] - goal[0]) + abs(position[1] - goal[1])


def euclidean(position, goal):
	"""LĂ©gvonalbeli tĂˇvolsĂˇg."""
	row_distance = abs(position[0] - goal[0])
	column_distance = abs(position[1] - goal[1])
	return math.sqrt(row_distance ** 2 + column_distance ** 2)


def chebyshev(position, goal):
	"""A kĂ©t koordinĂˇtakĂĽlĂ¶nbsĂ©g kĂ¶zĂĽl a nagyobb."""
	return max(abs(position[0] - goal[0]), abs(position[1] - goal[1]))


def octile(position, goal):
	"""JĂł becslĂ©s egyenes Ă©s sqrt(2) kĂ¶ltsĂ©gĹ± ĂˇtlĂłs mozgĂˇshoz."""
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


def get_heuristic(name):
	"""Visszaadja a nĂ©vhez tartozĂł heurisztikĂˇt."""
	try:
		return HEURISTICS[name]
	except KeyError as error:
		raise ValueError(f"Ismeretlen heurisztika: {name}") from error

```

### codes_diploma/astar_project/compose_simulation_obstacle_avoidance.py

```python
"""Harom szimulacios kepkocka egyetlen, beillesztheto abrahoz."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from PIL import Image


FRAME_DIRECTORY = Path(__file__).resolve().parent / "results" / "figures"
FRAME_NAMES = (
    "simulation_02_frame_0100.png",
    "simulation_03_frame_0250.png",
    "simulation_04_frame_0500.png",
)
CROP_BOX = (570, 235, 1810, 1035)


def main():
    figure, axes = plt.subplots(1, 3, figsize=(18, 6), dpi=180)
    figure.subplots_adjust(wspace=0.03, left=0, right=1, top=1, bottom=0)

    for axis, filename in zip(axes, FRAME_NAMES):
        image_path = FRAME_DIRECTORY / filename
        if not image_path.exists():
            raise FileNotFoundError(f"Hianyzo szimulacios kepkocka: {image_path}")
        with Image.open(image_path) as source_image:
            grid_image = source_image.crop(CROP_BOX)
        axis.imshow(grid_image)
        axis.axis("off")

    output_path = FRAME_DIRECTORY / "simulation_obstacle_avoidance_sequence.png"
    figure.savefig(output_path, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    print(f"Abra mentve: {output_path}")


if __name__ == "__main__":
    main()
```

### codes_diploma/astar_project/experiments.py

```python
"""ReprodukĂˇlhatĂł A* Ă¶sszehasonlĂ­tĂł kĂ­sĂ©rletek."""

import csv
import math
from pathlib import Path

from .astar_baseline import astar_search
from .astar_variants import HEURISTICS, get_heuristic
from .grid_map import GridMap


def _path_cost(path):
    """KiszĂˇmĂ­tja a rĂˇcsĂştvonal kĂ¶ltsĂ©gĂ©t egyenes/ĂˇtlĂłs lĂ©pĂ©sekkel."""
    if not path:
        return None
    return sum(
        math.hypot(current[0] - previous[0], current[1] - previous[1])
        for previous, current in zip(path, path[1:])
    )


def build_experiment_scenarios():
    """Visszaadja azonos mĂ©retĹ±, reprodukĂˇlhatĂł tesztpĂˇlyĂˇkat.

    A pĂˇlyĂˇk kĂ¶zĂ¶tt van szabad tĂ©r, ĂˇtjĂˇrĂłt tartalmazĂł akadĂˇlypĂˇlya,
    sarokvĂˇgĂˇst tiltĂł eset Ă©s olyan pĂˇlya is, ahol ĂˇtlĂłs mozgĂˇs nĂ©lkĂĽl
    nincs megoldĂˇs.
    """
    scenarios = {}

    original_map = GridMap(width=30, height=20, resolution=0.2)
    vertical_column = 10
    horizontal_row = 12
    for row in range(2, 18):
        if row not in range(7, 13):
            original_map.add_obstacle(row, vertical_column)
    for column in range(12, 28):
        if column not in range(19, 25):
            original_map.add_obstacle(horizontal_row, column)
    scenarios["original_simulation"] = (original_map, (2, 2), (17, 27))

    compact_map = GridMap(width=10, height=7)
    for row in range(7):
        if row not in (2, 3):
            compact_map.add_obstacle(row, 3)
    for column in range(4, 9):
        if column not in (6, 7):
            compact_map.add_obstacle(4, column)
    scenarios["compact_corridor"] = (compact_map, (0, 0), (6, 9))

    corner_map = GridMap(width=5, height=5)
    corner_map.add_obstacle(1, 2)
    corner_map.add_obstacle(2, 1)
    scenarios["corner_cutting"] = (corner_map, (1, 1), (3, 3))

    diagonal_only_map = GridMap(width=3, height=3)
    diagonal_only_map.add_obstacle(0, 1)
    diagonal_only_map.add_obstacle(1, 0)
    diagonal_only_map.add_obstacle(1, 2)
    diagonal_only_map.add_obstacle(2, 1)
    scenarios["diagonal_only"] = (diagonal_only_map, (0, 0), (2, 2))

    return scenarios


def compare_heuristics(grid_map, start, goal, diagonal, heuristic_names=None):
    """Ă–sszeveti a heurisztikĂˇkat egyetlen pĂˇlyĂˇn.

    A visszatĂ©rĂ©si lista minden eleme tartalmazza a heurisztika nevĂ©t,
    a talĂˇlt Ăştvonalat, annak kĂ¶ltsĂ©gĂ©t, a kibĹ‘vĂ­tett csomĂłpontok szĂˇmĂˇt
    Ă©s azt, hogy sikerĂĽlt-e cĂ©lt elĂ©rni.
    """
    names = list(heuristic_names or HEURISTICS)
    rows = []
    for name in names:
        heuristic = get_heuristic(name)
        result = astar_search(
            grid_map,
            start,
            goal,
            diagonal=diagonal,
            heuristic=heuristic,
            return_details=True,
        )
        path = result["path"]
        rows.append(
            {
                "heuristic": name,
                "diagonal": diagonal,
                "success": path is not None,
                "path_cost": _path_cost(path),
                "path_length": len(path) if path is not None else None,
                "expanded_nodes": len(result["expanded_nodes"]),
                "path": path,
            }
        )
    return rows


def run_scenario_comparison(heuristic_names=None):
    """Minden pĂˇlyĂˇt lefuttat ĂˇtlĂłs Ă©s nem ĂˇtlĂłs mĂłdban."""
    rows = []
    for scenario_name, (grid_map, start, goal) in build_experiment_scenarios().items():
        for diagonal in (False, True):
            for row in compare_heuristics(
                grid_map, start, goal, diagonal, heuristic_names
            ):
                rows.append({"scenario": scenario_name, **row})
    return rows


def write_results(rows, output_path):
    """CSV-be menti a kĂ­sĂ©rleti eredmĂ©nyeket, Ăştvonal nĂ©lkĂĽl."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "scenario",
        "heuristic",
        "diagonal",
        "success",
        "path_cost",
        "path_length",
        "expanded_nodes",
    ]
    with output_path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row[field] for field in fields})
```

### codes_diploma/astar_project/generate_comparison_figures.py

```python
"""Pontokkal es vonalstilusokkal jelolt heurisztika-abra generalasa."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from .astar_baseline import astar_search
from .astar_variants import HEURISTICS, get_heuristic
from .experiments import _path_cost, build_experiment_scenarios


COLORS = {
    "manhattan": "#0072B2",
    "euclidean": "#E69F00",
    "chebyshev": "#009E73",
    "octile": "#CC79A7",
}


def _draw_scenario(grid_map, start, goal, output_path):
    figure, axes = plt.subplots(1, 2, figsize=(17, 8), dpi=180)
    for axis, diagonal, title in (
        (axes[0], False, "NĂ©gyirĂˇnyĂş mozgĂˇs"),
        (axes[1], True, "ĂtlĂłs mozgĂˇs is engedĂ©lyezett"),
    ):
        for row in range(grid_map.height):
            for column in range(grid_map.width):
                if grid_map.grid[row][column] == 1:
                    axis.add_patch(
                        Rectangle(
                            (column * grid_map.resolution, row * grid_map.resolution),
                            grid_map.resolution,
                            grid_map.resolution,
                            facecolor="#455A64",
                            edgecolor="none",
                            zorder=1,
                        )
                    )
        for row in range(grid_map.height + 1):
            axis.axhline(
                row * grid_map.resolution,
                color="#78909C",
                linewidth=0.65,
                alpha=0.75,
                zorder=0,
            )
        for column in range(grid_map.width + 1):
            axis.axvline(
                column * grid_map.resolution,
                color="#78909C",
                linewidth=0.65,
                alpha=0.75,
                zorder=0,
            )
        for heuristic_name in HEURISTICS:
            color = COLORS[heuristic_name]
            result = astar_search(
                grid_map,
                start,
                goal,
                diagonal=diagonal,
                heuristic=get_heuristic(heuristic_name),
                return_details=True,
            )
            path = result["path"]
            if path is None:
                continue
            world_path = [
                grid_map.grid_to_world(row, column)
                for row, column in path
            ]
            path_x = [x for x, _ in world_path]
            path_y = [y for _, y in world_path]
            cost = _path_cost(path)
            label = f"{heuristic_name.title()}: {cost:.2f}"
            line, = axis.plot(
                path_x,
                path_y,
                color=color,
                linestyle="--",
                dashes=(3, 2),
                marker="o",
                markersize=2.4,
                markeredgewidth=0.45,
                markeredgecolor="white",
                linewidth=1.8,
                alpha=0.92,
                label=label,
                zorder=4,
            )

        start_x, start_y = grid_map.grid_to_world(*start)
        goal_x, goal_y = grid_map.grid_to_world(*goal)
        axis.scatter(
            [start_x], [start_y], s=90, marker="o",
            facecolor="#00A651", edgecolor="white", linewidth=2, zorder=5,
        )
        axis.scatter(
            [goal_x], [goal_y], s=110, marker="*",
            facecolor="#E31B23", edgecolor="white", linewidth=1.5, zorder=5,
        )
        axis.text(
            start_x, start_y, "S", color="white", ha="center",
            va="center", weight="bold", zorder=6,
        )
        axis.text(
            goal_x, goal_y, "G", color="white", ha="center",
            va="center", weight="bold", zorder=6,
        )
        axis.set_title(title, fontsize=15, weight="bold")
        axis.set_xlabel("x [m]")
        axis.set_ylabel("y [m]")
        axis.set_xlim(0, grid_map.width * grid_map.resolution)
        axis.set_ylim(0, grid_map.height * grid_map.resolution)
        axis.set_aspect("equal")
        axis.legend(
            loc="lower left",
            fontsize=8,
            framealpha=0.92,
            title="Heurisztika: kĂ¶ltsĂ©g",
        )

    figure.suptitle(
        "A* heurisztikĂˇk az eredeti szimulĂˇciĂłs tĂ©rkĂ©pen",
        fontsize=18,
        weight="bold",
    )
    figure.tight_layout(rect=(0, 0.10, 1, 0.94))
    figure.savefig(output_path, bbox_inches="tight")
    plt.close(figure)


def main():
    output_directory = (
        Path(__file__).resolve().parent / "results" / "figures"
    )
    output_directory.mkdir(parents=True, exist_ok=True)
    original_map, start, goal = build_experiment_scenarios()[
        "original_simulation"
    ]
    _draw_scenario(
        original_map,
        start,
        goal,
        output_directory / "heuristics_original_simulation.png",
    )
    print(f"Abraak mentve: {output_directory}")


if __name__ == "__main__":
    main()
```

### codes_diploma/astar_project/generate_simulation_heuristic_comparison.py

```python
"""A valodi A*+DWA szimulacios terkep osszehasonlito abrazolasa."""

import importlib.util
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.patheffects as patheffects
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from .astar_variants import HEURISTICS, get_heuristic
from .experiments import _path_cost
from .. import simulation


COLORS = {
    "manhattan": "#0057B8",
    "euclidean": "#F28E00",
    "chebyshev": "#009E73",
    "octile": "#D81B60",
}

LINESTYLES = {
    "manhattan": "-",
    "euclidean": "--",
    "chebyshev": "-.",
    "octile": ":",
}


def _load_planner_class():
    file_path = Path(simulation.__file__).with_name("DWA+A.py")
    spec = importlib.util.spec_from_file_location("dwa_a_comparison", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.AStarDWAPlanner


def _draw_map(axis, grid_map):
    for row in range(grid_map.height):
        for column in range(grid_map.width):
            if grid_map.grid[row][column] == 1:
                axis.add_patch(
                    Rectangle(
                        (
                            column * grid_map.resolution,
                            row * grid_map.resolution,
                        ),
                        grid_map.resolution,
                        grid_map.resolution,
                        facecolor="#455A64",
                        edgecolor="none",
                        zorder=1,
                    )
                )
    for row in range(grid_map.height + 1):
        axis.axhline(
            row * grid_map.resolution,
            color="#78909C",
            linewidth=0.65,
            alpha=0.75,
            zorder=0,
        )
    for column in range(grid_map.width + 1):
        axis.axvline(
            column * grid_map.resolution,
            color="#78909C",
            linewidth=0.65,
            alpha=0.75,
            zorder=0,
        )


def _draw_paths(axis, grid_map, start_cell, goal_cell, diagonal):
    for heuristic_name in HEURISTICS:
        _draw_path(
            axis,
            grid_map,
            start_cell,
            goal_cell,
            diagonal,
            heuristic_name,
        )


def _draw_path(axis, grid_map, start_cell, goal_cell, diagonal, heuristic_name):
    planner_class = _load_planner_class()
    start = grid_map.grid_to_world(*start_cell)
    goal = grid_map.grid_to_world(*goal_cell)
    heuristic = get_heuristic(heuristic_name)
    planner = planner_class(
        grid_map,
        config=simulation.robotconfig(),
        diagonal=diagonal,
    )
    path = planner.plan_global(
        start,
        goal,
        heuristic=heuristic,
        smooth=False,
    )
    if path:
        path_x, path_y = zip(*path)
        grid_path = [grid_map.world_to_grid(x, y) for x, y in path]
        cost = _path_cost(grid_path)
        axis.plot(
            path_x,
            path_y,
            color=COLORS[heuristic_name],
            linestyle=LINESTYLES[heuristic_name],
            linewidth=2.8,
            alpha=1.0,
            marker="o",
            markersize=2.8,
            markeredgewidth=0.7,
            markeredgecolor="#FFFFFF",
            label=f"{heuristic_name.title()}: {cost:.2f}",
            zorder=4,
            path_effects=[
                patheffects.Stroke(linewidth=5.0, foreground="#FFFFFF"),
                patheffects.Normal(),
            ],
        )


def main():
    grid_map, start_cell, goal_cell, *_ = simulation.create_scene(
        width=30,
        height=20,
        resolution=0.2,
        start_cell=(2, 2),
        goal_cell=(17, 27),
        inflation_radius=0.1,
    )
    matplotlib.use("Agg", force=True)
    figure, axes = plt.subplots(1, 2, figsize=(17, 8), dpi=180)
    for axis, diagonal, title in (
        (axes[0], False, "NĂ©gyirĂˇnyĂş A* + DWA"),
        (axes[1], True, "ĂtlĂłs A* + DWA"),
    ):
        _draw_map(axis, grid_map)
        _draw_paths(axis, grid_map, start_cell, goal_cell, diagonal)
        start_x, start_y = grid_map.grid_to_world(*start_cell)
        goal_x, goal_y = grid_map.grid_to_world(*goal_cell)
        axis.scatter(
            [start_x],
            [start_y],
            s=90,
            color="#00A651",
            edgecolors="white",
            linewidths=1.5,
            zorder=6,
        )
        axis.scatter(
            [goal_x],
            [goal_y],
            s=110,
            marker="*",
            color="#E31B23",
            edgecolors="white",
            linewidths=1.2,
            zorder=6,
        )
        axis.set_title(title, fontsize=15, weight="bold")
        axis.set_xlabel("x [m]")
        axis.set_ylabel("y [m]")
        axis.set_xlim(0, grid_map.width * grid_map.resolution)
        axis.set_ylim(0, grid_map.height * grid_map.resolution)
        axis.set_aspect("equal")
        axis.legend(
            loc="upper center",
            bbox_to_anchor=(0.5, -0.10),
            ncol=2,
            fontsize=8,
            framealpha=0.92,
            title="Heurisztika: kĂ¶ltsĂ©g",
        )

    figure.suptitle(
        "A*+DWA Ăştvonalak az eredeti, inflĂˇlt szimulĂˇciĂłs tĂ©rkĂ©pen",
        fontsize=18,
        weight="bold",
    )
    figure.tight_layout(rect=(0, 0.06, 1, 0.94))
    output_path = (
        Path(__file__).resolve().parent
        / "results"
        / "figures"
        / "simulation_heuristic_comparison.png"
    )
    figure.savefig(output_path, bbox_inches="tight")
    plt.close(figure)
    print(f"Abra mentve: {output_path}")


if __name__ == "__main__":
    main()
```

### codes_diploma/astar_project/grid_map.py

```python
"""Egyszeru racsterkep az A* algoritmushoz."""

import math


class GridMap:
    """Negyzetes cellakbol allo, ketdimenzios terkep."""

    def __init__(
        self,
        width,
        height,
        resolution=0.1,
        origin_x=0.0,
        origin_y=0.0,
        unknown=False,
    ):
        if width <= 0 or height <= 0:
            raise ValueError("A terkep merete legyen pozitiv.")
        if resolution <= 0:
            raise ValueError("A felbontas legyen pozitiv.")

        self.width = width
        self.height = height
        self.resolution = resolution
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.grid = []

        initial_value = 2 if unknown else 0
        for _ in range(height):
            self.grid.append([initial_value] * width)

    def is_inside(self, row, column):
        """Megadja, hogy a cella a terkepen belul van-e."""
        return 0 <= row < self.height and 0 <= column < self.width

    def is_free(self, row, column):
        """Megadja, hogy a cella szabad-e."""
        return self.is_inside(row, column) and self.grid[row][column] == 0

    def world_to_grid(self, x, y):
        """Vilagkoordinatat (meterben) racskoordinatava alakit."""
        column = math.floor((x - self.origin_x) / self.resolution)
        row = math.floor((y - self.origin_y) / self.resolution)
        return row, column

    def grid_to_world(self, row, column):
        """A cella kozepontjat visszaadja vilagkoordinataban."""
        x = self.origin_x + (column + 0.5) * self.resolution
        y = self.origin_y + (row + 0.5) * self.resolution
        return x, y

    def add_obstacle(self, row, column):
        """Akadalykent megjelol egy cellat."""
        if not self.is_inside(row, column):
            raise ValueError("Az akadaly a terkepen kivul van.")
        self.grid[row][column] = 1

    def remove_obstacle(self, row, column):
        """Szabad cellava tesz egy cellat."""
        if not self.is_inside(row, column):
            raise ValueError("A cella a terkepen kivul van.")
        self.grid[row][column] = 0

    def mark_free(self, row, column):
        """A robot altal megvizsgalt cellat szabadnak jelol."""
        if not self.is_inside(row, column):
            raise ValueError("A cella a terkepen kivul van.")
        self.grid[row][column] = 0

    def add_obstacle_world(self, x, y, radius=0.0):
        """Vilagkoordinatas akadalyat egy vagy tobb cellaba ir."""
        center_row, center_column = self.world_to_grid(x, y)
        cell_radius = int(radius / self.resolution) + 1

        for row in range(center_row - cell_radius, center_row + cell_radius + 1):
            for column in range(
                center_column - cell_radius,
                center_column + cell_radius + 1,
            ):
                if not self.is_inside(row, column):
                    continue
                cell_x, cell_y = self.grid_to_world(row, column)
                distance = ((cell_x - x) ** 2 + (cell_y - y) ** 2) ** 0.5
                if distance <= radius + self.resolution:
                    self.add_obstacle(row, column)

    def update_from_obstacles(self, obstacles):
        """Szimulacios akadalyobjektumokbol frissiti a terkepet.

        Az objektumoknak ``x``, ``y`` es opcionisan ``radius`` attributummal
        kell rendelkezniuk, ahogy a DWA Obstacle osztĂˇlyĂˇnak.
        """
        for obstacle in obstacles:
            radius = getattr(obstacle, "radius", 0.0)
            self.add_obstacle_world(obstacle.x, obstacle.y, radius)

    def inflate_obstacles(self, radius):
        """Biztonsagi tavolsaggal kitagitja az akadalycellakat."""
        if radius < 0:
            raise ValueError("A biztonsagi sugar nem lehet negativ.")
        if radius == 0:
            return

        obstacle_cells = [
            (row, column)
            for row in range(self.height)
            for column in range(self.width)
            if self.grid[row][column] == 1
        ]
        cell_radius = math.ceil(radius / self.resolution)

        for obstacle_row, obstacle_column in obstacle_cells:
            for row in range(
                obstacle_row - cell_radius,
                obstacle_row + cell_radius + 1,
            ):
                for column in range(
                    obstacle_column - cell_radius,
                    obstacle_column + cell_radius + 1,
                ):
                    if self.is_inside(row, column):
                        self.grid[row][column] = 1

    def get_neighbors(self, row, column, diagonal=False):
        """Visszaadja a szabad szomszedos cellakat."""
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        if diagonal:
            directions += [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        neighbors = []
        for row_change, column_change in directions:
            new_row = row + row_change
            new_column = column + column_change
            if self.is_free(new_row, new_column):
                is_diagonal = row_change != 0 and column_change != 0
                if is_diagonal:
                    if not self.is_free(row, new_column):
                        continue
                    if not self.is_free(new_row, column):
                        continue
                neighbors.append((new_row, new_column))

        return neighbors
```

### codes_diploma/astar_project/metrics.py

```python
"""Path quality and experiment performance metrics."""
```

### codes_diploma/astar_project/path_smoothing.py

```python
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


r"""VizsgĂˇljuk meg a kĂłdot **fĂĽggvĂ©nyrĹ‘l fĂĽggvĂ©nyre, sorrĂłl sorra**, rĂ©szletesen kitĂ©rve az Ă¶sszes paramĂ©terre, belsĹ‘ vĂˇltozĂłra Ă©s a mĂ¶gĂ¶ttes logikĂˇra.

---

### 1. `_bezier_point(start_point, control_point, end_point, parameter)`

Ez a fĂĽggvĂ©ny felelĹ‘s a mĂˇsodfokĂş BĂ©zier-gĂ¶rbe egyetlen koordinĂˇtĂˇjĂˇnak kiszĂˇmĂ­tĂˇsĂˇĂ©rt egy adott $t$ paramĂ©terhelyen.

* **ParamĂ©terek:**
* `start_point`: Egy `(x, y)` vagy `(row, column)` koordinĂˇtapĂˇr, amely a BĂ©zier-szakasz kezdĹ‘pontjĂˇt ($P_0$) jelenti.
* `control_point`: Egy koordinĂˇtapĂˇr, amely a kontrollpontot ($P_1$, azaz maga a sarokpont) adja meg, ami felĂ© a gĂ¶rbe "hajlik".
* `end_point`: Egy koordinĂˇtapĂˇr, amely a BĂ©zier-szakasz vĂ©gpontjĂˇt ($P_2$) jelenti.
* `parameter`: Egy lebegĹ‘pontos szĂˇm ($t$), amely $0.0$ Ă©s $1.0$ kĂ¶zĂ¶tt mozog ($0$ a szakasz eleje, $1$ a vĂ©ge).


* **BelsĹ‘ vĂˇltozĂłk:**
* `weight`: KiszĂˇmĂ­tja a `1 - parameter` Ă©rtĂ©ket (ez a $(1-t)$ tĂ©nyezĹ‘ a kĂ©pletben).


* **MĹ±kĂ¶dĂ©s:**
* BehelyettesĂ­ti az Ă©rtĂ©keket a mĂˇsodfokĂş BĂ©zier-kĂ©pletbe kĂĽlĂ¶n az $x$ Ă©s $y$ koordinĂˇtĂˇra:
$\text{koordinĂˇta} = (1-t)^2 \cdot P_{0} + 2(1-t)t \cdot P_{1} + t^2 \cdot P_{2}$.
* VisszatĂ©r egy Ăşj, simĂ­tott `(x, y)` ponttal (ami mĂˇr lebegĹ‘pontos tizedesjegyeket is tartalmazhat).



---

### 2. `_remove_straight_points(path)`

Az A* Ăˇltal adott Ăştvonal sok felesleges, egymĂˇs melletti pontot tartalmaz egyenes szakaszokon. Ez a fĂĽggvĂ©ny kiszĹ±ri Ĺ‘ket, hogy csak a sarkok maradjanak.

* **ParamĂ©terek:**
* `path`: Az eredeti rĂˇcspontok listĂˇja (pl. `[(0,0), (0,1), (0,2), (1,3), ...]`).


* **BelsĹ‘ vĂˇltozĂłk:**
* `turning_points`: Egy lista, amely kezdetben csak a kezdĹ‘pontot (`path[0]`) tartalmazza, ide gyĹ±jtjĂĽk majd a sarkokat.
* `point_index`: A ciklus futĂłindexe, amivel egyesĂ©vel haladunk vĂ©gig a belsĹ‘ pontokon.
* `previous_point`, `current_point`, `next_point`: Egy hĂˇrmas ablak ($m-1, m, m+1$) a szomszĂ©dos csomĂłpontok vizsgĂˇlatĂˇhoz.
* `incoming_row`, `incoming_column`: Az Ă©rkezĹ‘ vektor komponensei (`current` minus `previous`).
* `outgoing_row`, `outgoing_column`: A tĂˇvozĂł vektor komponensei (`next` minus `current`).


* **MĹ±kĂ¶dĂ©s:**
* KĂ©t vektoriĂˇlis irĂˇnyt hasonlĂ­t Ă¶ssze kereszt-szorzattal (`incoming_row * outgoing_column != incoming_column * outgoing_row`).
* Ha a kereszt-szorzat nem nulla, az azt jelenti, hogy az irĂˇny megvĂˇltozott (vagyis a pont egy kanyar / sarok). Ekkor bekerĂĽl a `turning_points`-ba. Ha nulla, az azt jelenti, hogy a pont egy egyenes rĂ©sze, Ă­gy a kĂłd figyelmen kĂ­vĂĽl hagyja (kidobja).
* VĂ©gĂĽl hozzĂˇadja a cĂ©lpontot (`path[-1]`) is, majd visszatĂ©r a sarkok listĂˇjĂˇval.



---

### 3. `_curve_points(start_point, control_point, end_point, sample_count)`

Egy adott kanyar szakaszhoz tartozĂł Ă¶sszes mintapontot generĂˇlja le a BĂ©zier-kĂ©plet ismĂ©telt meghĂ­vĂˇsĂˇval.

* **ParamĂ©terek:**
* `start_point`: A kanyar kezdĹ‘pontja.
* `control_point`: A kanyar kontrollpontja (sarok).
* `end_point`: A kanyar vĂ©gpontja.
* `sample_count`: EgĂ©sz szĂˇm, amely megadja, hogy hĂˇny darab kis lĂ©pĂ©sre (mintĂˇra) bontsa fel a kanyar Ă­vĂ©t.


* **BelsĹ‘ vĂˇltozĂłk:**
* `sample_index`: A ciklusban $0$-tĂłl `sample_count`-ig szĂˇmolĂł index.


* **MĹ±kĂ¶dĂ©s:**
* EllenĹ‘rzi, hogy a `sample_count` pozitĂ­v-e (ha nem, `ValueError`-t dob).
* Egy listagenerĂˇtorral vĂ©gigfut a lĂ©pĂ©seken, kiszĂˇmolja a $t = \text{sample\_index} / \text{sample\_count}$ arĂˇnyt, meghĂ­vja a `_bezier_point`-ot, Ă©s Ă¶sszegyĹ±jti az Ă­v pontjait egy listĂˇba.



---

### 4. `bezier_curve_points(path, samples_per_segment=10)`

Ez szervezi Ă¶ssze a teljes Ăştvonal simĂ­tĂˇsĂˇt a sarkok Ă©s a kanyarok kĂ¶zĂ¶tt.

* **ParamĂ©terek:**
* `path`: Az eredeti A* Ăştvonal.
* `samples_per_segment`: HĂˇny mintapontot kĂ©szĂ­tsen egy-egy kanyarhoz (alapĂ©rtelmezĂ©sben `10`).


* **BelsĹ‘ vĂˇltozĂłk:**
* `turning_points`: A `_remove_straight_points(path)` Ăˇltal megtisztĂ­tott sarkok listĂˇja.
* `curve`: Az Ă©pĂĽlĹ‘, simĂ­tott Ăştvonalat tĂˇrolĂł lista, amely a kezdĹ‘ponttal indul.
* `point_index`: A sarkokon vĂ©gigiterĂˇlĂł index.
* `previous_point`, `control_point`, `next_point`: A soron kĂ¶vetkezĹ‘ sarok Ă©s a szomszĂ©dai.
* `start_point`, `end_point`: A BĂ©zier-Ă­v tĂ©nyleges kezdĹ‘- Ă©s vĂ©gpontja. *MegjegyzĂ©s:* Ezeket a kĂłd a szomszĂ©dos Ă©lek **felezĹ‘pontjainĂˇl** veszi fel, kivĂ©ve a teljes Ăşt elejĂ©t Ă©s vĂ©gĂ©t, ahol rĂ¶gzĂ­tetten a valĂłdi kezdĹ‘/vĂ©gpontot hasznĂˇlja.
* `segment_points`: Az aktuĂˇlis kanyarhoz generĂˇlt pontok listĂˇja.


* **MĹ±kĂ¶dĂ©s:**
* VĂ©gigmegy a sarkokon, kiszĂˇmolja a felezĹ‘pontok alapjĂˇn a BĂ©zier-Ă­vek hatĂˇrait, generĂˇlja a pontokat a `_curve_points`-szal, majd hozzĂˇfĹ±zi a `curve` listĂˇhoz (ĂĽgyelve arra, hogy a csatlakozĂˇsi pontok ne duplĂˇzĂłdjanak meg a `segment_points[1:]` szeletelĂ©ssel).



---

### 5. `_is_path_safe(grid_map, path, diagonal=False)`

Ez a legfontosabb **biztonsĂˇgi vĂ©dĹ‘hĂˇlĂł**, ami garantĂˇlja, hogy a robot ne ĂĽtkĂ¶zzĂ¶n neki semminek a simĂ­tĂˇs miatt.

* **ParamĂ©terek:**
* `grid_map`: A tĂ©rkĂ©p objektum (amelyben az akadĂˇlyok helye van tĂˇrolva).
* `path`: A simĂ­tott, lebegĹ‘pontos koordinĂˇtĂˇkat tartalmazĂł Ăştvonal.
* `diagonal`: Logikai Ă©rtĂ©k (`True` / `False`), ami engedĂ©lyezi-e az ĂˇtlĂłs rĂˇcslĂ©pĂ©seket.


* **BelsĹ‘ vĂˇltozĂłk:**
* `rounded_cells`: Mivel a BĂ©zier-gĂ¶rbe tizedesjegyeket ad (pl. `(1.23, 4.56)`), ez a lista **egĂ©sz rĂˇcscellĂˇkra kerekĂ­ti** (`round()`) az Ă¶sszes pontot, hogy illeszkedjenek a diszkrĂ©t rĂˇcstĂ©rkĂ©pre.
* `current_cell`, `next_cell`: Az egymĂˇst kĂ¶vetĹ‘ cellĂˇk a `zip()` iterĂˇciĂłban.


* **MĹ±kĂ¶dĂ©s:**
1. EllenĹ‘rzi, hogy a kerekĂ­tett Ăştvonal **minden egyes cellĂˇja szabad-e** (`grid_map.is_free(*cell)`). Ha bĂˇrhol akadĂˇlyba ĂĽtkĂ¶zne, azonnal `False`-lal visszatĂ©r.
2. EllenĹ‘rzi a lĂ©pĂ©skapcsolatokat is: a `grid_map.get_neighbors(...)` segĂ­tsĂ©gĂ©vel megnĂ©zi, hogy az egymĂˇst kĂ¶vetĹ‘ pontok valĂłban szomszĂ©dos, szabĂˇlyos lĂ©pĂ©sek-e a rĂˇcson (Ă­gy a robot nem tud "Ăˇtugrani" egy falat vagy illegĂˇlis ugrĂˇst tenni). Ha minden rendben, `True`-t ad vissza.



---

### 6. `smooth_path_bezier(grid_map, path, samples_per_curve=8, diagonal=False)`

A fĹ‘ vezĂ©rlĹ‘fĂĽggvĂ©ny, ami Ă¶sszehozza a generĂˇlĂˇst Ă©s a biztonsĂˇgi ellenĹ‘rzĂ©st.

* **ParamĂ©terek:**
* `grid_map`: A tĂ©rkĂ©p objektum.
* `path`: Az eredeti A* Ăştvonal.
* `samples_per_curve`: A kanyarok finomsĂˇga (alapĂ©rtelmezett: `8` mintapont kanyaroonkĂ©nt).
* `diagonal`: ĂtlĂłs mozgĂˇs engedĂ©lyezĂ©se.


* **BelsĹ‘ vĂˇltozĂłk:**
* `turning_points`: A kiszĹ±rt sarkok listĂˇja.
* `smoothed_path`: A `bezier_curve_points` Ăˇltal legyĂˇrtott simĂ­tott Ăştvonal.


* **MĹ±kĂ¶dĂ©s:**
* Ha az Ăştvonal tĂşl rĂ¶vid (< 3 pont), simĂ­tĂˇs nĂ©lkĂĽl visszaadja.
* Lefuttatja a BĂ©zier-simĂ­tĂˇst (`smoothed_path`).
* MeghĂ­vja az `_is_path_safe`-et. **Ha a simĂ­tott Ăşt biztonsĂˇgos, akkor a simĂ­tott utat adja vissza. Ha viszont a kanyar miatt a robot tĂşl kĂ¶zel menne egy falhoz (vagyis nem biztonsĂˇgos), akkor a kĂłd eldobja az egĂ©szet, Ă©s az eredeti, garantĂˇltan biztonsĂˇgos A* Ăştvonalat adja vissza.**



---

### 7. `smooth_path(grid_map, path, diagonal=False, samples_per_curve=8)`

* **ParamĂ©terek:** Ugyanazok, mint az elĹ‘zĹ‘ fĂĽggvĂ©nynĂ©l.
* **MĹ±kĂ¶dĂ©s:** Ez egy **kompatibilitĂˇsi burkolĂłfĂĽggvĂ©ny (wrapper)**. Ha a projekted mĂˇs moduljai korĂˇbban a `smooth_path` nevet hĂ­vtĂˇk meg, ez a fĂĽggvĂ©ny vĂˇltozatlanul tovĂˇbbĂ­tja az Ă¶sszes paramĂ©tert a `smooth_path_bezier`-nek, Ă­gy nem kell ĂˇtĂ­rnod a tĂ¶bbi fĂˇjlodban a fĂĽggvĂ©nyhĂ­vĂˇsokat.
    """
```

### codes_diploma/astar_project/plots.py

```python
"""Plotting helpers for maps, paths, and comparisons."""
```

### codes_diploma/astar_project/run_experiment.py

```python
"""Parancssori belĂ©pĂ©si pont az A* Ă¶sszehasonlĂ­tĂł kĂ­sĂ©rletekhez."""

from pathlib import Path

from .experiments import run_scenario_comparison, write_results


if __name__ == "__main__":
    output = (
        Path(__file__).resolve().parent
        / "results"
        / "tables"
        / "heuristic_comparison.csv"
    )
    rows = run_scenario_comparison()
    write_results(rows, output)
    print(f"{len(rows)} eredmĂ©ny mentve: {output}")
```

### codes_diploma/astar_project/scenarios.py

```python
"""Reproducible map and planning scenarios."""
```

### codes_diploma/astar_project/tests/test_astar_baseline.py

```python
"""A klasszikus A* alapviselkedĂ©sĂ©nek tesztjei."""

import math
import unittest

from codes_diploma.astar_project.astar_baseline import astar_search
from codes_diploma.astar_project.astar_variants import (
	chebyshev,
	euclidean,
	get_heuristic,
	manhattan,
	octile,
)
from codes_diploma.astar_project.grid_map import GridMap


class TestAstarSearch(unittest.TestCase):
	def test_heuristics_can_be_selected(self):
		self.assertEqual(manhattan((0, 0), (2, 3)), 5)
		self.assertAlmostEqual(euclidean((0, 0), (2, 3)), math.sqrt(13))
		self.assertEqual(chebyshev((0, 0), (2, 3)), 3)
		self.assertAlmostEqual(octile((0, 0), (2, 3)), 3 + 2 * (math.sqrt(2) - 1))
		self.assertIs(get_heuristic("octile"), octile)

	def test_custom_heuristic_can_be_passed(self):
		grid_map = GridMap(width=4, height=1)

		path = astar_search(
			grid_map,
			(0, 0),
			(0, 3),
			heuristic=lambda position, goal: 0,
		)

		self.assertEqual(path, [(0, 0), (0, 1), (0, 2), (0, 3)])

	def test_finds_straight_path(self):
		grid_map = GridMap(width=4, height=1)

		path = astar_search(grid_map, (0, 0), (0, 3))

		self.assertEqual(path, [(0, 0), (0, 1), (0, 2), (0, 3)])

	def test_avoids_obstacle(self):
		grid_map = GridMap(width=5, height=3)
		grid_map.add_obstacle(1, 2)

		path = astar_search(grid_map, (1, 0), (1, 4))

		self.assertIsNotNone(path)
		self.assertNotIn((1, 2), path)
		self.assertEqual(path[0], (1, 0))
		self.assertEqual(path[-1], (1, 4))

	def test_returns_none_when_goal_is_unreachable(self):
		grid_map = GridMap(width=3, height=3)
		for row, column in ((0, 1), (1, 0), (1, 2), (2, 1)):
			grid_map.add_obstacle(row, column)

		path = astar_search(grid_map, (0, 0), (2, 2))

		self.assertIsNone(path)

	def test_diagonal_motion_uses_diagonal_neighbors(self):
		grid_map = GridMap(width=3, height=3)

		path = astar_search(grid_map, (0, 0), (2, 2), diagonal=True)

		self.assertEqual(path, [(0, 0), (1, 1), (2, 2)])

	def test_detailed_result_contains_neighbors_for_each_search_step(self):
		grid_map = GridMap(width=3, height=1)

		result = astar_search(
			grid_map,
			(0, 0),
			(0, 2),
			return_details=True,
		)

		self.assertEqual(result["search_steps"][0]["current"], (0, 0))
		self.assertEqual(result["search_steps"][0]["neighbors"], [(0, 1)])
		self.assertEqual(result["search_steps"][0]["neighbor_scores"][0]["g"], 1.0)
		self.assertEqual(result["search_steps"][0]["neighbor_scores"][0]["h"], 1.0)
		self.assertEqual(result["search_steps"][0]["neighbor_scores"][0]["f"], 2.0)
		self.assertEqual(result["search_steps"][0]["next_position"], (0, 1))
		self.assertEqual(result["search_steps"][0]["priority_queue"][0]["position"], (0, 1))
		self.assertEqual(result["search_steps"][0]["priority_queue"][0]["f"], 2.0)

	def test_rejects_blocked_start_or_goal(self):
		grid_map = GridMap(width=2, height=2)
		grid_map.add_obstacle(0, 0)

		with self.assertRaises(ValueError):
			astar_search(grid_map, (0, 0), (1, 1))


if __name__ == "__main__":
	unittest.main()
```

### codes_diploma/astar_project/tests/test_astar_simulation.py

```python
"""Teszt a statikus A* matplotlib szimulaciohoz."""

import unittest

from codes_diploma.astar_project.astar_baseline import astar_search
from codes_diploma.astar_project.astar_simulation import (
    _parse_position,
    create_demo_map,
    create_robot_trajectory,
    plot_simulation,
)
from codes_diploma.astar_project.path_smoothing import bezier_curve_points


class TestAstarSimulation(unittest.TestCase):
    def test_position_input_is_read_as_row_and_column(self):
        self.assertEqual(_parse_position(" 2, 17 "), (2, 17))

    def test_demo_map_has_a_valid_static_path(self):
        grid_map, start, goal = create_demo_map()

        path = astar_search(grid_map, start, goal, diagonal=True)

        self.assertIsNotNone(path)
        self.assertEqual(path[0], start)
        self.assertEqual(path[-1], goal)
        self.assertTrue(all(grid_map.is_free(row, column) for row, column in path))

    def test_demo_path_creates_continuous_smoothing_points(self):
        grid_map, start, goal = create_demo_map()
        path = astar_search(grid_map, start, goal, diagonal=True)

        curve = bezier_curve_points(path)

        self.assertEqual(curve[0], path[0])
        self.assertEqual(curve[-1], path[-1])
        self.assertNotEqual(curve, path)

    def test_robot_trajectory_starts_and_ends_at_path_points(self):
        grid_map, start, goal = create_demo_map()
        path = astar_search(grid_map, start, goal)

        trajectory = create_robot_trajectory(grid_map, path, steps_per_cell=4)

        self.assertEqual(trajectory[0], grid_map.grid_to_world(*start))
        self.assertEqual(trajectory[-1], grid_map.grid_to_world(*goal))
        self.assertEqual(len(trajectory), 1 + (len(path) - 1) * 4)

    def test_plot_simulation_can_be_created_without_showing_window(self):
        grid_map, start, goal = create_demo_map()
        path = astar_search(grid_map, start, goal)
        trajectory = create_robot_trajectory(grid_map, path)

        figure, robot_animation = plot_simulation(
            grid_map,
            path,
            trajectory,
            start,
            goal,
            show=False,
        )

        self.assertIsNotNone(figure)
        self.assertIsNotNone(robot_animation)
        figure.clf()

    def test_plot_uses_smoothed_trajectory_when_enabled(self):
        grid_map = create_demo_map(width=5, height=5)[0]
        path = [(0, 0), (0, 2), (2, 2)]
        trajectory = create_robot_trajectory(
            grid_map, path, smooth=True, diagonal=True
        )

        figure, _ = plot_simulation(
            grid_map,
            path,
            trajectory,
            path[0],
            path[-1],
            show=False,
            smoothed=True,
        )

        smoothed_line = next(
            line
            for line in figure.axes[1].lines
            if line.get_label() == "Bezier-simitott utvonal"
        )
        self.assertEqual(list(zip(*smoothed_line.get_data())), trajectory)
        figure.clf()

    def test_next_button_advances_the_current_search_cell(self):
        grid_map, start, goal = create_demo_map()
        result = astar_search(
            grid_map,
            start,
            goal,
            diagonal=True,
            return_details=True,
        )
        trajectory = create_robot_trajectory(grid_map, result["path"])

        figure, _ = plot_simulation(
            grid_map,
            result["path"],
            trajectory,
            start,
            goal,
            expanded_nodes=result["expanded_nodes"],
            search_steps=result["search_steps"],
            show=False,
        )

        map_axes = figure.axes[1]
        current_search = next(
            artist
            for artist in map_axes.collections
            if artist.get_label() == "C: aktualis cella"
        )
        first_position = tuple(current_search.get_offsets()[0])
        figure._astar_next_frame()
        second_position = tuple(current_search.get_offsets()[0])

        self.assertNotEqual(first_position, second_position)
        figure.clf()


if __name__ == "__main__":
    unittest.main()
```

### codes_diploma/astar_project/tests/test_dwa_a.py

```python
"""A DWA+A.py A*â€“DWA illesztĂ©sĂ©nek tesztjei."""

import importlib.util
import pathlib
import unittest

from codes_diploma.astar_project.grid_map import GridMap
from codes_diploma.robot import robotconfig, robotstate


def point_to_path_distance(point, path):
	minimum = float("inf")
	for start, end in zip(path, path[1:]):
		dx = end[0] - start[0]
		dy = end[1] - start[1]
		length_squared = dx * dx + dy * dy
		if length_squared == 0:
			projection = start
		else:
			ratio = max(0.0, min(1.0, ((point[0] - start[0]) * dx + (point[1] - start[1]) * dy) / length_squared))
			projection = (start[0] + ratio * dx, start[1] + ratio * dy)
		minimum = min(minimum, ((point[0] - projection[0]) ** 2 + (point[1] - projection[1]) ** 2) ** 0.5)
	return minimum


def load_planner_class():
	file_path = pathlib.Path(__file__).parents[2] / "DWA+A.py"
	spec = importlib.util.spec_from_file_location("dwa_a_module", file_path)
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module.AStarDWAPlanner


class TestDwaA(unittest.TestCase):
	def test_astar_path_becomes_waypoints_and_dwa_pair(self):
		planner_class = load_planner_class()
		grid_map = GridMap(width=5, height=1, resolution=1.0)
		planner = planner_class(grid_map, config=robotconfig(), diagonal=False)

		path = planner.plan_global((0.1, 0.1), (4.1, 0.1))
		result = planner.plan_local(robotstate(x=0.5, y=0.5))

		self.assertEqual(len(path), 5)
		self.assertIn(result["target"], planner.waypoints)
		self.assertEqual(result["target"], planner.waypoints[planner.waypoint_index])
		self.assertEqual(len(result["best_pair"]), 4)
		self.assertTrue(all(
			point_to_path_distance(point, planner.bezier_path) < 1e-9
			for point in planner.waypoints
		))

	def test_waypoint_changes_only_after_reaching_active_point(self):
		planner_class = load_planner_class()
		grid_map = GridMap(width=5, height=1, resolution=1.0)
		planner = planner_class(grid_map, config=robotconfig(), diagonal=False, waypoint_tolerance=0.1)
		planner.plan_global((0.1, 0.1), (4.1, 0.1), smooth=False)

		planner.plan_local(robotstate(x=0.5, y=0.5))
		self.assertEqual(planner.waypoint_index, 1)

		active_waypoint = planner.waypoints[planner.waypoint_index]
		planner.plan_local(robotstate(x=active_waypoint[0], y=active_waypoint[1]))
		self.assertEqual(planner.waypoint_index, 2)

	def test_goal_returns_stop_command(self):
		planner_class = load_planner_class()
		grid_map = GridMap(width=3, height=1, resolution=1.0)
		planner = planner_class(grid_map, config=robotconfig(), diagonal=False)
		planner.plan_global((0.1, 0.1), (2.1, 0.1), smooth=False)

		goal = planner.waypoints[-1]
		result = planner.plan_local(robotstate(x=goal[0], y=goal[1]))

		self.assertTrue(result["finished"])
		self.assertEqual(result["best_pair"], [0.0, 0.0, 0.0, 0.0])


if __name__ == "__main__":
	unittest.main()
```

### codes_diploma/astar_project/tests/test_dynamic_obstacle_crossing.py

```python
"""Deterministikus teszt oldalrol keresztezo mozgo akadallyal."""

import unittest

from codes_diploma.DWA import optimisation
from codes_diploma.robot import Goal, Obstacle, robotconfig, robotstate


class TestDynamicObstacleCrossing(unittest.TestCase):
	def test_dwa_reacts_to_crossing_obstacle(self):
		config = robotconfig()
		state = robotstate(x=0.5, y=0.0, irany=0.0)
		goal = Goal(3.0, 0.0)

		clear_pair, _ = optimisation(config, state, goal, [])
		crossing_obstacle = Obstacle(1.5, -0.5, radius=0.15, vx=0.0, vy=0.2)
		obstacle_pair, safe_pairs = optimisation(config, state, goal, [crossing_obstacle])

		self.assertIsNotNone(clear_pair)
		self.assertIsNotNone(obstacle_pair)
		self.assertTrue(safe_pairs)
		self.assertLess(obstacle_pair[0], clear_pair[0])
		self.assertGreaterEqual(obstacle_pair[0], 0.0)


if __name__ == "__main__":
	unittest.main()
```

### codes_diploma/astar_project/tests/test_experiments.py

```python
"""Az A* heurisztika- Ă©s mozgĂˇsmĂłd-Ă¶sszehasonlĂ­tĂˇs tesztjei."""

import unittest

from codes_diploma.astar_project.experiments import (
    build_experiment_scenarios,
    compare_heuristics,
    run_scenario_comparison,
)


class TestExperiments(unittest.TestCase):
    def test_all_heuristics_are_compared_in_both_motion_modes(self):
        rows = run_scenario_comparison()

        self.assertEqual(len(rows), 4 * 2 * 4)
        self.assertEqual(
            {row["heuristic"] for row in rows},
            {"manhattan", "euclidean", "chebyshev", "octile"},
        )
        self.assertEqual({row["diagonal"] for row in rows}, {False, True})

    def test_non_diagonal_mode_rejects_diagonal_only_map(self):
        grid_map, start, goal = build_experiment_scenarios()["diagonal_only"]

        rows = compare_heuristics(grid_map, start, goal, diagonal=False)

        self.assertTrue(all(not row["success"] for row in rows))

    def test_corner_cutting_is_not_used_when_diagonal_is_enabled(self):
        grid_map, start, goal = build_experiment_scenarios()["corner_cutting"]

        rows = compare_heuristics(grid_map, start, goal, diagonal=True)

        self.assertTrue(all(row["success"] for row in rows))
        for row in rows:
            self.assertNotIn((2, 2), row["path"])


if __name__ == "__main__":
    unittest.main()
```

### codes_diploma/astar_project/tests/test_grid_map.py

```python
"""A GridMap alapmuveleteinek tesztjei."""

import unittest

from codes_diploma.astar_project.grid_map import GridMap


class TestGridMap(unittest.TestCase):
	def test_diagonal_corner_cutting_is_rejected(self):
		grid_map = GridMap(width=3, height=3)
		grid_map.add_obstacle(0, 1)
		grid_map.add_obstacle(1, 0)

		neighbors = grid_map.get_neighbors(0, 0, diagonal=True)

		self.assertNotIn((1, 1), neighbors)

	def test_inflate_obstacles_marks_nearby_cells(self):
		grid_map = GridMap(width=5, height=5, resolution=0.1)
		grid_map.add_obstacle(2, 2)

		grid_map.inflate_obstacles(0.1)

		self.assertEqual(grid_map.grid[1][1], 1)
		self.assertEqual(grid_map.grid[3][3], 1)
		self.assertTrue(grid_map.is_free(0, 0))


if __name__ == "__main__":
	unittest.main()
```

### codes_diploma/astar_project/tests/test_path_smoothing.py

```python
"""Az utvonal-simitas tesztjei."""

import unittest

from codes_diploma.astar_project.grid_map import GridMap
from codes_diploma.astar_project.path_smoothing import (
	_is_path_safe,
	_cut_point,
	bezier_curve_points,
	smooth_path,
)


class TestPathSmoothing(unittest.TestCase):
	def test_keeps_a_straight_path_unchanged(self):
		grid_map = GridMap(width=5, height=1)
		path = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]

		self.assertEqual(smooth_path(grid_map, path), path)

	def test_creates_a_bezier_path_between_turning_points(self):
		grid_map = GridMap(width=5, height=5)

		path = smooth_path(grid_map, [(0, 0), (0, 2), (2, 2)], diagonal=True)

		self.assertEqual(path[0], (0, 0))
		self.assertEqual(path[-1], (2, 2))
		self.assertTrue(
			all(
				grid_map.is_free(round(row), round(column))
				for row, column in path
			)
		)

	def test_uses_all_points_in_a_dynamic_order_curve(self):
		grid_map = GridMap(width=5, height=5)
		path = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]

		smoothed_path = smooth_path(grid_map, path, diagonal=True)
		curve = bezier_curve_points(path, samples_per_segment=15)

		self.assertEqual(smoothed_path[0], path[0])
		self.assertEqual(smoothed_path[-1], path[-1])
		self.assertGreater(len(curve), len(path))
		self.assertNotEqual(curve[1], path[1])

	def test_keeps_a_path_around_an_obstacle(self):
		grid_map = GridMap(width=5, height=3)
		grid_map.add_obstacle(1, 2)
		path = [(1, 0), (0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (1, 4)]

		result = smooth_path(grid_map, path)

		self.assertEqual(result[0], path[0])
		self.assertEqual(result[-1], path[-1])
		self.assertNotIn((1, 2), result)

	def test_rejects_non_neighbor_jump(self):
		grid_map = GridMap(width=5, height=1)

		self.assertFalse(_is_path_safe(grid_map, [(0, 0), (0, 2)]))

	def test_bezier_cut_point_respects_maximum_distance(self):
		cut_point = _cut_point((0.0, 2.0), (0.0, 0.0), 1.5)

		self.assertAlmostEqual(cut_point[0], 0.0)
		self.assertAlmostEqual(cut_point[1], 0.5)


if __name__ == "__main__":
	unittest.main()
```

### codes_diploma/astar_project/tests/test_robot_and_dwa.py

```python
"""A robot.py Ă©s a DWA.py cĂ©lzott tesztjei."""

import unittest

from codes_diploma.DWA import optimisation
from codes_diploma.robot import Obstacle, Goal, get_robot_kinematics, robotconfig, robotstate


class TestRobotAndDWA(unittest.TestCase):
	def test_robot_kinematics(self):
		config = robotconfig()
		linear, angular = get_robot_kinematics(10.0, 10.0, config)

		self.assertAlmostEqual(linear, 0.33)
		self.assertAlmostEqual(angular, 0.0)

	def test_original_parameters_are_preserved(self):
		config = robotconfig()

		self.assertEqual(config.r_kerek, 0.033)
		self.assertEqual(config.b, 0.08)
		self.assertEqual(config.w_kerek_max, 15)
		self.assertEqual(config.a_max, 2)
		self.assertEqual(config.dt, 0.1)
		self.assertEqual(config.predict_time, 3)
		self.assertEqual(config.rob_radius, 0.1)

	def test_dwa_returns_original_pair_format(self):
		best_pair, safe_pairs = optimisation(
			robotconfig(),
			robotstate(),
			Goal(2.0, 0.0),
			[],
		)

		self.assertIsNotNone(best_pair)
		self.assertTrue(safe_pairs)
		self.assertEqual(len(best_pair), 4)

	def test_moving_obstacle(self):
		obstacle = Obstacle(1.0, 2.0, radius=0.1, vx=0.5)

		obstacle.move(2.0)

		self.assertEqual((obstacle.x, obstacle.y), (2.0, 2.0))


if __name__ == "__main__":
	 unittest.main()
```

### codes_diploma/astar_project/tests/test_simulation.py

```python
"""A grafikus szimulacio grafika nelkuli tesztjei."""

import unittest

from codes_diploma.simulation import create_scene


class TestSimulation(unittest.TestCase):
	def test_scene_contains_static_and_moving_obstacles(self):
		grid_map, start_cell, goal_cell, start, goal, state, static_obstacles, dynamic_obstacles = create_scene()

		self.assertIsNotNone(grid_map)
		self.assertNotEqual(start, goal)
		self.assertTrue(static_obstacles)
		self.assertTrue(dynamic_obstacles)
		self.assertTrue(dynamic_obstacles[0].vx != 0.0 or dynamic_obstacles[0].vy != 0.0)


if __name__ == "__main__":
	unittest.main()
```

### codes_diploma/ASTAR_PROJEKT_FOLYAMATBRA.gv

```
digraph AStarCurrentCode {
    graph [
        label="A* jelenlegi kodjanak fuggvenyhivasai"
        labelloc=t
        labeljust=c
        fontsize=22
        fontname="Arial Bold"
        rankdir=TB
        splines=ortho
        nodesep=0.35
        ranksep=0.55
        pad=0.25
        bgcolor="white"
    ]

    node [
        shape=box
        style="rounded,filled"
        fontname="Arial"
        fontsize=11
        margin="0.16,0.10"
        color="#475569"
        penwidth=1.5
    ]

    edge [
        fontname="Arial"
        fontsize=9
        color="#64748b"
        penwidth=1.2
        arrowsize=0.7
    ]

    subgraph cluster_files {
        label="Megvalositott fajlok"
        fontname="Arial Bold"
        fontsize=14
        color="#166534"
        style="rounded"
        bgcolor="#f0fdf4"

        grid_file [label="grid_map.py\nGridMap osztaly\n2D racsterkep", fillcolor="#dcfce7", color="#15803d"]
        astar_file [label="astar_baseline.py\nklasszikus A*", fillcolor="#dcfce7", color="#15803d"]
        variants_file [label="astar_variants.py\nvalaszthato heurisztikak", fillcolor="#dcfce7", color="#15803d"]
        experiments_file [label="experiments.py\n4 palya x 2 mozgasmĂłd x\n4 heurisztika", fillcolor="#dcfce7", color="#15803d"]
        runner_file [label="run_experiment.py\nCSV eredmenymentes", fillcolor="#dcfce7", color="#15803d"]
        smoothing_file [label="path_smoothing.py\nmasodfoku Bezier-simitas", fillcolor="#dcfce7", color="#15803d"]
        simulation_file [label="astar_simulation.py\nmatplotlib szimulacio", fillcolor="#dcfce7", color="#15803d"]
    }

    start [label="astar_search(...)\nbemenet: grid_map, start, goal, diagonal, heuristic\nreturn_details=True a szimulaciohoz", shape=parallelogram, fillcolor="#dbeafe", color="#2563eb"]
    settings [label="Beallitasi ablak\nmeretek, resolution, start, cel\natlos mozgas, heurisztika\nautomatikus lejatszas", fillcolor="#ede9fe", color="#7c3aed"]

    subgraph cluster_runtime {
        label="astar_search() teljes futasi folyamata"
        fontname="Arial Bold"
        fontsize=14
        color="#2563eb"
        style="rounded"
        bgcolor="#eff6ff"

        inside [label="grid_map.is_inside(...)\nstart es cel a terkepen belul?", fillcolor="#dbeafe", color="#2563eb"]
        free [label="grid_map.is_free(...)\nstart es cel szabad?", fillcolor="#dbeafe", color="#2563eb"]
        invalid [label="Hiba\nValueError", shape=parallelogram, fillcolor="#fee2e2", color="#dc2626"]
    initialize [label="2. Kereses elokeszitese\nopen_list = []\ncame_from = {}\ng_costs[start] = 0", fillcolor="#dbeafe", color="#2563eb"]
    first_heuristic [label="_heuristic vagy sajat heuristic(start, goal)\nkezdo f_cost kiszamitasa", fillcolor="#dbeafe", color="#2563eb"]
    add_start [label="Kezdo cella bekerul\naz open_list listaba", fillcolor="#dbeafe", color="#2563eb"]

        has_nodes [label="Van meg elem\naz open_list listaban?", shape=diamond, fillcolor="#dbeafe", color="#2563eb"]
        choose [label="Legkisebb prioritasi elem\nbest_node = min(open_list)\nopen_list.remove(best_node)", fillcolor="#dbeafe", color="#2563eb"]
        read_best [label="Az elem adatainak kiolvasasa\nf_cost | g_cost | current_position", fillcolor="#dbeafe", color="#2563eb"]
        old_entry [label="Dragabb regi bejegyzes?\ncurrent_g_cost > g_costs[current_position]", shape=diamond, fillcolor="#dbeafe", color="#2563eb"]
        goal_check [label="A current_position\na celcella?", shape=diamond, fillcolor="#dbeafe", color="#2563eb"]
        neighbors [label="grid_map.get_neighbors(...)\ncsak szabad szomszedok", fillcolor="#dbeafe", color="#2563eb"]
        movement [label="_movement_cost(current, neighbor)\negyenes vagy atlos lepes", fillcolor="#dbeafe", color="#2563eb"]
        new_g [label="new_g_cost =\ncurrent_g_cost + movement_cost", fillcolor="#dbeafe", color="#2563eb"]
        better [label="Jobb az uj ut?\nnew_g_cost < regi koltseg", shape=diamond, fillcolor="#dbeafe", color="#2563eb"]
        update [label="Adatok frissitese\ncame_from[neighbor] = current_position\ng_costs[neighbor] = new_g_cost", fillcolor="#dbeafe", color="#2563eb"]
        neighbor_heuristic [label="_heuristic vagy sajat heuristic(neighbor, goal)\nf_cost = new_g_cost + h_cost", fillcolor="#dbeafe", color="#2563eb"]
        add_neighbor [label="A* hozzaadja a szomszedot\naz open_list listahoz", fillcolor="#dbeafe", color="#2563eb"]
        no_path [label="return None\nnincs elerheto ut", shape=parallelogram, fillcolor="#fee2e2", color="#dc2626"]
    reconstruct [label="_reconstruct_path(came_from, current_position)\ncelbol visszafele koveti az elozo cellakat", fillcolor="#dcfce7", color="#15803d"]
    result [label="A* eredmeny\npath + expanded_nodes + search_steps", shape=parallelogram, fillcolor="#dcfce7", color="#15803d"]
    }

    subgraph cluster_simulation {
        label="astar_simulation.py jelenlegi hivasai"
        fontname="Arial Bold"
        fontsize=13
        color="#7c3aed"
        style="rounded"
        bgcolor="#faf5ff"

        simulation_start [label="run_simulation()\nszimulacio inditasa", fillcolor="#ede9fe", color="#7c3aed"]
        demo_map [label="create_demo_map()\nismert statikus terkep\nstart es cel", fillcolor="#ede9fe", color="#7c3aed"]
        planning_data [label="expanded_nodes\nA* altal vizsgalt cellak", fillcolor="#ede9fe", color="#7c3aed"]
        trajectory [label="create_robot_trajectory()\nA* cellautvonal ->\nvilagkoordinatas robotpontok", fillcolor="#ede9fe", color="#7c3aed"]
        smoothing [label="smooth_path()\nvalodi kanyarok\nmasodfoku Bezier\nakadalyellenorzessel", fillcolor="#ede9fe", color="#7c3aed"]
        plot [label="plot_simulation()\negy egyszeru frissitesi ciklus\nprioritasi sor + robotmozgas", fillcolor="#ede9fe", color="#7c3aed"]
        draw [label="draw_map()\nakadalyok, start, cel, tengelyek", fillcolor="#ede9fe", color="#7c3aed"]
        animation [label="robot pont + nyom\nFuncAnimation frissitese", shape=parallelogram, fillcolor="#ede9fe", color="#7c3aed"]

        simulation_start -> settings
        settings -> demo_map [label="Alkalmaz"]
        demo_map -> grid_inflate [label="robot_radius"]
        grid_inflate -> start [label="kitagitott GridMap, start, goal"]
        result -> planning_data [label="expanded_nodes"]
        result -> smoothing [label="path, ha bekapcsolva"]
        result -> trajectory [label="path, ha kikapcsolva"]
        smoothing -> trajectory [label="simĂ­tott path"]
        planning_data -> plot [label="vizsgalt cellak"]
        trajectory -> plot [label="trajectory"]
        plot -> draw
        plot -> animation
    }

    subgraph cluster_experiments {
        label="experiments.py Ă¶sszehasonlĂ­tĂˇs"
        fontname="Arial Bold"
        fontsize=13
        color="#0f766e"
        style="rounded"
        bgcolor="#f0fdfa"

        scenario_maps [label="build_experiment_scenarios()\nopen_space, corridor\ncorner_cutting, diagonal_only", fillcolor="#ccfbf1", color="#0f766e"]
        comparison [label="compare_heuristics()\ndiagonal = False / True\nManhattan, Euclidean,\nChebyshev, Octile", fillcolor="#ccfbf1", color="#0f766e"]
        safety_cases [label="SarokvĂˇgĂˇs ellenĹ‘rzĂ©se\nĂ©s nincs Ăştvonal eset", shape=diamond, fillcolor="#ccfbf1", color="#0f766e"]
        csv_output [label="write_results()\nheuristic_comparison.csv", shape=parallelogram, fillcolor="#ccfbf1", color="#0f766e"]
        figure_output [label="generate_comparison_figures.py\noriginal_simulation tĂ©rkĂ©p\nstraight Ă©s diagonal PNG pontokkal", shape=parallelogram, fillcolor="#ccfbf1", color="#0f766e"]
        simulation_figure_output [label="generate_simulation_heuristic_comparison.py\ncreate_scene + obstacle inflation\nAStarDWAPlanner.plan_global()\ntwo-panel simulation figure", shape=parallelogram, fillcolor="#ccfbf1", color="#0f766e"]

        runner_file -> scenario_maps
        scenario_maps -> comparison
        comparison -> safety_cases
        comparison -> csv_output
        comparison -> figure_output
        comparison -> simulation_figure_output
    }

    grid_file -> start [label="GridMap objektum"]
    astar_file -> start [label="belepesi fuggveny"]
    variants_file -> start [label="heuristic"]
    variants_file -> comparison [label="4 heurisztika"]
    astar_file -> comparison [label="astar_search"]
    grid_file -> scenario_maps [label="GridMap pĂˇlyĂˇk"]
    experiments_file -> comparison [label="kĂ­sĂ©rleti logika"]
    runner_file -> csv_output [label="parancssori futtatĂˇs"]
    smoothing_file -> smoothing [label="smooth_path"]
    simulation_file -> simulation_start [label="szimulacio belepesi pont"]
    simulation_start -> settings [label="UI bemenetek"]

    robot_core_file [label="robot.py\nrobotstate, robotconfig\nkinematika, akadaly", fillcolor="#ffedd5", color="#c2410c"]
    dwa_file [label="DWA.py\npairstochoose, safepairs\noptimisation", fillcolor="#ffedd5", color="#c2410c"]
    hybrid_file [label="DWA+A.py\nAStarDWAPlanner\nwaypoint-kovetes", fillcolor="#ffedd5", color="#c2410c"]
    simulation_dwa_file [label="simulation.py\nMatplotlib animacio\nmozgo akadalyak", fillcolor="#ffedd5", color="#c2410c"]
    robot_start [label="AStarDWAPlanner.plan_global()\nstart/goal vilagkoordinataban", shape=parallelogram, fillcolor="#fed7aa", color="#c2410c"]
    robot_path [label="astar_search()\nracsutvonal -> vilagkoordinatas waypointok", fillcolor="#fed7aa", color="#c2410c"]
    local_start [label="AStarDWAPlanner.plan_local()\nrobotstate + akadalyok", fillcolor="#fed7aa", color="#c2410c"]
    dwa_window [label="safepairs()\ndinamikus kereksebesseg-ablak", fillcolor="#fed7aa", color="#c2410c"]
    dwa_sensor [label="get_dist_on_trajectory()\n3 m szenzorhatar + 180 fokos FOV\nmozgo akadaly pozicioja t idoben", fillcolor="#fed7aa", color="#c2410c"]
    dwa_admissible [label="AdmissableVelocity()\nmegallhato-e az utkozes elott?", shape=diamond, fillcolor="#fed7aa", color="#c2410c"]
    dwa_rollout [label="optimisation()\nheading + tavolsag + sebesseg pontozasa", fillcolor="#fed7aa", color="#c2410c"]
    dwa_command [label="best_pair\n[v, w, w_L, w_R]", shape=parallelogram, fillcolor="#ffedd5", color="#c2410c"]
    robot_core_file -> dwa_file [label="robotmodell"]
    dwa_file -> hybrid_file [label="lokalis DWA"]
    hybrid_file -> simulation_dwa_file [label="szimulacios ciklus"]
    hybrid_file -> robot_start [label="globalis terv"]
    robot_start -> robot_path
    robot_path -> local_start
    local_start -> dwa_window
    dwa_window -> dwa_sensor
    dwa_sensor -> dwa_admissible
    dwa_admissible -> dwa_rollout [label="igen"]
    dwa_admissible -> dwa_window [label="nem: kovetkezo par"]
    dwa_rollout -> dwa_command
    hybrid_file -> local_start [label="waypoint"]

    start -> inside
    inside -> free [label="ervenyes"]
    inside -> invalid [label="nem ervenyes"]
    free -> initialize [label="szabad"]
    free -> invalid [label="foglalt"]
    initialize -> first_heuristic
    first_heuristic -> add_start
    add_start -> has_nodes

    has_nodes -> choose [label="igen"]
    has_nodes -> no_path [label="nem"]
    choose -> read_best
    read_best -> old_entry
    old_entry -> has_nodes [label="igen: kihagy"]
    old_entry -> goal_check [label="nem"]
    goal_check -> reconstruct [label="igen"]
    reconstruct -> result
    goal_check -> neighbors [label="nem"]
    neighbors -> movement
    movement -> new_g
    new_g -> better
    better -> has_nodes [label="nem: nem frissit"]
    better -> update [label="igen"]
    update -> neighbor_heuristic
    neighbor_heuristic -> add_neighbor
    add_neighbor -> has_nodes

    subgraph cluster_grid_calls {
        label="A GridMap aktualis, A* altal hasznalt metodusai"
        fontname="Arial Bold"
        fontsize=13
        color="#15803d"
        style="rounded,dashed"
        bgcolor="#f7fff8"

        grid_inside [label="is_inside(row, column)\nindex hatar ellenorzese", fillcolor="#dcfce7", color="#15803d"]
        grid_free [label="is_free(row, column)\ncell erteke 0?", fillcolor="#dcfce7", color="#15803d"]
        grid_neighbors [label="get_neighbors(row, column, diagonal)\nszabad szomszedok visszaadasa", fillcolor="#dcfce7", color="#15803d"]
        grid_inflate [label="inflate_obstacles(radius)\nrobotbiztonsagi sav", fillcolor="#dcfce7", color="#15803d"]
        directions [label="1. Alapiranyok\nfel, le, balra, jobbra", fillcolor="#dcfce7", color="#15803d"]
        diagonal_check [label="2. diagonal igaz?\n+4 atlos irany", shape=diamond, fillcolor="#dcfce7", color="#15803d"]
        candidate_loop [label="3. Iranyok egyenkenti\nvegigvizsgalasa", fillcolor="#dcfce7", color="#15803d"]
        corner_check [label="Atlos sarokvagas?\nket oldalso cella szabad?", shape=diamond, fillcolor="#dcfce7", color="#15803d"]
        append_neighbor [label="4. Ha szabad:\nneighbors.append(...) ", fillcolor="#dcfce7", color="#15803d"]
        return_neighbors [label="5. return neighbors\nA* ezt kapja vissza", shape=parallelogram, fillcolor="#dcfce7", color="#15803d"]
    }

    inside -> grid_inside [style=dashed, color="#15803d"]
    free -> grid_free [style=dashed, color="#15803d"]
    neighbors -> grid_neighbors [style=dashed, color="#15803d"]
    grid_free -> grid_inside [style=dashed, label="belul van-e?", color="#15803d"]
    grid_neighbors -> directions [color="#15803d"]
    directions -> diagonal_check [color="#15803d"]
    diagonal_check -> candidate_loop [label="nem", color="#15803d"]
    diagonal_check -> candidate_loop [label="igen", color="#15803d"]
    candidate_loop -> grid_free [label="minden iranyra", color="#15803d"]
    grid_free -> corner_check [label="igen: atlos", color="#15803d"]
    grid_free -> append_neighbor [label="igen: egyenes", color="#15803d"]
    corner_check -> append_neighbor [label="nem veszelyes", color="#15803d"]
    corner_check -> candidate_loop [label="veszelyes: kihagy", color="#15803d"]
    grid_free -> candidate_loop [label="nem: kihagy", color="#15803d"]
    append_neighbor -> candidate_loop [label="kovetkezo irany", color="#15803d"]
    candidate_loop -> return_neighbors [label="minden irany kesz", color="#15803d"]
    return_neighbors -> movement [style=dashed, label="szabad szomszedok vissza az A*-nak", color="#15803d"]

    subgraph cluster_ros2 {
        label="ROS 2 / Gazebo robotfĂĽggetlen C++ integrĂˇciĂł"
        fontname="Arial Bold"
        fontsize=14
        color="#0f766e"
        style="rounded"
        bgcolor="#f0fdfa"

        ros_scan [label="/scan LaserScan\nakadĂˇlymĂ©rĂ©sek", fillcolor="#ccfbf1", color="#0f766e"]
        ros_odom [label="/odom Odometry\nx, y, yaw\n+ initial_pose (0.8, 0.8)", fillcolor="#ccfbf1", color="#0f766e"]
        ros_grid [label="astar_dwa_node\n8 x 5 m-es statikus Grid\nkĂ¶r alakĂş akadĂˇlyinflĂˇciĂł", fillcolor="#ccfbf1", color="#0f766e"]
        ros_astar [label="A* globĂˇlis Ăştvonal\nstatikus pĂˇlyĂˇn, Grid cellĂˇkbĂłl\nworld pontok", fillcolor="#ccfbf1", color="#0f766e"]
        ros_waypoint [label="KĂ¶vetkezĹ‘ waypoint\nĂştvonalpont vagy cĂ©l", fillcolor="#ccfbf1", color="#0f766e"]
        ros_dwa [label="DWA rollout\nkerĂ©ksebessĂ©g-dinamikus ablak\nAdmissableVelocity + Alfa/Beta/Gamma", fillcolor="#ccfbf1", color="#0f766e"]
        ros_cmd [label="/cmd_vel Twist\nROSbot vagy Gazebo meghajtĂˇs", shape=parallelogram, fillcolor="#99f6e4", color="#0f766e"]
        ros_markers [label="/astar_dwa_markers MarkerArray\nA* Ăştvonal, cĂ©l, biztonsĂˇgi zĂłnĂˇk,\nLiDAR-pontok, DWA trajektĂłria", shape=parallelogram, fillcolor="#99f6e4", color="#0f766e"]
        ros_map [label="/astar_map OccupancyGrid\nismert tĂ©rkĂ©p + inflĂˇlt akadĂˇlycellĂˇk", shape=parallelogram, fillcolor="#99f6e4", color="#0f766e"]
        ros_goal [label="/goal_pose PoseStamped\nĂşj vilĂˇgkoordinĂˇtĂˇs cĂ©l", fillcolor="#ccfbf1", color="#0f766e"]
        rviz_goal [label="RViz 2D Goal Pose\nkattintĂˇs + irĂˇnyhĂşzĂˇs", fillcolor="#ccfbf1", color="#0f766e"]
        gazebo_gui [label="Gazebo GUI\nWSLg: X11-kompatibilis renderelĂ©s\nfekete kĂ©p esetĂ©n: software_rendering:=true", fillcolor="#fef3c7", color="#d97706"]

        ros_scan -> ros_grid
        ros_odom -> ros_grid
        ros_grid -> ros_astar
        ros_astar -> ros_waypoint
        ros_waypoint -> ros_dwa
        ros_scan -> ros_dwa
        ros_odom -> ros_dwa
        ros_dwa -> ros_cmd
        ros_astar -> ros_markers
        ros_dwa -> ros_markers
        ros_grid -> ros_map
        ros_goal -> ros_astar [label="cĂ©l"]
        rviz_goal -> ros_goal [label="kattintĂˇssal"]
        known_map [label="elĹ‘re ismert statikus akadĂˇlyparamĂ©terek", fillcolor="#ccfbf1", color="#0f766e"]
        moving_obstacle [label="moving_obstacle_node\nSetEntityPose + egyenletes Python-pĂˇlya", fillcolor="#bfdbfe", color="#2563eb"]
        pose_bridge [label="ros_gz_bridge\n/world/dwa_world/set_pose\nROS2 service -> Gazebo", fillcolor="#dbeafe", color="#2563eb"]
        known_map -> ros_astar
        moving_obstacle -> pose_bridge [label="SetEntityPose kĂ©rĂ©s"]
        pose_bridge -> gazebo_gui [style=dashed, label="modell pozĂ­ciĂłja"]
        moving_obstacle -> ros_scan [style=dashed, label="LiDAR-ban megjelenik"]
        gazebo_gui -> ros_scan [style=dashed, label="szimulĂˇciĂłs szenzorok"]
        ros_cmd -> gazebo_gui [style=dashed, label="modell mozgatĂˇsa"]
    }

    labelloc="t"
}
```

### codes_diploma/DWA.py

```python
"""Dinamikus ablakos lokĂˇlis ĂştvonaltervezĂ©s (Dynamic Window Approach - DWA)."""

import math
import numpy as np
from .robot import get_robot_kinematics, robotstate, update


"""
KiszĂˇmĂ­tja a megtett utat az Ă­v mentĂ©n az elsĹ‘ ĂĽtkĂ¶zĂ©sig.
Ha nincs ĂĽtkĂ¶zĂ©s a predict_time alatt, egy nagy Ă©rtĂ©ket ad vissza.
"""
def get_dist_on_trajectory(state, config, w_L, w_R, obstacle_list):
    temp_robot = robotstate(x=state.x, y=state.y, irany=state.irany, w_L=state.w_L, w_R=state.w_R)
    accumulated_dist = 0.0
    v_actual, _ = get_robot_kinematics(w_L, w_R, config)
    
    # --- SZENZOR PARAMĂ‰TEREK ---
    max_sensor_dist = 3.0  # 3 mĂ©terig lĂˇt el a LiDAR
    fov_angle = math.radians(180)  # 180 fokos lĂˇtĂłszĂ¶g elĂ¶l
    
    for t in np.arange(0, config.predict_time, config.dt):
        for obs in obstacle_list:
            # 1. Szenzor szĹ±rĂ©s: Csak azt lĂˇtja, ami kĂ¶zel van
            dist_now = math.hypot(state.x - obs.x, state.y - obs.y)
            if dist_now > max_sensor_dist:
                continue
                
            # 2. FOV szĹ±rĂ©s: Csak azt lĂˇtja, ami elĹ‘tte van (+-90 fok)
            angle_to_obs = math.atan2(obs.y - state.y, obs.x - state.x)
            diff_angle = math.atan2(
                math.sin(angle_to_obs - state.irany),
                math.cos(angle_to_obs - state.irany)
            )
            if abs(diff_angle) > fov_angle / 2:
                continue

            # 3. DINAMIKUS PREDIKCIĂ“: Hol lesz az akadĂˇly 't' idĹ‘ mĂşlva?
            obs_future_x = obs.x + obs.vx * t
            obs_future_y = obs.y + obs.vy * t
            
            dist_centers = math.hypot(temp_robot.x - obs_future_x, temp_robot.y - obs_future_y)
            
            # 4. KĂśLĂ–NVĂLASZTOTT INFLĂCIĂ“: Statikus fal mellett szĹ±k rĂˇhagyĂˇs, mozgĂłnĂˇl teljes
            is_static = (obs.vx == 0.0 and obs.vy == 0.0)
            if is_static:
                collision_threshold = obs.radius + config.rob_radius + getattr(config, "static_safety_margin", 0.01)
            else:
                collision_threshold = config.rob_radius + obs.radius + config.safety_margin
            
            if dist_centers <= collision_threshold:
                return accumulated_dist 
        
        # ĂllapotfrissĂ­tĂ©s az Ă­v mentĂ©n
        update(temp_robot, config, w_L, w_R, config.dt)
        accumulated_dist += abs(v_actual) * config.dt
                
    return 10.0


#############xx FĂ‰KEZĂ‰SI FELTĂ‰TELEK ###############
def AdmissableVelocity(robotconfig, w_L, w_R, state, obstacle_list):
    """
    EllenĹ‘rzi, hogy a robot meg tud-e Ăˇllni az adott Ă­ven az ĂĽtkĂ¶zĂ©s elĹ‘tt.
    """
    # 1. KiszĂˇmĂ­tjuk a tĂˇvolsĂˇgot az Ă­v mentĂ©n az ĂĽtkĂ¶zĂ©sig
    dist_to_obs = get_dist_on_trajectory(state, robotconfig, w_L, w_R, obstacle_list)
    
    # 2. Megkapjuk a lineĂˇris sebessĂ©get (v)
    v, _ = get_robot_kinematics(w_L, w_R, robotconfig)
    
    # FĂ©kezĂ©si feltĂ©tel: |v| <= sqrt(2 * a_max * dist)
    if abs(v) <= math.sqrt(2 * robotconfig.a_max * dist_to_obs):
        return True
    return False


"""        
Ă–sszes vĂˇlaszthatĂł v,w pĂˇr kiszĂˇmolĂˇsa kerekekbĹ‘l szĂˇmĂ­tva
"""
def pairstochoose(robotconfig, robotstate):

    w_dot_max = robotconfig.a_max / robotconfig.r_kerek         # w_dot = a / r
   
    w_L_min_actual = max(robotconfig.w_kerek_min, robotstate.w_L - w_dot_max * robotconfig.dt)
    w_L_max_actual = min(robotconfig.w_kerek_max, robotstate.w_L + w_dot_max * robotconfig.dt)

    w_R_min_actual = max(robotconfig.w_kerek_min, robotstate.w_R - w_dot_max * robotconfig.dt)
    w_R_max_actual = min(robotconfig.w_kerek_max, robotstate.w_R + w_dot_max * robotconfig.dt)
   
    w_L_samples = np.arange(w_L_min_actual, w_L_max_actual + robotconfig.w_kerek_resolution, robotconfig.w_kerek_resolution)
    w_R_samples = np.arange(w_R_min_actual, w_R_max_actual + robotconfig.w_kerek_resolution, robotconfig.w_kerek_resolution)

    all_pairs = []
    for w_L in w_L_samples:
        for w_R in w_R_samples:
            v, w = get_robot_kinematics(w_L, w_R, robotconfig)

            all_pairs.append([v, w, w_L, w_R])
    return all_pairs


########################Ă–sszes lehetsĂ©ges vĂˇlaszthatĂł pĂˇlya eltĂˇrolĂˇsa ami biztonsĂˇgos megĂˇllĂˇst biztosĂ­t#######################x

def safepairs(robotconfig, state, obstacle_list):
    """
    EredĹ‘ keresĂ©si tĂ©r (Vr = Vs â© Vd â© Va):
    KiszĹ±ri azokat a sebessĂ©gpĂˇrokat, amelyek kielĂ©gĂ­tik a megĂˇllĂˇsi feltĂ©telt,
    Ă©s kiszĹ±ri a tolatĂł pĂˇlyĂˇkat (hacsak nincs kifejezetten engedĂ©lyezve a tolatĂˇs).
    """
    allow_reverse = getattr(robotconfig, "allow_reverse", False)
    
    admissible_list = []  # Ebben csak a "jĂł" pĂˇrok lesznek
    
    for pair in pairstochoose(robotconfig, state):
        v = pair[0]
        w_L = pair[2]
        w_R = pair[3]
        
        # ElĹ‘remeneti kĂ©nyszer: ne vĂˇlasszon tolatĂˇst vĂ©szmegoldĂˇskĂ©nt
        if not allow_reverse and v < 0.0:
            continue
            
        if AdmissableVelocity(robotconfig, w_L, w_R, state, obstacle_list):
            admissible_list.append(pair)
                
    return admissible_list


################################################

############# optimalizĂˇciĂł #####################
def optimisation(robotconfig, state, goal, obstacle_list):
    # 1. BiztonsĂˇgos sebessĂ©gpĂˇrok lekĂ©rĂ©se
    safe_list = safepairs(robotconfig, state, obstacle_list)
    
    # Ha nincs biztonsĂˇgos Ăşt (ĂśRES A LISTA -> DEADLOCK)
    if not safe_list:
        # Visszaadunk egy speciĂˇlis jelzĂ©st (None), hogy a fĹ‘ciklus tudja: Recovery kell
        return None, []

    best_score = -float('inf')
    best_pair = None
    
    dist_to_goal = math.hypot(goal.x - state.x, goal.y - state.y)
    v_max_robot = robotconfig.w_kerek_max * robotconfig.r_kerek
    
    # 2. AdaptĂ­v predikciĂł: cĂ©lhoz kĂ¶zeledve vagy Ă©les szĂ¶geltĂ©rĂ©s esetĂ©n dinamikusan rĂ¶vidĂĽl
    adaptive_predict_time = robotconfig.predict_time
    heading_to_goal = math.atan2(goal.y - state.y, goal.x - state.x)
    heading_error = abs(
        math.atan2(
            math.sin(heading_to_goal - state.irany),
            math.cos(heading_to_goal - state.irany),
        )
    )
    
    if dist_to_goal < 1.0:
        adaptive_predict_time = max(0.5, dist_to_goal * 2.0)
    
    alfa = robotconfig.Alfa      # CĂ©lra tartĂˇs sĂşlya
    beta = robotconfig.Beta      # AkadĂˇlykerĂĽlĂ©s sĂşlya
    gamma = robotconfig.Gamma    # SebessĂ©gszabĂˇlyozĂˇs sĂşlya

    for v, w, w_L, w_R in safe_list:  
        # Gyors szimulĂˇciĂł a jĂ¶vĹ‘beli Ăˇllapot becslĂ©sĂ©hez az adaptĂ­v idĹ‘ablak vĂ©gĂ©ig
        temp_robot = robotstate(x=state.x, y=state.y, irany=state.irany, w_L=state.w_L, w_R=state.w_R)
        for _ in np.arange(0, adaptive_predict_time, robotconfig.dt):
            update(temp_robot, robotconfig, w_L, w_R, robotconfig.dt)
        
        # --- PONTOZĂSI LOGIKA ---

        # A: Heading score (IrĂˇnyhiba normalizĂˇlva 0 Ă©s 1 kĂ¶zĂ©, atan2 periodicitĂˇs-kezelĂ©ssel)
        angle_to_goal = getattr(goal, "heading", None)
        if angle_to_goal is None:
            angle_to_goal = math.atan2(goal.y - temp_robot.y, goal.x - temp_robot.x)
            
        error_angle = math.atan2(
            math.sin(angle_to_goal - temp_robot.irany), 
            math.cos(angle_to_goal - temp_robot.irany)
        )
        score_heading = (math.pi - abs(error_angle)) / math.pi
        
        # B: Dist score (AkadĂˇlyoktĂłl valĂł tĂˇvolsĂˇg az Ă­v mentĂ©n)
        score_dist = get_dist_on_trajectory(state, robotconfig, w_L, w_R, obstacle_list)
        
        # C: Velocity score (Szabad haladĂˇs esetĂ©n maximĂˇlis tempĂł, cĂ©l kĂ¶zelĂ©ben dinamikus lebegtetĂ©s)
        slow_down_distance = getattr(goal, "slow_down_distance", 0.8)
        if not getattr(goal, "slow_down", True) and dist_to_goal > slow_down_distance:
            score_vel = v / v_max_robot
        else:
            # Nem engedi a cĂ©lsebessĂ©get 0-ra fulladni, dinamikusabban hĂşz a cĂ©l felĂ©
            v_target = min(v_max_robot, max(0.08, dist_to_goal * 1.4))
            score_vel = 1.0 - (abs(v_target - v) / v_max_robot)

        # VĂ©gsĹ‘ pontszĂˇm kiszĂˇmĂ­tĂˇsa a kĂ¶ltsĂ©gfĂĽggvĂ©ny sĂşlyaival
        score = (alfa * score_heading + 
                 beta * score_dist + 
                 gamma * score_vel)

        if score > best_score:
            best_score = score
            best_pair = [v, w, w_L, w_R]

    return best_pair, safe_list
```

### codes_diploma/DWA+A.py

```python
"""A* globĂˇlis Ăştvonal Ă©s DWA lokĂˇlis vezĂ©rlĂ©s integrĂˇciĂłja."""

from __future__ import annotations  # TĂ­pusannotĂˇciĂłk kĂ©sleltetett kiĂ©rtĂ©kelĂ©se (elĹ‘re hivatkozhatĂł tĂ­pusok)
import math  # Matematikai mĹ±veletekhez (hypot, gyĂ¶kvonĂˇs, trigonometria)
from typing import Any, Dict, List, Optional, Sequence, Tuple

# KĂĽlsĹ‘ projektmodulok importĂˇlĂˇsa a tervezĂ©shez Ă©s konfigurĂˇciĂłhoz
from codes_diploma.astar_project.astar_baseline import astar_search  # DiszkrĂ©t A* keresĹ‘ algoritmus
from codes_diploma.astar_project.path_smoothing import smooth_path  # BĂ©zier-alapĂş saroklekerekĂ­tĹ‘ algoritmus
from codes_diploma.DWA import optimisation, pairstochoose  # DWA sebessĂ©gtĂ©r mintavĂ©telezĂ©s Ă©s kĂ¶ltsĂ©goptimalizĂˇlĂˇs
from codes_diploma.robot import Goal, robotconfig  # CĂ©lpont reprezentĂˇciĂł Ă©s robot fizikai paramĂ©terei
from typing import Tuple  # TĂ­pusjelĂ¶lĂ©sek a tiszta C++-os kĂłdkĂ©phez

# TĂ­pusaliasok a C++ 'using' vagy 'typedef' mintĂˇjĂˇra
Point2D = Tuple[float, float]  # Folytonos vilĂˇgkoordinĂˇta: (x, y) mĂ©terben
GridCoord = Tuple[int, int]  # DiszkrĂ©t tĂ©rkĂ©pkoordinĂˇta: (sor, oszlop) cellaindexben


class AStarDWAPlanner:
    """KĂ©tszintĹ± hibrid ĂştvonaltervezĹ‘ Ă©s mozgĂˇsvezĂ©rlĹ‘ osztĂˇly."""

    def __init__(
        self,
        grid_map: Any,  # Bemeneti foglaltsĂˇgi rĂˇcstĂ©rkĂ©p
        config: Optional[Any] = None,  # Robot dinamikai Ă©s geometriai korlĂˇtai
        diagonal: bool = True,  # EngedĂ©lyezi-e a 8-irĂˇnyĂş (ĂˇtlĂłs) mozgĂˇst az A*-ban
        waypoint_tolerance: float = 0.2,  # AlapĂ©rtelmezett elfogadĂˇsi sugĂˇr egy ponthoz [m]
        waypoint_spacing: float = 0.2,  # Waypointok kĂ¶zĂ¶tti egyenletes tĂˇvolsĂˇg az ĂşjramintavĂ©telezĂ©skor [m]
    ) -> None:
        self.grid_map = grid_map  # TĂ©rkĂ©p elmentĂ©se a koordinĂˇta-transzformĂˇciĂłkhoz
        self.config = config if config is not None else robotconfig()  # KonfigurĂˇciĂł inicializĂˇlĂˇsa
        self.diagonal: bool = diagonal  # ĂtlĂłs szomszĂ©dok engedĂ©lyezĂ©sĂ©nek mentĂ©se
        self.waypoint_tolerance: float = waypoint_tolerance  # NĂ©vleges toleranciasugĂˇr rĂ¶gzĂ­tĂ©se
        self.waypoint_spacing: float = waypoint_spacing  # ĂšjramintavĂ©telezĂ©si lĂ©pĂ©skĂ¶z rĂ¶gzĂ­tĂ©se

        self.path: List[Point2D] = []  # VĂ©gleges, aktĂ­van kĂ¶vetett folytonos Ăştvonal pontjai
        self.astar_path: List[Point2D] = []  # Nyers, tĂ¶rĂ©spontos A* vilĂˇgkoordinĂˇtĂˇk listĂˇja
        self.bezier_path: List[Point2D] = []  # SaroklekerekĂ­tett, simĂ­tott BĂ©zier pontok listĂˇja
        self.waypoints: List[Point2D] = []  # Egyenletesen diszkretizĂˇlt cĂ©lpontok lĂˇncolata
        self.waypoint_index: int = 0  # Az aktuĂˇlisan kĂ¶vetett referencia waypoint sorszĂˇma

    def _current_tolerance(self, state: Any) -> float:
        """KiszĂˇmĂ­tja az adaptĂ­v toleranciĂˇt a cĂ©lhoz mĂ©rt tĂˇvolsĂˇg alapjĂˇn."""
        if not self.waypoints:  # Ha nincs betĂ¶ltve Ăştvonal
            return self.waypoint_tolerance  # Az alapĂ©rtelmezett tĹ±rĂ©ssel tĂ©r vissza

        goal_x, goal_y = self.waypoints[-1]  # A legutolsĂł pont (globĂˇlis vĂ©gcĂ©l) koordinĂˇtĂˇi
        goal_distance: float = math.hypot(goal_x - state.x, goal_y - state.y)  # Robot-vĂ©gcĂ©l tĂˇvolsĂˇg

        # 0.05m Ă©s waypoint_tolerance kĂ¶zĂ© szorĂ­tott, tĂˇvolsĂˇgarĂˇnyos dinamikus tĹ±rĂ©s
        return max(0.05, min(self.waypoint_tolerance, goal_distance * 0.2))

    @staticmethod
    def _create_waypoints(path: Sequence[Point2D], spacing: float = 0.2) -> List[Point2D]:
        """A nyers/simĂ­tott gĂ¶rbĂ©t egyenlĹ‘ Ă­vhosszĂşsĂˇgĂş szakaszokra osztja fel."""
        if not path:  # Ăśres Ăştvonal esetĂ©n
            return []  # Ăśres listĂˇt ad vissza

        waypoints: List[Point2D] = [path[0]]  # A kezdĹ‘pont mindig bekerĂĽl elsĹ‘ waypointkĂ©nt
        remaining_distance: float = spacing  # A kĂ¶vetkezĹ‘ pont lehelyezĂ©sĂ©ig hĂˇtralĂ©vĹ‘ tĂˇvolsĂˇg
        segment_start: Point2D = path[0]  # A vizsgĂˇlt Ăştszakasz kezdĹ‘koordinĂˇtĂˇja

        for segment_end in path[1:]:  # VĂ©giglĂ©pked az Ăştvonal egymĂˇst kĂ¶vetĹ‘ pontjain
            dx: float = segment_end[0] - segment_start[0]  # Szakasz X irĂˇnyĂş hossza
            dy: float = segment_end[1] - segment_start[1]  # Szakasz Y irĂˇnyĂş hossza
            segment_length: float = math.hypot(dx, dy)  # KĂ©t pont kĂ¶zĂ¶tti euklideszi tĂˇvolsĂˇg

            if segment_length == 0.0:  # Ha a kĂ©t egymĂˇst kĂ¶vetĹ‘ pont egybeesik
                continue  # Ătugorjuk a felesleges nullosztĂˇst

            while segment_length >= remaining_distance:  # Ha a szakasz hosszabb a szĂĽksĂ©ges tĂˇvnĂˇl
                ratio: float = remaining_distance / segment_length  # InterpolĂˇciĂłs arĂˇny [0.0, 1.0]
                point: Point2D = (  # BeszĂşrt Ăşj pont kiszĂˇmĂ­tĂˇsa lineĂˇris arĂˇnyosĂ­tĂˇssal
                    segment_start[0] + ratio * dx,  # Ăšj pont X koordinĂˇtĂˇja
                    segment_start[1] + ratio * dy,  # Ăšj pont Y koordinĂˇtĂˇja
                )
                waypoints.append(point)  # Pont hozzĂˇadĂˇsa a diszkrĂ©t lĂˇnchoz

                segment_start = point  # A szakasz Ăşj kezdĹ‘pontja az imĂ©nt beszĂşrt pont lesz
                dx = segment_end[0] - segment_start[0]  # HĂˇtralĂ©vĹ‘ szakasz X tĂˇvolsĂˇgĂˇnak frissĂ­tĂ©se
                dy = segment_end[1] - segment_start[1]  # HĂˇtralĂ©vĹ‘ szakasz Y tĂˇvolsĂˇgĂˇnak frissĂ­tĂ©se
                segment_length = math.hypot(dx, dy)  # HĂˇtralĂ©vĹ‘ szakasz hosszĂˇnak ĂşjraszĂˇmolĂˇsa
                remaining_distance = spacing  # VisszaĂˇllĂ­tjuk a teljes lĂ©pĂ©skĂ¶zt a kĂ¶vetkezĹ‘ ponthoz

            remaining_distance -= segment_length  # Levonjuk a szakaszbĂłl megmaradt tĂ¶rt tĂˇvolsĂˇgot
            segment_start = segment_end  # ĂtlĂ©pĂĽnk a kĂ¶vetkezĹ‘ szakaszra

        if waypoints[-1] != path[-1]:  # Ha a lĂ©pĂ©skĂ¶zĂ¶k miatt a legvĂ©gsĹ‘ pont kimaradt volna
            waypoints.append(path[-1])  # Explicit hozzĂˇadjuk a pontos cĂ©lpontot

        return waypoints  # Visszaadjuk a kiszĂˇmĂ­tott, egyenletes pontlistĂˇt

    def _update_pruned_lookahead_target(self, state: Any) -> Tuple[Point2D, int]:
        """ElvĂ©gzi a szakasz-metszĂ©st (pruning) Ă©s kijelĂ¶li az elĹ‘retekintĹ‘ cĂ©lpontot."""
        search_window: int = 25  # KeresĂ©si ablak mĂ©rete (ennyi pontot vizsgĂˇl elĹ‘re a robot elĹ‘tt)
        end_search: int = min(len(self.waypoints), self.waypoint_index + search_window)  # KeresĂ©s felsĹ‘ indexe

        min_dist: float = float("inf")  # Legkisebb tĂˇvolsĂˇg kezdeti Ă©rtĂ©ke vĂ©gtelenre ĂˇllĂ­tva
        closest_idx: int = self.waypoint_index  # LegkĂ¶zelebbi pont indexĂ©nek tĂˇrolĂłja

        for i in range(self.waypoint_index, end_search):  # Ciklus az elĹ‘retekintĂ©si ablakon
            dist: float = math.hypot(self.waypoints[i][0] - state.x, self.waypoints[i][1] - state.y)  # TĂˇvolsĂˇg mĂ©rĂ©se
            if dist < min_dist:  # Ha talĂˇltunk kĂ¶zelebbi pontot a robot pillanatnyi helyĂ©hez
                min_dist = dist  # ElmentjĂĽk az Ăşj minimĂˇlis tĂˇvolsĂˇgot
                closest_idx = i  # ElmentjĂĽk a legkĂ¶zelebbi pont sorszĂˇmĂˇt

        self.waypoint_index = max(self.waypoint_index, closest_idx)  # MonotonitĂˇs: index nem lĂ©phet vissza

        # AdaptĂ­v elĹ‘retekintĂ©si tĂˇvolsĂˇg a pillanatnyi transzlĂˇciĂłs sebessĂ©g (v) alapjĂˇn: [0.35m - 0.80m]
        lookahead_distance: float = max(0.35, min(0.80, abs(state.v) * 1.2))

        accumulated_dist: float = 0.0  # GĂ¶rbe mentĂ©n kumulĂˇlt Ă­vhossz Ă¶sszegzĹ‘je
        target_idx: int = self.waypoint_index  # A kijelĂ¶lt elĹ‘retekintĂ©si pont indexe

        for i in range(self.waypoint_index, len(self.waypoints) - 1):  # ĂŤvhossz Ă¶sszegzĂ©se a metszett indextĹ‘l
            p1: Point2D = self.waypoints[i]  # Szakasz kezdĹ‘pontja
            p2: Point2D = self.waypoints[i + 1]  # Szakasz vĂ©gpontja
            accumulated_dist += math.hypot(p2[0] - p1[0], p2[1] - p1[1])  # TĂˇvolsĂˇg hozzĂˇadĂˇsa az Ă­vhosszhoz
            if accumulated_dist >= lookahead_distance:  # Ha elĂ©rtĂĽk a sebessĂ©gfĂĽggĹ‘ elĹ‘retekintĂ©st
                target_idx = i + 1  # KijelĂ¶ljĂĽk ezt a pontot kĂ¶zvetlen cĂ©lpontnak
                break  # Megvan a pont, kilĂ©pĂĽnk a ciklusbĂłl
        else:
            target_idx = len(self.waypoints) - 1  # Ha elfogyott a pĂˇlya, a legutolsĂł pontra Ăˇllunk rĂˇ

        return self.waypoints[target_idx], target_idx  # Visszaadjuk a koordinĂˇtĂˇt Ă©s annak indexĂ©t

    def plan_global(
        self,
        start_world: Point2D,  # Start pozĂ­ciĂł vilĂˇgkoordinĂˇtĂˇban (x, y) [m]
        goal_world: Point2D,  # CĂ©l pozĂ­ciĂł vilĂˇgkoordinĂˇtĂˇban (x, y) [m]
        heuristic: Optional[Any] = None,  # Egyedi A* heurisztika fĂĽggvĂ©ny (ha nincs, euklideszi)
        smooth: bool = True,  # EngedĂ©lyezze-e a BĂ©zier Ă­ves simĂ­tĂˇst
        samples_per_curve: int = 8,  # GĂ¶rbĂ©nkĂ©nti mintavĂ©teli pontok szĂˇma a simĂ­tĂˇsnĂˇl
        max_cut_distance: Optional[float] = None,  # SaroklevĂˇgĂˇs maximĂˇlis megengedett tĂˇvolsĂˇga
    ) -> Optional[Tuple[Point2D, ...]]:
        """GlobĂˇlis A* keresĂ©s, saroksimĂ­tĂˇs Ă©s waypoint lĂˇnc generĂˇlĂˇsa."""
        start_grid: GridCoord = self.grid_map.world_to_grid(*start_world)  # Start ĂˇtvĂˇltĂˇsa rĂˇcskoordinĂˇtĂˇra
        goal_grid: GridCoord = self.grid_map.world_to_grid(*goal_world)  # CĂ©l ĂˇtvĂˇltĂˇsa rĂˇcskoordinĂˇtĂˇra

        raw_path: Optional[List[GridCoord]] = astar_search(  # A* ĂştvonalkeresĂ©s futtatĂˇsa a rĂˇcson
            self.grid_map,  # Bemeneti tĂ©rkĂ©p
            start_grid,  # KezdĹ‘cella
            goal_grid,  # CĂ©lcella
            diagonal=self.diagonal,  # 8-irĂˇnyĂş szomszĂ©dsĂˇg vizsgĂˇlata
            heuristic=heuristic,  # Heurisztika ĂˇtadĂˇsa
        )

        if raw_path is None:  # Ha nincs jĂˇrhatĂł Ăşt a start Ă©s a cĂ©l kĂ¶zĂ¶tt
            self.path.clear()  # VĂ©gleges Ăşt ĂĽrĂ­tĂ©se
            self.astar_path.clear()  # Nyers A* Ăşt ĂĽrĂ­tĂ©se
            self.bezier_path.clear()  # SimĂ­tott Ăşt ĂĽrĂ­tĂ©se
            self.waypoints.clear()  # DiszkrĂ©t pontok ĂĽrĂ­tĂ©se
            self.waypoint_index = 0  # Index nullĂˇzĂˇsa
            return None  # TervezĂ©si hiba jelzĂ©se

        # A* cellaindexek visszavĂˇltĂˇsa mĂ©ter alapĂş vilĂˇgkoordinĂˇtĂˇkra
        self.astar_path = [self.grid_map.grid_to_world(r, c) for r, c in raw_path]

        if smooth:  # Ha kĂ©rtĂĽnk saroklekerekĂ­tĂ©st
            if max_cut_distance is None:  # Ha nincs explicit beĂˇllĂ­tva vĂˇgĂˇsi limit
                max_cut_distance = 0.5 * self.grid_map.resolution  # FĂ©l cellĂˇnyi felbontĂˇst engedĂĽnk vĂˇgni

            smoothed_raw_path = smooth_path(  # BĂ©zier simĂ­tĂˇs vĂ©grehajtĂˇsa
                self.grid_map,  # TĂ©rkĂ©p az ĂĽtkĂ¶zĂ©smentes Ă­vekhez
                raw_path,  # Nyers rĂˇcsĂştvonal
                diagonal=self.diagonal,  # ĂtlĂłs mozgĂˇs figyelembevĂ©tele
                samples_per_curve=samples_per_curve,  # ĂŤvmintĂˇk sĹ±rĹ±sĂ©ge
                max_cut_distance=max_cut_distance,  # MaximĂˇlis sarokvĂˇgĂˇsi tĂˇvolsĂˇg
            )
            # SimĂ­tott rĂˇcspontok transzformĂˇlĂˇsa vilĂˇgkoordinĂˇtĂˇkra
            self.bezier_path = [self.grid_map.grid_to_world(r, c) for r, c in smoothed_raw_path]
        else:
            self.bezier_path = list(self.astar_path)  # SimĂ­tĂˇs nĂ©lkĂĽl az A* Ăşt marad

        self.path = list(self.bezier_path)  # AktĂ­v trajektĂłria frissĂ­tĂ©se
        self.waypoints = self._create_waypoints(self.path, self.waypoint_spacing)  # Egyenletes ĂşjramintavĂ©tel
        self.waypoint_index = min(1, len(self.waypoints) - 1)  # Az elsĹ‘ aktĂ­v waypoint

        return tuple(self.path)  # Ăštvonal visszaadĂˇsa konstans tuple formĂˇtumban

    def plan_local(self, state: Any, obstacles: Sequence[Any] = ()) -> Optional[Dict[str, Any]]:
        """Egy vezĂ©rlĂ©si ciklust hajt vĂ©gre: cĂ©lpontot frissĂ­t Ă©s DWA parancsot generĂˇl."""
        if not self.waypoints:  # Ha nincs kĂ¶vethetĹ‘ waypoint generĂˇlva
            return None  # Nincs feladat, visszatĂ©rĂ©s

        if self.reached_goal(state):  # Ha a robot beĂ©rt a legvĂ©gsĹ‘ cĂ©l toleranciakĂ¶rĂ©be
            return {
                "waypoint": self.waypoints[-1],  # ElĂ©rt utolsĂł pont
                "target": self.waypoints[-1],  # CĂ©lkĂ©nt rĂ¶gzĂ­tett utolsĂł pont
                "best_pair": [0.0, 0.0, 0.0, 0.0],  # Nulla sebessĂ©g: robot megĂˇllĂ­tĂˇsa [v, w, ...]
                "safe_pairs": [],  # Nincsenek tovĂˇbbi vizsgĂˇlt Ăˇgak
                "all_pairs": [],  # Nincsenek tovĂˇbbi vizsgĂˇlt Ăˇgak
                "finished": True,  # Sikeres cĂ©lba Ă©rĂ©s flag-je
            }

        current = self.waypoints[self.waypoint_index]
        current_tolerance = self._current_tolerance(state)
        if self.waypoint_index < len(self.waypoints) - 1:
            next_point = self.waypoints[self.waypoint_index + 1]
            to_current = (current[0] - state.x, current[1] - state.y)
            next_direction = (
                next_point[0] - current[0],
                next_point[1] - current[1],
            )
            passed_waypoint = (
                to_current[0] * next_direction[0]
                + to_current[1] * next_direction[1]
                < 0
            )
            if (
                math.hypot(current[0] - state.x, current[1] - state.y)
                <= current_tolerance
                or passed_waypoint
            ) and abs(state.v) <= 0.3:
                self.waypoint_index += 1

        target = self.waypoints[self.waypoint_index]
        is_final_waypoint: bool = self.waypoint_index == len(self.waypoints) - 1
        slow_down_distance: float = 0.5 if is_final_waypoint else 0.35  # VĂ©gcĂ©lnĂˇl korĂˇbban kezdĂĽnk lassĂ­tani

        # LassĂ­tĂˇs engedĂ©lyezĂ©se ha konfigurĂˇlva van, vagy ha a pĂˇlya legvĂ©gĂ©re Ă©rtĂĽnk
        enable_slowdown: bool = (
            getattr(self.config, "enable_waypoint_slowdown", False) or is_final_waypoint
        )

        goal = Goal(  # DWA lokĂˇlis cĂ©lpont objektum pĂ©ldĂˇnyosĂ­tĂˇsa
            target[0],  # CĂ©l X koordinĂˇtĂˇja
            target[1],  # CĂ©l Y koordinĂˇtĂˇja
            self.waypoint_tolerance,  # CĂ©lhoz tartozĂł hibatĹ±rĂ©s
            slow_down=enable_slowdown,  # SebessĂ©gcsĂ¶kkentĂ©si kĂ©nyszer bekapcsolĂˇsa
            slow_down_distance=slow_down_distance,  # LassĂ­tĂˇsi zĂłna sugara
        )

        # DWA sebessĂ©gtĂ©r kiĂ©rtĂ©kelĂ©se: optimĂˇlis sebessĂ©gpĂˇr Ă©s ĂĽtkĂ¶zĂ©smentes alternatĂ­vĂˇk
        best_pair, safe_pairs = optimisation(self.config, state, goal, obstacles)
        all_pairs = pairstochoose(self.config, state)  # Az Ă¶sszes kinematikailag lehetsĂ©ges ablak-mintavĂ©tel

        return {
            "waypoint": self.waypoints[self.waypoint_index],  # AktĂ­v referencia-waypoint
            "target": target,  # DWA Ăˇltal kĂ¶zvetlenĂĽl cĂ©lzott elĹ‘retekintĂ©si pont
            "best_pair": best_pair,  # KivĂˇlasztott optimĂˇlis beavatkozĂłjel: [v, w, ...]
            "safe_pairs": safe_pairs,  # ĂśtkĂ¶zĂ©smentes pĂˇlyĂˇk halmaza (megjelenĂ­tĂ©shez/naplĂłzĂˇshoz)
            "all_pairs": all_pairs,  # Ă–sszes dinamikai ablakba esĹ‘ sebessĂ©gpĂˇr
            "finished": self.reached_goal(state),  # VĂ©gcĂ©l elĂ©rĂ©si ĂˇllapotĂˇnak visszajelzĂ©se
        }

    def reached_goal(self, state: Any) -> bool:
        """MegvizsgĂˇlja, hogy a robot elĂ©rte-e a globĂˇlis vĂ©gcĂ©lt a dinamikus toleranciĂˇn belĂĽl."""
        if not self.waypoints:  # Ha nincs Ăştvonal
            return False  # Nem Ă©rhettĂĽnk cĂ©lba

        goal_x, goal_y = self.waypoints[-1]  # GlobĂˇlis cĂ©l X Ă©s Y pozĂ­ciĂłja
        dist_to_goal: float = math.hypot(goal_x - state.x, goal_y - state.y)  # AktuĂˇlis tĂˇvolsĂˇg a cĂ©lig
        return dist_to_goal <= self._current_tolerance(state)  # TĂˇvolsĂˇg Ă¶sszevetĂ©se a szĹ±kĂ­tett toleranciĂˇval
```

### codes_diploma/KODMAGYARAZATOK.md

```markdown
---

# `astar_project/grid_map.py`

## 1. A `GridMap` feladata

A `GridMap` kĂ©tdimenziĂłs rĂˇcstĂ©rkĂ©pet valĂłsĂ­t meg az A* algoritmus szĂˇmĂˇra. A folytonos vilĂˇgot kis, nĂ©gyzet alakĂş cellĂˇkra osztja. Az A* ezeken a cellĂˇkon keres Ăştvonalat.

Egy cella Ăˇllapota:

- `0`: szabad
- `1`: akadĂˇly
- `2`: ismeretlen

A rĂˇcskoordinĂˇta formĂˇja `(row, column)`, vagyis `(sor, oszlop)`.

## 2. A konstruktor paramĂ©terei

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

- `width`: a tĂ©rkĂ©p szĂ©lessĂ©ge cellĂˇkban.
- `height`: a tĂ©rkĂ©p magassĂˇga cellĂˇkban.
- `resolution`: egy cella fizikai mĂ©rete mĂ©terben.
- `origin_x`, `origin_y`: a rĂˇcs kezdĹ‘pontja a vilĂˇgkoordinĂˇta-rendszerben.
- `unknown`: ha igaz, minden cella kezdetben ismeretlen (`2`); egyĂ©bkĂ©nt szabad (`0`).

A szĂ©lessĂ©gnek, magassĂˇgnak Ă©s felbontĂˇsnak pozitĂ­vnak kell lennie.

## 3. Mit jelent a `resolution`?

A `resolution` egy cella oldalhosszĂˇt jelenti. PĂ©ldĂˇul:

```python
resolution = 0.1
```

esetĂ©n egy cella `0,1 m x 0,1 m`, azaz `10 cm x 10 cm`.

A teljes fizikai tĂ©rkĂ©pmĂ©ret:

```text
szĂ©lessĂ©g = width * resolution
magassĂˇg  = height * resolution
```

EzĂ©rt a kĂ¶vetkezĹ‘ tĂ©rkĂ©p:

```python
GridMap(width=10, height=6, resolution=0.1)
```

fizikailag `1,0 m x 0,6 m` terĂĽletet fed le.

Kisebb felbontĂˇs rĂ©szletesebb tĂ©rkĂ©pet eredmĂ©nyez, de tĂ¶bb cellĂˇt Ă©s tĂ¶bb szĂˇmĂ­tĂˇst jelent. Nagyobb felbontĂˇs gyorsabb, de pontatlanabb lehet, Ă©s keskeny ĂˇtjĂˇrĂłkat vagy kisebb akadĂˇlyokat elveszĂ­thet.

## 4. A belsĹ‘ rĂˇcs

A tĂ©rkĂ©p egy `height` sorbĂłl Ă©s soronkĂ©nt `width` cellĂˇbĂłl ĂˇllĂł listĂˇban tĂˇrolĂłdik:

```python
self.grid[row][column]
```

PĂ©ldĂˇul egy 4 x 3-as tĂ©rkĂ©p kezdetben:

```text
[0, 0, 0, 0]
[0, 0, 0, 0]
[0, 0, 0, 0]
```

A Python-indexelĂ©s miatt az elsĹ‘ cella `(0, 0)`, az utolsĂł pedig `(height - 1, width - 1)`.

## 5. RĂˇcs- Ă©s vilĂˇgkoordinĂˇtĂˇk

A program kĂ©t koordinĂˇtarendszert hasznĂˇl:

- rĂˇcskoordinĂˇta: `(row, column)`, egĂ©sz cellaindexekkel;
- vilĂˇgkoordinĂˇta: `(x, y)`, jellemzĹ‘en mĂ©terben.

A `column` az `x` irĂˇnyhoz, a `row` az `y` irĂˇnyhoz tartozik. A `world_to_grid` Ă©s `grid_to_world` fĂĽggvĂ©nyek fordĂ­tanak a kĂ©t rendszer kĂ¶zĂ¶tt.

## 6. `world_to_grid`

```python
column = floor((x - origin_x) / resolution)
row = floor((y - origin_y) / resolution)
```

A fĂĽggvĂ©ny megkeresi, hogy egy vilĂˇgkoordinĂˇtĂˇjĂş pont melyik cellĂˇba esik.

Ha `resolution=0.1`, az origĂł pedig `(0, 0)`, akkor a `(0.26, 0.14)` pont:

```text
column = floor(0.26 / 0.1) = 2
row    = floor(0.14 / 0.1) = 1
```

ĂŤgy az eredmĂ©ny `(1, 2)`. A `floor` azĂ©rt kell, mert a pontot tartalmazĂł cella indexĂ©t keressĂĽk, nem a legkĂ¶zelebbi cellĂˇt.

## 7. `grid_to_world`

```python
x = origin_x + (column + 0.5) * resolution
y = origin_y + (row + 0.5) * resolution
```

A fĂĽggvĂ©ny egy cella kĂ¶zĂ©ppontjĂˇt adja vissza vilĂˇgkoordinĂˇtĂˇban. A `+0.5` azt jelenti, hogy nem a cella sarkĂˇt, hanem a kĂ¶zepĂ©t hasznĂˇljuk.

PĂ©ldĂˇul `resolution=0.1`, origĂł `(0, 0)` Ă©s cella `(1, 2)` esetĂ©n:

```text
x = (2 + 0.5) * 0.1 = 0.25
 y = (1 + 0.5) * 0.1 = 0.15
```

A kĂ©t ĂˇtalakĂ­tĂˇs nem feltĂ©tlenĂĽl adja vissza ugyanazt a vilĂˇgpontot: a `world_to_grid` egy teljes cellĂˇba kerekĂ­t, a `grid_to_world` pedig annak kĂ¶zĂ©ppontjĂˇt adja vissza.

## 8. CellĂˇk Ă©s akadĂˇlyok

- `is_inside(row, column)`: ellenĹ‘rzi, hogy a cella a tĂ©rkĂ©pen belĂĽl van-e.
- `is_free(row, column)`: akkor igaz, ha a cella a tĂ©rkĂ©pen belĂĽl van Ă©s Ă©rtĂ©ke `0`.
- `add_obstacle(row, column)`: a cellĂˇt akadĂˇllyĂˇ (`1`) teszi.
- `remove_obstacle(row, column)`: a cellĂˇt szabaddĂˇ (`0`) teszi.
- `mark_free(row, column)`: a vizsgĂˇlt cellĂˇt szabadnak (`0`) jelĂ¶li.

A cellĂˇn kĂ­vĂĽli mĂłdosĂ­tĂˇsok `ValueError` kivĂ©telt okoznak.

## 9. `add_obstacle_world`

Ez a fĂĽggvĂ©ny vilĂˇgkoordinĂˇtĂˇban megadott akadĂˇlyt alakĂ­t Ăˇt rĂˇcsos akadĂˇllyĂˇ. ElĹ‘szĂ¶r a kĂ¶zĂ©ppont cellĂˇjĂˇt keresi meg a `world_to_grid` segĂ­tsĂ©gĂ©vel, majd a sugĂˇr alapjĂˇn kĂ¶zeli cellĂˇkat vizsgĂˇl.

A cellĂˇk kĂ¶zĂ©ppontja Ă©s az akadĂˇly kĂ¶zĂ©ppontja kĂ¶zĂ¶tti tĂˇvolsĂˇgot szĂˇmolja. A megfelelĹ‘en kĂ¶zeli cellĂˇkat akadĂˇlynak jelĂ¶li. A `radius + resolution` feltĂ©tel szĂˇndĂ©kosan kissĂ© konzervatĂ­v: biztonsĂˇgi tĂˇvolsĂˇgot is figyelembe vesz.

## 10. `update_from_obstacles`

A fĂĽggvĂ©ny tĂ¶bb akadĂˇlyobjektumbĂłl frissĂ­ti a tĂ©rkĂ©pet. Az objektumoktĂłl `x` Ă©s `y` attribĂştumot vĂˇr, a `radius` pedig opcionĂˇlis. Minden akadĂˇlyt az `add_obstacle_world` dolgoz fel.

## 11. `get_neighbors`

AlapĂ©rtelmezĂ©sben a nĂ©gy fĹ‘irĂˇny szomszĂ©dait vizsgĂˇlja:

```text
    fel
bal     jobb
    le
```

`diagonal=True` esetĂ©n a nĂ©gy ĂˇtlĂłs irĂˇny is engedĂ©lyezett, Ă­gy legfeljebb nyolc szomszĂ©d lehet. A fĂĽggvĂ©ny csak a pĂˇlyĂˇn belĂĽli Ă©s szabad cellĂˇkat adja vissza.

ĂtlĂłs lĂ©pĂ©snĂ©l kĂĽlĂ¶n ellenĹ‘rzi a kĂ©t kĂ¶ztes oldalsĂł cellĂˇt is. Ha pĂ©ldĂˇul a robot egy sarok kĂ¶rĂĽl prĂłbĂˇlna ĂˇtlĂłsan lĂ©pni, de a kĂ©t oldalcellĂˇbĂłl valamelyik akadĂˇly, akkor az ĂˇtlĂłs lĂ©pĂ©st elutasĂ­tja. Ezzel nem lehet kĂ©t akadĂˇlycellĂˇnak a kĂ¶zĂ¶s sarkĂˇn ĂˇtvĂˇgni.

## 12. `inflate_obstacles`

```python
grid_map.inflate_obstacles(radius)
```

Ez a fĂĽggvĂ©ny a robot mĂ©rete miatt biztonsĂˇgi tartalĂ©kot Ă©pĂ­t a tĂ©rkĂ©pbe. Az akadĂˇlycellĂˇk kĂ¶rĂĽli kĂ¶zeli cellĂˇkat is akadĂˇlynak jelĂ¶li.

Ha a rĂˇcsfelbontĂˇs `0,2 m`, a robot sugara pedig `0,08 m`, akkor a program egy cellĂˇnyi kĂ¶rnyezetet is figyelembe vesz, mert a robot nem matematikai pontkĂ©nt mozog. Az A* Ă­gy nem olyan Ăştvonalat tervez, amelynek a kĂ¶zĂ©pvonala ugyan szabad, de a robot szĂ©le mĂˇr hozzĂˇĂ©rne az akadĂˇlyhoz.

Ez a mĹ±velet a tervezĂ©s elĹ‘tt mĂłdosĂ­tja a `GridMap` cellĂˇit. A szimulĂˇciĂłban ezĂ©rt a megjelenĂ­tett szĂĽrke akadĂˇlyterĂĽlet mĂˇr a biztonsĂˇgi zĂłnĂˇt is tartalmazza.

## 13. `print_map`

A tĂ©rkĂ©p egyszerĹ± szĂ¶veges megjelenĂ­tĂ©se:

- `.`: szabad cella
- `#`: akadĂˇly
- `?`: ismeretlen cella
- `S`: kezdĹ‘pont
- `G`: cĂ©lpont

A `start` Ă©s `goal` paramĂ©ter csak a kiĂ­rĂˇst mĂłdosĂ­tja, a tĂ©rkĂ©p belsĹ‘ ĂˇllapotĂˇt nem.

## 14. RĂ¶vid pĂ©lda

```python
example_map = GridMap(width=10, height=6, resolution=0.1)
example_map.add_obstacle(2, 3)
example_map.print_map(start=(0, 0), goal=(5, 9))
```

Itt a tĂ©rkĂ©p 10 x 6 cellĂˇs, minden cella 10 cm x 10 cm, ezĂ©rt a teljes terĂĽlet 1,0 m x 0,6 m. A `(2, 3)` cella akadĂˇllyĂˇ vĂˇlik.

---

# `astar_project/astar_baseline.py`

## 1. A fĂˇjl cĂ©lja

Az `astar_baseline.py` a klasszikus A* algoritmust valĂłsĂ­tja meg a `GridMap` rĂˇcstĂ©rkĂ©pĂ©n. Ez a projekt referenciaalgoritmusa: elĹ‘szĂ¶r egy egyszerĹ±, ellenĹ‘rizhetĹ‘ A* kell, Ă©s csak utĂˇna Ă©rdemes tovĂˇbbfejlesztett heurisztikĂˇkat vagy szomszĂ©dsĂˇgi szabĂˇlyokat vizsgĂˇlni.

Az algoritmus bemenete rĂˇcskoordinĂˇtĂˇkat hasznĂˇl:

```python
start = (sor, oszlop)
goal = (sor, oszlop)
```

A `resolution` itt nem vĂˇltoztatja meg a keresĂ©s cellaszintĹ± logikĂˇjĂˇt. A mozgĂˇsi kĂ¶ltsĂ©gek cellalĂ©pĂ©sekben vannak megadva; a vilĂˇgkoordinĂˇtĂˇkra tĂ¶rtĂ©nĹ‘ ĂˇtvĂˇltĂˇst a `GridMap` vĂ©gzi.

## 2. Az `astar_search` fĂĽggvĂ©ny

```python
astar_search(
    grid_map, start, goal, diagonal=False, return_details=False, heuristic=None
)
```

ParamĂ©terek:

- `grid_map`: a `GridMap` pĂ©ldĂˇnya, amely megmondja, mely cellĂˇk szabadok.
- `start`: kezdĹ‘cella `(row, column)` formĂˇban.
- `goal`: cĂ©lcella `(row, column)` formĂˇban.
- `diagonal`: ha `False`, csak a nĂ©gy fĹ‘irĂˇny hasznĂˇlhatĂł; ha `True`, az ĂˇtlĂłs irĂˇnyok is engedĂ©lyezettek.
- `return_details`: ha `False`, csak az Ăştvonalat adja vissza; ha `True`, az Ăştvonal mellett a tervezĂ©s kĂ¶zben kibĹ‘vĂ­tett cellĂˇkat is visszaadja.
- `heuristic`: opcionĂˇlis, `(position, goal)` paramĂ©terĹ± sajĂˇt heurisztika. Ha nincs megadva, a `diagonal` Ă©rtĂ©ke alapjĂˇn Manhattan- vagy Euklideszi-becslĂ©s fut.

A visszatĂ©rĂ©si Ă©rtĂ©k egy cellĂˇkbĂłl ĂˇllĂł lista, pĂ©ldĂˇul:

```python
[(0, 0), (0, 1), (0, 2)]
```

Az elsĹ‘ elem a kezdĹ‘cella, az utolsĂł a cĂ©lcella. Ha nincs Ăşt, a fĂĽggvĂ©ny `None` Ă©rtĂ©ket ad vissza. Ha a kezdĹ‘- vagy cĂ©lcella Ă©rvĂ©nytelen, illetve akadĂˇly, `ValueError` keletkezik.

## 3. Az A* alapgondolata

Az A* minden vizsgĂˇlt cellĂˇhoz kĂ¶ltsĂ©get rendel:

$$
f(n) = g(n) + h(n)
$$

- `g(n)`: a kezdĹ‘tĹ‘l az aktuĂˇlis cellĂˇig megtett Ăşt tĂ©nyleges kĂ¶ltsĂ©ge.
- `h(n)`: becslĂ©s az aktuĂˇlis cellĂˇtĂłl a cĂ©lig.
- `f(n)`: a teljes becsĂĽlt kĂ¶ltsĂ©g; ezt hasznĂˇlja a keresĂ©s a kĂ¶vetkezĹ‘ cella kivĂˇlasztĂˇsĂˇra.

A prioritĂˇsi sor mindig azt a nyitott cellĂˇt veszi elĹ‘re, amelynek a legkisebb `f` Ă©rtĂ©ke van.

## 4. A prioritĂˇsi sor Ă©s az adatszerkezetek

Az egyszerĹ±bb tanulĂˇsi vĂˇltozat egy sima `open_list` listĂˇt hasznĂˇl. A lista elemei:

```python
(f_cost, g_cost, position)
```

Az elsĹ‘ Ă©rtĂ©k az `f_cost`, ez alapjĂˇn keressĂĽk meg a kĂ¶vetkezĹ‘ cellĂˇt. A `g_cost` az eddig megtett Ăşt kĂ¶ltsĂ©ge, a `position` pedig a cella koordinĂˇtĂˇja. A kivĂˇlasztĂˇs Ă­gy tĂ¶rtĂ©nik:

```python
best_node = min(open_list)
open_list.remove(best_node)
```

Ez kĂ¶nnyebben Ă©rthetĹ‘, mint egy kĂĽlĂ¶n prioritĂˇsi sor hasznĂˇlata: vĂ©gignĂ©zzĂĽk a listĂˇt, kivĂˇlasztjuk a legkisebb tuple-t, majd eltĂˇvolĂ­tjuk.

KĂ©t szĂłtĂˇr tĂˇrolja a keresĂ©s ĂˇllapotĂˇt:

- `g_costs`: az ismert legjobb kĂ¶ltsĂ©g a kezdĹ‘tĹ‘l az adott cellĂˇig;
- `came_from`: minden elĂ©rt cellĂˇhoz eltĂˇrolja, melyik cellĂˇbĂłl Ă©rkeztĂĽnk.

A `came_from` nem a teljes Ăştvonalat tĂˇrolja minden lĂ©pĂ©snĂ©l, hanem szĂĽlĹ‘kapcsolatokat. EzutĂˇn a cĂ©lbĂłl visszafelĂ© kĂ¶vetjĂĽk ezeket a kapcsolatokat, majd megfordĂ­tjuk a listĂˇt.

`return_details=True` esetĂ©n az A* eredmĂ©nye ilyen szĂłtĂˇr:

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

Az `expanded_nodes` a tervezĂ©s megfigyelĂ©sĂ©hez kell. A cellĂˇk sorrendben kerĂĽlnek bele, amikor az A* tĂ©nylegesen kivĂˇlasztja Ă©s feldolgozza Ĺ‘ket. A matplotlib szimulĂˇciĂł ezeket vilĂˇgoskĂ©k pontokkĂ©nt vagy cellakĂ¶zĂ©ppontokkĂ©nt jelenĂ­ti meg.

Az Ăşj `search_steps` minden feldolgozott aktuĂˇlis cellĂˇhoz eltĂˇrolja a
`GridMap.get_neighbors()` Ăˇltal visszaadott szomszĂ©dokat. Ez fontos kĂĽlĂ¶nbsĂ©g:
az A* egy aktuĂˇlis cella Ă¶sszes engedĂ©lyezett szomszĂ©djĂˇt megvizsgĂˇlja, de nem
mindegyikbĹ‘l lesz kĂ¶vetkezĹ‘ feldolgozott cella. A szomszĂ©dok kĂ¶ltsĂ©gĂ©t
Ă¶sszehasonlĂ­tja, majd a prioritĂˇsi sorbĂłl a legjobb `f = g + h` Ă©rtĂ©kĹ± cellĂˇt
vĂˇlasztja ki.

PĂ©ldĂˇul a `(0, 0)` cellĂˇbĂłl a szabad szomszĂ©dok lehetnek `(0, 1)` Ă©s `(1, 0)`.
MindkettĹ‘ megjelenik a `neighbor_scores` adatai kĂ¶zĂ¶tt. Ha `(0, 1)` kapja a
kedvezĹ‘bb prioritĂˇst, akkor ez lesz a kĂ¶vetkezĹ‘ feldolgozott cella, mĂ­g
`(1, 0)` vĂˇrakozĂł jelĂ¶ltkĂ©nt maradhat a `priority_queue` adataiban.

A `priority_queue` ugyanezen lĂ©pĂ©s utĂˇn a mĂ©g vĂˇrakozĂł, Ă©rvĂ©nyes jelĂ¶lteket
tĂˇrolja `f` szerint rendezve. A szimulĂˇciĂł bal oldali panelje ezt a listĂˇt
mutatja. A lista elsĹ‘ eleme az a cella, amelyet az A* a kĂ¶vetkezĹ‘ kĂ¶rben
kivĂˇlasztana. A lista minden kĂ©zi `Kovetkezo` lĂ©pĂ©snĂ©l frissĂĽl, ezĂ©rt a tĂ©rkĂ©p
Ă©s a prioritĂˇsi sorrend egyĂĽtt magyarĂˇzza az Ăştvonal kialakulĂˇsĂˇt.

A szimulĂˇciĂł a prioritĂˇsi panelen kiĂ­rja a `neighbor_scores` Ă©s a
`priority_queue` alapjĂˇn megjelenĂ­tett sĂşlyokat:

- `g`: a starttĂłl a jelĂ¶ltig vezetĹ‘ eddigi kĂ¶ltsĂ©g;
- `h`: a jelĂ¶lttĹ‘l a cĂ©lig becsĂĽlt kĂ¶ltsĂ©g;
- `f`: `g + h`, vagyis az A* Ăˇltal Ă¶sszehasonlĂ­tott teljes becslĂ©s.

PĂ©ldĂˇul egy vĂ­zszintes lĂ©pĂ©snĂ©l, ha a jelĂ¶ltig `g=1,0`, a cĂ©lig becsĂĽlt
tĂˇvolsĂˇg pedig `h=3,0`, akkor `f=4,0`. KĂ©t azonos `f` Ă©rtĂ©kĹ± jelĂ¶lt kĂ¶zĂĽl a
program a tuple-sorrend Ă©s a pillanatnyi prioritĂˇsi lista alapjĂˇn vĂˇlaszt; ez
nem azt jelenti, hogy valamelyik cellĂˇt kihagyta, hanem azt, hogy az egyik
jelĂ¶lt elĹ‘bb kerĂĽl feldolgozĂˇsra.

## 5. A heurisztika

4-szomszĂ©dos keresĂ©snĂ©l a Manhattan-tĂˇvolsĂˇgot hasznĂˇlja:

$$
h(n) = |row_n-row_g| + |column_n-column_g|
$$

Ez azt szĂˇmolja meg, hĂˇny vĂ­zszintes Ă©s fĂĽggĹ‘leges lĂ©pĂ©s kellene akadĂˇlyok nĂ©lkĂĽl.

ĂtlĂłs keresĂ©snĂ©l az alapimplementĂˇciĂł egyszerĹ± Euklideszi heurisztikĂˇt hasznĂˇl:

$$
h(n) = \sqrt{(row_n-row_g)^2 + (column_n-column_g)^2}
$$

Ez lĂ©gvonalbeli becslĂ©st ad az aktuĂˇlis cellĂˇtĂłl a cĂ©lig. Nem szĂˇmol az akadĂˇlyokkal,
ezĂ©rt az akadĂˇlyok miatt tĂ©nylegesen szĂĽksĂ©ges Ăşt nem lehet rĂ¶videbb ennĂ©l.
Az ĂˇtlĂłs mozgĂˇs tĂ©nyleges kĂ¶ltsĂ©ge ettĹ‘l fĂĽggetlenĂĽl `sqrt(2)` marad.

Az `astar_variants.py` tovĂˇbbi, Ă¶sszehasonlĂ­thatĂł fĂĽggvĂ©nyeket tartalmaz:

- `manhattan`: vĂ­zszintes Ă©s fĂĽggĹ‘leges mozgĂˇshoz;
- `euclidean`: lĂ©gvonalbeli becslĂ©s;
- `chebyshev`: az eltĂ©rĹ‘ koordinĂˇtĂˇk kĂ¶zĂĽl a nagyobbik;
- `octile`: egyenes Ă©s `sqrt(2)` kĂ¶ltsĂ©gĹ± ĂˇtlĂłs mozgĂˇshoz.

A kivĂˇlasztott heurisztika az `astar_search(..., heuristic=...)` paramĂ©terrel adhatĂł Ăˇt.
PĂ©ldĂˇul: `astar_search(grid_map, start, goal, diagonal=True, heuristic=octile)`.
SajĂˇt fĂĽggvĂ©nyhez elĂ©g a `(position, goal)` paramĂ©tereket fogadĂł fĂĽggvĂ©ny, pĂ©ldĂˇul
`lambda position, goal: 0`.

## 6. A bemenetek mĂłdosĂ­tĂˇsa a felĂĽleten

A `astar_simulation.py` Tkinter beĂˇllĂ­tĂˇsi ablaka a `Szimulacio inditasa` gombbal
indĂ­tja el a szimulĂˇciĂłt. Itt mĂłdosĂ­thatĂł a tĂ©rkĂ©p szĂ©lessĂ©ge Ă©s magassĂˇga, a
`resolution`, a robot sugara, a start- Ă©s cĂ©lcella, az ĂˇtlĂłs mozgĂˇs, valamint a
heurisztika. Az automatikus lejĂˇtszĂˇs alapĂ©rtelmezĂ©s szerint be van kapcsolva,
Ă­gy a tervezĂ©s Ă©s a robot mozgĂˇsa kattintĂˇs nĂ©lkĂĽl vĂ©gigfut; kikapcsolva a
`Kovetkezo` gombbal lehet lĂ©ptetni.
A start Ă©s a cĂ©l formĂˇtuma `sor,oszlop`, pĂ©ldĂˇul `2,17`.

Az `Utvonal simitasa` kapcsolĂł alapĂ©rtelmezĂ©s szerint be van kapcsolva. Bekapcsolt
Ăˇllapotban az A* ĂştvonalĂˇt a
`path_smoothing.py` dolgozza fel. A jelenlegi megoldĂˇs megkeresi a kĂ¶zel
derĂ©kszĂ¶gĹ± kanyarokat, a valĂłdi kanyarokhoz mĂˇsodfokĂş BĂ©zier-gĂ¶rbĂ©t kĂ©szĂ­t,
majd a mintapontokat kerekĂ­tve ĂĽtkĂ¶zĂ©s Ă©s szomszĂ©dsĂˇg szempontjĂˇbĂłl ellenĹ‘rzi.
Ha a gĂ¶rbe nem biztonsĂˇgos, az eredeti A* Ăştvonal marad meg.

## 7. A mozgĂˇsi kĂ¶ltsĂ©g

Az `_movement_cost` kĂ©t szomszĂ©dos cella kĂ¶zĂ¶tt szĂˇmol:

- egyenes lĂ©pĂ©s kĂ¶ltsĂ©ge: `1.0`;
- ĂˇtlĂłs lĂ©pĂ©s kĂ¶ltsĂ©ge: `sqrt(2)`.

Ha `resolution=0.1`, akkor ezek a cellalĂ©pĂ©sek fizikailag 0,1 mĂ©teres, illetve kĂ¶rĂĽlbelĂĽl 0,1414 mĂ©teres mozgĂˇst jelentenek. Az alapimplementĂˇciĂł kĂ¶ltsĂ©gei azonban cellaegysĂ©gekben maradnak.

## 8. A keresĂ©si ciklus

1. A kezdĹ‘cella bekerĂĽl a prioritĂˇsi sorba.
2. A legkisebb prioritĂˇsĂş cellĂˇt kivesszĂĽk.
3. Ha ez a cĂ©l, a `came_from` kapcsolatokbĂłl visszaĂ©pĂ­tjĂĽk az utat.
4. EgyĂ©bkĂ©nt lekĂ©rjĂĽk a szabad szomszĂ©dokat a `GridMap.get_neighbors` segĂ­tsĂ©gĂ©vel.
5. Minden szomszĂ©dra kiszĂˇmoljuk az Ăşj `g` kĂ¶ltsĂ©get.
6. Ha ez jobb, mint a korĂˇbban ismert kĂ¶ltsĂ©g, frissĂ­tjĂĽk a szĂĽlĹ‘t Ă©s a prioritĂˇst.
7. Ha az `open_list` lista kiĂĽrĂĽl cĂ©l elĂ©rĂ©se nĂ©lkĂĽl, nincs Ăşt.

Az elavult lista-bejegyzĂ©seket ez a feltĂ©tel hagyja figyelmen kĂ­vĂĽl:

```python
if current_g > g_costs[current]:
    continue
```

Erre azĂ©rt van szĂĽksĂ©g, mert egy cellĂˇhoz kĂ©sĹ‘bb jobb Ăşt is Ă©rkezhet, mikĂ¶zben a rĂ©gi bejegyzĂ©s mĂ©g bent marad a listĂˇban. Ez a megoldĂˇs tanulĂˇsi cĂ©lbĂłl egyszerĹ±bb, de nagy tĂ©rkĂ©pen lassabb lehet, mert a `min(open_list)` minden kĂ¶rben vĂ©gignĂ©zi a listĂˇt.

## 8. KonkrĂ©t szĂˇmolĂˇsi pĂ©lda

Legyen a kezdĹ‘cella `(0, 0)`, a cĂ©l `(0, 3)`, Ă©s hasznĂˇljunk 4-szomszĂ©dos keresĂ©st. A kezdĹ‘cellĂˇnĂˇl:

```text
g = 0
h = |0 - 0| + |0 - 3| = 3
f = 0 + 3 = 3
```

Ha az algoritmus a `(0, 1)` cellĂˇba lĂ©p:

```text
g = 1
h = |0 - 0| + |1 - 3| = 2
f = 1 + 2 = 3
```

A `(0, 2)` cellĂˇnĂˇl:

```text
g = 2
h = |0 - 0| + |2 - 3| = 1
f = 2 + 1 = 3
```

A cĂ©l `(0, 3)` elĂ©rĂ©sekor:

```text
g = 3
h = 0
f = 3
```

Ha a kĂ¶zvetlen Ăştban akadĂˇly van, a kĂ¶zvetlen szomszĂ©d nem kerĂĽl be a jelĂ¶ltek kĂ¶zĂ©, Ă©s az A* olyan kerĂĽlĹ‘ cellĂˇkat vizsgĂˇl, amelyek `f` Ă©rtĂ©ke alapjĂˇn Ă­gĂ©retesek.

## 9. TesztelĂ©s

A `tests/test_astar_baseline.py` teszteli:

- az egyenes Ăşt megtalĂˇlĂˇsĂˇt;
- akadĂˇly megkerĂĽlĂ©sĂ©t;
- elĂ©rhetetlen cĂ©l esetĂ©n a `None` eredmĂ©nyt;
- az ĂˇtlĂłs mozgĂˇst;
- a beĂ©pĂ­tett Ă©s egyedi heurisztikĂˇk kivĂˇlasztĂˇsĂˇt;
- a rĂ©szletes `search_steps` Ă©s `priority_queue` adatok lĂ©trejĂ¶ttĂ©t;
- foglalt kezdĹ‘cella elutasĂ­tĂˇsĂˇt.

A tesztek a Python beĂ©pĂ­tett `unittest` moduljĂˇt hasznĂˇljĂˇk, ezĂ©rt kĂĽlĂ¶n tesztkeretrendszer nĂ©lkĂĽl is futtathatĂłk:

```text
python -m unittest codes_diploma.astar_project.tests.test_astar_baseline -v
```

---

# `astar_project/astar_simulation.py`

## 1. A szimulĂˇciĂł cĂ©lja

Az `astar_simulation.py` az A* mĹ±kĂ¶dĂ©sĂ©t mutatja meg egy ismert, statikus tĂ©rkĂ©pen. A tĂ©rkĂ©p mĂˇr elĹ‘re tartalmazza az akadĂˇlyokat, ezĂ©rt az A* a tervezĂ©s elĹ‘tt ismeri a teljes pĂˇlyĂˇt.

Ez a szimulĂˇciĂł nem DWA. Nem vizsgĂˇl sebessĂ©gpĂˇrokat, gyorsulĂˇst, fĂ©kezĂ©st vagy mozgĂł akadĂˇlyokat. A robot egy egyszerĹ±, `0,08 m` sugarĂş kĂ¶r alakĂş testkĂ©nt kĂ¶veti az A* Ăˇltal kĂ©szĂ­tett globĂˇlis Ăştvonalat. A demo az A* ĂˇtlĂłs keresĂ©si mĂłdjĂˇt hasznĂˇlja, ezĂ©rt ahol nincs akadĂˇly, ĂˇtlĂłsan is tud haladni.

```text
GridMap -> A* tervezĂ©si nyom -> A* Ăştvonal -> vilĂˇgkoordinĂˇtĂˇk -> robottrajektĂłria -> matplotlib animĂˇciĂł
```

Ez jĂł elsĹ‘ szimulĂˇciĂł, mert kĂĽlĂ¶n lĂˇthatĂł benne a tĂ©rkĂ©p, a tervezett Ăştvonal Ă©s a robot mozgĂˇsa. KĂ©sĹ‘bb erre lehet rĂˇĂ©pĂ­teni a sebessĂ©get, a fordulĂˇsi korlĂˇtot vagy a teljes robotmodellt.

## 2. `create_demo_map`

```python
grid_map, start, goal = create_demo_map()
```

Ez lĂ©trehoz egy `30 x 20` cellĂˇs tĂ©rkĂ©pet `0,2 m` felbontĂˇssal. A tĂ©rkĂ©p fizikai mĂ©rete:

```text
szĂ©lessĂ©g = 30 * 0,2 m = 6,0 m
magassĂˇg  = 20 * 0,2 m = 4,0 m
```

A fĂĽggvĂ©ny kĂ©t falat helyez el. A falakban szĂˇndĂ©kosan rĂ©sek vannak, ezĂ©rt az A* a nyĂ­lĂˇsokon keresztĂĽl keres kerĂĽlĹ‘utat.

A visszatĂ©rĂ©si Ă©rtĂ©kek:

- `grid_map`: az ismert statikus tĂ©rkĂ©p;
- `start`: kezdĹ‘ rĂˇcscella;
- `goal`: cĂ©l rĂˇcscella.

## 3. RobotmĂ©ret Ă©s akadĂˇlybiztonsĂˇg

A demo robot sugara `0,08 m`. A `create_demo_map()` az akadĂˇlyok felvĂ©tele utĂˇn meghĂ­vja:

```python
grid_map.inflate_obstacles(robot_radius)
```

EzutĂˇn az A* mĂˇr a kitĂˇgĂ­tott akadĂˇlytĂ©rkĂ©pen tervez. A szimulĂˇciĂłban megjelenĂ­tett narancssĂˇrga robot kĂ¶re ugyanekkora sugarĂş, ezĂ©rt a kĂ©pen lĂˇthatĂł robotmĂ©ret Ă©s a tervezĂ©sben hasznĂˇlt biztonsĂˇgi tĂˇvolsĂˇg egymĂˇshoz tartozik.

Az ĂˇtlĂłs sarokvĂˇgĂˇst a `GridMap.get_neighbors()` kĂĽlĂ¶n is tiltja. ĂŤgy kĂ©t akadĂˇlycellĂˇnak a kĂ¶zĂ¶s sarkĂˇn sem tud Ăˇthaladni a robot kĂ¶zĂ©ppontja.

## 4. `create_robot_trajectory`

```python
trajectory = create_robot_trajectory(grid_map, path)
```

Az A* Ăştvonala cellĂˇk listĂˇja. A robot mozgĂˇsĂˇhoz vilĂˇgkoordinĂˇtĂˇk kellenek, ezĂ©rt minden cellĂˇt a `grid_to_world` alakĂ­t Ăˇt a cella kĂ¶zĂ©ppontjĂˇra.

EzutĂˇn a fĂĽggvĂ©ny kĂ©t egymĂˇst kĂ¶vetĹ‘ cellakĂ¶zĂ©ppont kĂ¶zĂ¶tt `steps_per_cell` kĂ¶ztes pontot kĂ©szĂ­t. AlapĂ©rtelmezĂ©sben `steps_per_cell=4`, ezĂ©rt `resolution=0.2` esetĂ©n egy egyenes cellalĂ©pĂ©s 0,2 mĂ©ter, egy szimulĂˇciĂłs lĂ©pĂ©s pedig kĂ¶rĂĽlbelĂĽl 0,05 mĂ©ter.

A fĂĽggvĂ©ny nem Ăşj Ăştvonalat keres. Csak az A* Ăˇltal mĂˇr kiszĂˇmolt cellaĂştvonalbĂłl kĂ©szĂ­t folytonosabb megjelenĂ­tĂ©si mozgĂˇst.

## 5. `draw_map`

```python
draw_map(axes, grid_map, start, goal)
```

Kirajzolja az akadĂˇlycellĂˇkat szĂĽrke nĂ©gyzetkĂ©nt, a startot zĂ¶ld pontkĂ©nt, a cĂ©lt piros pontkĂ©nt, valamint a vilĂˇgkoordinĂˇta-tengelyeket mĂ©terben.

Az akadĂˇlycellĂˇk helye a rĂˇcsbĂłl Ă­gy alakul Ăˇt:

```text
x = origin_x + column * resolution
y = origin_y + row * resolution
```

ĂŤgy a tĂ©glalap pontosan a megfelelĹ‘ fizikai cellaterĂĽletre kerĂĽl.

## 6. `plot_simulation`

```python
figure, robot_animation = plot_simulation(
    grid_map, path, trajectory, start, goal
)
```

Ez egy szĂˇndĂ©kosan rĂ¶vid, kĂ©tpaneles megjelenĂ­tĹ‘, amely a DWA-szimulĂˇciĂł egyszerĹ± mĹ±kĂ¶dĂ©sĂ©hez hasonlĂłan egyetlen fĹ‘ animĂˇciĂłs ciklusban frissĂ­ti az ĂˇbrĂˇt:

1. a bal oldalon az aktuĂˇlis prioritĂˇsi sort mutatja `g`, `h`, `f` Ă©rtĂ©kekkel;
2. ugyanitt kiĂ­rja a prioritĂˇsi fĂĽggvĂ©nyt: $f(n)=g(n)+h(n)$, ahol `g(n)` az eddigi Ăşt kĂ¶ltsĂ©ge, `h(n)` a cĂ©lhoz tartozĂł becslĂ©s, `f(n)` pedig a teljes prioritĂˇsi Ă©rtĂ©k;
3. ĂˇtlĂłs keresĂ©snĂ©l a kĂ¶nnyebben Ă©rtelmezhetĹ‘ Euklideszi heurisztikĂˇt hasznĂˇlja: `h(n) = sqrt(dr^2 + dc^2)`, ahol `dr` Ă©s `dc` az aktuĂˇlis cella Ă©s a cĂ©l sor-, illetve oszlopkĂĽlĂ¶nbsĂ©ge;
4. ugyanitt lĂˇthatĂłk a lĂ©pĂ©skĂ¶ltsĂ©gek: egyenes lĂ©pĂ©s `1,0`, ĂˇtlĂłs lĂ©pĂ©s `sqrt(2)`, valamint a demo-paramĂ©terek;
5. a jobb oldalon kirajzolja az akadĂˇlyokat, a vizsgĂˇlt cellĂˇkat, az aktuĂˇlis keresĂ©si cellĂˇt, a startot Ă©s a cĂ©lt;
6. a tervezĂ©s vĂ©gĂ©n megjelenĂ­ti az eredeti Ă©s szĂĽksĂ©g esetĂ©n a BĂ©zier-simĂ­tott Ăştvonalat;
7. a robot a kivĂˇlasztott trajektĂłriĂˇt Ă©s annak nyomĂˇt animĂˇlja;
8. az automatikus lejĂˇtszĂˇs mellett a `Kovetkezo` Ă©s `Ujrakezdes` gomb, illetve a jobb nyĂ­l kĂ©zi vezĂ©rlĂ©st ad.

A prioritĂˇsi panel a tĂ©nyleges `priority_queue` tartalmĂˇt mutatja, legfeljebb
nyolc vĂˇrakozĂł elemmel. A tĂ©rkĂ©pen a halvĂˇny pontok a feldolgozott
`expanded_nodes` cellĂˇk, a narancssĂˇrga jelĂ¶lĹ‘ az aktuĂˇlis keresĂ©si cella, a
robot pedig csak a tervezĂ©si szakasz utĂˇn jelenik meg. A kĂłd nem hasznĂˇl kĂĽlĂ¶n
`X`, `N` vagy `O` szĂ¶veges cellajelĂ¶lĂ©seket.

JelĂ¶lĂ©sek:

- `C`: az animĂˇciĂł adott pillanatĂˇban ezt a cellĂˇt dolgozza fel az A*;
- a halvĂˇny pontok: az A* Ăˇltal mĂˇr vizsgĂˇlt cellĂˇk;
- a kĂ©k szaggatott vonal: a vĂ©gsĹ‘, visszaĂ©pĂ­tett Ăştvonal.

A `show=False` hasznĂˇlhatĂł tesztelĂ©skor, Ă­gy az Ăˇbra lĂ©trejĂ¶n, de nem nyĂ­lik meg grafikus ablak. A szimulĂˇciĂł kĂ©zi lĂ©ptetĂ©sĹ±, ezĂ©rt a keresĂ©s Ă©s a robotmozgĂˇs egyarĂˇnt kĂ¶nnyen kĂ¶vethetĹ‘. A megjelenĂ­tĹ‘ nem modellez sebessĂ©get, gyorsulĂˇst vagy valĂłdi robotkinematikĂˇt; a cĂ©lja az A* mĹ±kĂ¶dĂ©sĂ©nek szemlĂ©ltetĂ©se.

## 7. `run_simulation`

```python
run_simulation()
```

Ez a szimulĂˇciĂł belĂ©pĂ©si pontja:

```text
beĂˇllĂ­tĂˇsi ablak
    -> create_demo_map
    -> astar_search(diagonal=..., heuristic=..., return_details=True)
    -> expanded_nodes megjelenitese
    -> smooth_path (ha engedĂ©lyezett)
    -> create_robot_trajectory
    -> plot_simulation
```

A tĂ©nyleges belĂ©pĂ©si sorrendben a `run_simulation()` elĹ‘szĂ¶r a Tkinter
beĂˇllĂ­tĂˇsi ablakot nyitja meg. Az alkalmazott Ă©rtĂ©kekbĹ‘l a `_run_simulation()`
lĂ©trehozza a demo tĂ©rkĂ©pet, kivĂˇlasztja a heurisztikĂˇt, lefuttatja az A*-ot,
opcionĂˇlisan simĂ­t, majd lĂ©trehozza a trajektĂłriĂˇt Ă©s az animĂˇciĂłt.

A fĂˇjl kĂ¶zvetlen futtatĂˇsa:

```text
python -m codes_diploma.astar_project.astar_simulation
```

## 8. Mit mutat Ă©s mit nem mutat?

Mutatja:

- az ismert statikus rĂˇcstĂ©rkĂ©pet;
- az A* Ăˇltal vizsgĂˇlt cellĂˇkat (`expanded_nodes`) Ă©s az aktuĂˇlis keresĂ©si cellĂˇt;
- az aktuĂˇlis prioritĂˇsi sor rĂ©szletes adatait (`g`, `h`, `f`);
- az akadĂˇlykerĂĽlĹ‘ A* globĂˇlis Ăştvonalat;
- az eredeti Ă©s a tĂ©nylegesen hasznĂˇlt Ăştvonalat, ha a simĂ­tĂˇs engedĂ©lyezett;
- a rĂˇcs- Ă©s vilĂˇgkoordinĂˇtĂˇk kapcsolatĂˇt;
- a robot mozgĂˇsĂˇt az Ăştvonalon;
- az Ăştvonalat Ă©s a robot nyomĂˇt.

Nem mutatja:

- a robot valĂłdi gyorsulĂˇsĂˇt Ă©s fĂ©kezĂ©sĂ©t;
- a differenciĂˇlis hajtĂˇs kinematikĂˇjĂˇt;
- a DWA sebessĂ©gpĂˇr-keresĂ©sĂ©t;
- Ăşj akadĂˇlyok Ă©rzĂ©kelĂ©sĂ©t futĂˇs kĂ¶zben;
- mozgĂł akadĂˇlyok elkerĂĽlĂ©sĂ©t.

Ezek kĂ©sĹ‘bbi fejlesztĂ©si fĂˇzisok lehetnek, de nem tartoznak ehhez az elsĹ‘ statikus A* demonstrĂˇciĂłhoz.

## 9. TesztelĂ©s

A `tests/test_astar_simulation.py` ellenĹ‘rzi a demo Ăştvonalat, a trajektĂłria kezdĹ‘- Ă©s vĂ©gpontjĂˇt, a pontok szĂˇmĂˇt, valamint a matplotlib Ăˇbra ablak nĂ©lkĂĽli lĂ©trehozĂˇsĂˇt.

```text
python -m unittest codes_diploma.astar_project.tests.test_astar_simulation -v
```

---

# `astar_project/path_smoothing.py`

## A jelenlegi kĂłd

```python
def _bezier_point(start_point, control_point, end_point, parameter):
    """Egy pontot szĂˇmol egy mĂˇsodfokĂş BĂ©zier-gĂ¶rbĂ©n."""


def _remove_straight_points(path):
    """EltĂˇvolĂ­tja az egyenes szakaszok kĂ¶ztes pontjait."""


def bezier_curve_points(path, samples_per_segment=10):
    """Folytonos pontokat kĂ©szĂ­t a valĂłdi kanyarok kĂ¶rĂĽl."""


def _is_path_safe(grid_map, path, diagonal=False):
    """KerekĂ­tett cellĂˇkon ellenĹ‘rzi az akadĂˇlyt Ă©s a szomszĂ©dsĂˇgot."""


def smooth_path_bezier(grid_map, path, samples_per_curve=8, diagonal=False):
    """BiztonsĂˇgos mĂˇsodfokĂş BĂ©zier-simĂ­tĂˇst kĂ©szĂ­t."""


def smooth_path(grid_map, path, diagonal=False, samples_per_curve=8):
    """Kompatibilis belĂ©pĂ©si pont a BĂ©zier-simĂ­tĂˇshoz."""
```

## 1. A fĂˇjl cĂ©lja

Ez a modul az A* Ăˇltal kĂ©szĂ­tett rĂˇcsos Ăştvonalat prĂłbĂˇlja kevĂ©sbĂ© tĂ¶rdelttĂ©
tenni. Nem keres Ăşj utat, Ă©s nem mĂłdosĂ­tja az A* `g`, `h` vagy `f` kĂ¶ltsĂ©geit.
UtĂłfeldolgozĂˇskĂ©nt mĹ±kĂ¶dik:

```text
A* Ăştvonal
    -> egyenes kĂ¶ztes pontok eltĂˇvolĂ­tĂˇsa
    -> hĂˇrom kontrollpont meghatĂˇrozĂˇsa minden kanyarnĂˇl
    -> mĂˇsodfokĂş BĂ©zier-pontok mintavĂ©tele
    -> ellenĹ‘rzĂ©shez cellĂˇkra kerekĂ­tĂ©s
    -> rĂˇcsos akadĂˇly- Ă©s szomszĂ©dsĂˇgi ellenĹ‘rzĂ©s
    -> elfogadott simĂ­tott Ăşt vagy eredeti Ăştvonal
```

## 2. Az Ăştvonal adatai

Az A* Ăştvonala `(row, column)` pĂˇrok listĂˇja. PĂ©ldĂˇul:

```python
[(0, 0), (0, 1), (0, 2), (1, 2)]
```

Ez azt jelenti, hogy a robot kĂ©t cellĂˇt vĂ­zszintesen halad, majd egy sort
lefelĂ© fordul. A rĂˇcskoordinĂˇta nem mĂ©terben megadott vilĂˇgkoordinĂˇta. Ha a
`GridMap` `resolution` Ă©rtĂ©ke `0.2`, akkor egy rĂˇcslĂ©pĂ©s `0.2 m`.

## 3. A mĂˇsodfokĂş BĂ©zier-matematika

Egy kanyarhoz hĂˇrom pontot hasznĂˇlunk:

- `P0`: a kanyar kezdĹ‘pontja;
- `P1`: az eredeti A* kanyarcellĂˇja, vagyis a kontrollpont;
- `P2`: a kanyar vĂ©gpontja.

A kĂ©plet:

$$
B(t)=(1-t)^2P_0+2(1-t)tP_1+t^2P_2,
\qquad 0\leq t\leq 1.
$$

A `t` Ă©rtĂ©ke `0` Ă©s `1` kĂ¶zĂ¶tt vĂˇltozik. A gĂ¶rbe a `P0` pontbĂłl indul, a
`P2` pontba Ă©rkezik, Ă©s a `P1` kontrollpont felĂ© hajlik.

### KonkrĂ©t szĂˇmolĂˇsi pĂ©lda

Legyen:

```text
P0 = (0, 0)
P1 = (0, 2)
P2 = (2, 2)
t  = 0,5
```

Ekkor a sorĂ©rtĂ©k:

```text
(1 - 0,5)^2 * 0 + 2 * (1 - 0,5) * 0,5 * 0 + 0,5^2 * 2
= 0,5
```

Az oszlopĂ©rtĂ©k:

```text
(1 - 0,5)^2 * 0 + 2 * (1 - 0,5) * 0,5 * 2 + 0,5^2 * 2
= 1,5
```

A gĂ¶rbe mintapontja tehĂˇt `(0,5; 1,5)`. Ez folytonos koordinĂˇta, amelyet a
megjelenĂ­tĹ‘ megtart, a biztonsĂˇgi ellenĹ‘rzĂ©s viszont egĂ©sz rĂˇcscellĂˇra kerekĂ­t.

## 4. A fontos fĂĽggvĂ©nyek

### `_bezier_point(start_point, control_point, end_point, parameter)`

A mĂˇsodfokĂş BĂ©zier-kĂ©pletet alkalmazza egyetlen `t` Ă©rtĂ©kre. A `weight` a
`1 - t`, ezĂ©rt a hĂˇrom pont sĂşlya fokozatosan vĂˇltozik a gĂ¶rbe mentĂ©n.

### `_remove_straight_points(path)`

A hĂˇrom egymĂˇst kĂ¶vetĹ‘ pontbĂłl kĂ©pzett irĂˇnyvektorok kereszt-szorzatĂˇt vizsgĂˇlja.
Ha az Ă©rtĂ©k nulla, a pontok egy egyenesre esnek, ezĂ©rt a kĂ¶zĂ©psĹ‘ pontot nem kell
simĂ­tani. ĂŤgy egyenes ĂştvonalnĂˇl nem keletkezik felesleges gĂ¶rbe.

### `bezier_curve_points(path, samples_per_segment=10)`

ElĹ‘szĂ¶r eltĂˇvolĂ­tja az egyenes szakaszok kĂ¶ztes pontjait, majd minden valĂłdi
kanyarhoz hĂˇrom pontot vĂˇlaszt. A szomszĂ©dos Ă©lek felezĹ‘pontjai adjĂˇk a `P0`
Ă©s `P2` kezdĹ‘- Ă©s vĂ©gpontot, az eredeti kanyarcellĂˇja pedig a `P1` kontrollpont.
Az eredmĂ©ny folytonos, lebegĹ‘pontos rĂˇcskoordinĂˇtĂˇkbĂłl Ăˇll.

### `_is_path_safe(grid_map, path, diagonal=False)`

EgĂ©sz cellĂˇkra kerekĂ­ti a gĂ¶rbe pontjait, majd ellenĹ‘rzi, hogy minden cella
szabad-e, Ă©s minden egymĂˇst kĂ¶vetĹ‘ cella a `GridMap` engedĂ©lyezett szomszĂ©dja-e.
ĂŤgy az akadĂˇlyba lĂłgĂł gĂ¶rbe Ă©s a tiltott ĂˇtlĂłs sarokvĂˇgĂˇs elutasĂ­tĂˇsra kerĂĽl.

### `smooth_path_bezier(grid_map, path, samples_per_curve=8, diagonal=False)`

A rĂˇcstĂ©rkĂ©ppel egyĂĽtt meghĂ­vja a folytonos BĂ©zier-simĂ­tĂˇst, majd biztonsĂˇgi
ellenĹ‘rzĂ©st vĂ©gez. Ha a simĂ­tĂˇs veszĂ©lyes, az eredeti A* Ăştvonalat adja vissza.

### `smooth_path(grid_map, path, diagonal=False, samples_per_curve=8)`

Kompatibilis belĂ©pĂ©si pont, amely a `smooth_path_bezier` fĂĽggvĂ©nyt hĂ­vja.
AzĂ©rt maradt meg, mert az `astar_simulation.py` Ă©s a korĂˇbbi hĂ­vĂłk ezt a nevet
hasznĂˇljĂˇk.

### `bezier_curve_points(path, samples_per_segment=10)`

Ez a fĂĽggvĂ©ny folytonos, lebegĹ‘pontos BĂ©zier-pontokat kĂ©szĂ­t. A szimulĂˇciĂł ezt
hasznĂˇlja a robot trajektĂłriĂˇjĂˇhoz.

## 5. Kapcsolat a szimulĂˇciĂłval

Az `astar_simulation.py` simĂ­tĂˇs nĂ©lkĂĽl az eredeti A* cellautat hasznĂˇlja.
SimĂ­tĂˇskor a `smooth_path()` biztonsĂˇgi ellenĹ‘rzĂ©ssel folytonos BĂ©zier-pontokat
ad vissza, amelyeket a `create_robot_trajectory()` vilĂˇgkoordinĂˇtĂˇra alakĂ­t.
Ha a biztonsĂˇgi ellenĹ‘rzĂ©s elutasĂ­tja a gĂ¶rbĂ©t, az eredeti A* Ăştvonal marad.
A `plot_simulation()` `smoothed=True` jelzĹ‘je ilyenkor a BĂ©zier-vonalat a
folytonos robottrajektĂłriĂˇbĂłl rajzolja, ezĂ©rt a megjelenĂ­tett Ăşt nem esik vissza
az eredeti rĂˇcsos vonalra akkor sem, ha a kerekĂ­tett cellalista vĂˇltozatlan marad.
A piros vonal mindig a tĂ©nylegesen hasznĂˇlt, biztonsĂˇgos trajektĂłriĂˇt mutatja.

Az automatikus lejĂˇtszĂˇs alapĂ©rtelmezett idĹ‘zĂ­tĂ©se `250 ms` a tervezĂ©si
kĂ©pkockĂˇknĂˇl Ă©s `60 ms` a robotmozgĂˇsnĂˇl. A nem simĂ­tott mozgĂˇs cellĂˇnkĂ©nt nĂ©gy
kĂ¶ztes mintapontot kap; a simĂ­tott mozgĂˇs szakaszonkĂ©nt hĂşsz BĂ©zier-mintĂˇt
hasznĂˇl, hogy a gĂ¶rbe rĂˇcsos ellenĹ‘rzĂ©se ne ugorjon Ăˇt cellĂˇkat.

## 6. TesztelĂ©s Ă©s korlĂˇtok

A `test_path_smoothing.py` ellenĹ‘rzi, hogy:

- a BĂ©zier-simĂ­tĂˇs eltĂ©rhet az eredeti tĂ¶rĂ¶tt ĂşttĂłl;
- az egyenes Ăştvonal vĂˇltozatlan marad;
- akadĂˇly mellett az Ăştvonal nem kerĂĽlhet tiltott cellĂˇba;
- a kezdĹ‘- Ă©s vĂ©gpont megmarad.

FuttatĂˇs:

```text
python -m unittest codes_diploma.astar_project.tests.test_path_smoothing -v
```

SzĹ±k folyosĂłban vagy akadĂˇly sarkĂˇnĂˇl a gĂ¶rbe elutasĂ­thatĂł. Ilyenkor a modul
nem erĹ‘lteti a simĂ­tĂˇst, hanem az eredeti A* Ăştvonalat tartja meg.

---

# A kĂ¶zĂ¶s robotmag Ă©s az A*â€“DWA elsĹ‘ integrĂˇciĂłja

## 1. A fĂˇjlok cĂ©lja

A `codes_diploma/robot.py` a robotmodellt, a `codes_diploma/DWA.py` a lokĂˇlis DWA-t, a `codes_diploma/DWA+A.py` pedig az A* Ă©s a DWA kapcsolatĂˇt tartalmazza.

## 2. Adatfolyam Ă©s fontos adatok

Az A* bemenete `GridMap`, valamint a start- Ă©s cĂ©lpont vilĂˇgkoordinĂˇtĂˇja. A `DWA+A.py` az `astar_search()` eredmĂ©nyĂ©t waypointlistĂˇvĂˇ alakĂ­tja, majd a `robotstate` Ă©s `Obstacle` lista alapjĂˇn meghĂ­vja az `optimisation()` fĂĽggvĂ©nyt. A kimenet az eredeti `[v, w, w_L, w_R]` forma.

`robotstate` mezĹ‘i: `x`, `y`, `v`, `w`, `irany`, `w_L` Ă©s `w_R`. Az `Obstacle` kĂ¶r alakĂş; a `vx` Ă©s `vy` mezĹ‘k az egyenletes mozgĂˇs sebessĂ©gĂ©t jelentik. A `move(dt)` frissĂ­ti az akadĂˇly helyĂ©t.

## 3. RobotparamĂ©terek Ă©s kinematika

Az alapĂ©rtelmezett `robotconfig` kerĂ©ksugara `0,033 m`, tengelytĂˇvja `0,08 m`, maximĂˇlis kerĂ©ksebessĂ©ge `15 rad/s`, idĹ‘lĂ©pĂ©se `0,1 s`, elĹ‘retekintĂ©se `3 s`, robotrĂˇdiusza `0,10 m`, biztonsĂˇgi margĂłja pedig `0,15 m`.

A differenciĂˇlis hajtĂˇs Ă¶sszefĂĽggĂ©sei:

$$
v = r\frac{\omega_L + \omega_R}{2},
\qquad
\omega = r\frac{\omega_R - \omega_L}{b}
$$

Itt `r` a kerĂ©k sugara mĂ©terben, `b` a tengelytĂˇv mĂ©terben, `omega_L` Ă©s `omega_R` a kerekek radiĂˇn/mĂˇsodperc egysĂ©gĹ± szĂ¶gsebessĂ©gei, `v` a robot lineĂˇris sebessĂ©ge mĂ©ter/mĂˇsodpercben, `omega` pedig a fordulĂˇsi sebessĂ©g radiĂˇn/mĂˇsodpercben. PĂ©ldĂˇul `10 rad/s` azonos kerĂ©ksebessĂ©gnĂ©l:

$$
v = 0{,}033\frac{10+10}{2} = 0{,}33\ \mathrm{m/s},
\qquad
\omega = 0{,}033\frac{10-10}{0{,}08} = 0\ \mathrm{rad/s}
$$

Ez egyenes haladĂˇst jelent. Az `update()` az eredeti kĂ©plettel korlĂˇtozza a kerĂ©ksebessĂ©g vĂˇltozĂˇsĂˇt: egy `0,1 s` idĹ‘lĂ©pĂ©sben legfeljebb `(2 / 0,033) * 0,1` radiĂˇn/mĂˇsodperc vĂˇltozĂˇs engedĂ©lyezett.

## 4. A DWA dĂ¶ntĂ©si menete

A `pairstochoose()` Ă©s a `safepairs()` az aktuĂˇlis kerĂ©ksebessĂ©g kĂ¶rĂĽl dinamikus ablakot kĂ©pez. A `safepairs()` csak elĹ‘rehaladĂł (`v >= 0`) pĂˇrokat engedĂ©lyez. Az `optimisation()` a kĂ¶ztes waypointok elĹ‘tt bĂˇtran halad, Ă©s csak az utolsĂł `0,2 m`-en igazĂ­tja a sebessĂ©get; a vĂ©gsĹ‘ cĂ©lpontnĂˇl a lassĂ­tĂˇsi zĂłna `0,5 m`.

Egy `0,10 m` sugarĂş robot, egy `0,20 m` sugarĂş akadĂˇly Ă©s `0,15 m` margĂłja akkor ĂĽtkĂ¶zik, ha a kĂ¶zĂ©ppontok tĂˇvolsĂˇga legfeljebb `0,10 + 0,20 + 0,15 = 0,45 m`. A mozgĂł akadĂˇlynĂˇl a tĂˇvolsĂˇgvizsgĂˇlat az adott predikciĂłs idĹ‘pontra szĂˇmolt pozĂ­ciĂłt hasznĂˇlja.

Az eredeti logika szerint a `get_dist_on_trajectory()` csak a robot szenzorhatĂˇrĂˇn belĂĽli (`3 m`) Ă©s a robot elĹ‘tti `180` fokos lĂˇtĂłmezĹ‘ben lĂ©vĹ‘ akadĂˇlyokat vizsgĂˇlja. A mozgĂł akadĂˇly pozĂ­ciĂłja `x + vx * t`, illetve `y + vy * t` alapjĂˇn vĂˇltozik. Az `AdmissableVelocity()` ezutĂˇn a megĂˇllĂ­thatĂłsĂˇgot is ellenĹ‘rzi:

$$
|v| \leq \sqrt{2 a_{max} d}
$$

`v` a pillanatnyi lineĂˇris sebessĂ©g, `a_max = 2,0 m/s^2` a lassulĂˇsi korlĂˇt, `d` pedig az elsĹ‘ ĂĽtkĂ¶zĂ©sig szĂˇmĂ­tott tĂˇvolsĂˇg. PĂ©ldĂˇul `d = 0,5 m` esetĂ©n a megengedett sebessĂ©g legfeljebb `sqrt(2 * 2,0 * 0,5) = 1,41 m/s`. Ha egy trajektĂłria nem teljesĂ­ti ezt, a DWA elutasĂ­tja.

Az Ă©rvĂ©nyes sebessĂ©gpĂˇrok pontszĂˇma az aktuĂˇlis `Alfa = 5`, `Beta = 2`, `Gamma = 3` sĂşlyokat hasznĂˇlja: a cĂ©lirĂˇnyt, az ĂĽtkĂ¶zĂ©sig megtett tĂˇvolsĂˇgot Ă©s a sebessĂ©get kombinĂˇlja. A robot hĂˇtramenete a szimulĂˇciĂłban tiltott. Ha nincs biztonsĂˇgos pĂˇr, az `optimisation()` `(None, [])` Ă©rtĂ©ket ad vissza.

## 5. A* Ă©s DWA kapcsolata

Az A* nem ad ki kĂ¶zvetlenĂĽl `cmd_vel` ĂĽzenetet. A `DWA+A.py` mindig az aktuĂˇlis
aktĂ­v waypointot adja a DWA-nak. A kĂ¶vetkezĹ‘ waypoint csak akkor vĂˇlik aktĂ­vvĂˇ,
ha a robot `0,20 m`-es helyzettĹ±rĂ©sen belĂĽlre Ă©r Ă©s a sebessĂ©ge legfeljebb
`0,30 m/s`. A kĂ¶ztes pontoknĂˇl a befogĂˇsi zĂłna kicsi, a vĂ©gsĹ‘ cĂ©lpontnĂˇl
viszont `0,5 m`-es lassĂ­tĂˇsi zĂłna mĹ±kĂ¶dik.

## 6. BiztonsĂˇgi korlĂˇtok Ă©s jelenlegi hatĂˇr

Az A* tĂ©rkĂ©p statikus; a mozgĂł akadĂˇlyt a jelenlegi prototĂ­pus csak a DWA lokĂˇlis predikciĂłjĂˇban kezeli. A LiDAR-pontfelhĹ‘bĹ‘l kĂ¶rakadĂˇly-listĂˇt kĂ©szĂ­tĹ‘ ROS2-adapter, a zajszĹ±rĂ©s, a teljes fĂ©kezĂ©si teszt Ă©s a globĂˇlis ĂşjratervezĂ©s mĂ©g kĂĽlĂ¶n feladat. A robotmodell Ă©s a DWA-modul ezĂ©rt kĂ¶zvetlenĂĽl nem importĂˇl ROS2- vagy Matplotlib-csomagot.

## 7. TesztelĂ©s

Az alĂˇbbi tesztek ellenĹ‘rzik a kĂ¶zĂ¶s robotmagot, a kinematikĂˇt, a gyorsulĂˇskorlĂˇtot, a mozgĂł akadĂˇly elĹ‘rejelzĂ©sĂ©t, a DWA ĂĽtkĂ¶zĂ©selutasĂ­tĂˇsĂˇt Ă©s az A* waypoint-kimenetĂ©t:

```text
python -m unittest codes_diploma.astar_project.tests.test_robot_and_dwa codes_diploma.astar_project.tests.test_dwa_a
```

## 8. EgyszerĹ± ĂşjrahasznĂˇlat

Az A* Ă©s a DWA minimĂˇlis hasznĂˇlata:

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

ROS2-ben a `linear_speed` Ă©rtĂ©ke kerĂĽlhet a `Twist.linear.x`, az
`angular_speed` pedig a `Twist.angular.z` mezĹ‘be. A ROS2-node feladata az
odometriĂˇbĂłl lĂ©trehozott `robotstate`, a LiDAR-bĂłl lĂ©trehozott `Obstacle` lista
Ă©s a `Twist` publikĂˇlĂˇsa.

Az Ăşj fĂˇjlok rĂ¶viden:

- `robot.py`: robotĂˇllapot, kinematika Ă©s akadĂˇlyok;
- `DWA.py`: DWA-sebessĂ©gpĂˇrok, biztonsĂˇg Ă©s pontozĂˇs;
- `DWA+A.py`: A* waypoint Ă©s DWA Ă¶sszekĂ¶tĂ©se;
- `test_robot_and_dwa.py`, `test_dwa_a.py`: a kĂ©t egysĂ©g tesztjei.

Az A*â€“DWA teljes folyamatĂˇt a `DWA+A.py` osztĂˇlya kezeli. A `best_pair` formĂˇja
`[v, w, w_L, w_R]`; a ROS2-node a `v` Ă©s `w` Ă©rtĂ©keket `Twist.linear.x` Ă©s
`Twist.angular.z` mezĹ‘be Ă­rhatja.

## 10. A szimulĂˇciĂłs felĂĽlet A* szerinti megjelenĂ­tĂ©se

A `codes_diploma/simulation.py` a meglĂ©vĹ‘ A* szimulĂˇciĂł felĂ©pĂ­tĂ©sĂ©t kĂ¶veti,
de a robotmozgĂˇst DWA-val egĂ©szĂ­ti ki. A bal oldali informĂˇciĂłs panel az A*
aktuĂˇlis cellĂˇjĂˇt Ă©s a prioritĂˇsi sor rĂ¶vid rĂ©szletĂ©t mutatja. A tĂ©rkĂ©pen:

- a vĂ©kony vonalak a rĂˇcscellĂˇk hatĂˇrai;
- a sĂ¶tĂ©t cellĂˇk a statikus akadĂˇlyok;
- a kĂ©k pontok az A* Ăˇltal mĂˇr vizsgĂˇlt cellĂˇk;
- a narancssĂˇrga pont az A* aktuĂˇlis keresĂ©si pontja;
- a sĂˇrga csillag a DWA aktuĂˇlis waypointja;
- a fekete szaggatott vonal az A* globĂˇlis Ăştvonala;
- a narancssĂˇrga vonal a DWA lokĂˇlis elĹ‘rejelzett trajektĂłriĂˇja;
- a piros kĂ¶rĂ¶k a statikus Ă©s mozgĂł akadĂˇlyok;
- a kĂ©k vonal a robot eddigi nyomvonala.

A program indĂ­tĂˇsakor az A* szimulĂˇciĂłjĂˇhoz hasonlĂł beĂˇllĂ­tĂˇsi ablak jelenik
meg. MegadhatĂł a rĂˇcs szĂ©lessĂ©ge, magassĂˇga, felbontĂˇsa, start- Ă©s cĂ©lcellĂˇja,
az ĂˇtlĂłs mozgĂˇs, valamint az automatikus lejĂˇtszĂˇs. A beĂˇllĂ­tott start- Ă©s
cĂ©lcella rĂˇcskoordinĂˇta, pĂ©ldĂˇul `(2, 2)`, amely a `0,2 m` felbontĂˇsĂş tĂ©rkĂ©pen
a cella kĂ¶zĂ©ppontjĂˇn keresztĂĽl vilĂˇgkoordinĂˇtĂˇvĂˇ alakul.

A szimulĂˇciĂł kĂ©t vizuĂˇlis fĂˇzisbĂłl Ăˇll. ElĹ‘szĂ¶r az A* keresĂ©s lĂ©pĂ©sei jelennek
meg egymĂˇs utĂˇn. EzutĂˇn minden animĂˇciĂłs idĹ‘lĂ©pĂ©sben a mozgĂł akadĂˇlyok
frissĂĽlnek, a DWA kivĂˇlasztja a `best_pair` Ă©rtĂ©ket, a `robot.py` `update()`
fĂĽggvĂ©nye mozgatja a robotot, vĂ©gĂĽl a rajz frissĂĽl. A globĂˇlis A* Ă©s BĂ©zier-
Ăştvonal minden megjelenĂ­tĂ©si pontjĂˇt kis piros pont jelĂ¶li; ezek a pontok a
teljes animĂˇciĂł alatt lĂˇthatĂłk. A vezĂ©rlĂ©s ettĹ‘l kĂĽlĂ¶n ritkĂ­tott waypoint-listĂˇt
hasznĂˇl.

Az aktĂ­v waypoint-index monoton nĂ¶vekszik: a DWA nem vĂˇlaszthat ki Ăşjra korĂˇbbi
Ăştvonalpontot, Ă©s nem ugorhat Ăˇt elĹ‘re pontokat. Egy waypoint csak akkor vĂˇlt,
ha a robot `0,20 m`-en belĂĽlre Ă©rt Ă©s a sebessĂ©ge legfeljebb `0,30 m/s`. A vĂ©gsĹ‘ waypoint elĂ©rĂ©sekor a
`plan_local()` `[0, 0, 0, 0]` parancsot ad vissza, ezĂ©rt a cĂ©lba Ă©rt robot nem
kap Ăşjabb mozgĂˇsi utasĂ­tĂˇst.

Az indĂ­tĂłablakban beĂˇllĂ­thatĂł a rĂˇcs szĂ©lessĂ©ge, magassĂˇga, felbontĂˇsa,
akadĂˇlyinflĂˇciĂłja, start- Ă©s cĂ©lcellĂˇja, tovĂˇbbĂˇ az A* heurisztikĂˇja
(`manhattan`, `euclidean`, `chebyshev`, `octile`), az ĂˇtlĂłs mozgĂˇs, az
automatikus lejĂˇtszĂˇs, valamint az `Alfa`, `Beta` Ă©s `Gamma` DWA-sĂşlyok.
KĂĽlĂ¶n kapcsolĂłval engedĂ©lyezhetĹ‘ vagy kikapcsolhatĂł a waypoint-lassĂ­tĂˇs.

A BĂ©zier-simĂ­tĂˇs kanyarainĂˇl a kontrollponttĂłl mĂ©rt vĂˇgĂˇsi tĂˇvolsĂˇg legfeljebb
`3 * resolution` mĂ©ter. ĂŤgy pĂ©ldĂˇul `0,20 m` felbontĂˇsnĂˇl legfeljebb `0,60 m`
vĂˇgĂˇs engedĂ©lyezett. Ha a gĂ¶rbe akadĂˇlyt Ă©rintene, a biztonsĂˇgi ellenĹ‘rzĂ©s az
eredeti A* Ăştvonalat tartja meg.

## 9. EgyszerĹ± A*â€“DWA szimulĂˇciĂł

A `codes_diploma/simulation.py` kĂĽlĂ¶n megjelenĂ­tĂ©si rĂ©teg. Nem tartalmaz Ăşj
ĂştvonaltervezĂ©si vagy DWA-algoritmust, hanem a `robot.py`, a `DWA.py` Ă©s a
`DWA+A.py` fĂĽggvĂ©nyeit hĂ­vja meg.

A `create_scene()` lĂ©trehoz egy rĂˇcstĂ©rkĂ©pet, statikus akadĂˇlyokat, kĂ©t mozgĂł
akadĂˇlyt, robotĂˇllapotot Ă©s cĂ©lt. A `create_simulation()` ezutĂˇn A* Ăştvonalat
keres, Matplotlib-ĂˇbrĂˇt kĂ©szĂ­t, Ă©s minden animĂˇciĂłs lĂ©pĂ©sben ezt a sorrendet
hajtja vĂ©gre:

```text
mozgĂł akadĂˇlyok frissĂ­tĂ©se
    -> aktuĂˇlis waypoint kivĂˇlasztĂˇsa
    -> DWA best_pair kivĂˇlasztĂˇsa
    -> robot.py: update()
    -> robot, akadĂˇlyok Ă©s trajektĂłriĂˇk kirajzolĂˇsa
```

A `best_pair` formĂˇja `[v, w, w_L, w_R]`. Ha a DWA nem ad biztonsĂˇgos pĂˇrt,
a szimulĂˇciĂł nullĂˇs kerĂ©ksebessĂ©ggel frissĂ­ti a robotot. A narancssĂˇrga vonal
a kivĂˇlasztott kerĂ©ksebessĂ©g-pĂˇr rĂ¶vid elĹ‘rejelzett trajektĂłriĂˇja, a kĂ©k vonal
pedig a robot eddigi nyomvonala.

### FuttatĂˇs

A projekt gyĂ¶kerĂ©bĹ‘l:

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

Ez megakadĂˇlyozza, hogy a DWA egy mar elhagyott ponthoz visszaforduljon.
Az `optimisation()` bemeneti celja az aktiv waypoint, nem egy kulon, elugro
racskoordinata.

### 11.7. `simulation.py`: grafikus szimulacio

A szimulacios ciklus sorrendje:

```text
1. A* vizsgalt cellak megjelenitese
2. statikus es mozgo akadalyak letrehozasa
3. mozgĂł akadalyak frissitese
4. aktiv waypoint es DWA cel meghatarozasa
5. DWA best_pair kivalsztasa
6. robot.update()
7. robotnyom, BĂ©zier-ut, pontok es akadalyak kirajzolasa
```

A megjelenites jelolesei:

- vilagos kek pontok: A* altal vizsgalt cellak;
- zold vonal: BĂ©zier-utvonal;
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
robotkinematikat, a DWA-t, az A*--DWA kapcsolatot, a mozgĂł akadalyat es a
szimulacios jelenetet. A legutobbi teljes ellenorzes eredmenye: `32 teszt
sikeres`.

A megjelenĂ­tĂ©s automatikusan elindul Ă©s legfeljebb `600` animĂˇciĂłs lĂ©pĂ©st
futtat. A szimulĂˇciĂłhoz nem kell ROS2; a Matplotlib Ă©s NumPy telepĂ­tĂ©se
szĂĽksĂ©ges.

## 12. ROS 2 / Gazebo robotfĂĽggetlen C++ A* + DWA integrĂˇciĂł

### 12.1. A csomag cĂ©lja

Az Ăşj `ros2_astar_dwa_gazebo/src/astar_dwa_controller` csomag a korĂˇbbi
Python prototĂ­pustĂłl fĂĽggetlen, C++17 alapĂş ROS 2 vezĂ©rlĹ‘. A
[astar_dwa_node.cpp](./ros2_astar_dwa_gazebo/src/astar_dwa_controller/src/astar_dwa_node.cpp)
nem tartalmaz TurtleBot3- vagy ROSbot-specifikus meghajtĂˇsi kĂłdot. SzabvĂˇnyos
ROS ĂĽzeneteket fogad Ă©s kĂĽld, ezĂ©rt a robotmodell kĂ©sĹ‘bb topic-paramĂ©terekkel
cserĂ©lhetĹ‘.

### 12.2. Adatfolyam

```text
/scan + /odom
    -> lokĂˇlis akadĂˇlyrĂˇcs
    -> A* (Grid cellĂˇk)
    -> kĂ¶vetkezĹ‘ waypoint
    -> DWA sebessĂ©gvizsgĂˇlat
    -> /cmd_vel
```

A `/goal_pose` ĂĽzenet Ăşj vilĂˇgkoordinĂˇtĂˇs cĂ©lt ĂˇllĂ­t be. Az A* Ăştvonalat a
`/astar_path` `nav_msgs/Path` topicon teszi kĂ¶zzĂ©. A robot szĂˇmĂˇra a lĂ©nyeges
interfĂ©sz tehĂˇt: `LaserScan`, `Odometry`, `PoseStamped`, `Twist` Ă©s `Path`.

### 12.3. Fontos paramĂ©terek Ă©s koordinĂˇtĂˇk

Az `astar_dwa_controller/config/rosbot.yaml` tartalmazza a topic-neveket,
a cĂ©lt, a `map_size` Ă©rtĂ©ket, a `resolution` cellamĂ©retet Ă©s a
`robot_radius` biztonsĂˇgi sugarat. A C++ node lokĂˇlis, nĂ©gyzetes rĂˇcsot Ă©pĂ­t
a robot kĂ¶rĂĽl. A rĂˇcskoordinĂˇta:

```text
row = floor((y - origin_y) / resolution)
column = floor((x - origin_x) / resolution)
```

PĂ©ldĂˇul `resolution = 0.20 m`, `origin_y = -6.0 m`, `y = 0.4 m` esetĂ©n
`row = floor(6.4 / 0.2) = 32`. A cellakĂ¶zĂ©ppont visszaalakĂ­tĂˇsa:
`y = origin_y + (row + 0.5) * resolution`, ezĂ©rt a 32-es sor kĂ¶zĂ©ppontja
`-6 + 32.5 * 0.2 = 0.5 m`.

### 12.4. A* Ă©s DWA mĹ±kĂ¶dĂ©se

Az A* prioritĂˇsi sort hasznĂˇl. A `g` az eddigi cellakĂ¶ltsĂ©g, a `h` az
egyenes vonalĂş becslĂ©s a cĂ©lig, az `f = g + h` pedig a kivĂˇlasztĂˇsi Ă©rtĂ©k.
Egy ĂˇtlĂłs lĂ©pĂ©s kĂ¶ltsĂ©ge `sqrt(2)`, egyenes lĂ©pĂ©sĂ© `1`. PĂ©ldĂˇul egy kĂ©t
egyenes Ă©s egy ĂˇtlĂłs lĂ©pĂ©s kĂ¶ltsĂ©ge `1 + 1 + 1.414 = 3.414` cellakĂ¶ltsĂ©g.
ĂtlĂłs sarokvĂˇgĂˇs csak akkor engedĂ©lyezett, ha a kĂ©t oldalsĂł cella is szabad.

A DWA a `v = 0...0.4 m/s` Ă©s `omega = -1.2...1.2 rad/s` mintapĂˇrokat
vizsgĂˇlja. Minden pĂˇr 15 darab, egyenkĂ©nt `0.1 s` hosszĂş elĹ‘relĂ©pĂ©ssel
szimulĂˇlĂłdik. ĂśtkĂ¶zĂ©s esetĂ©n a pĂˇr kiesik. A pontszĂˇm:

```text
score = -goal_distance - 0.25 * |heading_error| + 0.15 * v
```

Ha egy jelĂ¶lt 1 m-re van a cĂ©ltĂłl, a szĂ¶geltĂ©rĂ©s `0.2 rad`, a sebessĂ©g
`0.4 m/s`, akkor a pontszĂˇm `-1 - 0.25*0.2 + 0.15*0.4 =
-1 - 0.05 + 0.06 = -0.99`. A nagyobb pontszĂˇmĂş biztonsĂˇgos pĂˇr
kerĂĽl a `/cmd_vel` ĂĽzenetbe.

### 12.5. ROSbot ĂˇtĂĽltethetĹ‘sĂ©g

A ROSbot sajĂˇt bringupja biztosĂ­tja a motorvezĂ©rlĂ©st, odometriĂˇt Ă©s LiDAR-t.
Az algoritmus nem nyĂşl kĂ¶zvetlenĂĽl a motorokhoz. Ha a ROSbot pĂ©ldĂˇul
`/rosbot/scan`, `/rosbot/odom` Ă©s `/rosbot/cmd_vel` topicokat hasznĂˇl, a
paramĂ©terekkel ezek adhatĂłk meg; a C++ forrĂˇs nem vĂˇltozik. A Gazebo-vilĂˇg
robotmodellje jelenleg TurtleBot3, ezĂ©rt a ROSbot modellcsere kĂĽlĂ¶n
szimulĂˇciĂłs konfigurĂˇciĂłs lĂ©pĂ©s, nem algoritmusmĂłdosĂ­tĂˇs.

### 12.6. EllenĹ‘rzĂ©s

Windows alatt a ROS fejlĂ©cek hiĂˇnyĂˇban a Python launch-fĂˇjlok szintaxisa
ellenĹ‘rizhetĹ‘. A tĂ©nyleges C++ fordĂ­tĂˇs WSL-ben tĂ¶rtĂ©nik:

```bash
cd ~/projects/ros2_astar_dwa_gazebo
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
```

### 12.7. Ismert tĂ©rkĂ©p, LiDAR Ă©s megjelenĂ­tĂ©s

Az `astar_dwa_node` kizĂˇrĂłlag az elĹ‘re ismert statikus tĂ©rkĂ©pet hasznĂˇlja.
Az `known_obstacle_x`, `known_obstacle_y` Ă©s
`known_obstacle_radius` paramĂ©terekbĹ‘l Ă©pĂ­ti fel az A* statikus tĂ©rkĂ©pĂ©t.
Ez a szimulĂˇciĂłban azt jelenti, hogy a piros Ă©s narancssĂˇrga statikus
akadĂˇlyok helye elĹ‘re ismert. A DWA ettĹ‘l mĂ©g a `/scan` aktuĂˇlis mĂ©rĂ©sĂ©t
hasznĂˇlja, Ă­gy az elĹ‘re nem ismert vagy mozgĂł akadĂˇlyokra is reagĂˇl.

Az automatikus `lidar_map` Ă©s `frontier` mĂłdok eltĂˇvolĂ­tva, ezĂ©rt a LiDAR
csak a DWA pillanatnyi akadĂˇlyvizsgĂˇlatĂˇhoz hasznĂˇlatos.

A `visualization.launch.py` RViz2-konfigurĂˇciĂłja az `odom` fix keretben
megjelenĂ­ti a TF-fa koordinĂˇtĂˇit, a narancssĂˇrga `/scan` pontokat, a kĂ©k
odometriĂˇt Ă©s a zĂ¶ld `/astar_path` Ăştvonalat. Ez a megjelenĂ­tĂ©s nem avatkozik
be a vezĂ©rlĂ©sbe: ugyanazok a szabvĂˇnyos ROS topicok hasznĂˇlhatĂłk Gazebo-ban
Ă©s a valĂłdi ROSboton.

### 12.8. MozgĂł akadĂˇly szimulĂˇciĂł

A `moving_obstacle_node.py` a Gazebo `SetEntityPose` szolgĂˇltatĂˇsĂˇn keresztĂĽl
mozgatja a `moving_obstacle` nevĹ± kĂ©k hengert. A pozĂ­ciĂł:

```text
x = 3.0 m
y = 1.8 m + 1.2 m * sin(0.6 * t)
```

ahol `t` mĂˇsodpercben mĂ©rt szimulĂˇciĂłs idĹ‘. PĂ©ldĂˇul `t = 0` esetĂ©n
`y = 1.8 m`, `t = 1` esetĂ©n pedig kĂ¶rĂĽlbelĂĽl
`1.8 + 1.2 * 0.565 = 2.478 m`. A henger a LiDAR-ban megjelenik, Ă©s a DWA
ĂĽtkĂ¶zĂ©svizsgĂˇlata a kĂ¶vetkezĹ‘ elĹ‘rejelzett pontoknĂˇl figyelembe veszi.

### 12.9. RViz-hibakeresĂ©s Ă©s a lĂˇthatĂł mĹ±kĂ¶dĂ©s

Az RViz konfigurĂˇciĂł fix koordinĂˇtakerete `odom`, nem `map`. A jelenlegi
Gazebo-vĂˇltozatban nincs SLAM vagy tĂ©rkĂ©pkiszolgĂˇlĂł, ezĂ©rt `map` TF nem
lĂ©tezik; a `Fixed Frame: map` hiba emiatt helyes hibajelzĂ©s. A
`visualization.launch.py` az `astar_dwa.rviz` konfigurĂˇciĂłt Ă©s az `odom`
fix frame-et tĂ¶lti be.

Az `astar_dwa_node` minden vezĂ©rlĂ©si ciklusban kĂ¶zzĂ©teszi az
`/astar_dwa_markers` `visualization_msgs/MarkerArray` ĂĽzenetet:

- zĂ¶ld gĂ¶mb: aktuĂˇlis A* cĂ©l/waypoint;
- zĂ¶ld vonal: A* Ăştvonal;
- piros hengerek: ismert statikus akadĂˇlyok;
- kĂ©k vonal: a kivĂˇlasztott DWA sebessĂ©gpĂˇr 15 lĂ©pĂ©ses elĹ‘rejelzĂ©se.

Az odometriĂˇbĂłl a node dinamikusan publikĂˇlja az `odom -> base_link`, majd a
`base_link -> base_scan` TF-et. Ez teszi lehetĹ‘vĂ©, hogy az RViz a `/scan`
LiDAR-pontokat az `odom` fix frame-be transzformĂˇlja. A valĂłs ROSboton ezt a
TF-et cĂ©lszerĹ± a robot sajĂˇt bringupjĂˇra bĂ­zni; a vezĂ©rlĹ‘ topic- Ă©s frame
paramĂ©terezĂ©se mellett a szabvĂˇnyos interfĂ©sz vĂˇltozatlan marad.

## 13. RViz-es cĂ©lkijelĂ¶lĂ©s Ă©s OccupancyGrid tĂ©rkĂ©p

### A fĂˇjlok cĂ©lja

Az `astar_dwa_node.cpp` most az `/astar_map` `nav_msgs/OccupancyGrid` topicot
is publikĂˇlja. Ez a `known_map` mĂłdban a statikus akadĂˇlyokat, a robot
rĂˇhagyĂˇsĂˇval inflĂˇlt tiltott cellĂˇkat Ă©s a tĂ©rkĂ©p szĂ©lĂ©t mutatja. Az
`astar_dwa.rviz` ehhez hozzĂˇadja a `Known occupancy map` displayt, valamint a
`SetGoal` eszkĂ¶zt, amely a `/goal_pose` topicon kĂĽld cĂ©lt.

### Adatfolyam Ă©s cĂ©lkijelĂ¶lĂ©s

Az RViz `2D Goal Pose` eszkĂ¶z kattintĂˇsbĂłl Ă©s az egĂ©r hĂşzĂˇsĂˇnak irĂˇnyĂˇbĂłl
`PoseStamped` ĂĽzenetet kĂ©szĂ­t. A node a pozĂ­ciĂł `x` Ă©s `y` mezĹ‘jĂ©t eltĂˇrolja
`goal_x_` Ă©s `goal_y_` Ă©rtĂ©kkĂ©nt, naplĂłzza az Ăşj cĂ©lt, majd a kĂ¶vetkezĹ‘
vezĂ©rlĂ©si ciklusban Ăşjra lefuttatja az A*-t. PĂ©ldĂˇul egy `(4.0, 2.0)` cĂ©l az
`odom` koordinĂˇtarendszerben a tĂ©rkĂ©p origĂłjĂˇtĂłl 4 mĂ©terre keletre Ă©s 2 mĂ©terre
Ă©szakra van; a node ezt a vilĂˇgkoordinĂˇtĂˇt cellĂˇvĂˇ alakĂ­tja.

### TĂ©rkĂ©p Ă©s koordinĂˇta-ĂˇtalakĂ­tĂˇs

Az OccupancyGrid origĂłja `(-map_size/2, -map_size/2)`, a cellamĂ©ret
`resolution`. Egy `(x, y) = (4.0, 2.0)` pont `resolution = 0.20 m` Ă©s
`map_size = 16 m` mellett:

```text
column = floor((4.0 + 8.0) / 0.20) = 60
row    = floor((2.0 + 8.0) / 0.20) = 50
```

Ez azt jelenti, hogy a pont a 80x80 cellĂˇs tĂ©rkĂ©p 60. oszlopĂˇba Ă©s 50. sorĂˇba
kerĂĽl. Az akadĂˇlyok kĂ¶rĂĽl a kĂłd
`ceil((obstacle.radius + robot_radius) / resolution)` sugarĂş kĂ¶rben 100-as
Ă©rtĂ©kĹ±, foglalt cellĂˇkat ĂˇllĂ­t be; a tĂ¶bbi ismert szabad cella 0.

### LĂˇthatĂł mĹ±kĂ¶dĂ©s

A cĂ©lmarker most gĂ¶mbbĹ‘l, cĂ©lfeliratbĂłl Ă©s sĂ­kbeli cĂ©ljelbĹ‘l Ăˇll. Az A* vonal
vastagabb, a DWA elĹ‘rejelzett vonala kĂĽlĂ¶n kĂ©k magassĂˇgban fut, tovĂˇbbĂˇ a
robot footprintje Ă©s haladĂˇsi nyila is lĂˇthatĂł. A `/astar_map` tartĂłs
QoS-szal kĂ©szĂĽl, ezĂ©rt az RViz kĂ©sĹ‘bbi csatlakozĂˇsakor is megkapja az egyszer
publikĂˇlt statikus tĂ©rkĂ©pet. A node az odom elsĹ‘ beĂ©rkezĂ©se utĂˇn, majd minden
vezĂ©rlĂ©si ciklusban meghĂ­vja a `publish_map()` fĂĽggvĂ©nyt. A `known_map` mĂłd
akadĂˇlylistĂˇja nem fĂĽgg a LiDAR elsĹ‘ ĂĽzenetĂ©tĹ‘l, ezĂ©rt a tĂ©rkĂ©p akkor is
nem ĂĽres, ha a szenzoradat nĂ©hĂˇny pillanattal kĂ©sĹ‘bb Ă©rkezik.

Az RViz cĂ©lĂĽzenete nem Gazebo-topic. A `/goal_pose` a vezĂ©rlĹ‘ node bemenete;
az Ăşj cĂ©l alapjĂˇn az A* Ăştvonal ĂşjraszĂˇmolĂłdik, majd a DWA a Gazebo felĂ© a
`/cmd_vel` topicot hasznĂˇlja. Ha mĂ©g nincs LiDAR, a node mĂˇr akkor is kĂ¶zzĂ©teszi
a cĂ©lmarkert, de sebessĂ©gparancsot csak Ă©rvĂ©nyes szenzoradat utĂˇn ad.

### KorlĂˇtok Ă©s ellenĹ‘rzĂ©s

Az RViz-bĹ‘l Ă©rkezĹ‘ cĂ©l az `odom` keretben legyen. A statikus tĂ©rkĂ©p nem
tartalmazza a mozgĂł kĂ©k akadĂˇlyt, mert annak aktuĂˇlis helyĂ©t a LiDAR Ă©s a DWA
kezeli. EllenĹ‘rizhetĹ‘:

```bash
ros2 topic echo /astar_map --once
ros2 topic echo /goal_pose --once
```

Az RViz `TF` display tengelyei korĂˇbban piros X-tengelyeket Ă©s nyilakat
rajzoltak a `base_link` Ă©s `base_scan` keretekhez. Ezek vizualizĂˇciĂłs elemek,
nem akadĂˇlyok Ă©s nem A*-Ăştvonalak; a projekt konfigurĂˇciĂłjĂˇban a nyilak,
tengelyek Ă©s frame-nevek most ki vannak kapcsolva a tisztĂˇbb nĂ©zet Ă©rdekĂ©ben.

## 14. LiDAR-alapĂş felhalmozott tĂ©rkĂ©p

### A fĂˇjl cĂ©lja

Az `astar_dwa_node.cpp` `planning_source` paramĂ©tere kĂ©t mĹ±kĂ¶dĂ©st vĂˇlaszt:
`known_map` esetĂ©n a YAML-ben megadott statikus akadĂˇlyokbĂłl kĂ©szĂĽl a tervezĂ©si
tĂ©rkĂ©p; `lidar_map` esetĂ©n a node a LiDAR-mĂ©rĂ©sekbĹ‘l fokozatosan felĂ©pĂ­tett
`OccupancyGrid`-et hasznĂˇlja. Ez a mĂłd a korĂˇbbi ismerttĂ©rkĂ©pes megoldĂˇst nem
tĂ¶rli, csak alternatĂ­v forrĂˇst ad az A* szĂˇmĂˇra.

### Adatfolyam

Az `scan()` eltĂˇrolja az Ăşj `LaserScan` ĂĽzenetet, majd `lidar_map` vagy
`frontier` mĂłdban
meghĂ­vja az `update_lidar_map()` fĂĽggvĂ©nyt. Ez a robot aktuĂˇlis
`pose_` Ă©rtĂ©kĂ©vel az `odom` keretbe alakĂ­tja a LiDAR-sugarakat. A
`mark_lidar_ray()` a robot cellĂˇjĂˇtĂłl a mĂ©rĂ©si vĂ©gpontig halad:

- a kĂ¶ztes cellĂˇk Ă©rtĂ©ke `0`, vagyis szabad;
- Ă©rvĂ©nyes akadĂˇlymĂ©rĂ©snĂ©l a vĂ©gpont Ă©rtĂ©ke `100`, vagyis foglalt;
- `inf` vagy tartomĂˇnyon kĂ­vĂĽli mĂ©rĂ©snĂ©l a `range_max` vĂ©gpontja nem lesz
  foglalt, csak a sugĂˇr kĂ¶ztes cellĂˇi lesznek szabadok;
- a korĂˇbbi cellaĂ©rtĂ©kek megmaradnak, Ă­gy a tĂ©rkĂ©p Ă¶sszeadja a tĂ¶bb
  pozĂ­ciĂłbĂłl Ă©rkezĹ‘ megfigyelĂ©seket.

Az `astar()` a `planning_obstacles()` eredmĂ©nyĂ©t hasznĂˇlja. `lidar_map`
mĂłdban a `lidar_map_obstacles()` minden `100`-as cellĂˇbĂłl akadĂˇlypontot
kĂ©pez, majd az A* a robot sugarĂˇval Ă©s a cella fĂ©lmĂ©retĂ©vel inflĂˇlja az
akadĂˇly kĂ¶rnyezetĂ©t. A DWA ettĹ‘l kĂĽlĂ¶n tovĂˇbbra is az aktuĂˇlis, nyers
`obstacles()` LiDAR-pontokat hasznĂˇlja. A lokĂˇlis DWA csak a robot elĹ‘tti
180 fokos Ă©s legfeljebb 3 mĂ©teres mĂ©rĂ©si tartomĂˇnyt hasznĂˇlja, Ă­gy a falak
Ă©s akadĂˇlyok mĂ¶gĂ¶tti 360 fokos pontfelhĹ‘ nem kĂ©nyszerĂ­ti indokolatlan
megĂˇllĂˇsra vagy helyben forgĂˇsra.

### RĂˇcs, koordinĂˇtĂˇk Ă©s kĂ©plet

A tĂ©rkĂ©p nĂ©gyzetes, oldala `map_size` mĂ©ter, cellamĂ©rete `resolution` mĂ©ter,
origĂłja az `odom` rendszerben `(-map_size/2, -map_size/2)`. A
`map_cell(x, y, row, column)` kĂ©plete:

```text
column = floor((x + map_size / 2) / resolution)
row    = floor((y + map_size / 2) / resolution)
```

Itt `x` Ă©s `y` mĂ©terben mĂ©rt vilĂˇgkoordinĂˇta, `row` Ă©s `column` egĂ©sz
cellaindex. PĂ©ldĂˇul `map_size = 16 m`, `resolution = 0.20 m` Ă©s
`(x, y) = (4.0, 2.0)` esetĂ©n:

```text
column = floor((4.0 + 8.0) / 0.20) = floor(60.0) = 60
row    = floor((2.0 + 8.0) / 0.20) = floor(50.0) = 50
```

Ez a 80x80 cellĂˇs tĂ©rkĂ©p `(50, 60)` cellĂˇja. Ha a robot
`(0, 0)` ponton Ăˇll, Ă©s egy sugĂˇr `2.0 m` tĂˇvolsĂˇgban, `0` radiĂˇn szĂ¶gben
akadĂˇlyt mĂ©r, akkor a vĂ©gpont `(2.0, 0.0)`, amelynek cellĂˇja:

```text
column = floor((2.0 + 8.0) / 0.20) = 50
row    = floor((0.0 + 8.0) / 0.20) = 40
```

A `mark_lidar_ray()` a robot cellĂˇjĂˇtĂłl a `(40, 50)` vĂ©gpontig a diszkrĂ©t
vonal cellĂˇit jelĂ¶li szabadnak, majd a `(40, 50)` cellĂˇt foglaltra ĂˇllĂ­tja.

### MegjelenĂ­tĂ©s Ă©s hasznĂˇlat

Az `publish_map()` `lidar_map` mĂłdban kĂ¶zvetlenĂĽl ezt a rĂˇcsot publikĂˇlja
`/astar_map` nĂ©ven. Az `OccupancyGrid` jelentĂ©se:

- `-1`: mĂ©g nem lĂˇtott / ismeretlen;
- `0`: LiDAR-sugĂˇr Ăˇltal szabadnak lĂˇtott cella;
- `100`: LiDAR-mĂ©rĂ©s vĂ©gpontja, feltĂ©telezett akadĂˇly.

A mĂłd a launch paramĂ©terĂ©vel kapcsolhatĂł, a YAML alapĂ©rtelmezĂ©se mellett:

```bash
ros2 launch dwa_gazebo_sim simulation.launch.py planning_source:=lidar_map
```

EzutĂˇn Ăşjra kell fordĂ­tani a workspace-t, majd a teljes
`simulation.launch.py` indĂ­tĂˇssal lehet futtatni. `known_map` mĂłdban az
OccupancyGrid tovĂˇbbra is a YAML statikus akadĂˇlyait Ă©s a biztonsĂˇgi
inflĂˇciĂłt mutatja.

### BiztonsĂˇgi korlĂˇtok

Ez a megoldĂˇs LiDAR-odometriai tĂ©rkĂ©p, nem teljes SLAM. Az `odom` driftje a
tĂ©rkĂ©pben is megjelenhet, nincs loop closure Ă©s nincs map->odom korrekciĂł.
A cellĂˇn kĂ­vĂĽli sugarakat a node elutasĂ­tja. Az ismeretlen cellĂˇkat a jelenlegi egyszerĹ±
szimulĂˇciĂłs A* nem tiltja le, ezĂ©rt a robot a cĂ©l felĂ© haladva fedezhet fel
Ăşj terĂĽletet; valĂłdi biztonsĂˇgkritikus navigĂˇciĂłhoz az ismeretlen cellĂˇkat
blokkolni vagy Nav2/SLAM Toolbox megoldĂˇssal kezelni kell.

### EllenĹ‘rzĂ©s

A C++ vĂˇltoztatĂˇs WSL-ben fordĂ­thatĂł Ă©s indĂ­thatĂł:

```bash
cd "/mnt/c/Users/Rum DĂˇniel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo"
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source install/setup.bash
ros2 launch dwa_gazebo_sim simulation.launch.py
```

FutĂˇs kĂ¶zben a tĂ©rkĂ©p ellenĹ‘rzĂ©se:

```bash
ros2 topic echo /astar_map --once
```

Az ĂĽzenetben a `data` tĂ¶mbben kell megjelenniĂĽk a `-1`, `0` Ă©s `100`
Ă©rtĂ©keknek; `known_map` mĂłdban a `-1` Ă©rtĂ©k nem rĂ©sze az elĹ‘re ismert
statikus tĂ©rkĂ©pnek.

## 15. Frontier-alapĂş automatikus feltĂ©rkĂ©pezĂ©s

### MĹ±kĂ¶dĂ©s

Az Ăşj `planning_source: frontier` mĂłd nem hasznĂˇl elĹ‘re megadott cĂ©lt. A
vezĂ©rlĹ‘ indulĂł Ăˇllapota Ă©s alapĂ©rtelmezett cĂ©lkoordinĂˇtĂˇja `(0, 0)`, de a cĂ©l
nem aktĂ­v, ezĂ©rt `known_map` Ă©s `lidar_map` mĂłdban is csak `/goal_pose`
ĂĽzenet utĂˇn indul a robot. Frontier mĂłdban a node a felhalmozott LiDAR-rĂˇcs
alapjĂˇn automatikusan aktivĂˇl cĂ©lt.

Frontier cĂ©lcellĂˇnak azt az ismert szabad cellĂˇt tekinti, amely:

- legalĂˇbb egy 8-szomszĂ©dja mĂ©g ismeretlen (`-1`);
- legalĂˇbb `0.6 m` tĂˇvolsĂˇgra van a robottĂłl.

A `select_frontier_goal()` a feltĂ©teleknek megfelelĹ‘ szabad cellĂˇk kĂ¶zĂĽl a
legkĂ¶zelebbit vĂˇlasztja. Ezt a vilĂˇgkoordinĂˇtĂˇs cellakĂ¶zĂ©ppontot az A* cĂ©ljakĂ©nt ĂˇllĂ­tja be,
majd a DWA a kĂ¶vetkezĹ‘ waypoint felĂ© mozgatja a robotot. A frontier elĂ©rĂ©se
utĂˇn a cĂ©l deaktivĂˇlĂłdik, Ă©s a kĂ¶vetkezĹ‘ vezĂ©rlĂ©si ciklus Ăşj frontiert keres.
Ha nincs tĂ¶bb ilyen cella, a node nulla sebessĂ©get publikĂˇl Ă©s megĂˇll.

Ha a frontier cĂ©lhoz az aktuĂˇlis, inflĂˇlt LiDAR-tĂ©rkĂ©pen az A* nem talĂˇl
Ăştvonalat, a cĂ©l nem tĂ¶rlĹ‘dik azonnal. A node megtartja a kivĂˇlasztott
frontiert, Ă©s korlĂˇtozott recovery-forgatĂˇst indĂ­t. A haladĂˇsfigyelĹ‘ akkor is
recovery-t indĂ­t, ha tĂ¶bb mĂˇsodpercig nincs legalĂˇbb `0.10 m` odometriai
elmozdulĂˇs. A forgatĂˇs legfeljebb `2.5 s`, utĂˇna Ăşj A* Ăştvonal kĂ©szĂĽl. A cĂ©l
Ă­gy nem kerĂĽl tĂ¶rlĂ©sre, Ă©s a vezĂ©rlĂ©s nem keveri Ă¶ssze a DWA Ăˇltal vĂˇlasztott
nullasebessĂ©get a sikeres cĂ©lbaĂ©rĂ©ssel.

A LiDAR-tĂ©rkĂ©p ray-castinget hasznĂˇl. ValĂłs, Ă©rvĂ©nyes vĂ©gpontnĂˇl a sugĂˇr
kĂ¶ztes cellĂˇi szabadak, a vĂ©gpont foglalt; `inf` vagy tartomĂˇnyon kĂ­vĂĽli
mĂ©rĂ©snĂ©l a sugĂˇr a `range_max` hatĂˇrig csak szabad cellĂˇkat jelĂ¶l. ĂŤgy a
nyitott elĹ‘re irĂˇny nem marad tĂ©vesen teljesen ismeretlen, Ă©s a frontier
keresĹ‘ tĂ©nylegesen tud elĂ©rhetĹ‘ cĂ©lcellĂˇt talĂˇlni.

A Gazebo-fizika stabilitĂˇsa Ă©rdekĂ©ben a DWA kimenete sebessĂ©grĂˇmpĂˇn halad:
a lineĂˇris sebessĂ©g legfeljebb `0.20 m/s`, a szĂ¶gsebessĂ©g legfeljebb
`0.8 rad/s`, egy 0,1 mĂˇsodperces ciklusban pedig a vĂˇltozĂˇs legfeljebb
`0.04 m/s` Ă©s `0.20 rad/s`. Ăśres A* Ăştvonal esetĂ©n a node nulla sebessĂ©get
publikĂˇl Ă©s megĂˇll.

### Adatfolyam Ă©s pĂ©lda

```text
LiDAR -> lidar_map -> szabad/ismeretlen hatĂˇr keresĂ©se
                         -> frontier cĂ©l
                         -> A* -> DWA -> /cmd_vel
                                      |
                                      +-> Ăşj LiDAR-mĂ©rĂ©s
```

Ha a robot `(0, 0)` helyen van, `resolution = 0.20 m`, Ă©s egy szabad cella
kĂ¶zĂ©ppontja `(1.1, 0.3)`, akkor a frontier cĂ©l ez a vilĂˇgpont lesz. Az A*
ezt a cĂ©lcellĂˇt hasznĂˇlja; amikor a robot `0.3 m`-nĂ©l kĂ¶zelebb Ă©r, a cĂ©l
lezĂˇrul, Ă©s Ăşj hatĂˇrcella kivĂˇlasztĂˇsa indul.

### KorlĂˇtok

Ez a frontier-mĂłd egyszerĹ± odometria-alapĂş feltĂ©rkĂ©pezĂ©s. Az `odom` driftje
eltolhatja a korĂˇbbi mĂ©rĂ©seket, Ă©s nincs loop closure. Az ismeretlen cellĂˇkat
az egyszerĹ± A* ĂˇtjĂˇrhatĂłnak kezeli, mikĂ¶zben a frontier kivĂˇlasztĂˇsa csak
ismert szabad cellĂˇra esik. ValĂłs, biztonsĂˇgkritikus roboton az ismeretlen
cellĂˇkat konzervatĂ­van blokkolni, illetve SLAM Toolbox/Nav2 rendszert hasznĂˇlni
cĂ©lszerĹ±.

### IndĂ­tĂˇs Ă©s ellenĹ‘rzĂ©s

```bash
ros2 launch dwa_gazebo_sim simulation.launch.py planning_source:=frontier
```

A naplĂłban az automatikusan kivĂˇlasztott cĂ©l ilyen formĂˇban jelenik meg:

```text
Uj frontier cel: x=..., y=... m
```

---

# `simulation.py` â€“ 1.1 SzimulĂˇciĂłs eredmĂ©nyek Ă©s forgatĂłkĂ¶nyvek

## 1. A fĂˇjl cĂ©lja

A `simulation.py` az A* globĂˇlis ĂştvonaltervezĂ©st Ă©s a DWA lokĂˇlis mozgĂˇstervezĂ©st
egy kĂ¶zĂ¶s, kĂ©tdimenziĂłs jelenetben mutatja be. A szimulĂˇciĂł nem csak a vĂ©gsĹ‘
Ăştvonalat rajzolja ki: az A* keresĂ©s kĂ¶zben megjelenĂ­ti a vizsgĂˇlt cellĂˇkat Ă©s
a prioritĂˇsi sort, a DWA szakaszban pedig a lehetsĂ©ges pĂˇlyĂˇkat, a mozgĂł
akadĂˇlyokat, a waypointot Ă©s a fĂ©kezĂ©si szakaszokat is.

Az alapbeĂˇllĂ­tĂˇsokkal a tĂ©rkĂ©p `30 x 20` cellĂˇs, a felbontĂˇs `0,2 m/cella`,
ezĂ©rt a megjelenĂ­tett terĂĽlet `6,0 m x 4,0 m`. A kezdĹ‘cella `(2, 2)`, a
cĂ©lcella `(17, 27)`, ahol a koordinĂˇta formĂˇja `(sor, oszlop)`. A vilĂˇgban
ezek kĂ¶zĂ©ppontjai rendre `(0,5 m, 0,5 m)` Ă©s `(5,5 m, 3,5 m)`.

## 2. Adatfolyam

Az `create_scene()` elkĂ©szĂ­ti a rĂˇcstĂ©rkĂ©pet, a statikus akadĂˇlyokat, a kĂ©t
mozgĂł akadĂˇlyt Ă©s a robot kezdeti ĂˇllapotĂˇt. Az akadĂˇlyinflĂˇciĂł utĂˇn az
`astar_search()` megkeresi a globĂˇlis Ăştvonalat. Ezt az `AStarDWAPlanner`
Bezier-simĂ­tĂˇssal waypointokkĂˇ alakĂ­tja. Az animĂˇciĂł elsĹ‘ rĂ©sze az A* keresĂ©s
lĂ©pĂ©seit, a mĂˇsodik rĂ©sze pedig a DWA ciklusait futtatja:

```text
create_scene -> A* keresĂ©s -> Bezier Ăştvonal Ă©s waypointok
             -> mozgĂł akadĂˇlyok -> DWA pĂˇlyajelĂ¶ltek -> robotfrissĂ­tĂ©s
```

A `compute_onlab_trajectories()` minden DWA sebessĂ©gpĂˇrhoz elĹ‘re kiszĂˇmĂ­tja a
jĂłsolt pĂˇlyĂˇt, majd a pĂˇlya vĂ©gĂ©rĹ‘l indĂ­tott fĂ©kezĂ©si szakaszt. A pĂˇlya piros,
ha ĂĽtkĂ¶zĂ©sveszĂ©lyes vagy a megĂˇllĂˇshoz szĂĽksĂ©ges tĂˇvolsĂˇg nem elegendĹ‘; a
biztonsĂˇgos pĂˇlyĂˇk szĂĽrkĂ©k, a kivĂˇlasztott pĂˇlya zĂ¶ld.

## 3. Fontos fĂĽggvĂ©nyek Ă©s adatok

- `load_planner_class()`: betĂ¶lti a `DWA+A.py` fĂˇjlban lĂ©vĹ‘
  `AStarDWAPlanner` osztĂˇlyt.
- `parse_cell(value)`: a `"sor,oszlop"` szĂ¶veget egĂ©sz koordinĂˇtapĂˇrrĂˇ alakĂ­tja.
- `create_scene(...)`: a rĂˇcsot Ă©s az akadĂˇlyokat hozza lĂ©tre.
- `create_simulation(...)`: elvĂ©gzi a tervezĂ©st, felĂ©pĂ­ti a Matplotlib-ĂˇbrĂˇt,
  majd visszaadja a `figure` Ă©s `FuncAnimation` objektumot.
- `compute_onlab_trajectories(...)`: a DWA jelĂ¶ltek biztonsĂˇgĂˇt Ă©s fĂ©kezĂ©si
  ĂştjĂˇt szĂˇmolja.
- `update_frame(frame)`: A* vagy DWA Ăˇllapot szerint frissĂ­ti az ĂˇbrĂˇt.
- `run_simulation()`: a Tkinter beĂˇllĂ­tĂłablakot indĂ­tja el.

Az Ăˇbra bal oldali informĂˇciĂłs panelje az A* lĂ©pĂ©sĂ©t Ă©s prioritĂˇsi Ă©rtĂ©keit,
illetve a DWA fĂˇzisban a robot helyzetĂ©t, sebessĂ©gĂ©t, az Ă¶sszes, veszĂ©lyes Ă©s
biztonsĂˇgos pĂˇlyĂˇk darabszĂˇmĂˇt mutatja. A jobb oldali tĂ©rkĂ©pen a sĂ¶tĂ©t cellĂˇk
az inflĂˇlt akadĂˇlyterĂĽletet, a piros kĂ¶rĂ¶k a dinamikus vagy statikus akadĂˇlyokat,
a vilĂˇgoszĂ¶ld vonal a simĂ­tott Ăştvonalat, a kĂ©k nyomvonal pedig a robot tĂ©nyleges
mozgĂˇsĂˇt jelzi.

## 4. A kĂ©pek Ă©rtelmezĂ©se

Az alapbeĂˇllĂ­tĂˇsokkal mentett kĂ©pkockĂˇk a
`codes_diploma/astar_project/results/figures/` mappĂˇban talĂˇlhatĂłk.

1. `simulation_01_frame_0000.png`: az A* keresĂ©s elsĹ‘ lĂ©pĂ©se. A bal oldali
   panelen az aktuĂˇlis cella `(2, 2)`, a prioritĂˇsi sorban pedig az `f` Ă©rtĂ©kek
   lĂˇthatĂłk. A vilĂˇgoskĂ©k pontok a mĂˇr kibĹ‘vĂ­tett A* cellĂˇkat jelĂ¶lik.
2. `simulation_02_frame_0100.png`: az A* keresĂ©s kĂ©sĹ‘i szakasza. A statikus
   akadĂˇlyok kĂ¶zĂ¶tti ĂˇtjĂˇrĂłk Ă©s az inflĂˇciĂł miatt tiltott biztonsĂˇgi zĂłnĂˇk
   szemlĂ©ltetik, hogy a robot nem matematikai pontkĂ©nt tervez Ăştvonalat.
3. `simulation_03_frame_0250.png`: a DWA mozgĂˇs kĂ¶zbeni Ăˇllapota. A robot
   kĂ¶rĂĽl sok piros Ă©s szĂĽrke jelĂ¶lt pĂˇlya lĂˇthatĂł; a piros jelĂ¶ltek veszĂ©lyesek,
   a szĂĽrke jelĂ¶ltek a pillanatnyilag megengedett alternatĂ­vĂˇk. A vastag zĂ¶ld
   gĂ¶rbe az aktuĂˇlisan vĂˇlasztott pĂˇlyĂˇt, a csillag a waypointot jelĂ¶li.
4. `simulation_04_frame_0500.png`: a robot a kĂ¶zĂ©psĹ‘ akadĂˇlyrendszer utĂˇn
   kĂ¶zelĂ­t a felsĹ‘ ĂˇtjĂˇrĂłhoz. Ez jĂł kĂ©p az akadĂˇlykerĂĽlĂ©s Ă©s a waypoint-kĂ¶vetĂ©s
   egyĂĽttes bemutatĂˇsĂˇra.
5. `simulation_05_frame_0650.png`: kĂ©sĹ‘i DWA Ăˇllapot, amikor a robot mĂˇr a cĂ©l
   elĹ‘tti szakaszon halad. A kĂ©k nyomvonal Ă©s a zĂ¶ld globĂˇlis Ăştvonal kĂ¶zĂ¶tti
   eltĂ©rĂ©s a lokĂˇlis korrekciĂłt szemlĂ©lteti.
6. `simulation_06_frame_0725.png`: vĂ©gĂˇllapot. A panelen `Cel elerve`, a
   sebessĂ©g `0,00 m/s`, a robot pedig a cĂ©l kĂ¶rĂĽl Ăˇll. Ez a legjobb Ă¶sszefoglalĂł
   kĂ©p a sikeres ĂştvonaltervezĂ©s Ă©s vĂ©grehajtĂˇs bemutatĂˇsĂˇra.

## 5. KonkrĂ©t szĂˇmolĂˇsi pĂ©lda

Az alapbeĂˇllĂ­tĂˇsban a cĂ©lcella `(17, 27)`, a felbontĂˇs `0,2 m`, az origĂł
`(0,0)`. A cĂ©lpont vilĂˇgkoordinĂˇtĂˇja:

```text
x = (27 + 0,5) * 0,2 m = 5,5 m
y = (17 + 0,5) * 0,2 m = 3,5 m
```

Az animĂˇciĂłban a tervezĂ©si fĂˇzis 125 kĂ©pkockĂˇbĂłl Ăˇll. A DWA mozgĂˇs ezĂ©rt a
`movement_start = 126` kĂ©pkockĂˇnĂˇl kezdĹ‘dik, Ă©s legfeljebb 600 mozgĂˇsi lĂ©pĂ©st
kap. A `frame = 250` kĂ©p Ă­gy a `250 - 126 = 124`-edik mozgĂˇsi Ăˇllapot kĂ¶rnyĂ©kĂ©t
mutatja, nem egy Ăşjratervezett globĂˇlis A* Ăştvonalat.

## 6. KorlĂˇtok Ă©s indĂ­tĂˇs

A kĂ¶zvetlen

```text
python -m codes_diploma.simulation
```

indĂ­tĂˇs a Tkinter beĂˇllĂ­tĂłablakot Ă©s utĂˇna a blokkolĂł Matplotlib-ablakot nyitja
meg, ezĂ©rt parancssori futtatĂˇsban az ablak bezĂˇrĂˇsĂˇig nem ad vissza promptot.
KĂ©pek mentĂ©sĂ©hez a `create_simulation(..., show=False)` visszaadott ĂˇbrĂˇjĂˇnak
kĂ©pkockĂˇi menthetĹ‘k. A jelenlegi kĂ©pek az `euclidean` heurisztikĂˇval,
ĂˇtlĂłs mozgĂˇssal, `0,11 m` inflĂˇciĂłval Ă©s Bezier-simĂ­tĂˇssal kĂ©szĂĽltek.

A vizsgĂˇlat nem jelent statisztikai Ă¶sszehasonlĂ­tĂˇst: egy rĂ¶gzĂ­tett jelenet
egy futĂˇsĂˇt dokumentĂˇlja. TĂ¶bb forgatĂłkĂ¶nyvhĂ¶z kĂĽlĂ¶n kell vĂˇltoztatni pĂ©ldĂˇul
a kezdĹ‘- Ă©s cĂ©lcellĂˇt, az inflĂˇciĂłt, a heurisztikĂˇt, a simĂ­tĂˇst vagy a DWA
`alpha`, `beta`, `gamma` sĂşlyait, majd azonos mĂłdon menteni Ă©s Ă¶sszevetni a
kĂ©peket Ă©s a mĂ©rĹ‘szĂˇmokat.

## 7. EllenĹ‘rzĂ©s

Lefutott a kĂ©rt `python -m codes_diploma.simulation` parancs; a grafikus
ablakos mĹ±kĂ¶dĂ©s miatt a folyamatot a kĂ©pernyĹ‘mentĂ©sre szolgĂˇlĂł vezĂ©relt futĂˇs
egĂ©szĂ­tette ki. A vezĂ©relt futĂˇs hat kĂ©pet mentett a
`codes_diploma/astar_project/results/figures/` mappĂˇba, Ă¶sszesen 726 animĂˇciĂłs
kĂ©pkockĂˇval. A kĂ©peken ellenĹ‘rizhetĹ‘ az A* tervezĂ©si szakasz, a DWA jelĂ¶lt
pĂˇlyĂˇi, a fĂ©kezĂ©si megjelenĂ­tĂ©s Ă©s a cĂ©l elĂ©rĂ©se.

---

# `experiments.py` Ă©s `run_experiment.py` â€“ heurisztika- Ă©s mozgĂˇsmĂłd-vizsgĂˇlat

## 1. A vizsgĂˇlat cĂ©lja

Az Ă¶sszehasonlĂ­tĂł mĂ©rĂ©s nĂ©gy heurisztikĂˇt vizsgĂˇl azonos pĂˇlyĂˇkon:
Manhattan, Euklideszi, Chebyshev Ă©s octile. Minden pĂˇlya kĂ©t mĂłdban fut:
ĂˇtlĂłs mozgĂˇssal (`diagonal=True`) Ă©s csak nĂ©gy fĹ‘irĂˇnyĂş mozgĂˇssal
(`diagonal=False`). ĂŤgy kĂĽlĂ¶n lĂˇthatĂł a heurisztika hatĂˇsa, valamint az,
hogy az ĂˇtlĂłs lĂ©pĂ©s megengedĂ©se vagy tiltĂˇsa megvĂˇltoztatja-e a megoldhatĂłsĂˇgot.

## 2. PĂˇlyĂˇk Ă©s adatfolyam

A `build_experiment_scenarios()` nĂ©gy rĂ¶gzĂ­tett pĂˇlyĂˇt kĂ©szĂ­t:

- `original_simulation`: az eredeti `simulation.py` 30Ă—20 cellĂˇs fal- Ă©s
  ĂˇtjĂˇrĂłelrendezĂ©se, start `(2,2)` Ă©s cĂ©l `(17,27)` ponttal;
- `compact_corridor`: ennek kisebb, 10Ă—7 cellĂˇs szemlĂ©ltetĹ‘ vĂˇltozata;
- `corner_cutting`: saroknĂˇl elhelyezett akadĂˇlyok, ahol a kĂ¶zĂ¶s sarok
  ĂˇtvĂˇgĂˇsĂˇt a `GridMap.get_neighbors()` tiltja;
- `diagonal_only`: kereszt alakĂş akadĂˇly, amelyben a start Ă©s a cĂ©l kĂ¶zĂ¶tt
  csak egy nem engedĂ©lyezett ĂˇtlĂłs ĂˇtkelĂ©s lenne.

Az `original_simulation` pĂˇlya az eredeti szimulĂˇciĂł fal- Ă©s ĂˇtjĂˇrĂłelrendezĂ©sĂ©t
hasznĂˇlja. A `compact_corridor` ennek kisebb, 10Ă—7 cellĂˇs vĂˇltozata. A kĂ©pek
elsĹ‘dleges eredmĂ©nye az eredeti tĂ©rkĂ©pen kĂ©szĂĽlt; az inflĂˇciĂłt Ă©s a DWA
mozgĂł akadĂˇlyait ez az A* Ă¶sszehasonlĂ­tĂˇs kĂĽlĂ¶n nem tartalmazza.

A `run_scenario_comparison()` minden pĂˇlyĂˇt mindkĂ©t mozgĂˇsmĂłdban, azon belĂĽl
mind a nĂ©gy heurisztikĂˇval lefuttat. A `compare_heuristics()` az A* rĂ©szletes
eredmĂ©nyĂ©bĹ‘l a kĂ¶vetkezĹ‘ket menti: sikeressĂ©g, Ăştvonal kĂ¶ltsĂ©ge, Ăştvonalhossz,
vizsgĂˇlt csomĂłpontok szĂˇma Ă©s maga az Ăştvonal. A `write_results()` az Ăştvonal
kivĂ©telĂ©vel CSV-be Ă­rja az Ă¶sszehasonlĂ­thatĂł mĂ©rĹ‘szĂˇmokat.

## 3. EredmĂ©nyek

Az eredmĂ©nyfĂˇjl:

`codes_diploma/astar_project/results/tables/heuristic_comparison.csv`

Ă–sszesen 32 sor kĂ©szĂĽlt: 4 pĂˇlya Ă— 2 mozgĂˇsmĂłd Ă— 4 heurisztika.

Az `original_simulation` pĂˇlyĂˇn fĹ‘irĂˇnyĂş mozgĂˇsnĂˇl minden heurisztika 40,00
kĂ¶ltsĂ©gĹ± utat talĂˇlt. ĂtlĂłs mozgĂˇsnĂˇl a Manhattan kĂ¶ltsĂ©ge 32,38, az
Euklideszi, Chebyshev Ă©s octile vĂˇltozatokĂ© 31,21 lett. Ez a kĂĽlĂ¶nbsĂ©g nem
heurisztikai hiba, hanem az engedĂ©lyezett mozgĂˇsok Ă©s a heurisztika egyĂĽttese.

A `compact_corridor` pĂˇlyĂˇn az ĂˇtjĂˇrĂłk miatt minden konfigurĂˇciĂł talĂˇlt utat.
FĹ‘irĂˇnyĂş mĂłdban a kĂ¶ltsĂ©g `15,0`, ĂˇtlĂłs mĂłdban `12,0711` lett. Az
`diagonal_only` pĂˇlyĂˇn viszont mind a nĂ©gy heurisztika helyesen `success=False`
eredmĂ©nyt adott nem ĂˇtlĂłs Ă©s ĂˇtlĂłs mĂłdban is: a cĂ©l kĂ¶rĂĽli akadĂˇlyok miatt a
tiltott sarokĂˇtvĂˇgĂˇssal sem lehet szabĂˇlyos Ăştvonalat lĂ©trehozni.

## 4. SarokvĂˇgĂˇs kezelĂ©se

ĂtlĂłs mozgĂˇs esetĂ©n sem elĂ©g azt ellenĹ‘rizni, hogy az ĂˇtlĂłs cĂ©lcella szabad-e.
A `GridMap.get_neighbors()` a kĂ©t kĂ¶ztes oldalsĂł cellĂˇt is megvizsgĂˇlja. Ha
pĂ©ldĂˇul `(1,1)` cellĂˇbĂłl a `(2,2)` cellĂˇba lĂ©pne a robot, akkor a `(1,2)` Ă©s
`(2,1)` cellĂˇnak is szabadnak kell lennie. Ha valamelyik akadĂˇly, az ĂˇtlĂłs
szomszĂ©dot elutasĂ­tja. Ez akadĂˇlyozza meg, hogy a robot kĂ©t akadĂˇly kĂ¶zĂ¶s
sarkĂˇn fizikailag ĂˇtvĂˇgjon.

A `corner_cutting` teszt ezt ellenĹ‘rzi: a talĂˇlt Ăşt nem tartalmazza a
tiltott `(2,2)` sarokĂˇtvĂˇgĂˇsi cellĂˇt. A teszt ugyanakkor azt is ellenĹ‘rzi,
hogy a pĂˇlya kerĂĽlĹ‘ Ăşton tovĂˇbbra is megoldhatĂł marad.

## 5. KonkrĂ©t kĂ¶ltsĂ©gpĂ©lda

Az eredeti szimulĂˇciĂłs pĂˇlyĂˇn a start `(2,2)`, a cĂ©l `(17,27)`. FĹ‘irĂˇnyĂş
mĂłdban 40 egyenes lĂ©pĂ©s szĂĽksĂ©ges. ĂtlĂłs mozgĂˇsnĂˇl a start Ă©s a cĂ©l
koordinĂˇtakĂĽlĂ¶nbsĂ©ge `15` sor Ă©s `25` oszlop, ezĂ©rt az ideĂˇlis, akadĂˇlyt nem
keresztezĹ‘ geometriai alsĂł becslĂ©s 15 ĂˇtlĂłs Ă©s 10 egyenes lĂ©pĂ©s:

```text
15 * sqrt(2) + 10 * 1
= 15 * 1,41421356 + 10
= 31,2132
```

Az eredeti falak miatt a tĂ©nyleges Ăşt ennĂ©l hosszabb lehet. A mĂ©rĂ©sben a
Manhattan vĂˇltozat 32,38, a mĂˇsik hĂˇrom heurisztika 31,21 kĂ¶ltsĂ©get adott;
ez azt is megmutatja, hogy a Manhattan heurisztika ĂˇtlĂłs kĂ¶ltsĂ©g mellett nem
ugyanolyan termĂ©szetes vĂˇlasztĂˇs, mint az octile vagy az Euklideszi heurisztika.

Az egyenes lĂ©pĂ©s kĂ¶ltsĂ©ge 1 cella, az ĂˇtlĂłs lĂ©pĂ©s kĂ¶ltsĂ©ge
`sqrt(2) â‰ 1,4142` cella. A heurisztika a kibĹ‘vĂ­tett csomĂłpontok szĂˇmĂˇt
befolyĂˇsolhatja, de szabĂˇlyos, megengedett mozgĂˇsoknĂˇl nem vezethet
olcsĂłbb Ăştvonalhoz az optimĂˇlisnĂˇl.

## 6. IndĂ­tĂˇs Ă©s tesztelĂ©s

Az Ă¶sszehasonlĂ­tĂˇs indĂ­tĂˇsa:

```text
python -m codes_diploma.astar_project.run_experiment
```

A cĂ©lzott tesztek:

```text
python -m unittest codes_diploma.astar_project.tests.test_experiments codes_diploma.astar_project.tests.test_astar_baseline codes_diploma.astar_project.tests.test_grid_map -v
```

A futtatĂˇs eredmĂ©nye: 13 teszt sikeres. A tesztek ellenĹ‘rzik mind a nĂ©gy
heurisztika Ă©s mindkĂ©t mozgĂˇsmĂłd lefutĂˇsĂˇt, a nem ĂˇtlĂłs mĂłdban elutasĂ­tott
megoldhatatlan pĂˇlyĂˇt Ă©s a sarokvĂˇgĂˇs tiltĂˇsĂˇt.

## 7. Az egysĂ©ges, kontrasztos Ă¶sszehasonlĂ­tĂł ĂˇbrĂˇk

Az aktuĂˇlis ĂˇbrĂˇk ismĂ©t egyetlen tĂ©rkĂ©pen jelenĂ­tik meg mind a nĂ©gy heurisztika ĂştvonalĂˇt. A heurisztikĂˇkat nagy kontrasztĂş szĂ­nek kĂĽlĂ¶nbĂ¶ztetik meg: Manhattan kĂ©k, Euklideszi narancssĂˇrga, Chebyshev zĂ¶ld, Octile lila. A folytonos vonal az ĂˇtlĂłs mozgĂˇs tiltĂˇsĂˇt, a szaggatott vonal az ĂˇtlĂłs mozgĂˇs engedĂ©lyezĂ©sĂ©t jelenti. Az Ăştvonalak vastagok, fehĂ©r kontĂşrt kapnak, ezĂ©rt a szomszĂ©dos vagy egymĂˇst fedĹ‘ szakaszok is jobban elkĂĽlĂ¶nĂĽlnek. A kezdĹ‘pont zĂ¶ld `S`, a cĂ©lpont piros `G` jelĂ¶lĂ©st kapott.

Az ĂˇbrĂˇkat a `python -m codes_diploma.astar_project.generate_comparison_figures` parancs generĂˇlja Ăşjra. A program minden forgatĂłkĂ¶nyvhĂ¶z egy kĂ©pet ment a `codes_diploma/astar_project/results/figures/` kĂ¶nyvtĂˇrba.

### 7.1. Eredeti szimulĂˇciĂłs tĂ©rkĂ©p

**KĂ©p:** `heuristics_original_simulation.png`

**KĂ©palĂˇĂ­rĂˇs:** *A nĂ©gy A* heurisztika Ăştvonalainak Ă¶sszehasonlĂ­tĂˇsa az eredeti szimulĂˇciĂłs tĂ©rkĂ©pen.*

**BeilleszthetĹ‘ szĂ¶veg:**
Az Ăˇbra ugyanazon, 30Ă—20 cellĂˇs tĂ©rkĂ©pen mutatja be a Manhattan, Euklideszi, Chebyshev Ă©s Octile heurisztika Ăˇltal talĂˇlt Ăştvonalakat. A szĂ­n a heurisztikĂˇt, a vonal tĂ­pusa pedig a mozgĂˇsi mĂłdot jelĂ¶li. ĂŤgy egyetlen tĂ©rkĂ©pen lĂˇthatĂł, hogy az ĂˇtlĂłs lĂ©pĂ©sek engedĂ©lyezĂ©se rĂ¶videbb Ăştvonalakat eredmĂ©nyezhet, mikĂ¶zben az akadĂˇlyok megkerĂĽlĂ©sĂ©nek szabĂˇlyai minden vĂˇltozatban Ă©rvĂ©nyben maradnak.

### 7.2. Kisebb, ĂˇtjĂˇrĂłs ellenĹ‘rzĹ‘ pĂˇlya

**KĂ©p:** `heuristics_compact_corridor.png`

**KĂ©palĂˇĂ­rĂˇs:** *Heurisztika-Ă¶sszehasonlĂ­tĂˇs kisebb, ĂˇtjĂˇrĂłkat tartalmazĂł rĂˇcstĂ©rkĂ©pen.*

**BeilleszthetĹ‘ szĂ¶veg:**
A kisebb ellenĹ‘rzĹ‘ pĂˇlya egy fĂĽggĹ‘leges Ă©s egy vĂ­zszintes akadĂˇlyfalon kialakĂ­tott ĂˇtjĂˇrĂłkat tartalmaz. Az Ăˇbra azt szemlĂ©lteti, hogy az Ă¶sszes vizsgĂˇlt heurisztika kĂ©pes megtalĂˇlni a falak kĂ¶zĂ¶tti szabĂˇlyos Ăştvonalat, az ĂˇtlĂłs mozgĂˇs pedig csĂ¶kkenti az Ăştvonal geometriai kĂ¶ltsĂ©gĂ©t.

### 7.3. SarokvĂˇgĂˇsi vizsgĂˇlat

**KĂ©p:** `heuristics_corner_cutting.png`

**KĂ©palĂˇĂ­rĂˇs:** *A sarokvĂˇgĂˇs elleni szomszĂ©dvizsgĂˇlat hatĂˇsa ĂˇtlĂłs mozgĂˇsnĂˇl.*

**BeilleszthetĹ‘ szĂ¶veg:**
Az ĂˇtlĂłs mozgĂˇs engedĂ©lyezĂ©se mellett az algoritmus nem lĂ©phet Ăˇt kĂ©t akadĂˇly kĂ¶zĂ¶s sarkĂˇn. A szomszĂ©dvizsgĂˇlat a kĂ©t kĂ¶ztes oldalsĂł cellĂˇt is ellenĹ‘rzi, ezĂ©rt a megtalĂˇlt Ăştvonal szabĂˇlyos kerĂĽlĹ‘utat hasznĂˇl.

### 7.4. Megoldhatatlan pĂˇlya

**KĂ©p:** `heuristics_diagonal_only.png`

**KĂ©palĂˇĂ­rĂˇs:** *Megoldhatatlan rĂˇcspĂˇlya felismerĂ©se kĂ©t mozgĂˇsi mĂłdban.*

**BeilleszthetĹ‘ szĂ¶veg:**
A kereszt alakĂş akadĂˇlyrendszer elzĂˇrja a kezdĹ‘- Ă©s a cĂ©lcellĂˇt. Egyik heurisztika sem tud szabĂˇlyos Ăştvonalat lĂ©trehozni, ezĂ©rt az algoritmus mindkĂ©t mozgĂˇsi mĂłdban helyesen jelzi a `NO PATH` eredmĂ©nyt. Ez megerĹ‘sĂ­ti, hogy a heurisztika a keresĂ©s sorrendjĂ©t befolyĂˇsolja, az akadĂˇly- Ă©s szomszĂ©dsĂˇgi szabĂˇlyokat nem Ă­rja felĂĽl.
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
## 8. ROS 2 A* + DWA akadĂˇlyinflĂˇciĂł Ă©s Ăştvonalhiba

Az `astar_dwa_node.cpp` az odometriĂˇbĂłl, a cĂ©lbĂłl Ă©s a statikus akadĂˇlyokbĂłl
A* rĂˇcstĂ©rkĂ©pet kĂ©szĂ­t, majd a DWA-val sebessĂ©get kĂĽld a `/cmd_vel` tĂ©mĂˇra.
A mostani javĂ­tĂˇs az akadĂˇlyinflĂˇciĂłt Ă©rinti: a korĂˇbbi nĂ©gyzetes tiltĂˇs
lezĂˇrhatta a fizikailag ĂˇtjĂˇrhatĂł rĂ©seket.

A paramĂ©terek szerint a rĂˇcs felbontĂˇsa `resolution=0.20 m`, a robot sugara
`robot_radius=0.28 m`. Egy 0,35 m sugarĂş akadĂˇlynĂˇl a biztonsĂˇgi sugĂˇr:

```text
0,35 m + 0,28 m = 0,63 m
```

Az Ăşj kĂłd a cellakĂ¶zĂ©ppont Ă©s az akadĂˇlykĂ¶zĂ©ppont euklideszi tĂˇvolsĂˇgĂˇt mĂ©ri:

```text
d = sqrt((x_c - x_o)^2 + (y_c - y_o)^2)
```

ahol `x_c,y_c` a cellakĂ¶zĂ©ppont, `x_o,y_o` az akadĂˇly kĂ¶zĂ©ppontja mĂ©terben.
Csak a `d <= 0,63 m` feltĂ©telnek megfelelĹ‘ cellĂˇk lesznek blokkoltak.
KorĂˇbban a teljes nĂ©gyzetes rĂˇcsblokk tiltott volt, Ă­gy kĂ©t akadĂˇly kĂ¶zĂ¶tt
Ă¶sszeĂ©rhettek a biztonsĂˇgi zĂłnĂˇk.

PĂ©ldĂˇul 1,80 m kĂ¶zĂ©pponttĂˇvolsĂˇg Ă©s kĂ©t 0,63 m-es biztonsĂˇgi sugĂˇr esetĂ©n:

```text
1,80 m - 2 * 0,63 m = 0,54 m
```

marad geometriai szabad tĂˇvolsĂˇg. A kĂ¶r alakĂş inflĂˇciĂł ezĂ©rt kevĂ©sbĂ©
konzervatĂ­v, mikĂ¶zben a robot sugarĂˇt tovĂˇbbra is figyelembe veszi.

Ha a kezdĹ‘- vagy cĂ©lcella kĂ­vĂĽl esik a tĂ©rkĂ©pen, vagy blokkolt, a node most
diagnosztikai figyelmeztetĂ©st Ă­r ki a `start=(row,column)`, `goal=(row,column)`,
`start_blocked` Ă©s `goal_blocked` Ă©rtĂ©kekkel. Ez megmutatja, hogy Ă©rvĂ©nytelen
cella vagy tĂ©nylegesen megszakadt A* kapcsolat okozza-e az ĂĽres Ăştvonalat.

A DWA kĂĽlĂ¶n rĂ©teg: az A* Ăştvonal megtalĂˇlĂˇsa utĂˇn a LiDAR-pontok alapjĂˇn mĂ©g
megĂˇllĂ­thatja a robotot, ha minden kiprĂłbĂˇlt sebessĂ©gpĂˇlya ĂĽtkĂ¶zne. A javĂ­tĂˇs
az A* statikus tĂ©rkĂ©pĂ©t teszi pontosabbĂˇ, a lokĂˇlis LiDAR-viselkedĂ©st nem
rejti el.

EllenĹ‘rzĂ©s:

```bash
colcon build --symlink-install --packages-select astar_dwa_controller
```

### 2026-11-02 Python-kompatibilis DWA frissites

- `collision_distance` most a trajektoria megtett ivhossza, nem konstans
    `10.0`; kesoi utkozesnel a jelolt a fekezesi feltetelen keresztul marad.
- A predikcios ido a lokalis cel tavolsagahoz igazodik.
- A sebessegpont a Python `v_target = min(v_max, max(0.08, 1.4 * dist))`
    logikajat koveti.
- A `robot_radius` `0.22`, a `safety_margin` `0.05` a YAML-ben.
- Az A* inflacio es a map/marker biztonsagi zona is tartalmazza a margint.
- A legutobbi build mindket csomagra sikeres:
    `colcon build --packages-select astar_dwa_controller dwa_gazebo_sim --symlink-install`.

EzutĂˇn az `/astar_path`, `/astar_map` Ă©s `/astar_dwa_markers` tĂ©mĂˇkon lehet
ellenĹ‘rizni, hogy a kĂ©t akadĂˇly kĂ¶zĂ¶tti Ăştvonal lĂ©trejĂ¶n-e.
## 9. A ROS 2 A* + DWA tesztelĂ©si vizualizĂˇciĂłja Ă©s sebessĂ©gkorlĂˇtja

Az `astar_dwa_node.cpp` vezĂ©rlĹ‘je kĂ©t kĂĽlĂ¶n feladatot vĂ©gez. Az A* a statikus
akadĂˇlyokbĂłl Ăştvonalat kĂ©szĂ­t, a DWA pedig a LiDAR alapjĂˇn kivĂˇlasztja a
kĂ¶vetkezĹ‘ sebessĂ©gpĂˇrt. A tesztelĂ©s ĂˇttekinthetĹ‘bb lett az RViz
`/astar_dwa_markers` tĂ©mĂˇjĂˇn:

- zĂ¶ld vonal: A* Ăştvonal;
- kĂ©k vonal: az aktuĂˇlisan kivĂˇlasztott DWA-elĹ‘rejelzĂ©s;
- piros hengerek: ismert statikus akadĂˇlyok;
- halvĂˇnysĂˇrga lapok: statikus akadĂˇly plusz robot-sugĂˇr biztonsĂˇgi zĂłnĂˇja;
- sĂˇrga pontok: a LiDAR Ăˇltal Ă©ppen Ă©rzĂ©kelt akadĂˇlypontok;
- kĂ©k ĂˇttetszĹ‘ henger Ă©s nyĂ­l: robotpozĂ­ciĂł Ă©s haladĂˇsi irĂˇny.

A maximĂˇlis lineĂˇris sebessĂ©g most paramĂ©terezett. A `rosbot.yaml`
`max_linear_velocity=0.32 m/s` Ă©rtĂ©ke azt jelenti, hogy a kiadott
`Twist.linear.x` nem lehet nagyobb 0,32 m/s-nĂ©l. A korĂˇbbi kĂłd ezt 0,20 m/s-ra
korlĂˇtozta, mikĂ¶zben a DWA 0,40 m/s-ig vizsgĂˇlt sebessĂ©geket. A
`max_angular_velocity=1.00 rad/s` az elfordulĂˇsi sebessĂ©g felsĹ‘ hatĂˇra.

A vezĂ©rlĹ‘ ciklusa 0,10 s. Az Ăşj lineĂˇris gyorsĂ­tĂˇsi lĂ©pĂ©s legfeljebb 0,08 m/s
ciklusonkĂ©nt, vagyis ideĂˇlis esetben:

```text
0,32 m/s / 0,08 m/s = 4 ciklus
4 * 0,10 s = 0,40 s
```

alatt Ă©ri el a maximĂˇlis Ă©rtĂ©ket. Ez nem gyorsĂ­tja fel a veszĂ©lyes helyzeteket:
az ĂĽtkĂ¶zĂ©svizsgĂˇlat minden DWA-jelĂ¶lt pĂˇlyĂˇn tovĂˇbbra is lefut.

Az RViz-es vizsgĂˇlat menete:

1. `/astar_path`: van-e globĂˇlis Ăştvonal;
2. `/astar_map`: a statikus biztonsĂˇgi zĂłnĂˇk helye;
3. sĂˇrga LiDAR-pontok: lĂˇt-e a robot vĂˇratlan akadĂˇlyt;
4. kĂ©k DWA-vonal: a lokĂˇlis vezĂ©rlĹ‘ merre tervezi a kĂ¶vetkezĹ‘ 1,5 mĂˇsodpercet.

Ha zĂ¶ld Ăştvonal van, de a kĂ©k vonal rĂ¶vid vagy a robot Ăˇll, akkor a DWA
LiDAR-biztonsĂˇgi ellenĹ‘rzĂ©se ĂˇllĂ­totta meg. Ha zĂ¶ld Ăştvonal sincs, akkor az
A* statikus tĂ©rkĂ©pĂ©t vagy a cĂ©lt kell ellenĹ‘rizni.

## 10. A Gazebo mozgĂł akadĂˇly mĹ±kĂ¶dĂ©se Ă©s javĂ­tĂˇsa

### A fĂˇjlok cĂ©lja

A mozgĂł akadĂˇly mĹ±kĂ¶dĂ©sĂ©t hĂˇrom fĂˇjl egyĂĽtt adja:

- `worlds/dwa_world.sdf`: a `moving_obstacle` Gazebo-modellje;
- `dwa_gazebo_sim/moving_obstacle_node.py`: a modell Ăşj pozĂ­ciĂłjĂˇt szĂˇmĂ­tja;
- `launch/bridge_and_controller.launch.py`: ROS 2 service bridge-et indĂ­t a
  Gazebo `/world/dwa_world/set_pose` szolgĂˇltatĂˇsĂˇhoz.

### Adatfolyam

Az akadĂˇly kezdeti vilĂˇgkoordinĂˇtĂˇja `(x, y, z) = (3.0, 1.8, 0.45) m`.
A `moving_obstacle_node` 0,05 mĂˇsodpercenkĂ©nt frissĂ­tĂ©si ciklust futtat. A
pozĂ­ciĂł y-koordinĂˇtĂˇja:

```text
y(t) = 1,8 + 1,2 * sin(0,6 * t) m
```

Itt `t` a node Ăˇltal kĂ¶vetett idĹ‘ mĂˇsodpercben, a `1,8 m` a kĂ¶zĂ©pvonal, a
`1,2 m` a kitĂ©rĂ©s amplitĂşdĂłja, a `0,6 1/s` pedig a szĂ¶gsebessĂ©g jellegĹ±
szorzĂł. PĂ©ldĂˇul `t = 0 s` esetĂ©n:

```text
y(0) = 1,8 + 1,2 * sin(0) = 1,8 m
```

`t = 2 s` esetĂ©n `0,6 * 2 = 1,2`, ezĂ©rt
`y(2) â‰ 1,8 + 1,2 * 0,932 â‰ 2,92 m`. Az x-koordinĂˇta vĂ©gig `3,0 m`,
tehĂˇt az akadĂˇly fĂĽggĹ‘leges irĂˇnyban mozog.

### Mi akadĂˇlyozta a mozgĂˇst?

KorĂˇbban a world fĂˇjlban ez szerepelt:

```xml
<static>true</static>
```

Ez azt jelentette, hogy a Gazebo a modellt statikus objektumkĂ©nt kezelte.
Ezt `<static>false</static>` Ă©rtĂ©kre mĂłdosĂ­tottam. Ezen kĂ­vĂĽl a node ugyan
meghĂ­vta a service klienst, de a launch fĂˇjl nem bridge-elte a
`SetEntityPose` szolgĂˇltatĂˇst. Most ez is bekerĂĽlt:

```text
/world/dwa_world/set_pose@ros_gz_interfaces/srv/SetEntityPose
```

Ez a kapcsolat tovĂˇbbĂ­tja a ROS 2 service-kĂ©rĂ©st a Gazebo transport felĂ©.

### A node biztonsĂˇgos frissĂ­tĂ©se

A node a `request_in_flight` Ăˇllapottal biztosĂ­tja, hogy ne kĂĽldjĂ¶n Ăşj
pozĂ­ciĂłkĂ©rĂ©st addig, amĂ­g az elĹ‘zĹ‘ vĂˇlasz meg nem Ă©rkezett. ĂŤgy a 20 Hz-es
timer nem halmozza fel a Gazebo service-kĂ©rĂ©seket. A vĂˇlasz `success` mezĹ‘jĂ©t
ellenĹ‘rzi, Ă©s sikertelen frissĂ­tĂ©snĂ©l figyelmeztetĂ©st Ă­r a ROS 2 naplĂłba.

### EllenĹ‘rzĂ©s

A mĂłdosĂ­tĂˇs utĂˇn lefutott:

```bash
colcon build --symlink-install --packages-select dwa_gazebo_sim
python3 -m py_compile moving_obstacle_node.py
```

A futĂˇsi ellenĹ‘rzĂ©s sorĂˇn a Gazebo pose-adatĂˇban a `moving_obstacle` y-Ă©rtĂ©ke
vĂˇltozott, pĂ©ldĂˇul `2,8703 m`, majd `2,8536 m`, kĂ©sĹ‘bb `2,8359 m` lett. Ez
igazolja, hogy az akadĂˇly mĂˇr nem csak a node-ban szĂˇmolja a pĂˇlyĂˇt, hanem a
Gazebo-modell tĂ©nyleges pozĂ­ciĂłja is frissĂĽl.

## 11. A mozgĂł akadĂˇly kezelĂ©se az A* + DWA C++ vezĂ©rlĹ‘ben

### A fĂˇjl cĂ©lja

Az `astar_dwa_node.cpp` a ROS 2 vezĂ©rlĹ‘ben kĂ©t kĂĽlĂ¶n feladatot kapcsol Ă¶ssze:
az A* egy rĂ¶vid, globĂˇlis Ăştvonalat keres, a DWA pedig a kĂ¶vetkezĹ‘ Ăştvonalpont
felĂ© vĂˇlaszt sebessĂ©get. A korĂˇbbi mĹ±kĂ¶dĂ©sben az A* csak a YAML-ben megadott
statikus akadĂˇlyokat hasznĂˇlta. A mozgĂł akadĂˇlyt ugyan lĂˇtta a LiDAR, de az A*
Ăştvonala nem vĂˇltozott, ezĂ©rt az Ăştvonal a dinamikus akadĂˇlyon keresztĂĽl is
vezethetett.

### Adatfolyam Ă©s mĂłdosĂ­tĂˇs

A vezĂ©rlĂ©si ciklus az `obstacles()` fĂĽggvĂ©nnyel a `/scan` LaserScan mĂ©rĂ©si
pontjait vilĂˇgkoordinĂˇtĂˇra alakĂ­tja, Ă©s csak a robot elĹ‘tti, legfeljebb 3,0 m-es
tartomĂˇnyt tartja meg. Az aktuĂˇlis LiDAR-akadĂˇlyokat a lokĂˇlis DWA hasznĂˇlja; a globĂˇlis A* rĂˇcs
tovĂˇbbra is a statikus akadĂˇlymodellt hasznĂˇlja, a Python-szimulĂˇtor logikĂˇjĂˇval
Ă¶sszhangban.

### Fontos fĂĽggvĂ©nyek

- `obstacles()`: a LiDAR-pontokat szĹ±ri Ă©s `Obstacle{x, y, radius}` adatokkĂˇ
  alakĂ­tja;
- `astar(const std::vector<Obstacle>& sensed_obstacles)`: a statikus tĂ©rkĂ©pet
  statikus akadĂˇlyok alapjĂˇn felĂ©pĂ­ti az A* rĂˇcsot; a LiDAR-listĂˇt a lokĂˇlis
  DWA kezeli;
- `dwa(...)`: elĹ‘rehaladĂł, helyben fordulĂł Ă©s visszatolatĂł sebessĂ©gpĂˇrokat
  vizsgĂˇl, majd a cĂ©lhoz kĂ¶zelebb vivĹ‘ biztonsĂˇgos pĂˇrost vĂˇlasztja;
- `control()`: egy ciklusban egyszer gyĹ±jti a LiDAR-akadĂˇlyokat, Ăşjratervez,
  kivĂˇlasztja a waypointot, majd publikĂˇlja a `/cmd_vel` ĂĽzenetet.

### DWA biztonsĂˇgi vĂˇltozĂˇs

A DWA sebessĂ©gmintĂˇja elĹ‘remenĹ‘ jelĂ¶lteket vizsgĂˇl. A jelĂ¶lt pĂˇlya
15 lĂ©pĂ©sen keresztĂĽl, 0,1 s-os lĂ©pĂ©ssel kerĂĽl ellenĹ‘rzĂ©sre, vagyis a konfigurĂˇlt
vizsgĂˇlt idĹ‘tĂˇv 1,5 s. A LiDAR-mĂ©rĂ©s pontszerĹ±, ezĂ©rt az akadĂˇly sugara `0 m`;
a robot sugarĂˇhoz `0,05 m` biztonsĂˇgi tartalĂ©k adĂłdik.

PĂ©ldĂˇul egy LiDAR-pont 0,36 m-re van a jelĂ¶lt robotpozĂ­ciĂłtĂłl:

```text
robot_radius + obstacle_radius + tartalek
= 0,28 m + 0,00 m + 0,05 m
= 0,33 m
```

Ez a pĂˇlya veszĂ©lyesnek minĹ‘sĂĽl, ezĂ©rt a DWA mĂˇsik elfordulĂˇsi irĂˇnyt vagy
visszatolatĂł pĂˇlyĂˇt keres. Ha egyetlen minta sem biztonsĂˇgos, a korĂˇbbi
biztonsĂˇgi Ăˇg marad Ă©rvĂ©nyben: a robot `v=0` sebessĂ©ggel a cĂ©l irĂˇnyĂˇba fordul,
nem hajt bele az akadĂˇlyba.

### MiĂ©rt oldja meg az elakadĂˇst?

Ha a mozgĂł akadĂˇly a globĂˇlis A* Ăştvonalra kerĂĽl, a DWA a lokĂˇlis
elĹ‘rejelzĂ©sben kerĂĽli ki vagy fĂ©kezi le. A LiDAR minden mĂ©rĂ©si pontjĂˇt nem
szabad kĂĽlĂ¶n A* akadĂˇlykĂ©nt inflĂˇlni, mert egy fizikai akadĂˇly sok sĹ±rĹ± pontot
ad, Ă©s a cellĂˇk kĂ¶rĂĽli zĂłnĂˇk tĂ©vesen teljes ĂˇtjĂˇrĂłkat zĂˇrhatnak le.

### EllenĹ‘rzĂ©s

A mĂłdosĂ­tott csomag ellenĹ‘rzĂ¶tt buildje:

```bash
source /opt/ros/jazzy/setup.bash
cd ros2_astar_dwa_gazebo
colcon build --packages-select astar_dwa_controller --symlink-install
```

A build sikeresen lefutott. Az RViz-ben az `/astar_path`, a sĂˇrga LiDAR-pontok
Ă©s a kĂ©k DWA-trajektĂłria egyĂĽttesĂ©t kell figyelni. Ha a robot mĂ©gsem halad,
a vezĂ©rlĹ‘ naplĂłjĂˇban az `Az A* nem talĂˇlt elĂ©rhetĹ‘ Ăştvonalat` ĂĽzenet
kĂĽlĂ¶nvĂˇlasztja a valĂłdi ĂştvonalhiĂˇnyt a DWA biztonsĂˇgi megĂˇllĂˇsĂˇtĂłl.

## 12. A ROS/Gazebo tĂ©rkĂ©p Ă©s a Python-szimulĂˇtor Ă¶sszehangolĂˇsa

A ROS/Gazebo vĂˇltozat most a Python `simulation.py` alapĂ©rtelmezett tĂ©rkĂ©pĂ©t
hasznĂˇlja referenciakĂ©nt. A rĂˇcs 30 oszlopbĂłl Ă©s 20 sorbĂłl Ăˇll, a
`resolution=0,2 m`, ezĂ©rt a tervezĂ©si terĂĽlet 6,0 m szĂ©les Ă©s 4,0 m magas.
A rĂˇcs origĂłja `(0,0) m`, Ă­gy a `(2,2)` kezdĹ‘cella kĂ¶zĂ©ppontja:

```text
x = (2 + 0,5) * 0,2 = 0,5 m
y = (2 + 0,5) * 0,2 = 0,5 m
```

A `(17,27)` cĂ©lcella kĂ¶zĂ©ppontja ugyanĂ­gy `(5,5; 3,5) m`. A fĂĽggĹ‘leges
akadĂˇlysor a 10. oszlopban, a 7-12. sorok kĂ¶zĂ¶tt nyitott rĂ©ssel, a vĂ­zszintes
akadĂˇlysor pedig a 12. sorban, a 19-24. oszlopok kĂ¶zĂ¶tti nyitott rĂ©ssel
szerepel. A Gazebo SDF-ben ezek Ă¶sszefĂĽggĹ‘, 0,2 m vastag falszakaszokkĂ©nt
jelennek meg; ez a cellĂˇk fizikai megfelelĹ‘je.

### A kĂ©t mozgĂł akadĂˇly

A Python-szimulĂˇtorban szereplĹ‘ akadĂˇlyok ROS oldali kezdĹ‘pozĂ­ciĂłja Ă©s
sebessĂ©ge:

```text
moving_obstacle_1: (2,4; 0,4) m + (0; 0,20) m/s * t
moving_obstacle_2: (6,8; 2,1) m + (-0,25; 0) m/s * t
```

PĂ©ldĂˇul 5 mĂˇsodpercnĂ©l az elsĹ‘ akadĂˇly helye
`(2,4; 1,4) m`, a mĂˇsodikĂ© pedig `(5,55; 2,1) m`. A
`moving_obstacle_node.py` ezeket a pozĂ­ciĂłkat a
`/world/dwa_world/set_pose` szolgĂˇltatĂˇson keresztĂĽl adja Ăˇt a GazebĂłnak.
Egyszerre csak egy service-kĂ©rĂ©s van fĂĽggĹ‘ben, ezĂ©rt az akadĂˇlyfrissĂ­tĂ©s nem
halmozĂłdik fel.

### A DWA mĹ±kĂ¶dĂ©si egyezĂ©se

Az `astar_dwa_node.cpp` DWA-rĂ©sze a Python `robotconfig` fĹ‘ paramĂ©tereit
hasznĂˇlja: kerĂ©ksugĂˇr `0,033 m`, kerĂ©ktĂˇvolsĂˇg `0,08 m`, maximĂˇlis
kerĂ©ksebessĂ©g `15 rad/s`, kerĂ©ksebessĂ©g-lĂ©pĂ©s `1 rad/s`, gyorsulĂˇsi korlĂˇt
`2 m/sÂ˛`, `dt=0,1 s`, elĹ‘rejelzĂ©si idĹ‘ `3 s`, biztonsĂˇgi rĂˇhagyĂˇs `0,15 m`,
valamint `Alfa=5`, `Beta=2`, `Gamma=3`.

Egy bal Ă©s jobb kerĂ©ksebessĂ©gbĹ‘l a Python- Ă©s ROS-kĂłd azonos mĂłdon szĂˇmolja:

```text
v = ((w_L + w_R) / 2) * r
w = ((w_R - w_L) / (2 * b)) * r
```

PĂ©ldĂˇul `w_L=w_R=10 rad/s` esetĂ©n `v=0,33 m/s`, `w=0 rad/s`, tehĂˇt a robot
egyenesen halad. A ROS DWA a dinamikus ablakban ezeket a kerĂ©ksebessĂ©geket
vizsgĂˇlja, a pĂˇlyĂˇt 0,1 s-os lĂ©pĂ©sekben integrĂˇlja, Ă©s az ĂĽtkĂ¶zĂ©sig mĂ©rt
tĂˇvolsĂˇg alapjĂˇn alkalmazza a Python-fĂ©le megĂˇllĂ­thatĂłsĂˇgi feltĂ©telt:

```text
|v| <= sqrt(2 * a_max * distance_to_obstacle)
```

Ez a dokumentĂˇciĂł Ă©s az `ASTAR_PROJEKT_FOLYAMATBRA.gv` az Ăşj,
kerĂ©ksebessĂ©g-alapĂş ROS DWA-hĂ­vĂˇsi sorrendet tĂĽkrĂ¶zi.

---

# `astar_dwa_node.cpp` â€“ ROS odometria, cĂ©l Ă©s A* Ăştvonal ellenĹ‘rzĂ©se

## 1. A fĂˇjl cĂ©lja

Az `astar_dwa_node.cpp` a ROS 2 Ă©s Gazebo kĂ¶zĂ¶tti vezĂ©rlĹ‘csomĂłpont. Az
`/odom` Ă©s `/scan` adataibĂłl felĂ©pĂ­ti a robot aktuĂˇlis ĂˇllapotĂˇt Ă©s a
pillanatnyi akadĂˇlykĂ©pet, az RViz `/goal_pose` ĂĽzenetĂ©bĹ‘l cĂ©lt vesz Ăˇt, majd
A*-Ăştvonalat Ă©s DWA-sebessĂ©get publikĂˇl `/astar_path` Ă©s `/cmd_vel` tĂ©mĂˇkon.

## 2. Odometriai kezdĹ‘eltolĂˇs

A TurtleBot Gazebo odometria-pluginja a robot spawnhelyĂ©hez kĂ©pest lokĂˇlis
koordinĂˇtĂˇt ad vissza, mikĂ¶zben a modell `(0.8, 0.8)` mĂ©teren spawnol. EzĂ©rt a
konfigurĂˇciĂłban `initial_pose_x = 0.8 m` Ă©s `initial_pose_y = 0.8 m`. Az `odom()`
ezt a vilĂˇgkoordinĂˇtĂˇra ĂˇllĂ­tĂł offsetet adja hozzĂˇ:

```cpp
pose_.x = msg->pose.pose.position.x + initial_pose_x_;
pose_.y = msg->pose.pose.position.y + initial_pose_y_;
```

A Gazebo-odom `(0, 0)` mĂ©rĂ©s Ă­gy a tervezĹ‘ben `(0.8, 0.8)` vilĂˇgpozĂ­ciĂłvĂˇ
vĂˇlik. `resolution = 0.2 m/cella` mellett ez:

```text
column = floor(0.8 / 0.2) = 4
row    = floor(0.8 / 0.2) = 4
```

tehĂˇt a Python-szimulĂˇtor kezdĹ‘cellĂˇja `(4, 4)`, nem egy kĂ©tszeresen eltolt
pozĂ­ciĂł.

## 3. CĂ©l- Ă©s Ăştvonal-adatfolyam

Az RViz `2D Goal Pose` eszkĂ¶ze `geometry_msgs/msg/PoseStamped` ĂĽzenetet kĂĽld
`/goal_pose` tĂ©mĂˇn. A node a vilĂˇgkoordinĂˇtĂˇs `x` Ă©s `y` Ă©rtĂ©ket eltĂˇrolja,
majd a vezĂ©rlĂ©si ciklusban a jelenlegi pozĂ­ciĂłbĂłl Ă©s a cĂ©lbĂłl cellĂˇt kĂ©szĂ­t.
Az A* eredmĂ©nye `nav_msgs/msg/Path` formĂˇban jelenik meg `/astar_path`-on;
az Ăştvonal pontjai az `odom` frame-ben, 0,2 mĂ©teres cellakĂ¶zĂ©ppontokkĂ©nt
szerepelnek. A kĂ¶vetkezĹ‘ waypointot a DWA lokĂˇlis vezĂ©rlĂ©se kĂ¶veti, amely a
`/cmd_vel` Twist ĂĽzenetet publikĂˇlja.

## 4. BiztonsĂˇgi feltĂ©telek

Odometria nĂ©lkĂĽl a vezĂ©rlĹ‘ nem tervez. Ă‰rvĂ©nytelen vagy foglalt kezdĹ‘- illetve
cĂ©lcella esetĂ©n az A* figyelmeztetĂ©st Ă­r, ĂĽres Ăştvonalat publikĂˇl Ă©s nulla
sebessĂ©ggel ĂˇllĂ­tja meg a robotot. EzĂ©rt a `/astar_path` topic meglĂ©te Ă¶nmagĂˇban
nem elĂ©g: az ĂĽzenet `poses` tĂ¶mbjĂ©nek is tartalmaznia kell Ăştvonalpontokat.

## 5. EllenĹ‘rzĂ¶tt futĂˇs

A javĂ­tĂˇs ellenĹ‘rzĂ©sĂ©hez a kĂ¶vetkezĹ‘ parancs futott:

```bash
colcon build --packages-select astar_dwa_controller --symlink-install
```

A build sikeres volt. Tiszta Gazebo- Ă©s bridge-indĂ­tĂˇs utĂˇn a `/goal_pose`
cĂ©l `(5.50, 3.50)` Ă©rtĂ©kkel Ă©rkezett meg, a node `ut=27 pont` Ăştvonalat Ă­rt
a naplĂłba, Ă©s az `/astar_path` ĂĽzenet 27, a cĂ©lhoz vezetĹ‘ pontot tartalmazott.

---

# PĂˇlyahatĂˇr-vĂ©delem Ă©s a Gazebo-pĂˇlya nagyĂ­tĂˇsa

A korĂˇbbi `6,0 m x 4,0 m` tĂ©rkĂ©p csak az A* cellakeresĂ©sĂ©nek hatĂˇra volt. A DWA
elĹ‘rejelzĂ©se azonban kizĂˇrĂłlag a LiDAR Ăˇltal Ă©rzĂ©kelt akadĂˇlyokat vizsgĂˇlta,
ezĂ©rt a pĂˇlya szĂ©lĂ©n nem volt olyan feltĂ©tel, amely a sebessĂ©gjelĂ¶ltet
elutasĂ­totta volna. A Gazebo-vilĂˇgban sem volt fizikai hatĂˇrfal.

Az aktuĂˇlis pĂˇlya `8,0 m x 5,0 m`, `0,2 m/cella` felbontĂˇssal, vagyis
`40 x 25` cellĂˇs. A robot kezdĹ‘pontja `(0,8 m, 0,8 m)`, amelynek cellĂˇja:

```text
column = floor(0.8 / 0.2) = 4
row    = floor(0.8 / 0.2) = 4
```

A DWA most minden elĹ‘rejelzett pontnĂˇl ellenĹ‘rzi a
`robot_radius + safety_margin = 0,28 + 0,15 = 0,43 m` biztonsĂˇgi sĂˇvot.
Ez azt jelenti, hogy a robot kĂ¶zĂ©ppontja nem kĂ¶zelĂ­theti meg a pĂˇlya szĂ©lĂ©t
`0,43 m`-nĂ©l jobban. PĂ©ldĂˇul az alsĂł hatĂˇrnĂˇl a megengedett tartomĂˇny kezdete
`y = 0,43 m`; az ennĂ©l kisebb `y` Ă©rtĂ©ket eredmĂ©nyezĹ‘ DWA-jelĂ¶ltet a node
veszĂ©lyesnek jelĂ¶li Ă©s nem vĂˇlasztja ki.

A vilĂˇgfĂˇjl nĂ©gy statikus falat is tartalmaz a `0..8 m` Ă©s `0..5 m` terĂĽlet
kĂ¶rĂĽl. ĂŤgy a vizuĂˇlis pĂˇlya Ă©s a tervezĹ‘ rĂˇcsa ugyanazt a koordinĂˇtatartomĂˇnyt
hasznĂˇlja. Ha a robot mĂˇr a biztonsĂˇgi hatĂˇron kĂ­vĂĽl van, a vezĂ©rlĹ‘ nulla
`/cmd_vel` Ă©rtĂ©ket kĂĽld, Ă©s figyelmeztetĂ©st Ă­r a naplĂłba.

A ROS- Ă©s Python-DWA kĂ¶zĂ¶tti fontos kĂĽlĂ¶nbsĂ©g, hogy a ROS-vezĂ©rlĹ‘ a
kerĂ©ksebessĂ©g-jelĂ¶ltekbĹ‘l szĂˇmĂ­tott `v` Ă©s `w` Ă©rtĂ©keket publikĂˇlja. Ha a
jelĂ¶lt tĂşllĂ©pi a publikĂˇlt sebessĂ©ghatĂˇrt, a korĂˇbbi kĂłd csak a vĂ©gsĹ‘ Twist
ĂĽzenetet vĂˇgta le. PĂ©ldĂˇul egy `w = 1,86 rad/s` jelĂ¶ltbĹ‘l `1,0 rad/s` kerĂĽlt
ki a topicra, mikĂ¶zben a belsĹ‘ kerĂ©kĂˇllapot tovĂˇbbra is az `1,86` Ă©rtĂ©kĹ±
jelĂ¶ltet kĂ¶vette. Ez eltĂ©rĂ©st okozott a tervezett Ă©s a tĂ©nyleges mozgĂˇs kĂ¶zĂ¶tt.
Az aktuĂˇlis kĂłd mĂˇr a DWA pontozĂˇsa elĹ‘tt elutasĂ­tja azokat a jelĂ¶lteket,
amelyek `v > 0,32 m/s` vagy `|w| > 1,0 rad/s` Ă©rtĂ©ket adnak.

Ha a LiDAR-biztonsĂˇgi feltĂ©tel, a pĂˇlyahatĂˇr vagy a sebessĂ©gkorlĂˇt miatt egyetlen
elĹ‘remeneti jelĂ¶lt sem marad, a node ezt kĂĽlĂ¶n kezeli. A korĂˇbbi kerĂ©ksebessĂ©g
helyett lenullĂˇzza a kerĂ©kĂˇllapotot, Ă©s a cĂ©l irĂˇnyĂˇba legfeljebb
`1,0 rad/s` helyben forgĂˇst ad vissza. ĂŤgy a robot nem marad csendben nulla
sebessĂ©gen egy rĂ©gi vagy Ă©rvĂ©nytelen DWA-Ăˇllapot miatt.

---

# IrĂˇnybaĂˇllĂ­tĂˇs a kĂ¶rkĂ¶rĂ¶s mozgĂˇs elkerĂĽlĂ©sĂ©re

A vezĂ©rlĹ‘ a kĂ¶vetkezĹ‘ waypoint Ă©s a robot aktuĂˇlis `pose_.yaw` Ă©rtĂ©ke alapjĂˇn
irĂˇnyhibĂˇt szĂˇmol:

```text
heading_error = wrap(atan2(target_y - pose_y, target_x - pose_x) - yaw)
```

Az `atan2` a cĂ©l felĂ© mutatĂł szĂ¶get adja radiĂˇnban, a `yaw` a robot jelenlegi
irĂˇnyultsĂˇga, a `wrap` pedig `[-pi, pi]` tartomĂˇnyba hozza a kĂĽlĂ¶nbsĂ©get.
PĂ©ldĂˇul ha a cĂ©lirĂˇny `1,2 rad`, a robot irĂˇnya `-0,2 rad`, akkor a hiba
`1,4 rad`, ezĂ©rt a robot elĹ‘szĂ¶r helyben fordul, nem pedig elĹ‘remenetben
kĂ¶rĂ¶z.

Ha az abszolĂşt irĂˇnyhiba nagyobb `0,6 rad` Ă©rtĂ©knĂ©l, a vezĂ©rlĹ‘ `linear.x=0`
Ă©rtĂ©ket kĂĽld, az `angular.z` pedig a hiba elĹ‘jelĂ©nek megfelelĹ‘en legfeljebb
`1,0 rad/s`. A kerĂ©ksebessĂ©g-Ăˇllapotot is nullĂˇzza, Ă­gy a kĂ¶vetkezĹ‘ DWA-ciklus
nem Ă¶rĂ¶kĂ¶l rĂ©gi forgĂˇsi lendĂĽletet. Csak `0,6 rad` alatt indul Ăşjra az
elĹ‘remeneti DWA.
```

### codes_diploma/robot.py

```python
"""DifferenciĂˇlis meghajtĂˇsĂş robotmodell."""

import math

import numpy as np


def get_robot_kinematics(w_L, w_R, config):
	"""KerĂ©ksebessĂ©gbĹ‘l lineĂˇris Ă©s szĂ¶gsebessĂ©get szĂˇmol."""
	v = ((w_L + w_R) / 2) * config.r_kerek
	w = ((w_R - w_L) / (2 * config.b)) * config.r_kerek
	return v, w


class Obstacle:
	def __init__(self, x, y, radius=0.1, vx=0.0, vy=0.0):
		self.x = x
		self.y = y
		self.radius = radius
		self.vx = vx
		self.vy = vy

	def move(self, dt):
		self.x += self.vx * dt
		self.y += self.vy * dt


class Goal:
	def __init__(self, x, y, tolerance=0.15, slow_down=True, slow_down_distance=0.8, heading=None):
		self.x = x
		self.y = y
		self.tolerance = tolerance
		self.slow_down = slow_down
		self.slow_down_distance = slow_down_distance
		self.heading = heading


class robotconfig:
	def __init__(robot):
		robot.r_kerek = 0.033
		robot.b = 0.08
		robot.w_kerek_max = 15
		robot.a_max = 2
		robot.w_kerek_min = -robot.w_kerek_max
		robot.w_kerek_resolution = 1
		robot.allow_reverse = False
		robot.dt = 0.1
		robot.predict_time = 3
		robot.rob_radius = robot.b + 0.02
		robot.safety_margin = 0.15
		robot.static_safety_margin = 0.01  # Ăšj paramĂ©ter a statikus falak melletti tĹ±rĂ©shez
		robot.Alfa = 5
		robot.Beta = 2
		robot.Gamma = 3
		robot.enable_waypoint_slowdown = False


class robotstate:
	def __init__(robot, x=0, y=0, v=0, w=0, irany=0, w_L=0, w_R=0):
		robot.x = x
		robot.y = y
		robot.v = v
		robot.w = w
		robot.irany = irany
		robot.w_L = w_L
		robot.w_R = w_R


def update(robot, config, w_L_target, w_R_target, dt):
	"""FrissĂ­ti a robotot a gyorsulĂˇskorlĂˇtozĂˇs Ă©s a kinematika alapjĂˇn."""
	max_w_dot = config.a_max / config.r_kerek
	w_L_new = robot.w_L + np.clip(
		w_L_target - robot.w_L,
		-max_w_dot * dt,
		max_w_dot * dt,
	)
	w_R_new = robot.w_R + np.clip(
		w_R_target - robot.w_R,
		-max_w_dot * dt,
		max_w_dot * dt,
	)
	v, w = get_robot_kinematics(w_L_new, w_R_new, config)
	theta_0 = robot.irany

	if abs(w) > 1e-6:
		robot.x += (v / w) * (math.sin(theta_0 + w * dt) - math.sin(theta_0))
		robot.y += -(v / w) * (math.cos(theta_0 + w * dt) - math.cos(theta_0))
	else:
		robot.x += v * math.cos(theta_0) * dt
		robot.y += v * math.sin(theta_0) * dt

	robot.irany += w * dt
	robot.v = v
	robot.w = w
	robot.w_L = w_L_new
	robot.w_R = w_R_new

	return np.array([robot.x, robot.y, robot.irany, robot.v, robot.w, robot.w_L, robot.w_R])
```

### codes_diploma/ros2_astar_dwa_gazebo/README.md

```markdown
# ROS 2 + Gazebo A* + DWA

ROS 2 Jazzy + Gazebo szimulacio TurtleBot3 Waffle robottal:

- A* globalis utvonaltervezes;
- DWA lokalis sebessegvezerles;
- elore ismert statikus akadalyterkep;
- RViz-bol kuldheto celpozicio.

## Forditas WSL2 alatt

WSL Ubuntu terminalban:

```bash
cd "/mnt/c/Users/Rum DĂˇniel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo"
unset AMENT_PREFIX_PATH
unset COLCON_PREFIX_PATH
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source install/setup.bash
```

Ha a launch vagy a vilagfajl modosult, elegendo a Gazebo-csomagot ujraepiteni:

```bash
colcon build --symlink-install --packages-select dwa_gazebo_sim
source install/setup.bash
```

## Mukodo Gazebo-inditas

A megbĂ­zhatĂł indĂ­tĂˇsi sorrend mindig ez:

1. Gazebo vilĂˇg;
2. ROSâ€“Gazebo bridge, A* + DWA vezĂ©rlĹ‘ Ă©s mozgĂł akadĂˇly node;
3. RViz;
4. cĂ©lpozĂ­ciĂł kĂĽldĂ©se az RViz `2D Goal Pose` eszkĂ¶zĂ©vel vagy terminĂˇlbĂłl.

Egy munkamenetben csak egy Gazebo, egy bridge/vezĂ©rlĹ‘ launch Ă©s egy RViz
pĂ©ldĂˇny fusson. Ha a robot nem mozog, elĹ‘szĂ¶r a folyamatokat Ă©s a topicokat
ellenĹ‘rizd, ne kĂĽldj egymĂˇs utĂˇn tĂ¶bb Ăşj cĂ©lt.

A WSLg-s Gazebo GUI a projekt vilĂˇgĂˇval kĂ¶zvetlenĂĽl indĂ­tva mĹ±kĂ¶dik. A fekete
kĂ©pernyĹ‘ elkerĂĽlĂ©sĂ©hez ne kĂ©nyszerĂ­tsd az OpenGL/llvmpipe vĂˇltozĂłkat; az
`xcb` mĂłd Ă©s a rendszer alapĂ©rtelmezett OpenGL beĂˇllĂ­tĂˇsa mĹ±kĂ¶dik.

```bash
export TURTLEBOT3_MODEL=waffle
export DISPLAY=:0
export XDG_RUNTIME_DIR=/tmp/gazebo-runtime
mkdir -p "$XDG_RUNTIME_DIR"
chmod 700 "$XDG_RUNTIME_DIR"
export QT_QPA_PLATFORM=xcb
export QT_X11_NO_MITSHM=1
export GZ_SIM_RESOURCE_PATH=/opt/ros/jazzy/share/turtlebot3_gazebo/models

gz sim -v 4 -r \
"/mnt/c/Users/Rum DĂˇniel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/worlds/dwa_world.sdf"
```

A `GZ_SIM_RESOURCE_PATH` azĂ©rt szĂĽksĂ©ges, mert a vilĂˇgfĂˇjl a
`model://turtlebot3_waffle` modellt hasznĂˇlja. Ha ez nincs beĂˇllĂ­tva, a Gazebo
ablaka elindulhat, de a vilĂˇg vagy a robot nem tĂ¶ltĹ‘dik be.

A kĂ¶zvetlen `gz sim` indĂ­tĂˇs a tesztelt megoldĂˇs. A ROS bridge Ă©s az A* node
kĂĽlĂ¶n, mĂˇsodik terminĂˇlban indĂ­tandĂł, miutĂˇn a Gazebo szerver Ă©s GUI mĂˇr fut.
E nĂ©lkĂĽl az RViz Ă©s a vezĂ©rlĹ‘ nem kap `/scan`, `/odom` Ă©s `/clock` adatokat.

```bash
cd "/mnt/c/Users/Rum DĂˇniel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo"
unset AMENT_PREFIX_PATH
unset COLCON_PREFIX_PATH
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch dwa_gazebo_sim bridge_and_controller.launch.py
```

EllenĹ‘rizd, hogy a bridge Ă©s a vezĂ©rlĹ‘ tĂ©nyleg lĂ©trehozta-e a kapcsolatokat:

```bash
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
ros2 topic list
ros2 topic info /odom
ros2 topic info /scan
ros2 topic info /goal_pose
```

ElvĂˇrt Ăˇllapot:

- `/odom`: `Publisher count: 1`;
- `/scan`: `Publisher count: 1`;
- `/goal_pose`: `Subscription count: 1`;
- `/astar_path`: aktĂ­v publisher.

Ha az `/odom` vagy `/scan` mĂ©g nem lĂ©tezik, vĂˇrj nĂ©hĂˇny mĂˇsodpercet. Ha
tovĂˇbbra sem jelenik meg, ellenĹ‘rizd, hogy a Gazebo szerver fut-e, majd a
bridge-et indĂ­tsd Ăşjra.

Az `rqt_graph` elĹ‘tt vĂˇrd meg, hogy a bridge lĂ©trehozza az `/scan` Ă©s `/odom`
topicokat. A ROS2 discovery gyorsĂ­tĂˇsĂˇhoz ezt hasznĂˇld:

```bash
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
rqt_graph --force-discover
```

Ha az `rqt_graph` ĂĽres, ne indĂ­ts Ăşjabb Gazebo-pĂ©ldĂˇnyt. EllenĹ‘rizd a grĂˇfot
kĂ¶zvetlen discovery-val:

```bash
ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST ros2 node list --no-daemon
ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST ros2 topic list --no-daemon
```

Egy munkamenetben csak egy Gazebo-pĂ©ldĂˇny Ă©s egy bridge fusson. TĂ¶bb rĂ©gi
`gz sim`, `parameter_bridge` vagy `ros2 launch` folyamat ĂĽres vagy hibĂˇs
`rqt_graph`-ot okozhat.

Az A* a statikus akadĂˇlyokat a robot sugarĂˇval nĂ¶veli, de kĂ¶r alakĂş
inflĂˇciĂłval. Ez azĂ©rt fontos, mert a kĂ©t akadĂˇly kĂ¶zĂ¶tti fizikailag ĂˇtjĂˇrhatĂł
rĂ©s Ă­gy nem zĂˇrĂłdik le mestersĂ©gesen nĂ©gyzetes blokkal.

A kĂ©t mozgĂł akadĂˇly a Python-szimulĂˇtorral azonos kezdĹ‘ĂˇllapotbĂłl indul:
`moving_obstacle_1=(2.4, 0.4) m`, sebessĂ©ge `(vx, vy)=(0, 0.20) m/s`,
valamint `moving_obstacle_2=(6.8, 2.1) m`, sebessĂ©ge
`(vx, vy)=(-0.25, 0) m/s`. A `moving_obstacle_node` a bridge-en keresztĂĽl
bekĂ¶tĂ¶tt `/world/dwa_world/set_pose` szolgĂˇltatĂˇssal frissĂ­ti Ĺ‘ket. A node
egyszerre csak egy pozĂ­ciĂłfrissĂ­tĂ©st tart fĂĽggĹ‘ben, ezĂ©rt nem Ăˇrasztja el a
Gazebo szolgĂˇltatĂˇst egymĂˇsra torlĂłdĂł kĂ©rĂ©sekkel.

EllenĹ‘rzĂ©shez:

```bash
ros2 node list
ros2 service list | grep set_pose
ros2 service type /world/dwa_world/set_pose
```

Ha a node elindult, de a modell nem mozog, ellenĹ‘rizd, hogy a world Ăşj pĂ©ldĂˇnya
indult-e a mĂłdosĂ­tott forrĂˇsbĂłl, Ă©s ne maradjon futva egy rĂ©gi Gazebo-pĂ©ldĂˇny.
Az Ăşj world Ă©s az akadĂˇlymozgĂˇs a Python-szimulĂˇciĂł `0,1 s` idĹ‘lĂ©pĂ©ses,
egyenletes `vx/vy` modelljĂ©t kĂ¶veti.

A Gazebo tĂ©rkĂ©pe jelenleg `8 x 5 m`, `0,2 m` felbontĂˇssal, vagyis `40 x 25`
cellĂˇs tervezĂ©si terĂĽlet. A Gazebo robotmodell `(0,8; 0,8) m` helyen spawnol.
Az `/odom` plugin lokĂˇlis koordinĂˇtĂˇjĂˇt a vezĂ©rlĹ‘ a
`rosbot.yaml` `initial_pose_x/y = 0,8 m` offsetjĂ©vel alakĂ­tja tĂ©rkĂ©pi
vilĂˇgkoordinĂˇtĂˇvĂˇ. A tesztelt cĂ©lpozĂ­ciĂł `(6,5; 4,2) m`.

Az RViz-ben az A* Ăştvonal zĂ¶ld, a kivĂˇlasztott DWA-trajektĂłria kĂ©k, a
statikus akadĂˇlyok pirosak, azok robotmĂ©rettel nĂ¶velt biztonsĂˇgi zĂłnĂˇja
halvĂˇnysĂˇrga, a LiDAR Ăˇltal Ă©rzĂ©kelt pontok pedig sĂˇrgĂˇk. A vezĂ©rlĹ‘ alapĂ©rtelmezett
maximĂˇlis lineĂˇris sebessĂ©ge `0,32 m/s`; ez a `rosbot.yaml` paramĂ©terben
ĂˇllĂ­thatĂł.

## RViz inditasa

Harmadik terminalban:

```bash
source /opt/ros/jazzy/setup.bash
source "/mnt/c/Users/Rum DĂˇniel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo/install/setup.bash"
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
export DISPLAY=:0
export XDG_RUNTIME_DIR=/tmp/gazebo-runtime
mkdir -p "$XDG_RUNTIME_DIR"
chmod 700 "$XDG_RUNTIME_DIR"
export QT_QPA_PLATFORM=xcb
export QT_X11_NO_MITSHM=1
ros2 launch dwa_gazebo_sim visualization.launch.py
```

Az RViz konfigurĂˇciĂł automatikusan az `odom` Fixed Frame-et Ă©s a
`2D Goal Pose` eszkĂ¶zt tĂ¶lti be. Ha a gomb nem lĂˇthatĂł, az RViz bal oldali
eszkĂ¶ztĂˇrĂˇban vĂˇlaszd ki a `2D Goal Pose` ikont, majd kattints a tĂ©rkĂ©pen a
cĂ©lhelyre Ă©s hĂşzd meg a kĂ­vĂˇnt irĂˇnyt.

TerminĂˇlbĂłl ugyanĂ­gy kĂĽldhetĹ‘ cĂ©l:

```bash
ros2 topic pub --once /goal_pose geometry_msgs/msg/PoseStamped \
  "{header: {frame_id: odom}, pose: {position: {x: 6.5, y: 4.2, z: 0.0}, orientation: {w: 1.0}}}"
```

Ăšj cĂ©lpozĂ­ciĂłt mindig azutĂˇn kĂĽldj, hogy az `/odom`, `/scan` Ă©s `/goal_pose`
kapcsolatokat ellenĹ‘rizted. A cĂ©lpozĂ­ciĂł nem marad meg a vezĂ©rlĹ‘
ĂşjraindĂ­tĂˇsa utĂˇn.

## Gyors hibaellenĹ‘rzĂ©s

```bash
ros2 node list
ros2 topic list
ros2 topic info /odom
ros2 topic info /scan
ros2 topic info /goal_pose
ros2 topic echo /astar_path --once
```

Ha az RViz-ben nem tudsz cĂ©lt adni, ellenĹ‘rizd, hogy az `astar_dwa_node` fut-e
Ă©s a `/goal_pose` topicnĂˇl `Subscription count: 1` lĂˇthatĂł-e. Ha az RViz
ablak ĂĽres, ellenĹ‘rizd az `odom` Fixed Frame-et Ă©s azt, hogy az `/odom` Ă©s
`/scan` publisher szĂˇmlĂˇlĂłja egy-e. Ha a robot szĹ±k akadĂˇlyrĂ©sben lassĂ­t,
az aktuĂˇlis DWA-diagnosztika a bridge/vezĂ©rlĹ‘ terminĂˇlban lĂˇthatĂł:

```text
DWA jeloltek: teszt=..., sebesseg=..., hatar=..., akadaly=..., fekezes=...
```

Az `akadaly` Ă©rtĂ©k nĂ¶vekedĂ©se LiDAR-alapĂş biztonsĂˇgi elutasĂ­tĂˇst jelent; ez
szĹ±k ĂˇtjĂˇrĂłban lassulĂˇst okozhat, de Ă¶nmagĂˇban nem jelenti azt, hogy az A*
nem talĂˇlt Ăştvonalat.

## Fontos topicok

- `/goal_pose`: kezi celpozicio;
- `/astar_path`: A* utvonal;
- `/astar_map`: ismert akadalyterkep;
- `/scan`: LiDAR-meres;
- `/cmd_vel`: Gazebo fele kuldott sebessegparancs.

## Leallitas

A futo Gazebo-terminalban nyomd meg a `Ctrl+C` billentyukombinaciot. Ez nem
beirando shell-parancs.
```

### codes_diploma/ros2_astar_dwa_gazebo/src/astar_dwa_controller/CMakeLists.txt

```
cmake_minimum_required(VERSION 3.8)
project(astar_dwa_controller)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(visualization_msgs REQUIRED)
find_package(tf2_ros REQUIRED)

add_executable(astar_dwa_node src/astar_dwa_node.cpp)
ament_target_dependencies(astar_dwa_node rclcpp geometry_msgs nav_msgs sensor_msgs visualization_msgs tf2_ros)

install(TARGETS astar_dwa_node DESTINATION lib/${PROJECT_NAME})
install(DIRECTORY config launch rviz DESTINATION share/${PROJECT_NAME})
ament_package()
```

### codes_diploma/ros2_astar_dwa_gazebo/src/astar_dwa_controller/config/rosbot.yaml

```yaml
astar_dwa_node:
  ros__parameters:
    cmd_vel_topic: /cmd_vel
    odom_topic: /odom
    scan_topic: /scan
    goal_topic: /goal_pose
    path_topic: /astar_path
    goal_x: 6.5
    goal_y: 4.2
    known_obstacle_x: [2.1, 2.1, 2.1, 2.1, 2.1, 2.1, 2.1, 2.1, 2.1, 2.1, 2.1, 2.1, 2.5, 2.7, 2.9, 3.1, 3.3, 3.5, 3.7, 3.9, 5.1, 5.3, 5.5]
    known_obstacle_y: [0.5, 0.7, 0.9, 1.1, 2.7, 2.9, 3.1, 3.3, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5]
    known_obstacle_radius: [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
    map_size: 8.2
    map_height: 5.2
    map_origin_x: -0.1
    map_origin_y: -0.1
    initial_pose_x: 0.8
    initial_pose_y: 0.8
    resolution: 0.20
    robot_radius: 0.28
    control_period: 0.10
    max_linear_velocity: 0.32
    max_angular_velocity: 1.00
    wheel_radius: 0.033
    wheel_base: 0.08
    wheel_max: 15.0
    wheel_resolution: 1.0
    acceleration_limit: 2.0
    predict_time: 1.5
    safety_margin: 0.05
    alpha: 5.0
    beta: 2.0
    gamma: 3.0
```

### codes_diploma/ros2_astar_dwa_gazebo/src/astar_dwa_controller/launch/controller.launch.py

```python
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    package_share = get_package_share_directory("astar_dwa_controller")
    return LaunchDescription([
        Node(
            package="astar_dwa_controller",
            executable="astar_dwa_node",
            name="astar_dwa_node",
            output="screen",
            parameters=[os.path.join(package_share, "config", "rosbot.yaml")],
        )
    ])
```

### codes_diploma/ros2_astar_dwa_gazebo/src/astar_dwa_controller/package.xml

```xml
<?xml version="1.0"?>
<package format="3">
  <name>astar_dwa_controller</name>
  <version>0.1.0</version>
  <description>RobotfĂĽggetlen C++ A* Ă©s DWA ROS 2 vezĂ©rlĹ‘.</description>
  <maintainer email="rumdaniel@todo.todo">rumdaniel</maintainer>
  <license>MIT</license>
  <depend>rclcpp</depend>
  <depend>geometry_msgs</depend>
  <depend>nav_msgs</depend>
  <depend>sensor_msgs</depend>
  <depend>visualization_msgs</depend>
  <depend>tf2_ros</depend>
  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>
```

### codes_diploma/ros2_astar_dwa_gazebo/src/astar_dwa_controller/rviz/astar_dwa.rviz

```
Panels:
  - Class: rviz_common/Displays
    Name: Displays
  - Class: rviz_common/Views
    Name: Views
Visualization Manager:
  Class: ""
  Displays:
    - Class: rviz_default_plugins/Grid
      Name: Ground grid
      Enabled: true
      Cell Size: 1
      Plane: XY
      Plane Cell Count: 20
      Reference Frame: <Fixed Frame>
    - Class: rviz_default_plugins/Map
      Name: Known occupancy map
      Enabled: true
      Topic:
        Depth: 1
        Durability Policy: Transient Local
        History Policy: Keep Last
        Reliability Policy: Reliable
        Value: /astar_map
      Alpha: 0.45
      Color Scheme: map
      Draw Behind: true
    - Class: rviz_default_plugins/TF
      Name: TF
      Enabled: true
      Frame Timeout: 15
      Marker Scale: 0.5
      Show Arrows: false
      Show Axes: false
      Show Names: false
    - Class: rviz_default_plugins/LaserScan
      Name: LiDAR
      Enabled: true
      Topic:
        Depth: 5
        Durability Policy: Volatile
        History Policy: Keep Last
        Reliability Policy: Best Effort
        Value: /scan
      Size (m): 0.04
      Style: Points
      Color: 255; 170; 0
      Decay Time: 0.2
    - Class: rviz_default_plugins/Path
      Name: A* planned path
      Enabled: true
      Topic:
        Depth: 5
        Durability Policy: Volatile
        History Policy: Keep Last
        Reliability Policy: Reliable
        Value: /astar_path
      Color: 0; 255; 40
      Line Style: Billboards
      Line Width: 0.3
    - Class: rviz_default_plugins/Odometry
      Name: Odometry
      Enabled: true
      Topic:
        Depth: 5
        Durability Policy: Volatile
        History Policy: Keep Last
        Reliability Policy: Reliable
        Value: /odom
      Keep: 100
      Shape: Arrow
      Color: 80; 150; 255
      Shaft Length: 0.35
      Shaft Radius: 0.04
    - Class: rviz_default_plugins/MarkerArray
      Name: A* and DWA internals
      Enabled: true
      Marker Topic: /astar_dwa_markers
  Enabled: true
  Global Options:
    Background Color: 35; 40; 48
    Fixed Frame: odom
    Frame Rate: 30
  Name: root
  Tools:
    - Class: rviz_default_plugins/Interact
    - Class: rviz_default_plugins/MoveCamera
    - Class: rviz_default_plugins/Select
    - Class: rviz_default_plugins/SetGoal
      Topic: /goal_pose
  Views:
    Current:
      Class: rviz_default_plugins/TopDownOrtho
      Name: Top view
      Angle: 0
      Scale: 8
      Target Frame: odom
      X: 4
      Y: 2.5
Window Geometry:
  Height: 900
  Width: 1400
  X: 50
  Y: 50
```

### codes_diploma/ros2_astar_dwa_gazebo/src/astar_dwa_controller/src/astar_dwa_node.cpp

```cpp
#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <functional>
#include <limits>
#include <memory>
#include <optional>
#include <queue>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

#include "geometry_msgs/msg/pose_stamped.hpp"
#include "geometry_msgs/msg/transform_stamped.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include "nav_msgs/msg/occupancy_grid.hpp"
#include "nav_msgs/msg/path.hpp"
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"
#include "tf2_ros/transform_broadcaster.h"
#include "visualization_msgs/msg/marker_array.hpp"

namespace {
struct Obstacle { double x, y, radius; };
struct Pose { double x{0.0}, y{0.0}, yaw{0.0}; };
double angle_error(double value) { return std::atan2(std::sin(value), std::cos(value)); }
double distance(double ax, double ay, double bx, double by) {
  return std::hypot(ax - bx, ay - by);
}
}

class AStarDwaNode final : public rclcpp::Node {
public:
  AStarDwaNode() : Node("astar_dwa_node") {
    cmd_topic_ = declare_parameter("cmd_vel_topic", std::string("/cmd_vel"));
    odom_topic_ = declare_parameter("odom_topic", std::string("/odom"));
    scan_topic_ = declare_parameter("scan_topic", std::string("/scan"));
    goal_topic_ = declare_parameter("goal_topic", std::string("/goal_pose"));
    path_topic_ = declare_parameter("path_topic", std::string("/astar_path"));
    goal_x_ = declare_parameter("goal_x", 0.0);
    goal_y_ = declare_parameter("goal_y", 0.0);
    map_size_ = declare_parameter("map_size", 16.0);
    map_height_ = declare_parameter("map_height", 4.0);
    map_origin_x_ = declare_parameter("map_origin_x", 0.0);
    map_origin_y_ = declare_parameter("map_origin_y", 0.0);
    initial_pose_x_ = declare_parameter("initial_pose_x", 0.5);
    initial_pose_y_ = declare_parameter("initial_pose_y", 0.5);
    resolution_ = declare_parameter("resolution", 0.20);
    robot_radius_ = declare_parameter("robot_radius", 0.28);
    max_linear_velocity_ = declare_parameter("max_linear_velocity", 0.32);
    max_angular_velocity_ = declare_parameter("max_angular_velocity", 1.0);
    wheel_radius_ = declare_parameter("wheel_radius", 0.033);
    wheel_base_ = declare_parameter("wheel_base", 0.08);
    wheel_max_ = declare_parameter("wheel_max", 15.0);
    wheel_resolution_ = declare_parameter("wheel_resolution", 1.0);
    acceleration_limit_ = declare_parameter("acceleration_limit", 2.0);
    predict_time_ = declare_parameter("predict_time", 3.0);
    safety_margin_ = declare_parameter("safety_margin", 0.15);
    alpha_ = declare_parameter("alpha", 5.0);
    beta_ = declare_parameter("beta", 2.0);
    gamma_ = declare_parameter("gamma", 3.0);
    known_obstacle_x_ = declare_parameter(
      "known_obstacle_x", std::vector<double>{});
    known_obstacle_y_ = declare_parameter(
      "known_obstacle_y", std::vector<double>{});
    known_obstacle_radius_ = declare_parameter(
      "known_obstacle_radius", std::vector<double>{});
    const double period = declare_parameter("control_period", 0.10);
    cmd_pub_ = create_publisher<geometry_msgs::msg::Twist>(cmd_topic_, 10);
    path_pub_ = create_publisher<nav_msgs::msg::Path>(path_topic_, 10);
    map_pub_ = create_publisher<nav_msgs::msg::OccupancyGrid>(
      "/astar_map", rclcpp::QoS(1).transient_local().reliable());
    marker_pub_ = create_publisher<visualization_msgs::msg::MarkerArray>("/astar_dwa_markers", 10);
    tf_broadcaster_ = std::make_unique<tf2_ros::TransformBroadcaster>(*this);
    odom_sub_ = create_subscription<nav_msgs::msg::Odometry>(
      odom_topic_, 10, [this](nav_msgs::msg::Odometry::ConstSharedPtr msg) { odom(msg); });
    scan_sub_ = create_subscription<sensor_msgs::msg::LaserScan>(
      scan_topic_, 10, [this](sensor_msgs::msg::LaserScan::ConstSharedPtr msg) { scan(msg); });
    goal_sub_ = create_subscription<geometry_msgs::msg::PoseStamped>(
      goal_topic_, 10, [this](geometry_msgs::msg::PoseStamped::ConstSharedPtr msg) {
        goal_x_ = msg->pose.position.x; goal_y_ = msg->pose.position.y;
        has_goal_ = true;
        RCLCPP_INFO(get_logger(), "Uj cel: x=%.2f m, y=%.2f m", goal_x_, goal_y_); });
    timer_ = create_wall_timer(
      std::chrono::duration_cast<std::chrono::milliseconds>(
        std::chrono::duration<double>(period)),
      [this]() { control(); });
    RCLCPP_INFO(get_logger(), "RobotfĂĽggetlen A* + DWA C++ node elindult");
  }

private:
  void odom(const nav_msgs::msg::Odometry::ConstSharedPtr msg) {
    const auto & q = msg->pose.pose.orientation;
    pose_.x = msg->pose.pose.position.x + initial_pose_x_;
    pose_.y = msg->pose.pose.position.y + initial_pose_y_;
    pose_.yaw = std::atan2(2.0 * (q.w * q.z + q.x * q.y),
                           1.0 - 2.0 * (q.y * q.y + q.z * q.z));
    geometry_msgs::msg::TransformStamped transform;
    transform.header.stamp = msg->header.stamp;
    transform.header.frame_id = "odom";
    transform.child_frame_id = "base_link";
    transform.transform.translation.x = pose_.x;
    transform.transform.translation.y = pose_.y;
    transform.transform.rotation = q;
    tf_broadcaster_->sendTransform(transform);
    transform.header.frame_id = "base_link";
    transform.child_frame_id = "base_scan";
    transform.transform.translation.x = 0.0;
    transform.transform.translation.y = 0.0;
    transform.transform.translation.z = 0.16;
    transform.transform.rotation.x = 0.0;
    transform.transform.rotation.y = 0.0;
    transform.transform.rotation.z = 0.0;
    transform.transform.rotation.w = 1.0;
    tf_broadcaster_->sendTransform(transform);
    have_odom_ = true;
  }
  void scan(const sensor_msgs::msg::LaserScan::ConstSharedPtr msg) {
    scan_ = msg;
    have_scan_ = true;
  }
  int map_width() const {
    return std::max(3, static_cast<int>(std::ceil(map_size_ / resolution_)));
  }
  int map_height() const {
    return std::max(3, static_cast<int>(std::ceil(map_height_ / resolution_)));
  }
  std::vector<Obstacle> obstacles() const {
    std::vector<Obstacle> result;
    if (!scan_) return result;
    constexpr double max_sensor_distance = 3.0;
    constexpr double front_half_angle = 1.57079632679;
    for (std::size_t i = 0; i < scan_->ranges.size(); ++i) {
      const double r = scan_->ranges[i];
      if (!std::isfinite(r) || r < scan_->range_min || r > scan_->range_max) continue;
      if (r < robot_radius_ + 0.08) continue;
      const double relative_angle =
        scan_->angle_min + static_cast<double>(i) * scan_->angle_increment;
      if (r > max_sensor_distance || std::abs(angle_error(relative_angle)) > front_half_angle)
        continue;
      const double a = pose_.yaw + relative_angle;
      result.push_back({pose_.x + r * std::cos(a), pose_.y + r * std::sin(a), 0.0});
    }
    return result;
  }
  std::vector<Obstacle> planning_obstacles() const {
    std::vector<Obstacle> result;
    const std::size_t count = std::min(
      {known_obstacle_x_.size(), known_obstacle_y_.size(), known_obstacle_radius_.size()});
    for (std::size_t i = 0; i < count; ++i)
      result.push_back({known_obstacle_x_[i], known_obstacle_y_[i], known_obstacle_radius_[i]});
    return result;
  }
  std::vector<std::pair<double, double>> astar(
    const std::vector<Obstacle> & sensed_obstacles) const {
    const int width = std::max(3, static_cast<int>(std::ceil(map_size_ / resolution_)));
    const int height = map_height();
    const double ox = map_origin_x_, oy = map_origin_y_;
    std::vector<bool> blocked(width * height, false);
    auto inside = [width, height](int r, int c) { return r >= 0 && c >= 0 && r < height && c < width; };
    auto index = [width](int r, int c) { return r * width + c; };
    auto cell = [resolution = resolution_, ox, oy](double x, double y) {
      return std::pair<int, int>{static_cast<int>(std::floor((y - oy) / resolution)),
                                 static_cast<int>(std::floor((x - ox) / resolution))};
    };
    auto world = [resolution = resolution_, ox, oy](int r, int c) {
      return std::pair<double, double>{ox + (c + 0.5) * resolution, oy + (r + 0.5) * resolution};
    };
    (void)sensed_obstacles;
    const auto search_obstacles = planning_obstacles();
    for (const auto & obstacle : search_obstacles) {
      const auto center = cell(obstacle.x, obstacle.y);
      const double inflation = robot_radius_ + obstacle.radius;
      const int radius = static_cast<int>(std::ceil(
        inflation / resolution_));
      for (int r = center.first - radius; r <= center.first + radius; ++r)
        for (int c = center.second - radius; c <= center.second + radius; ++c)
          if (inside(r, c)) {
            const auto point = world(r, c);
            if (distance(point.first, point.second, obstacle.x, obstacle.y) <= inflation) {
              blocked[index(r, c)] = true;
            }
          }
    }
    const double boundary_margin = robot_radius_ + safety_margin_;
    for (int r = 0; r < height; ++r) {
      for (int c = 0; c < width; ++c) {
        const auto point = world(r, c);
        if (point.first < ox + boundary_margin ||
            point.first > ox + map_size_ - boundary_margin ||
            point.second < oy + boundary_margin ||
            point.second > oy + map_height_ - boundary_margin) {
          blocked[index(r, c)] = true;
        }
      }
    }
    const auto start = cell(pose_.x, pose_.y), target = cell(goal_x_, goal_y_);
    if (!inside(start.first, start.second) || !inside(target.first, target.second) ||
        blocked[index(start.first, start.second)] || blocked[index(target.first, target.second)]) {
      RCLCPP_WARN_THROTTLE(
        get_logger(), *get_clock(), 5000,
        "A* ervenytelen kezdo/celcella: start=(%d,%d), cel=(%d,%d), "
        "start_blocked=%s, cel_blocked=%s",
        start.first, start.second, target.first, target.second,
        (inside(start.first, start.second) && blocked[index(start.first, start.second)])
          ? "igen" : "nem",
        (inside(target.first, target.second) && blocked[index(target.first, target.second)])
          ? "igen" : "nem");
      return {};
    }
    struct Entry { double f, g; int r, c; bool operator>(const Entry & other) const { return f > other.f; } };
    std::priority_queue<Entry, std::vector<Entry>, std::greater<Entry>> open;
    std::vector<double> cost(width * width, std::numeric_limits<double>::infinity());
    std::vector<int> parent(width * width, -1);
    auto heuristic = [&target](int r, int c) { return std::hypot(target.first - r, target.second - c); };
    open.push({heuristic(start.first, start.second), 0.0, start.first, start.second});
    cost[index(start.first, start.second)] = 0.0;
    const int directions[8][2] = {{1,0},{-1,0},{0,1},{0,-1},{1,1},{1,-1},{-1,1},{-1,-1}};
    while (!open.empty()) {
      const auto current = open.top(); open.pop();
      if (current.g > cost[index(current.r, current.c)]) continue;
      if (current.r == target.first && current.c == target.second) break;
      for (const auto & direction : directions) {
        const int nr = current.r + direction[0], nc = current.c + direction[1];
        if (!inside(nr, nc) || blocked[index(nr, nc)]) continue;
        if (direction[0] && direction[1] &&
            (blocked[index(current.r, nc)] || blocked[index(nr, current.c)])) continue;
        const double ng = current.g + ((direction[0] && direction[1]) ? std::sqrt(2.0) : 1.0);
        if (ng < cost[index(nr, nc)]) {
          cost[index(nr, nc)] = ng; parent[index(nr, nc)] = index(current.r, current.c);
          open.push({ng + heuristic(nr, nc), ng, nr, nc});
        }
      }
    }
    std::vector<std::pair<double, double>> path;
    int current = index(target.first, target.second), start_index = index(start.first, start.second);
    if (current != start_index && parent[current] < 0) return path;
    while (current >= 0) {
      path.push_back(world(current / width, current % width));
      if (current == start_index) break;
      current = parent[current];
    }
    std::reverse(path.begin(), path.end());
    return path;
  }
  void publish_map() {
    nav_msgs::msg::OccupancyGrid map;
    map.header.frame_id = "odom";
    map.header.stamp = now();
    map.info.resolution = resolution_;
    map.info.width = static_cast<std::uint32_t>(map_width());
    map.info.height = static_cast<std::uint32_t>(map_height());
    map.info.origin.position.x = map_origin_x_;
    map.info.origin.position.y = map_origin_y_;
    map.info.origin.orientation.w = 1.0;
    map.data.assign(map.info.width * map.info.height, 0);
    auto cell = [this](double x, double y) {
      return std::pair<int, int>{
        static_cast<int>(std::floor((x - map_origin_x_) / resolution_)),
        static_cast<int>(std::floor((y - map_origin_y_) / resolution_))};
    };
    const int width = static_cast<int>(map.info.width);
    for (const auto & obstacle : planning_obstacles()) {
      const auto center = cell(obstacle.x, obstacle.y);
      const int radius = static_cast<int>(std::ceil(
        (obstacle.radius + robot_radius_) / resolution_));
      for (int y = center.second - radius; y <= center.second + radius; ++y) {
        for (int x = center.first - radius; x <= center.first + radius; ++x) {
          if (x >= 0 && y >= 0 && x < width && y < map_height()) {
            const double dx = (x + 0.5) * resolution_ - (center.first + 0.5) * resolution_;
            const double dy = (y + 0.5) * resolution_ - (center.second + 0.5) * resolution_;
            if (std::hypot(dx, dy) <= obstacle.radius + robot_radius_) {
            map.data[y * width + x] = 100;
            }
          }
        }
      }
    }
    map_pub_->publish(map);
  }
  std::pair<double, double> wheel_kinematics(double left, double right) const {
    const double velocity = ((left + right) / 2.0) * wheel_radius_;
    const double angular = ((right - left) / (2.0 * wheel_base_)) * wheel_radius_;
    return {velocity, angular};
  }
  std::pair<double, double> dwa(double target_x, double target_y,
                                const std::vector<Obstacle> & sensed) {
    const double wheel_acceleration = acceleration_limit_ / wheel_radius_;
    const double left_min = std::max(-wheel_max_, wheel_left_ - wheel_acceleration * dt_);
    const double left_max = std::min(wheel_max_, wheel_left_ + wheel_acceleration * dt_);
    const double right_min = std::max(-wheel_max_, wheel_right_ - wheel_acceleration * dt_);
    const double right_max = std::min(wheel_max_, wheel_right_ + wheel_acceleration * dt_);
    double best_score = -std::numeric_limits<double>::infinity();
    double best_left = wheel_left_, best_right = wheel_right_;
    bool found_candidate = false;
    std::size_t rejected_velocity = 0;
    std::size_t rejected_boundary = 0;
    std::size_t rejected_obstacle = 0;
    std::size_t rejected_braking = 0;
    std::size_t tested_candidates = 0;
    for (double left = left_min; left <= left_max + wheel_resolution_ * 0.5;
         left += wheel_resolution_) {
      for (double right = right_min; right <= right_max + wheel_resolution_ * 0.5;
           right += wheel_resolution_) {
        ++tested_candidates;
        const auto candidate = wheel_kinematics(left, right);
        const double v = candidate.first;
        if (v < 0.0) {
          ++rejected_velocity;
          continue;
        }
        if (v > max_linear_velocity_ ||
            std::abs(candidate.second) > max_angular_velocity_) {
          ++rejected_velocity;
          continue;
        }
        double x = pose_.x, y = pose_.y, yaw = pose_.yaw;
        double simulated_left = wheel_left_, simulated_right = wheel_right_;
        double collision_distance = 10.0;
        bool safe = true;
        for (double t = 0.0; t < predict_time_; t += dt_) {
          simulated_left += std::clamp(
            left - simulated_left, -wheel_acceleration * dt_, wheel_acceleration * dt_);
          simulated_right += std::clamp(
            right - simulated_right, -wheel_acceleration * dt_, wheel_acceleration * dt_);
          const auto simulated = wheel_kinematics(simulated_left, simulated_right);
          if (std::abs(simulated.second) > 1e-6) {
            x += (simulated.first / simulated.second) *
              (std::sin(yaw + simulated.second * dt_) - std::sin(yaw));
            y -= (simulated.first / simulated.second) *
              (std::cos(yaw + simulated.second * dt_) - std::cos(yaw));
          } else {
            x += simulated.first * std::cos(yaw) * dt_;
            y += simulated.first * std::sin(yaw) * dt_;
          }
          yaw += simulated.second * dt_;
          const double margin = robot_radius_ + safety_margin_;
          if (x < map_origin_x_ + margin ||
              x > map_origin_x_ + map_size_ - margin ||
              y < map_origin_y_ + margin ||
              y > map_origin_y_ + map_height_ - margin) {
            collision_distance = std::min({
              x - map_origin_x_, map_origin_x_ + map_size_ - x,
              y - map_origin_y_, map_origin_y_ + map_height_ - y});
            safe = false;
            ++rejected_boundary;
            break;
          }
          for (const auto & obstacle : sensed) {
            if (distance(x, y, obstacle.x, obstacle.y) <=
                robot_radius_ + obstacle.radius + safety_margin_) {
              collision_distance = std::abs(simulated.first) * t;
              safe = false;
              ++rejected_obstacle;
              break;
            }
          }
          if (!safe) break;
        }
        if (!safe) continue;
        if (std::abs(candidate.first) >
          std::sqrt(2.0 * acceleration_limit_ * collision_distance)) {
          ++rejected_braking;
          continue;
        }
        const double goal_heading = std::atan2(target_y - y, target_x - x);
        const double heading_score =
          (M_PI - std::abs(angle_error(goal_heading - yaw))) / M_PI;
        const double distance_score = collision_distance;
        const double velocity_score = candidate.first / (wheel_max_ * wheel_radius_);
        const double score = alpha_ * heading_score + beta_ * distance_score +
          gamma_ * velocity_score;
        if (score > best_score) {
          best_score = score;
          best_left = left;
          best_right = right;
          found_candidate = true;
        }
      }
    }
    RCLCPP_INFO_THROTTLE(
      get_logger(), *get_clock(), 2000,
      "DWA jeloltek: teszt=%zu, sebesseg=%zu, hatar=%zu, akadaly=%zu, fekezes=%zu, elfogadott=%s",
      tested_candidates, rejected_velocity, rejected_boundary, rejected_obstacle,
      rejected_braking, found_candidate ? "igen" : "nem");
    if (!found_candidate) {
      const double target_heading = std::atan2(target_y - pose_.y, target_x - pose_.x);
      const double turn_error = angle_error(target_heading - pose_.yaw);
      wheel_left_ = 0.0;
      wheel_right_ = 0.0;
      return {0.0, std::clamp(turn_error, -max_angular_velocity_, max_angular_velocity_)};
    }
    wheel_left_ = best_left;
    wheel_right_ = best_right;
    return wheel_kinematics(wheel_left_, wheel_right_);
  }
  visualization_msgs::msg::Marker make_marker(
    int id, int type, double x, double y, double z,
    double scale, float r, float g, float b) const {
    visualization_msgs::msg::Marker marker;
    marker.header.frame_id = "odom";
    marker.header.stamp = now();
    marker.ns = "astar_dwa";
    marker.id = id;
    marker.type = type;
    marker.action = visualization_msgs::msg::Marker::ADD;
    marker.pose.position.x = x;
    marker.pose.position.y = y;
    marker.pose.position.z = z;
    marker.pose.orientation.w = 1.0;
    marker.scale.x = scale;
    marker.scale.y = scale;
    marker.scale.z = scale;
    marker.color.r = r;
    marker.color.g = g;
    marker.color.b = b;
    marker.color.a = 0.9;
    marker.lifetime = rclcpp::Duration::from_seconds(0.4);
    return marker;
  }
  void publish_debug(const std::vector<std::pair<double, double>> & path,
                     double target_x, double target_y,
                     double velocity, double angular_velocity) {
    visualization_msgs::msg::MarkerArray markers;
    auto goal = make_marker(0, visualization_msgs::msg::Marker::SPHERE,
                            target_x, target_y, 0.35, 0.45, 0.1, 1.0, 0.2);
    markers.markers.push_back(goal);
    auto goal_ring = make_marker(3, visualization_msgs::msg::Marker::CYLINDER,
                                 target_x, target_y, 0.03, 1.0, 0.1, 1.0, 0.2);
    goal_ring.scale.z = 0.04;
    goal_ring.color.a = 0.75;
    markers.markers.push_back(goal_ring);
    auto goal_text = make_marker(4, visualization_msgs::msg::Marker::TEXT_VIEW_FACING,
                                 target_x, target_y, 0.85, 0.1, 0.1, 1.0, 0.2);
    goal_text.text = "CEL";
    goal_text.scale.z = 0.28;
    goal_text.color.a = 1.0;
    markers.markers.push_back(goal_text);
    auto path_marker = make_marker(1, visualization_msgs::msg::Marker::LINE_STRIP,
                                   0.0, 0.0, 0.18, 0.1, 0.1, 1.0, 0.2);
    path_marker.points.clear();
    for (const auto & point : path) {
      geometry_msgs::msg::Point p;
      p.x = point.first; p.y = point.second; p.z = 0.08;
      path_marker.points.push_back(p);
    }
    markers.markers.push_back(path_marker);
    int id = 10;
    for (const auto & obstacle : planning_obstacles()) {
      auto marker = make_marker(id++, visualization_msgs::msg::Marker::CYLINDER,
                                obstacle.x, obstacle.y, 0.45,
                                obstacle.radius * 2.0, 0.9, 0.15, 0.1);
      marker.scale.z = 0.9;
      markers.markers.push_back(marker);
      auto safety = make_marker(id++, visualization_msgs::msg::Marker::CYLINDER,
                                obstacle.x, obstacle.y, 0.02,
                                2.0 * (obstacle.radius + robot_radius_),
                                1.0, 0.35, 0.05);
      safety.scale.z = 0.02;
      safety.color.a = 0.25;
      markers.markers.push_back(safety);
    }
    int sensed_id = 100;
    for (const auto & obstacle : obstacles()) {
      auto marker = make_marker(sensed_id++,
                                visualization_msgs::msg::Marker::SPHERE,
                                obstacle.x, obstacle.y, 0.16, 0.10,
                                1.0, 0.75, 0.05);
      marker.color.a = 0.85;
      markers.markers.push_back(marker);
    }
    auto trajectory = make_marker(2, visualization_msgs::msg::Marker::LINE_STRIP,
                                  0.0, 0.0, 0.22, 0.09, 0.2, 0.6, 1.0);
    trajectory.points.clear();
    double x = pose_.x, y = pose_.y, yaw = pose_.yaw;
    for (int step = 0; step < 15; ++step) {
      x += velocity * std::cos(yaw) * 0.1;
      y += velocity * std::sin(yaw) * 0.1;
      yaw += angular_velocity * 0.1;
      geometry_msgs::msg::Point p;
      p.x = x; p.y = y; p.z = 0.12;
      trajectory.points.push_back(p);
    }
    markers.markers.push_back(trajectory);
    auto robot = make_marker(5, visualization_msgs::msg::Marker::CYLINDER,
                             pose_.x, pose_.y, 0.04, 0.58, 0.2, 0.7, 1.0);
    robot.scale.z = 0.05;
    robot.color.a = 0.35;
    markers.markers.push_back(robot);
    auto heading = make_marker(6, visualization_msgs::msg::Marker::ARROW,
                               pose_.x, pose_.y, 0.28, 0.08, 0.2, 0.7, 1.0);
    heading.points.clear();
    geometry_msgs::msg::Point start, end;
    start.x = pose_.x; start.y = pose_.y; start.z = 0.28;
    end.x = pose_.x + 0.55 * std::cos(pose_.yaw);
    end.y = pose_.y + 0.55 * std::sin(pose_.yaw); end.z = 0.28;
    heading.points = {start, end};
    heading.scale.x = 0.08; heading.scale.y = 0.14; heading.scale.z = 0.14;
    markers.markers.push_back(heading);
    marker_pub_->publish(markers);
  }
  void control() {
    if (!have_odom_) return;
    publish_map();
    if (!have_scan_) {
      publish_debug({}, pose_.x, pose_.y, 0.0, 0.0);
      return;
    }
    if (!has_goal_) {
      cmd_pub_->publish(geometry_msgs::msg::Twist{});
      publish_debug({}, pose_.x, pose_.y, 0.0, 0.0);
      return;
    }
    const auto sensed_obstacles = obstacles();
    const auto path = astar(sensed_obstacles);
    nav_msgs::msg::Path path_msg; path_msg.header.frame_id = "odom";
    path_msg.header.stamp = now();
    for (const auto & point : path) {
      geometry_msgs::msg::PoseStamped pose;
      pose.header = path_msg.header; pose.pose.position.x = point.first;
      pose.pose.position.y = point.second; pose.pose.orientation.w = 1.0;
      path_msg.poses.push_back(pose);
    }
    path_pub_->publish(path_msg);
    geometry_msgs::msg::Twist command;
    if (path.empty()) {
      last_linear_velocity_ = 0.0;
      last_angular_velocity_ = 0.0;
      cmd_pub_->publish(command);
      RCLCPP_WARN_THROTTLE(
        get_logger(), *get_clock(), 5000,
        "Az A* nem talalt elerheto utvonalat; a robot megall.");
      publish_debug({}, goal_x_, goal_y_, 0.0, 0.0);
      return;
    }
    if (distance(pose_.x, pose_.y, goal_x_, goal_y_) < 0.3) {
      last_linear_velocity_ = 0.0;
      last_angular_velocity_ = 0.0;
      cmd_pub_->publish(command);
      return;
    }
    const double boundary_margin = robot_radius_ + safety_margin_;
    if (pose_.x < map_origin_x_ + boundary_margin ||
        pose_.x > map_origin_x_ + map_size_ - boundary_margin ||
        pose_.y < map_origin_y_ + boundary_margin ||
        pose_.y > map_origin_y_ + map_height_ - boundary_margin) {
      last_linear_velocity_ = 0.0;
      last_angular_velocity_ = 0.0;
      cmd_pub_->publish(command);
      RCLCPP_WARN_THROTTLE(
        get_logger(), *get_clock(), 5000,
        "A robot a palya biztonsagi hataran kivul van; sebesseg nullazva.");
      publish_debug(path, pose_.x, pose_.y, 0.0, 0.0);
      return;
    }
    double target_x = goal_x_, target_y = goal_y_;
    for (const auto & point : path)
      if (distance(pose_.x, pose_.y, point.first, point.second) > 0.5) {
        target_x = point.first; target_y = point.second; break;
      }
    const double target_heading = std::atan2(target_y - pose_.y, target_x - pose_.x);
    const double heading_error = angle_error(target_heading - pose_.yaw);
    if (std::abs(heading_error) > 0.6) {
      last_linear_velocity_ = 0.0;
      last_angular_velocity_ = 0.0;
      wheel_left_ = 0.0;
      wheel_right_ = 0.0;
      command.angular.z = std::clamp(
        heading_error, -max_angular_velocity_, max_angular_velocity_);
      publish_debug(path, target_x, target_y, 0.0, command.angular.z);
      cmd_pub_->publish(command);
      return;
    }
    const auto velocity = dwa(target_x, target_y, sensed_obstacles);
    RCLCPP_INFO_THROTTLE(
      get_logger(), *get_clock(), 2000,
      "Frontier vezerles: cel=(%.2f, %.2f), waypoint=(%.2f, %.2f), waypoint_tav=%.2f, ut=%zu pont, cmd=(%.2f, %.2f)",
      goal_x_, goal_y_, target_x, target_y,
      distance(pose_.x, pose_.y, target_x, target_y), path.size(),
      velocity.first, velocity.second);
    command.linear.x = std::clamp(velocity.first, -max_linear_velocity_, max_linear_velocity_);
    command.angular.z = std::clamp(velocity.second, -max_angular_velocity_, max_angular_velocity_);
    publish_debug(path, target_x, target_y, command.linear.x, command.angular.z);
    cmd_pub_->publish(command);
  }

  std::string cmd_topic_, odom_topic_, scan_topic_, goal_topic_, path_topic_;
  double goal_x_, goal_y_, map_size_, map_height_, map_origin_x_, map_origin_y_;
  double initial_pose_x_, initial_pose_y_;
  double resolution_, robot_radius_;
  double max_linear_velocity_, max_angular_velocity_;
  std::vector<double> known_obstacle_x_, known_obstacle_y_, known_obstacle_radius_;
  Pose pose_; sensor_msgs::msg::LaserScan::ConstSharedPtr scan_;
  bool have_odom_{false}, have_scan_{false}, has_goal_{false};
  double wheel_radius_{0.033}, wheel_base_{0.08}, wheel_max_{15.0};
  double wheel_resolution_{1.0}, acceleration_limit_{2.0};
  double predict_time_{3.0}, safety_margin_{0.15};
  double alpha_{5.0}, beta_{2.0}, gamma_{3.0}, dt_{0.1};
  double wheel_left_{0.0}, wheel_right_{0.0};
  double last_linear_velocity_{0.0}, last_angular_velocity_{0.0};
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr cmd_pub_;
  rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr path_pub_;
  rclcpp::Publisher<nav_msgs::msg::OccupancyGrid>::SharedPtr map_pub_;
  rclcpp::Publisher<visualization_msgs::msg::MarkerArray>::SharedPtr marker_pub_;
  std::unique_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster_;
  rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr odom_sub_;
  rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr scan_sub_;
  rclcpp::Subscription<geometry_msgs::msg::PoseStamped>::SharedPtr goal_sub_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char ** argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<AStarDwaNode>());
  rclcpp::shutdown();
  return 0;
}
```

### codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/dwa_gazebo_sim/__init__.py

```python
```

### codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/dwa_gazebo_sim/astar.py

```python
"""Grid-based A* planner."""

import heapq
import math


class Grid:
    def __init__(self, width, height, resolution, origin_x, origin_y):
        self.width, self.height = width, height
        self.resolution = resolution
        self.origin_x, self.origin_y = origin_x, origin_y
        self.cells = [[False] * width for _ in range(height)]

    def in_bounds(self, row, column):
        return 0 <= row < self.height and 0 <= column < self.width

    def free(self, row, column):
        return self.in_bounds(row, column) and not self.cells[row][column]

    def world_to_grid(self, x, y):
        return (math.floor((y - self.origin_y) / self.resolution),
                math.floor((x - self.origin_x) / self.resolution))

    def grid_to_world(self, row, column):
        return (self.origin_x + (column + 0.5) * self.resolution,
                self.origin_y + (row + 0.5) * self.resolution)

    def add_obstacle(self, x, y, radius):
        center = self.world_to_grid(x, y)
        cells = math.ceil(radius / self.resolution)
        for row in range(center[0] - cells, center[0] + cells + 1):
            for column in range(center[1] - cells, center[1] + cells + 1):
                if self.in_bounds(row, column):
                    cx, cy = self.grid_to_world(row, column)
                    if math.hypot(cx - x, cy - y) <= radius + self.resolution:
                        self.cells[row][column] = True


def astar(grid, start, goal, diagonal=True):
    if not grid.free(*start) or not grid.free(*goal):
        return []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    if diagonal:
        directions += [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    def heuristic(cell):
        return math.hypot(goal[0] - cell[0], goal[1] - cell[1])

    queue = [(heuristic(start), 0.0, start)]
    parents, costs = {}, {start: 0.0}
    while queue:
        _, current_cost, current = heapq.heappop(queue)
        if current_cost > costs[current]:
            continue
        if current == goal:
            path = [current]
            while current in parents:
                current = parents[current]
                path.append(current)
            return list(reversed(path))
        for dr, dc in directions:
            neighbor = current[0] + dr, current[1] + dc
            if not grid.free(*neighbor):
                continue
            if dr and dc and (not grid.free(current[0] + dr, current[1])
                              or not grid.free(current[0], current[1] + dc)):
                continue
            cost = current_cost + (math.sqrt(2) if dr and dc else 1.0)
            if cost < costs.get(neighbor, math.inf):
                costs[neighbor] = cost
                parents[neighbor] = current
                heapq.heappush(queue, (cost + heuristic(neighbor), cost, neighbor))
    return []
```

### codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/dwa_gazebo_sim/dwa.py

```python
"""Differential-drive Dynamic Window Approach controller."""

import math


def _angle(value):
    return math.atan2(math.sin(value), math.cos(value))


def choose_velocity(state, goal, obstacles, robot_radius):
    best = None
    for velocity in (0.0, 0.08, 0.16, 0.24, 0.32, 0.4):
        for angular_velocity in (-1.2, -0.8, -0.4, 0.0, 0.4, 0.8, 1.2):
            x, y, yaw = state
            safe = True
            for _ in range(15):
                x += velocity * math.cos(yaw) * 0.1
                y += velocity * math.sin(yaw) * 0.1
                yaw += angular_velocity * 0.1
                if any(math.hypot(x - ox, y - oy) < robot_radius + radius
                       for ox, oy, radius in obstacles):
                    safe = False
                    break
            if not safe:
                continue
            heading = math.atan2(goal[1] - y, goal[0] - x)
            score = (-math.hypot(goal[0] - x, goal[1] - y)
                     - 0.25 * abs(_angle(heading - yaw)) + 0.15 * velocity)
            if best is None or score > best[0]:
                best = score, velocity, angular_velocity
    return (best[1], best[2]) if best else (0.0, 0.0)
```

### codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/dwa_gazebo_sim/dwa_node.py

```python
import math

import rclpy
from geometry_msgs.msg import PoseStamped, Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


def yaw_from_quaternion(q):
    return math.atan2(
        2.0 * (q.w * q.z + q.x * q.y),
        1.0 - 2.0 * (q.y * q.y + q.z * q.z),
    )


class DwaNode(Node):
    def __init__(self):
        super().__init__("dwa_node")
        self.declare_parameter("goal_x", 7.0)
        self.declare_parameter("goal_y", 5.0)
        self.declare_parameter("goal_tolerance", 0.25)
        self.declare_parameter("simulation_time", 1.5)
        self.declare_parameter("robot_radius", 0.28)

        self.cmd_pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.create_subscription(Odometry, "/odom", self.odom_callback, 10)
        self.create_subscription(LaserScan, "/scan", self.scan_callback, 10)
        self.create_subscription(PoseStamped, "/goal_pose", self.goal_callback, 10)
        self.create_timer(0.1, self.control_callback)

        self.x = self.y = self.yaw = 0.0
        self.goal_x = float(self.get_parameter("goal_x").value)
        self.goal_y = float(self.get_parameter("goal_y").value)
        self.obstacles = []
        self.have_odom = False
        self.have_scan = False
        self.get_logger().info(
            f"DWA elindult, cel: ({self.goal_x:.2f}, {self.goal_y:.2f})"
        )

    def odom_callback(self, msg):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        self.yaw = yaw_from_quaternion(msg.pose.pose.orientation)
        self.have_odom = True

    def goal_callback(self, msg):
        self.goal_x = msg.pose.position.x
        self.goal_y = msg.pose.position.y
        self.get_logger().info(f"Uj cel: ({self.goal_x:.2f}, {self.goal_y:.2f})")

    def scan_callback(self, msg):
        self.obstacles = []
        for index, distance in enumerate(msg.ranges):
            if math.isfinite(distance) and msg.range_min <= distance <= msg.range_max:
                angle = msg.angle_min + index * msg.angle_increment
                self.obstacles.append(
                    (self.x + distance * math.cos(self.yaw + angle),
                     self.y + distance * math.sin(self.yaw + angle))
                )
        self.have_scan = True

    def rollout(self, velocity, angular_velocity, horizon):
        x, y, yaw = self.x, self.y, self.yaw
        step = 0.1
        for _ in range(max(1, int(horizon / step))):
            x += velocity * math.cos(yaw) * step
            y += velocity * math.sin(yaw) * step
            yaw += angular_velocity * step
            if any(
                math.hypot(x - ox, y - oy)
                < float(self.get_parameter("robot_radius").value)
                for ox, oy in self.obstacles
            ):
                return None
        return x, y, yaw

    def control_callback(self):
        if not self.have_odom or not self.have_scan:
            return
        distance = math.hypot(self.goal_x - self.x, self.goal_y - self.y)
        if distance <= float(self.get_parameter("goal_tolerance").value):
            self.cmd_pub.publish(Twist())
            return

        horizon = float(self.get_parameter("simulation_time").value)
        best = None
        for velocity in (0.0, 0.1, 0.2, 0.3, 0.4):
            for angular_velocity in (
                -1.0, -0.75, -0.5, -0.25, 0.0, 0.25, 0.5, 0.75, 1.0
            ):
                end = self.rollout(velocity, angular_velocity, horizon)
                if end is None:
                    continue
                end_x, end_y, end_yaw = end
                goal_heading = math.atan2(self.goal_y - end_y, self.goal_x - end_x)
                heading_error = abs(
                    math.atan2(math.sin(goal_heading - end_yaw),
                               math.cos(goal_heading - end_yaw))
                )
                score = (
                    -math.hypot(self.goal_x - end_x, self.goal_y - end_y)
                    - 0.2 * heading_error
                    + 0.1 * velocity
                )
                if best is None or score > best[0]:
                    best = score, velocity, angular_velocity

        command = Twist()
        if best is not None:
            command.linear.x = best[1]
            command.angular.z = best[2]
        self.cmd_pub.publish(command)


def main(args=None):
    rclpy.init(args=args)
    node = DwaNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

### codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/dwa_gazebo_sim/moving_obstacle_node.py

```python
import rclpy
from geometry_msgs.msg import Pose
from rclpy.node import Node
from ros_gz_interfaces.srv import SetEntityPose


class MovingObstacle(Node):
    def __init__(self):
        super().__init__("moving_obstacle")
        self.client = self.create_client(
            SetEntityPose, "/world/dwa_world/set_pose"
        )
        self.obstacles = [
            ("moving_obstacle_1", 2.4, 0.4, 0.0, 0.20),
            ("moving_obstacle_2", 6.8, 2.1, -0.25, 0.0),
        ]
        self.time = 0.0
        self.obstacle_index = 0
        self.request_in_flight = False
        self.service_wait_logged = False
        self.timer = self.create_timer(0.10, self.update)

    def update(self):
        dt = 0.10
        self.time += dt
        if not self.client.service_is_ready():
            if not self.service_wait_logged:
                self.get_logger().warning(
                    "A Gazebo set_pose szolgaltatas meg nem erheto el."
                )
                self.service_wait_logged = True
            return
        self.service_wait_logged = False
        if self.request_in_flight:
            return

        self.request_in_flight = True
        name, x, y, vx, vy = self.obstacles[self.obstacle_index]
        request = SetEntityPose.Request()
        request.entity.name = name
        request.entity.type = request.entity.MODEL
        request.pose = Pose()
        request.pose.position.x = x + vx * self.time
        request.pose.position.y = y + vy * self.time
        request.pose.position.z = 0.45
        request.pose.orientation.w = 1.0
        future = self.client.call_async(request)
        future.add_done_callback(self._handle_pose_response)

    def _handle_pose_response(self, future):
        try:
            response = future.result()
        except Exception as error:
            self.get_logger().warning(f"A Gazebo poziciofrissitese sikertelen: {error}")
        else:
            if not response.success:
                self.get_logger().warning(
                    "A Gazebo nem fogadta el a mozgĂł akadĂˇly pozĂ­ciĂłfrissĂ­tĂ©sĂ©t."
                )
        self.obstacle_index = (self.obstacle_index + 1) % len(self.obstacles)
        self.request_in_flight = False


def main(args=None):
    rclpy.init(args=args)
    node = MovingObstacle()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
```

### codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/dwa_gazebo_sim/planner_node.py

```python
import math

import rclpy
from geometry_msgs.msg import PoseStamped, Twist
from nav_msgs.msg import Odometry, Path
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

from .astar import Grid, astar
from .dwa import choose_velocity


class AStarDwaNode(Node):
    def __init__(self):
        super().__init__("astar_dwa_planner")
        self.declare_parameter("goal_x", 7.0)
        self.declare_parameter("goal_y", 5.0)
        self.declare_parameter("map_size", 12.0)
        self.declare_parameter("resolution", 0.2)
        self.declare_parameter("robot_radius", 0.28)
        self.goal = (float(self.get_parameter("goal_x").value),
                     float(self.get_parameter("goal_y").value))
        self.pose, self.scan, self.path = None, None, []
        self.cmd_pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.path_pub = self.create_publisher(Path, "/astar_path", 10)
        self.create_subscription(Odometry, "/odom", self.odom_callback, 10)
        self.create_subscription(LaserScan, "/scan", self.scan_callback, 10)
        self.create_subscription(PoseStamped, "/goal_pose", self.goal_callback, 10)
        self.create_timer(0.25, self.plan_and_control)
        self.get_logger().info("A* -> DWA planner started")

    def odom_callback(self, message):
        q = message.pose.pose.orientation
        yaw = math.atan2(2 * (q.w * q.z + q.x * q.y),
                         1 - 2 * (q.y * q.y + q.z * q.z))
        self.pose = (message.pose.pose.position.x, message.pose.pose.position.y, yaw)

    def scan_callback(self, message):
        self.scan = message

    def goal_callback(self, message):
        self.goal = (message.pose.position.x, message.pose.position.y)
        self.path = []

    def obstacles(self):
        result = []
        for index, distance in enumerate(self.scan.ranges):
            if math.isfinite(distance) and self.scan.range_min <= distance <= self.scan.range_max:
                angle = self.pose[2] + self.scan.angle_min + index * self.scan.angle_increment
                result.append((self.pose[0] + distance * math.cos(angle),
                               self.pose[1] + distance * math.sin(angle), 0.08))
        return result

    def build_plan(self):
        size = float(self.get_parameter("map_size").value)
        resolution = float(self.get_parameter("resolution").value)
        origin = self.pose[0] - size / 2, self.pose[1] - size / 2
        width = max(3, math.ceil(size / resolution))
        grid = Grid(width, width, resolution, origin[0], origin[1])
        radius = float(self.get_parameter("robot_radius").value)
        for x, y, _ in self.obstacles():
            grid.add_obstacle(x, y, radius)
        path = astar(grid, grid.world_to_grid(self.pose[0], self.pose[1]),
                     grid.world_to_grid(*self.goal), diagonal=True)
        return [grid.grid_to_world(*cell) for cell in path]

    def publish_path(self):
        message = Path()
        message.header.frame_id = "odom"
        message.header.stamp = self.get_clock().now().to_msg()
        for x, y in self.path:
            pose = PoseStamped()
            pose.header = message.header
            pose.pose.position.x, pose.pose.position.y = x, y
            pose.pose.orientation.w = 1.0
            message.poses.append(pose)
        self.path_pub.publish(message)

    def plan_and_control(self):
        if self.pose is None or self.scan is None:
            return
        self.path = self.build_plan()
        self.publish_path()
        if math.hypot(self.goal[0] - self.pose[0], self.goal[1] - self.pose[1]) < 0.3:
            self.cmd_pub.publish(Twist())
            return
        waypoint = self.goal
        for point in self.path:
            if math.hypot(point[0] - self.pose[0], point[1] - self.pose[1]) > 0.5:
                waypoint = point
                break
        velocity, angular_velocity = choose_velocity(
            self.pose, waypoint, self.obstacles(),
            float(self.get_parameter("robot_radius").value))
        command = Twist()
        command.linear.x, command.angular.z = velocity, angular_velocity
        self.cmd_pub.publish(command)


def main(args=None):
    rclpy.init(args=args)
    node = AStarDwaNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

### codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/launch/bridge_and_controller.launch.py

```python
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
import os


def generate_launch_description():
    controller_share = get_package_share_directory("astar_dwa_controller")
    return LaunchDescription([
        Node(
            package="ros_gz_bridge",
            executable="parameter_bridge",
            arguments=[
                "/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist",
                "/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry",
                "/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan",
                "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
                "/world/dwa_world/set_pose@ros_gz_interfaces/srv/SetEntityPose",
            ],
            parameters=[{"use_sim_time": True}],
        ),
        Node(
            package="astar_dwa_controller",
            executable="astar_dwa_node",
            parameters=[
                os.path.join(controller_share, "config", "rosbot.yaml"),
                {"use_sim_time": True},
            ],
        ),
        Node(
            package="dwa_gazebo_sim",
            executable="moving_obstacle_node",
            parameters=[{"use_sim_time": True}],
        ),
    ])
```

### codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/launch/simulation.launch.py

```python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    package_share = get_package_share_directory("dwa_gazebo_sim")
    turtlebot_share = get_package_share_directory("turtlebot3_gazebo")
    model_path = os.path.join(turtlebot_share, "models")
    world_path = os.path.join(package_share, "worlds", "dwa_world.sdf")
    gui = LaunchConfiguration("gui")
    verbose = LaunchConfiguration("verbose")
    qt_platform = LaunchConfiguration("qt_platform")
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("ros_gz_sim"),
                         "launch", "gz_sim.launch.py")
        ),
        launch_arguments={
            # gz_sim.launch.py tokenizes this argument string; quote the path
            # because the workspace may be located under a Windows user name
            # containing spaces.
            "gz_args": ['"' + world_path + '" -r -v ', verbose, ' ', gui],
        }.items(),
    )
    bridge = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(package_share, "launch", "bridge_and_controller.launch.py")
        ),
        launch_arguments={}.items(),
    )
    return LaunchDescription([
        DeclareLaunchArgument(
            "gui",
            default_value="-g",
            description="Gazebo mod: -g GUI-val, -s szerver modban",
        ),
        DeclareLaunchArgument(
            "verbose",
            default_value="1",
            description="Gazebo naplĂłzĂˇsi szintje (0-4)",
        ),
        DeclareLaunchArgument(
            "qt_platform",
            default_value="xcb",
            description="Qt platform: xcb WSLg/X11-hez, wayland alternatĂ­vakĂ©nt",
        ),
        SetEnvironmentVariable("GZ_SIM_RESOURCE_PATH", model_path),
        SetEnvironmentVariable("QT_QPA_PLATFORM", qt_platform),
        SetEnvironmentVariable("QT_X11_NO_MITSHM", "1"),
        SetEnvironmentVariable("ROS_AUTOMATIC_DISCOVERY_RANGE", "LOCALHOST"),
        gazebo,
        bridge,
    ])
```

### codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/launch/visualization.launch.py

```python
from launch import LaunchDescription
from launch.actions import SetEnvironmentVariable
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    rviz_config = os.path.join(
        get_package_share_directory("astar_dwa_controller"),
        "rviz",
        "astar_dwa.rviz",
    )
    return LaunchDescription([
        SetEnvironmentVariable("ROS_AUTOMATIC_DISCOVERY_RANGE", "LOCALHOST"),
        SetEnvironmentVariable("QT_QPA_PLATFORM", "xcb"),
        SetEnvironmentVariable("QT_X11_NO_MITSHM", "1"),
        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            output="screen",
            arguments=["-d", rviz_config, "-f", "odom"],
        )
    ])
```

### codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/package.xml

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>dwa_gazebo_sim</name>
  <version>0.1.0</version>
  <description>Gazebo vilĂˇg Ă©s ROS-Gazebo bridge az A* + DWA vezĂ©rlĹ‘hĂ¶z.</description>
  <maintainer email="rumdaniel@todo.todo">rumdaniel</maintainer>
  <license>MIT</license>

  <depend>rclpy</depend>
  <depend>geometry_msgs</depend>
  <depend>nav_msgs</depend>
  <depend>sensor_msgs</depend>
  <depend>ros_gz_interfaces</depend>
  <depend>ros_gz_bridge</depend>
  <depend>ros_gz_sim</depend>
  <exec_depend>turtlebot3_gazebo</exec_depend>
  <exec_depend>astar_dwa_controller</exec_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
```

### codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/setup.py

```python
from glob import glob
import os
from setuptools import find_packages, setup

package_name = "dwa_gazebo_sim"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.py")),
        (os.path.join("share", package_name, "worlds"), glob("worlds/*.sdf")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    entry_points={
        "console_scripts": [
            "planner_node = dwa_gazebo_sim.planner_node:main",
            "moving_obstacle_node = dwa_gazebo_sim.moving_obstacle_node:main"
        ],
    },
)
```

### codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/worlds/dwa_world.sdf

```xml
<?xml version="1.0"?>
<sdf version="1.8">
  <world name="dwa_world">
    <physics name="default_physics" type="ignored">
      <max_step_size>0.001</max_step_size>
      <real_time_update_rate>1000</real_time_update_rate>
      <real_time_factor>1</real_time_factor>
    </physics>
    <plugin filename="gz-sim-physics-system" name="gz::sim::systems::Physics"/>
    <plugin filename="gz-sim-sensors-system" name="gz::sim::systems::Sensors">
      <render_engine>ogre2</render_engine>
    </plugin>
    <plugin filename="gz-sim-scene-broadcaster-system" name="gz::sim::systems::SceneBroadcaster"/>
    <plugin filename="gz-sim-user-commands-system" name="gz::sim::systems::UserCommands"/>
    <light type="directional" name="sun">
      <pose>0 0 10 0 0 0</pose>
      <direction>-0.5 0.1 -0.9</direction>
    </light>
    <model name="ground_plane">
      <static>true</static>
      <link name="link">
        <collision name="collision"><geometry><plane><normal>0 0 1</normal></plane></geometry></collision>
        <visual name="visual"><geometry><plane><normal>0 0 1</normal></plane></geometry>
          <material><ambient>0.16 0.18 0.22 1</ambient><diffuse>0.22 0.25 0.30 1</diffuse></material>
        </visual>
      </link>
    </model>
    <model name="boundary_bottom">
      <static>true</static><pose>4 -0.10 0.5 0 0 0</pose>
      <link name="link"><collision name="collision"><geometry><box><size>8.2 0.2 1</size></box></geometry></collision>
        <visual name="visual"><geometry><box><size>8.2 0.2 1</size></box></geometry>
          <material><ambient>0.15 0.15 0.18 1</ambient><diffuse>0.15 0.15 0.18 1</diffuse></material>
        </visual></link>
    </model>
    <model name="boundary_top">
      <static>true</static><pose>4 5.10 0.5 0 0 0</pose>
      <link name="link"><collision name="collision"><geometry><box><size>8.2 0.2 1</size></box></geometry></collision>
        <visual name="visual"><geometry><box><size>8.2 0.2 1</size></box></geometry>
          <material><ambient>0.15 0.15 0.18 1</ambient><diffuse>0.15 0.15 0.18 1</diffuse></material>
        </visual></link>
    </model>
    <model name="boundary_left">
      <static>true</static><pose>-0.10 2.5 0.5 0 0 0</pose>
      <link name="link"><collision name="collision"><geometry><box><size>0.2 5.2 1</size></box></geometry></collision>
        <visual name="visual"><geometry><box><size>0.2 5.2 1</size></box></geometry>
          <material><ambient>0.15 0.15 0.18 1</ambient><diffuse>0.15 0.15 0.18 1</diffuse></material>
        </visual></link>
    </model>
    <model name="boundary_right">
      <static>true</static><pose>8.10 2.5 0.5 0 0 0</pose>
      <link name="link"><collision name="collision"><geometry><box><size>0.2 5.2 1</size></box></geometry></collision>
        <visual name="visual"><geometry><box><size>0.2 5.2 1</size></box></geometry>
          <material><ambient>0.15 0.15 0.18 1</ambient><diffuse>0.15 0.15 0.18 1</diffuse></material>
        </visual></link>
    </model>
    <model name="obstacle_1">
      <static>true</static><pose>2.1 0.9 0.5 0 0 0</pose>
      <link name="link"><collision name="collision"><geometry><box><size>0.2 0.8 1</size></box></geometry></collision>
        <visual name="visual"><geometry><box><size>0.2 0.8 1</size></box></geometry>
          <material><ambient>0.8 0.1 0.1 1</ambient><diffuse>0.8 0.1 0.1 1</diffuse></material>
        </visual></link>
    </model>
    <model name="obstacle_2">
      <static>true</static><pose>2.1 3.1 0.5 0 0 0</pose>
      <link name="link"><collision name="collision"><geometry><box><size>0.2 0.8 1</size></box></geometry></collision>
        <visual name="visual"><geometry><box><size>0.2 0.8 1</size></box></geometry>
          <material><ambient>0.9 0.4 0.05 1</ambient><diffuse>0.9 0.4 0.05 1</diffuse></material>
        </visual></link>
    </model>
    <model name="obstacle_3">
      <static>true</static><pose>3.2 2.5 0.5 0 0 0</pose>
      <link name="link"><collision name="collision"><geometry><box><size>1.6 0.2 1</size></box></geometry></collision>
        <visual name="visual"><geometry><box><size>1.6 0.2 1</size></box></geometry>
          <material><ambient>0.55 0.1 0.75 1</ambient><diffuse>0.55 0.1 0.75 1</diffuse></material>
        </visual></link>
    </model>
    <model name="obstacle_4">
      <static>true</static><pose>5.3 2.5 0.5 0 0 0</pose>
      <link name="link"><collision name="collision"><geometry><box><size>0.6 0.2 1</size></box></geometry></collision>
        <visual name="visual"><geometry><box><size>0.6 0.2 1</size></box></geometry>
          <material><ambient>0.95 0.75 0.05 1</ambient><diffuse>0.95 0.75 0.05 1</diffuse></material>
        </visual></link>
    </model>
    <model name="moving_obstacle_1">
      <static>false</static>
      <pose>2.4 0.4 0.45 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry><cylinder><radius>0.18</radius><length>0.9</length></cylinder></geometry>
        </collision>
        <visual name="visual">
          <geometry><cylinder><radius>0.18</radius><length>0.9</length></cylinder></geometry>
          <material><ambient>0.1 0.4 0.9 1</ambient><diffuse>0.1 0.4 0.9 1</diffuse></material>
        </visual>
      </link>
    </model>
    <model name="moving_obstacle_2">
      <static>false</static>
      <pose>6.8 2.1 0.45 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry><cylinder><radius>0.18</radius><length>0.9</length></cylinder></geometry>
        </collision>
        <visual name="visual">
          <geometry><cylinder><radius>0.18</radius><length>0.9</length></cylinder></geometry>
          <material><ambient>0.1 0.8 0.4 1</ambient><diffuse>0.1 0.8 0.4 1</diffuse></material>
        </visual>
      </link>
    </model>
    <include>
      <uri>model://turtlebot3_waffle</uri>
      <name>turtlebot3_waffle</name>
      <pose>0.8 0.8 0.05 0 0 0</pose>
    </include>
  </world>
</sdf>
```

### codes_diploma/ROS2_FONTOS_NODE_TOPICOK.gv

```
digraph ROS2ImportantGraph {
    graph [
        label="ROS 2 A* + DWA - fontos node-ok Ă©s topicok"
        labelloc=t
        fontsize=22
        fontname="Arial Bold"
        rankdir=LR
        splines=ortho
        nodesep=0.45
        ranksep=0.8
        pad=0.25
        bgcolor="white"
    ]

    node [
        shape=box
        style="rounded,filled"
        fontname="Arial"
        fontsize=11
        margin="0.16,0.10"
        color="#475569"
        penwidth=1.5
    ]

    edge [
        fontname="Arial"
        fontsize=9
        color="#64748b"
        penwidth=1.2
        arrowsize=0.7
    ]

    gazebo [
        label="Gazebo Sim\nfizikai vilĂˇg + robot\n/clock, szenzorok"
        fillcolor="#fef3c7"
        color="#d97706"
    ]

    bridge [
        label="/ros_gz_bridge\nGazebo <-> ROS 2\nĂˇtalakĂ­tĂł"
        fillcolor="#dbeafe"
        color="#2563eb"
    ]

    controller [
        label="/astar_dwa_node\nA* globĂˇlis tervezĹ‘\nDWA lokĂˇlis vezĂ©rlĹ‘"
        fillcolor="#dcfce7"
        color="#15803d"
    ]

    moving [
        label="/moving_obstacle\nmozgĂł akadĂˇly\nidĹ‘zĂ­tett pozĂ­ciĂłfrissĂ­tĂ©s"
        fillcolor="#ffedd5"
        color="#c2410c"
    ]

    rviz [
        label="/rviz2\nRViz megjelenĂ­tĂ©s\nMap, Path, TF, LiDAR, Markers"
        fillcolor="#ede9fe"
        color="#7c3aed"
    ]

    goal [
        label="RViz 2D Goal Pose\nfelhasznĂˇlĂłi cĂ©l"
        shape=parallelogram
        fillcolor="#fce7f3"
        color="#db2777"
    ]

    clock [label="/clock\nszimulĂˇciĂłs idĹ‘", shape=note, fillcolor="#f1f5f9"]
    scan [label="/scan\nLaserScan", shape=note, fillcolor="#fef3c7", color="#d97706"]
    odom [label="/odom\nOdometry", shape=note, fillcolor="#fef3c7", color="#d97706"]
    cmd [label="/cmd_vel\nTwist", shape=note, fillcolor="#bfdbfe", color="#2563eb"]
    goal_topic [label="/goal_pose\nPoseStamped", shape=note, fillcolor="#fbcfe8", color="#db2777"]
    map [label="/astar_map\nOccupancyGrid", shape=note, fillcolor="#bbf7d0", color="#15803d"]
    path [label="/astar_path\nnav_msgs/Path", shape=note, fillcolor="#bbf7d0", color="#15803d"]
    markers [label="/astar_dwa_markers\nMarkerArray", shape=note, fillcolor="#bbf7d0", color="#15803d"]
    tf [label="/tf\nodom -> base_link\nbase_link -> base_scan", shape=note, fillcolor="#ddd6fe", color="#7c3aed"]

    gazebo -> clock [label="publishes"]
    gazebo -> scan [label="publishes"]
    gazebo -> odom [label="publishes"]
    cmd -> bridge [label="ROS -> Gazebo"]
    bridge -> scan [label="Gazebo -> ROS"]
    bridge -> odom [label="Gazebo -> ROS"]
    bridge -> clock [label="Gazebo -> ROS"]
    bridge -> cmd [label="forwards"]

    clock -> controller [label="subscribes"]
    scan -> controller [label="subscribes"]
    odom -> controller [label="subscribes"]
    goal_topic -> controller [label="subscribes"]
    goal -> goal_topic [label="publishes"]

    controller -> cmd [label="publishes"]
    controller -> map [label="publishes"]
    controller -> path [label="publishes"]
    controller -> markers [label="publishes"]
    controller -> tf [label="publishes"]

    map -> rviz [label="display"]
    path -> rviz [label="display"]
    scan -> rviz [label="display"]
    markers -> rviz [label="display"]
    tf -> rviz [label="display"]
    odom -> rviz [label="display"]

    clock -> moving [label="subscribes"]
    moving -> gazebo [label="SetEntityPose service"]
}
```

### codes_diploma/simulation.py

```python
"""A* + DWA szimulacio az onlabos palyamegjelenitessel es a palyak vegi fekezessel."""

import importlib.util
import math
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

import matplotlib

matplotlib.use("TkAgg")

from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle, Rectangle
import matplotlib.pyplot as plt

from codes_diploma.astar_project.astar_baseline import astar_search
from codes_diploma.astar_project.astar_variants import get_heuristic
from codes_diploma.astar_project.grid_map import GridMap
from codes_diploma.DWA import AdmissableVelocity, get_dist_on_trajectory
from codes_diploma.robot import Obstacle, robotconfig, robotstate, update


def load_planner_class():
    """Betolti a pluszjelet tartalmazo DWA+A.py modult."""
    file_path = Path(__file__).with_name("DWA+A.py")
    spec = importlib.util.spec_from_file_location("dwa_a_module", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.AStarDWAPlanner


def parse_cell(value):
    """Szoveges cellakoordinatat konvertal egesz parra."""
    row, column = (int(part.strip()) for part in value.split(","))
    return row, column


def create_scene(
    width=30,
    height=20,
    resolution=0.2,
    start_cell=(2, 2),
    goal_cell=(17, 27),
    inflation_radius=0.11,
):
    """Letrehozza az A* es DWA kozos terkepet es akadalyait."""
    grid_map = GridMap(width=width, height=height, resolution=resolution)
    vertical_column = min(10, width - 2)
    horizontal_row = min(12, height - 2)
    static_cells = []

    for row in range(2, max(2, height - 2)):
        if row not in range(7, 13):
            static_cells.append((row, vertical_column))
    for column in range(12, max(12, width - 2)):
        if column not in range(19, 25):
            static_cells.append((horizontal_row, column))

    for cell in static_cells:
        if grid_map.is_inside(*cell) and cell not in (start_cell, goal_cell):
            grid_map.add_obstacle(*cell)
    grid_map.inflate_obstacles(inflation_radius)

    start = grid_map.grid_to_world(*start_cell)
    goal = grid_map.grid_to_world(*goal_cell)
    state = robotstate(x=start[0], y=start[1], irany=0.0)
    static_obstacles = [
        Obstacle(*grid_map.grid_to_world(*cell), radius=0.12)
        for cell in static_cells
    ]
    dynamic_obstacles = [
        Obstacle(2.4, 0.4, radius=0.18, vx=0.0, vy=0.20),
        Obstacle(6.8, 2.1, radius=0.18, vx=-0.25, vy=0.0),
    ]
    return (
        grid_map,
        start_cell,
        goal_cell,
        start,
        goal,
        state,
        static_obstacles,
        dynamic_obstacles,
    )


def compute_onlab_trajectories(state, config, all_pairs, best_pair, obstacles):
    """Kiszamolja a josolt palyakat es azok vegen a fekezesi szakaszokat az onlab alapjan."""
    unsafe_paths = []
    unsafe_brakes = []

    safe_paths = []
    safe_brakes = []

    best_path = ([], [])
    best_brake = ([], [])

    predict_steps = max(1, int(round(config.predict_time / config.dt)))

    for v, w, w_L, w_R in all_pairs:
        # Csak elorehaladast vizsgalunk, ha a hatramenet tiltott
        if not getattr(config, "allow_reverse", False) and v < 0:
            continue

        is_best = False
        if best_pair is not None:
            if math.isclose(w_L, best_pair[2], abs_tol=1e-3) and math.isclose(
                w_R, best_pair[3], abs_tol=1e-3
            ):
                is_best = True

        is_safe = AdmissableVelocity(config, w_L, w_R, state, obstacles)
        dist_to_coll = get_dist_on_trajectory(state, config, w_L, w_R, obstacles)

        # 1. JĂłsolt szakasz (Trajectory rollout)
        ghost = robotstate(
            x=state.x, y=state.y, irany=state.irany, w_L=state.w_L, w_R=state.w_R
        )
        path_points = [(ghost.x, ghost.y)]
        for _ in range(predict_steps):
            update(ghost, config, w_L, w_R, config.dt)
            path_points.append((ghost.x, ghost.y))

        # 2. FĂ©kezĂ©si szakasz a jĂłsolt szakasz legvĂ©gĂ©tĹ‘l indĂ­tva (Ă¶nlabos kĂ©plet)
        t_stop = abs(v) / config.a_max if abs(v) > 0.0 else 0.0
        brake_robot = robotstate(
            x=ghost.x, y=ghost.y, irany=ghost.irany, w_L=w_L, w_R=w_R
        )
        brake_points = [(brake_robot.x, brake_robot.y)]
        brake_steps = (
            int(math.ceil(t_stop / config.dt)) if t_stop > 0.0 else 0
        )

        for step_idx in range(brake_steps):
            t = step_idx * config.dt
            factor = max(0.0, 1.0 - (t / t_stop)) if t_stop > 0.0 else 0.0
            update(brake_robot, config, w_L * factor, w_R * factor, config.dt)
            brake_points.append((brake_robot.x, brake_robot.y))

        # 3. SzĂ©tvĂˇlogatĂˇs
        if is_best:
            px, py = zip(*path_points)
            bx, by = zip(*brake_points)
            best_path = (list(px), list(py))
            best_brake = (list(bx), list(by))
        elif dist_to_coll < (abs(v) * config.predict_time) or not is_safe:
            unsafe_paths.append(path_points)
            unsafe_brakes.append(brake_points)
        else:
            safe_paths.append(path_points)
            safe_brakes.append(brake_points)

    return (
        unsafe_paths,
        unsafe_brakes,
        safe_paths,
        safe_brakes,
        best_path,
        best_brake,
    )


def create_simulation(
    width=30,
    height=20,
    resolution=0.2,
    start_cell=(2, 2),
    goal_cell=(17, 27),
    diagonal=True,
    heuristic_name="euclidean",
    inflation_radius=0.1,
    smooth=True,
    samples_per_curve=8,
    alpha=5.0,
    beta=2.0,
    gamma=3.0,
    waypoint_slowdown=False,
    show_original_astar=False,
    max_steps=600,
    auto_play=True,
    show=False,
):
    planner_class = load_planner_class()
    (
        grid_map,
        start_cell,
        goal_cell,
        start,
        goal,
        state,
        static_obstacles,
        dynamic_obstacles,
    ) = create_scene(
        width, height, resolution, start_cell, goal_cell, inflation_radius
    )
    heuristic = get_heuristic(heuristic_name)
    astar_result = astar_search(
        grid_map,
        start_cell,
        goal_cell,
        diagonal=diagonal,
        heuristic=heuristic,
        return_details=True,
    )
    if astar_result["path"] is None:
        raise RuntimeError("Az A* nem talalt utvonalat a beallitott terkepen.")

    config = robotconfig()
    config.Alfa = alpha
    config.Beta = beta
    config.Gamma = gamma
    config.enable_waypoint_slowdown = waypoint_slowdown
    planner = planner_class(grid_map, config=config, diagonal=diagonal)
    path = planner.plan_global(
        start,
        goal,
        heuristic=heuristic,
        smooth=smooth,
        samples_per_curve=samples_per_curve,
    )
    expanded_world = [
        grid_map.grid_to_world(*cell) for cell in astar_result["expanded_nodes"]
    ]
    path_world = list(path)
    planning_frames = max(1, len(expanded_world))
    movement_start = planning_frames + 1
    total_frames = movement_start + max_steps

    figure, (info_ax, map_ax) = plt.subplots(
        1, 2, figsize=(15, 8), gridspec_kw={"width_ratios": (1, 3)}
    )
    figure.subplots_adjust(bottom=0.13, right=0.82, wspace=0.08)
    info_ax.set_axis_off()
    info_ax.set_title("A* + DWA allapot")
    priority_text = info_ax.text(
        0.02, 0.95, "", va="top", family="monospace", fontsize=8
    )

    for row in range(grid_map.height + 1):
        map_ax.axhline(
            row * resolution,
            color="#78909c",
            linewidth=0.65,
            alpha=0.75,
            zorder=0,
        )
    for column in range(grid_map.width + 1):
        map_ax.axvline(
            column * resolution,
            color="#78909c",
            linewidth=0.65,
            alpha=0.75,
            zorder=0,
        )

    raw_obstacle_cells = set()
    vertical_column = min(10, width - 2)
    horizontal_row = min(12, height - 2)
    for row in range(2, max(2, height - 2)):
        if row not in range(7, 13):
            raw_obstacle_cells.add((row, vertical_column))
    for column in range(12, max(12, width - 2)):
        if column not in range(19, 25):
            raw_obstacle_cells.add((horizontal_row, column))

    inflation_rectangles = []
    for row in range(grid_map.height):
        for column in range(grid_map.width):
            if grid_map.grid[row][column] == 1:
                rect = Rectangle(
                    (column * resolution, row * resolution),
                    resolution,
                    resolution,
                    color="#455a64",
                    zorder=1,
                )
                map_ax.add_patch(rect)
                if (row, column) not in raw_obstacle_cells:
                    inflation_rectangles.append(rect)

    astar_world = list(planner.astar_path)
    astar_x, astar_y = zip(*astar_world)
    path_x, path_y = zip(*path_world)
    waypoint_x, waypoint_y = zip(*planner.waypoints)

    # 1. BĂ©zier Ăştvonal: zorder=4, de alpha=0.55-tel ĂˇttetszĹ‘, hogy ne takarja el az A*-ot
    map_ax.plot(
        path_x,
        path_y,
        "-",
        color="#2e7d32",
        linewidth=3.5,
        alpha=0.55,
        label="Bezier utvonal",
        zorder=4,
    )

# VĂ©kony, finom szaggatott vonal aprĂł csomĂłponti pontokkal a BĂ©zier felett
    (astar_line,) = map_ax.plot(
        astar_x,
        astar_y,
        linestyle="--",
        dashes=(3, 2),        # SĹ±rĹ±bb, rĂ¶videbb szaggatĂˇs a finomabb megjelenĂ©shez
        marker="o",
        markersize=2.0,       # AprĂł, finom pontok
        color="#0a22a7",      # Ă‰lĂ©nk narancs a jĂł kontrasztĂ©rt
        linewidth=1.0,        # VĂ©kony vonalvastagsĂˇg (korĂˇbbi 1.8 helyett)
        alpha=0.9,
        label="Eredeti A* racsutvonal",
        zorder=7,
    )
    astar_line.set_visible(show_original_astar)
    map_ax.scatter(
        waypoint_x,
        waypoint_y,
        s=14,
        color="#e53935",
        edgecolors="#bdef48",
        linewidths=0.5,
        label="Bezier DWA pontok",
        zorder=6,
    )
    explored = map_ax.scatter(
        [], [], s=18, color="#90caf9", alpha=0.45, label="A* vizsgalt cellak", zorder=3
    )
    current_cell = map_ax.scatter(
        [],
        [],
        s=110,
        color="#ff9800",
        edgecolors="#e65100",
        label="A* aktualis pont",
        zorder=5,
    )
    waypoint = map_ax.scatter(
        [],
        [],
        s=150,
        marker="*",
        color="#fdd835",
        edgecolors="#f57f17",
        label="DWA waypoint",
        zorder=7,
    )

    # Ă–sszes pĂˇlya Ă©s fĂ©kezĂ©si szakaszok az Ă¶nlabos megjelenĂ­tĂ©s szerint
    unsafe_collection = LineCollection(
        [],
        colors="red",
        linewidths=0.8,
        alpha=0.25,
        zorder=4,
        label="Nem biztonsagos palya (piros)",
    )
    map_ax.add_collection(unsafe_collection)

    safe_collection = LineCollection(
        [],
        colors="gray",
        linewidths=0.8,
        alpha=0.25,
        zorder=4,
        label="Biztonsagos palya (szurke)",
    )
    map_ax.add_collection(safe_collection)

    brakes_collection = LineCollection(
        [],
        colors="red",
        linewidths=0.8,
        alpha=0.35,
        zorder=4,
        label="Fekezesi szakasz (palya vegen)",
    )
    map_ax.add_collection(brakes_collection)

    (best_line,) = map_ax.plot(
        [],
        [],
        color="lime",
        linewidth=3.5,
        label="Valasztott legjobb (lime)",
        zorder=8,
    )
    (best_brake_line,) = map_ax.plot(
        [],
        [],
        color="red",
        linewidth=2.5,
        linestyle="--",
        label="Valasztott fekezese",
        zorder=9,
    )

    robot = Circle(
        start,
        config.rob_radius,
        fill=False,
        color="#1565c0",
        linewidth=2,
        label="Robot",
        zorder=10,
    )
    map_ax.add_patch(robot)
    goal_patch = Circle(
        goal,
        config.rob_radius * 0.6,
        fill=False,
        color="#2e7d32",
        linewidth=2,
        label="Cel",
        zorder=6,
    )
    map_ax.add_patch(goal_patch)
    (trail_line,) = map_ax.plot(
        [start[0]],
        [start[1]],
        color="#1565c0",
        linewidth=2,
        label="Robot nyoma",
        zorder=4,
    )
    status = map_ax.text(
        0.02,
        0.98,
        "A* tervezes",
        transform=map_ax.transAxes,
        va="top",
        zorder=11,
    )

    all_obstacles = static_obstacles + dynamic_obstacles
    obstacle_patches = [
        Circle(
            (obstacle.x, obstacle.y),
            obstacle.radius,
            color="#d32f2f",
            alpha=0.65,
            zorder=5,
        )
        for obstacle in all_obstacles
    ]
    for patch in obstacle_patches:
        map_ax.add_patch(patch)

    map_ax.set_xlim(0, width * resolution)
    map_ax.set_ylim(0, height * resolution)
    map_ax.set_aspect("equal")
    map_ax.set_xlabel("x [m]")
    map_ax.set_ylabel("y [m]")
    map_ax.set_title("A* racs, DWA palyak es a palyak vegi fekezes")
    map_ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), fontsize=8)

    trail_x = [state.x]
    trail_y = [state.y]
    last_movement_frame = -1
    last_result = None

    def priority_description(frame):
        if frame >= len(astar_result["search_steps"]):
            return "A* kesz\n\nDWA fazis\nmozgo akadalyak"
        step = astar_result["search_steps"][frame]
        return (
            f"A* lepes: {frame + 1}\n"
            f"aktualis: {step['current']}\n\n"
            f"prioritas\npozicio       f\n"
            + "\n".join(
                f"{item['position']!s:12s} {item['f']:6.2f}"
                for item in step.get("priority_queue", [])[:8]
            )
        )

    def advance_robot_one_step():
        nonlocal last_result
        for obstacle in dynamic_obstacles:
            obstacle.move(config.dt)
        last_result = planner.plan_local(state, all_obstacles)
        best_pair = (
            last_result["best_pair"] if last_result is not None else None
        )
        if best_pair is None:
            update(state, config, 0.0, 0.0, config.dt)
        else:
            update(state, config, best_pair[2], best_pair[3], config.dt)
        trail_x.append(state.x)
        trail_y.append(state.y)

    def update_frame(frame):
        nonlocal last_movement_frame
        if frame < planning_frames:
            explored.set_offsets(expanded_world[: frame + 1])
            current_cell.set_offsets([expanded_world[frame]])
            waypoint.set_offsets([[math.nan, math.nan]])
            priority_text.set_text(priority_description(frame))
            status.set_text(f"A* tervezes: {frame + 1}/{planning_frames}")
            return

        if frame == movement_start - 1:
            for rect in inflation_rectangles:
                rect.set_visible(False)
            explored.set_offsets(expanded_world)
            current_cell.set_offsets([[math.nan, math.nan]])
            priority_text.set_text(
                priority_description(len(astar_result["search_steps"]))
            )
            status.set_text("A* kesz - DWA mozgas indul")
            return

        movement_frame = min(frame - movement_start, max_steps - 1)
        while last_movement_frame < movement_frame:
            advance_robot_one_step()
            last_movement_frame += 1

        if last_result is not None:
            active_waypoint = last_result["waypoint"]
            target = last_result["target"]
            best_pair = last_result.get("best_pair", None)
            all_pairs = last_result.get("all_pairs", [])
            waypoint.set_offsets([active_waypoint])
        else:
            active_waypoint = None
            target = None
            best_pair = None
            all_pairs = []

        (
            unsafe_p,
            unsafe_b,
            safe_p,
            safe_b,
            best_p,
            best_b,
        ) = compute_onlab_trajectories(
            state, config, all_pairs, best_pair, all_obstacles
        )

        unsafe_collection.set_segments(unsafe_p)
        safe_collection.set_segments(safe_p)
        brakes_collection.set_segments(unsafe_b + safe_b)

        best_line.set_data(best_p[0], best_p[1])
        best_brake_line.set_data(best_b[0], best_b[1])

        trail_line.set_data(trail_x, trail_y)
        robot.center = (state.x, state.y)
        for patch, obstacle in zip(obstacle_patches, all_obstacles):
            patch.center = (obstacle.x, obstacle.y)

        priority_text.set_text(
            f"DWA allapot\n"
            f"robot: ({state.x:.2f}, {state.y:.2f})\n"
            f"sebesseg: {state.v:.2f} m/s\n"
            f"osszes palya: {len(all_pairs)} db\n"
            f"veszelyes (piros): {len(unsafe_p)} db\n"
            f"biztonsagos (szurke): {len(safe_p)} db\n"
            f"waypointok: {len(planner.waypoints)}\n"
            f"aktualis: {active_waypoint}\n"
            f"DWA cel: {target}"
        )
        status.set_text(
            "Cel elerve"
            if planner.reached_goal(state)
            else f"DWA mozgas: {movement_frame + 1}/{max_steps}"
        )

    animation = FuncAnimation(
        figure,
        update_frame,
        frames=total_frames,
        interval=80,
        repeat=False,
        blit=False,
    )
    figure._simulation_animation = animation
    if show:
        plt.show(block=True)
    return figure, animation


def run_simulation():
    """Elinditja a beallitasi ablakot."""
    window = tk.Tk()
    window.title("A* + DWA beallitasok")
    window.resizable(False, False)
    frame = ttk.Frame(window, padding=16)
    frame.grid()
    fields = {
        "width": ("Szelesseg cellaban", "30"),
        "height": ("Magassag cellaban", "20"),
        "resolution": ("Felbontas [m]", "0.2"),
        "start": ("Start (sor,oszlop)", "2,2"),
        "goal": ("Cel (sor,oszlop)", "17,27"),
        "inflation": ("Akadalyinflacio [m]", "0.11"),
        "alpha": ("Alfa - iranykovetes", "5"),
        "beta": ("Beta - akadalybiztonsag", "2"),
        "gamma": ("Gamma - sebesseg", "3"),
    }
    entries = {}
    for row, (name, (label, value)) in enumerate(fields.items()):
        ttk.Label(frame, text=label).grid(
            row=row, column=0, sticky="w", padx=(0, 12), pady=4
        )
        entry = ttk.Entry(frame, width=18)
        entry.insert(0, value)
        entry.grid(row=row, column=1, pady=4)
        entries[name] = entry

    diagonal = tk.BooleanVar(value=True)
    smooth = tk.BooleanVar(value=True)
    waypoint_slowdown = tk.BooleanVar(value=False)
    show_original_astar = tk.BooleanVar(value=False)
    heuristic = tk.StringVar(value="euclidean")

    tk.Checkbutton(frame, text="Atlos mozgas", variable=diagonal).grid(
        row=9, column=0, columnspan=2, sticky="w"
    )
    tk.Checkbutton(frame, text="Bezier utvonal simitasa", variable=smooth).grid(
        row=10, column=0, columnspan=2, sticky="w"
    )
    tk.Checkbutton(
        frame, text="Waypoint lassitas", variable=waypoint_slowdown
    ).grid(row=11, column=0, columnspan=2, sticky="w")
    tk.Checkbutton(
        frame, text="Eredeti A* utvonal", variable=show_original_astar
    ).grid(row=12, column=0, columnspan=2, sticky="w")
    tk.Label(frame, text="A* heurisztika").grid(
        row=13, column=0, sticky="w", pady=4
    )
    heuristic_box = ttk.Combobox(
        frame,
        textvariable=heuristic,
        values=("manhattan", "euclidean", "chebyshev", "octile"),
        state="readonly",
        width=16,
    )
    heuristic_box.grid(row=13, column=1, pady=4)

    def start():
        try:
            settings = {name: entry.get() for name, entry in entries.items()}
            width = int(settings["width"])
            height = int(settings["height"])
            resolution = float(settings["resolution"])
            inflation = float(settings["inflation"])
            alpha = float(settings["alpha"])
            beta = float(settings["beta"])
            gamma = float(settings["gamma"])
            start_cell = parse_cell(settings["start"])
            goal_cell = parse_cell(settings["goal"])
            if not (width > 2 and height > 2 and resolution > 0 and inflation >= 0):
                raise ValueError(
                    "A terkep merete es a felbontas legyen pozitiv."
                )
            if min(alpha, beta, gamma) < 0 or alpha + beta + gamma == 0:
                raise ValueError(
                    "A sullyok legyenek nem negativak, es legalabb egy legyen pozitiv."
                )
            if not (0 <= start_cell[0] < height and 0 <= start_cell[1] < width):
                raise ValueError("A start legyen a terkepen belul.")
            if not (0 <= goal_cell[0] < height and 0 <= goal_cell[1] < width):
                raise ValueError("A cel legyen a terkepen belul.")
            window.destroy()
            create_simulation(
                width,
                height,
                resolution,
                start_cell,
                goal_cell,
                diagonal.get(),
                heuristic.get(),
                inflation,
                smooth=smooth.get(),
                alpha=alpha,
                beta=beta,
                gamma=gamma,
                waypoint_slowdown=waypoint_slowdown.get(),
                show_original_astar=show_original_astar.get(),
                auto_play=True,
                show=True,
            )
        except (TypeError, ValueError, RuntimeError) as error:
            messagebox.showerror("Hibas beallitas", str(error), parent=window)

    tk.Button(frame, text="Szimulacio inditasa", command=start).grid(
        row=14, column=0, columnspan=2, sticky="ew", pady=(12, 0)
    )
    window.mainloop()


if __name__ == "__main__":
    run_simulation()
```

### codes_diploma/tudasbazis.MD

```markdown
# TudĂˇsbĂˇzis: KizĂˇrĂłlag A*-alapĂş ĂštvonaltervezĂ©s (DiszkrĂ©t Ă©s Folytonos / SBA*)

> **BĹ‘vĂ­tĂ©si FigyelmeztetĂ©s**: Ezt a tĂˇrat a jĂ¶vĹ‘ben tovĂˇbbi irodalmakkal, optimalizĂˇlĂˇsi eljĂˇrĂˇsokkal (pl. kinodinamikus korlĂˇtok, MPC, hibrid rĂˇcs-mintavĂ©teles mĂłdszerek) folyamatosan bĹ‘vĂ­teni fogjuk.
> **CĂ©l**: LLM (AI) Ăˇgens betanĂ­tĂˇsa Ă©s tiszta, DWA-mentes, *kizĂˇrĂłlag A*-alapĂş* (diszkrĂ©t optimalizĂˇlt A* + folytonos SBA*) mozgĂˇstervezĹ‘ kĂłd generĂˇlĂˇsĂˇhoz (C++20 / Python).

---

## 1. Modul: DiszkrĂ©t, TovĂˇbbfejlesztett A* (GlobĂˇlis / RĂˇcsalapĂş TervezĂ©s)
**ForrĂˇs**: Jin, M. & Wang, H. (2023) [cite: 2].
**AlkalmazĂˇsi kĂ¶rnyezet**: Ismert statikus globĂˇlis tĂ©rkĂ©p (raster map, pl. $30\times30$).

### 1.1. AlapozĂˇs Ă©s KĂ¶ltsĂ©gfĂĽggvĂ©ny
* HagyomĂˇnyos A* kĂ¶ltsĂ©gbecslĂ©s: $f(n) = g(n) + h(n)$ [cite: 2].
* $g(n)$ a Start ($S$) Ă©s aktuĂˇlis pont ($C$) kĂ¶zĂ¶tti tĂ©nyleges tĂˇvolsĂˇg [cite: 2].
* $h(n)$ heurisztikus becslĂ©s $C$-bĹ‘l a CĂ©lhoz ($T$) [cite: 2].
* Euklideszi tĂˇvolsĂˇg heurisztika: $h(n) = \sqrt{(x_n - x_g)^2 + (y_n - y_g)^2}$ [cite: 2].

### 1.2. Dinamikus Heurisztikus FĂĽggvĂ©ny
* A heurisztika dinamikusan sĂşlyozandĂł az aktuĂˇlis pozĂ­ciĂł tĂ©rbeli arĂˇnya szerint [cite: 2].
* KĂ©plet: $h(n)^* = \left(1 + \frac{l}{L}\right) * h(n)$, ahol $l$ a $C$-tĹ‘l $T$-ig, $L$ a $C$-tĹ‘l $S$-ig mĂ©rt tĂˇvolsĂˇg [cite: 2].
* Start kĂ¶zelĂ©ben $l/L$ nagy $\implies$ nagy sĂşly $\implies$ szĹ±kebb keresĂ©si terĂĽlet, gyorsabb keresĂ©s [cite: 2].
* CĂ©l kĂ¶zelĂ©ben kisebb szorzĂł $\implies$ tĂ¶bb keresĂ©si csomĂłpont $\implies$ optimĂˇlis Ăştvonal garancia [cite: 2].

### 1.3. 5-SzomszĂ©dsĂˇgĂş KeresĂ©s Ă©s SarokvĂˇgĂˇs-vĂ©delem
* 8-szomszĂ©dsĂˇg helyett 5-szomszĂ©dsĂˇg hasznĂˇlata a hatĂ©konysĂˇg nĂ¶velĂ©sĂ©re [cite: 2].
* IrĂˇnyvĂˇlasztĂˇs alapja: $m$ vektor ($C \to T$) Ă©s $n$ vektor ($C$-n ĂˇtmenĹ‘ fĂĽggĹ‘leges) bezĂˇrt szĂ¶ge [cite: 2].
* TĂˇblĂˇzatos 5-szomszĂ©dsĂˇg szabĂˇlyok [cite: 2]:
  * Clamping angle $.
  * Clamping angle $.
  * Clamping angle $.
  * Clamping angle $.
  * Clamping angle $.
  * Clamping angle $.
  * Clamping angle $.
  * Clamping angle $.
* ĂtlĂłs ĂˇthatolĂˇs (sarokvĂˇgĂˇs / ĂĽtkĂ¶zĂ©sveszĂ©ly) megelĹ‘zĂ©se: akadĂˇly a 2-es szomszĂ©dban $\implies$ tĂ¶rli 1,3-at; akadĂˇly a 4-esben $\implies$ tĂ¶rli 3,5-Ă¶t; akadĂˇly a 6-osban $\implies$ tĂ¶rli 7,5-Ă¶t; akadĂˇly a 8-asban $\implies$ tĂ¶rli 1,7-et [cite: 2].

### 1.4. RedundĂˇns Node / Ăštvonal-simĂ­tĂˇs (Path Smoothing)
* KollineĂˇris node-ok szĹ±rĂ©se: starttĂłl indulva 3 szomszĂ©dos node ($A,B,C$) vektorirĂˇnya 0 fokos eltĂ©rĂ©sĹ± $\implies$ $B$ tĂ¶rlĂ©se [cite: 2].
* Inflection bypass (tĂ¶rĂ©spont-ĂˇtugrĂˇs): starttĂłl inflekciĂłs pontok Ă¶sszekĂ¶tĂ©se ($AE, AF, AI$). Ha $AE$ nem metsz akadĂˇlyt Ă©s hossza kisebb, mint $A\to C\to E$, frissĂ­ti az utat $A\to E$-re [cite: 2].

---

## 2. Modul: MintavĂ©telezĂ©sen AlapulĂł A* (SBA*) Folytonos Terekben
**ForrĂˇs**: Persson, S. M. & Sharf, I. (2014) [cite: 4].
**cĂ©l**: Folytonos konfigurĂˇciĂłs terek ($\mathcal{X}$), ĂĽtkĂ¶zĂ©smentes subset $\mathcal{F} \subseteq \mathcal{X}$, lokĂˇlisan elĂ©rhetĹ‘ rĂ©giĂł $\mathcal{R}_l(u) \subseteq \mathcal{F}$.

### 2.1. CsomĂłpont-Ă©rtĂ©k Ă©s ValĂłszĂ­nĹ±sĂ©gi ĂltalĂˇnosĂ­tĂˇs
* Klasszikus A* binĂˇris maszk helyettesĂ­tĂ©se informĂˇciĂłnyeresĂ©g-modellel [cite: 4]:
  $$r(u) \triangleq \begin{cases} f(u) & u \in \{OPEN\} \\ \infty & \text{egyĂ©bkĂ©nt} \end{cases}$$
* EsemĂ©nyek: $\text{NEW}$ (Ăşj rĂ©szleges Ăşt), $\text{FREE}$ (ĂĽtkĂ¶zĂ©smentes szegmens) [cite: 4].
  $$r(u) = P(\text{NEW, FREE}|u)f(u) + (1 - P(\text{NEW, FREE}|u))\infty$$ [cite: 4]
  FĂĽggetlen eloszlĂˇsokkal: $P(\text{NEW, FREE}|u) = P(\text{NEW}|u)P(\text{FREE}|u)$ [cite: 4].
* VĂˇrhatĂł Ă©rtĂ©k / kulcsĂ©rtĂ©k:
  $$r(u) = \frac{f(u)}{P(\text{NEW, FREE}|u)}$$ [cite: 4]
* TopolĂłgiai alapok:
  * $\beta$-LOOKOUT: $\beta(S) \triangleq \{u \in S | \mu(\mathcal{R}_l(u)\setminus S) \ge \beta \mu(\mathcal{R}_l(S)\setminus S)\}$ [cite: 4].
  * $(\alpha, \beta)$-expansive space: $\mu(\beta(S)) \ge \alpha\mu(S)$ minden $u \in \mathcal{F}, S \subseteq \mathcal{R}_l(u)$ esetĂ©n [cite: 4].
  * LokĂˇlis Voronoi rĂ©giĂł: $\mathcal{V}_l(u) \triangleq \mathcal{R}_l(u) \cap \mathcal{V}(u)$ [cite: 4].
  * Konvergencia tĂ©tel (Theorem 4): CĂ©lvolumen $g > 0$, $\gamma \in (0,1]$. $n$ node esetĂ©n cĂ©l elĂ©rĂ©se valĂłszĂ­nĹ±sĂ©ggel $\ge 1-\gamma$, ha $n \ge \frac{k}{\alpha}\log\frac{2k}{\gamma} + \frac{2}{g}\log\frac{2}{\gamma}$, ahol $k = \frac{1}{\beta}\log\frac{2}{g}$ [cite: 4].
  * $\eta$-entanglement torzĂ­tĂˇs (Corollary 5): $d_\sigma(u,v) \le \eta d(u,v) \implies P'(u) = \frac{1}{f(u)}\frac{\mu(\mathcal{V}_L(u))}{\mu(\mathcal{R}_L(V))}$, $\alpha$ helyett $\alpha/\eta$ Ăˇll [cite: 4].

### 2.2. Praktikus PrediktĂ­v Modell (KL-divergencia & Gaussian Mixture)
* ValĂłszĂ­nĹ±sĂ©gek KL divergenciĂˇval [cite: 4]:
  $$P(\text{NEW}|u) = 1 - e^{-D_{KL}(S_u || S_{N,u})}$$
  $$P(\text{FREE}|u) = 1 - e^{-D_{KL}(S_u || S_{C,u})}$$
* NormĂˇl eloszlĂˇs pdf ($k$-dim): $S_u(x) = \frac{1}{(2\pi\sigma_u^2)^{k/2}} e^{-\frac{dist(x,p(u))^2}{2\sigma_u^2}}$ [cite: 4].
* KL divergencia egyenlĹ‘ $\sigma$-val: $D_{KL}(S_u || S_v) = \frac{dist(p(u),p(v))^2}{2\sigma^2}$ [cite: 4].
* VariĂˇciĂłs approximĂˇciĂł Gaussian mixture-re: $P(\text{NEW}|u) = 1 - \sum_{v \in N_u} S_u(p(v))e^{-D_{KL}(S_u || S_v)}$ [cite: 4].
* InkrementĂˇlis sĹ±rĹ±sĂ©g ($d(u)$) Ă©s szĹ±kĂĽlet ($c(u)$) [cite: 4]:
  $$d_{k+1}(u) = (1 - S_u(p(v)))d_k(u) + S_u(p(v))e^{-D_{KL}(S_u || S_v)}$$
  $$c_{k+1}(u) = (1 - S_u(p(v)))c_k(u) + S_u(p(v))e^{-D_{KL}(S_u || S_{c_v})}$$
* VĂ©gleges gyakorlati kulcsĂ©rtĂ©k [cite: 4]:
  $$r(u) = \frac{g(u) + h(u)}{(1 - c(u))(1 - d(u))}$$

### 2.3. Algoritmus StratĂ©giĂˇk Ă©s FinomhangolĂˇsok (Csak A*)
* **IdealizĂˇlt ciklus**: $u_{exp} = \arg\min_{u\in V} r(u)$, majd `RANDOMWALK(u_exp)` [cite: 4].
* **Praktikus Eager SBA*-Loop**: Min-heap $Q$ rendelve $r[u]$-hoz, legkisebb kinyerĂ©se, kiterjesztĂ©s, `CONNECT_PREDECESSORS` Ă©s `CONNECT_SUCCESSORS` (RRG-szerĹ± Ă©lesĂ­tĂ©s Ă©s rekurzĂ­v/BFS inkonzisztencia-propagĂˇlĂˇs $g[v]$-hez) [cite: 4].
* **Lazy & Pruned trade-off**: RRT*-stĂ­lusĂş Ă©l-metszĂ©s (pruning) szuboptimĂˇlis Ă©lekre, lusta ĂĽtkĂ¶zĂ©svizsgĂˇlat (`dist` elĹ‘szĂ¶r, `STEER` utĂˇna). Constriction $c(u)$ csak ĂĽtkĂ¶zĂ©ses hiba esetĂ©n frissĂĽl [cite: 4].
* **Anytime A* cĂ©l-torzĂ­tĂˇs**: Lagrange-szorzĂł $\lambda$ bevezetĂ©se a cĂ©l elĂ©rĂ©sĂ©nek gyorsĂ­tĂˇsĂˇra [cite: 4]:
  $$r'_{any}(u) = \frac{g(u) + h(u) + \lambda(h(u) - h_b)}{(1-c(u))(1-d(u))}$$
  Kezdeti $\lambda = 5.0$, elĂ©rĂ©s utĂˇn 0-ra decaylik [cite: 4].
* **SA-SBA* (Simulated Annealing egyensĂşlyozĂˇs)**: $\epsilon_{th} = 1 - \exp(-T_0 / \log N)$. Magas $T_0$-nĂˇl explorĂˇciĂłs lĂ©pĂ©s (vĂ©letlen mintavĂ©tel + steer mint RRT*-szerĹ± node gen), alacsony $T_0$-nĂˇl exploitatĂ­v SBA* node gen. *MegjegyzĂ©s: a vezĂ©rlĹ‘/cĂ©lzott struktĂşra az A* optimalizĂˇciĂłs keretĂ©ben marad [cite: 4].*

---

## 3. Modul: LLM Prompt KĂłdgenerĂˇlĂˇsi SpecifikĂˇciĂł (KizĂˇrĂłlag A*)
* **CĂ©lnyelv**: C++20 vagy Python 3.10+
* **AdatstruktĂşra kĂ¶vetelmĂ©nyek**:
  * Vertex struct: `p_pos`, `g_cost`, `h_cost`, `d_density`, `c_constriction`, `r_key`, `pred_ptr`.
  * Priority Queue / Min-Heap $Q$: KulcsalapĂş rendezĂ©s $r[u]$ szerint, `requeue` tĂˇmogatĂˇssal.
  * TĂ©rkĂ©ptĂˇrolĂˇs / Nearest Neighbor: DVP-tree (Dynamic Vantage-Point Tree) $O(\log N)$ lekĂ©rdezĂ©shez, cache-barĂˇt BFS tĂ¶mb layout [cite: 4].
* **ImplementĂˇciĂłs lĂ©pĂ©sek egy AI szĂˇmĂˇra**:
  1. DefinĂ­ciĂłk Ă©s KL-divergencia / Gaussian skĂˇlafaktorok rĂ¶gzĂ­tĂ©se.
  2. Folytonos `RANDOMWALK` / `STEER` fĂĽggetlen kinematikai interfĂ©sz megvalĂłsĂ­tĂˇsa.
  3. `SBA_LOOP` Ă©s a lazy/pruned Ă¶sszekĂ¶tĹ‘ rutinok lekĂłdolĂˇsa.
  4. Anytime Lagrange $\lambda$ Ă©s SA $\epsilon_{th}$ schedule integrĂˇlĂˇsa a main loop-ba.

  # TudĂˇsbĂˇzis: KizĂˇrĂłlag A*-AlapĂş ĂštvonaltervezĂ©s (DiszkrĂ©t optimalizĂˇlt & Folytonos SBA*)

> **BĹ‘vĂ­tĂ©si FigyelmeztetĂ©s**: Ezt a tĂˇrat a jĂ¶vĹ‘ben tovĂˇbbi irodalmakkal, optimalizĂˇlĂˇsi eljĂˇrĂˇsokkal (pl. kinodinamikus korlĂˇtok, MPC, hibrid rĂˇcs-mintavĂ©teles mĂłdszerek) folyamatosan bĹ‘vĂ­teni fogjuk.
> **CĂ©l**: LLM (AI) Ăˇgens betanĂ­tĂˇsa Ă©s tiszta, DWA-mentes, *kizĂˇrĂłlag A*-alapĂş* (diszkrĂ©t optimalizĂˇlt A* + folytonos SBA*) mozgĂˇstervezĹ‘ kĂłd generĂˇlĂˇsĂˇhoz (C++20 / Python).

---

## 1. Modul: DiszkrĂ©t, TovĂˇbbfejlesztett A* CsalĂˇd (GlobĂˇlis / RĂˇcsalapĂş TervezĂ©s)
**AlkalmazĂˇsi kĂ¶rnyezet**: Ismert statikus globĂˇlis rĂˇcstĂ©rkĂ©p (raster map, $M\times N$, pl. $30\times30$).

### 1.1. AlapozĂˇs Ă©s KĂ¶ltsĂ©gfĂĽggvĂ©ny
* AlapĂ©rtelmezett A* Ă©rtĂ©kelĹ‘ fĂĽggvĂ©ny:
  $$f(n) = g(n) + h(n)$$
  * $g(n)$: Start ($S$) Ă©s aktuĂˇlis node ($C$) kĂ¶zĂ¶tti tĂ©nyleges mozgĂˇsi kĂ¶ltsĂ©g [cite: 2].
  * $h(n)$: BecsĂĽlt kĂ¶ltsĂ©g $C$-bĹ‘l a CĂ©lhoz ($T$).
* Alap heurisztika variĂˇciĂłk:
  * Euklideszi tĂˇvolsĂˇg: $h(n) = \sqrt{(x_n - x_g)^2 + (y_n - y_g)^2}$.
  * Manhattan tĂˇvolsĂˇg (alacsonyabb szĂˇmĂ­tĂˇsi komplexitĂˇs): $h(n) = |x_n - x_g| + |y_n - y_g|$ [cite: 5].

### 1.2. Heurisztikai SĂşlyozĂˇsi Modellek (Irodalmi variĂˇciĂłk)

#### A) Jin & Wang (2023) â€“ PozĂ­ciĂłarĂˇnyos dinamikus sĂşlyozĂˇs [cite: 3]
* Legyen $l = \text{dist}(C, T)$ Ă©s $L = \text{dist}(C, S)$ [cite: 3].
* Dinamikus heurisztika:
  $$h(n)^* = \left(1 + \frac{l}{L}\right) \cdot h(n)$$ [cite: 3]
  * *HatĂˇs*: $C \approx S \implies l/L \text{ nagy} \implies h(n)^*$ nagy $\implies$ fĂłkuszĂˇlt/szĹ±k keresĂ©s. $C \approx T \implies l/L \text{ kicsi} \implies$ standard heurisztika $\implies$ optimĂˇlis Ăştvonal garancia [cite: 3].

#### B) Liu, Wang, Wu & Wei (2023) â€“ Kinematikai kĂ©nyszerĂ­tĂ©s & ExponenciĂˇlis skĂˇlĂˇzĂˇs [cite: 5]
* TĂˇvolsĂˇg-arĂˇny paramĂ©ter $P \in$ a node $N(x_n, y_n)$, start $S(x_s, y_s)$ Ă©s cĂ©l $G(x_g, y_g)$ kĂ¶zĂ¶tt [cite: 5]:
  $$P = \frac{|x_n - x_g| + |y_n - y_g|}{|x_s - x_g| + |y_s - y_g|}$$ [cite: 5]
* ExponenciĂˇlis dinamikus sĂşlyozĂˇsĂş Ă©rtĂ©kelĹ‘ fĂĽggvĂ©ny:
  $$f(n) = g(n) + e^P \cdot h(n)$$ [cite: 5]
  * *HatĂˇs*: AdaptĂ­van igazĂ­tja a $h(n)$ sĂşlyĂˇt az akadĂˇlyinformĂˇciĂłk Ă©s a tĂ©rbeli pozĂ­ciĂł vĂˇltozĂˇsĂˇhoz, csĂ¶kkentve a redundĂˇns node-lĂˇtogatĂˇsokat Ă©s a fordulatok szĂˇmĂˇt [cite: 5].

### 1.3. IrĂˇny-/SzomszĂ©dsĂˇg-optimalizĂˇlĂˇs Ă©s SarokvĂˇgĂˇs-vĂ©delem

#### A) Jin & Wang (2023) 5-irĂˇnyĂş szĹ±rĂ©s [cite: 3]
* 8-szomszĂ©dsĂˇg helyett cĂ©lra mutatĂł 5-irĂˇnyĂşra szĹ±kĂ­tĂ©s a $C\to T$ vektor $m$ Ă©s a fĂĽggĹ‘leges $n$ szĂ¶ge alapjĂˇn $\theta = \angle(m,n)$:
  * $.
  * TovĂˇbbi tartomĂˇnyok: 22.5Â°-os lĂ©pĂ©sekben forgatva az 5-Ă¶s maszkot [cite: 3].
* SarokvĂˇgĂˇs elleni vĂ©delem (ĂĽtkĂ¶zĂ©sbiztonsĂˇg): akadĂˇly a 2-es szomszĂ©dban $\implies$ tĂ¶rli 1,3-at; akadĂˇly a 4-esben $\implies$ tĂ¶rli 3,5-Ă¶t; akadĂˇly a 6-osban $\implies$ tĂ¶rli 7,5-Ă¶t; akadĂˇly a 8-asban $\implies$ tĂ¶rli 1,7-et [cite: 3].

#### B) Liu et al. (2023) Kinematikai IrĂˇny-tĂˇbla [cite: 5]
* A cĂ©lpont relatĂ­v szĂ¶ge $\theta$ alapjĂˇn az 8-irĂˇnyĂş child-node halmazbĂłl fixen eldobja a robot kinematikĂˇjĂˇval vagy mozgĂˇsirĂˇnyĂˇval ellentĂ©tes 3 redundĂˇns irĂˇnyt (pl. hĂˇtrafelĂ©/rossz szĂ¶gbe mutatĂł irĂˇnyok).

### 1.4. RedundĂˇns Node / Ăštvonal-simĂ­tĂˇs (Path Smoothing) [cite: 3]
1. *KollineĂˇris szĹ±rĂ©s*: Ha a hĂˇrom szomszĂ©dos node ($A, B, C$) kĂ¶zti vektorirĂˇny-vĂˇltozĂˇs 0 (szĂ¶g = 0), tĂ¶rĂ¶ld $B$-t [cite: 3].
2. *Inflection bypass*: StarttĂłl indulva kĂ¶sd Ă¶ssze a tĂ¶rĂ©spontokat ($A\to E, A\to F, A\to I$). Ha az $A\to E$ szakasz akadĂˇlymentes Ă©s hossza $< \text{cost}(A\to C\to E)$, frissĂ­tsd az utat $A\to E$-re. IsmĂ©teld a csĂşcsokrĂłl [cite: 3].

---

## 2. Modul: MintavĂ©telezĂ©sen AlapulĂł A* (SBA*) Folytonos Terekben
**ForrĂˇs**: Persson, S. M. & Sharf, I. (2014) [cite: 4].
**cĂ©l**: Folytonos konfigurĂˇciĂłs terek ($\mathcal{X}$), ĂĽtkĂ¶zĂ©smentes subset $\mathcal{F} \subseteq \mathcal{X}$, lokĂˇlisan elĂ©rhetĹ‘ rĂ©giĂł $\mathcal{R}_l(u) \subseteq \mathcal{F}$.

### 2.1. CsomĂłpont-Ă©rtĂ©k Ă©s ValĂłszĂ­nĹ±sĂ©gi ĂltalĂˇnosĂ­tĂˇs
* Klasszikus A* binĂˇris maszk helyettesĂ­tĂ©se informĂˇciĂłnyeresĂ©g-modellel [cite: 4]:
  $$r(u) \triangleq \begin{cases} f(u) & u \in \{OPEN\} \\ \infty & \text{egyĂ©bkĂ©nt} \end{cases}$$
* EsemĂ©nyek: $\text{NEW}$ (Ăşj rĂ©szleges Ăşt), $\text{FREE}$ (ĂĽtkĂ¶zĂ©smentes szegmens) [cite: 4].
  $$r(u) = P(\text{NEW, FREE}|u)f(u) + (1 - P(\text{NEW, FREE}|u))\infty$$ [cite: 4]
  FĂĽggetlen eloszlĂˇsokkal: $P(\text{NEW, FREE}|u) = P(\text{NEW}|u)P(\text{FREE}|u)$ [cite: 4].
* VĂˇrhatĂł Ă©rtĂ©k / kulcsĂ©rtĂ©k:
  $$r(u) = \frac{f(u)}{P(\text{NEW, FREE}|u)}$$ [cite: 4]
* TopolĂłgiai alapok:
  * $\beta$-LOOKOUT: $\beta(S) \triangleq \{u \in S | \mu(\mathcal{R}_l(u)\setminus S) \ge \beta \mu(\mathcal{R}_l(S)\setminus S)\}$ [cite: 4].
  * $(\alpha, \beta)$-expansive space: $\mu(\beta(S)) \ge \alpha\mu(S)$ minden $u \in \mathcal{F}, S \subseteq \mathcal{R}_l(u)$ esetĂ©n [cite: 4].
  * LokĂˇlis Voronoi rĂ©giĂł: $\mathcal{V}_l(u) \triangleq \mathcal{R}_l(u) \cap \mathcal{V}(u)$ [cite: 4].
  * Konvergencia tĂ©tel (Theorem 4): CĂ©lvolumen $g > 0$, $\gamma \in (0,1]$. $n$ node esetĂ©n cĂ©l elĂ©rĂ©se valĂłszĂ­nĹ±sĂ©ggel $\ge 1-\gamma$, ha $n \ge \frac{k}{\alpha}\log\frac{2k}{\gamma} + \frac{2}{g}\log\frac{2}{\gamma}$, ahol $k = \frac{1}{\beta}\log\frac{2}{g}$ [cite: 4].
  * $\eta$-entanglement torzĂ­tĂˇs (Corollary 5): $d_\sigma(u,v) \le \eta d(u,v) \implies P'(u) = \frac{1}{f(u)}\frac{\mu(\mathcal{V}_L(u))}{\mu(\mathcal{R}_L(V))}$, $\alpha$ helyett $\alpha/\eta$ Ăˇll [cite: 4].

### 2.2. Praktikus PrediktĂ­v Modell (KL-divergencia & Gaussian Mixture)
* ValĂłszĂ­nĹ±sĂ©gek KL divergenciĂˇval [cite: 4]:
  $$P(\text{NEW}|u) = 1 - e^{-D_{KL}(S_u || S_{N,u})}$$
  $$P(\text{FREE}|u) = 1 - e^{-D_{KL}(S_u || S_{C,u})}$$
* NormĂˇl eloszlĂˇs pdf ($k$-dim): $S_u(x) = \frac{1}{(2\pi\sigma_u^2)^{k/2}} e^{-\frac{dist(x,p(u))^2}{2\sigma_u^2}}$ [cite: 4].
* KL divergencia egyenlĹ‘ $\sigma$-val: $D_{KL}(S_u || S_v) = \frac{dist(p(u),p(v))^2}{2\sigma^2}$ [cite: 4].
* VariĂˇciĂłs approximĂˇciĂł Gaussian mixture-re: $P(\text{NEW}|u) = 1 - \sum_{v \in N_u} S_u(p(v))e^{-D_{KL}(S_u || S_v)}$ [cite: 4].
* InkrementĂˇlis sĹ±rĹ±sĂ©g ($d(u)$) Ă©s szĹ±kĂĽlet ($c(u)$) [cite: 4]:
  $$d_{k+1}(u) = (1 - S_u(p(v)))d_k(u) + S_u(p(v))e^{-D_{KL}(S_u || S_v)}$$
  $$c_{k+1}(u) = (1 - S_u(p(v)))c_k(u) + S_u(p(v))e^{-D_{KL}(S_u || S_{c_v})}$$
* VĂ©gleges gyakorlati kulcsĂ©rtĂ©k [cite: 4]:
  $$r(u) = \frac{g(u) + h(u)}{(1 - c(u))(1 - d(u))}$$

### 2.3. Algoritmus StratĂ©giĂˇk Ă©s FinomhangolĂˇsok (KizĂˇrĂłlag A*)
* **IdealizĂˇlt ciklus**: $u_{exp} = \arg\min_{u\in V} r(u)$, majd `RANDOMWALK(u_exp)` [cite: 4].
* **Praktikus Eager SBA*-Loop**: Min-heap $Q$ rendelve $r[u]$-hoz, legkisebb kinyerĂ©se, kiterjesztĂ©s, `CONNECT_PREDECESSORS` Ă©s `CONNECT_SUCCESSORS` (RRG-szerĹ± Ă©lesĂ­tĂ©s Ă©s rekurzĂ­v/BFS inkonzisztencia-propagĂˇlĂˇs $g[v]$-hez) [cite: 4].
* **Lazy & Pruned trade-off**: RRT*-stĂ­lusĂş Ă©l-metszĂ©s (pruning) szuboptimĂˇlis Ă©lekre, lusta ĂĽtkĂ¶zĂ©svizsgĂˇlat (`dist` elĹ‘szĂ¶r, `STEER` utĂˇna). Constriction $c(u)$ csak ĂĽtkĂ¶zĂ©ses hiba esetĂ©n frissĂĽl [cite: 4].
* **Anytime A* cĂ©l-torzĂ­tĂˇs**: Lagrange-szorzĂł $\lambda$ bevezetĂ©se a cĂ©l elĂ©rĂ©sĂ©nek gyorsĂ­tĂˇsĂˇra [cite: 4]:
  $$r'_{any}(u) = \frac{g(u) + h(u) + \lambda(h(u) - h_b)}{(1-c(u))(1-d(u))}$$
  Kezdeti $\lambda = 5.0$, elĂ©rĂ©s utĂˇn 0-ra decaylik [cite: 4].
* **SA-SBA* (Simulated Annealing egyensĂşlyozĂˇs A*-keretben)**: $\epsilon_{th} = 1 - \exp(-T_0 / \log N)$. Magas $T_0$-nĂˇl explorĂˇciĂłs node-gen (vĂ©letlen mintavĂ©tel + steer), alacsony $T_0$-nĂˇl exploitatĂ­v $r(u)$ alapĂş node-gen.

---

## 3. Modul: LLM Prompt KĂłdgenerĂˇlĂˇsi SpecifikĂˇciĂł (KizĂˇrĂłlag A*)
* **CĂ©lnyelv**: C++20 vagy Python 3.10+
* **AdatstruktĂşra kĂ¶vetelmĂ©nyek**:
  * Grid / Node / Vertex struct: pozĂ­ciĂł, $g$, $h$, $f$, $r$, $d$, $c$, pred_ptr.
  * Priority Queue / Min-Heap $Q$: KulcsalapĂş rendezĂ©s $r[u]$ vagy $f(n)$ szerint.
  * TĂ©rkĂ©ptĂˇrolĂˇs / Nearest Neighbor: DVP-tree (Dynamic Vantage-Point Tree) $O(\log N)$ lekĂ©rdezĂ©shez (SBA*-hoz) [cite: 4] vagy 2D/3D rĂˇcs indexelĂ©s (diszkrĂ©t A*-hoz).
* **ImplementĂˇciĂłs lĂ©pĂ©sek egy AI szĂˇmĂˇra**:
  1. DiszkrĂ©t globĂˇlis A* (Manhattan/Euklideszi + $e^P h(n)$ exponenciĂˇlis skĂˇlĂˇzĂˇs + 5-irĂˇnyĂş szĹ±rĂ©s + smoothing) megĂ­rĂˇsa.
  2. Folytonos SBA* (KL-divergencia + $d(u)/c(u)$ inkrementĂˇlis frissĂ­tĂ©s) kiegĂ©szĂ­tĹ‘ modul implementĂˇlĂˇsa.
  3. FĹ‘ ciklus Ă¶sszekĂ¶tĂ©se az optimalizĂˇlt kĂ¶ltsĂ©gfunkciĂłkkal.



  # TudĂˇsbĂˇzis: Kinematikailag korlĂˇtozott A* Ă©s DWA fĂşziĂłs algoritlus mobil robotokhoz

*ForrĂˇs/HivatkozĂˇs:* Liu, Y., Wang, C., Wu, H., Wei, Y. (2023). *Mobile Robot Path Planning Based on Kinematically Constrained A-Star Algorithm and DWA Fusion Algorithm*. Mathematics, 11(21), 4552. DOI: 10.3390/math11214552.

---

## 1. ArchitektĂşra ĂˇttekintĂ©s
* **GlobĂˇlis tervezĹ‘**: Kinematikailag korlĂˇtozott/optimalizĂˇlt $A^*$ (offline/fĂ©l-online, statikus tĂ©rkĂ©p, kevesebb kanyar, alacsonyabb szĂˇmĂ­tĂˇsi kĂ¶ltsĂ©g).
* **LokĂˇlis tervezĹ‘**: OptimalizĂˇlt DWA (Dynamic Window Approach) (online, valĂłs idejĹ± dinamikus akadĂˇlykerĂĽlĂ©s, simĂˇbb sebessĂ©gprofil).
* **FĂşziĂłs mechanizmus**: Az $A^*$ globĂˇlis ĂştvonalĂˇbĂłl **kulcspontok (key nodes)** kinyerĂ©se, melyeket a DWA sorozatos cĂ©lpontkĂ©nt ($target_{node}$) kĂ¶vet.

---

## 2. GlobĂˇlis ĂştvonaltervezĂ©s: Fejlesztett $A*$
HagyomĂˇnyos Ă©rtĂ©kelĹ‘ fĂĽggvĂ©ny:
<div style="text-align:center; margin:1em 0; font-size:1.1em;"><span class="math">f(n) = g(n) + h(n)</span></div>
Ahol <span class="math">g(n)</span> a kezdĹ‘tĹ‘l mĂ©rt tĂ©nyleges kĂ¶ltsĂ©g, <span class="math">h(n)</span> a heurisztikus becslĂ©s.

### 2.1 SzomszĂ©dsĂˇgi optimalizĂˇlĂˇs (Neighborhood Optimization)
* **ProblĂ©ma**: A 8-irĂˇnyĂş szomszĂ©dsĂˇg redundĂˇns irĂˇnyokat tartalmaz, nĂ¶velve a szĂˇmĂ­tĂˇsi terhet.
* **MegoldĂˇs**: A cĂ©lpont Ă©s a aktuĂˇlis pont kĂ¶zĂ¶tti szĂ¶g (<span class="math">Î¸</span>, Ă©szakhoz kĂ©pest) alapjĂˇn **3 redundĂˇns irĂˇny eldobĂˇsa**, a maradĂ©k 5 irĂˇny vizsgĂˇlata (lĂˇsd 1. tĂˇblĂˇzat a cikkben).

### 2.2 Heurisztikus modell cserĂ©je
* **Euklideszi helyett Manhattan-tĂˇvolsĂˇg**:
<div style="text-align:center; margin:1em 0; font-size:1.1em;"><span class="math">D = |x<sub>i</sub> â’ x<sub>j</sub>| + |y<sub>i</sub> â’ y<sub>j</sub>|</span></div>
CsĂ¶kkenti a szĂˇmĂ­tĂˇsi komplexitĂˇst.

### 2.3 Dinamikus sĂşlyozĂˇs (Distance-Scale Parameter P)
TĂˇvolsĂˇg-arĂˇny paramĂ©ter definiĂˇlĂˇsa:
<div style="text-align:center; margin:1em 0; font-size:1.1em;"><span class="math">P = \frac{|x<sub>n</sub> â’ x<sub>g</sub>| + |y<sub>n</sub> â’ y<sub>g</sub>|}{|x<sub>s</sub> â’ x<sub>g</sub>| + |y<sub>s</sub> â’ y<sub>g</sub>|} \in [0, 1]</span></div>
JavĂ­tott Ă©rtĂ©kelĹ‘ fĂĽggvĂ©ny exponenciĂˇlis sĂşlyozĂˇssal:
<div style="text-align:center; margin:1em 0; font-size:1.1em;"><span class="math">f(n) = g(n) + e<sup>P</sup> Â· h(n)</span></div>
AdaptĂ­van hangolja a heurisztika sĂşlyĂˇt az akadĂˇlyok/pozĂ­ciĂł fĂĽggvĂ©nyĂ©ben.

---

## 3. LokĂˇlis ĂştvonaltervezĂ©s: OptimalizĂˇlt DWA
HagyomĂˇnyos pĂˇlyamutatĂł-fĂĽggvĂ©ny:
<div style="text-align:center; margin:1em 0; font-size:1.1em;"><span class="math">G(v, w) = Î± Â· vel(v, w) + Î˛ Â· head(v, w) + Îł Â· dist(v, w)</span></div>
* <span class="math">vel(v, w)</span>: lineĂˇris sebessĂ©g arĂˇnya (<span class="math">v<sub>i</sub> / ÎŁ v<sub>i</sub></span>)
* <span class="math">head(v, w)</span>: cĂ©lorientĂˇciĂłs eltĂ©rĂ©s normĂˇlt Ă©rtĂ©ke (<span class="math">(Ď€ â’ Î”Î¸<sub>i</sub>) / ÎŁ(Ď€ â’ Î”Î¸<sub>i</sub>)</span>)
* <span class="math">dist(v, w)</span>: legkĂ¶zelebbi akadĂˇly tĂˇvolsĂˇgĂˇnak arĂˇnya

### 3.1 SĂşlyparamĂ©ter-optimalizĂˇlĂˇs (Empirikus / ROS guide alapjĂˇn)
* Cikkben optimĂˇlisnak talĂˇlt sĂşlyok: **<span class="math">Î± = 15</span>, <span class="math">Î˛ = 37</span>, <span class="math">Îł = 0.02</span>** (a <span class="math">Î˛</span> dominanciĂˇja biztosĂ­tja a cĂ©legyenesben lĂ©vĹ‘ akadĂˇlyok kikerĂĽlĂ©sĂ©t anĂ©lkĂĽl, hogy feleslegesen nagy Ă­veket Ă­rna le a robot).

---

## 4. KĂ­sĂ©rleti eredmĂ©nyek & benchmark (Ă–sszefoglalĂł)

| Metrika / Teszt | HagyomĂˇnyos A* + DWA (Hibrid) | Kinematikailag korlĂˇtozott A* + DWA (FĂşziĂł) | JavulĂˇs / EredmĂ©ny |
| :--- | :--- | :--- | :--- |
| **SzimulĂˇciĂłs path length** | Referencia | â’ | **â’6.24%** Ăşt hosszabbodĂˇs helyett csĂ¶kkenĂ©s |
| **SzimulĂˇciĂłs turn count** | 4 | 1 | **â’75.0%** kanyarszĂˇm |
| **SzimulĂˇciĂłs planning time** | 91.04 s | 79.45 s | **â’12.73%** idĹ‘megtakarĂ­tĂˇs |
| **Statikus globĂˇlis turn count** | 8 | 2 | **â’75.0%** kanyar |
| **Statikus globĂˇlis length** | 6.6748 m | 6.2410 m | **â’6.5%** |
| **Statikus globĂˇlis time** | 0.03374 s | 0.02524 s | **â’25.20%** |

* **Dinamikus teszt (Mir-5 robot / ROS Melodic / C++)**:
  * SimĂˇbb X-tengelyĹ± lokĂˇlis pozĂ­ciĂłkĂ¶vetĂ©s.
  * Folytonosabb, stabilabb Z-tengelyĹ± szĂ¶gsebessĂ©g (<span class="math">cmd_vel</span>) kiadĂˇs, kevesebb rezgĂ©s/tranzienstechnikai hiba.

---

## 5. Nyitott kihĂ­vĂˇsok / TovĂˇbbi kutatĂˇsi irĂˇnyok
1. **Drivetrain / Chassis tranziensek**: A DWA kĂ¶zvetlenĂĽl adja ki a <span class="math">v, w</span> sebessĂ©get acceleration/braking limetek teljes figyelembevĂ©tele nĂ©lkĂĽl -> trajektĂłriakĂ¶vetĂ©si (trajectory tracking) rĂ©teg integrĂˇlĂˇsa szĂĽksĂ©ges.
2. **VizuĂˇlis szenzorok (Kinect V2 / IMU / LiDAR)** mĂ©lyebb fĂşziĂłja dinamikus target trackinghez.
3. **KĂĽltĂ©ri/szĹ±k folyosĂłs scenĂˇriĂłk**: GlobĂˇlis road-network integrĂˇciĂł nagy tĂˇvolsĂˇgĂş tervezĂ©shez.

---
```

### DOLGOZAT_KOD_AUDIT.md

```markdown
# Diplomamunka Ă©s kĂłd teljes Ă¶sszevetĂ©se

**EllenĹ‘rzĂ©s dĂˇtuma:** 2026-10-23  
**Ă–sszevetett dolgozat:** `Rum DĂˇniel Diplomamunka.docx`  
**Ă–sszevetett kĂłd:** `codes_diploma/` Python-projektje Ă©s a `ros2_astar_dwa_gazebo/` forrĂˇscsomagja

## 1. RĂ¶vid Ă¶sszesĂ­tĂ©s

A dolgozat Ă©s a kĂłd tĂ¶bb fontos ponton egyezik: a rĂˇcsos A* keresĂ©s, a `resolution` alapĂş koordinĂˇta-ĂˇtalakĂ­tĂˇs, a BĂ©zier-ĂştvonalsimĂ­tĂˇs, a Pythonos DWA, a differenciĂˇlhajtĂˇsĂş robotmodell, valamint az A* + DWA szimulĂˇciĂł tĂ©nylegesen megtalĂˇlhatĂł a projektben.

A dolgozat azonban jelen ĂˇllapotĂˇban nem tekinthetĹ‘ teljesen kĂłdhĹ±nek. A legfontosabb eltĂ©rĂ©sek:

- a megvalĂłsĂ­tott Python A* klasszikus A*, nem az Ă¶sszes dolgozatban vagy hĂˇttĂ©ranyagban emlĂ­tett tovĂˇbbfejlesztett A* vagy SBA*;
- a mĂ©rĂ©si Ă©s benchmark-eredmĂ©nyekhez nem talĂˇlhatĂł kĂ©sz mĂ©rĂ©si futtatĂł, metrikagyĹ±jtĂ©s vagy eredmĂ©nyfĂˇjl;
- a robotkinematikai fejezetbĹ‘l hiĂˇnyzik a kerĂ©ksebessĂ©g gyorsulĂˇskorlĂˇtozĂˇsa;
- a robotkinematikai (31) Ă©s (32) kĂ©pleteknĂ©l a derivĂˇltjelĂ¶lĂ©s szĂĽksĂ©ges;
- a Pythonos Ă©s a ROS2-es DWA kĂ©t kĂĽlĂ¶nbĂ¶zĹ‘ rĂ©szleges megvalĂłsĂ­tĂˇs, nem ugyanannak a kĂłdnak a kĂ¶zvetlen portja;
- a dokumentumban szereplĹ‘ algoritmusneveket Ă©s mĂ©rĂ©si szĂˇmokat csak akkor szabad sajĂˇt megvalĂłsĂ­tĂˇskĂ©nt vagy sajĂˇt eredmĂ©nykĂ©nt bemutatni, ha kĂĽlĂ¶n kĂłddal Ă©s reprodukĂˇlhatĂł futĂˇssal is igazolhatĂłk.

## 2. StĂˇtuszjelĂ¶lĂ©sek

| StĂˇtusz | JelentĂ©s |
|---|---|
| **Egyezik** | A dolgozat ĂˇllĂ­tĂˇsa Ă©s a jelenlegi kĂłd kĂ¶zvetlenĂĽl Ă¶sszhangban van. |
| **RĂ©szben egyezik** | Az alapĂ¶tlet vagy a fĹ‘ mĹ±kĂ¶dĂ©s lĂ©tezik, de a dolgozat tĂşl tĂˇg, mĂˇs paramĂ©tert hasznĂˇl, vagy fontos korlĂˇtozĂˇst nem emlĂ­t. |
| **EltĂ©r** | A dolgozat konkrĂ©t ĂˇllĂ­tĂˇsa nem felel meg a tĂ©nyleges implementĂˇciĂłnak. |
| **Nincs implementĂˇlva** | A dolgozatban vagy a projekttervben szereplĹ‘ elemhez nem talĂˇlhatĂł mĹ±kĂ¶dĹ‘ kĂłd. |
| **Nem igazolhatĂł** | A dolgozat ĂˇllĂ­tĂˇsa mĂ©rĂ©si eredmĂ©nyre vagy kĂĽlsĹ‘ bizonyĂ­tĂ©kra hivatkozik, de ehhez nincs reprodukĂˇlhatĂł helyi futtatĂˇs vagy eredmĂ©nyfĂˇjl. |

## 3. RĂˇcstĂ©rkĂ©p Ă©s koordinĂˇtĂˇk

| Dolgozati ĂˇllĂ­tĂˇs vagy tĂ©makĂ¶r | KĂłd bizonyĂ­tĂ©ka | StĂˇtusz | SzĂĽksĂ©ges teendĹ‘ |
|---|---|---|---|
| A kĂ¶rnyezet cellĂˇkbĂłl ĂˇllĂł rĂˇcstĂ©rkĂ©p. | [`grid_map.py`](codes_diploma/astar_project/grid_map.py): `GridMap`, `grid`, `width`, `height`. | **Egyezik** | Nincs alapvetĹ‘ javĂ­tĂˇs. |
| A `resolution` a cella fizikai mĂ©rete. | [`grid_map.py`](codes_diploma/astar_project/grid_map.py): `world_to_grid()` Ă©s `grid_to_world()`. | **Egyezik** | ĂŤrd le, hogy a `grid_to_world()` a cellakĂ¶zĂ©ppontot adja vissza. |
| A vilĂˇgkoordinĂˇta Ă©s rĂˇcskoordinĂˇta kĂ¶zĂ¶tt ĂˇtalakĂ­tĂˇs tĂ¶rtĂ©nik. | `world_to_grid()` `floor()`-t hasznĂˇl, `grid_to_world()` pedig `(column + 0.5) * resolution` Ă©s `(row + 0.5) * resolution` alakot. | **Egyezik** | A sorâ€“oszlop sorrendet kĂĽlĂ¶n jelĂ¶ld: `(row, column)`, vilĂˇgban `(x, y)`. |
| Az akadĂˇlyok inflĂˇciĂłval figyelembe veszik a robot mĂ©retĂ©t. | `GridMap.inflate_obstacles(radius)` cellĂˇkra kerekĂ­tett biztonsĂˇgi zĂłnĂˇt kĂ©szĂ­t. | **RĂ©szben egyezik** | Ne Ă­rd pontos kĂ¶rgeometriĂˇnak: a jelenlegi megoldĂˇs cellaalapĂş, nĂ©gyzetes kiterjesztĂ©st alkalmaz. |
| DiagonĂˇlis mozgĂˇsnĂˇl nincs sarokvĂˇgĂˇs akadĂˇly mellett. | `get_neighbors()` csak akkor enged ĂˇtlĂłs cellĂˇt, ha a kĂ©t ortogonĂˇlis szomszĂ©d is szabad. | **Egyezik** | Nincs alapvetĹ‘ javĂ­tĂˇs. |
| Ismeretlen cellĂˇk kezelĂ©se szerepelhet a tĂ©rkĂ©pen. | `GridMap(unknown=True)` kezdeti Ă©rtĂ©ke `2`, de az A* csak `grid == 0` cellĂˇt tekint szabadnak. | **RĂ©szben egyezik** | A dolgozatban tisztĂˇzd, hogy az ismeretlen cella jelenleg nem jĂˇrhatĂł, nem kĂĽlĂ¶n SLAM- vagy bizonytalansĂˇgi modell. |

## 4. Klasszikus A*

| Dolgozati ĂˇllĂ­tĂˇs vagy tĂ©makĂ¶r | KĂłd bizonyĂ­tĂ©ka | StĂˇtusz | SzĂĽksĂ©ges teendĹ‘ |
|---|---|---|---|
| Az A* kĂ¶ltsĂ©gfĂĽggvĂ©nye `f(n) = g(n) + h(n)`. | [`astar_baseline.py`](codes_diploma/astar_project/astar_baseline.py): `f_cost = new_g_cost + h_cost`. | **Egyezik** | Nincs javĂ­tĂˇs. |
| A keresĂ©s a legkisebb `f` Ă©rtĂ©kĹ± csomĂłpontot vĂˇlasztja. | `open_list` lista, `min(open_list)`. | **Egyezik** | A dolgozatban ne prioritĂˇsi kupackĂ©nt Ă­rd, mert a kĂłd egyszerĹ± listĂˇt hasznĂˇl. |
| A mozgĂˇsi kĂ¶ltsĂ©g egyenes lĂ©pĂ©snĂ©l 1, ĂˇtlĂłnĂˇl `sqrt(2)`. | `_movement_cost()` euklideszi cellakĂ¶ltsĂ©get szĂˇmĂ­t. | **Egyezik** | Nincs javĂ­tĂˇs. |
| 4- Ă©s 8-szomszĂ©dos keresĂ©s tĂˇmogatott. | `astar_search(..., diagonal=False/True)` Ă©s `GridMap.get_neighbors()`. | **Egyezik** | Nincs javĂ­tĂˇs. |
| Az alapĂ©rtelmezett heurisztika 4-szomszĂ©dnĂˇl Manhattan, ĂˇtlĂłs keresĂ©snĂ©l Euklideszi. | `_heuristic()` az Ăˇtadott `diagonal` alapjĂˇn vĂˇlaszt. | **Egyezik** | ĂŤrd hozzĂˇ, hogy egyedi heurisztika fĂĽggvĂ©ny is ĂˇtadhatĂł. |
| Manhattan, Euklideszi, Chebyshev Ă©s Octile heurisztika mĹ±kĂ¶dik. | [`astar_variants.py`](codes_diploma/astar_project/astar_variants.py): mind a nĂ©gy fĂĽggvĂ©ny Ă©s `get_heuristic()`. | **Egyezik** | Az egyes heurisztikĂˇk alkalmazĂˇsi feltĂ©telĂ©t pontosĂ­tsd. |
| Az A* tovĂˇbbfejlesztett, dinamikusan sĂşlyozott heurisztikĂˇt hasznĂˇl. | A jelenlegi `astar_baseline.py` nem tartalmaz dinamikus sĂşlyozĂˇst; csak Ăˇtadott heurisztikĂˇt hĂ­v. | **EltĂ©r** | Ha ilyen ĂˇllĂ­tĂˇs szerepel a dolgozatban, nevezd jĂ¶vĹ‘beli vagy tervezett fejlesztĂ©snek, vagy implementĂˇld Ă©s teszteld kĂĽlĂ¶n. |
| 5-szomszĂ©dsĂˇgĂş A* mĹ±kĂ¶dik. | A kĂłdban 4 vagy 8 irĂˇny van, Ă¶tĂ¶dik irĂˇny nincs. | **Nincs implementĂˇlva** | A dolgozatbĂłl tĂ¶rlendĹ‘ sajĂˇt implementĂˇciĂłkĂ©nt, vagy kĂĽlĂ¶n meg kell valĂłsĂ­tani. |
| EA*, EBA*, EBHA*, EBHSA* vĂˇltozatok mĹ±kĂ¶dnek. | Az `astar_variants.py` csak heurisztikĂˇkat tartalmaz, ilyen keresĹ‘vĂˇltozatokat nem. | **Nincs implementĂˇlva** | A dolgozatban csak irodalmi hĂˇttĂ©rkĂ©nt vagy jĂ¶vĹ‘beli munkakĂ©nt szerepeljen. |
| Az A* hibĂˇs start- vagy cĂ©lcella esetĂ©n hibĂˇt jelez, elĂ©rhetetlen cĂ©l esetĂ©n `None`-t ad. | `astar_search()` `ValueError`-t dob Ă©rvĂ©nytelen vagy foglalt vĂ©gpontnĂˇl; sikertelen keresĂ©snĂ©l `None` vagy rĂ©szletes szĂłtĂˇr tĂ©r vissza. | **Egyezik** | Nincs javĂ­tĂˇs. |

## 5. ĂštvonalsimĂ­tĂˇs Ă©s waypointok

| Dolgozati ĂˇllĂ­tĂˇs vagy tĂ©makĂ¶r | KĂłd bizonyĂ­tĂ©ka | StĂˇtusz | SzĂĽksĂ©ges teendĹ‘ |
|---|---|---|---|
| Az A* tĂ¶rĂ¶tt vonalas Ăştvonala simĂ­thatĂł. | [`path_smoothing.py`](codes_diploma/astar_project/path_smoothing.py), `smooth_path_bezier()`. | **Egyezik** | Ne ĂˇltalĂˇnos â€žoptimĂˇlis simĂ­tĂˇskĂ©ntâ€ť, hanem BĂ©zier-alapĂş geometriai utĂłfeldolgozĂˇskĂ©nt nevezd. |
| MĂˇsodfokĂş BĂ©zier-gĂ¶rbe kĂ©szĂĽl. | `_bezier_point()` kĂ©plete Ă©s `bezier_curve_points()`. | **Egyezik** | Nincs alapvetĹ‘ javĂ­tĂˇs. |
| Az egyenes szakasz kĂ¶ztes pontjai eltĂˇvolĂ­thatĂłk. | `_remove_straight_points()` kereszt-szorzattal azonosĂ­tja a kanyarokat. | **Egyezik** | Nincs javĂ­tĂˇs. |
| A simĂ­tott gĂ¶rbe akadĂˇlybiztos. | `_is_path_safe()` a pontokat cellĂˇkra kerekĂ­ti, majd szabad cellĂˇt Ă©s megengedett szomszĂ©dsĂˇgot ellenĹ‘riz. | **RĂ©szben egyezik** | ĂŤrd le, hogy a biztonsĂˇgi ellenĹ‘rzĂ©s diszkrĂ©t, kerekĂ­tett cellĂˇkon tĂ¶rtĂ©nik, nem folytonos geometriai gĂ¶rbeâ€“akadĂˇly metszĂ©svizsgĂˇlattal. |
| A sarokvĂˇgĂˇs alapĂ©rtĂ©ke legfeljebb egy teljes cella vagy `3 * resolution`. | `smooth_path_bezier()` Ă©s `AStarDWAPlanner.plan_global()` alapĂ©rtĂ©ke `0.5 * grid_map.resolution`. | **EltĂ©r** | A dolgozatban a tĂ©nyleges alapĂ©rtĂ©ket, `0.5 * resolution`-t hasznĂˇld. |
| A gĂ¶rbe irĂˇnyvĂˇltĂˇsĂˇt a kĂłd elutasĂ­tja. | `_has_direction_reversal()` Ă©s az eredeti Ăştvonalra visszaĂˇllĂˇs. | **Egyezik** | Nincs javĂ­tĂˇs. |
| A simĂ­tĂˇs biztosan lerĂ¶vidĂ­ti vagy optimalizĂˇlja az utat. | A kĂłd csak simĂ­t, nem szĂˇmol Ă¶sszehasonlĂ­tĂł ĂştminĹ‘sĂ©gi optimumot. | **Nem igazolhatĂł** | â€žSimĂˇbbâ€ť vagy â€žfolytonosabbâ€ť ĂştvonalkĂ©nt Ă­rd, ne bizonyĂ­tottan optimĂˇlis vagy rĂ¶videbb ĂştvonalkĂ©nt. |
| A simĂ­tott ĂştbĂłl egyenletes waypointlĂˇnc kĂ©szĂĽl. | [`DWA+A.py`](codes_diploma/DWA+A.py): `_create_waypoints()` `0.2 m` alapĂ©rtelmezett Ă­vhossz-lĂ©pĂ©ssel. | **Egyezik** | A waypointot kĂĽlĂ¶nĂ­tsd el a BĂ©zier-mintaponttĂłl. |

## 6. DWA Ă©s differenciĂˇlhajtĂˇsĂş robotmodell

| Dolgozati ĂˇllĂ­tĂˇs vagy tĂ©makĂ¶r | KĂłd bizonyĂ­tĂ©ka | StĂˇtusz | SzĂĽksĂ©ges teendĹ‘ |
|---|---|---|---|
| A DWA sebessĂ©gpĂˇrokat dinamikus ablakban keresi. | [`DWA.py`](codes_diploma/DWA.py): `pairstochoose()` az aktuĂˇlis kerĂ©ksebessĂ©g kĂ¶rĂĽli gyorsulĂˇsi ablakbĂłl mintavĂ©telez. | **Egyezik** | A dolgozatban jelezd, hogy a mintavĂ©tel kerĂ©k-szĂ¶gsebessĂ©gpĂˇrokon tĂ¶rtĂ©nik. |
| A kerĂ©k kerĂĽleti sebessĂ©ge `v_L = r * omega_L`, `v_R = r * omega_R`. | [`robot.py`](codes_diploma/robot.py): `get_robot_kinematics()`. | **Egyezik** | Nincs javĂ­tĂˇs. |
| A robot lineĂˇris sebessĂ©ge a kĂ©t kerĂ©ksebessĂ©g Ăˇtlaga. | `v = ((w_L + w_R) / 2) * r_kerek`. | **Egyezik** | Nincs javĂ­tĂˇs. |
| A robot szĂ¶gsebessĂ©ge `omega = (v_R - v_L) / (2b)`. | KĂłdban `w = ((w_R - w_L) / (2 * config.b)) * config.r_kerek`; `b = 0.08 m`. | **Egyezik** | `2b` legyen a teljes kerĂ©ktĂˇvolsĂˇg, `b` a fĂ©l tengelytĂˇv. |
| A (31)â€“(32) Ă¶sszefĂĽggĂ©sek a pozĂ­ciĂł sebessĂ©gkomponensei. | A dolgozatban a derivĂˇltjel hiĂˇnyzik; a kĂłd Ăˇllapotot frissĂ­t. | **RĂ©szben egyezik** | HasznĂˇld: `dot{x} = v cos(theta)`, `dot{y} = v sin(theta)`. |
| Egyenes haladĂˇsnĂˇl a robot az aktuĂˇlis irĂˇny mentĂ©n mozdul. | `update()` $ w == 0 ` Ăˇg: `x += v*cos(theta)*dt`, `y += v*sin(theta)*dt`. | **Egyezik** | MegjegyzendĹ‘ a kĂłdban hasznĂˇlt `abs(w) <= 1e-6` kĂĽszĂ¶b. |
| ĂŤves mozgĂˇsnĂˇl kĂ¶rĂ­ves integrĂˇlĂˇs tĂ¶rtĂ©nik. | `update()` $ abs(w) > 1e-6 ` Ăˇg zĂˇrt alakĂş szinuszos/koszinuszos kĂ©pleteket hasznĂˇl. | **Egyezik** | â€žNumerikus integrĂˇlĂˇsâ€ť helyett â€žzĂˇrt alakĂş kĂ¶rĂ­ves integrĂˇlĂˇsâ€ť a pontosabb megfogalmazĂˇs. |
| A cĂ©lzott kerĂ©ksebessĂ©g kĂ¶zvetlenĂĽl megvalĂłsul. | `update()` elĹ‘bb `np.clip()`-pel korlĂˇtozza a kerĂ©k-szĂ¶gsebessĂ©g vĂˇltozĂˇsĂˇt. | **EltĂ©r** | A dolgozatba vedd fel: `max_w_dot = a_max / r_kerek`, majd a cĂ©lĂ©rtĂ©k korlĂˇtozĂˇsa. |
| A robotparamĂ©terek a dolgozatban szereplĹ‘ Ă©rtĂ©kek. | `robotconfig()`: `r_kerek=0.033`, `b=0.08`, `w_kerek_max=15`, `a_max=2`, `dt=0.1`, `predict_time=3`. | **Egyezik** | Ezeket a mĂ©rtĂ©kegysĂ©gekkel egyĂĽtt add meg. |
| A DWA tetszĹ‘leges hĂˇtramenetet hasznĂˇlhat. | `allow_reverse=False`; a negatĂ­v `v` Ă©rtĂ©kĹ± pĂˇrokat a DWA kihagyja. | **RĂ©szben egyezik** | A dolgozatban Ă­rd le, hogy a jelenlegi alapbeĂˇllĂ­tĂˇs elĹ‘remenetet enged. |
| A DWA ĂĽtkĂ¶zĂ©svizsgĂˇlata a mozgĂł akadĂˇly jĂ¶vĹ‘beli pozĂ­ciĂłjĂˇt is figyelembe veszi. | `get_dist_on_trajectory()` `x + vx*t`, `y + vy*t` alapjĂˇn ellenĹ‘riz. | **Egyezik** | ĂŤrd hozzĂˇ a 3 m-es Ă©rzĂ©kelĂ©si tĂˇvolsĂˇgot Ă©s 180 fokos elĂĽlsĹ‘ lĂˇtĂłmezĹ‘t. |
| A megĂˇllĂˇsi feltĂ©tel `|v| <= sqrt(2*a_max*d)`. | `AdmissableVelocity()` ezt a feltĂ©telt hasznĂˇlja. | **Egyezik** | Nincs javĂ­tĂˇs. |
| A DWA sĂşlyai a szakirodalmi Ă©rtĂ©kek. | A Python `robotconfig()` alapĂ©rtĂ©kei `Alfa=5`, `Beta=2`, `Gamma=3`; a jelenlegi kĂłd nem a hĂˇttĂ©ranyagban szereplĹ‘ `15,37,0.02` Ă©rtĂ©keket hasznĂˇlja. | **EltĂ©r** | A dolgozatban a tĂ©nyleges kĂ­sĂ©rleti konfigurĂˇciĂłt add meg, vagy nevezd kĂĽlĂ¶n szakirodalmi Ă¶sszehasonlĂ­tĂˇsnak. |

## 7. A* + DWA Python-szimulĂˇciĂł

| Dolgozati ĂˇllĂ­tĂˇs vagy tĂ©makĂ¶r | KĂłd bizonyĂ­tĂ©ka | StĂˇtusz | SzĂĽksĂ©ges teendĹ‘ |
|---|---|---|---|
| A globĂˇlis A* Ă©s lokĂˇlis DWA egyĂĽttmĹ±kĂ¶dik. | [`DWA+A.py`](codes_diploma/DWA+A.py): `plan_global()` A*-t futtat, `plan_local()` DWA-parancsot vĂˇlaszt. | **Egyezik** | Nincs alapvetĹ‘ javĂ­tĂˇs. |
| Az A* statikus tĂ©rkĂ©pen dolgozik, a DWA kezeli a lokĂˇlis akadĂˇlyokat. | [`simulation.py`](codes_diploma/simulation.py): statikus falak a `GridMap`-ben, kĂĽlĂ¶n mozgĂł akadĂˇlylista a DWA-hoz. | **Egyezik** | A globĂˇlis tĂ©rkĂ©p dinamikus ĂşjratervezĂ©sĂ©nek hiĂˇnyĂˇt emlĂ­tsd meg. |
| A waypointok kĂ¶vetĂ©se adaptĂ­v elĹ‘retekintĂ©st hasznĂˇl. | `DWA+A.py`: `_update_pruned_lookahead_target()`, `0.35â€“0.80 m` kĂ¶zĂ© szorĂ­tott lookahead. | **Egyezik** | A pontos hatĂˇrokat add meg, ne ĂˇltalĂˇnos â€žadaptĂ­vâ€ť ĂˇllĂ­tĂˇs maradjon. |
| A vĂ©gsĹ‘ cĂ©l elĂ©rĂ©se fix, minden helyzetben azonos tolerancia. | `reached_goal()` Ă©s `_current_tolerance()` dinamikusan `0.05â€“0.2 m` kĂ¶zĂ¶tt szĂˇmol. | **EltĂ©r** | A dolgozatban dinamikus toleranciĂˇt Ă­rj. |
| A rendszer globĂˇlisan Ăşjratervez, ha mozgĂł akadĂˇly kerĂĽl az Ăştra. | A `plan_local()` az aktuĂˇlis Ăştvonal waypointjait kĂ¶veti; Ăşj A* keresĂ©s nincs minden akadĂˇlymozgĂˇs utĂˇn. | **Nincs implementĂˇlva** | Ne ĂˇllĂ­ts globĂˇlis dinamikus ĂşjratervezĂ©st, csak lokĂˇlis DWA-elkerĂĽlĂ©st. |
| A szimulĂˇciĂł megjelenĂ­ti a biztonsĂˇgos Ă©s veszĂ©lyes pĂˇlyĂˇkat, valamint a fĂ©kezĂ©si szakaszokat. | `simulation.py`: `compute_onlab_trajectories()` Ă©s Matplotlib `LineCollection` objektumok. | **Egyezik** | Nincs javĂ­tĂˇs. |
| A simĂ­tĂˇs alapĂ©rtelmezett vĂˇgĂˇsa `0.5 * resolution`. | `AStarDWAPlanner.plan_global()` Ă©s `smooth_path_bezier()`. | **Egyezik** | Nincs javĂ­tĂˇs. |

## 8. TisztĂˇn A*-os szimulĂˇciĂł

| Dolgozati ĂˇllĂ­tĂˇs vagy tĂ©makĂ¶r | KĂłd bizonyĂ­tĂ©ka | StĂˇtusz | SzĂĽksĂ©ges teendĹ‘ |
|---|---|---|---|
| Az A* demonstrĂˇciĂł statikus tĂ©rkĂ©pen fut. | [`astar_simulation.py`](codes_diploma/astar_project/astar_simulation.py): `create_demo_map()`, `plot_simulation()`. | **Egyezik** | Nincs javĂ­tĂˇs. |
| Ez a demonstrĂˇciĂł teljes fizikai robotmodellt hasznĂˇl. | A modul a cellaĂştvonalbĂłl interpolĂˇlt vagy BĂ©zier-pontokat kĂ©szĂ­t; nem hĂ­vja a `robot.update()` kinematikai frissĂ­tĂ©sĂ©t. | **EltĂ©r** | A dolgozatban kĂĽlĂ¶nĂ­tsd el az A* vizualizĂˇciĂłt az A* + DWA fizikai szimulĂˇciĂłtĂłl. |
| A tisztĂˇn A*-os modul sebessĂ©get, gyorsulĂˇst Ă©s mozgĂł akadĂˇlyt vizsgĂˇl. | A `create_robot_trajectory()` csak geometriai pontokat generĂˇl. | **Nincs implementĂˇlva** | Ezt ne tulajdonĂ­tsd az `astar_simulation.py` modulnak. |

## 9. MĂ©rĂ©si rendszer Ă©s eredmĂ©nyek

| Dolgozati ĂˇllĂ­tĂˇs vagy tĂ©makĂ¶r | KĂłd bizonyĂ­tĂ©ka | StĂˇtusz | SzĂĽksĂ©ges teendĹ‘ |
|---|---|---|---|
| A projekt automatikusan Ăştvonalhosszt, kanyarszĂˇmot Ă©s futĂˇsi idĹ‘t mĂ©r. | [`metrics.py`](codes_diploma/astar_project/metrics.py) jelenleg csak moduldokumentĂˇciĂłt tartalmaz. | **Nincs implementĂˇlva** | A dolgozat mĂ©rĂ©si mĂłdszerĂ©t vagy kĂłdoldalon kell megvalĂłsĂ­tani, vagy kĂ©zi/elĹ‘zetes eredmĂ©nykĂ©nt kell jelĂ¶lni. |
| A projekt tĂ¶bb forgatĂłkĂ¶nyvet automatikusan lefuttat. | [`experiments.py`](codes_diploma/astar_project/experiments.py) jelenleg nem tartalmaz futtatĂˇsi logikĂˇt. | **Nincs implementĂˇlva** | Ne ĂˇllĂ­ts automatikus paramĂ©ter-sĂ¶prĂ©st. |
| A parancssori kĂ­sĂ©rletfuttatĂł kĂ©sz. | [`run_experiment.py`](codes_diploma/astar_project/run_experiment.py) explicit mĂłdon `Experiment runner is not implemented yet.` ĂĽzenettel Ăˇll le. | **EltĂ©r** | A dolgozatban kĂ©sz mĂ©rĂ©si infrastruktĂşrakĂ©nt nem szerepelhet. |
| A mĂ©rĂ©si eredmĂ©nyek reprodukĂˇlhatĂłk a `results` mappĂˇbĂłl. | A `results/raw`, `figures`, `tables` mappĂˇkban nincs futtatott eredmĂ©nyadatokra utalĂł kĂ©sz eredmĂ©nykĂ©szlet. | **Nem igazolhatĂł** | A dolgozatban minden szĂˇmhoz add meg a futtatĂł szkriptet, paramĂ©tereket Ă©s eredmĂ©nyfĂˇjlt. |
| A tudĂˇsbĂˇzisban szereplĹ‘ benchmarkok sajĂˇt kĂ­sĂ©rleti eredmĂ©nyek. | [`tudasbazis.MD`](codes_diploma/tudasbazis.MD) irodalmi/tervezĂ©si hĂˇttĂ©rszĂ¶veg; a helyi mĂ©rĂ©si pipeline hiĂˇnyzik. | **Nem igazolhatĂł** | A `-6.24%`, `-75%`, idĹ‘- Ă©s ĂştvonalhosszĂ©rtĂ©keket ne nevezd sajĂˇt mĂ©rĂ©snek bizonyĂ­tĂ©k nĂ©lkĂĽl. |

## 10. ROS2 Ă©s Gazebo

| Dolgozati ĂˇllĂ­tĂˇs vagy tĂ©makĂ¶r | KĂłd bizonyĂ­tĂ©ka | StĂˇtusz | SzĂĽksĂ©ges teendĹ‘ |
|---|---|---|---|
| ROS2 + Gazebo szimulĂˇciĂł TurtleBot3 Waffle robottal mĹ±kĂ¶dik. | [`dwa_world.sdf`](codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/worlds/dwa_world.sdf), launch- Ă©s csomagfĂˇjlok. | **Egyezik** | A futtatĂˇsi kĂ¶rnyezetet, ROS2-disztribĂşciĂłt Ă©s Gazebo-verziĂłt pontosĂ­tsd. |
| A ROS2-ben A* globĂˇlis Ăştvonal Ă©s DWA lokĂˇlis vezĂ©rlĂ©s mĹ±kĂ¶dik. | C++ [`astar_dwa_node.cpp`](codes_diploma/ros2_astar_dwa_gazebo/src/astar_dwa_controller/src/astar_dwa_node.cpp), Python `dwa_node.py`, `planner_node.py`. | **RĂ©szben egyezik** | A C++ Ă©s Python Ăˇgakat kĂĽlĂ¶n Ă­rd le; ne kezeld Ĺ‘ket egyetlen azonos implementĂˇciĂłkĂ©nt. |
| A ROS2-es DWA a Python DWA teljes vĂˇltozata. | A ROS2 Ăˇg kĂĽlĂ¶n vezĂ©rlĂ©si kĂłdot Ă©s sajĂˇt sebessĂ©gmintĂˇkat hasznĂˇl. | **EltĂ©r** | â€žROS2-kompatibilis prototĂ­pusâ€ť vagy â€žrĂ©szleges integrĂˇciĂłâ€ť a pontosabb megnevezĂ©s. |
| A LiDAR-adatok alapjĂˇn lokĂˇlis akadĂˇlytĂ©rkĂ©p kĂ©szĂĽl. | `planner_node.py` LiDAR-adatbĂłl rĂˇcsot Ă©pĂ­t Ă©s A*-t futtat; a launch konfigurĂˇciĂłtĂłl fĂĽggĹ‘en a C++ controller Ăˇg is hasznĂˇlhatĂł. | **RĂ©szben egyezik** | A tĂ©nylegesen indĂ­tott launch fĂˇjlt Ă©s a vĂˇlasztott node-ot nevezd meg. |
| A mozgĂł akadĂˇlyt a globĂˇlis A* elkerĂĽli. | `moving_obstacle_node.py` mozgatja az akadĂˇlyt, de a statikus globĂˇlis tĂ©rkĂ©p nem minden ciklusban tervez Ăşjra. | **Nincs implementĂˇlva** | LokĂˇlis akadĂˇlyelkerĂĽlĂ©skĂ©nt Ă­rd le, ne globĂˇlis dinamikus ĂşjratervezĂ©skĂ©nt. |
| A ROS2/Gazebo futĂˇsbĂłl mĂ©rĂ©si eredmĂ©nyek szĂˇrmaznak. | ForrĂˇskĂłd Ă©s launch fĂˇjlok vannak, de a dolgozati eredmĂ©nyekhez kĂ¶tĂ¶tt automatikus adatgyĹ±jtĂ©s nem azonosĂ­thatĂł. | **Nem igazolhatĂł** | A mĂ©rĂ©si naplĂłkat, rosbaget vagy kiĂ©rtĂ©kelĹ‘ szkriptet csatolni kellene. |

## 11. Fogalmi Ă©s szĂ¶veges eltĂ©rĂ©sek

| Hely vagy ĂˇllĂ­tĂˇs | Jelenlegi problĂ©ma | JavĂ­tĂˇs |
|---|---|---|
| DWA bevezetĹ‘je | A dolgozat egyik rĂ©szĂ©ben â€žszinkronhajtĂˇsĂş robotâ€ť szerepel, mikĂ¶zben a sajĂˇt modell differenciĂˇlhajtĂˇsĂş. | CserĂ©ld â€ždifferenciĂˇlhajtĂˇsĂş robotâ€ť-ra. |
| Robotkinematika (31)â€“(32) | A kĂ©pletekben az `x` Ă©s `y` derivĂˇltjele hiĂˇnyzik. | `dot{x}` Ă©s `dot{y}` jelĂ¶lĂ©st hasznĂˇlj. |
| Robotkinematika (30) | A `b` Ă©s `2b` jelentĂ©se csak akkor helyes, ha `b` fĂ©l tengelytĂˇv. | ĂŤrd le: `2b` teljes kerĂ©ktĂˇvolsĂˇg, `b` fĂ©l tengelytĂˇv. |
| RobotĂˇllapot frissĂ­tĂ©se | A dolgozat csak a kinematikai kĂ©pleteket Ă­rja le, az aktuĂˇlis kerĂ©ksebessĂ©gek gyorsulĂˇskorlĂˇtozĂˇsĂˇt nem. | Vedd fel az `a_max / r` alapĂş kerĂ©ksebessĂ©g-korlĂˇtot. |
| IntegrĂˇlĂˇs megnevezĂ©se | A kĂłd Ă­ves mozgĂˇsnĂˇl zĂˇrt alakĂş kĂ¶rĂ­ves megoldĂˇst hasznĂˇl. | â€žZĂˇrt alakĂş kĂ¶rĂ­ves integrĂˇlĂˇsâ€ť legyen a pontos megfogalmazĂˇs. |
| A* vĂˇltozatok | A hĂˇttĂ©ranyagban vagy tervben szereplĹ‘ algoritmusokat a mĹ±kĂ¶dĹ‘ Python kĂłd nem tartalmazza. | VĂˇlaszd kĂĽlĂ¶n: szakirodalmi hĂˇttĂ©r, terv, megvalĂłsĂ­tott algoritmus. |
| MĂ©rĂ©si eredmĂ©nyek | A szĂˇmokhoz nincs azonosĂ­thatĂł helyi mĂ©rĂ©si pipeline Ă©s eredmĂ©nyfĂˇjl. | Minden szĂˇm mellĂ© futtatĂˇsi paramĂ©ter, kĂłd, dĂˇtum Ă©s eredmĂ©nyfĂˇjl szĂĽksĂ©ges. |

## 12. EllenĹ‘rzĂ¶tt tesztek Ă©s ellenĹ‘rzĂ©si korlĂˇtok

A robot- Ă©s DWA-mag cĂ©lzott tesztje sikeresen lefutott:

```text
python -m unittest codes_diploma.astar_project.tests.test_robot_and_dwa
Ran 4 tests in 0.336s
OK
```

A dolgozat Ă©s a kĂłd Ă¶sszevetĂ©se sorĂˇn ellenĹ‘rzĂ¶tt fĹ‘ forrĂˇsok:

- [`robot.py`](codes_diploma/robot.py)
- [`DWA.py`](codes_diploma/DWA.py)
- [`DWA+A.py`](codes_diploma/DWA+A.py)
- [`simulation.py`](codes_diploma/simulation.py)
- [`grid_map.py`](codes_diploma/astar_project/grid_map.py)
- [`astar_baseline.py`](codes_diploma/astar_project/astar_baseline.py)
- [`astar_variants.py`](codes_diploma/astar_project/astar_variants.py)
- [`path_smoothing.py`](codes_diploma/astar_project/path_smoothing.py)
- [`astar_simulation.py`](codes_diploma/astar_project/astar_simulation.py)
- [`metrics.py`](codes_diploma/astar_project/metrics.py)
- [`experiments.py`](codes_diploma/astar_project/experiments.py)
- [`run_experiment.py`](codes_diploma/astar_project/run_experiment.py)
- [`astar_dwa_node.cpp`](codes_diploma/ros2_astar_dwa_gazebo/src/astar_dwa_controller/src/astar_dwa_node.cpp)
- [`planner_node.py`](codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/dwa_gazebo_sim/planner_node.py)
- [`dwa_node.py`](codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/dwa_gazebo_sim/dwa_node.py)
- [`moving_obstacle_node.py`](codes_diploma/ros2_astar_dwa_gazebo/src/dwa_gazebo_sim/dwa_gazebo_sim/moving_obstacle_node.py)
- [`README.md`](codes_diploma/ros2_astar_dwa_gazebo/README.md)

A DOCX kĂ©pletei Word OMML matematikai objektumkĂ©nt szerepelnek; a robotkinematikai fejezet (27)â€“(37) kĂ©pleteinek szerkezete kĂĽlĂ¶n ki lett olvasva. A teljes dolgozat vizuĂˇlis tĂ¶rdelĂ©se, ĂˇbraalĂˇĂ­rĂˇsai Ă©s minden kĂĽlsĹ‘ szakirodalmi hivatkozĂˇs tartalmi hitelessĂ©ge ebbĹ‘l a kĂłd-auditbĂłl nem bizonyĂ­thatĂł.

## 13. JavĂ­tĂˇsi sorrend

1. A dolgozatban javĂ­tsd a robotkinematikai jelĂ¶lĂ©seket Ă©s egĂ©szĂ­tsd ki a gyorsulĂˇskorlĂˇtozĂˇssal.
2. VĂˇlaszd kĂĽlĂ¶n a mĹ±kĂ¶dĹ‘ klasszikus A* Ă©s a csak tervezett/tĂˇrgyalt A* vĂˇltozatokat.
3. A mĂ©rĂ©si eredmĂ©nyeket csak reprodukĂˇlhatĂł futtatĂˇs utĂˇn hagyd sajĂˇt eredmĂ©nykĂ©nt.
4. A Pythonos Ă©s ROS2-es DWA implementĂˇciĂłt kĂĽlĂ¶n rendszerkĂ©nt Ă­rd le.
5. A tisztĂˇn A*-os demonstrĂˇciĂłt kĂĽlĂ¶nĂ­tsd el az A* + DWA fizikai szimulĂˇciĂłtĂłl.
6. A dolgozat vĂ©gĂ©n vagy a mellĂ©kletben add meg a konkrĂ©t futtatĂˇsi parancsokat, paramĂ©tereket Ă©s teszteredmĂ©nyeket.

## 14. Ctrl+F keresĹ‘lista a dolgozathoz

Az alĂˇbbi kifejezĂ©seket mĂˇsold be a Word keresĹ‘jĂ©be. A talĂˇlat utĂˇn ellenĹ‘rizd a
mellette megadott ĂˇllĂ­tĂˇst, kĂ©pletet vagy fejezetet.

| KeresendĹ‘ pontos szĂ¶vegrĂ©szlet | Hol talĂˇlhatĂł / mit ellenĹ‘rizz | JavĂ­tĂˇs vagy megjegyzĂ©s |
|---|---|---|
| `szinkronhajtĂˇsĂş mobilrobot` | DWA elmĂ©leti bevezetĂ©se | A sajĂˇt modell differenciĂˇlhajtĂˇsĂş, ezĂ©rt ezt cserĂ©ld `differenciĂˇlhajtĂˇsĂş mobilrobot` kifejezĂ©sre. |
| `A megvalĂłsĂ­tĂˇsom Ă©s a dolgozatom mĂˇsodik lĂ©nyeges eleme` | DWA fejezet eleje | Ez a DWA-rĂ©sz kezdĹ‘mondata; ellenĹ‘rizd ugyanebben a bekezdĂ©sben a robot tĂ­pusĂˇt Ă©s a sebessĂ©gtĂ©r definĂ­ciĂłjĂˇt. |
| `A kinematikai korlĂˇtokat a szinkronhajtĂˇsĂş robot sebessĂ©gterĂ©nek` | DWA fejezet | A â€žszinkronhajtĂˇsĂşâ€ť megnevezĂ©s itt is hibĂˇs a jelenlegi robotmodellhez kĂ©pest. |
| `Mivel a robot jelentĹ‘s tehetetlensĂ©ggel rendelkezik` | Dinamikus ablak Ă©s gyorsulĂˇsi korlĂˇt | Ez a szĂ¶veg a DWA dinamikus ablakĂˇt Ă­rja le. EgĂ©szĂ­tsd ki azzal, hogy a `robot.py` az ĂˇllapotfrissĂ­tĂ©sben is korlĂˇtozza a kerĂ©k-szĂ¶gsebessĂ©g vĂˇltozĂˇsĂˇt. |
| `Ahogyan a kĂłdomban is megvalĂłsĂ­tottam` | A DWA dinamikus ablakĂˇnak magyarĂˇzata | EllenĹ‘rizd, hogy a hivatkozott kĂ©plet tĂ©nyleg a `pairstochoose()` Ă©s nem csak elmĂ©leti sebessĂ©gtĂ©r mĹ±kĂ¶dĂ©sĂ©t Ă­rja-e le. |
| `A megvalĂłsĂ­tott rendszerben az A* algoritmus felel` | A* Ă©s DWA fĂşziĂłja | Ez a rĂ©sz jĂłl illeszkedik a `DWA+A.py` mĹ±kĂ¶dĂ©sĂ©hez; ellenĹ‘rizd, hogy a globĂˇlis ĂşjratervezĂ©s hiĂˇnya szerepel-e. |
| `BĂ©zier-gĂ¶rbĂ©kkel simĂ­tunk` | A* Ă©s DWA fĂşziĂłja | Egyezik a `path_smoothing.py` Ă©s `DWA+A.py` mĹ±kĂ¶dĂ©sĂ©vel. Ne nevezd optimĂˇlis simĂ­tĂˇsnak. |
| `mĂˇsodfokĂş BĂ©zier-gĂ¶rbĂ©kkel simĂ­tom` | ĂštvonalsimĂ­tĂˇs fejezete | Egyezik; a kĂ¶vetkezĹ‘ mondatokban keresd a kerekĂ­tett cellĂˇkon vĂ©gzett biztonsĂˇgi ellenĹ‘rzĂ©st is. |
| `A rendszer rĂˇcscellĂˇkra kerekĂ­ti a gĂ¶rbe pontjait` | BĂ©zier-simĂ­tĂˇs biztonsĂˇgi ellenĹ‘rzĂ©se | Egyezik a `_is_path_safe()` mĹ±kĂ¶dĂ©sĂ©vel, de ez diszkrĂ©t ellenĹ‘rzĂ©s, nem folytonos gĂ¶rbeâ€“akadĂˇly metszĂ©svizsgĂˇlat. |
| `Ha az Ă­v nem biztonsĂˇgos` | BĂ©zier-simĂ­tĂˇs fallback Ăˇga | Egyezik: a kĂłd ilyenkor az eredeti A* Ăştvonalat adja vissza. |
| `create_waypoints fĂĽggvĂ©ny vĂ©gzi` | Waypoint-ĂşjramintavĂ©telezĂ©s | A dolgozatban ellenĹ‘rizd a pontos lĂ©pĂ©skĂ¶zt: a kĂłd alapĂ©rtĂ©ke `0.2 m`. |
| `pontosan` Ă©s `mĂ©terenkĂ©nt helyez el` | A `create_waypoints` mondatĂˇnak kĂ¶rnyezete | Csak akkor maradjon Ă­gy, ha az egyenlĹ‘ Ă­vhosszĂş waypoint-generĂˇlĂˇsrĂłl van szĂł; a BĂ©zier-mintapontok nem ugyanazok, mint a waypointok. |
| `Path Pruning (Ăštvonal-metszĂ©s)` | PĂˇlyakĂ¶vetĂ©si fejezet | Egyezik a `_update_pruned_lookahead_target()` fĂĽggvĂ©nnyel; keresd a `25` elemĹ± keresĂ©si ablak Ă©s a `0.35â€“0.80 m` lookahead Ă©rtĂ©ket. |
| `legkĂ¶zelebbi pont keresĂ©sĂ©t a megelĹ‘zĹ‘ ciklus indexĂ©tĹ‘l` | Path pruning rĂ©sz | Egyezik a kĂłddal, mert a waypoint-index nem lĂ©p vissza. |
| `A szimulĂˇciĂł alapjĂˇt a differenciĂˇlhajtĂˇsĂş robot matematikai modellje adja` | Robotkinematikai fejezet eleje | A fejezet megfelelĹ‘ kiindulĂˇs; innen keresd a (27)â€“(37) kĂ©pleteket. |
| `Ahol a 2b paramĂ©ter a kĂ©t hajtott kerĂ©k kĂ¶zĂ¶tti tengelytĂˇvolsĂˇgot jelĂ¶li` | A (30) kĂ©plet utĂˇn | Ez csak akkor pontos, ha `b` fĂ©l tengelytĂˇv. A kĂłdban `b = 0.08 m`, ezĂ©rt a teljes kerĂ©ktĂˇvolsĂˇg `2b = 0.16 m`. |
| `a szĂ¶gsebessĂ©g nulla` | Egyenes vonalĂş mozgĂˇs leĂ­rĂˇsa | EllenĹ‘rizd, hogy a kĂ©plet mellett szerepel-e a kĂłdbeli kĂĽszĂ¶b: `abs(w) <= 1e-6`, nem csak az elmĂ©leti `w = 0`. |
| `az ĂˇllapotfrissĂ­tĂ©s numerikus integrĂˇlĂˇssal valĂłsul meg` | A (31)â€“(32) kĂ©pletek elĹ‘tti bekezdĂ©s | ĂŤves mozgĂˇsnĂˇl pontosabb: `zĂˇrt alakĂş kĂ¶rĂ­ves integrĂˇlĂˇs`. |
| `A robot Ăşj ĂˇllapotĂˇnak` | A (33)â€“(35) kĂ©pletek bevezetĂ©se | Itt ellenĹ‘rizd a vĂˇltozĂłkat: `x`, `y`, `theta`, `v`, `w` Ă©s `dt`. |
| `Amennyiben a szĂ¶gsebessĂ©g nem nulla` | A (36)â€“(37) kĂ¶rĂ­ves kĂ©pletek bevezetĂ©se | Egyezik a kĂłd `abs(w) > 1e-6` ĂˇgĂˇval. |
| `Ez a matematikai megkĂ¶zelĂ­tĂ©s biztosĂ­tja` | Robotkinematikai fejezet zĂˇrĂłmondata | A mondat maradhat, de Ă©rdemes hozzĂˇtenni, hogy ez ideĂˇlis, csĂşszĂˇsmentes kinematikai modell. |
| `A szimulĂˇciĂłs eredmĂ©nyek Ă©s forgatĂłkĂ¶nyvek vizsgĂˇlata` | EredmĂ©nyfejezet cĂ­me | EllenĹ‘rizd minden tĂˇblĂˇzat Ă©s Ăˇbra mĂ¶gĂ¶tt a futtatott kĂłdot, paramĂ©tert Ă©s eredmĂ©nyfĂˇjlt. |
| `A szimulĂˇciĂłk igazoljĂˇk` | A heurisztikĂˇk vagy eredmĂ©nyek Ă©rtĂ©kelĂ©se | Minden ilyen mondathoz kell helyi mĂ©rĂ©si eredmĂ©ny; a jelenlegi `metrics.py` Ă©s `run_experiment.py` nem szolgĂˇltat kĂ©sz benchmark-pipeline-t. |
| `legmagasabb szĂˇmĂ­tĂˇsi hatĂ©konysĂˇgot` | Heurisztika-Ă¶sszegzĂ©s | Csak mĂ©rĂ©si tĂˇblĂˇzattal Ă©s azonos forgatĂłkĂ¶nyvekkel igazolhatĂł; elmĂ©leti ĂˇllĂ­tĂˇskĂ©nt Ăłvatosabban fogalmazd. |
| `ROS 2 szoftverarchitektĂşra Ă©s Gazebo szimulĂˇciĂłs kĂ¶rnyezet` | ROS2/Gazebo fejezet cĂ­me | Az indĂ­tott launch fĂˇjlt Ă©s a tĂ©nylegesen hasznĂˇlt C++ vagy Python node-ot nevezd meg. |
| `ROS 2 csomĂłpont-architektĂşra Ă©s kommunikĂˇciĂłs interfĂ©szek` | ROS2 alfejezet | EllenĹ‘rizd a topicneveket Ă©s azt, hogy a dolgozat ne ĂˇllĂ­tsa a Python DWA teljes ROS2-portjĂˇt. |
| `Gazebo 3D fizikai szimulĂˇciĂł` | Gazebo alfejezet | A vilĂˇg Ă©s a robotmodell jelen van, de automatikus mĂ©rĂ©si eredmĂ©ny csak naplĂłval vagy kiĂ©rtĂ©kelĹ‘ szkripttel bizonyĂ­thatĂł. |
```

### frames_2026-10-29_16.36.43.gv

```
digraph G {
"odom" -> "base_link"[label=" Broadcaster: default_authority\nAverage rate: 50.82\nBuffer length: 1.22\nMost recent transform: 88.42\nOldest transform: 87.2\n"];
"base_link" -> "base_scan"[label=" Broadcaster: default_authority\nAverage rate: 50.833\nBuffer length: 1.2\nMost recent transform: 88.4\nOldest transform: 87.2\n"];
edge [style=invis];
 subgraph cluster_legend { style=bold; color=black; label ="view_frames Result";
"Recorded at time: 1793288203.5363119"[ shape=plaintext ] ;
}->"odom";
}
```

### Önlab/DWA_py.py

```python
import matplotlib.pyplot as plt     # kirajzolĂˇsra- szimulĂˇciĂł           --> cmd:pip install matplotlib numpy
import math                         # matematikai mĹ±veletekre pl.:pi

import numpy as np      #gyorsabb szĂˇmolĂˇs miatt --> ez C-ben Ă­rodott

import pandas as pd
import time
"""
get_robot_kinematics : a kerĂ©kadatokbĂłl v,w pĂˇrokat szĂˇmol --> differenciĂˇlis meghajtĂˇsĂş robot elmĂ©lete
"""
def get_robot_kinematics(w_L, w_R, config):
    v = ((w_L + w_R) / 2) * config.r_kerek
    w = ((w_R - w_L) / (2 * config.b)) * config.r_kerek
    return v, w

"""
AkadĂˇly osztĂˇly
"""
class Obstacle:
    def __init__(self, x, y, radius=0.1, vx=0.0, vy=0.0):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = vx  # sebessĂ©g x irĂˇnyban
        self.vy = vy  # sebessĂ©g y irĂˇnyban

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt


"""        
AkadĂˇlyok pĂ©ldĂˇnyosĂ­tĂˇsa
"""
obstacle_list = [
    
    Obstacle(1.5, 1.0, radius=0.4),
    Obstacle(2.5, 1.2, radius=0.4),
    Obstacle(3.5, 0.8, radius=0.4),
    Obstacle(2.0, 4.0, radius=0.4),
    Obstacle(3.0, 4.2, radius=0.4),
    Obstacle(4.0, 3.8, radius=0.4),
    Obstacle(5.0, 2.5, radius=0.6),
    Obstacle(2.5, -1.0, radius=0.3, vx=0.0, vy=0.3),
    Obstacle(5.0, 6.0, radius=0.25, vx=0.0, vy=-0.5),
    Obstacle(3.5, 2.8, radius=0.2, vx=0.6, vy=0.0),
    Obstacle(6.0, 1.5, radius=0.2, vx=-0.4, vy=0.1),
    Obstacle(1.2, 5.5, radius=0.15),
    Obstacle(6.8, 4.5, radius=0.2),
    Obstacle(7.2, 2.0, radius=0.15),
    
    ]
    
"""""
    Obstacle(0.6, 0.25, radius=0.15),
    Obstacle(1.5, 0.5, radius=0.15),  
    Obstacle(2.0, -0.2, radius=0.08),
    Obstacle(0.8, 1.2, radius=0.2),
    Obstacle(2.5, 1.0, radius=0.1),
    Obstacle(1.0, 2.5, radius=0.15),
    Obstacle(3.0, 0.5, radius=0.3),
    Obstacle(4.5, 1.5, radius=0.2),
    Obstacle(2.0, 3.5, radius=0.25),
    Obstacle(5.5, 3.5, radius=0.3),
    Obstacle(4.0, 4.5, radius=0.2),
    Obstacle(6.5, 2.0, radius=0.2),
    Obstacle(2.5, 1.5, 0.25, vx=0.2, vy=0.1),  # MozgĂł
    Obstacle(4.5, 1.5, 0.2, vx=-0.15, vy=0.3), # MozgĂł
    Obstacle(3.0, 3.0, 0.25, vx=0.3, vy=-0.2), # MozgĂł
    Obstacle(3.5, 0.0, radius=0.6, vx=0.0, vy=0.4)
    """


"""
CĂ©l kitĹ±zĂ©se
"""
class Goal:
    def __init__(self, x, y, tolerance=0.15):
        self.x = x
        self.y = y
        self.tolerance = tolerance

"""
KiszĂˇmĂ­tja a megtett utat az Ă­v mentĂ©n az elsĹ‘ ĂĽtkĂ¶zĂ©sig.
Ha nincs ĂĽtkĂ¶zĂ©s a predict_time alatt, egy nagy Ă©rtĂ©ket ad vissza.
"""
def get_dist_on_trajectory(state, config, w_L, w_R, obstacle_list):
    temp_robot = robotstate(x=state.x, y=state.y, irany=state.irany, w_L=state.w_L, w_R=state.w_R)
    accumulated_dist = 0.0
    v_actual, _ = get_robot_kinematics(w_L, w_R, config)
    
    # --- SZENZOR PARAMĂ‰TEREK ---
    max_sensor_dist = 3.0  # 3 mĂ©terig lĂˇt el a Lidar
    fov_angle = math.radians(180) # 180 fokos lĂˇtĂłszĂ¶g elĂ¶l
    
    for t in np.arange(0, config.predict_time, config.dt):
        for obs in obstacle_list:
            # 1. Szenzor szĹ±rĂ©s: Csak azt lĂˇtja, ami kĂ¶zel van
            dist_now = math.hypot(state.x - obs.x, state.y - obs.y)
            if dist_now > max_sensor_dist:
                continue
                
            # 2. FOV szĹ±rĂ©s: Csak azt lĂˇtja, ami elĹ‘tte van (+-90 fok)
            angle_to_obs = math.atan2(obs.y - state.y, obs.x - state.x)
            diff_angle = math.atan2(math.sin(angle_to_obs - state.irany), math.cos(angle_to_obs - state.irany))
            if abs(diff_angle) > fov_angle / 2:
                continue

            # 3. DINAMIKUS PREDIKCIĂ“: Hol lesz az akadĂˇly 't' idĹ‘ mĂşlva?
            obs_future_x = obs.x + obs.vx * t
            obs_future_y = obs.y + obs.vy * t
            
            dist_centers = math.hypot(temp_robot.x - obs_future_x, temp_robot.y - obs_future_y)
            
            if dist_centers <= (config.rob_radius + obs.radius + config.safety_margin):
                return accumulated_dist 
        
        update(temp_robot, config, w_L, w_R, config.dt)
        accumulated_dist += abs(v_actual) * config.dt
                
    return 10.0


#############xx FĂ‰KEZĂ‰SI FELTĂ‰TELEK ###############
def AdmissableVelocity(robotconfig, w_L, w_R, state, obstacle_list):
    """
    EllenĹ‘rzi, hogy a robot meg tud-e Ăˇllni az adott Ă­ven az ĂĽtkĂ¶zĂ©s elĹ‘tt.
    """
    # 1. KiszĂˇmĂ­tjuk a tĂˇvolsĂˇgot az Ă­v mentĂ©n az ĂĽtkĂ¶zĂ©sig
    dist_to_obs = get_dist_on_trajectory(state, robotconfig, w_L, w_R, obstacle_list)
    
    # 2. Megkapjuk a lineĂˇris sebessĂ©get (v)
    v, _ = get_robot_kinematics(w_L, w_R, robotconfig)
    
    #Ez a kĂ©plet le van vezetve --> admissable velocity lap
    if abs(v) <= math.sqrt(2 * robotconfig.a_max * dist_to_obs):
        return True
    return False
   
############################################################
"""#DifferenciĂˇlis meghajtĂˇsĂş robot esetĂ©n"""
class robotconfig:
    def __init__(robot):
        # feltĂ©telezem hogy a negativ Ă©s poziti sebessĂ©gek megegyeznek v_max = v_min Ă©s w_max=w_min --> ezeket kiszĂˇmolom a kerekek adataibol Ă©s a robot konfigurĂˇciĂłjĂˇbĂłl/ felĂ©pĂ­tĂ©sĂ©bĹ‘l
        robot.r_kerek = 0.033   #[m]
        robot.b = 0.08 #[m]
        robot.w_kerek_max = 15 #rad/s
        robot.a_max = 2 # [m/s^2] gyorsulĂˇs
       
        robot.w_kerek_min = -robot.w_kerek_max
       
        # FelbontĂˇsok a mintavĂ©telezĂ©shez (most a kerĂ©k szĂ¶gsebessĂ©gĂ©re vonatkozĂłan)
        robot.w_kerek_resolution = 1 # [rad/s] A kerĂ©k szĂ¶gsebessĂ©g mintavĂ©telezĂ©si finomsĂˇga.
       
        #DWA idĹ‘paramĂ©terek
        robot.dt = 0.1 # [s] --> idĹ‘lĂ©spĂ©s (felbontĂˇs)
        robot.predict_time = 3 # [s] --> mennyi idĹ‘re lĂˇsson elĹ‘re
   
        #robot-alakja--> legyen kĂ¶r az egyszerĹ±sĂ©g kedvĂ©Ă©rt
        robot.rob_radius = robot.b + 0.02 #[m]
        
        robot.safety_margin = 0.15
       
        ########OptimalizĂˇciĂł###########
       
        #G(v,w)= Alfa*heading(v,w)+Beta*dist(v,w)+Gamma*vel(v,w)
        robot.Alfa = 3  #cĂ©lra tarĂˇs sĂşlya  2
        robot.Beta = 3 # AkadĂˇly kerĂĽlĂ©s sĂşlya  2
        robot.Gamma = 7 #SebessĂ©g sĂşlya 5
       
"""
Robot jelenlegi ĂˇllapotĂˇnak eltĂˇrolĂˇsa
"""
class robotstate:
    def __init__(robot, x=0, y=0, v=0, w=0, irany = 0, w_L=0, w_R=0):  #default konstruktor
        robot.x = x
        robot.y = y
        robot.v = v
        robot.w = w
        robot.irany = irany
        robot.w_L = w_L
        robot.w_R = w_R

"""
Robot ĂˇllapotĂˇnak frissĂ­tĂ©se
"""
def update(robot, config, w_L_target, w_R_target, dt):
    # GyorsulĂˇs korlĂˇtozĂˇsa
    max_w_dot = config.a_max / config.r_kerek  # max kerĂ©k szĂ¶gsebessĂ©g vĂˇltozĂˇs
    
    # KorlĂˇtozzuk, hogy mennyit vĂˇltozhat a kerĂ©ksebessĂ©g ennyi idĹ‘ alatt
    w_L_new = robot.w_L + np.clip(w_L_target - robot.w_L, -max_w_dot * dt, max_w_dot * dt)
    w_R_new = robot.w_R + np.clip(w_R_target - robot.w_R, -max_w_dot * dt, max_w_dot * dt)
    
    # Most szĂˇmoljuk a kinematikĂˇt a KORLĂTOZOTT sebessĂ©ggel
    v, w = get_robot_kinematics(w_L_new, w_R_new, config)
    
    # PozĂ­ciĂł frissĂ­tĂ©s (ugyanaz, mint elĹ‘bb)
    theta_0 = robot.irany
    
    if(abs(w) > 1e-6):  # kis kĂĽszĂ¶b a nullĂˇhoz
        robot.x += (v/w) * (math.sin(theta_0 + w*dt) - math.sin(theta_0))
        robot.y += - (v/w) * (math.cos(theta_0 + w*dt) - math.cos(theta_0))
    else:
        robot.x += v * math.cos(theta_0) * dt
        robot.y += v * math.sin(theta_0) * dt
    
    robot.irany += w * dt
    robot.v = v
    robot.w = w
    robot.w_L = w_L_new
    robot.w_R = w_R_new
    
    return np.array([robot.x, robot.y, robot.irany, robot.v, robot.w, robot.w_L, robot.w_R])

"""        
Ă–sszes vĂˇlaszthatĂł v,w pĂˇr kiszĂˇmolĂˇsa kerekekbĹ‘l szĂˇmĂ­tva
"""
def pairstochoose (robotconfig, robotstate):

    w_dot_max = robotconfig.a_max / robotconfig.r_kerek         #w=a/r
   
    w_L_min_actual = max(robotconfig.w_kerek_min, robotstate.w_L - w_dot_max * robotconfig.dt)
    w_L_max_actual = min(robotconfig.w_kerek_max, robotstate.w_L + w_dot_max * robotconfig.dt)

    w_R_min_actual = max(robotconfig.w_kerek_min, robotstate.w_R - w_dot_max * robotconfig.dt)
    w_R_max_actual = min(robotconfig.w_kerek_max, robotstate.w_R + w_dot_max * robotconfig.dt)
   
    w_L_samples = np.arange(w_L_min_actual, w_L_max_actual + robotconfig.w_kerek_resolution, robotconfig.w_kerek_resolution)
    w_R_samples = np.arange(w_R_min_actual, w_R_max_actual + robotconfig.w_kerek_resolution, robotconfig.w_kerek_resolution)

    all_pairs = []
    for w_L in w_L_samples:
        for w_R in w_R_samples:
            v, w = get_robot_kinematics(w_L, w_R, robotconfig)

            all_pairs.append([v, w, w_L, w_R])
    return all_pairs

########################Ă–sszes lehetsĂ©ges vĂˇlazthatĂł pĂˇlya eltĂˇrolĂˇsa ami biztonsĂˇgos megĂˇllĂˇst biztosĂ­t, ez frissĂĽljĂ¶n minden egyes dĂ¶ntĂˇshozĂˇsnĂˇl#######################x

def safepairs (robotconfig, state, obstacle_list):
    w_dot_max = robotconfig.a_max / robotconfig.r_kerek
    
    # Dinamikus ablak kiszĂˇmĂ­tĂˇsa (mint a pairstochoose-ban)
    w_L_min_actual = max(robotconfig.w_kerek_min, state.w_L - w_dot_max * robotconfig.dt)
    w_L_max_actual = min(robotconfig.w_kerek_max, state.w_L + w_dot_max * robotconfig.dt)

    w_R_min_actual = max(robotconfig.w_kerek_min, state.w_R - w_dot_max * robotconfig.dt)
    w_R_max_actual = min(robotconfig.w_kerek_max, state.w_R + w_dot_max * robotconfig.dt)
    
    w_L_samples = np.arange(w_L_min_actual, w_L_max_actual + robotconfig.w_kerek_resolution, robotconfig.w_kerek_resolution)
    w_R_samples = np.arange(w_R_min_actual, w_R_max_actual + robotconfig.w_kerek_resolution, robotconfig.w_kerek_resolution)

    admissible_list = [] # Ebben csak a "jĂł" pĂˇrok lesznek
    
    for w_L in w_L_samples:
        for w_R in w_R_samples:
            if AdmissableVelocity(robotconfig, w_L, w_R, state, obstacle_list):
                v, w = get_robot_kinematics(w_L, w_R, robotconfig)
                admissible_list.append([v, w, w_L, w_R])
                
    return admissible_list

################################################

############# optimalizĂˇciĂł #####################
def optimisation(robotconfig, state, goal, obstacle_list):
    # 1. BiztonsĂˇgos sebessĂ©gpĂˇrok lekĂ©rĂ©se
    safe_list = safepairs(robotconfig, state, obstacle_list)
    
    # Ha nincs biztonsĂˇgos Ăşt (ĂśRES A LISTA -> DEADLOCK)
    if not safe_list:
        # Visszaadunk egy speciĂˇlis jelzĂ©st (None), hogy a fĹ‘ciklus tudja: Recovery kell
        return None, []

    best_score = -float('inf')
    best_pair = None
    
    dist_to_goal = math.hypot(goal.x - state.x, goal.y - state.y)
    v_max_robot = robotconfig.w_kerek_max * robotconfig.r_kerek
    
    # 2. AdaptĂ­v predikciĂł: kĂ¶zelebb rĂ¶videbb idĹ‘re nĂ©zĂĽnk elĹ‘re a precizitĂˇsĂ©rt
    adaptive_predict_time = robotconfig.predict_time
    if dist_to_goal < 1.0:
        adaptive_predict_time = max(0.5, dist_to_goal * 2.0)

    alfa = robotconfig.Alfa    # CĂ©lra tartĂˇs (pl. 2.0)
    beta = robotconfig.Beta    # AkadĂˇlykerĂĽlĂ©s (pl. 1.0)
    gamma = robotconfig.Gamma          # SebessĂ©gszabĂˇlyozĂˇs sĂşlya (magasabb, hogy hallgasson a lassĂ­tĂˇsra)

    for v, w, w_L, w_R in safe_list:  
        # Gyors szimulĂˇciĂł a jĂ¶vĹ‘beli Ăˇllapot becslĂ©sĂ©hez
        temp_robot = robotstate(x=state.x, y=state.y, irany=state.irany, w_L=state.w_L, w_R=state.w_R)
        for _ in np.arange(0, adaptive_predict_time, robotconfig.dt):
            update(temp_robot, robotconfig, w_L, w_R, robotconfig.dt)
        
        # --- PONTOZĂSI LOGIKA ---

        # A: Heading score (IrĂˇnyhiba normalizĂˇlva 0 Ă©s 1 kĂ¶zĂ©)
        angle_to_goal = math.atan2(goal.y - temp_robot.y, goal.x - temp_robot.x)
        error_angle = math.atan2(math.sin(angle_to_goal - temp_robot.irany), 
                                 math.cos(angle_to_goal - temp_robot.irany))
        score_heading = (math.pi - abs(error_angle)) / math.pi
        
        # B: Dist score (AkadĂˇlyoktĂłl valĂł tĂˇvolsĂˇg)
        score_dist = get_dist_on_trajectory(state, robotconfig, w_L, w_R, obstacle_list)
        
        # C: Velocity score (Folytonos lassulĂˇsi gĂ¶rbe)
        if dist_to_goal > 0.8:
            # Messze: egyszerĹ±en jutalmazzuk a sebessĂ©get (0.0 - 1.0)
            score_vel = v / v_max_robot
        else:
            # KĂ¶zel: v_target kĂ¶vetĂ©se. v_target = tĂˇvolsĂˇg (pl. 0.5m-nĂ©l 0.5m/s az ideĂˇlis)
            # A pontszĂˇm 1.0 ha tĂ¶kĂ©letesen tartja a lassulĂˇst, Ă©s csĂ¶kken ha eltĂ©r tĹ‘le.
            v_target = max(0.0, dist_to_goal) 
            score_vel = 1.0 - (abs(v_target - v) / v_max_robot)

        # VĂ©gsĹ‘ pontszĂˇm kiszĂˇmĂ­tĂˇsa
        score = (alfa * score_heading + 
                 beta * score_dist + 
                 gamma * score_vel)

        if score > best_score:
            best_score = score
            best_pair = [v, w, w_L, w_R]

    return best_pair, safe_list

"""
szimulĂˇciĂłs rĂ©sz
"""
def plot_all_trajectories(state, config, all_pairs, best_pair, goal, obstacles):
    # Ha sweep mĂłdban vagyunk, ne csinĂˇljon semmit
    if not plt.get_fignums(): 
        return
    
    plt.clf()
    ax = plt.gca()
    
    # BeĂˇllĂ­tjuk a keretet, hogy ne mozogjon a robot utĂˇn
    ax.set_xlim(-1.0, 8.5) 
    ax.set_ylim(-1.0, 6.5)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True, linestyle='--', alpha=0.5)

    # 1. CĂ©l Ă©s AkadĂˇlyok rajzolĂˇsa
    ax.plot(goal.x, goal.y, "gx", markersize=12, mew=3, label="CĂ©l")
    for obs in obstacles:
        ax.add_patch(plt.Circle((obs.x, obs.y), obs.radius, color="red", alpha=0.3))
    
    # 2. Ă–sszes lehetsĂ©ges pĂˇlya vĂ©gigpĂ¶rgetĂ©se
    for v, w, w_L, w_R in all_pairs:
        # PONTOS ELLENĹRZĂ‰S: Ez-e a kivĂˇlasztott legjobb pĂˇros?
        is_best = False
        if best_pair is not None:
            if math.isclose(w_L, best_pair[2], abs_tol=1e-3) and \
               math.isclose(w_R, best_pair[3], abs_tol=1e-3):
                is_best = True

        is_safe = AdmissableVelocity(config, w_L, w_R, state, obstacles)
        dist_to_coll = get_dist_on_trajectory(state, config, w_L, w_R, obstacles)
        
        # --- SZĂŤNMEGHATĂROZĂS ---
        if dist_to_coll < (abs(v) * config.predict_time) or not is_safe:
            path_color = "red"    # ĂśtkĂ¶zĂ©sveszĂ©ly = Piros
        elif is_best:
            path_color = "lime"   # VĂˇlasztott legjobb = Ă‰lĂ©nkzĂ¶ld
        elif v > 0:
            path_color = "gray"   # TĂ¶bbi biztonsĂˇgos elĹ‘re = SzĂĽrke (halvĂˇny)
        else:
            path_color = "blue"   # HĂˇtramenet = KĂ©k (ha v < 0)

        # MegjelenĂ­tĂ©si beĂˇllĂ­tĂˇsok: a legjobb Ăşt legyen legfelĂĽl Ă©s legvastagabb
        z_ord = 10 if is_best else 1
        alpha_val = 1.0 if is_best else 0.15
        lw_val = 3.5 if is_best else 0.8

        # --- JĂ“SOLT SZAKASZ (Trajectory rollout) ---
        ghost = robotstate(x=state.x, y=state.y, irany=state.irany, w_L=state.w_L, w_R=state.w_R)
        path_x, path_y = [ghost.x], [ghost.y]

        # PredikciĂłs szimulĂˇciĂł
        for _ in np.arange(0, config.predict_time, config.dt):
            update(ghost, config, w_L, w_R, config.dt)
            path_x.append(ghost.x)
            path_y.append(ghost.y)
        
        ax.plot(path_x, path_y, color=path_color, alpha=alpha_val, linewidth=lw_val, zorder=z_ord)

        # --- FĂ‰KEZĂ‰SI SZAKASZ (A vonalak vĂ©gĂ©n lĂ©vĹ‘ Ă­v) ---
        t_stop = abs(v) / config.a_max if abs(v) > 0 else 0
        brake_robot = robotstate(x=ghost.x, y=ghost.y, irany=ghost.irany, w_L=w_L, w_R=w_R)
        brake_x, brake_y = [brake_robot.x], [brake_robot.y]
        
        for t in np.arange(0, t_stop, config.dt):
            factor = max(0, 1.0 - (t / t_stop)) if t_stop > 0 else 0
            update(brake_robot, config, w_L * factor, w_R * factor, config.dt)
            brake_x.append(brake_robot.x)
            brake_y.append(brake_robot.y)
            
        # A fĂ©kezĂ©si szakasz mindig piros marad
        ax.plot(brake_x, brake_y, color="red", alpha=alpha_val * 0.7, linewidth=lw_val * 0.7, zorder=z_ord)

    # 3. A Robot Ă©s az aktuĂˇlis megtett Ăşt nyomvonala (trail) rajzolĂˇsa
    ax.add_patch(plt.Circle((state.x, state.y), config.rob_radius, color="blue", fill=False, lw=2))
    plt.arrow(state.x, state.y, config.rob_radius * math.cos(state.irany),
              config.rob_radius * math.sin(state.irany), head_width=0.05, fc='b', ec='b')

    plt.title(f"DWA SzimulĂˇciĂł - v: {state.v:.2f} m/s")
    plt.draw()
    plt.pause(0.01)
    

def start_original_simulation():
    conf = robotconfig()
    state = robotstate(x=0, y=0, irany=0, w_L=0, w_R=0)
    goal = Goal(x=7.0, y=5.0)
    
    plt.ion()
    plt.figure(figsize=(10, 8))

    # ĂllapotjelzĹ‘ a deadlockhoz
    is_recovering = False

    for step in range(1200): # Kicsit tĂ¶bb lĂ©pĂ©s, mert a forgĂˇs idĹ‘
        for obs in obstacle_list:
            obs.move(conf.dt)

        best, all_pairs = optimisation(conf, state, goal, obstacle_list)
        
        # --- DEADLOCK KEZELĂ‰S ---
        if best is None:
            is_recovering = True
            # ForgĂˇs egy helyben: ellentĂ©tes irĂˇnyĂş kerĂ©ksebessĂ©gek
            # A w_kerek_max felĂ©vel forgunk, hogy biztonsĂˇgos legyen
            recovery_w_L = -conf.w_kerek_max * 0.3
            recovery_w_R = conf.w_kerek_max * 0.3
            
            update(state, conf, recovery_w_L, recovery_w_R, conf.dt)
            print(f"LĂ©pĂ©s {step}: DEADLOCK! Helyben forgĂˇs...")
        else:
            is_recovering = False
            update(state, conf, best[2], best[3], conf.dt)

        # MegjelenĂ­tĂ©s
        if step % 3 == 0:
            # Ha recovery van, ĂĽres listĂˇt adunk a rajzolĂłnak
            plot_all_trajectories(state, conf, all_pairs if best else [], best, goal, obstacle_list)
        
        if math.hypot(state.x - goal.x, state.y - goal.y) < goal.tolerance:
            print("CĂ©lba Ă©rt!")
            break

    plt.ioff()
    plt.show()
    
##################xTĂBLĂZATOS############################

def run_single_test(a, b, g):
    """
    RĂ©szletes szimulĂˇciĂłs futĂˇs adathalĂˇszathoz.
    """
    conf = robotconfig()
    conf.Alfa = a
    conf.Beta = b
    conf.Gamma = g
    
    state = robotstate(x=0, y=0, irany=0, w_L=0, w_R=0)
    goal = Goal(x=7.0, y=5.0)
    
    # FrissĂ­tett akadĂˇlylista a standard teszthez
    current_obs_list = [
        
        Obstacle(1.5, 1.0, radius=0.4), Obstacle(2.5, 1.2, radius=0.4),
        Obstacle(3.5, 0.8, radius=0.4), Obstacle(2.0, 4.0, radius=0.4),
        Obstacle(3.0, 4.2, radius=0.4), Obstacle(4.0, 3.8, radius=0.4),
        Obstacle(5.0, 2.5, radius=0.6),
        Obstacle(2.5, -1.0, radius=0.3, vx=0.0, vy=0.3),
        Obstacle(5.0, 6.0, radius=0.25, vx=0.0, vy=-0.5),
        Obstacle(3.5, 2.8, radius=0.2, vx=0.6, vy=0.0)
        
    ]

    min_dist = float('inf')
    collision = False
    total_v = 0.0
    step_count = 0
    max_steps = 600 

    for step in range(max_steps):
        for obs in current_obs_list: obs.move(conf.dt)

        for obs in current_obs_list:
            d = math.hypot(state.x - obs.x, state.y - obs.y) - (conf.rob_radius + obs.radius)
            if d < min_dist: min_dist = d
            if d <= 0:
                collision = True
                break
        if collision: break

        best, _ = optimisation(conf, state, goal, current_obs_list)
        
        if best:
            update(state, conf, best[2], best[3], conf.dt)
        else:
            update(state, conf, 0, 0, conf.dt)
            
        total_v += state.v
        step_count = step
        
        if math.hypot(state.x - goal.x, state.y - goal.y) < goal.tolerance:
            avg_v = total_v / (step_count + 1)
            return [a, b, g, "SIKER", False, round(min_dist, 3), step_count, round(avg_v, 3)]

    avg_v = total_v / (step_count + 1) if step_count > 0 else 0
    eredmeny = "ĂśTKĂ–ZĂ‰S" if collision else "TIMEOUT"
    return [a, b, g, eredmeny, collision, round(min_dist, 3), step_count, round(avg_v, 3)]

def start_sweep():
    """
    ParamĂ©ter sweep 0-tĂłl 10-ig minden egĂ©sz Ă©rtĂ©kre.
    Ă–sszesen 11 * 11 * 11 = 1331 futtatĂˇs.
    """
    import numpy as np
    sweep_results = []
    
    # TartomĂˇny definiĂˇlĂˇsa (0, 1, 2 ... 10)
    vals = np.arange(0, 11, 1) 
    total_runs = len(vals)**3
    
    print(f"--- RĂ‰SZLETES SWEEP INDĂŤTĂSA ---")
    print(f"TartomĂˇny: 0-10 | KombinĂˇciĂłk: {total_runs}")
    print("Ez eltarthat egy ideig, kĂ©rlek vĂˇrj...")
    
    start_time = time.time()
    count = 0

    for a in vals:
        for b in vals:
            for g in vals:
                res = run_single_test(a, b, g)
                sweep_results.append(res)
                count += 1
                
                # HaladĂˇsi naplĂł minden 50. futĂˇs utĂˇn
                if count % 50 == 0:
                    percent = round((count / total_runs) * 100, 1)
                    print(f"HaladĂˇs: {percent}% ({count}/{total_runs})")

    # TĂˇblĂˇzat Ă¶sszeĂˇllĂ­tĂˇsa
    columns = ["Alpha", "Beta", "Gamma", "EredmĂ©ny", "ĂśtkĂ¶zĂ©s", "Min_TĂˇvolsĂˇg", "LĂ©pĂ©sszĂˇm", "Ătlag_SebessĂ©g"]
    df = pd.DataFrame(sweep_results, columns=columns)
    
    # FĂˇjl mentĂ©se (letĂ¶lthetĹ‘ CSV)
    filename = "dwa_sweep_eredmenyek_10.csv"
    df.to_csv(filename, index=False)
    
    total_duration = round((time.time() - start_time) / 60, 2)
    print(f"\n--- SWEEP KĂ‰SZ ---")
    print(f"FutĂˇsi idĹ‘: {total_duration} perc")
    print(f"FĂˇjl elmentve: {filename}")
    
    # Megmutatjuk a legjobb 10 sikeres futamot sebessĂ©g szerint rendezve
    print("\nLegjobb 10 konfigurĂˇciĂł (Sikeres, leggyorsabb szerint):")
    success_df = df[df["EredmĂ©ny"] == "SIKER"].sort_values(by="LĂ©pĂ©sszĂˇm", ascending=True)
    print(success_df.head(10).to_string(index=False))


# --- INNEN TUDSZ VĂLTANI ---
if __name__ == "__main__":
    # 1. SWEEP MĂ“D (tĂˇblĂˇzat):
    #start_sweep()

    # 2. EREDETI MĂ“D (grafika) - Ha ezt akarod, vedd ki a '#' jelet alĂłla:
    start_original_simulation()
```

### Önlab/ros2_ws/frames_2026-04-27_18.43.46.gv

```
digraph G {
"base_footprint" -> "base_link"[label=" Broadcaster: default_authority\nAverage rate: 10000.0\nBuffer length: 0.0\nMost recent transform: 0.0\nOldest transform: 0.0\n"];
"odom" -> "base_footprint"[label=" Broadcaster: default_authority\nAverage rate: 51.25\nBuffer length: 0.8\nMost recent transform: 33.22\nOldest transform: 32.42\n"];
"base_footprint" -> "base_scan"[label=" Broadcaster: default_authority\nAverage rate: 10000.0\nBuffer length: 0.0\nMost recent transform: 0.0\nOldest transform: 0.0\n"];
"map" -> "odom"[label=" Broadcaster: default_authority\nAverage rate: 11.111\nBuffer length: 0.9\nMost recent transform: 33.3\nOldest transform: 32.4\n"];
edge [style=invis];
 subgraph cluster_legend { style=bold; color=black; label ="view_frames Result";
"Recorded at time: 1777308226.179179"[ shape=plaintext ] ;
}->"map";
}
```

### Önlab/ros2_ws/readme.txt

```
# --- TERMINĂL 1: Gazebo ---
export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:/opt/ros/jazzy/share/turtlebot3_gazebo/models
export LIBGL_ALWAYS_SOFTWARE=1
gz sim -v 4 ~/ros2_ws/src/my_gazebo_worlds/worlds/dwa_test.sdf

# --- TERMINĂL 2: Bridge + DWA (launch fĂˇjllal) ---
cd ~/ros2_ws
source install/setup.bash
ros2 launch dwa_planner dwa_launch.py

# --- TERMINĂL 3: SLAM Toolbox ---
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=True

# --- TERMINĂL 4: RViz2 ---
rviz2


đźŽŻ RViz beĂˇllĂ­tĂˇsok (egyszer elĂ©g elmenteni):
ĂllĂ­tsd be a Fixed Frame-et map-re

Add hozzĂˇ a Map display-t (/map topic)

Add hozzĂˇ a TF display-t
```

### Önlab/ros2_ws/src/dwa_planner/dwa_planner/__init__.py

```python
```

### Önlab/ros2_ws/src/dwa_planner/dwa_planner/dwa_node.py

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, PoseStamped
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import math
import numpy as np
from tf2_ros import TransformListener, Buffer
from tf2_geometry_msgs import do_transform_point
from geometry_msgs.msg import PointStamped

class DWANode(Node):
    def __init__(self):
        super().__init__('dwa_node')
        # PublikĂˇlĂłk
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.filtered_scan_pub = self.create_publisher(LaserScan, '/scan_filtered', 10)

        # FeliratkozĂłk
        self.create_subscription(LaserScan, '/scan', self.scan_cb, 10)
        self.create_subscription(Odometry, '/odom', self.odom_cb, 10)
        self.create_subscription(PoseStamped, '/goal_pose', self.goal_cb, 10)
        
        self.x, self.y, self.yaw = 0.0, 0.0, 0.0
        self.obstacles = []
        self.goal_x, self.goal_y = None, None
        
        # TF2 a SLAM-hez
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.map_x, self.map_y, self.map_yaw = 0.0, 0.0, 0.0
        self.use_slam = False
        
        # Timer-ek
        self.create_timer(0.05, self.update_robot_pose)
        self.create_timer(0.1, self.control_loop)
        
        self.get_logger().info("--- DWA NODE ELINDULT ---")

    def update_robot_pose(self):
        """LekĂ©ri a robot pozĂ­ciĂłjĂˇt a map keretben (SLAM-tĂłl)"""
        try:
            # EllenĹ‘rizzĂĽk, hogy lĂ©tezik-e a transzformĂˇciĂł
            if self.tf_buffer.can_transform('map', 'base_footprint', rclpy.time.Time()):
                transform = self.tf_buffer.lookup_transform('map', 'base_footprint', rclpy.time.Time())
                self.map_x = transform.transform.translation.x
                self.map_y = transform.transform.translation.y
                q = transform.transform.rotation
                self.map_yaw = math.atan2(2*(q.w*q.z + q.x*q.y), 1-2*(q.y*q.y + q.z*q.z))
                self.use_slam = True
            else:
                self.use_slam = False
        except Exception as e:
            self.use_slam = False
            pass

    def goal_cb(self, msg):
        self.goal_x, self.goal_y = msg.pose.position.x, msg.pose.position.y
        self.get_logger().info(f'Ăšj cĂ©l: ({self.goal_x}, {self.goal_y})')

    def odom_cb(self, msg):
        self.x, self.y = msg.pose.pose.position.x, msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        self.yaw = math.atan2(2*(q.w*q.z + q.x*q.y), 1-2*(q.y*q.y + q.z*q.z))

    def scan_cb(self, msg):
        self.obstacles = []
        filtered_msg = msg
        new_ranges = list(msg.ranges)

        for i, r in enumerate(new_ranges):
            if 0.25 < r < 3.0 and not math.isinf(r):
                # A DWA belsĹ‘ szĂˇmĂ­tĂˇsĂˇhoz az akadĂˇlyokat a robot aktuĂˇlis pozĂ­ciĂłjĂˇhoz viszonyĂ­tva tĂˇroljuk
                angle = msg.angle_min + i * msg.angle_increment + self.yaw
                ox = self.x + r * math.cos(angle)
                oy = self.y + r * math.sin(angle)
                self.obstacles.append([ox, oy])
            else:
                new_ranges[i] = float('inf')

        filtered_msg.ranges = new_ranges
        self.filtered_scan_pub.publish(filtered_msg)

    def control_loop(self):
        if self.goal_x is None: 
            return
        
        # HasznĂˇljuk a SLAM pozĂ­ciĂłt, ha van
        if self.use_slam:
            current_x = self.map_x
            current_y = self.map_y
            current_yaw = self.map_yaw
        else:
            current_x = self.x
            current_y = self.y
            current_yaw = self.yaw
        
        dist_to_goal = math.hypot(self.goal_x - current_x, self.goal_y - current_y)
        if dist_to_goal < 0.2:
            self.cmd_pub.publish(Twist())
            self.goal_x = None
            self.get_logger().info("CELBA ERTEM!")
            return

        best_v, best_w, max_score = 0.0, 0.0, -1e9
        
        for v in [0.2, 0.3]:  # TĂ¶bb sebessĂ©g opciĂł
            for w in np.linspace(-0.8, 0.8, 11):
                new_yaw = current_yaw + w * 1.0
                px = current_x + v * math.cos(new_yaw) * 1.0
                py = current_y + v * math.sin(new_yaw) * 1.0
                
                safe = True
                for ox, oy in self.obstacles:
                    if math.hypot(px - ox, py - oy) < 0.4:
                        safe = False
                        break
                
                if safe:
                    score = -math.hypot(self.goal_x - px, self.goal_y - py)
                    if score > max_score:
                        max_score, best_v, best_w = score, v, w

        msg = Twist()
        msg.linear.x = float(best_v)
        msg.angular.z = float(best_w)
        self.cmd_pub.publish(msg)

def main():
    rclpy.init()
    rclpy.spin(DWANode())
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Önlab/ros2_ws/src/dwa_planner/launch/dwa_launch.py

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=[
                '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
                '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
                '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
                '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
                '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V'
            ],
            parameters=[{'use_sim_time': True}],
        ),
        Node(
            package='dwa_planner',
            executable='dwa_node',
            parameters=[{'use_sim_time': True}],
        ),
    ])
```

### Önlab/ros2_ws/src/dwa_planner/package.xml

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>dwa_planner</name>
  <version>0.0.0</version>
  <description>TODO: Package description</description>
  <maintainer email="rumdaniel@todo.todo">rumdaniel</maintainer>
  <license>TODO: License declaration</license>
	<depend>visualization_msgs</depend>
  <depend>rclpy</depend>
  <depend>geometry_msgs</depend>
  <depend>nav_msgs</depend>
  <depend>tf2_ros</depend>
  <depend>tf2</depend>
  <depend>tf2_geometry_msgs</depend>

  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
```

### Önlab/ros2_ws/src/dwa_planner/setup.py

```python
from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'dwa_planner'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'dwa_node = dwa_planner.dwa_node:main'
        ],
    },
)
```

### Önlab/ros2_ws/src/my_gazebo_worlds/worlds/dwa_test.sdf

```xml
<?xml version="1.0" ?>
<sdf version="1.8">
    <world name="dwa_world">
        <physics name="1ms" type="ignored">
            <max_step_size>0.001</max_step_size>
        </physics>
        <plugin filename="gz-sim-physics-system" name="gz::sim::systems::Physics"/>
        <plugin filename="gz-sim-sensors-system" name="gz::sim::systems::Sensors">
            <render_engine>ogre2</render_engine>
        </plugin>
        <plugin filename="gz-sim-user-commands-system" name="gz::sim::systems::UserCommands"/>
        <plugin filename="gz-sim-scene-broadcaster-system" name="gz::sim::systems::SceneBroadcaster"/>

        <light type="directional" name="sun">
            <cast_shadows>true</cast_shadows>
            <pose>0 0 10 0 0 0</pose>
            <direction>-0.5 0.1 -0.9</direction>
        </light>

        <model name="ground_plane">
            <static>true</static>
            <link name="link">
                <collision name="c">
                    <geometry><plane><normal>0 0 1</normal></plane></geometry>
                </collision>
                <visual name="v">
                    <geometry><plane><normal>0 0 1</normal></plane></geometry>
                    <material><ambient>0.8 0.8 0.8 1</ambient><diffuse>0.8 0.8 0.8 1</diffuse></material>
                </visual>
            </link>
        </model>

        <model name="obs1">
            <pose>2.0 0.5 0.5 0 0 0</pose>
            <link name="l">
                <collision name="c"><geometry><box><size>0.5 0.5 1</size></box></geometry></collision>
                <visual name="v"><geometry><box><size>0.5 0.5 1</size></box></geometry></visual>
            </link>
        </model>

        <model name="obs2">
            <pose>3.5 -0.5 0.5 0 0 0</pose>
            <link name="l">
                <collision name="c"><geometry><box><size>0.5 0.5 1</size></box></geometry></collision>
                <visual name="v"><geometry><box><size>0.5 0.5 1</size></box></geometry></visual>
            </link>
        </model>

        <include>
            <uri>model://turtlebot3_waffle</uri>
            <name>turtlebot3_waffle</name>
            <pose>0 0 0.05 0 0 0</pose> </include>
    </world>
</sdf>
```

### tf2_frames_latest.gv

```
digraph G {
"odom" -> "base_link"[label=" Broadcaster: default_authority\nAverage rate: 50.82\nBuffer length: 1.22\nMost recent transform: 88.42\nOldest transform: 87.2\n"];
"base_link" -> "base_scan"[label=" Broadcaster: default_authority\nAverage rate: 50.833\nBuffer length: 1.2\nMost recent transform: 88.4\nOldest transform: 87.2\n"];
edge [style=invis];
 subgraph cluster_legend { style=bold; color=black; label ="view_frames Result";
"Recorded at time: 1793288203.5363119"[ shape=plaintext ] ;
}->"odom";
}
```

## Aktualis AI-kezatadas - 2026-11-01

Ez a fejezet a jelenlegi ROS 2 Jazzy + Gazebo Sim projekt aktualis allapota.
Masik AI-nak ezt a fejezetet es a felsorolt forrasfajlokat add at; a regi,
beagyazott fajlmasolatokat ne tekintse automatikusan frissebbnek.

### Projekt

- Workspace: `codes_diploma/ros2_astar_dwa_gazebo`
- ROS: Jazzy
- Gazebo Sim: 8.10.0
- Robot: TurtleBot3 Waffle
- A projekt WSL2 Ubuntu alatt fut.
- A fo szimulacio egy launchbol inditja a Gazebo-t, a bridge-et, az A* + DWA
  node-ot es a mozgo akadaly node-ot.

### Aktualis, ellenorzott fajlok

- `src/astar_dwa_controller/src/astar_dwa_node.cpp`
- `src/astar_dwa_controller/config/rosbot.yaml`
- `src/astar_dwa_controller/launch/controller.launch.py`
- `src/dwa_gazebo_sim/launch/simulation.launch.py`
- `src/dwa_gazebo_sim/launch/bridge_and_controller.launch.py`
- `src/dwa_gazebo_sim/launch/visualization.launch.py`
- `src/dwa_gazebo_sim/worlds/dwa_world.sdf`
- `src/dwa_gazebo_sim/setup.py`
- `README.md`

### Elvegzett kodjavitasok

1. Az A* `cost` es `parent` tombjei `width * height` meretuak. A regi
    `width * width` foglalas nem maradhat vissza.
2. A LiDAR sajat roboton beluli pontjai ki vannak szurve. Ha nincs DWA-jelolt,
    a node biztonsagos, lassu elorehaladassal probalja feloldani a teves
    deadlockot; valos akadaly eseten forgasi fallback marad.
3. A nyers Gazebo `/odom` lokalis koordinata. A node egyszer hozzaadja a
    `rosbot.yaml` `initial_pose_x/y = 0.8` offsetjet, igy az A* es a vilagban
    megadott cel/akadaly koordinatak egy rendszerben vannak.
4. A statikus falpontok a `rosbot.yaml` fajlban az SDF falak 0.2 m-es mintai.
5. A controller, bridge es RViz hasznalja a `use_sim_time: true` parametert.
6. A fo Gazebo launch kozvetlenul a `gz sim` binarist inditja, nem a
    `gz_sim.launch.py` wrappert. A mukodo forma:
    `gz sim -v 4 -r <dwa_world.sdf>`.
7. Az `AI_KODCSOMAG.md` nem helyettesiti a tenyleges forrasfajlokat. Minden
    kodkovetkeztetest a fenti aktualis fajlokbol kell ellenorizni.

### Aktualitasan igazolt mukodes

- A tiszta build sikeres:
  `colcon build --symlink-install --packages-up-to dwa_gazebo_sim`
- Az `/odom` publisher megjelent a koordinata-javitas utan.
- A `/goal_pose` cel bejutott az A* + DWA node-ba.
- Az A* utvonal letrejott, peldaul `ut=28 pont`.
- A DWA sebessegparancsot adott, peldaul `cmd=(0.31, 0.21)`.
- A `/cmd_vel` bridge a Gazebo fele csatlakozik.
- RViz topicok: `/odom`, `/scan`, `/astar_path`, `/astar_map`,
  `/astar_dwa_markers`, `/goal_pose`.

### Ismert koordinata-megjelenitesi kockazat

Az RViz nyers `Odometry` display-je a Gazebo lokalis `/odom` uzenetet mutatja,
mig az A* terkep es a statikus markerek a kezdopozicio-offsettel korrigalt
vilagkoordinatat hasznaljak. Ha RViz-ben ket eltolodott reteget latni, a nyers
`Odometry` display-t kapcsold ki, a Fixed Frame maradjon `odom`. A TF es az A*
marker koordinatait ezutan kell veglegesiteni, nem ujabb offset hozzaadasaval.

### Masolhato feladatprompt masik AI-nak

```text
Egy ROS 2 Jazzy + Gazebo Sim 8.10 projektet kell folytatnod WSL2 Ubuntu alatt.
A projekt TurtleBot3 Waffle robotot, C++ A* globalis es DWA lokalis tervezot
hasznal. A fo workspace:
codes_diploma/ros2_astar_dwa_gazebo

Eloszor olvasd el a tenyleges aktualis fajlokat:
src/astar_dwa_controller/src/astar_dwa_node.cpp
src/astar_dwa_controller/config/rosbot.yaml
src/astar_dwa_controller/launch/controller.launch.py
src/dwa_gazebo_sim/launch/simulation.launch.py
src/dwa_gazebo_sim/launch/bridge_and_controller.launch.py
src/dwa_gazebo_sim/launch/visualization.launch.py
src/dwa_gazebo_sim/worlds/dwa_world.sdf
README.md

Ne a regi AI_KODCSOMAG.md-beagyazott kodmasolatbol kovetkeztess, hanem a
tenyleges forrasokat ellenorizd.

A mar kijavitott hibak:
- A* cost es parent tomb merete width * height.
- LiDAR sajat roboton beluli pontjai szurve vannak.
- DWA deadlock esetere lassu, biztonsagos elorehaladasi fallback van.
- A nyers Gazebo odom lokalis, ezert az initial_pose_x/y egyszeri offsetkent
  kerul a belso vilagkoordinataba.
- A statikus falpontok a SDF falak 0.2 m-es mintai.
- use_sim_time minden erintett ROS node-on true.
- A fo launch kozvetlen gz sim folyamatot indit.

Aktualis ellenorzes:
colcon build --symlink-install --packages-up-to dwa_gazebo_sim

Inditas Terminal 1-ben:
source /opt/ros/jazzy/setup.bash
export TURTLEBOT3_MODEL=waffle
export DISPLAY=:0
export XDG_RUNTIME_DIR=/tmp/gazebo-runtime
mkdir -p "$XDG_RUNTIME_DIR"
chmod 700 "$XDG_RUNTIME_DIR"
cd "/mnt/c/Users/Rum Dániel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo"
source install/setup.bash
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
ros2 launch dwa_gazebo_sim simulation.launch.py software_rendering:=true

Inditas Terminal 2-ben:
source /opt/ros/jazzy/setup.bash
export DISPLAY=:0
export XDG_RUNTIME_DIR=/tmp/gazebo-runtime
mkdir -p "$XDG_RUNTIME_DIR"
chmod 700 "$XDG_RUNTIME_DIR"
export QT_QPA_PLATFORM=xcb
export QT_X11_NO_MITSHM=1
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
cd "/mnt/c/Users/Rum Dániel/Desktop/Diplomamunka/codes_diploma/ros2_astar_dwa_gazebo"
source install/setup.bash
ros2 launch dwa_gazebo_sim visualization.launch.py

Nyitott feladat:
Vizsgald meg az RViz-ben, hogy a nyers /odom Odometry display okoz-e masodik,
eltolt koordinatareteget. A static map, A* path es marker frame jelenleg odom.
Ne adj ujabb offsetet addig, amig a nyers odom, TF, OccupancyGrid es MarkerArray
frame-je nincs egyutt ellenorizve.
``` 

### Legujabb allapot - DWA res elotti megtorpanas

2026-11-02-en a C++ `astar_dwa_node.cpp`-ben eltavolitasra kerult a kulon
`heading_error > 0.6` ag, amely teljesen nullazta a linearis sebesseget, ha a
robot az elso res elott iranyt akart valtani. A DWA sajat heading-score-ja,
trajektoria-predikcioja es akadalyellenorzese dont most a lassu, ivben torteno
befordulasrol.

Az RViz nyers `Odometry` display-e alapbol kikapcsolt allapotba kerult, mert a
lokalis Gazebo odometria es a vilagkoordinatas statikus A* retegek egyutt egy
eltolodott trailszeru megjelenitest okoztak.

Ellenorzott tesztlog:

```text
DWA jeloltek: teszt=169, sebesseg=123, hatar=0, akadaly=0,
fekezes=0, elfogadott=igen
Frontier vezerles: waypoint=(1.20, 1.20), cmd=(0.15, 0.62)
Frontier vezerles: waypoint=(1.60, 1.60), cmd=(0.32, 0.21)
```

Ez igazolja, hogy a robot az elso waypoint fele elorehaladva fordul, nem a
regi teljes megallasi agban varakozik.

A legujabb DWA-javitas az `obstacles()` fuggvenyben kiszuri a LiDAR-pontokat,
ha azok a `planning_obstacles()` statikus falpontjainak `resolution` tavolsagan
belul vannak. Az A* tovabbra is hasznalja a statikus falterkepeket, de a DWA
nem kezeli ugyanazt a falat masodik, dinamikus akadalykent.

### Python es C++ modell kapcsolata

A C++ ROS 2 node ugyanazokat az alapelveket hasznalja, mint az `Onlab/DWA_py.py`:
differencialis kerekkinematika, gyorsulaskorlatozas, trajektoria-predikcio,
megallhatosagi feltetel es heading/tavolsag/sebesseg pontozas. Nem azonos
program es nem azonos parameterekkel fut: elter a robot sugar, a `predict_time`,
a DWA-sulyok es az akadalylista forrasa. A C++ valtozat a Gazebo `/scan` es
`/odom` adatait hasznalja, a Python valtozat sajat szimulalt akadalylistat.

### Legujabb frissites - biztonsagosabb globalis utvonal es RViz

- Az A* inflacio most `robot_radius + obstacle.radius + safety_margin`.
- A `/astar_map` es az RViz biztonsagi markerek ugyanazt a megnovelt
    inflacios sugarat mutatjak.
- A DWA LiDAR-szures a statikus falakat nem kezeli ujra dinamikus akadalykent.
- A DWA waypoint-eloreneyezese `0.5 m` helyett `0.35 m`, hogy ne vagja le az
    A* biztonsagos kanyarjait a szuk res elott.
- RViz-ben alapbol ki van kapcsolva a statikus `/astar_map`, a statikus
    MarkerArray es a nyers Odometry trail. A LiDAR marad aktiv, a nezeti cel a
    `base_link`, a TopDownOrtho skala `3.5`.

Az utolso C++ build sikeres:

```text
colcon build --symlink-install --packages-select astar_dwa_controller
```

### Legujabb A* LiDAR-frissites

Az A* statikus inflacioja a falak sarkainak nagyobb tavolsagara `+0.35 m`
extra biztonsagi erteket hasznal. Ez a frissites a zold globalis utvonalat
nemcsak a falak oldalatol, hanem a sarkoktol is tavolabb tartja.

Az `astar()` keresesi akadalylistaja most egyesiti a `planning_obstacles()`
statikus akadalyait es a control ciklus aktualis `sensed_obstacles` LiDAR-
pontjait. Az A* igy az ujratervezeskor nemcsak a kezdeti statikus terkepet,
hanem a friss szenzoros akadalyhelyzetet is blokkolt cellakkal kezeli.

### Aktualis A* + DWA szetvalasztas

Az A* statikus `planning_obstacles()` alapjan dolgozik; a LiDAR-pontok nem
modositjak a globalis racsterkepe. A `control()` az A* utvonal aktualis
waypoint-indexet Python-szeruen kezeli: 0,20 m-es tolerancia vagy a ponton valo
atadas utan lep tovabb, majd az A* lokalis erintoiranyaba ad celpontot a DWA-nak.
Igy a DWA az `alpha_` heading-pontozassal a zold utvonal iranyat koveti, mikozben
a mozgo akadalyakat a LiDAR-alapu lokaliz biztonsagi ellenorzes kezeli.

### Mozgo akadaly biztonsagi javitas

Az `obstacles()` most nem szuri ki automatikusan a statikus falak kornyezetebe
eso LiDAR-pontokat. Ez szukseges, mert a fal mellett halado mozgó henger pontjai
korabban eltuntek a DWA bemenetebol, es a robot nem reagalt rajuk. Az A* tovabbra
is csak a statikus `planning_obstacles()` terkepet hasznalja; a DWA minden
ervenyes LiDAR-pontot lokalis akadalykent ellenoriz.

A legujabb minimalis javitas az `obstacles()` fuggvenyben csak a statikus
falpontok kozvetlen, `static_obstacle.radius + 0.12 m` kornyezetet szuri ki.
A falaktol tavolabbi LiDAR-pontok, igy a mozgó akadalyak, megmaradnak a DWA
szamara.

### Legujabb DWA-menekulesi frissites

- Az `obstacles()` LiDAR-szures kozeli hatara `0.12 m`, igy a mozgó akadaly
    kozeli pontjai nem vesznek el.
- A `dwa()` az utkozesnel mindig figyelembe veszi a
    `robot_radius + safety_margin` biztonsagi tavolsagot.
- Ha nincs biztonsagos eloremeno jelolt, a robot eloszor lassu, `0.04 m/s`
    hatramenetet probal, majd legalabb `0.5 * max_angular_velocity` helyben
    fordulasi korrekciot ad.
- Az A* ujratervezesi es `control()` logikahoz ebben a frissitesben nem
    nyultunk.

A jelenlegi C++ fajl diagnosztikaja hibamentes.

### 2026-11-03 ellenorzott friss runtime

Friss inditas utan egyetlen fo launch futott:

- egy Gazebo szerver es egy Gazebo GUI;
- egy `parameter_bridge`;
- egy `astar_dwa_node`;
- egy `moving_obstacle` node.

Az ellenorzott topic-allapot:

```text
/odom: Publisher count: 1, Subscription count: 1
/scan: Publisher count: 1, Subscription count: 1
/astar_path: aktiv
```

A tesztcel `(6.5, 4.2)` volt az `odom`-hoz igazított vilagkoordinataban. A robot
az elso szakaszokon `0.38 m/s` koruli sebesseggel haladt, majd az utolso minta
szerint a Gazebo lokalıs odometriaja `(5.423, 3.308)` volt. A vezerlo ehhez
hozzaadja az `(0.8, 0.8)` kezdopozicio-offsetet, ezert a vezerlesi koordinata
`(6.223, 4.108)` lett. Ez a celhoz korulbelul `0.29 m` tavolsag, igy a jelenlegi
`0.30 m` cel-tolerancia alapjan a vezerlo helyesen nullazta a sebesseget.

A futas kozben a DWA kezdeti diagnosztikaja `akadaly=0`, `hatar=0`,
`elfogadott=igen` volt. A cel elotti megallast nem masodik Gazebo-peldany,
dupla `/odom`, vagy A*-utvonalhiany okozta; a vegso megallas a vezerloben
definialt cel-tolerancia kovetkezmenye. A `debug_path` Gazebo-modell letrehozasa
is lefutott; az elso eltavolıtasi kiserletnel megjeleno "entity not found" uzenet
csak azt jelezte, hogy korabbi debug-modell meg nem letezett.

Az ellenorzeshez hasznalt fo parancsok:

```bash
colcon build --symlink-install --packages-select astar_dwa_controller
ros2 launch dwa_gazebo_sim simulation.launch.py software_rendering:=true
ros2 topic info /odom
ros2 topic info /scan
ros2 topic echo /odom --once
```

A forrasdiagnosztika tovabbra is hibamentes. A C++ fordítás a Windows-meghajton
lassan fejezodott be, ezert a futtatas soran kulonosen fontos volt a binaris
es a launch egyetlen peldanyanak ellenorzese.

### 2026-11-03 dinamikus akadaly- es gridellenorzes

A `moving_obstacle_node.py` cel-elofizetese `Pose` tipusrol `PoseStamped` tipusra
lett javitva, mert a `/goal_pose` topic tenylegesen `geometry_msgs/msg/PoseStamped`
uzenetet kuld. A node igy csak a cel uzenet utan es a `/sim_active=true` jelzes
utan novelheti a `self.time` erteket.

A javitott futasban az A* `resolution=0.20 m` mellett `41 x 26` cellas racson
40 pontos utvonalat talalt. Ez nem tul nagy grid, ezert a felbontas durvitasat
nem alkalmaztuk: a nagyobb cella a statikus falsarkok korul kevesebb geometriai
pontossagot adna. A robot a `6.30, 2.50` waypointig eljutott; a vegso saroknal
a DWA diagnosztikaja `akadaly=53-54` volt, tehat a fennmarado elakadas lokalis
LiDAR-ellenorzes, nem A*-utvonalhiany.

### 2026-11-03 DWA+A waypoint- és célkövetési frissítés

Az `astar_dwa_node.cpp` most tartós `current_path_`, `waypoint_index_` és
`need_replan_` tagokat használ. Az A* csak új cél vagy üres útvonal esetén fut
újra, a kezdő blokkolt cellát pedig a keresés előtt felszabadítja. A waypoint-
követés a Python `DWA+A.py` logikájához igazodva legfeljebb nyolc ponton belül
keresi a legközelebbi előrehaladást, majd `0.45 m` összegzett ívhossz alapján
választ lookahead célpontot. A helyben forgatás küszöbe `0.85` radián.

Az aktuális `rosbot.yaml` `robot_radius=0.22` és `safety_margin=0.08` értékeket
használ; a C++ hardcoded biztonsági margó-felülírása megszűnt.

### 2026-11-03 dinamikus LiDAR-regresszió javítása

A DWA lokális `obstacles()` feldolgozása többé nem dobja el a statikus falak
környezetében mért LiDAR-pontokat. A korábbi geometriai közelség alapú szűrés
a fal mellett haladó mozgó akadály pontjait is eltávolíthatta, ezért a DWA nem
látta időben a hengert. A globális A* továbbra is kizárólag a YAML ismert
statikus akadályait használja; a lokális DWA minden érvényes LiDAR-pontot a
clearance-vizsgálatba ad.

A mozgó akadályok helyzete és sebessége nincs hardcode-olva a C++ vezérlőben
vagy a YAML-ben. A DWA a mozgó akadályokat ugyanúgy a valós szenzoros adatból
kezeli, mint bármely más lokális akadályt; a predikció kizárólag az aktuális
LiDAR-bemenetre támaszkodhat.

A Gazebo `debug_path` modellje csak vizuális elemeket tartalmaz, collision elemet
nem, ezért a waypoint-gömbök nem lehetnek LiDAR-akadályok. A DWA LiDAR-feldolgozása
most csak a statikus fal közvetlen visszaverődési pontjait szűri ki
`static_radius + 0.05 m` távolságon belül; a fal mellett mozgó akadályok pontjai
megmaradnak a lokális akadályvizsgálathoz.

### 2026-11-03 szembejövő akadály kikerülése

A DWA most külön kezeli az ütközésig megtett ívhosszt és az oldaltávolságot.
Az oldaltávolság csak a pályák pontozásában szerepel, ezért egy biztonságos,
akadálytól oldalra ívelő pálya nem kerül elutasításra pusztán a clearance miatt.
Ha minden jelölt ív blokkolt és a legközelebbi akadály szemből érkezik, a vezérlő
nem álló helyben várakozik, hanem `0.08 m/s` előremenettel az akadálytól elfelé
fordul. A `control()` csak akkor enged helyben forgatást, ha a legközelebbi
LiDAR-akadály távolabb van `0.85 m`-nél és a heading hiba legalább `0.95 rad`.

### 2026-11-03 RViz-célküldéses indulás

Az `astar_dwa_controller/config/rosbot.yaml` alapértelmezett célkoordinátái
`goal_x=0.0` és `goal_y=0.0`. A node ezért induláskor nem állítja be a
`has_goal_` állapotot, hanem nullás sebességgel várakozik. A mozgás csak az
RViz-ből érkező `2D Goal Pose` `/goal_pose` üzenet után indul.

### Gazebo 3D A* debug-path vizualizacio

A C++ `astar_dwa_node` most a friss A* utvonalbol egyetlen `debug_path` Gazebo
modellt spawnol: a ritkitott utvonal kek, a waypointok zold, es csak
`<visual>` elemeket tartalmaz, collision nelkul. Ezert a Gazebo-ban lathato
utvonal nem valik LiDAR-akadallya.

### Kovetkezo runtime teszt - bal also sarok

Biztonsagos bal also sarok cel az `odom` keretben:

```bash
ros2 topic pub --once /goal_pose geometry_msgs/msg/PoseStamped \
    "{header: {frame_id: odom}, pose: {position: {x: 0.7, y: 0.7, z: 0.0}, orientation: {w: 1.0}}}"
```

A jelenlegi C++ fo launch az A* utvonalat `/astar_path` es
`/astar_dwa_markers` topicokon RViz-be rajzolja. Gazebo 3D-ben a `debug_path`
modell csak a Python `planner_node.py` agon van implementalva; a C++ fo launch
nem spawnol kulon visual-only SDF utvonalmodellt.

Az indítási sorrendben a cél csak akkor küldhető, amikor a vezérlő már
feliratkozott a `/goal_pose` topicra. Ezt a `ros2 topic info /goal_pose`
paranccsal kell ellenőrizni. A `/clock` topicnak pontosan egy Gazebo bridge-
publisherrel kell rendelkeznie; több bridge idő-visszalépést okoz RViz-ben.

A stabil indítás ellenőrzött sorrendje: régi ROS/Gazebo/RViz processzek
leállítása, egyetlen `simulation.launch.py` indítása, `/clock` és `/odom`
ellenőrzése `Publisher count: 1` értékkel, majd csak ezután az RViz indítása.
Így a TF-buffer nem kap két különböző vagy visszalépő szimulációs időt.

