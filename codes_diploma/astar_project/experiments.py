"""Reprodukálható A* összehasonlító kísérletek."""

import csv
import math
from pathlib import Path

from .astar_baseline import astar_search
from .astar_variants import HEURISTICS, get_heuristic
from .grid_map import GridMap


def _path_cost(path):
    """Kiszámítja a rácsútvonal költségét egyenes/átlós lépésekkel."""
    if not path:
        return None
    return sum(
        math.hypot(current[0] - previous[0], current[1] - previous[1])
        for previous, current in zip(path, path[1:])
    )


def build_experiment_scenarios():
    """Visszaadja azonos méretű, reprodukálható tesztpályákat.

    A pályák között van szabad tér, átjárót tartalmazó akadálypálya,
    sarokvágást tiltó eset és olyan pálya is, ahol átlós mozgás nélkül
    nincs megoldás.
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
    """Összeveti a heurisztikákat egyetlen pályán.

    A visszatérési lista minden eleme tartalmazza a heurisztika nevét,
    a talált útvonalat, annak költségét, a kibővített csomópontok számát
    és azt, hogy sikerült-e célt elérni.
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
    """Minden pályát lefuttat átlós és nem átlós módban."""
    rows = []
    for scenario_name, (grid_map, start, goal) in build_experiment_scenarios().items():
        for diagonal in (False, True):
            for row in compare_heuristics(
                grid_map, start, goal, diagonal, heuristic_names
            ):
                rows.append({"scenario": scenario_name, **row})
    return rows


def write_results(rows, output_path):
    """CSV-be menti a kísérleti eredményeket, útvonal nélkül."""
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
