"""ROS-only copy of the Python scene; original simulation sources stay unchanged."""

import importlib.util
import math
import xml.etree.ElementTree as ET
from pathlib import Path

import codes_diploma.robot as robot_module
from codes_diploma.astar_project.grid_map import GridMap
from codes_diploma.robot import Obstacle, robotstate

PHYSICS_STEP = 0.001


def load_planner_class(optimizer=None):
    file_path = Path(robot_module.__file__).with_name("DWA+A.py")
    spec = importlib.util.spec_from_file_location("dwa_a_module", file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load planner: {file_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if optimizer is not None:
        module.optimisation = optimizer
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


def create_gazebo_scene(world_file, resolution=0.2, inflation_radius=0.27):
    if not math.isfinite(resolution) or resolution <= 0:
        raise ValueError("Map resolution must be finite and positive")
    world = ET.parse(world_file).getroot().find("world")
    if world is None:
        raise ValueError("Missing Gazebo world")
    models = {model.get("name"): model for model in world.findall("model")}
    poses = {name: [float(value) for value in model.findtext("pose", "0 0 0 0 0 0").split()]
             for name, model in models.items()}
    origin_x, origin_y = poses["boundary_left"][0], poses["boundary_bottom"][1]
    width = math.ceil((poses["boundary_right"][0] - origin_x) / resolution)
    height = math.ceil((poses["boundary_top"][1] - origin_y) / resolution)
    grid = GridMap(width, height, resolution, origin_x, origin_y)
    statics = []
    for name, model in models.items():
        size = model.findtext("link/collision/geometry/box/size")
        if model.findtext("static") != "true" or size is None:
            continue
        x, y, _, roll, pitch, yaw = poses[name]
        if abs(roll) + abs(pitch) + abs(yaw) > 1e-6:
            raise ValueError("The reference world requires axis-aligned walls")
        size_x, size_y, _ = map(float, size.split())
        half_x, half_y = size_x / 2, size_y / 2
        cell_margin = inflation_radius + resolution / math.sqrt(2)
        for row in range(height):
            for column in range(width):
                cell_x, cell_y = grid.grid_to_world(row, column)
                dx, dy = max(abs(cell_x - x) - half_x, 0), max(abs(cell_y - y) - half_y, 0)
                if math.hypot(dx, dy) <= cell_margin:
                    grid.add_obstacle(row, column)
        along_x = size_x >= size_y
        length, thickness = (size_x, size_y) if along_x else (size_y, size_x)
        count = max(1, math.ceil(length / resolution))
        radius = math.hypot(thickness / 2, length / count / 2)
        for index in range(count + 1):
            offset = -length / 2 + length * index / count
            statics.append(Obstacle(x + offset if along_x else x,
                                    y if along_x else y + offset, radius=radius))
    include = world.find("include")
    if include is None:
        raise ValueError("Missing TurtleBot include")
    spawn = [float(value) for value in include.findtext("pose", "0 0 0 0 0 0").split()]
    if abs(spawn[5]) > 1e-6:
        raise ValueError("The reference spawn yaw must be zero")
    start = (spawn[0], spawn[1])
    velocities = {"moving_obstacle_1": (0.0, 0.20), "moving_obstacle_2": (-0.25, 0.0)}
    dynamic = []
    for name, (vx, vy) in velocities.items():
        radius = float(models[name].findtext("link/collision/geometry/cylinder/radius"))
        dynamic.append(Obstacle(*poses[name][:2], radius=radius, vx=vx, vy=vy))
    return grid, start, (6.5, 4.2), robotstate(x=start[0], y=start[1]), statics, dynamic