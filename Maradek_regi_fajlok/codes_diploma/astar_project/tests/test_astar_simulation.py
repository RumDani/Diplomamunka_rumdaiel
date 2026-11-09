"""Teszt a statikus A* matplotlib szimulaciohoz."""

import unittest

from codes_diploma.astar_project.astar_baseline import astar_search
from codes_diploma.astar_project.astar_simulation import (
    _parse_position,
    create_demo_map,
    create_robot_trajectory,
    plot_simulation,
)
from codes_diploma.astar_project.path_smoothing import bezier_curve_points


class TestAstarSimulation(unittest.TestCase):
    def test_position_input_is_read_as_row_and_column(self):
        self.assertEqual(_parse_position(" 2, 17 "), (2, 17))

    def test_demo_map_has_a_valid_static_path(self):
        grid_map, start, goal = create_demo_map()

        path = astar_search(grid_map, start, goal, diagonal=True)

        self.assertIsNotNone(path)
        self.assertEqual(path[0], start)
        self.assertEqual(path[-1], goal)
        self.assertTrue(all(grid_map.is_free(row, column) for row, column in path))

    def test_demo_path_creates_continuous_smoothing_points(self):
        grid_map, start, goal = create_demo_map()
        path = astar_search(grid_map, start, goal, diagonal=True)

        curve = bezier_curve_points(path)

        self.assertEqual(curve[0], path[0])
        self.assertEqual(curve[-1], path[-1])
        self.assertNotEqual(curve, path)

    def test_robot_trajectory_starts_and_ends_at_path_points(self):
        grid_map, start, goal = create_demo_map()
        path = astar_search(grid_map, start, goal)

        trajectory = create_robot_trajectory(grid_map, path, steps_per_cell=4)

        self.assertEqual(trajectory[0], grid_map.grid_to_world(*start))
        self.assertEqual(trajectory[-1], grid_map.grid_to_world(*goal))
        self.assertEqual(len(trajectory), 1 + (len(path) - 1) * 4)

    def test_plot_simulation_can_be_created_without_showing_window(self):
        grid_map, start, goal = create_demo_map()
        path = astar_search(grid_map, start, goal)
        trajectory = create_robot_trajectory(grid_map, path)

        figure, robot_animation = plot_simulation(
            grid_map,
            path,
            trajectory,
            start,
            goal,
            show=False,
        )

        self.assertIsNotNone(figure)
        self.assertIsNotNone(robot_animation)
        figure.clf()

    def test_plot_uses_smoothed_trajectory_when_enabled(self):
        grid_map = create_demo_map(width=5, height=5)[0]
        path = [(0, 0), (0, 2), (2, 2)]
        trajectory = create_robot_trajectory(
            grid_map, path, smooth=True, diagonal=True
        )

        figure, _ = plot_simulation(
            grid_map,
            path,
            trajectory,
            path[0],
            path[-1],
            show=False,
            smoothed=True,
        )

        smoothed_line = next(
            line
            for line in figure.axes[1].lines
            if line.get_label() == "Bezier-simitott utvonal"
        )
        self.assertEqual(list(zip(*smoothed_line.get_data())), trajectory)
        figure.clf()

    def test_next_button_advances_the_current_search_cell(self):
        grid_map, start, goal = create_demo_map()
        result = astar_search(
            grid_map,
            start,
            goal,
            diagonal=True,
            return_details=True,
        )
        trajectory = create_robot_trajectory(grid_map, result["path"])

        figure, _ = plot_simulation(
            grid_map,
            result["path"],
            trajectory,
            start,
            goal,
            expanded_nodes=result["expanded_nodes"],
            search_steps=result["search_steps"],
            show=False,
        )

        map_axes = figure.axes[1]
        current_search = next(
            artist
            for artist in map_axes.collections
            if artist.get_label() == "C: aktualis cella"
        )
        first_position = tuple(current_search.get_offsets()[0])
        figure._astar_next_frame()
        second_position = tuple(current_search.get_offsets()[0])

        self.assertNotEqual(first_position, second_position)
        figure.clf()


if __name__ == "__main__":
    unittest.main()
