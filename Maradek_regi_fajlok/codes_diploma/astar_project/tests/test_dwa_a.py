"""A DWA+A.py A*–DWA illesztésének tesztjei."""

import importlib.util
import pathlib
import unittest

from codes_diploma.astar_project.grid_map import GridMap
from codes_diploma.robot import robotconfig, robotstate


def point_to_path_distance(point, path):
	minimum = float("inf")
	for start, end in zip(path, path[1:]):
		dx = end[0] - start[0]
		dy = end[1] - start[1]
		length_squared = dx * dx + dy * dy
		if length_squared == 0:
			projection = start
		else:
			ratio = max(0.0, min(1.0, ((point[0] - start[0]) * dx + (point[1] - start[1]) * dy) / length_squared))
			projection = (start[0] + ratio * dx, start[1] + ratio * dy)
		minimum = min(minimum, ((point[0] - projection[0]) ** 2 + (point[1] - projection[1]) ** 2) ** 0.5)
	return minimum


def load_planner_class():
	file_path = pathlib.Path(__file__).parents[2] / "DWA+A.py"
	spec = importlib.util.spec_from_file_location("dwa_a_module", file_path)
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module.AStarDWAPlanner


class TestDwaA(unittest.TestCase):
	def test_astar_path_becomes_waypoints_and_dwa_pair(self):
		planner_class = load_planner_class()
		grid_map = GridMap(width=5, height=1, resolution=1.0)
		planner = planner_class(grid_map, config=robotconfig(), diagonal=False)

		path = planner.plan_global((0.1, 0.1), (4.1, 0.1))
		result = planner.plan_local(robotstate(x=0.5, y=0.5))

		self.assertEqual(len(path), 5)
		self.assertIn(result["target"], planner.waypoints)
		self.assertEqual(result["target"], planner.waypoints[planner.waypoint_index])
		self.assertEqual(len(result["best_pair"]), 4)
		self.assertTrue(all(
			point_to_path_distance(point, planner.bezier_path) < 1e-9
			for point in planner.waypoints
		))

	def test_waypoint_changes_only_after_reaching_active_point(self):
		planner_class = load_planner_class()
		grid_map = GridMap(width=5, height=1, resolution=1.0)
		planner = planner_class(grid_map, config=robotconfig(), diagonal=False, waypoint_tolerance=0.1)
		planner.plan_global((0.1, 0.1), (4.1, 0.1), smooth=False)

		planner.plan_local(robotstate(x=0.5, y=0.5))
		self.assertEqual(planner.waypoint_index, 1)

		active_waypoint = planner.waypoints[planner.waypoint_index]
		planner.plan_local(robotstate(x=active_waypoint[0], y=active_waypoint[1]))
		self.assertEqual(planner.waypoint_index, 2)

	def test_goal_returns_stop_command(self):
		planner_class = load_planner_class()
		grid_map = GridMap(width=3, height=1, resolution=1.0)
		planner = planner_class(grid_map, config=robotconfig(), diagonal=False)
		planner.plan_global((0.1, 0.1), (2.1, 0.1), smooth=False)

		goal = planner.waypoints[-1]
		result = planner.plan_local(robotstate(x=goal[0], y=goal[1]))

		self.assertTrue(result["finished"])
		self.assertEqual(result["best_pair"], [0.0, 0.0, 0.0, 0.0])


if __name__ == "__main__":
	unittest.main()