"""Az utvonal-simitas tesztjei."""

import unittest

from codes_diploma.astar_project.grid_map import GridMap
from codes_diploma.astar_project.path_smoothing import (
	_is_path_safe,
	_cut_point,
	bezier_curve_points,
	smooth_path,
)


class TestPathSmoothing(unittest.TestCase):
	def test_keeps_a_straight_path_unchanged(self):
		grid_map = GridMap(width=5, height=1)
		path = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]

		self.assertEqual(smooth_path(grid_map, path), path)

	def test_creates_a_bezier_path_between_turning_points(self):
		grid_map = GridMap(width=5, height=5)

		path = smooth_path(grid_map, [(0, 0), (0, 2), (2, 2)], diagonal=True)

		self.assertEqual(path[0], (0, 0))
		self.assertEqual(path[-1], (2, 2))
		self.assertTrue(
			all(
				grid_map.is_free(round(row), round(column))
				for row, column in path
			)
		)

	def test_uses_all_points_in_a_dynamic_order_curve(self):
		grid_map = GridMap(width=5, height=5)
		path = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]

		smoothed_path = smooth_path(grid_map, path, diagonal=True)
		curve = bezier_curve_points(path, samples_per_segment=15)

		self.assertEqual(smoothed_path[0], path[0])
		self.assertEqual(smoothed_path[-1], path[-1])
		self.assertGreater(len(curve), len(path))
		self.assertNotEqual(curve[1], path[1])

	def test_keeps_a_path_around_an_obstacle(self):
		grid_map = GridMap(width=5, height=3)
		grid_map.add_obstacle(1, 2)
		path = [(1, 0), (0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (1, 4)]

		result = smooth_path(grid_map, path)

		self.assertEqual(result[0], path[0])
		self.assertEqual(result[-1], path[-1])
		self.assertNotIn((1, 2), result)

	def test_rejects_non_neighbor_jump(self):
		grid_map = GridMap(width=5, height=1)

		self.assertFalse(_is_path_safe(grid_map, [(0, 0), (0, 2)]))

	def test_bezier_cut_point_respects_maximum_distance(self):
		cut_point = _cut_point((0.0, 2.0), (0.0, 0.0), 1.5)

		self.assertAlmostEqual(cut_point[0], 0.0)
		self.assertAlmostEqual(cut_point[1], 0.5)


if __name__ == "__main__":
	unittest.main()
