#pragma once

#include <algorithm>
#include <cmath>
#include <cstddef>
#include <functional>
#include <limits>
#include <utility>
#include <vector>

namespace path_tracking {
using Path = std::vector<std::pair<double, double>>;

struct TrackingTarget {
  std::size_t waypoint{0}, target_index{0};
  std::pair<double, double> projection, target;
  double lookahead{0.35};
};

inline TrackingTarget prune_lookahead(
  const Path & path, std::size_t current, double x, double y, double velocity,
  const std::function<bool(const std::pair<double, double> &)> & reachable) {
  TrackingTarget result;
  if (path.empty()) return result;
  current = std::min(current, path.size() - 1);
  result.waypoint = result.target_index = current;
  result.projection = result.target = path[current];
  result.lookahead = std::clamp(0.35 + std::abs(velocity) * 1.2, 0.35, 0.80);
  if (path.size() == 1) return result;
  const std::size_t first = current > 0 ? current - 1 : 0;
  const std::size_t end = std::min(path.size() - 1, current + 25);
  std::size_t segment = first;
  bool found = false;
  double nearest = std::numeric_limits<double>::infinity();
  for (std::size_t index = first; index < end; ++index) {
    const double delta_x = path[index + 1].first - path[index].first;
    const double delta_y = path[index + 1].second - path[index].second;
    const double length_squared = delta_x * delta_x + delta_y * delta_y;
    const double fraction = length_squared > 0.0 ? std::clamp(
      ((x - path[index].first) * delta_x + (y - path[index].second) * delta_y) / length_squared, 0.0, 1.0) : 0.0;
    const std::pair<double, double> projected{
      path[index].first + fraction * delta_x, path[index].second + fraction * delta_y};
    const double distance = std::hypot(projected.first - x, projected.second - y);
    if (distance >= nearest || !reachable(projected)) continue;
    nearest = distance;
    found = true;
    segment = index;
    result.projection = projected;
    result.waypoint = std::max(current, index + (fraction > 1e-9 ? 1 : 0));
  }
  if (!found) return result;
  const auto along_path = [&](double remaining) {
    auto start = result.projection;
    for (std::size_t index = segment + 1; index < path.size(); ++index) {
      const double delta_x = path[index].first - start.first;
      const double delta_y = path[index].second - start.second;
      const double length = std::hypot(delta_x, delta_y);
      if (length > 0.0 && remaining < length) {
        return std::make_pair(std::pair<double, double>{start.first + remaining / length * delta_x,
                                                       start.second + remaining / length * delta_y}, index);
      }
      remaining -= length;
      start = path[index];
    }
    return std::make_pair(path.back(), path.size() - 1);
  };
  for (double lookahead = result.lookahead; lookahead >= 0.05; lookahead *= 0.5) {
    const auto candidate = along_path(lookahead);
    if (!reachable(candidate.first)) continue;
    result.target = candidate.first;
    result.target_index = candidate.second;
    result.lookahead = lookahead;
    return result;
  }
  result.target = result.projection;
  result.target_index = result.waypoint;
  result.lookahead = 0.0;
  return result;
}

inline double distance_to_path(const Path & path, std::size_t first, std::size_t last,
                               double x, double y) {
  if (path.empty()) return std::numeric_limits<double>::infinity();
  first = std::min(first, path.size() - 1);
  last = std::clamp(last, first, path.size() - 1);
  double nearest = std::hypot(x - path[first].first, y - path[first].second);
  for (std::size_t index = first; index < last; ++index) {
    const auto & start = path[index];
    const auto & end = path[index + 1];
    const double dx = end.first - start.first;
    const double dy = end.second - start.second;
    const double length_squared = dx * dx + dy * dy;
    // Measure against the finite segment, not just its waypoints or an infinite line.
    const double fraction = length_squared > 0.0 ? std::clamp(
      ((x - start.first) * dx + (y - start.second) * dy) / length_squared, 0.0, 1.0) : 0.0;
    nearest = std::min(nearest, std::hypot(
      x - start.first - fraction * dx, y - start.second - fraction * dy));
  }
  return nearest;
}

inline double tracking_cost(const Path & path, std::size_t first, std::size_t last,
                            double x, double y, double target_x, double target_y,
                            double path_distance_bias, double goal_distance_bias) {
  return path_distance_bias * distance_to_path(path, first, last, x, y) +
         goal_distance_bias * std::hypot(target_x - x, target_y - y);
}

inline double return_progress(double initial_distance, double final_distance, double max_travel) {
  return std::clamp((initial_distance - final_distance) / std::max(max_travel, 1e-3), -1.0, 1.0);
}

inline bool is_returning(double initial_distance, double final_distance,
                         double tolerance, double max_travel) {
  return initial_distance > tolerance &&
         (final_distance <= tolerance ||
          return_progress(initial_distance, final_distance, max_travel) >= 0.05);
}

inline bool prefer_candidate(bool returning, double score, bool best_returning, double best_score) {
  return returning != best_returning ? returning : score > best_score;
}

inline std::pair<double, double> rejoin_command(double target_distance, double heading_error,
                                               double max_linear, double max_angular) {
  const double angular = std::clamp(2.0 * heading_error, -max_angular, max_angular);
  const double linear = std::abs(heading_error) >= 1.2 ? 0.0 :
    std::min(max_linear, 1.5 * target_distance) * std::max(0.0, std::cos(heading_error));
  return {linear, angular};
}

inline double command_error(double linear, double angular,
                             const std::pair<double, double> & reference,
                             double max_linear, double max_angular) {
  const double linear_error = (linear - reference.first) / std::max(max_linear, 1e-3);
  const double angular_error = (angular - reference.second) / std::max(max_angular, 1e-3);
  return linear_error * linear_error + angular_error * angular_error;
}

inline bool collision_course(double relative_x, double relative_y,
                              double relative_vx, double relative_vy,
                              double clearance, double horizon) {
  if (std::hypot(relative_x, relative_y) <= clearance) return true;
  const double closing_dot = relative_x * relative_vx + relative_y * relative_vy;
  const double speed_squared = relative_vx * relative_vx + relative_vy * relative_vy;
  if (closing_dot >= 0.0 || speed_squared < 1e-9) return false;
  const double closest_time = std::clamp(-closing_dot / speed_squared, 0.0, horizon);
  return std::hypot(relative_x + relative_vx * closest_time,
                    relative_y + relative_vy * closest_time) <= clearance;
}
}