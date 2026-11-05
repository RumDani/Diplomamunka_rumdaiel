"""ROS-only copy of the Python scene; original simulation sources stay unchanged."""

import importlib.util
from pathlib import Path

import codes_diploma.robot as robot_module
from codes_diploma.astar_project.grid_map import GridMap
from codes_diploma.robot import Obstacle, robotstate

PHYSICS_STEP = 0.001


def load_planner_class():
    file_path = Path(robot_module.__file__).with_name("DWA+A.py")
    spec = importlib.util.spec_from_file_location("dwa_a_module", file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load planner: {file_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.AStarDWAPlanner


def create_scene(
    width=30, height=20, resolution=0.2, start_cell=(2, 2),
    goal_cell=(17, 27), inflation_radius=0.11,
):
    grid = GridMap(width=width, height=height, resolution=resolution)
    cells = [(row, min(10, width - 2)) for row in range(2, max(2, height - 2))
             if row not in range(7, 13)]
    cells += [(min(12, height - 2), column) for column in range(12, max(12, width - 2))
              if column not in range(19, 25)]
    for cell in cells:
        if grid.is_inside(*cell) and cell not in (start_cell, goal_cell):
            grid.add_obstacle(*cell)
    grid.inflate_obstacles(inflation_radius)
    start, goal = grid.grid_to_world(*start_cell), grid.grid_to_world(*goal_cell)
    statics = [Obstacle(*grid.grid_to_world(*cell), radius=0.12) for cell in cells]
    dynamic = [Obstacle(2.4, 0.4, radius=0.18, vx=0.0, vy=0.20),
               Obstacle(6.8, 2.1, radius=0.18, vx=-0.25, vy=0.0)]
    return grid, start, goal, robotstate(x=start[0], y=start[1], irany=0.0), statics, dynamic