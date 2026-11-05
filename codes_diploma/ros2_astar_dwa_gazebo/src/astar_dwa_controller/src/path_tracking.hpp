#pragma once

#include <algorithm>
#include <cmath>
#include <cstddef>
#include <limits>
#include <utility>
#include <vector>

namespace path_tracking {
using Path = std::vector<std::pair<double, double>>;

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
  const double linear = std::abs(heading_error) >= 0.6 ? 0.0 :
    std::min(max_linear, 0.8 * target_distance) * std::max(0.0, std::cos(heading_error));
  return {linear, angular};
}

inline double command_error(double linear, double angular,
                             const std::pair<double, double> & reference,
                             double max_linear, double max_angular) {
  const double linear_error = (linear - reference.first) / std::max(max_linear, 1e-3);
  const double angular_error = (angular - reference.second) / std::max(max_angular, 1e-3);
  return linear_error * linear_error + angular_error * angular_error;
}
}