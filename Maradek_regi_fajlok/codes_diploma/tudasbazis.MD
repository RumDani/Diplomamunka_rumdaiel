# Tudásbázis: Kizárólag A*-alapú Útvonaltervezés (Diszkrét és Folytonos / SBA*)

> **Bővítési Figyelmeztetés**: Ezt a tárat a jövőben további irodalmakkal, optimalizálási eljárásokkal (pl. kinodinamikus korlátok, MPC, hibrid rács-mintavételes módszerek) folyamatosan bővíteni fogjuk.
> **Cél**: LLM (AI) ágens betanítása és tiszta, DWA-mentes, *kizárólag A*-alapú* (diszkrét optimalizált A* + folytonos SBA*) mozgástervező kód generálásához (C++20 / Python).

---

## 1. Modul: Diszkrét, Továbbfejlesztett A* (Globális / Rácsalapú Tervezés)
**Forrás**: Jin, M. & Wang, H. (2023) [cite: 2].
**Alkalmazási környezet**: Ismert statikus globális térkép (raster map, pl. $30\times30$).

### 1.1. Alapozás és Költségfüggvény
* Hagyományos A* költségbecslés: $f(n) = g(n) + h(n)$ [cite: 2].
* $g(n)$ a Start ($S$) és aktuális pont ($C$) közötti tényleges távolság [cite: 2].
* $h(n)$ heurisztikus becslés $C$-ből a Célhoz ($T$) [cite: 2].
* Euklideszi távolság heurisztika: $h(n) = \sqrt{(x_n - x_g)^2 + (y_n - y_g)^2}$ [cite: 2].

### 1.2. Dinamikus Heurisztikus Függvény
* A heurisztika dinamikusan súlyozandó az aktuális pozíció térbeli aránya szerint [cite: 2].
* Képlet: $h(n)^* = \left(1 + \frac{l}{L}\right) * h(n)$, ahol $l$ a $C$-től $T$-ig, $L$ a $C$-től $S$-ig mért távolság [cite: 2].
* Start közelében $l/L$ nagy $\implies$ nagy súly $\implies$ szűkebb keresési terület, gyorsabb keresés [cite: 2].
* Cél közelében kisebb szorzó $\implies$ több keresési csomópont $\implies$ optimális útvonal garancia [cite: 2].

### 1.3. 5-Szomszédságú Keresés és Sarokvágás-védelem
* 8-szomszédság helyett 5-szomszédság használata a hatékonyság növelésére [cite: 2].
* Irányválasztás alapja: $m$ vektor ($C \to T$) és $n$ vektor ($C$-n átmenő függőleges) bezárt szöge [cite: 2].
* Táblázatos 5-szomszédság szabályok [cite: 2]:
  * Clamping angle $.
  * Clamping angle $.
  * Clamping angle $.
  * Clamping angle $.
  * Clamping angle $.
  * Clamping angle $.
  * Clamping angle $.
  * Clamping angle $.
* Átlós áthatolás (sarokvágás / ütközésveszély) megelőzése: akadály a 2-es szomszédban $\implies$ törli 1,3-at; akadály a 4-esben $\implies$ törli 3,5-öt; akadály a 6-osban $\implies$ törli 7,5-öt; akadály a 8-asban $\implies$ törli 1,7-et [cite: 2].

### 1.4. Redundáns Node / Útvonal-simítás (Path Smoothing)
* Kollineáris node-ok szűrése: starttól indulva 3 szomszédos node ($A,B,C$) vektoriránya 0 fokos eltérésű $\implies$ $B$ törlése [cite: 2].
* Inflection bypass (töréspont-átugrás): starttól inflekciós pontok összekötése ($AE, AF, AI$). Ha $AE$ nem metsz akadályt és hossza kisebb, mint $A\to C\to E$, frissíti az utat $A\to E$-re [cite: 2].

---

## 2. Modul: Mintavételezésen Alapuló A* (SBA*) Folytonos Terekben
**Forrás**: Persson, S. M. & Sharf, I. (2014) [cite: 4].
**cél**: Folytonos konfigurációs terek ($\mathcal{X}$), ütközésmentes subset $\mathcal{F} \subseteq \mathcal{X}$, lokálisan elérhető régió $\mathcal{R}_l(u) \subseteq \mathcal{F}$.

### 2.1. Csomópont-érték és Valószínűségi Általánosítás
* Klasszikus A* bináris maszk helyettesítése információnyereség-modellel [cite: 4]:
  $$r(u) \triangleq \begin{cases} f(u) & u \in \{OPEN\} \\ \infty & \text{egyébként} \end{cases}$$
* Események: $\text{NEW}$ (új részleges út), $\text{FREE}$ (ütközésmentes szegmens) [cite: 4].
  $$r(u) = P(\text{NEW, FREE}|u)f(u) + (1 - P(\text{NEW, FREE}|u))\infty$$ [cite: 4]
  Független eloszlásokkal: $P(\text{NEW, FREE}|u) = P(\text{NEW}|u)P(\text{FREE}|u)$ [cite: 4].
* Várható érték / kulcsérték:
  $$r(u) = \frac{f(u)}{P(\text{NEW, FREE}|u)}$$ [cite: 4]
* Topológiai alapok:
  * $\beta$-LOOKOUT: $\beta(S) \triangleq \{u \in S | \mu(\mathcal{R}_l(u)\setminus S) \ge \beta \mu(\mathcal{R}_l(S)\setminus S)\}$ [cite: 4].
  * $(\alpha, \beta)$-expansive space: $\mu(\beta(S)) \ge \alpha\mu(S)$ minden $u \in \mathcal{F}, S \subseteq \mathcal{R}_l(u)$ esetén [cite: 4].
  * Lokális Voronoi régió: $\mathcal{V}_l(u) \triangleq \mathcal{R}_l(u) \cap \mathcal{V}(u)$ [cite: 4].
  * Konvergencia tétel (Theorem 4): Célvolumen $g > 0$, $\gamma \in (0,1]$. $n$ node esetén cél elérése valószínűséggel $\ge 1-\gamma$, ha $n \ge \frac{k}{\alpha}\log\frac{2k}{\gamma} + \frac{2}{g}\log\frac{2}{\gamma}$, ahol $k = \frac{1}{\beta}\log\frac{2}{g}$ [cite: 4].
  * $\eta$-entanglement torzítás (Corollary 5): $d_\sigma(u,v) \le \eta d(u,v) \implies P'(u) = \frac{1}{f(u)}\frac{\mu(\mathcal{V}_L(u))}{\mu(\mathcal{R}_L(V))}$, $\alpha$ helyett $\alpha/\eta$ áll [cite: 4].

### 2.2. Praktikus Prediktív Modell (KL-divergencia & Gaussian Mixture)
* Valószínűségek KL divergenciával [cite: 4]:
  $$P(\text{NEW}|u) = 1 - e^{-D_{KL}(S_u || S_{N,u})}$$
  $$P(\text{FREE}|u) = 1 - e^{-D_{KL}(S_u || S_{C,u})}$$
* Normál eloszlás pdf ($k$-dim): $S_u(x) = \frac{1}{(2\pi\sigma_u^2)^{k/2}} e^{-\frac{dist(x,p(u))^2}{2\sigma_u^2}}$ [cite: 4].
* KL divergencia egyenlő $\sigma$-val: $D_{KL}(S_u || S_v) = \frac{dist(p(u),p(v))^2}{2\sigma^2}$ [cite: 4].
* Variációs approximáció Gaussian mixture-re: $P(\text{NEW}|u) = 1 - \sum_{v \in N_u} S_u(p(v))e^{-D_{KL}(S_u || S_v)}$ [cite: 4].
* Inkrementális sűrűség ($d(u)$) és szűkület ($c(u)$) [cite: 4]:
  $$d_{k+1}(u) = (1 - S_u(p(v)))d_k(u) + S_u(p(v))e^{-D_{KL}(S_u || S_v)}$$
  $$c_{k+1}(u) = (1 - S_u(p(v)))c_k(u) + S_u(p(v))e^{-D_{KL}(S_u || S_{c_v})}$$
* Végleges gyakorlati kulcsérték [cite: 4]:
  $$r(u) = \frac{g(u) + h(u)}{(1 - c(u))(1 - d(u))}$$

### 2.3. Algoritmus Stratégiák és Finomhangolások (Csak A*)
* **Idealizált ciklus**: $u_{exp} = \arg\min_{u\in V} r(u)$, majd `RANDOMWALK(u_exp)` [cite: 4].
* **Praktikus Eager SBA*-Loop**: Min-heap $Q$ rendelve $r[u]$-hoz, legkisebb kinyerése, kiterjesztés, `CONNECT_PREDECESSORS` és `CONNECT_SUCCESSORS` (RRG-szerű élesítés és rekurzív/BFS inkonzisztencia-propagálás $g[v]$-hez) [cite: 4].
* **Lazy & Pruned trade-off**: RRT*-stílusú él-metszés (pruning) szuboptimális élekre, lusta ütközésvizsgálat (`dist` először, `STEER` utána). Constriction $c(u)$ csak ütközéses hiba esetén frissül [cite: 4].
* **Anytime A* cél-torzítás**: Lagrange-szorzó $\lambda$ bevezetése a cél elérésének gyorsítására [cite: 4]:
  $$r'_{any}(u) = \frac{g(u) + h(u) + \lambda(h(u) - h_b)}{(1-c(u))(1-d(u))}$$
  Kezdeti $\lambda = 5.0$, elérés után 0-ra decaylik [cite: 4].
* **SA-SBA* (Simulated Annealing egyensúlyozás)**: $\epsilon_{th} = 1 - \exp(-T_0 / \log N)$. Magas $T_0$-nál explorációs lépés (véletlen mintavétel + steer mint RRT*-szerű node gen), alacsony $T_0$-nál exploitatív SBA* node gen. *Megjegyzés: a vezérlő/célzott struktúra az A* optimalizációs keretében marad [cite: 4].*

---

## 3. Modul: LLM Prompt Kódgenerálási Specifikáció (Kizárólag A*)
* **Célnyelv**: C++20 vagy Python 3.10+
* **Adatstruktúra követelmények**:
  * Vertex struct: `p_pos`, `g_cost`, `h_cost`, `d_density`, `c_constriction`, `r_key`, `pred_ptr`.
  * Priority Queue / Min-Heap $Q$: Kulcsalapú rendezés $r[u]$ szerint, `requeue` támogatással.
  * Térképtárolás / Nearest Neighbor: DVP-tree (Dynamic Vantage-Point Tree) $O(\log N)$ lekérdezéshez, cache-barát BFS tömb layout [cite: 4].
* **Implementációs lépések egy AI számára**:
  1. Definíciók és KL-divergencia / Gaussian skálafaktorok rögzítése.
  2. Folytonos `RANDOMWALK` / `STEER` független kinematikai interfész megvalósítása.
  3. `SBA_LOOP` és a lazy/pruned összekötő rutinok lekódolása.
  4. Anytime Lagrange $\lambda$ és SA $\epsilon_{th}$ schedule integrálása a main loop-ba.

  # Tudásbázis: Kizárólag A*-Alapú Útvonaltervezés (Diszkrét optimalizált & Folytonos SBA*)

> **Bővítési Figyelmeztetés**: Ezt a tárat a jövőben további irodalmakkal, optimalizálási eljárásokkal (pl. kinodinamikus korlátok, MPC, hibrid rács-mintavételes módszerek) folyamatosan bővíteni fogjuk.
> **Cél**: LLM (AI) ágens betanítása és tiszta, DWA-mentes, *kizárólag A*-alapú* (diszkrét optimalizált A* + folytonos SBA*) mozgástervező kód generálásához (C++20 / Python).

---

## 1. Modul: Diszkrét, Továbbfejlesztett A* Család (Globális / Rácsalapú Tervezés)
**Alkalmazási környezet**: Ismert statikus globális rácstérkép (raster map, $M\times N$, pl. $30\times30$).

### 1.1. Alapozás és Költségfüggvény
* Alapértelmezett A* értékelő függvény:
  $$f(n) = g(n) + h(n)$$
  * $g(n)$: Start ($S$) és aktuális node ($C$) közötti tényleges mozgási költség [cite: 2].
  * $h(n)$: Becsült költség $C$-ből a Célhoz ($T$).
* Alap heurisztika variációk:
  * Euklideszi távolság: $h(n) = \sqrt{(x_n - x_g)^2 + (y_n - y_g)^2}$.
  * Manhattan távolság (alacsonyabb számítási komplexitás): $h(n) = |x_n - x_g| + |y_n - y_g|$ [cite: 5].

### 1.2. Heurisztikai Súlyozási Modellek (Irodalmi variációk)

#### A) Jin & Wang (2023) – Pozícióarányos dinamikus súlyozás [cite: 3]
* Legyen $l = \text{dist}(C, T)$ és $L = \text{dist}(C, S)$ [cite: 3].
* Dinamikus heurisztika:
  $$h(n)^* = \left(1 + \frac{l}{L}\right) \cdot h(n)$$ [cite: 3]
  * *Hatás*: $C \approx S \implies l/L \text{ nagy} \implies h(n)^*$ nagy $\implies$ fókuszált/szűk keresés. $C \approx T \implies l/L \text{ kicsi} \implies$ standard heurisztika $\implies$ optimális útvonal garancia [cite: 3].

#### B) Liu, Wang, Wu & Wei (2023) – Kinematikai kényszerítés & Exponenciális skálázás [cite: 5]
* Távolság-arány paraméter $P \in$ a node $N(x_n, y_n)$, start $S(x_s, y_s)$ és cél $G(x_g, y_g)$ között [cite: 5]:
  $$P = \frac{|x_n - x_g| + |y_n - y_g|}{|x_s - x_g| + |y_s - y_g|}$$ [cite: 5]
* Exponenciális dinamikus súlyozású értékelő függvény:
  $$f(n) = g(n) + e^P \cdot h(n)$$ [cite: 5]
  * *Hatás*: Adaptívan igazítja a $h(n)$ súlyát az akadályinformációk és a térbeli pozíció változásához, csökkentve a redundáns node-látogatásokat és a fordulatok számát [cite: 5].

### 1.3. Irány-/Szomszédság-optimalizálás és Sarokvágás-védelem

#### A) Jin & Wang (2023) 5-irányú szűrés [cite: 3]
* 8-szomszédság helyett célra mutató 5-irányúra szűkítés a $C\to T$ vektor $m$ és a függőleges $n$ szöge alapján $\theta = \angle(m,n)$:
  * $.
  * További tartományok: 22.5°-os lépésekben forgatva az 5-ös maszkot [cite: 3].
* Sarokvágás elleni védelem (ütközésbiztonság): akadály a 2-es szomszédban $\implies$ törli 1,3-at; akadály a 4-esben $\implies$ törli 3,5-öt; akadály a 6-osban $\implies$ törli 7,5-öt; akadály a 8-asban $\implies$ törli 1,7-et [cite: 3].

#### B) Liu et al. (2023) Kinematikai Irány-tábla [cite: 5]
* A célpont relatív szöge $\theta$ alapján az 8-irányú child-node halmazból fixen eldobja a robot kinematikájával vagy mozgásirányával ellentétes 3 redundáns irányt (pl. hátrafelé/rossz szögbe mutató irányok).

### 1.4. Redundáns Node / Útvonal-simítás (Path Smoothing) [cite: 3]
1. *Kollineáris szűrés*: Ha a három szomszédos node ($A, B, C$) közti vektorirány-változás 0 (szög = 0), töröld $B$-t [cite: 3].
2. *Inflection bypass*: Starttól indulva kösd össze a töréspontokat ($A\to E, A\to F, A\to I$). Ha az $A\to E$ szakasz akadálymentes és hossza $< \text{cost}(A\to C\to E)$, frissítsd az utat $A\to E$-re. Ismételd a csúcsokról [cite: 3].

---

## 2. Modul: Mintavételezésen Alapuló A* (SBA*) Folytonos Terekben
**Forrás**: Persson, S. M. & Sharf, I. (2014) [cite: 4].
**cél**: Folytonos konfigurációs terek ($\mathcal{X}$), ütközésmentes subset $\mathcal{F} \subseteq \mathcal{X}$, lokálisan elérhető régió $\mathcal{R}_l(u) \subseteq \mathcal{F}$.

### 2.1. Csomópont-érték és Valószínűségi Általánosítás
* Klasszikus A* bináris maszk helyettesítése információnyereség-modellel [cite: 4]:
  $$r(u) \triangleq \begin{cases} f(u) & u \in \{OPEN\} \\ \infty & \text{egyébként} \end{cases}$$
* Események: $\text{NEW}$ (új részleges út), $\text{FREE}$ (ütközésmentes szegmens) [cite: 4].
  $$r(u) = P(\text{NEW, FREE}|u)f(u) + (1 - P(\text{NEW, FREE}|u))\infty$$ [cite: 4]
  Független eloszlásokkal: $P(\text{NEW, FREE}|u) = P(\text{NEW}|u)P(\text{FREE}|u)$ [cite: 4].
* Várható érték / kulcsérték:
  $$r(u) = \frac{f(u)}{P(\text{NEW, FREE}|u)}$$ [cite: 4]
* Topológiai alapok:
  * $\beta$-LOOKOUT: $\beta(S) \triangleq \{u \in S | \mu(\mathcal{R}_l(u)\setminus S) \ge \beta \mu(\mathcal{R}_l(S)\setminus S)\}$ [cite: 4].
  * $(\alpha, \beta)$-expansive space: $\mu(\beta(S)) \ge \alpha\mu(S)$ minden $u \in \mathcal{F}, S \subseteq \mathcal{R}_l(u)$ esetén [cite: 4].
  * Lokális Voronoi régió: $\mathcal{V}_l(u) \triangleq \mathcal{R}_l(u) \cap \mathcal{V}(u)$ [cite: 4].
  * Konvergencia tétel (Theorem 4): Célvolumen $g > 0$, $\gamma \in (0,1]$. $n$ node esetén cél elérése valószínűséggel $\ge 1-\gamma$, ha $n \ge \frac{k}{\alpha}\log\frac{2k}{\gamma} + \frac{2}{g}\log\frac{2}{\gamma}$, ahol $k = \frac{1}{\beta}\log\frac{2}{g}$ [cite: 4].
  * $\eta$-entanglement torzítás (Corollary 5): $d_\sigma(u,v) \le \eta d(u,v) \implies P'(u) = \frac{1}{f(u)}\frac{\mu(\mathcal{V}_L(u))}{\mu(\mathcal{R}_L(V))}$, $\alpha$ helyett $\alpha/\eta$ áll [cite: 4].

### 2.2. Praktikus Prediktív Modell (KL-divergencia & Gaussian Mixture)
* Valószínűségek KL divergenciával [cite: 4]:
  $$P(\text{NEW}|u) = 1 - e^{-D_{KL}(S_u || S_{N,u})}$$
  $$P(\text{FREE}|u) = 1 - e^{-D_{KL}(S_u || S_{C,u})}$$
* Normál eloszlás pdf ($k$-dim): $S_u(x) = \frac{1}{(2\pi\sigma_u^2)^{k/2}} e^{-\frac{dist(x,p(u))^2}{2\sigma_u^2}}$ [cite: 4].
* KL divergencia egyenlő $\sigma$-val: $D_{KL}(S_u || S_v) = \frac{dist(p(u),p(v))^2}{2\sigma^2}$ [cite: 4].
* Variációs approximáció Gaussian mixture-re: $P(\text{NEW}|u) = 1 - \sum_{v \in N_u} S_u(p(v))e^{-D_{KL}(S_u || S_v)}$ [cite: 4].
* Inkrementális sűrűség ($d(u)$) és szűkület ($c(u)$) [cite: 4]:
  $$d_{k+1}(u) = (1 - S_u(p(v)))d_k(u) + S_u(p(v))e^{-D_{KL}(S_u || S_v)}$$
  $$c_{k+1}(u) = (1 - S_u(p(v)))c_k(u) + S_u(p(v))e^{-D_{KL}(S_u || S_{c_v})}$$
* Végleges gyakorlati kulcsérték [cite: 4]:
  $$r(u) = \frac{g(u) + h(u)}{(1 - c(u))(1 - d(u))}$$

### 2.3. Algoritmus Stratégiák és Finomhangolások (Kizárólag A*)
* **Idealizált ciklus**: $u_{exp} = \arg\min_{u\in V} r(u)$, majd `RANDOMWALK(u_exp)` [cite: 4].
* **Praktikus Eager SBA*-Loop**: Min-heap $Q$ rendelve $r[u]$-hoz, legkisebb kinyerése, kiterjesztés, `CONNECT_PREDECESSORS` és `CONNECT_SUCCESSORS` (RRG-szerű élesítés és rekurzív/BFS inkonzisztencia-propagálás $g[v]$-hez) [cite: 4].
* **Lazy & Pruned trade-off**: RRT*-stílusú él-metszés (pruning) szuboptimális élekre, lusta ütközésvizsgálat (`dist` először, `STEER` utána). Constriction $c(u)$ csak ütközéses hiba esetén frissül [cite: 4].
* **Anytime A* cél-torzítás**: Lagrange-szorzó $\lambda$ bevezetése a cél elérésének gyorsítására [cite: 4]:
  $$r'_{any}(u) = \frac{g(u) + h(u) + \lambda(h(u) - h_b)}{(1-c(u))(1-d(u))}$$
  Kezdeti $\lambda = 5.0$, elérés után 0-ra decaylik [cite: 4].
* **SA-SBA* (Simulated Annealing egyensúlyozás A*-keretben)**: $\epsilon_{th} = 1 - \exp(-T_0 / \log N)$. Magas $T_0$-nál explorációs node-gen (véletlen mintavétel + steer), alacsony $T_0$-nál exploitatív $r(u)$ alapú node-gen.

---

## 3. Modul: LLM Prompt Kódgenerálási Specifikáció (Kizárólag A*)
* **Célnyelv**: C++20 vagy Python 3.10+
* **Adatstruktúra követelmények**:
  * Grid / Node / Vertex struct: pozíció, $g$, $h$, $f$, $r$, $d$, $c$, pred_ptr.
  * Priority Queue / Min-Heap $Q$: Kulcsalapú rendezés $r[u]$ vagy $f(n)$ szerint.
  * Térképtárolás / Nearest Neighbor: DVP-tree (Dynamic Vantage-Point Tree) $O(\log N)$ lekérdezéshez (SBA*-hoz) [cite: 4] vagy 2D/3D rács indexelés (diszkrét A*-hoz).
* **Implementációs lépések egy AI számára**:
  1. Diszkrét globális A* (Manhattan/Euklideszi + $e^P h(n)$ exponenciális skálázás + 5-irányú szűrés + smoothing) megírása.
  2. Folytonos SBA* (KL-divergencia + $d(u)/c(u)$ inkrementális frissítés) kiegészítő modul implementálása.
  3. Fő ciklus összekötése az optimalizált költségfunkciókkal.



  # Tudásbázis: Kinematikailag korlátozott A* és DWA fúziós algoritlus mobil robotokhoz

*Forrás/Hivatkozás:* Liu, Y., Wang, C., Wu, H., Wei, Y. (2023). *Mobile Robot Path Planning Based on Kinematically Constrained A-Star Algorithm and DWA Fusion Algorithm*. Mathematics, 11(21), 4552. DOI: 10.3390/math11214552.

---

## 1. Architektúra áttekintés
* **Globális tervező**: Kinematikailag korlátozott/optimalizált $A^*$ (offline/fél-online, statikus térkép, kevesebb kanyar, alacsonyabb számítási költség).
* **Lokális tervező**: Optimalizált DWA (Dynamic Window Approach) (online, valós idejű dinamikus akadálykerülés, simább sebességprofil).
* **Fúziós mechanizmus**: Az $A^*$ globális útvonalából **kulcspontok (key nodes)** kinyerése, melyeket a DWA sorozatos célpontként ($target_{node}$) követ.

---

## 2. Globális útvonaltervezés: Fejlesztett $A*$
Hagyományos értékelő függvény:
<div style="text-align:center; margin:1em 0; font-size:1.1em;"><span class="math">f(n) = g(n) + h(n)</span></div>
Ahol <span class="math">g(n)</span> a kezdőtől mért tényleges költség, <span class="math">h(n)</span> a heurisztikus becslés.

### 2.1 Szomszédsági optimalizálás (Neighborhood Optimization)
* **Probléma**: A 8-irányú szomszédság redundáns irányokat tartalmaz, növelve a számítási terhet.
* **Megoldás**: A célpont és a aktuális pont közötti szög (<span class="math">θ</span>, északhoz képest) alapján **3 redundáns irány eldobása**, a maradék 5 irány vizsgálata (lásd 1. táblázat a cikkben).

### 2.2 Heurisztikus modell cseréje
* **Euklideszi helyett Manhattan-távolság**:
<div style="text-align:center; margin:1em 0; font-size:1.1em;"><span class="math">D = |x<sub>i</sub> − x<sub>j</sub>| + |y<sub>i</sub> − y<sub>j</sub>|</span></div>
Csökkenti a számítási komplexitást.

### 2.3 Dinamikus súlyozás (Distance-Scale Parameter P)
Távolság-arány paraméter definiálása:
<div style="text-align:center; margin:1em 0; font-size:1.1em;"><span class="math">P = \frac{|x<sub>n</sub> − x<sub>g</sub>| + |y<sub>n</sub> − y<sub>g</sub>|}{|x<sub>s</sub> − x<sub>g</sub>| + |y<sub>s</sub> − y<sub>g</sub>|} \in [0, 1]</span></div>
Javított értékelő függvény exponenciális súlyozással:
<div style="text-align:center; margin:1em 0; font-size:1.1em;"><span class="math">f(n) = g(n) + e<sup>P</sup> · h(n)</span></div>
Adaptívan hangolja a heurisztika súlyát az akadályok/pozíció függvényében.

---

## 3. Lokális útvonaltervezés: Optimalizált DWA
Hagyományos pályamutató-függvény:
<div style="text-align:center; margin:1em 0; font-size:1.1em;"><span class="math">G(v, w) = α · vel(v, w) + β · head(v, w) + γ · dist(v, w)</span></div>
* <span class="math">vel(v, w)</span>: lineáris sebesség aránya (<span class="math">v<sub>i</sub> / Σ v<sub>i</sub></span>)
* <span class="math">head(v, w)</span>: célorientációs eltérés normált értéke (<span class="math">(π − Δθ<sub>i</sub>) / Σ(π − Δθ<sub>i</sub>)</span>)
* <span class="math">dist(v, w)</span>: legközelebbi akadály távolságának aránya

### 3.1 Súlyparaméter-optimalizálás (Empirikus / ROS guide alapján)
* Cikkben optimálisnak talált súlyok: **<span class="math">α = 15</span>, <span class="math">β = 37</span>, <span class="math">γ = 0.02</span>** (a <span class="math">β</span> dominanciája biztosítja a célegyenesben lévő akadályok kikerülését anélkül, hogy feleslegesen nagy íveket írna le a robot).

---

## 4. Kísérleti eredmények & benchmark (Összefoglaló)

| Metrika / Teszt | Hagyományos A* + DWA (Hibrid) | Kinematikailag korlátozott A* + DWA (Fúzió) | Javulás / Eredmény |
| :--- | :--- | :--- | :--- |
| **Szimulációs path length** | Referencia | − | **−6.24%** út hosszabbodás helyett csökkenés |
| **Szimulációs turn count** | 4 | 1 | **−75.0%** kanyarszám |
| **Szimulációs planning time** | 91.04 s | 79.45 s | **−12.73%** időmegtakarítás |
| **Statikus globális turn count** | 8 | 2 | **−75.0%** kanyar |
| **Statikus globális length** | 6.6748 m | 6.2410 m | **−6.5%** |
| **Statikus globális time** | 0.03374 s | 0.02524 s | **−25.20%** |

* **Dinamikus teszt (Mir-5 robot / ROS Melodic / C++)**:
  * Simább X-tengelyű lokális pozíciókövetés.
  * Folytonosabb, stabilabb Z-tengelyű szögsebesség (<span class="math">cmd_vel</span>) kiadás, kevesebb rezgés/tranzienstechnikai hiba.

---

## 5. Nyitott kihívások / További kutatási irányok
1. **Drivetrain / Chassis tranziensek**: A DWA közvetlenül adja ki a <span class="math">v, w</span> sebességet acceleration/braking limetek teljes figyelembevétele nélkül -> trajektóriakövetési (trajectory tracking) réteg integrálása szükséges.
2. **Vizuális szenzorok (Kinect V2 / IMU / LiDAR)** mélyebb fúziója dinamikus target trackinghez.
3. **Kültéri/szűk folyosós scenáriók**: Globális road-network integráció nagy távolságú tervezéshez.

---