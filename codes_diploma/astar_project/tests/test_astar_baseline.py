"""A klasszikus A* alapviselkedésének tesztjei."""

import unittest

from codes_diploma.astar_project.astar_baseline import astar_search
from codes_diploma.astar_project.grid_map import GridMap


class TestAstarSearch(unittest.TestCase):
	def test_finds_straight_path(self):
		grid_map = GridMap(width=4, height=1)

		path = astar_search(grid_map, (0, 0), (0, 3))

		self.assertEqual(path, [(0, 0), (0, 1), (0, 2), (0, 3)])

	def test_avoids_obstacle(self):
		grid_map = GridMap(width=5, height=3)
		grid_map.add_obstacle(1, 2)

		path = astar_search(grid_map, (1, 0), (1, 4))

		self.assertIsNotNone(path)
		self.assertNotIn((1, 2), path)
		self.assertEqual(path[0], (1, 0))
		self.assertEqual(path[-1], (1, 4))

	def test_returns_none_when_goal_is_unreachable(self):
		grid_map = GridMap(width=3, height=3)
		for row, column in ((0, 1), (1, 0), (1, 2), (2, 1)):
			grid_map.add_obstacle(row, column)

		path = astar_search(grid_map, (0, 0), (2, 2))

		self.assertIsNone(path)

	def test_diagonal_motion_uses_diagonal_neighbors(self):
		grid_map = GridMap(width=3, height=3)

		path = astar_search(grid_map, (0, 0), (2, 2), diagonal=True)

		self.assertEqual(path, [(0, 0), (1, 1), (2, 2)])

	def test_rejects_blocked_start_or_goal(self):
		grid_map = GridMap(width=2, height=2)
		grid_map.add_obstacle(0, 0)

		with self.assertRaises(ValueError):
			astar_search(grid_map, (0, 0), (1, 1))


if __name__ == "__main__":
	unittest.main()
