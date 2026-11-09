# Python 2D szimuláció (A* + DWA)

Matematikai (nem ROS-os) szimuláció: az A* tervezi az utat, a DWA vezeti a robotot, a mozgó akadályokat kikerülve. Python 3, a `numpy` és a `matplotlib` kell hozzá (a grafikus ablakhoz `tkinter`).

## Mappák
```
Python_szimulacio/
└── codes_diploma/
    ├── simulation.py        indító és animáció
    ├── DWA+A.py             A* és DWA összekapcsolása (waypointok)
    ├── DWA.py               DWA algoritmus (pontozás)
    ├── robot.py             robotmodell és paraméterek
    ├── astar_project/       A* keresés, heurisztikák, rácstérkép, útvonalsimítás
    └── sulyvizsgalat/       DWA súlyvizsgálat (szkript + eredmény CSV)
```

## Indítás
Terminálban (PowerShell), ebből a mappából (`Python_szimulacio`):
```
cd "<útvonal>\Projekt\Python_szimulacio"
pip install numpy matplotlib
$env:PYTHONIOENCODING="utf-8"
python -m codes_diploma.simulation
```
1. Először egy **„A* + DWA beallitasok"** ablak jelenik meg (méret, start, cél, α/β/γ súlyok). Ez a tálcán/más ablak mögött is lehet.
2. Az alapértékek jók, kattints a **„Szimulacio inditasa"** gombra.
3. Megnyílik az animáció (A* útvonal, DWA pályák, mozgó akadályok), és automatikusan lejátszik.

Az ablak bezárásával a program leáll.

## Súlyvizsgálat (opcionális, ~1,5 óra)
```
python codes_diploma\sulyvizsgalat\dwa_weight_sweep.py
```
Az eredmény a `codes_diploma\sulyvizsgalat\dwa_weight_sweep.csv` fájlba kerül.
