"""A* + DWA szimulacio lathato racs- es pontkivalasztasokkal."""

import importlib.util
import math
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

import matplotlib

if __name__ == "__main__":
	matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle, Rectangle

from codes_diploma.astar_project.astar_baseline import astar_search
from codes_diploma.astar_project.astar_variants import get_heuristic
from codes_diploma.astar_project.grid_map import GridMap
from codes_diploma.robot import Obstacle, robotconfig, robotstate, update


def load_planner_class():
	"""Betolti a plusz karaktert tartalmazo DWA+A.py fajlt."""
	file_path = Path(__file__).with_name("DWA+A.py")
	spec = importlib.util.spec_from_file_location("dwa_a_module", file_path)
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module.AStarDWAPlanner


def parse_cell(value):
	row, column = (int(part.strip()) for part in value.split(","))
	return row, column


def create_scene(width=30, height=20, resolution=0.2, start_cell=(2, 2), goal_cell=(17, 27), inflation_radius=0.1):
	"""Letrehozza az A* es DWA kozos palyajat."""
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
	static_obstacles = [Obstacle(*grid_map.grid_to_world(*cell), radius=0.12) for cell in static_cells]
	dynamic_obstacles = [
		Obstacle(2.5, 1.2, radius=0.18, vx=0.0, vy=0.18),
		Obstacle(4.3, 2.8, radius=0.18, vx=-0.12, vy=0.0),
	]
	return grid_map, start_cell, goal_cell, start, goal, state, static_obstacles, dynamic_obstacles


def create_simulation(width=30, height=20, resolution=0.2, start_cell=(2, 2), goal_cell=(17, 27), diagonal=True, heuristic_name="euclidean", inflation_radius=0.1, smooth=True, samples_per_curve=8, alpha=5.0, beta=2.0, gamma=3.0, waypoint_slowdown=False, show_original_astar=False, max_steps=600, auto_play=True, show=False):
	"""Letrehozza az A* tervezesi es a DWA mozgas animaciojat."""
	planner_class = load_planner_class()
	grid_map, start_cell, goal_cell, start, goal, state, static_obstacles, dynamic_obstacles = create_scene(
		width, height, resolution, start_cell, goal_cell, inflation_radius
	)
	heuristic = get_heuristic(heuristic_name)
	astar_result = astar_search(grid_map, start_cell, goal_cell, diagonal=diagonal, heuristic=heuristic, return_details=True)
	if astar_result["path"] is None:
		raise RuntimeError("Az A* nem talalt utvonalat a beallitott terkepen.")

	config = robotconfig()
	config.Alfa = alpha
	config.Beta = beta
	config.Gamma = gamma
	config.enable_waypoint_slowdown = waypoint_slowdown
	planner = planner_class(grid_map, config=config, diagonal=diagonal)
	path = planner.plan_global(start, goal, heuristic=heuristic, smooth=smooth, samples_per_curve=samples_per_curve)
	expanded_world = [grid_map.grid_to_world(*cell) for cell in astar_result["expanded_nodes"]]
	path_world = list(path)
	planning_frames = max(1, len(expanded_world))
	movement_start = planning_frames + 1
	total_frames = movement_start + max_steps

	figure, (info_ax, map_ax) = plt.subplots(1, 2, figsize=(15, 8), gridspec_kw={"width_ratios": (1, 3)})
	figure.subplots_adjust(bottom=0.13, right=0.82, wspace=0.08)
	info_ax.set_axis_off()
	info_ax.set_title("A* + DWA allapot")
	priority_text = info_ax.text(0.02, 0.95, "", va="top", family="monospace", fontsize=8)

	for row in range(grid_map.height + 1):
		map_ax.axhline(row * resolution, color="#78909c", linewidth=0.65, alpha=0.75, zorder=0)
	for column in range(grid_map.width + 1):
		map_ax.axvline(column * resolution, color="#78909c", linewidth=0.65, alpha=0.75, zorder=0)
	for row in range(grid_map.height):
		for column in range(grid_map.width):
			if grid_map.grid[row][column] == 1:
				map_ax.add_patch(Rectangle((column * resolution, row * resolution), resolution, resolution, color="#455a64", zorder=1))

	astar_world = list(planner.astar_path)
	astar_x, astar_y = zip(*astar_world)
	path_x, path_y = zip(*path_world)
	waypoint_x, waypoint_y = zip(*planner.waypoints)
	astar_line, = map_ax.plot(astar_x, astar_y, ":", color="#b0bec5", linewidth=1.3, label="A* racsutvonal", zorder=2)
	astar_line.set_visible(show_original_astar)
	map_ax.plot(path_x, path_y, "-", color="#2e7d32", linewidth=3.5, label="Bezier utvonal", zorder=4)
	map_ax.scatter(waypoint_x, waypoint_y, s=14, color="#e53935", edgecolors="#1b5e20", linewidths=0.8, label="Bezier DWA pontok", zorder=6)
	explored = map_ax.scatter([], [], s=18, color="#90caf9", alpha=0.45, label="A* vizsgalt cellak", zorder=3)
	current_cell = map_ax.scatter([], [], s=110, color="#ff9800", edgecolors="#e65100", label="A* aktualis pont", zorder=5)
	waypoint = map_ax.scatter([], [], s=150, marker="*", color="#fdd835", edgecolors="#f57f17", label="DWA waypoint", zorder=7)
	robot = Circle(start, config.rob_radius, fill=False, color="#1565c0", linewidth=2, label="Robot", zorder=7)
	map_ax.add_patch(robot)
	goal_patch = Circle(goal, config.rob_radius * 0.6, fill=False, color="#2e7d32", linewidth=2, label="Cel", zorder=6)
	map_ax.add_patch(goal_patch)
	trail_line, = map_ax.plot([start[0]], [start[1]], color="#1565c0", linewidth=2, label="Robot nyoma", zorder=4)
	local_line, = map_ax.plot([], [], color="#ef6c00", linewidth=2.5, label="DWA trajektoria", zorder=6)
	status = map_ax.text(0.02, 0.98, "A* tervezes", transform=map_ax.transAxes, va="top", zorder=10)

	all_obstacles = static_obstacles + dynamic_obstacles
	obstacle_patches = [Circle((obstacle.x, obstacle.y), obstacle.radius, color="#d32f2f", alpha=0.65, zorder=5) for obstacle in all_obstacles]
	for patch in obstacle_patches:
		map_ax.add_patch(patch)

	map_ax.set_xlim(0, width * resolution)
	map_ax.set_ylim(0, height * resolution)
	map_ax.set_aspect("equal")
	map_ax.set_xlabel("x [m]")
	map_ax.set_ylabel("y [m]")
	map_ax.set_title("A* racs, DWA es mozgo akadalyak")
	map_ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), fontsize=8)

	trail_x = [state.x]
	trail_y = [state.y]
	last_movement_frame = -1
	last_result = None

	def priority_description(frame):
		if frame >= len(astar_result["search_steps"]):
			return "A* kesz\n\nDWA fazis\nmozgo akadalyak"
		step = astar_result["search_steps"][frame]
		return f"A* lepes: {frame + 1}\naktualis: {step['current']}\n\nprioritas\npozicio       f\n" + "\n".join(
			f"{item['position']!s:12s} {item['f']:6.2f}" for item in step.get("priority_queue", [])[:8]
		)

	def predict_local_path(best_pair):
		if best_pair is None:
			return [], []
		ghost = robotstate(x=state.x, y=state.y, irany=state.irany, w_L=state.w_L, w_R=state.w_R)
		local_x, local_y = [ghost.x], [ghost.y]
		for _ in range(int(config.predict_time / config.dt)):
			update(ghost, config, best_pair[2], best_pair[3], config.dt)
			local_x.append(ghost.x)
			local_y.append(ghost.y)
		return local_x, local_y

	def advance_robot_one_step():
		nonlocal last_result
		for obstacle in dynamic_obstacles:
			obstacle.move(config.dt)
		last_result = planner.plan_local(state, all_obstacles)
		best_pair = last_result["best_pair"] if last_result is not None else None
		if best_pair is None:
			update(state, config, 0.0, 0.0, config.dt)
		else:
			update(state, config, best_pair[2], best_pair[3], config.dt)
		trail_x.append(state.x)
		trail_y.append(state.y)

	def update_frame(frame):
		nonlocal last_movement_frame
		if frame < planning_frames:
			explored.set_offsets(expanded_world[:frame + 1])
			current_cell.set_offsets([expanded_world[frame]])
			waypoint.set_offsets([[math.nan, math.nan]])
			priority_text.set_text(priority_description(frame))
			status.set_text(f"A* tervezes: {frame + 1}/{planning_frames}")
			return

		if frame == movement_start - 1:
			explored.set_offsets(expanded_world)
			current_cell.set_offsets([[math.nan, math.nan]])
			priority_text.set_text(priority_description(len(astar_result["search_steps"])))
			status.set_text("A* kesz - DWA mozgas indul")
			return

		movement_frame = min(frame - movement_start, max_steps - 1)
		while last_movement_frame < movement_frame:
			advance_robot_one_step()
			last_movement_frame += 1
		if last_result is not None:
			active_waypoint = last_result["waypoint"]
			target = last_result["target"]
			waypoint.set_offsets([active_waypoint])
		else:
			active_waypoint = None
			target = None
		local_x, local_y = predict_local_path(last_result["best_pair"] if last_result else None)
		local_line.set_data(local_x, local_y)
		trail_line.set_data(trail_x, trail_y)
		robot.center = (state.x, state.y)
		for patch, obstacle in zip(obstacle_patches, all_obstacles):
			patch.center = (obstacle.x, obstacle.y)
			priority_text.set_text(f"DWA\nrobot: ({state.x:.2f}, {state.y:.2f})\nsebesseg: {state.v:.2f} m/s\nwaypointok: {len(planner.waypoints)}\naktualis: {active_waypoint}\nDWA cel: {target}")
		status.set_text("Cel elerve" if planner.reached_goal(state) else f"DWA mozgas: {movement_frame + 1}/{max_steps}")

	animation = FuncAnimation(figure, update_frame, frames=total_frames, interval=100, repeat=False, blit=False)
	figure._simulation_animation = animation
	if not auto_play:
		animation.event_source.stop()
		update_frame(0)
	if show:
		plt.show(block=True)
	return figure, animation


def run_simulation():
	"""A* stilusu egyszeru beallitasi ablakot nyit."""
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
		"inflation": ("Akadalyinflacio [m]", "0.1"),
			"alpha": ("Alfa - iranykovetes", "5"),
			"beta": ("Beta - akadalybiztonsag", "2"),
			"gamma": ("Gamma - sebesseg", "3"),
	}
	entries = {}
	for row, (name, (label, value)) in enumerate(fields.items()):
		ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w", padx=(0, 12), pady=4)
		entry = ttk.Entry(frame, width=18)
		entry.insert(0, value)
		entry.grid(row=row, column=1, pady=4)
		entries[name] = entry
	diagonal = tk.BooleanVar(value=True)
	auto_play = tk.BooleanVar(value=True)
	smooth = tk.BooleanVar(value=True)
	waypoint_slowdown = tk.BooleanVar(value=False)
	show_original_astar = tk.BooleanVar(value=False)
	heuristic = tk.StringVar(value="euclidean")
	tk.Checkbutton(frame, text="Atlos mozgas", variable=diagonal).grid(row=9, column=0, columnspan=2, sticky="w")
	tk.Checkbutton(frame, text="Automatikus lejatszas", variable=auto_play).grid(row=10, column=0, columnspan=2, sticky="w")
	tk.Checkbutton(frame, text="Bezier utvonal simitasa", variable=smooth).grid(row=11, column=0, columnspan=2, sticky="w")
	tk.Checkbutton(frame, text="Waypoint lassitas", variable=waypoint_slowdown).grid(row=12, column=0, columnspan=2, sticky="w")
	tk.Checkbutton(frame, text="Eredeti A* utvonal", variable=show_original_astar).grid(row=13, column=0, columnspan=2, sticky="w")
	tk.Label(frame, text="A* heurisztika").grid(row=14, column=0, sticky="w", pady=4)
	heuristic_box = ttk.Combobox(frame, textvariable=heuristic, values=("manhattan", "euclidean", "chebyshev", "octile"), state="readonly", width=16)
	heuristic_box.grid(row=14, column=1, pady=4)

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
				raise ValueError("A terkep merete es a felbontas legyen pozitiv.")
			if min(alpha, beta, gamma) < 0 or alpha + beta + gamma == 0:
				raise ValueError("A sullyok legyenek nem negativak, es legalabb egy legyen pozitiv.")
			if not (0 <= start_cell[0] < height and 0 <= start_cell[1] < width):
				raise ValueError("A start legyen a terkepen belul.")
			if not (0 <= goal_cell[0] < height and 0 <= goal_cell[1] < width):
				raise ValueError("A cel legyen a terkepen belul.")
			window.destroy()
			create_simulation(width, height, resolution, start_cell, goal_cell, diagonal.get(), heuristic.get(), inflation, smooth=smooth.get(), alpha=alpha, beta=beta, gamma=gamma, waypoint_slowdown=waypoint_slowdown.get(), show_original_astar=show_original_astar.get(), auto_play=auto_play.get(), show=True)
		except (TypeError, ValueError, RuntimeError) as error:
			messagebox.showerror("Hibas beallitas", str(error), parent=window)

	tk.Button(frame, text="Szimulacio inditasa", command=start).grid(row=15, column=0, columnspan=2, sticky="ew", pady=(12, 0))
	window.mainloop()


if __name__ == "__main__":
	run_simulation()
