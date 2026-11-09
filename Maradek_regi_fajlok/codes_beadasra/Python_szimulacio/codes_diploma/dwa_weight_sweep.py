"""DWA sulyparameter-sweep a Python szimulacios kornyezeten (headless)."""
import csv
import itertools
import math
import os
import sys
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import matplotlib

matplotlib.use("Agg")

from codes_diploma.astar_project.astar_variants import get_heuristic
from codes_diploma.robot import robotconfig, update
from codes_diploma.simulation import create_scene, load_planner_class

OUT_DIR = Path(__file__).with_name("dwa_sweep_results")


def run_case(alpha, beta, gamma, max_steps=600):
    (grid_map, _, _, start, goal, state, statics, dynamics) = create_scene(
        30, 20, 0.2, (2, 2), (17, 27), 0.1
    )
    config = robotconfig()
    config.Alfa, config.Beta, config.Gamma = alpha, beta, gamma
    planner = load_planner_class()(grid_map, config=config, diagonal=True)
    planner.plan_global(start, goal, heuristic=get_heuristic("euclidean"),
                        smooth=True, samples_per_curve=8)
    obstacles = statics + dynamics
    length, min_clear, collisions, no_command = 0.0, math.inf, 0, 0
    previous = (state.x, state.y)
    reached = False
    for step in range(max_steps):
        for obstacle in dynamics:
            obstacle.move(config.dt)
        result = planner.plan_local(state, obstacles)
        best = result["best_pair"] if result is not None else None
        if best is None:
            no_command += 1
            update(state, config, 0.0, 0.0, config.dt)
        else:
            update(state, config, best[2], best[3], config.dt)
        length += math.hypot(state.x - previous[0], state.y - previous[1])
        previous = (state.x, state.y)
        clearance = min(math.hypot(state.x - o.x, state.y - o.y) - o.radius - config.rob_radius
                        for o in obstacles)
        min_clear = min(min_clear, clearance)
        if clearance < 0:
            collisions += 1
        if planner.reached_goal(state):
            reached = True
            break
    return {
        "alpha": alpha, "beta": beta, "gamma": gamma, "reached": reached,
        "time_s": round((step + 1) * config.dt, 1), "path_m": round(length, 2),
        "min_clearance_m": round(min_clear, 3), "collision_steps": collisions,
        "no_command_steps": no_command,
    }


def run_args(args):
    return run_case(*args)


def main():
    # 3x3x3 racs, tartalmazza az alapertekeket (5, 2, 3)
    combos = list(itertools.product([2, 5, 8], [1, 2, 4], [1, 3, 5]))
    OUT_DIR.mkdir(exist_ok=True)
    rows = []
    with Pool(max(1, (os.cpu_count() or 2) - 1)) as pool:
        for row in pool.imap_unordered(run_args, combos):
            rows.append(row)
            print(row, flush=True)
    rows.sort(key=lambda r: (r["alpha"], r["beta"], r["gamma"]))
    with open(OUT_DIR / "dwa_weight_sweep.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
