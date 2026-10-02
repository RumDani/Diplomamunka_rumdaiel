"""Deterministikus teszt oldalrol keresztezo mozgo akadallyal."""

import unittest

from codes_diploma.DWA import optimisation
from codes_diploma.robot import Goal, Obstacle, robotconfig, robotstate


class TestDynamicObstacleCrossing(unittest.TestCase):
	def test_dwa_reacts_to_crossing_obstacle(self):
		config = robotconfig()
		state = robotstate(x=0.5, y=0.0, irany=0.0)
		goal = Goal(3.0, 0.0)

		clear_pair, _ = optimisation(config, state, goal, [])
		crossing_obstacle = Obstacle(1.5, -0.5, radius=0.15, vx=0.0, vy=0.2)
		obstacle_pair, safe_pairs = optimisation(config, state, goal, [crossing_obstacle])

		self.assertIsNotNone(clear_pair)
		self.assertIsNotNone(obstacle_pair)
		self.assertTrue(safe_pairs)
		self.assertLess(obstacle_pair[0], clear_pair[0])
		self.assertGreaterEqual(obstacle_pair[0], 0.0)


if __name__ == "__main__":
	unittest.main()