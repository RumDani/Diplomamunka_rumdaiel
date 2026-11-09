# Robotmodell: kinematika, konfiguráció, állapot, akadály és cél.
"""Differenciális meghajtású robotmodell."""

import math

import numpy as np


# Kerékszögsebességekből lineáris és szögsebesség.
def get_robot_kinematics(w_L, w_R, config):
	"""Keréksebességből lineáris és szögsebességet számol."""
	v = ((w_L + w_R) / 2) * config.r_kerek
	w = ((w_R - w_L) / (2 * config.b)) * config.r_kerek
	return v, w


# Kör alakú (mozgó) akadály.
class Obstacle:
	def __init__(self, x, y, radius=0.1, vx=0.0, vy=0.0):
		self.x = x
		self.y = y
		self.radius = radius
		self.vx = vx
		self.vy = vy

	# Akadály léptetése dt idővel.
	def move(self, dt):
		self.x += self.vx * dt
		self.y += self.vy * dt


# Célpont tűréssel és lassítási zónával.
class Goal:
	def __init__(self, x, y, tolerance=0.15, slow_down=True, slow_down_distance=0.8, heading=None):
		self.x = x
		self.y = y
		self.tolerance = tolerance
		self.slow_down = slow_down
		self.slow_down_distance = slow_down_distance
		self.heading = heading


# Robot fizikai és DWA paraméterei.
class robotconfig:
	def __init__(robot):
		robot.r_kerek = 0.033
		robot.b = 0.08
		robot.w_kerek_max = 15
		robot.a_max = 2
		robot.w_kerek_min = -robot.w_kerek_max
		robot.w_kerek_resolution = 1
		robot.allow_reverse = False
		robot.dt = 0.1
		robot.predict_time = 3
		robot.rob_radius = robot.b + 0.02
		robot.safety_margin = 0.15
		robot.static_safety_margin = 0.01  # Új paraméter a statikus falak melletti tűréshez
		robot.Alfa = 5
		robot.Beta = 2
		robot.Gamma = 3
		robot.enable_waypoint_slowdown = False


# Robot pillanatnyi állapota.
class robotstate:
	def __init__(robot, x=0, y=0, v=0, w=0, irany=0, w_L=0, w_R=0):
		robot.x = x
		robot.y = y
		robot.v = v
		robot.w = w
		robot.irany = irany
		robot.w_L = w_L
		robot.w_R = w_R


# Robotállapot léptetése dt idővel a kerékparancsok szerint.
def update(robot, config, w_L_target, w_R_target, dt):
	"""Frissíti a robotot a gyorsuláskorlátozás és a kinematika alapján."""
	max_w_dot = config.a_max / config.r_kerek
	w_L_new = robot.w_L + np.clip(
		w_L_target - robot.w_L,
		-max_w_dot * dt,
		max_w_dot * dt,
	)
	w_R_new = robot.w_R + np.clip(
		w_R_target - robot.w_R,
		-max_w_dot * dt,
		max_w_dot * dt,
	)
	v, w = get_robot_kinematics(w_L_new, w_R_new, config)
	theta_0 = robot.irany

	if abs(w) > 1e-6:
		robot.x += (v / w) * (math.sin(theta_0 + w * dt) - math.sin(theta_0))
		robot.y += -(v / w) * (math.cos(theta_0 + w * dt) - math.cos(theta_0))
	else:
		robot.x += v * math.cos(theta_0) * dt
		robot.y += v * math.sin(theta_0) * dt

	robot.irany += w * dt
	robot.v = v
	robot.w = w
	robot.w_L = w_L_new
	robot.w_R = w_R_new

	return np.array([robot.x, robot.y, robot.irany, robot.v, robot.w, robot.w_L, robot.w_R])