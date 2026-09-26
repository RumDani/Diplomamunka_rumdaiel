"""Az utvonal-simitas tesztjei."""

import unittest

from codes_diploma.astar_project.grid_map import GridMap
from codes_diploma.astar_project.path_smoothing import smooth_path


class TestPathSmoothing(unittest.TestCase):
	def test_creates_a_bezier_path_between_turning_points(self):
		grid_map = GridMap(width=5, height=5)

		path = smooth_path(grid_map, [(0, 0), (0, 2), (2, 2)], diagonal=True)

		self.assertEqual(path[0], (0, 0))
		self.assertEqual(path[-1], (2, 2))
		self.assertNotEqual(path, [(0, 0), (0, 2), (2, 2)])

	def test_keeps_a_path_around_an_obstacle(self):
		grid_map = GridMap(width=5, height=3)
		grid_map.add_obstacle(1, 2)
		path = [(1, 0), (0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (1, 4)]

		result = smooth_path(grid_map, path)

		self.assertEqual(result[0], path[0])
		self.assertEqual(result[-1], path[-1])
		self.assertNotIn((1, 2), result)


if __name__ == "__main__":
	unittest.main()
