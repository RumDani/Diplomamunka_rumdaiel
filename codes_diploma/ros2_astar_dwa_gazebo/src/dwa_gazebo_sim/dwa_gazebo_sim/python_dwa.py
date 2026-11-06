"""ROS DWA backend with cached trajectory distances and vectorized scan checks."""

import math

import numpy as np

from codes_diploma.DWA import pairstochoose
from codes_diploma.robot import robotstate, update


def optimisation(config, state, goal, obstacle_list):
    maximum_velocity = config.w_kerek_max * config.r_kerek
    target_heading = math.atan2(goal.y - state.y, goal.x - state.x)
    initial_heading_error = math.atan2(math.sin(target_heading - state.irany),
                                       math.cos(target_heading - state.irany))
    turning_velocity = maximum_velocity * max(0.0, math.cos(initial_heading_error))
    reachable_velocity = max(0.0, state.v - config.a_max * config.dt)
    velocity_limit = max(turning_velocity, reachable_velocity)
    candidates = pairstochoose(config, state)
    wheel_step = config.a_max / config.r_kerek * config.dt
    left_min = max(-config.w_kerek_max, state.w_L - wheel_step)
    left_max = min(config.w_kerek_max, state.w_L + wheel_step)
    right_min = max(-config.w_kerek_max, state.w_R - wheel_step)
    right_max = min(config.w_kerek_max, state.w_R + wheel_step)
    rotation_min, rotation_max = max(left_min, -right_max), min(left_max, -right_min)
    if rotation_min <= rotation_max:
        left = min(rotation_max, max(rotation_min, -initial_heading_error * config.b / config.r_kerek))
        angular = -left * config.r_kerek / config.b
        candidates.append([0.0, angular, left, -left])
    obstacles = np.asarray([
        (obstacle.x, obstacle.y, obstacle.radius, obstacle.vx, obstacle.vy)
        for obstacle in obstacle_list
    ], dtype=float).reshape(-1, 5)
    if len(obstacles):
        offsets = obstacles[:, :2] - (state.x, state.y)
        bearings = np.arctan2(offsets[:, 1], offsets[:, 0]) - state.irany
        errors = np.arctan2(np.sin(bearings), np.cos(bearings))
        obstacles = obstacles[(np.hypot(offsets[:, 0], offsets[:, 1]) <= 3.0) &
                              (np.abs(errors) <= math.pi / 2)]
    static = (obstacles[:, 3] == 0.0) & (obstacles[:, 4] == 0.0)
    thresholds = obstacles[:, 2] + config.rob_radius + np.where(
        static, getattr(config, "static_safety_margin", 0.01), config.safety_margin)
    times = np.arange(0, config.predict_time, config.dt)
    future_x = obstacles[None, :, 0] + times[:, None] * obstacles[None, :, 3]
    future_y = obstacles[None, :, 1] + times[:, None] * obstacles[None, :, 4]
    distances = {}
    dynamic_collisions = set()

    def trajectory_distance(pair):
        velocity, _, left, right = pair
        key = (left, right)
        if key in distances:
            return distances[key]
        result = 10.0
        if len(obstacles):
            predicted = robotstate(x=state.x, y=state.y, irany=state.irany,
                                   w_L=state.w_L, w_R=state.w_R)
            travelled = 0.0
            for step_index in range(len(times)):
                separations = np.hypot(predicted.x - future_x[step_index],
                                       predicted.y - future_y[step_index])
                collisions = separations <= thresholds
                if np.any(collisions) and result == 10.0:
                    result = travelled
                if np.any(collisions & ~static):
                    dynamic_collisions.add(key)
                    break
                update(predicted, config, left, right, config.dt)
                travelled += abs(velocity) * config.dt
        distances[key] = result
        return result

    safe_pairs = []
    allow_reverse = getattr(config, "allow_reverse", False)
    for pair in candidates:
        if not allow_reverse and pair[0] < 0.0:
            continue
        if (abs(pair[2]) > config.w_kerek_max + 1e-9 or
                abs(pair[3]) > config.w_kerek_max + 1e-9 or pair[0] > velocity_limit + 1e-9):
            continue
        collision_distance = trajectory_distance(pair)
        if (pair[2], pair[3]) in dynamic_collisions:
            continue
        if abs(pair[0]) <= math.sqrt(2 * config.a_max * collision_distance):
            safe_pairs.append(pair)
    if not safe_pairs:
        return None, []

    goal_distance = math.hypot(goal.x - state.x, goal.y - state.y)
    prediction_time = config.predict_time
    if goal_distance < 1.0:
        prediction_time = max(0.5, goal_distance * 2.0)
    score_times = np.arange(0, prediction_time, config.dt)
    best_score = -float("inf")
    best_pair = None
    for pair in safe_pairs:
        velocity, _, left, right = pair
        predicted = robotstate(x=state.x, y=state.y, irany=state.irany,
                               w_L=state.w_L, w_R=state.w_R)
        for _ in score_times:
            update(predicted, config, left, right, config.dt)
        goal_heading = getattr(goal, "heading", None)
        if goal_heading is None:
            goal_heading = math.atan2(goal.y - predicted.y, goal.x - predicted.x)
        heading_error = math.atan2(math.sin(goal_heading - predicted.irany),
                                   math.cos(goal_heading - predicted.irany))
        heading_score = (math.pi - abs(heading_error)) / math.pi
        distance_score = trajectory_distance(pair)
        slowdown_distance = getattr(goal, "slow_down_distance", 0.8)
        if not getattr(goal, "slow_down", True) and goal_distance > slowdown_distance:
            velocity_score = 1.0 - abs(turning_velocity - velocity) / maximum_velocity
        else:
            target_velocity = min(turning_velocity, max(0.08, goal_distance * 1.4))
            velocity_score = 1.0 - abs(target_velocity - velocity) / maximum_velocity
        score = (config.Alfa * heading_score + config.Beta * distance_score +
                 config.Gamma * velocity_score)
        if score > best_score:
            best_score = score
            best_pair = list(pair)
    return best_pair, safe_pairs