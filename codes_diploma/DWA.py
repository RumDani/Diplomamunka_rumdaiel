"""Dinamikus ablakos lokális útvonaltervezés."""

import math

import numpy as np

from .robot import get_robot_kinematics, robotstate, update


def get_dist_on_trajectory(state, config, w_L, w_R, obstacle_list):
	"""Az első ütközésig megtett távolságot számolja ki."""
	temp_robot = robotstate(x=state.x, y=state.y, irany=state.irany, w_L=state.w_L, w_R=state.w_R)
	accumulated_dist = 0.0
	v_actual, _ = get_robot_kinematics(w_L, w_R, config)
	max_sensor_dist = 3.0
	fov_angle = math.radians(180)

	for t in np.arange(0, config.predict_time, config.dt):
		for obs in obstacle_list:
			dist_now = math.hypot(state.x - obs.x, state.y - obs.y)
			if dist_now > max_sensor_dist:
				continue

			angle_to_obs = math.atan2(obs.y - state.y, obs.x - state.x)
			diff_angle = math.atan2(
				math.sin(angle_to_obs - state.irany),
				math.cos(angle_to_obs - state.irany),
			)
			if abs(diff_angle) > fov_angle / 2:
				continue

			obs_future_x = obs.x + obs.vx * t
			obs_future_y = obs.y + obs.vy * t
			dist_centers = math.hypot(temp_robot.x - obs_future_x, temp_robot.y - obs_future_y)
			if dist_centers <= config.rob_radius + obs.radius + config.safety_margin:
				return accumulated_dist

		update(temp_robot, config, w_L, w_R, config.dt)
		accumulated_dist += abs(v_actual) * config.dt

	return 10.0


def AdmissableVelocity(config, w_L, w_R, state, obstacle_list):
	"""Ellenőrzi, hogy a robot meg tud-e állni az ütközés előtt."""
	dist_to_obs = get_dist_on_trajectory(state, config, w_L, w_R, obstacle_list)
	v, _ = get_robot_kinematics(w_L, w_R, config)
	return abs(v) <= math.sqrt(2 * config.a_max * dist_to_obs)


def pairstochoose(config, state):
	"""Az aktuális dinamikus ablak összes keréksebesség-párja."""
	w_dot_max = config.a_max / config.r_kerek
	w_L_min = max(config.w_kerek_min, state.w_L - w_dot_max * config.dt)
	w_L_max = min(config.w_kerek_max, state.w_L + w_dot_max * config.dt)
	w_R_min = max(config.w_kerek_min, state.w_R - w_dot_max * config.dt)
	w_R_max = min(config.w_kerek_max, state.w_R + w_dot_max * config.dt)
	w_L_samples = np.arange(w_L_min, w_L_max + config.w_kerek_resolution, config.w_kerek_resolution)
	w_R_samples = np.arange(w_R_min, w_R_max + config.w_kerek_resolution, config.w_kerek_resolution)

	return [
		[v, w, w_L, w_R]
		for w_L in w_L_samples
		for w_R in w_R_samples
		for v, w in [get_robot_kinematics(w_L, w_R, config)]
	]


def safepairs(config, state, obstacle_list):
	"""Csak a megállítható keréksebesség-párokat adja vissza."""
	return [
		pair
		for pair in pairstochoose(config, state)
		if config.allow_reverse or pair[0] >= 0.0
		if AdmissableVelocity(config, pair[2], pair[3], state, obstacle_list)
	]


def optimisation(config, state, goal, obstacle_list):
	"""Kiválasztja a célhoz legjobban illeszkedő biztonságos párt."""
	safe_list = safepairs(config, state, obstacle_list)
	if not safe_list:
		return None, []

	best_score = -float("inf")
	best_pair = None
	dist_to_goal = math.hypot(goal.x - state.x, goal.y - state.y)
	v_max_robot = config.w_kerek_max * config.r_kerek
	adaptive_predict_time = config.predict_time
	heading_to_goal = math.atan2(goal.y - state.y, goal.x - state.x)
	heading_error = abs(math.atan2(math.sin(heading_to_goal - state.irany), math.cos(heading_to_goal - state.irany)))
	if dist_to_goal < 1.0:
		adaptive_predict_time = max(0.5, dist_to_goal * 2.0)
	elif heading_error > math.pi / 3.0:
		adaptive_predict_time = max(0.5, min(config.predict_time, dist_to_goal * 1.5))

	for v, w, w_L, w_R in safe_list:
		temp_robot = robotstate(x=state.x, y=state.y, irany=state.irany, w_L=state.w_L, w_R=state.w_R)
		for _ in np.arange(0, adaptive_predict_time, config.dt):
			update(temp_robot, config, w_L, w_R, config.dt)

		angle_to_goal = goal.heading
		if angle_to_goal is None:
			angle_to_goal = math.atan2(goal.y - temp_robot.y, goal.x - temp_robot.x)
		error_angle = math.atan2(math.sin(angle_to_goal - temp_robot.irany), math.cos(angle_to_goal - temp_robot.irany))
		score_heading = (math.pi - abs(error_angle)) / math.pi
		score_dist = get_dist_on_trajectory(state, config, w_L, w_R, obstacle_list)

		slow_down_distance = getattr(goal, "slow_down_distance", 0.8)
		if not getattr(goal, "slow_down", True) and dist_to_goal > slow_down_distance:
			score_vel = v / v_max_robot
		else:
			v_target = min(v_max_robot, max(0.08, dist_to_goal * 1.4))
			score_vel = 1.0 - abs(v_target - v) / v_max_robot

		score = config.Alfa * score_heading + config.Beta * score_dist + config.Gamma * score_vel
		if score > best_score:
			best_score = score
			best_pair = [v, w, w_L, w_R]

	return best_pair, safe_list