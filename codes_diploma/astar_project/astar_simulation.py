"""Egyszeru matplotlib szimulacio az A* utvonal bemutatasahoz."""

import math

import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from matplotlib.widgets import Button

from .astar_baseline import astar_search
from .grid_map import GridMap


def create_demo_map():
    """Letrehoz egy ismert, statikus akadalyokat tartalmazo terkepet."""
    grid_map = GridMap(width=30, height=20, resolution=0.2)
    robot_radius = 0.08

    vertical_wall = [(row, 10) for row in range(2, 18) if row not in range(7, 13)]
    horizontal_wall = [
        (12, column) for column in range(12, 28) if column not in range(19, 25)
    ]

    for row, column in vertical_wall + horizontal_wall:
        grid_map.add_obstacle(row, column)

    grid_map.inflate_obstacles(robot_radius)

    start = (2, 2)
    goal = (17, 27)
    return grid_map, start, goal


def create_robot_trajectory(grid_map, path, steps_per_cell=8):
    """Cellakozeppontok kozott egyenletes robottrajektoriat keszit."""
    if not path:
        return []

    world_path = [grid_map.grid_to_world(row, column) for row, column in path]
    trajectory = [world_path[0]]

    for (start_x, start_y), (goal_x, goal_y) in zip(
        world_path,
        world_path[1:],
    ):
        for step in range(1, steps_per_cell + 1):
            ratio = step / steps_per_cell
            x = start_x + ratio * (goal_x - start_x)
            y = start_y + ratio * (goal_y - start_y)
            trajectory.append((x, y))

    return trajectory


def draw_map(ax, grid_map, start, goal):
    """Kirajzolja a terkepet lathato cellaraccsal."""
    for row in range(grid_map.height):
        for column in range(grid_map.width):
            if grid_map.grid[row][column] != 1:
                continue

            x = grid_map.origin_x + column * grid_map.resolution
            y = grid_map.origin_y + row * grid_map.resolution
            ax.add_patch(
                Rectangle(
                    (x, y),
                    grid_map.resolution,
                    grid_map.resolution,
                    facecolor="#444444",
                    edgecolor="white",
                    linewidth=0.3,
                )
            )

    start_x, start_y = grid_map.grid_to_world(*start)
    goal_x, goal_y = grid_map.grid_to_world(*goal)
    ax.scatter(start_x, start_y, color="#16803c", s=80, label="Start", zorder=5)
    ax.scatter(goal_x, goal_y, color="#c62828", s=80, label="Cel", zorder=5)

    map_width = grid_map.width * grid_map.resolution
    map_height = grid_map.height * grid_map.resolution
    ax.set_xlim(grid_map.origin_x, grid_map.origin_x + map_width)
    ax.set_ylim(grid_map.origin_y, grid_map.origin_y + map_height)
    ax.set_aspect("equal")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    x_grid = [
        grid_map.origin_x + column * grid_map.resolution
        for column in range(grid_map.width + 1)
    ]
    y_grid = [
        grid_map.origin_y + row * grid_map.resolution
        for row in range(grid_map.height + 1)
    ]
    ax.set_xticks(x_grid, minor=True)
    ax.set_yticks(y_grid, minor=True)
    ax.grid(True, which="minor", color="#9e9e9e", alpha=0.45, linewidth=0.5)
    ax.grid(True, which="major", alpha=0.2)


def plot_simulation(
    grid_map,
    path,
    trajectory,
    start,
    goal,
    expanded_nodes=None,
    search_steps=None,
    robot_radius=0.08,
    planning_interval=650,
    movement_interval=140,
    show=True,
):
    """Megjeleniti az A* tervezest, majd a robot mozgasat."""
    figure = plt.figure(figsize=(14, 7))
    grid = figure.add_gridspec(1, 2, width_ratios=(1.05, 2.5))
    priority_axes = figure.add_subplot(grid[0, 0])
    axes = figure.add_subplot(grid[0, 1])
    figure.subplots_adjust(left=0.04, right=0.98, bottom=0.14, wspace=0.08)
    draw_map(axes, grid_map, start, goal)

    if expanded_nodes is None:
        expanded_nodes = []
    if search_steps is None:
        search_steps = []

    priority_axes.set_title("Prioritási sor", fontsize=12, pad=10)
    priority_axes.set_xticks([])
    priority_axes.set_yticks([])
    priority_axes.set_xlim(0, 1)
    priority_axes.set_ylim(0, 1)
    priority_axes.set_facecolor("#f4f7f9")
    priority_text = priority_axes.text(
        0.04,
        0.96,
        "",
        transform=priority_axes.transAxes,
        family="monospace",
        fontsize=8,
        color="#263238",
        va="top",
        linespacing=1.45,
    )

    expanded_world = [
        grid_map.grid_to_world(row, column)
        for row, column in expanded_nodes
    ]
    explored = axes.scatter(
        [],
        [],
        s=32,
        color="#90caf9",
        alpha=0.45,
        label="X: vizsgalt cella",
        zorder=2,
    )
    exploration_trace, = axes.plot(
        [],
        [],
        color="#5c6bc0",
        linewidth=0.9,
        alpha=0.3,
        label="Vizsgalati sorrend",
        zorder=1,
    )
    current_search = axes.scatter(
        [],
        [],
        s=90,
        color="#ff9800",
        edgecolors="#e65100",
        label="C: aktualis cella",
        zorder=5,
    )
    neighbor_candidates = axes.scatter(
        [],
        [],
        s=55,
        facecolors="none",
        edgecolors="#00897b",
        linewidths=1.2,
        label="N: vizsgalt szomszedjeloltek",
        zorder=4,
    )
    neighbor_links, = axes.plot(
        [],
        [],
        color="#26a69a",
        linewidth=0.8,
        alpha=0.7,
        zorder=2,
    )

    path_world = [grid_map.grid_to_world(row, column) for row, column in path]
    path_x = [position[0] for position in path_world]
    path_y = [position[1] for position in path_world]
    path_line, = axes.plot(
        path_x,
        path_y,
        "--",
        color="#1976d2",
        linewidth=1.5,
        label="O: vegso utvonal",
        zorder=3,
    )
    path_line.set_visible(False)

    expanded_labels = [
        axes.text(
            x,
            y,
            "X",
            color="#283593",
            fontsize=6,
            ha="center",
            va="center",
            visible=False,
            zorder=4,
        )
        for x, y in expanded_world
    ]
    path_labels = [
        axes.text(
            x,
            y,
            "O",
            color="#0d47a1",
            fontsize=7,
            fontweight="bold",
            ha="center",
            va="center",
            visible=False,
            zorder=4,
        )
        for x, y in path_world
    ]
    current_label = axes.text(
        math.nan,
        math.nan,
        "C",
        color="#bf360c",
        fontsize=8,
        fontweight="bold",
        ha="center",
        va="center",
        visible=False,
        zorder=7,
    )
    neighbor_labels = [
        axes.text(
            math.nan,
            math.nan,
            "",
            color="#00695c",
            fontsize=6,
            ha="center",
            va="center",
            visible=False,
            zorder=5,
        )
        for _ in range(8)
    ]

    trail, = axes.plot([], [], color="#f57c00", linewidth=2, label="Robot nyoma")
    robot = Circle(
        (math.nan, math.nan),
        radius=robot_radius,
        facecolor="#e65100",
        edgecolor="#7f2704",
        alpha=0.85,
        label="Robot",
        zorder=6,
    )
    axes.add_patch(robot)
    status = axes.text(0.02, 0.98, "Indulas", transform=axes.transAxes, va="top")
    decision_text = axes.text(
        0.02,
        0.86,
        "",
        transform=axes.transAxes,
        fontsize=8,
        color="#004d40",
        va="top",
        bbox={"facecolor": "white", "alpha": 0.8, "edgecolor": "none"},
    )
    axes.text(
        0.02,
        0.92,
        "X = vizsgalt | C = aktualis | N = szomszed | O = vegso utvonal",
        transform=axes.transAxes,
        fontsize=8,
        color="#263238",
        va="top",
        bbox={"facecolor": "white", "alpha": 0.75, "edgecolor": "none"},
    )
    axes.legend(loc="upper right")
    axes.set_title("A* tervezes es robotmozgas ismert, statikus terkepen")

    trajectory_x = [position[0] for position in trajectory]
    trajectory_y = [position[1] for position in trajectory]

    planning_frames = len(expanded_world)
    planning_pause_frames = 8
    movement_start = planning_frames + planning_pause_frames
    total_frames = movement_start + len(trajectory)

    def set_explored_points(points):
        if points:
            explored.set_offsets(points)
        else:
            explored.set_offsets([[math.nan, math.nan]])

    def set_label_visibility(labels, count):
        for index, label in enumerate(labels):
            label.set_visible(index < count)

    def set_current_label(position, visible):
        current_label.set_position(position)
        current_label.set_visible(visible)

    def set_priority_panel(frame):
        if frame < planning_frames and frame < len(search_steps):
            step = search_steps[frame]
            priority_rows = step.get("priority_queue", [])
            lines = [
                f"Lépés: {frame + 1}/{planning_frames}",
                f"Aktuális C: {step['current']}",
                "",
                "Sorrend: legkisebb f elöl",
                "pozíció       g     h     f",
                "--------------------------------",
            ]
            for index, row in enumerate(priority_rows[:16], start=1):
                marker = ">>" if index == 1 else "  "
                lines.append(
                    f"{marker}{index:2d}. {str(row['position']):9s} "
                    f"{row['g']:5.1f} {row['h']:5.1f} {row['f']:5.1f}"
                )
            if not priority_rows:
                lines.append("(üres prioritási sor)")
            priority_text.set_text("\n".join(lines))
        elif frame < movement_start:
            priority_text.set_text(
                "A* tervezés kész\n\n"
                "A kék O vonal a\n"
                "visszaépített útvonal."
            )
        else:
            priority_text.set_text(
                "Robotmozgás\n\n"
                "A robot most az O\n"
                "útvonalat követi."
            )

    def set_neighbors(step_index):
        if step_index >= len(search_steps):
            neighbors = []
        else:
            step = search_steps[step_index]
            neighbors = step["neighbors"]
            neighbor_scores = step.get("neighbor_scores", [])

        neighbor_world = [
            grid_map.grid_to_world(row, column)
            for row, column in neighbors
        ]
        if neighbor_world:
            neighbor_candidates.set_offsets(neighbor_world)
            current_position = search_steps[step_index]["current"]
            current_world = grid_map.grid_to_world(*current_position)
            link_x = []
            link_y = []
            for neighbor_x, neighbor_y in neighbor_world:
                link_x.extend([current_world[0], neighbor_x, math.nan])
                link_y.extend([current_world[1], neighbor_y, math.nan])
            neighbor_links.set_data(link_x, link_y)
        else:
            neighbor_candidates.set_offsets([[math.nan, math.nan]])
            neighbor_links.set_data([], [])

        for index, label in enumerate(neighbor_labels):
            if index < len(neighbor_world):
                label.set_position(neighbor_world[index])
                score = neighbor_scores[index] if index < len(neighbor_scores) else {}
                label.set_text(
                    "N\n"
                    f"g={score.get('g', 0):.1f} "
                    f"h={score.get('h', 0):.1f}\n"
                    f"f={score.get('f', 0):.1f}"
                )
                label.set_visible(True)
            else:
                label.set_visible(False)

        if step_index < len(search_steps):
            step = search_steps[step_index]
            score_text = ", ".join(
                f"{score['position']} f={score['f']:.1f}"
                for score in step.get("neighbor_scores", [])
            )
            next_position = step.get("next_position")
            decision_text.set_text(
                f"C={step['current']}  "
                f"g={step.get('current_g', 0):.1f} "
                f"h={step.get('current_h', 0):.1f} "
                f"f={step.get('current_f', 0):.1f}\n"
                f"Jeloltek f-szerint: {score_text}\n"
                f"Kovetkezo prioritasi cella: {next_position}"
            )
        else:
            decision_text.set_text("")

    def update(frame):
        if frame < planning_frames:
            visible_nodes = expanded_world[: frame + 1]
            set_explored_points(visible_nodes)
            exploration_trace.set_data(
                [point[0] for point in visible_nodes],
                [point[1] for point in visible_nodes],
            )
            set_label_visibility(expanded_labels, 0)
            set_label_visibility(path_labels, 0)
            set_neighbors(frame)
            set_priority_panel(frame)
            current_search.set_offsets([expanded_world[frame]])
            current_step = search_steps[frame]
            current_label.set_text(
                "C\n"
                f"f={current_step.get('current_f', 0):.1f}"
            )
            set_current_label(expanded_world[frame], True)
            path_line.set_visible(False)
            robot.center = (math.nan, math.nan)
            trail.set_data([], [])
            status.set_text(
                f"A* tervezes: {frame + 1}/{planning_frames} cella vizsgalva"
            )
        elif frame < movement_start:
            set_explored_points(expanded_world)
            exploration_trace.set_data(
                [point[0] for point in expanded_world],
                [point[1] for point in expanded_world],
            )
            set_label_visibility(expanded_labels, 0)
            set_label_visibility(path_labels, len(path_labels))
            set_neighbors(len(search_steps))
            set_priority_panel(frame)
            decision_text.set_text("A* kesz: az O jelolesu utvonal a visszaepitett legjobb ut.")
            current_search.set_offsets([[math.nan, math.nan]])
            set_current_label((math.nan, math.nan), False)
            path_line.set_visible(True)
            robot.center = (math.nan, math.nan)
            trail.set_data([], [])
            status.set_text("A* tervezes kesz - utvonal indul")
        else:
            simulation_frame = frame - movement_start
            set_explored_points(expanded_world)
            exploration_trace.set_data(
                [point[0] for point in expanded_world],
                [point[1] for point in expanded_world],
            )
            set_label_visibility(expanded_labels, 0)
            set_label_visibility(path_labels, len(path_labels))
            set_neighbors(len(search_steps))
            set_priority_panel(frame)
            decision_text.set_text("A* kesz: az O jelolesu utvonalon mozog a robot.")
            current_search.set_offsets([[math.nan, math.nan]])
            set_current_label((math.nan, math.nan), False)
            path_line.set_visible(True)
            robot.center = (
                trajectory_x[simulation_frame],
                trajectory_y[simulation_frame],
            )
            trail.set_data(
                trajectory_x[: simulation_frame + 1],
                trajectory_y[: simulation_frame + 1],
            )
            if simulation_frame == len(trajectory) - 1:
                status.set_text("A* utvonal kesz - cel elerve")
            else:
                status.set_text(
                    "Robot mozgas: "
                    f"{simulation_frame + 1}/{len(trajectory)}"
                )
        return (
            explored,
            exploration_trace,
            current_search,
            neighbor_candidates,
            neighbor_links,
            path_line,
            robot,
            trail,
            status,
            current_label,
            decision_text,
            priority_text,
            *neighbor_labels,
            *expanded_labels,
            *path_labels,
        )

    robot_animation = animation.FuncAnimation(
        figure,
        update,
        frames=total_frames,
        interval=planning_interval,
        repeat=False,
        blit=False,
    )

    figure.canvas.mpl_disconnect(robot_animation._first_draw_id)
    robot_animation.event_source.stop()
    figure._astar_animation = robot_animation
    manual_frame = 0
    update(manual_frame)

    next_button_axes = figure.add_axes((0.68, 0.035, 0.13, 0.06))
    reset_button_axes = figure.add_axes((0.83, 0.035, 0.13, 0.06))
    next_button = Button(next_button_axes, "Következő")
    reset_button = Button(reset_button_axes, "Újrakezdés")

    def next_frame(_event=None):
        nonlocal manual_frame
        manual_frame = min(manual_frame + 1, total_frames - 1)
        update(manual_frame)
        figure.canvas.draw()

    def reset_simulation(_event=None):
        nonlocal manual_frame
        manual_frame = 0
        update(manual_frame)
        figure.canvas.draw()

    next_button.on_clicked(next_frame)
    reset_button.on_clicked(reset_simulation)
    figure._astar_controls = (next_button, reset_button)
    figure._astar_next_frame = next_frame
    figure._astar_reset = reset_simulation

    figure.canvas.mpl_connect(
        "key_press_event",
        lambda event: next_frame() if event.key in ("right", " ") else None,
    )
    figure.canvas.draw()
    robot_animation._draw_was_started = True

    if show:
        plt.show()

    return figure, robot_animation


def run_simulation(show=True):
    """A teljes demo szimulacio futtatasa."""
    grid_map, start, goal = create_demo_map()
    search_result = astar_search(
        grid_map,
        start,
        goal,
        diagonal=True,
        return_details=True,
    )
    path = search_result["path"]

    if path is None:
        raise RuntimeError("A demo terkepen nem talalhato utvonal.")

    trajectory = create_robot_trajectory(grid_map, path)
    return plot_simulation(
        grid_map,
        path,
        trajectory,
        start,
        goal,
        expanded_nodes=search_result["expanded_nodes"],
        search_steps=search_result["search_steps"],
        show=show,
    )


if __name__ == "__main__":
    run_simulation()
