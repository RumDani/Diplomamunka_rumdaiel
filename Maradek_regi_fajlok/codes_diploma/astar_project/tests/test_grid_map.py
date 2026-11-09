"""A GridMap alapmuveleteinek tesztjei."""

import unittest

from codes_diploma.astar_project.grid_map import GridMap


class TestGridMap(unittest.TestCase):
	def test_diagonal_corner_cutting_is_rejected(self):
		grid_map = GridMap(width=3, height=3)
		grid_map.add_obstacle(0, 1)
		grid_map.add_obstacle(1, 0)

		neighbors = grid_map.get_neighbors(0, 0, diagonal=True)

		self.assertNotIn((1, 1), neighbors)

	def test_inflate_obstacles_marks_nearby_cells(self):
		grid_map = GridMap(width=5, height=5, resolution=0.1)
		grid_map.add_obstacle(2, 2)

		grid_map.inflate_obstacles(0.1)

		self.assertEqual(grid_map.grid[1][1], 1)
		self.assertEqual(grid_map.grid[3][3], 1)
		self.assertTrue(grid_map.is_free(0, 0))


if __name__ == "__main__":
	unittest.main()
