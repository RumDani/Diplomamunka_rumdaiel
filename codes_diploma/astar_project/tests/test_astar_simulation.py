"""Teszt a statikus A* matplotlib szimulaciohoz."""

import unittest

from codes_diploma.astar_project.astar_baseline import astar_search
from codes_diploma.astar_project.astar_simulation import (
    create_demo_map,
    create_robot_trajectory,
    plot_simulation,
)


class TestAstarSimulation(unittest.TestCase):
    def test_demo_map_has_a_valid_static_path(self):
        grid_map, start, goal = create_demo_map()

        path = astar_search(grid_map, start, goal, diagonal=True)

        self.assertIsNotNone(path)
        self.assertEqual(path[0], start)
        self.assertEqual(path[-1], goal)
        self.assertTrue(all(grid_map.is_free(row, column) for row, column in path))

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


if __name__ == "__main__":
    unittest.main()
