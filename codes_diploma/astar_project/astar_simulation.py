"""Egyszeru matplotlib szimulacio az A* utvonal bemutatasahoz."""

import math

import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

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
    robot_radius=0.08,
    show=True,
):
    """Megjeleniti az A* tervezest, majd a robot mozgasat."""
    figure, axes = plt.subplots(figsize=(10, 6))
    draw_map(axes, grid_map, start, goal)

    if expanded_nodes is None:
        expanded_nodes = []

    expanded_world = [
        grid_map.grid_to_world(row, column)
        for row, column in expanded_nodes
    ]
    explored = axes.scatter(
        [],
        [],
        s=28,
        color="#90caf9",
        alpha=0.75,
        label="A* vizsgalt cellak",
        zorder=2,
    )

    path_world = [grid_map.grid_to_world(row, column) for row, column in path]
    path_x = [position[0] for position in path_world]
    path_y = [position[1] for position in path_world]
    axes.plot(
        path_x,
        path_y,
        "--",
        color="#1976d2",
        linewidth=1.5,
        label="A* utvonal",
        zorder=3,
    )

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
    axes.legend(loc="upper right")
    axes.set_title("A* tervezes es robotmozgas ismert, statikus terkepen")

    trajectory_x = [position[0] for position in trajectory]
    trajectory_y = [position[1] for position in trajectory]

    planning_frames = len(expanded_world)
    total_frames = planning_frames + len(trajectory)

    def set_explored_points(points):
        if points:
            explored.set_offsets(points)
        else:
            explored.set_offsets([[math.nan, math.nan]])

    def update(frame):
        if frame < planning_frames:
            visible_nodes = expanded_world[: frame + 1]
            set_explored_points(visible_nodes)
            robot.center = (math.nan, math.nan)
            trail.set_data([], [])
            status.set_text(
                f"A* tervezes: {frame + 1}/{planning_frames} cella vizsgalva"
            )
        else:
            simulation_frame = frame - planning_frames
            set_explored_points(expanded_world)
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
        return explored, robot, trail, status

    robot_animation = animation.FuncAnimation(
        figure,
        update,
        frames=total_frames,
        interval=80,
        repeat=False,
        blit=True,
    )

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
        show=show,
    )


if __name__ == "__main__":
    run_simulation()
