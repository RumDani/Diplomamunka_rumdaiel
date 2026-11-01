"""Differential-drive Dynamic Window Approach controller."""

import math


def _angle(value):
    return math.atan2(math.sin(value), math.cos(value))


def choose_velocity(state, goal, obstacles, robot_radius):
    best = None
    for velocity in (0.0, 0.08, 0.16, 0.24, 0.32, 0.4):
        for angular_velocity in (-1.2, -0.8, -0.4, 0.0, 0.4, 0.8, 1.2):
            x, y, yaw = state
            safe = True
            for _ in range(15):
                x += velocity * math.cos(yaw) * 0.1
                y += velocity * math.sin(yaw) * 0.1
                yaw += angular_velocity * 0.1
                if any(math.hypot(x - ox, y - oy) < robot_radius + radius
                       for ox, oy, radius in obstacles):
                    safe = False
                    break
            if not safe:
                continue
            heading = math.atan2(goal[1] - y, goal[0] - x)
            score = (-math.hypot(goal[0] - x, goal[1] - y)
                     - 0.25 * abs(_angle(heading - yaw)) + 0.15 * velocity)
            if best is None or score > best[0]:
                best = score, velocity, angular_velocity
    return (best[1], best[2]) if best else (0.0, 0.0)
