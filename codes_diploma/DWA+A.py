"""A* globális útvonal és DWA lokális vezérlés egyben."""

import math

from codes_diploma.astar_project.astar_baseline import astar_search
from codes_diploma.astar_project.path_smoothing import smooth_path
from codes_diploma.DWA import optimisation, pairstochoose
from codes_diploma.robot import Goal, robotconfig


class AStarDWAPlanner:
    """Az A* waypointot ad a DWA lokális tervezőjének."""

    def __init__(
        self,
        grid_map,
        config=None,
        diagonal=True,
        waypoint_tolerance=0.2,
        waypoint_spacing=0.2,
    ):
        self.grid_map = grid_map
        self.config = config or robotconfig()
        self.diagonal = diagonal
        self.waypoint_tolerance = waypoint_tolerance
        self.waypoint_spacing = waypoint_spacing
        self.path = []
        self.astar_path = []
        self.bezier_path = []
        self.waypoints = []
        self.waypoint_index = 0

    def _current_tolerance(self, state):
        if not self.waypoints:
            return self.waypoint_tolerance
        goal_distance = math.hypot(
            self.waypoints[-1][0] - state.x, self.waypoints[-1][1] - state.y
        )
        return max(0.05, min(self.waypoint_tolerance, goal_distance * 0.2))

    @staticmethod
    def _create_waypoints(path, spacing=0.2):
        """Egyenletes tavolsagu pontokat keszit a simitott ut teljes hosszan."""
        if not path:
            return []
        waypoints = [path[0]]
        remaining_distance = spacing
        segment_start = path[0]
        for segment_end in path[1:]:
            segment_dx = segment_end[0] - segment_start[0]
            segment_dy = segment_end[1] - segment_start[1]
            segment_length = math.hypot(segment_dx, segment_dy)
            if segment_length == 0:
                continue
            while segment_length >= remaining_distance:
                ratio = remaining_distance / segment_length
                point = (
                    segment_start[0] + ratio * segment_dx,
                    segment_start[1] + ratio * segment_dy,
                )
                waypoints.append(point)
                segment_start = point
                segment_dx = segment_end[0] - segment_start[0]
                segment_dy = segment_end[1] - segment_start[1]
                segment_length = math.hypot(segment_dx, segment_dy)
                remaining_distance = spacing
            remaining_distance -= segment_length
            segment_start = segment_end
        if waypoints[-1] != path[-1]:
            waypoints.append(path[-1])
        return waypoints

    def plan_global(
        self,
        start_world,
        goal_world,
        heuristic=None,
        smooth=True,
        samples_per_curve=8,
        max_cut_distance=None,
    ):
        start = self.grid_map.world_to_grid(*start_world)
        goal = self.grid_map.world_to_grid(*goal_world)
        path = astar_search(
            self.grid_map,
            start,
            goal,
            diagonal=self.diagonal,
            heuristic=heuristic,
        )
        if path is None:
            self.path = []
            self.astar_path = []
            self.bezier_path = []
            self.waypoints = []
            self.waypoint_index = 0
            return None
        self.astar_path = [
            self.grid_map.grid_to_world(row, column) for row, column in path
        ]
        if smooth:
            if max_cut_distance is None:
                max_cut_distance = 0.5 * self.grid_map.resolution
            path = smooth_path(
                self.grid_map,
                path,
                diagonal=self.diagonal,
                samples_per_curve=samples_per_curve,
                max_cut_distance=max_cut_distance,
            )
        self.bezier_path = [
            self.grid_map.grid_to_world(row, column) for row, column in path
        ]
        self.path = list(self.bezier_path)
        self.waypoints = self._create_waypoints(self.path, self.waypoint_spacing)
        self.waypoint_index = min(1, len(self.waypoints) - 1)
        return tuple(self.path)

    def plan_local(self, state, obstacles=()):
        if not self.waypoints:
            return None
        if self.reached_goal(state):
            return {
                "waypoint": self.waypoints[-1],
                "target": self.waypoints[-1],
                "best_pair": [0.0, 0.0, 0.0, 0.0],
                "safe_pairs": [],
                "all_pairs": [],
                "finished": True,
            }

        current = self.waypoints[self.waypoint_index]
        tolerance = self._current_tolerance(state)
        passed_waypoint = False
        if self.waypoint_index < len(self.waypoints) - 1:
            next_point = self.waypoints[self.waypoint_index + 1]
            to_current = (current[0] - state.x, current[1] - state.y)
            next_direction = (
                next_point[0] - current[0],
                next_point[1] - current[1],
            )
            passed_waypoint = (
                to_current[0] * next_direction[0]
                + to_current[1] * next_direction[1]
                < 0
            )
        if (
            self.waypoint_index < len(self.waypoints) - 1
            and (
                math.hypot(current[0] - state.x, current[1] - state.y)
                <= tolerance
                or passed_waypoint
            )
            and abs(state.v) <= 0.3
        ):
            self.waypoint_index += 1

        target = self.waypoints[self.waypoint_index]
        is_final_waypoint = self.waypoint_index == len(self.waypoints) - 1
        slow_down_distance = 0.5 if is_final_waypoint else 0.35
        goal = Goal(
            target[0],
            target[1],
            self.waypoint_tolerance,
            slow_down=True,
            slow_down_distance=slow_down_distance,
        )
        best_pair, safe_pairs = optimisation(
            self.config, state, goal, obstacles
        )
        all_pairs = pairstochoose(self.config, state)

        return {
            "waypoint": self.waypoints[self.waypoint_index],
            "target": target,
            "best_pair": best_pair,
            "safe_pairs": safe_pairs,
            "all_pairs": all_pairs,
            "finished": self.reached_goal(state),
        }

    def reached_goal(self, state):
        return bool(self.waypoints) and (
            math.hypot(
                self.waypoints[-1][0] - state.x,
                self.waypoints[-1][1] - state.y,
            )
            <= self._current_tolerance(state)
        )