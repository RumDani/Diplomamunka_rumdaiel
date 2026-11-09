"""Pontokkal es vonalstilusokkal jelolt heurisztika-abra generalasa."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from .astar_baseline import astar_search
from .astar_variants import HEURISTICS, get_heuristic
from .experiments import _path_cost, build_experiment_scenarios


COLORS = {
    "manhattan": "#0072B2",
    "euclidean": "#E69F00",
    "chebyshev": "#009E73",
    "octile": "#CC79A7",
}


def _draw_scenario(grid_map, start, goal, output_path):
    figure, axes = plt.subplots(1, 2, figsize=(17, 8), dpi=180)
    for axis, diagonal, title in (
        (axes[0], False, "Négyirányú mozgás"),
        (axes[1], True, "Átlós mozgás is engedélyezett"),
    ):
        for row in range(grid_map.height):
            for column in range(grid_map.width):
                if grid_map.grid[row][column] == 1:
                    axis.add_patch(
                        Rectangle(
                            (column * grid_map.resolution, row * grid_map.resolution),
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
        for heuristic_name in HEURISTICS:
            color = COLORS[heuristic_name]
            result = astar_search(
                grid_map,
                start,
                goal,
                diagonal=diagonal,
                heuristic=get_heuristic(heuristic_name),
                return_details=True,
            )
            path = result["path"]
            if path is None:
                continue
            world_path = [
                grid_map.grid_to_world(row, column)
                for row, column in path
            ]
            path_x = [x for x, _ in world_path]
            path_y = [y for _, y in world_path]
            cost = _path_cost(path)
            label = f"{heuristic_name.title()}: {cost:.2f}"
            line, = axis.plot(
                path_x,
                path_y,
                color=color,
                linestyle="--",
                dashes=(3, 2),
                marker="o",
                markersize=2.4,
                markeredgewidth=0.45,
                markeredgecolor="white",
                linewidth=1.8,
                alpha=0.92,
                label=label,
                zorder=4,
            )

        start_x, start_y = grid_map.grid_to_world(*start)
        goal_x, goal_y = grid_map.grid_to_world(*goal)
        axis.scatter(
            [start_x], [start_y], s=90, marker="o",
            facecolor="#00A651", edgecolor="white", linewidth=2, zorder=5,
        )
        axis.scatter(
            [goal_x], [goal_y], s=110, marker="*",
            facecolor="#E31B23", edgecolor="white", linewidth=1.5, zorder=5,
        )
        axis.text(
            start_x, start_y, "S", color="white", ha="center",
            va="center", weight="bold", zorder=6,
        )
        axis.text(
            goal_x, goal_y, "G", color="white", ha="center",
            va="center", weight="bold", zorder=6,
        )
        axis.set_title(title, fontsize=15, weight="bold")
        axis.set_xlabel("x [m]")
        axis.set_ylabel("y [m]")
        axis.set_xlim(0, grid_map.width * grid_map.resolution)
        axis.set_ylim(0, grid_map.height * grid_map.resolution)
        axis.set_aspect("equal")
        axis.legend(
            loc="lower left",
            fontsize=8,
            framealpha=0.92,
            title="Heurisztika: költség",
        )

    figure.suptitle(
        "A* heurisztikák az eredeti szimulációs térképen",
        fontsize=18,
        weight="bold",
    )
    figure.tight_layout(rect=(0, 0.10, 1, 0.94))
    figure.savefig(output_path, bbox_inches="tight")
    plt.close(figure)


def main():
    output_directory = (
        Path(__file__).resolve().parent / "results" / "figures"
    )
    output_directory.mkdir(parents=True, exist_ok=True)
    original_map, start, goal = build_experiment_scenarios()[
        "original_simulation"
    ]
    _draw_scenario(
        original_map,
        start,
        goal,
        output_directory / "heuristics_original_simulation.png",
    )
    print(f"Abraak mentve: {output_directory}")


if __name__ == "__main__":
    main()
