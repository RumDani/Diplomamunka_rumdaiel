"""Az A* heurisztika- és mozgásmód-összehasonlítás tesztjei."""

import unittest

from codes_diploma.astar_project.experiments import (
    build_experiment_scenarios,
    compare_heuristics,
    run_scenario_comparison,
)


class TestExperiments(unittest.TestCase):
    def test_all_heuristics_are_compared_in_both_motion_modes(self):
        rows = run_scenario_comparison()

        self.assertEqual(len(rows), 4 * 2 * 4)
        self.assertEqual(
            {row["heuristic"] for row in rows},
            {"manhattan", "euclidean", "chebyshev", "octile"},
        )
        self.assertEqual({row["diagonal"] for row in rows}, {False, True})

    def test_non_diagonal_mode_rejects_diagonal_only_map(self):
        grid_map, start, goal = build_experiment_scenarios()["diagonal_only"]

        rows = compare_heuristics(grid_map, start, goal, diagonal=False)

        self.assertTrue(all(not row["success"] for row in rows))

    def test_corner_cutting_is_not_used_when_diagonal_is_enabled(self):
        grid_map, start, goal = build_experiment_scenarios()["corner_cutting"]

        rows = compare_heuristics(grid_map, start, goal, diagonal=True)

        self.assertTrue(all(row["success"] for row in rows))
        for row in rows:
            self.assertNotIn((2, 2), row["path"])


if __name__ == "__main__":
    unittest.main()
