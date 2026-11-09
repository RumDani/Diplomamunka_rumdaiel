"""A robot.py és a DWA.py célzott tesztjei."""

import unittest

from codes_diploma.DWA import optimisation
from codes_diploma.robot import Obstacle, Goal, get_robot_kinematics, robotconfig, robotstate


class TestRobotAndDWA(unittest.TestCase):
	def test_robot_kinematics(self):
		config = robotconfig()
		linear, angular = get_robot_kinematics(10.0, 10.0, config)

		self.assertAlmostEqual(linear, 0.33)
		self.assertAlmostEqual(angular, 0.0)

	def test_original_parameters_are_preserved(self):
		config = robotconfig()

		self.assertEqual(config.r_kerek, 0.033)
		self.assertEqual(config.b, 0.08)
		self.assertEqual(config.w_kerek_max, 15)
		self.assertEqual(config.a_max, 2)
		self.assertEqual(config.dt, 0.1)
		self.assertEqual(config.predict_time, 3)
		self.assertEqual(config.rob_radius, 0.1)

	def test_dwa_returns_original_pair_format(self):
		best_pair, safe_pairs = optimisation(
			robotconfig(),
			robotstate(),
			Goal(2.0, 0.0),
			[],
		)

		self.assertIsNotNone(best_pair)
		self.assertTrue(safe_pairs)
		self.assertEqual(len(best_pair), 4)

	def test_moving_obstacle(self):
		obstacle = Obstacle(1.0, 2.0, radius=0.1, vx=0.5)

		obstacle.move(2.0)

		self.assertEqual((obstacle.x, obstacle.y), (2.0, 2.0))


if __name__ == "__main__":
	 unittest.main()