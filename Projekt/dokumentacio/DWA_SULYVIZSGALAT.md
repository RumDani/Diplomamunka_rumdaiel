# DWA súlyvizsgálat – eredmények
## Módszer

A 2D Python szimulációban (A* + DWA) a DWA pontszámának súlyait változtattam: `pont = α·irány + β·távolság + γ·sebesség`. Két helyzetet futtattam: **S1** – alappálya, **S2** – az alappálya kiegészítve egy keresztező mozgó akadállyal. A futásidő **szimulált idő** (lépésszám · dt, dt = 0,1 s), ezért nem függ a gép sebességétől. Ütközésnek számít, ha a robot és egy akadály távolsága bármelyik lépésben negatív. Összesen 64 eset: α ∈ {2, 5, 8} × β ∈ {0, 2, 6} × γ ∈ {1, 3, 5} (predikciós idő 3 s, biztonsági sáv 0,15 m), továbbá predikciós idő {2, 4} s és biztonsági sáv {0,10; 0,20; 0,25} m az alapsúlyokkal (5/2/3). Maximum 400 lépés (40 s).

## Összesítés

| Helyzet | Esetek | Célba ért | Ütközés nélkül célba ért | Ütközött |
|---|---|---|---|---|
| S1 | 32 | 30 | 18 | 12 |
| S2 | 32 | 30 | 17 | 13 |

## Súlykombinációk (predikciós idő 3 s, biztonsági sáv 0,15 m)

Cellák: eredmény; szimulált idő; legkisebb akadálytávolság (negatív = ütközés).

| α | β | γ | S1 | S2 |
|---|---|---|---|---|
| 2 | 0 | 1 | ÜTKÖZÉS; 23.9 s; -0.27 m | ÜTKÖZÉS; 25.8 s; -0.27 m |
| 2 | 0 | 3 | ÜTKÖZÉS; 23.6 s; -0.27 m | ÜTKÖZÉS; 25.6 s; -0.28 m |
| 2 | 0 | 5 | ÜTKÖZÉS; 23.5 s; -0.27 m | ÜTKÖZÉS; 25.5 s; -0.27 m |
| 2 | 2 | 1 | OK; 25.2 s; 0.07 m | OK; 25.7 s; 0.07 m |
| 2 | 2 | 3 | OK; 27.3 s; 0.03 m | ÜTKÖZÉS; 25.8 s; -0.22 m |
| 2 | 2 | 5 | nem ért célba; 40.0 s; 0.02 m | nem ért célba; 40.0 s; 0.03 m |
| 2 | 6 | 1 | OK; 25.2 s; 0.07 m | OK; 25.7 s; 0.07 m |
| 2 | 6 | 3 | OK; 27.3 s; 0.03 m | OK; 25.9 s; 0.01 m |
| 2 | 6 | 5 | nem ért célba; 40.0 s; 0.02 m | nem ért célba; 40.0 s; 0.03 m |
| 5 | 0 | 1 | ÜTKÖZÉS; 24.5 s; -0.28 m | ÜTKÖZÉS; 26.2 s; -0.27 m |
| 5 | 0 | 3 | ÜTKÖZÉS; 23.7 s; -0.27 m | ÜTKÖZÉS; 25.8 s; -0.27 m |
| 5 | 0 | 5 | ÜTKÖZÉS; 23.7 s; -0.27 m | ÜTKÖZÉS; 25.5 s; -0.27 m |
| 5 | 2 | 1 | OK; 27.4 s; 0.08 m | OK; 27.5 s; 0.10 m |
| 5 (alap) | 2 | 3 | OK; 25.6 s; 0.11 m | OK; 25.4 s; 0.05 m |
| 5 | 2 | 5 | ÜTKÖZÉS; 25.4 s; -0.05 m | ÜTKÖZÉS; 25.0 s; -0.05 m |
| 5 | 6 | 1 | OK; 27.4 s; 0.08 m | OK; 27.5 s; 0.10 m |
| 5 | 6 | 3 | OK; 25.6 s; 0.11 m | OK; 25.4 s; 0.05 m |
| 5 | 6 | 5 | ÜTKÖZÉS; 25.4 s; -0.05 m | ÜTKÖZÉS; 25.0 s; -0.05 m |
| 8 | 0 | 1 | ÜTKÖZÉS; 24.5 s; -0.27 m | ÜTKÖZÉS; 26.4 s; -0.28 m |
| 8 | 0 | 3 | ÜTKÖZÉS; 24.0 s; -0.26 m | ÜTKÖZÉS; 25.7 s; -0.28 m |
| 8 | 0 | 5 | ÜTKÖZÉS; 23.8 s; -0.27 m | ÜTKÖZÉS; 25.9 s; -0.28 m |
| 8 | 2 | 1 | OK; 27.3 s; 0.09 m | OK; 27.5 s; 0.09 m |
| 8 | 2 | 3 | OK; 27.1 s; 0.06 m | OK; 27.1 s; 0.07 m |
| 8 | 2 | 5 | OK; 25.2 s; 0.07 m | OK; 25.5 s; 0.05 m |
| 8 | 6 | 1 | OK; 27.3 s; 0.09 m | OK; 27.5 s; 0.09 m |
| 8 | 6 | 3 | OK; 27.1 s; 0.06 m | OK; 27.1 s; 0.07 m |
| 8 | 6 | 5 | OK; 25.2 s; 0.07 m | OK; 25.5 s; 0.05 m |

## Predikciós idő és biztonsági sáv (α/β/γ = 5/2/3)

| Paraméter | Érték | S1 | S2 |
|---|---|---|---|
| predikciós idő | 2 s | ÜTKÖZÉS; 25.6 s; -0.22 m | ÜTKÖZÉS; 26.6 s; -0.08 m |
| predikciós idő | 3 s | OK; 25.6 s; 0.11 m | OK; 25.4 s; 0.05 m |
| predikciós idő | 4 s | OK; 24.0 s; 0.13 m | OK; 24.9 s; 0.13 m |
| biztonsági sáv | 0.10 m | OK; 24.9 s; 0.03 m | OK; 25.1 s; 0.05 m |
| biztonsági sáv | 0.15 m | OK; 25.6 s; 0.11 m | OK; 25.4 s; 0.05 m |
| biztonsági sáv | 0.20 m | OK; 25.7 s; 0.12 m | OK; 26.7 s; 0.03 m |
| biztonsági sáv | 0.25 m | OK; 28.2 s; 0.05 m | OK; 28.2 s; 0.05 m |

## Értékelés (dolgozatba szánt szöveg)

A súlyvizsgálat célja annak megállapítása volt, mely paraméterek határozzák meg a DWA biztonságos működését. A β (akadálytávolság-súly) a legkritikusabb: **β = 0 esetén mind a 18 futás ütközéssel végződött** mindkét helyzetben (átlagos legkisebb távolság −0,27 m), vagyis akadályérzékelés nélkül a pontozás csak az irányt és a sebességet jutalmazza, és a robot nekimegy az akadályoknak. β = 2 és β = 6 között az eredmény gyakorlatilag azonos (a távolság-pontszám korlátos, ezért telítődik), ezért a β = 2 elegendő. A γ (sebességsúly) növelése rontja a biztonságot, ha az α nem elég nagy: γ = 5 mellett α = 2 esetén a robot nem ért célba, α = 5 esetén ütközött, csak α = 8 mellett volt biztonságos. Vagyis a sebesség jutalmazása az irányítás súlyához viszonyítva számít. Az α = 2 lassúbb, bizonytalanabb haladást ad (több ütközés vagy nem teljesített út), az α = 5–8 megbízhatóbb.

Az alapbeállítás (α/β/γ = 5/2/3, predikciós idő 3 s, sáv 0,15 m) mindkét helyzetben ütközés nélkül célba ért (S1: 25,6 s, 0,108 m; S2: 25,4 s, 0,050 m legkisebb távolság), ezért ez maradt a választott konfiguráció. A 4 s-os predikciós idő valamivel nagyobb távolságot (0,126 / 0,132 m) és rövidebb időt adott, a 2 s-os viszont ütközést okozott, mert a robot későn reagál. A biztonsági sáv növelése nagyobb távolságot ad, de lassabbá teszi a haladást.

*Megjegyzés:* a Gazebo-szimulációban futó C++ vezérlő saját paraméterezésű, ezért ez a vizsgálat a Python 2D szimulációra vonatkozik. Az idő szimulált idő, a futási idő géptől független.
