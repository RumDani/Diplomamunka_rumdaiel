"""A valodi A*+DWA szimulacios terkep osszehasonlito abrazolasa."""

import importlib.util
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.patheffects as patheffects
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from .astar_variants import HEURISTICS, get_heuristic
from .experiments import _path_cost
from .. import simulation


COLORS = {
    "manhattan": "#0057B8",
    "euclidean": "#F28E00",
    "chebyshev": "#009E73",
    "octile": "#D81B60",
}

LINESTYLES = {
    "manhattan": "-",
    "euclidean": "--",
    "chebyshev": "-.",
    "octile": ":",
}


def _load_planner_class():
    file_path = Path(simulation.__file__).with_name("DWA+A.py")
    spec = importlib.util.spec_from_file_location("dwa_a_comparison", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.AStarDWAPlanner


def _draw_map(axis, grid_map):
    for row in range(grid_map.height):
        for column in range(grid_map.width):
            if grid_map.grid[row][column] == 1:
                axis.add_patch(
                    Rectangle(
                        (
                            column * grid_map.resolution,
                            row * grid_map.resolution,
                        ),
                        grid_map.resolution,
                        grid_map.resolution,
                        facecolor="#455A64",
                        edgecolor="none",
                        zorder=1,
                    )
                )
    for row in range(grid_map.height + 1):
        axis.axhline(
            row * grid_map.resolution,
            color="#78909C",
            linewidth=0.65,
            alpha=0.75,
            zorder=0,
        )
    for column in range(grid_map.width + 1):
        axis.axvline(
            column * grid_map.resolution,
            color="#78909C",
            linewidth=0.65,
            alpha=0.75,
            zorder=0,
        )


def _draw_paths(axis, grid_map, start_cell, goal_cell, diagonal):
    for heuristic_name in HEURISTICS:
        _draw_path(
            axis,
            grid_map,
            start_cell,
            goal_cell,
            diagonal,
            heuristic_name,
        )


def _draw_path(axis, grid_map, start_cell, goal_cell, diagonal, heuristic_name):
    planner_class = _load_planner_class()
    start = grid_map.grid_to_world(*start_cell)
    goal = grid_map.grid_to_world(*goal_cell)
    heuristic = get_heuristic(heuristic_name)
    planner = planner_class(
        grid_map,
        config=simulation.robotconfig(),
        diagonal=diagonal,
    )
    path = planner.plan_global(
        start,
        goal,
        heuristic=heuristic,
        smooth=False,
    )
    if path:
        path_x, path_y = zip(*path)
        grid_path = [grid_map.world_to_grid(x, y) for x, y in path]
        cost = _path_cost(grid_path)
        axis.plot(
            path_x,
            path_y,
            color=COLORS[heuristic_name],
            linestyle=LINESTYLES[heuristic_name],
            linewidth=2.8,
            alpha=1.0,
            marker="o",
            markersize=2.8,
            markeredgewidth=0.7,
            markeredgecolor="#FFFFFF",
            label=f"{heuristic_name.title()}: {cost:.2f}",
            zorder=4,
            path_effects=[
                patheffects.Stroke(linewidth=5.0, foreground="#FFFFFF"),
                patheffects.Normal(),
            ],
        )


def main():
    grid_map, start_cell, goal_cell, *_ = simulation.create_scene(
        width=30,
        height=20,
        resolution=0.2,
        start_cell=(2, 2),
        goal_cell=(17, 27),
        inflation_radius=0.1,
    )
    matplotlib.use("Agg", force=True)
    figure, axes = plt.subplots(1, 2, figsize=(17, 8), dpi=180)
    for axis, diagonal, title in (
        (axes[0], False, "Négyirányú A* + DWA"),
        (axes[1], True, "Átlós A* + DWA"),
    ):
        _draw_map(axis, grid_map)
        _draw_paths(axis, grid_map, start_cell, goal_cell, diagonal)
        start_x, start_y = grid_map.grid_to_world(*start_cell)
        goal_x, goal_y = grid_map.grid_to_world(*goal_cell)
        axis.scatter(
            [start_x],
            [start_y],
            s=90,
            color="#00A651",
            edgecolors="white",
            linewidths=1.5,
            zorder=6,
        )
        axis.scatter(
            [goal_x],
            [goal_y],
            s=110,
            marker="*",
            color="#E31B23",
            edgecolors="white",
            linewidths=1.2,
            zorder=6,
        )
        axis.set_title(title, fontsize=15, weight="bold")
        axis.set_xlabel("x [m]")
        axis.set_ylabel("y [m]")
        axis.set_xlim(0, grid_map.width * grid_map.resolution)
        axis.set_ylim(0, grid_map.height * grid_map.resolution)
        axis.set_aspect("equal")
        axis.legend(
            loc="upper center",
            bbox_to_anchor=(0.5, -0.10),
            ncol=2,
            fontsize=8,
            framealpha=0.92,
            title="Heurisztika: költség",
        )

    figure.suptitle(
        "A*+DWA útvonalak az eredeti, inflált szimulációs térképen",
        fontsize=18,
        weight="bold",
    )
    figure.tight_layout(rect=(0, 0.06, 1, 0.94))
    output_path = (
        Path(__file__).resolve().parent
        / "results"
        / "figures"
        / "simulation_heuristic_comparison.png"
    )
    figure.savefig(output_path, bbox_inches="tight")
    plt.close(figure)
    print(f"Abra mentve: {output_path}")


if __name__ == "__main__":
    main()
