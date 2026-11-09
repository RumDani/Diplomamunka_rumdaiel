"""DWA parameter-sweep a Python szimulacios kornyezeten (headless).

Az ido a SZIMULALT ido (lepesszam * dt), ezert nem fugg a gep sebessegetol.
Futtatas (a repo gyokerebol): python -m codes_diploma.dwa_weight_sweep [probe]
"""
import csv
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
from codes_diploma.robot import Obstacle, robotconfig, update
from codes_diploma.simulation import create_scene, load_planner_class

OUT_DIR = Path(__file__).with_name("dwa_sweep_results")
MAX_STEPS = 400  # 40 s szimulalt ido

# S1: az alap pálya, szembejövő mozgó akadály; S2: ehhez egy keresztező akadály is
SCENARIOS = {
    "S1": [],
    "S2": [(3.4, 0.2, 0.0, 0.14)],
}


def run_case(args):
    scenario, params = args
    (grid_map, _, _, start, goal, state, statics, dynamics) = create_scene(
        30, 20, 0.2, (2, 2), (17, 27), 0.1
    )
    for x, y, vx, vy in SCENARIOS[scenario]:
        dynamics.append(Obstacle(x, y, radius=0.18, vx=vx, vy=vy))
    config = robotconfig()
    config.Alfa, config.Beta, config.Gamma = params["alpha"], params["beta"], params["gamma"]
    config.predict_time = params["predict_time"]
    config.safety_margin = params["safety_margin"]
    planner = load_planner_class()(grid_map, config=config, diagonal=True)
    planner.plan_global(start, goal, heuristic=get_heuristic("euclidean"),
                        smooth=True, samples_per_curve=8)
    obstacles = statics + dynamics
    length, min_clear, collisions, no_command = 0.0, math.inf, 0, 0
    previous = (state.x, state.y)
    reached = False
    for step in range(MAX_STEPS):
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
    sim_time = (step + 1) * config.dt
    return {
        "scenario": scenario, **params, "reached": reached,
        "sim_time_s": round(sim_time, 1), "path_m": round(length, 2),
        "avg_speed_mps": round(length / sim_time, 3),
        "min_clearance_m": round(min_clear, 3), "collision_steps": collisions,
        "collision": collisions > 0, "no_command_steps": no_command,
    }


BASE = {"alpha": 5, "beta": 2, "gamma": 3, "predict_time": 3, "safety_margin": 0.15}


def build_jobs():
    jobs = []
    for scenario in SCENARIOS:
        for a in (2, 5, 8):
            for b in (0, 2, 6):
                for g in (1, 3, 5):
                    jobs.append((scenario, {**BASE, "alpha": a, "beta": b, "gamma": g}))
        for predict_time in (2, 4):
            jobs.append((scenario, {**BASE, "predict_time": predict_time}))
        for margin in (0.10, 0.20, 0.25):
            jobs.append((scenario, {**BASE, "safety_margin": margin}))
    return jobs


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "probe":
        jobs = [(s, {**BASE, "beta": b}) for s in SCENARIOS for b in (0, 20)]
    else:
        jobs = build_jobs()
    print(len(jobs), "eset", flush=True)
    OUT_DIR.mkdir(exist_ok=True)
    rows = []
    with Pool(max(1, (os.cpu_count() or 2) - 1)) as pool:
        for row in pool.imap_unordered(run_case, jobs):
            rows.append(row)
            print(row, flush=True)
    rows.sort(key=lambda r: (r["scenario"], r["alpha"], r["beta"], r["gamma"],
                             r["predict_time"], r["safety_margin"]))
    name = "probe.csv" if len(sys.argv) > 1 else "dwa_weight_sweep.csv"
    with open(OUT_DIR / name, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
