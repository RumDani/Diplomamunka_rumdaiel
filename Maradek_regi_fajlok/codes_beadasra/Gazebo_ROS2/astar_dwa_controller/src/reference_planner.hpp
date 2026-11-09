#pragma once

#include <algorithm>
#include <cmath>
#include <cstddef>
#include <cstdint>
#include <functional>
#include <limits>
#include <queue>
#include <tuple>
#include <utility>
#include <vector>
#include "path_tracking.hpp"

namespace reference_planner {
constexpr double pi = 3.14159265358979323846;
using Point = std::pair<double, double>;
using Path = std::vector<Point>;

inline double angle_error(double angle) {
	return std::atan2(std::sin(angle), std::cos(angle));
}

struct Config {
	double wheel_radius{0.033}, half_axle{0.1435}, wheel_max{0.26 / 0.033};
	double wheel_resolution{0.5}, acceleration{1.0}, dt{0.1}, predict_time{3.0};
	double radius{0.237}, safety_margin{0.15}, static_margin{0.03};
	double alpha{5.0}, beta{2.0}, gamma{3.0};
	double dynamic_clearance_weight{4.0}, dynamic_clearance_distance{0.6};
	bool waypoint_slowdown{false};
};

struct State {
	double x{0.0}, y{0.0}, yaw{0.0}, velocity{0.0}, angular{0.0}, left{0.0}, right{0.0};
};

struct Obstacle { double x, y, radius, vx, vy; };
struct Command { double velocity{0.0}, angular{0.0}, left{0.0}, right{0.0}; };
struct Result {
	Command command;
	std::size_t candidates{0}, admissible{0};
	std::size_t rejected_velocity{0}, rejected_dynamic{0}, rejected_braking{0};
	std::size_t rejected_dynamic_now{0};
	std::size_t forward_pairs{0};
	double score_progress{0.0}, score_dynamic{0.0}, score_distance{0.0};
	double clearance_gain{0.0};
	bool found{false};
	bool clearance_preferred{false};
	bool reorient{false}, approaching_obstacle{false};
};

inline Command kinematics(double left, double right, const Config & config) {
	return {(left + right) * 0.5 * config.wheel_radius,
					(right - left) * config.wheel_radius / (2.0 * config.half_axle), left, right};
}

inline void update(State & state, const Config & config, const Command & target) {
	const double step = config.acceleration / config.wheel_radius * config.dt;
	state.left += std::clamp(target.left - state.left, -step, step);
	state.right += std::clamp(target.right - state.right, -step, step);
	const auto command = kinematics(state.left, state.right, config);
	if (std::abs(command.angular) > 1e-6) {
		state.x += command.velocity / command.angular *
			(std::sin(state.yaw + command.angular * config.dt) - std::sin(state.yaw));
		state.y -= command.velocity / command.angular *
			(std::cos(state.yaw + command.angular * config.dt) - std::cos(state.yaw));
	} else {
		state.x += command.velocity * std::cos(state.yaw) * config.dt;
		state.y += command.velocity * std::sin(state.yaw) * config.dt;
	}
	state.yaw += command.angular * config.dt;
	state.velocity = command.velocity;
	state.angular = command.angular;
}

struct Trajectory {
	double distance{10.0};
	double dynamic_clearance{std::numeric_limits<double>::infinity()};
	bool dynamic_collision{false};
	bool initial_dynamic_collision{false};
};

inline Trajectory trajectory_distance(const Config & config, const State & state,
																	const Command & command, const std::vector<Obstacle> & obstacles) {
	State predicted = state;
	double travelled = 0.0;
	Trajectory result;
	for (std::size_t step = 0; step * config.dt < config.predict_time; ++step) {
		for (const auto & obstacle : obstacles) {
			const bool moving = obstacle.vx != 0.0 || obstacle.vy != 0.0;
			const double clearance = config.radius + obstacle.radius +
				(moving ? config.safety_margin : config.static_margin);
			const double separation = std::hypot(predicted.x - obstacle.x - obstacle.vx * step * config.dt,
				predicted.y - obstacle.y - obstacle.vy * step * config.dt) - clearance;
			if (moving) result.dynamic_clearance = std::min(result.dynamic_clearance, separation);
			if (separation <= 0.0) {
				if (result.distance == 10.0) result.distance = travelled;
				if (moving) {
					result.dynamic_collision = true;
					result.initial_dynamic_collision = step == 0;
					return result;
				}
			}
		}
		update(predicted, config, command);
		travelled += std::abs(command.velocity) * config.dt;
	}
	return result;
}

inline std::vector<double> wheel_samples(double measured, const Config & config) {
	const double step = config.acceleration / config.wheel_radius * config.dt;
	const double lower = std::clamp(measured - step, -config.wheel_max, config.wheel_max);
	const double upper = std::clamp(measured + step, -config.wheel_max, config.wheel_max);
	std::vector<double> samples;
	const auto count = static_cast<std::size_t>(std::ceil((upper - lower) / config.wheel_resolution));
	for (std::size_t index = 0; index <= count; ++index)
		samples.push_back(std::min(upper, lower + index * config.wheel_resolution));
	return samples;
}

inline void add_rotation_samples(std::vector<double> & left_samples,
								 std::vector<double> & right_samples,
								 const State & state, const Config & config,
								 double preferred_left) {
	const double step = config.acceleration / config.wheel_radius * config.dt;
	const double left_min = std::max(-config.wheel_max, state.left - step);
	const double left_max = std::min(config.wheel_max, state.left + step);
	const double right_min = std::max(-config.wheel_max, state.right - step);
	const double right_max = std::min(config.wheel_max, state.right + step);
	const double rotation_min = std::max(left_min, -right_max);
	const double rotation_max = std::min(left_max, -right_min);
	if (rotation_min > rotation_max) return;
	const auto append_unique = [](std::vector<double> & samples, double value) {
		if (std::none_of(samples.begin(), samples.end(), [value](double sample) {
				return std::abs(sample - value) < 1e-9;
			})) samples.push_back(value);
	};
	for (const double left : {rotation_min, rotation_max,
							  std::clamp(preferred_left, rotation_min, rotation_max)}) {
		append_unique(left_samples, left);
		append_unique(right_samples, -left);
	}
}

inline Result optimise(const Config & config, const State & state, Point goal,
											 bool final_waypoint, const std::vector<Obstacle> & sensed,
											 const Path * reference_path = nullptr, std::size_t waypoint = 0) {
	std::vector<Obstacle> visible;
	for (const auto & obstacle : sensed) {
		if (std::hypot(obstacle.x - state.x, obstacle.y - state.y) <= 3.0)
			visible.push_back(obstacle);
	}
	const double goal_distance = std::hypot(goal.first - state.x, goal.second - state.y);
	const double near_goal_horizon = goal_distance < 1.0 ? std::max(0.5, goal_distance * 2.0) : config.predict_time;
	const double maximum_velocity = config.wheel_max * config.wheel_radius;
	const bool track_path = reference_path != nullptr && !reference_path->empty();
	const std::size_t first = track_path ? std::min(waypoint > 0 ? waypoint - 1 : 0, reference_path->size() - 1) : 0;
	const std::size_t last = track_path ? std::min(first + 25, reference_path->size() - 1) : 0;
	const double initial_path_position = track_path ?
		path_tracking::project_position(*reference_path, first, last, state.x, state.y).along : 0.0;
	const double heading_error = angle_error(std::atan2(goal.second - state.y, goal.first - state.x) - state.yaw);
	bool approaching_obstacle = false;
	for (const auto & obstacle : visible) {
		if (obstacle.vx == 0.0 && obstacle.vy == 0.0) continue;
		if (path_tracking::collision_course(obstacle.x - state.x, obstacle.y - state.y,
				obstacle.vx - maximum_velocity * std::cos(state.yaw + heading_error),
				obstacle.vy - maximum_velocity * std::sin(state.yaw + heading_error),
				config.radius + obstacle.radius + config.safety_margin, config.predict_time)) {
			approaching_obstacle = true;
			break;
		}
	}
	const double horizon = approaching_obstacle ? config.predict_time : near_goal_horizon;
	const double heading_scale = approaching_obstacle ? 0.25 : 1.0;
	const auto braking_trajectory = approaching_obstacle ?
		trajectory_distance(config, state, Command{}, visible) : Trajectory{};
	const bool reorient = std::abs(heading_error) > pi / 2.0 && !approaching_obstacle;
	const double target_speed = reorient ? 0.0 : maximum_velocity;
	const double velocity_limit = reorient ? std::max(0.0, state.velocity - config.acceleration * config.dt) : maximum_velocity;
	auto left_samples = wheel_samples(state.left, config);
	auto right_samples = wheel_samples(state.right, config);
	const double preferred_rotation = reorient ?
		-heading_error * config.half_axle / config.wheel_radius : 0.0;
	add_rotation_samples(left_samples, right_samples, state, config, preferred_rotation);
	const bool slowdown = config.waypoint_slowdown || final_waypoint;
	const double slowdown_distance = final_waypoint ? 0.5 : 0.35;
	double best_score = -std::numeric_limits<double>::infinity();
	double best_rotation_score = -std::numeric_limits<double>::infinity();
	Command best_rotation;
	bool have_rotation = false;
	Result result;
	result.reorient = reorient;
	result.approaching_obstacle = approaching_obstacle;
	for (double left : left_samples) {
		for (double right : right_samples) {
			++result.candidates;
			const auto command = kinematics(left, right, config);
			if (command.velocity < 0.0 || command.velocity > velocity_limit + 1e-9) {
				++result.rejected_velocity;
				continue;
			}
			const auto trajectory = trajectory_distance(config, state, command, visible);
			if (trajectory.dynamic_collision) {
				++result.rejected_dynamic;
				if (trajectory.initial_dynamic_collision) ++result.rejected_dynamic_now;
				continue;
			}
			if (command.velocity > std::sqrt(2.0 * config.acceleration * trajectory.distance)) {
				++result.rejected_braking;
				continue;
			}
			++result.admissible;
			if (command.velocity > 0.01) ++result.forward_pairs;
			State predicted = state;
			for (std::size_t step = 0; step * config.dt < horizon; ++step) update(predicted, config, command);
			const double heading = std::atan2(goal.second - predicted.y, goal.first - predicted.x);
			const double heading_score = (pi - std::abs(angle_error(heading - predicted.yaw))) / pi;
			const double predicted_goal_distance = std::hypot(goal.first - predicted.x, goal.second - predicted.y);
			const double progress = track_path ?
				path_tracking::project_position(*reference_path, first, last, predicted.x, predicted.y).along - initial_path_position :
				goal_distance - predicted_goal_distance;
			const double progress_score = std::clamp(
				progress / (maximum_velocity * horizon), -1.0, 1.0);
			const double target_velocity = std::min(target_speed, std::max(0.08, goal_distance * 1.4));
			const double velocity_score = !slowdown && goal_distance > slowdown_distance ?
				command.velocity / maximum_velocity :
				1.0 - std::abs(target_velocity - command.velocity) / maximum_velocity;
			const double dynamic_score = std::isfinite(trajectory.dynamic_clearance) ?
				std::clamp(trajectory.dynamic_clearance / config.dynamic_clearance_distance, 0.0, 1.0) : 0.0;
			const double clearance_gain = approaching_obstacle && std::isfinite(braking_trajectory.dynamic_clearance) ?
				trajectory.dynamic_clearance - braking_trajectory.dynamic_clearance : 0.0;
			const bool clearance_preferred = approaching_obstacle && command.velocity > 0.01 && clearance_gain > 0.02;
			const double score = config.alpha * (heading_scale * heading_score + progress_score) + config.beta * trajectory.distance +
				config.gamma * velocity_score + config.dynamic_clearance_weight * dynamic_score;
			if (std::abs(command.velocity) <= 1e-9 && std::abs(command.angular) > 1e-6) {
				if (!have_rotation || score > best_rotation_score) {
					best_rotation_score = score;
					best_rotation = command;
					have_rotation = true;
				}
				continue;
			}
			if (!result.found || path_tracking::prefer_candidate(
					clearance_preferred, score, result.clearance_preferred, best_score)) {
				best_score = score;
				result.command = command;
				result.found = true;
				result.clearance_preferred = clearance_preferred;
				result.clearance_gain = clearance_gain;
				result.score_progress = config.alpha * progress_score;
				result.score_dynamic = config.dynamic_clearance_weight * dynamic_score;
				result.score_distance = config.beta * trajectory.distance;
			}
		}
	}
	if (result.forward_pairs == 0 && have_rotation) {
		result.command = best_rotation;
		result.found = true;
	}
	return result;
}

struct Grid {
	int width{0}, height{0};
	double resolution{0.1}, origin_x{0.0}, origin_y{0.0};
	std::vector<std::int8_t> blocked;

	bool free(int row, int column) const {
		return row >= 0 && column >= 0 && row < height && column < width &&
			blocked[static_cast<std::size_t>(row) * width + column] == 0;
	}
	std::pair<int, int> cell(Point point) const {
		return {static_cast<int>(std::floor((point.second - origin_y) / resolution)),
						static_cast<int>(std::floor((point.first - origin_x) / resolution))};
	}
	Point world(int row, int column) const {
		return {origin_x + (column + 0.5) * resolution, origin_y + (row + 0.5) * resolution};
	}
	bool connected(std::pair<int, int> start, std::pair<int, int> finish) const {
		const int row_step = finish.first - start.first, column_step = finish.second - start.second;
		return std::abs(row_step) <= 1 && std::abs(column_step) <= 1 && free(finish.first, finish.second) &&
			(row_step == 0 || column_step == 0 || (free(start.first, finish.second) && free(finish.first, start.second)));
	}
	Path astar(Point start_world, Point goal_world) const {
		const auto start = cell(start_world), goal = cell(goal_world);
		if (!free(start.first, start.second) || !free(goal.first, goal.second)) return {};
		const auto index = [this](int row, int column) { return row * width + column; };
		const auto heuristic = [&goal](int row, int column) { return std::hypot(goal.first - row, goal.second - column); };
		using Entry = std::tuple<double, double, int, int>;
		std::priority_queue<Entry, std::vector<Entry>, std::greater<Entry>> open;
		std::vector<double> costs(blocked.size(), std::numeric_limits<double>::infinity());
		std::vector<int> parents(blocked.size(), -1);
		costs[index(start.first, start.second)] = 0.0;
		open.emplace(heuristic(start.first, start.second), 0.0, start.first, start.second);
		const int directions[8][2] = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}, {-1, -1}, {-1, 1}, {1, -1}, {1, 1}};
		while (!open.empty()) {
			const auto [priority, cost, row, column] = open.top();
			(void)priority;
			open.pop();
			if (cost > costs[index(row, column)]) continue;
			if (std::make_pair(row, column) == goal) break;
			for (const auto & direction : directions) {
				const int next_row = row + direction[0], next_column = column + direction[1];
				if (!connected({row, column}, {next_row, next_column})) continue;
				const double next_cost = cost + std::hypot(direction[0], direction[1]);
				const int next_index = index(next_row, next_column);
				if (next_cost >= costs[next_index]) continue;
				costs[next_index] = next_cost;
				parents[next_index] = index(row, column);
				open.emplace(next_cost + heuristic(next_row, next_column), next_cost, next_row, next_column);
			}
		}
		int current = index(goal.first, goal.second);
		const int first = index(start.first, start.second);
		if (current != first && parents[current] < 0) return {};
		Path path;
		while (current >= 0) {
			path.push_back(world(current / width, current % width));
			if (current == first) break;
			current = parents[current];
		}
		std::reverse(path.begin(), path.end());
		return path;
	}
	bool safe(const Path & path) const {
		if (path.empty()) return true;
		auto previous = cell(path.front());
		if (!free(previous.first, previous.second)) return false;
		for (std::size_t index = 1; index < path.size(); ++index) {
			const Point delta{path[index].first - path[index - 1].first, path[index].second - path[index - 1].second};
			const int count = std::max(1, static_cast<int>(std::ceil(std::max(std::abs(delta.first), std::abs(delta.second)) / resolution)));
			for (int step = 1; step <= count; ++step) {
				const double fraction = static_cast<double>(step) / count;
				const auto next = cell({path[index - 1].first + fraction * delta.first, path[index - 1].second + fraction * delta.second});
				if (!connected(previous, next)) return false;
				previous = next;
			}
		}
		return true;
	}
	Path smooth(const Path & path) const {
		if (path.size() < 3) return path;
		Path turns{path.front()};
		for (std::size_t index = 1; index + 1 < path.size(); ++index) {
			const double incoming_x = path[index].first - path[index - 1].first;
			const double incoming_y = path[index].second - path[index - 1].second;
			const double outgoing_x = path[index + 1].first - path[index].first;
			const double outgoing_y = path[index + 1].second - path[index].second;
			if (std::abs(incoming_x * outgoing_y - incoming_y * outgoing_x) > 1e-10) turns.push_back(path[index]);
		}
		turns.push_back(path.back());
		if (turns.size() < 3) return path;
		const auto cut = [this](Point center, Point neighbor) {
			const double length = std::hypot(neighbor.first - center.first, neighbor.second - center.second);
			const double fraction = length == 0.0 ? 1.0 : std::min(1.0, 0.5 * resolution / length);
			return Point{center.first + fraction * (neighbor.first - center.first), center.second + fraction * (neighbor.second - center.second)};
		};
		Path curve{turns.front()};
		for (std::size_t index = 1; index + 1 < turns.size(); ++index) {
			const Point start = index == 1 ? turns.front() : cut(turns[index], turns[index - 1]);
			const Point finish = index + 2 == turns.size() ? turns.back() : cut(turns[index], turns[index + 1]);
			for (int sample = 1; sample <= 8; ++sample) {
				const double parameter = sample / 8.0, weight = 1.0 - parameter;
				curve.emplace_back(weight * weight * start.first + 2.0 * weight * parameter * turns[index].first + parameter * parameter * finish.first,
													 weight * weight * start.second + 2.0 * weight * parameter * turns[index].second + parameter * parameter * finish.second);
			}
		}
		curve.push_back(turns.back());
		for (std::size_t index = 1; index + 1 < curve.size(); ++index) {
			if ((curve[index].first - curve[index - 1].first) * (curve[index + 1].first - curve[index].first) +
					(curve[index].second - curve[index - 1].second) * (curve[index + 1].second - curve[index].second) < -1e-9) return path;
		}
		return safe(curve) ? curve : path;
	}
};

inline Path resample(const Path & path, double spacing = 0.2) {
	if (path.empty()) return {};
	Path points{path.front()};
	double remaining = spacing;
	Point start = path.front();
	for (std::size_t index = 1; index < path.size(); ++index) {
		double delta_x = path[index].first - start.first, delta_y = path[index].second - start.second;
		double length = std::hypot(delta_x, delta_y);
		if (length == 0.0) continue;
		while (length >= remaining) {
			const double fraction = remaining / length;
			start = {start.first + fraction * delta_x, start.second + fraction * delta_y};
			points.push_back(start);
			delta_x = path[index].first - start.first;
			delta_y = path[index].second - start.second;
			length = std::hypot(delta_x, delta_y);
			remaining = spacing;
		}
		remaining -= length;
		start = path[index];
	}
	if (points.back() != path.back()) points.push_back(path.back());
	return points;
}
}