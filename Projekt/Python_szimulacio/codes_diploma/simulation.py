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

        # 1. Jósolt szakasz (Trajectory rollout)
        ghost = robotstate(
            x=state.x, y=state.y, irany=state.irany, w_L=state.w_L, w_R=state.w_R
        )
        path_points = [(ghost.x, ghost.y)]
        for _ in range(predict_steps):
            update(ghost, config, w_L, w_R, config.dt)
            path_points.append((ghost.x, ghost.y))

        # 2. Fékezési szakasz a jósolt szakasz legvégétől indítva (önlabos képlet)
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

        # 3. Szétválogatás
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

    # 1. Bézier útvonal: zorder=4, de alpha=0.55-tel áttetsző, hogy ne takarja el az A*-ot
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

# Vékony, finom szaggatott vonal apró csomóponti pontokkal a Bézier felett
    (astar_line,) = map_ax.plot(
        astar_x,
        astar_y,
        linestyle="--",
        dashes=(3, 2),        # Sűrűbb, rövidebb szaggatás a finomabb megjelenéshez
        marker="o",
        markersize=2.0,       # Apró, finom pontok
        color="#0a22a7",      # Élénk narancs a jó kontrasztért
        linewidth=1.0,        # Vékony vonalvastagság (korábbi 1.8 helyett)
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

    # Összes pálya és fékezési szakaszok az önlabos megjelenítés szerint
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
