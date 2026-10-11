"""Egyszeru matplotlib szimulacio az A* utvonal bemutatasahoz."""

import math
import tkinter as tk
from tkinter import messagebox, ttk

import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from matplotlib.widgets import Button

from .astar_baseline import astar_search
from .astar_variants import get_heuristic
from .grid_map import GridMap
from .path_smoothing import bezier_curve_points, smooth_path


def create_demo_map(
    width=30,
    height=20,
    resolution=0.2,
    robot_radius=0.08,
    start=(2, 2),
    goal=(17, 27),
):
    """Letrehoz egy ismert, statikus akadalyokat tartalmazo terkepet."""
    grid_map = GridMap(width=width, height=height, resolution=resolution)
    vertical_column = min(10, width - 2)
    horizontal_row = min(12, height - 2)
    vertical_wall = [
        (row, vertical_column)
        for row in range(2, max(2, height - 2))
        if row not in range(7, 13)
    ]
    horizontal_wall = [
        (horizontal_row, column)
        for column in range(12, max(12, width - 2))
        if column not in range(19, 25)
    ]
    for row, column in vertical_wall + horizontal_wall:
        if grid_map.is_inside(row, column) and (row, column) not in (start, goal):
            grid_map.add_obstacle(row, column)
    grid_map.inflate_obstacles(robot_radius)
    return grid_map, start, goal


def _parse_position(value):
    """Egy 'sor,oszlop' szoveget racskoordinatava alakit."""
    row, column = (int(part.strip()) for part in value.split(","))
    return row, column


def _read_settings(fields, diagonal, heuristic):
    """Beolvassa es ellenorzi a beallitasi ablak ertekeit."""
    get_value = lambda field: field.get() if hasattr(field, "get") else field.text
    heuristic_name = heuristic.get() if hasattr(heuristic, "get") else heuristic.value_selected
    diagonal_value = diagonal.get() if hasattr(diagonal, "get") else diagonal.get_status()[0]
    settings = {
        "width": int(get_value(fields["width"])),
        "height": int(get_value(fields["height"])),
        "resolution": float(get_value(fields["resolution"])),
        "robot_radius": float(get_value(fields["robot_radius"])),
        "start": _parse_position(get_value(fields["start"])),
        "goal": _parse_position(get_value(fields["goal"])),
        "diagonal": diagonal_value,
        "smooth_path": fields["smooth_path"].get(),
        "auto_play": fields["auto_play"].get(),
        "heuristic": get_heuristic(heuristic_name),
    }
    if settings["width"] < 3 or settings["height"] < 3:
        raise ValueError("A terkep legalabb 3 x 3 meretu legyen.")
    if settings["resolution"] <= 0 or settings["robot_radius"] < 0:
        raise ValueError("A felbontas pozitiv, a robotmeret nem negativ legyen.")
    return settings


def _create_settings_window(on_apply):
    """Letrehozza az A* bemeneti ertekeinek feluletet."""
    window = tk.Tk()
    window.title("A* beallitasok")
    window.resizable(False, False)
    main = ttk.Frame(window, padding=20)
    main.grid()
    ttk.Label(main, text="A* szimulacio", font=("Segoe UI", 16, "bold")).grid(
        row=0, column=0, columnspan=2, sticky="w", pady=(0, 16)
    )

    values = {
        "width": ("Szelesseg", "30"),
        "height": ("Magassag", "20"),
        "resolution": ("Felbontas [m]", "0.2"),
        "robot_radius": ("Robot sugar [m]", "0.08"),
        "start": ("Start (sor,oszlop)", "2,2"),
        "goal": ("Cel (sor,oszlop)", "17,27"),
    }
    fields = {}
    for index, (name, (label, value)) in enumerate(values.items()):
        row = index + 1
        ttk.Label(main, text=label).grid(row=row, column=0, sticky="w", padx=(0, 20), pady=5)
        field = ttk.Entry(main, width=24)
        field.insert(0, value)
        field.grid(row=row, column=1, sticky="ew", pady=5)
        fields[name] = field

    diagonal = tk.BooleanVar(value=True)
    ttk.Checkbutton(main, text="Atlos mozgas engedelyezese", variable=diagonal).grid(
        row=7, column=0, columnspan=2, sticky="w", pady=(12, 5)
    )
    ttk.Label(main, text="Heurisztika").grid(row=8, column=0, sticky="w", pady=5)
    heuristic = ttk.Combobox(
        main,
        values=["manhattan", "euclidean", "chebyshev", "octile"],
        state="readonly",
        width=21,
    )
    heuristic.set("euclidean")
    heuristic.grid(row=8, column=1, sticky="ew", pady=5)

    smooth_path_value = tk.BooleanVar(value=True)
    ttk.Checkbutton(
        main,
        text="Utvonal simitasa",
        variable=smooth_path_value,
    ).grid(row=9, column=0, columnspan=2, sticky="w", pady=5)
    fields["smooth_path"] = smooth_path_value

    auto_play_value = tk.BooleanVar(value=True)
    tk.Checkbutton(
        main,
        text="Automatikus lejatszas",
        variable=auto_play_value,
    ).grid(row=10, column=0, columnspan=2, sticky="w", pady=5)
    fields["auto_play"] = auto_play_value

    def apply_settings():
        try:
            settings = _read_settings(fields, diagonal, heuristic)
            window.destroy()
            on_apply(settings)
            plt.show()
        except (TypeError, ValueError, RuntimeError) as error:
            messagebox.showerror("Hibas beallitas", str(error), parent=window)

    ttk.Button(main, text="Szimulacio inditasa", command=apply_settings).grid(
        row=11, column=0, columnspan=2, sticky="ew", pady=(16, 0)
    )
    return window


def _safe_curve(grid_map, curve, diagonal):
    cells = [grid_map.world_to_grid(x, y) for x, y in curve]
    return all(
        grid_map.is_free(*cell)
        for cell in cells
    ) and all(
        current_next == current
        or current_next in grid_map.get_neighbors(*current, diagonal)
        for current, current_next in zip(cells, cells[1:])
    )


def create_robot_trajectory(
    grid_map, path, steps_per_cell=4, smooth=False, diagonal=False
):
    """Az A* cellautvonalabol koztes pontokat keszit az animaciohoz."""
    if not path:
        return []

    world_path = [grid_map.grid_to_world(row, column) for row, column in path]
    if smooth:
        curve = bezier_curve_points(world_path, samples_per_segment=20)
        if _safe_curve(grid_map, curve, diagonal):
            return curve

    trajectory = [world_path[0]]
    for start, end in zip(world_path, world_path[1:]):
        for step in range(1, steps_per_cell + 1):
            ratio = step / steps_per_cell
            trajectory.append(
                (
                    start[0] + ratio * (end[0] - start[0]),
                    start[1] + ratio * (end[1] - start[1]),
                )
            )
    return trajectory


def draw_map(ax, grid_map, start, goal):
    """Kirajzolja a terkepet es a start-cel pontokat."""
    for row in range(grid_map.height):
        for column in range(grid_map.width):
            if grid_map.grid[row][column] != 1:
                continue
            ax.add_patch(
                Rectangle(
                    (column * grid_map.resolution, row * grid_map.resolution),
                    grid_map.resolution,
                    grid_map.resolution,
                    facecolor="#444444",
                    edgecolor="white",
                    linewidth=0.3,
                )
            )

    start_x, start_y = grid_map.grid_to_world(*start)
    goal_x, goal_y = grid_map.grid_to_world(*goal)
    ax.scatter(start_x, start_y, color="#16803c", s=70, label="Start", zorder=4)
    ax.scatter(goal_x, goal_y, color="#c62828", s=70, label="Cel", zorder=4)
    ax.set_xlim(0, grid_map.width * grid_map.resolution)
    ax.set_ylim(0, grid_map.height * grid_map.resolution)
    ax.set_aspect("equal")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_xticks(
        [
            grid_map.origin_x + column * grid_map.resolution
            for column in range(grid_map.width + 1)
        ],
        minor=True,
    )
    ax.set_yticks(
        [
            grid_map.origin_y + row * grid_map.resolution
            for row in range(grid_map.height + 1)
        ],
        minor=True,
    )
    ax.grid(True, which="minor", color="#9e9e9e", alpha=0.5, linewidth=0.5)
    ax.grid(True, which="major", alpha=0.2)


def _priority_text(search_steps, frame):
    """Rovid szoveges tablazat az aktualis prioritasi sorrol."""
    if frame >= len(search_steps):
        return "A* kesz\n\nA robot koveti\na kivalasztott utvonalat."

    step = search_steps[frame]
    lines = [
        f"Lepes: {frame + 1}",
        f"Aktualis: {step['current']}",
        "",
        "pozicio       g     h     f",
    ]
    for index, item in enumerate(step.get("priority_queue", [])[:8], start=1):
        lines.append(
            f"{index:2d}. {str(item['position']):9s} "
            f"{item['g']:5.1f} {item['h']:5.1f} {item['f']:5.1f}"
        )
    if len(lines) == 4:
        lines.append("(ures prioritasi sor)")
    return "\n".join(lines)


def plot_simulation(
    grid_map,
    path,
    trajectory,
    start,
    goal,
    expanded_nodes=None,
    search_steps=None,
    original_path=None,
    robot_radius=0.08,
    planning_interval=200,
    movement_interval=50,
    auto_play=False,
    show=True,
    smoothed=False,
):
    """A* es robotmozgasi abra kezi vagy automatikus lejatszassal."""
    expanded_nodes = expanded_nodes or []
    search_steps = search_steps or []
    figure, (priority_ax, map_ax) = plt.subplots(
        1, 2, figsize=(13, 6), gridspec_kw={"width_ratios": (1.35, 2.4)}
    )
    figure.subplots_adjust(bottom=0.14, right=0.82, wspace=0.12)

    priority_ax.set_title("Prioritasi sor")
    priority_ax.set_axis_off()
    priority_ax.text(
        0.02,
        0.98,
        "A* prioritasi keplet",
        va="top",
        fontsize=10,
        fontweight="bold",
        color="#263238",
    )
    priority_ax.text(
        0.02,
        0.88,
        "f(n) = g(n) + h(n)\n\n"
        "g: eddigi ut koltsege\n"
        "h: becsult tavolsag a celig\n"
        "f: teljes prioritasi ertek\n\n"
        "Euklideszi h(n):\n"
        "h(n) = sqrt(dr^2 + dc^2)\n"
        "dr = |goal_row - row|\n"
        "dc = |goal_col - col|\n\n"
        "Pelda: dr=15, dc=25\n"
        "h(n) = sqrt(15^2 + 25^2) = 29.15\n\n"
        "Egyenes = 1.0 | Atlos = 1.41\n"
        "resolution = 0.2 m | robot = 0.08 m",
        va="top",
        family="monospace",
        fontsize=8,
        color="#263238",
        linespacing=1.35,
    )
    priority_text = priority_ax.text(
        0.02,
        0.31,
        "",
        va="top",
        family="monospace",
        fontsize=7.5,
        color="#004d40",
        linespacing=1.25,
    )
    draw_map(map_ax, grid_map, start, goal)
    map_ax.set_title("A* utvonal es Bezier-simitas")

    expanded_world = [grid_map.grid_to_world(*cell) for cell in expanded_nodes]
    path_world = [grid_map.grid_to_world(*cell) for cell in path]
    original_world = [
        grid_map.grid_to_world(*cell) for cell in (original_path or path)
    ]
    display_path = trajectory if smoothed else path_world
    path_x, path_y = zip(*display_path)
    original_x, original_y = zip(*original_world)
    original_line, = map_ax.plot(
        original_x,
        original_y,
        ":",
        color="#9e9e9e",
        linewidth=2,
        label="Eredeti A* utvonal",
        visible=False,
        zorder=2,
    )
    path_line, = map_ax.plot(
        path_x,
        path_y,
        "-",
        color="#ef8a8a",
        linewidth=2.0,
        alpha=0.8,
        label="Bezier-simitott utvonal",
        visible=False,
        zorder=3,
    )
    explored = map_ax.scatter(
        [], [], s=28, color="#90caf9", alpha=0.6, label="Vizsgalt cellak"
    )
    current_search = map_ax.scatter(
        [], [], s=90, color="#ff9800", edgecolors="#e65100",
        label="C: aktualis cella", zorder=5
    )
    robot = Circle(
        (math.nan, math.nan), robot_radius, color="#e65100", label="Robot", zorder=6
    )
    map_ax.add_patch(robot)
    trail, = map_ax.plot([], [], color="#f57c00", linewidth=2, label="Robot nyoma")
    status = map_ax.text(0.02, 0.98, "Indulas", transform=map_ax.transAxes, va="top")
    map_ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), borderaxespad=0)

    trajectory_x = [point[0] for point in trajectory]
    trajectory_y = [point[1] for point in trajectory]
    planning_frames = len(expanded_world)
    movement_start = planning_frames + 1
    total_frames = movement_start + len(trajectory)
    current_frame = 0

    def update(frame):
        nonlocal current_frame
        current_frame = frame
        if frame < planning_frames:
            explored.set_offsets(expanded_world[: frame + 1])
            current_search.set_offsets([expanded_world[frame]])
            priority_text.set_text(_priority_text(search_steps, frame))
            status.set_text(f"A* tervezes: {frame + 1}/{planning_frames}")
            path_line.set_visible(False)
            original_line.set_visible(False)
            robot.center = (math.nan, math.nan)
            trail.set_data([], [])
        elif frame == movement_start - 1:
            explored.set_offsets(expanded_world or [[math.nan, math.nan]])
            current_search.set_offsets([[math.nan, math.nan]])
            priority_text.set_text(_priority_text(search_steps, len(search_steps)))
            status.set_text("A* kesz - robotmozgas indul")
            original_line.set_visible(True)
            path_line.set_visible(True)
            robot.center = (math.nan, math.nan)
            trail.set_data([], [])
        else:
            movement_frame = min(frame - movement_start, len(trajectory) - 1)
            explored.set_offsets(expanded_world or [[math.nan, math.nan]])
            current_search.set_offsets([[math.nan, math.nan]])
            priority_text.set_text(_priority_text(search_steps, len(search_steps)))
            original_line.set_visible(True)
            path_line.set_visible(True)
            robot.center = (trajectory_x[movement_frame], trajectory_y[movement_frame])
            trail.set_data(trajectory_x[: movement_frame + 1], trajectory_y[: movement_frame + 1])
            status.set_text(
                "Cel elerve" if movement_frame == len(trajectory) - 1
                else f"Robotmozgas: {movement_frame + 1}/{len(trajectory)}"
            )
        return (
            explored,
            current_search,
            original_line,
            path_line,
            robot,
            trail,
            status,
            priority_text,
        )

    robot_animation = animation.FuncAnimation(
        figure,
        update,
        frames=total_frames,
        interval=planning_interval,
        repeat=False,
        blit=False,
    )

    if not auto_play and robot_animation.event_source is not None:
        robot_animation.event_source.stop()
        update(0)

    next_button = Button(figure.add_axes((0.68, 0.035, 0.13, 0.06)), "Kovetkezo")
    reset_button = Button(figure.add_axes((0.83, 0.035, 0.13, 0.06)), "Ujrakezdes")

    def next_frame(_event=None):
        nonlocal current_frame
        current_frame = min(current_frame + 1, total_frames - 1)
        update(current_frame)
        figure.canvas.draw_idle()

    def reset_simulation(_event=None):
        nonlocal current_frame
        current_frame = 0
        update(current_frame)
        figure.canvas.draw_idle()

    next_button.on_clicked(next_frame)
    reset_button.on_clicked(reset_simulation)
    figure._astar_animation = robot_animation
    figure._astar_controls = (next_button, reset_button)
    figure._astar_next_frame = next_frame
    figure._astar_reset = reset_simulation
    figure.canvas.mpl_connect(
        "key_press_event",
        lambda event: next_frame() if event.key in ("right", " ") else None,
    )
    if show:
        plt.show()
    return figure, robot_animation


def _run_simulation(settings, show=True):
    """A megadott beallitasokkal lefuttatja a szimulaciot."""
    grid_map, start, goal = create_demo_map(
        width=settings["width"],
        height=settings["height"],
        resolution=settings["resolution"],
        robot_radius=settings["robot_radius"],
        start=settings["start"],
        goal=settings["goal"],
    )
    result = astar_search(
        grid_map,
        start,
        goal,
        diagonal=settings["diagonal"],
        heuristic=settings["heuristic"],
        return_details=True,
    )
    if result["path"] is None:
        raise RuntimeError("A demo terkepen nincs elerheto utvonal.")
    original_path = result["path"]
    path = original_path
    if settings["smooth_path"]:
        path = smooth_path(grid_map, path, settings["diagonal"])
    trajectory = create_robot_trajectory(
        grid_map,
        path,
        smooth=settings["smooth_path"],
        diagonal=settings["diagonal"],
    )
    return plot_simulation(
        grid_map,
        path,
        trajectory,
        start,
        goal,
        expanded_nodes=result["expanded_nodes"],
        search_steps=result["search_steps"],
        original_path=original_path,
        auto_play=settings["auto_play"],
        show=show,
        smoothed=settings["smooth_path"],
    )


def run_simulation(show=True):
    """Beallitasi ablakot nyit, majd elinditja az A* szimulaciot."""
    simulation_figure = [None]

    def apply_settings(settings):
        if simulation_figure[0] is not None:
            plt.close(simulation_figure[0])
        simulation_figure[0], _ = _run_simulation(settings, show=False)

    settings_figure = _create_settings_window(apply_settings)
    if show:
        settings_figure.mainloop()
    return settings_figure


if __name__ == "__main__":
    run_simulation()