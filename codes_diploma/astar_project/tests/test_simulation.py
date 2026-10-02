"""A grafikus szimulacio grafika nelkuli tesztjei."""

import unittest

from codes_diploma.simulation import create_scene


class TestSimulation(unittest.TestCase):
	def test_scene_contains_static_and_moving_obstacles(self):
		grid_map, start_cell, goal_cell, start, goal, state, static_obstacles, dynamic_obstacles = create_scene()

		self.assertIsNotNone(grid_map)
		self.assertNotEqual(start, goal)
		self.assertTrue(static_obstacles)
		self.assertTrue(dynamic_obstacles)
		self.assertTrue(dynamic_obstacles[0].vx != 0.0 or dynamic_obstacles[0].vy != 0.0)


if __name__ == "__main__":
	unittest.main()