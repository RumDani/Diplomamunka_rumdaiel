#include "../src/path_tracking.hpp"
#include "../src/reference_planner.hpp"

#include <iostream>
#include <stdexcept>

void require(bool condition, const char * message) {
  if (!condition) throw std::runtime_error(message);
}

void near(double actual, double expected, const char * message) {
  require(std::abs(actual - expected) < 1e-9, message);
}

int main() {
  using path_tracking::distance_to_path;
  using path_tracking::tracking_cost;
  const path_tracking::Path straight{{0.0, 0.0}, {1.0, 0.0}, {2.0, 0.0}};
  near(distance_to_path(straight, 0, 2, 0.5, 0.0), 0.0, "Use segments, not vertices");
  near(distance_to_path(straight, 0, 2, 0.5, 0.4), 0.4, "Measure lateral offset");
  near(distance_to_path(straight, 0, 2, -0.3, 0.4), 0.5, "Clamp segment projection");
  const path_tracking::Path repeated{{0.0, 0.0}, {0.0, 0.0}, {1.0, 0.0}};
  near(distance_to_path(repeated, 0, 2, 0.5, 0.2), 0.2, "Handle duplicate points");
  near(distance_to_path({{1.0, 1.0}}, 0, 0, 1.3, 1.4), 0.5, "Handle single point");
  require(std::isinf(distance_to_path({}, 0, 0, 0.0, 0.0)), "Empty path is not trackable");
  const path_tracking::Path corner{{0.0, 0.0}, {1.0, 0.0}, {1.0, 1.0}};
  near(distance_to_path(corner, 0, 2, 1.3, 0.6), 0.3, "Follow a corner");
  const path_tracking::Path hairpin{{0.0, 0.0}, {2.0, 0.0}, {2.0, 0.5}, {0.0, 0.5}};
  near(distance_to_path(hairpin, 0, 1, 0.5, 0.5), 0.5, "Do not reward a future return branch");

    const auto initial_position = path_tracking::project_position(straight, 0, 2, 0.5, 0.0);
    const auto detour_position = path_tracking::project_position(straight, 0, 2, 0.8, 0.8);
    near(initial_position.along, 0.5, "Locate the robot by path arc length");
    near(detour_position.along, 0.8, "Lateral detour can still advance along the path");
    require(detour_position.along > initial_position.along,
      "Do not penalize forward detours for moving away from a nearby goal");
    near(path_tracking::project_position(corner, 0, 2, 1.0, 0.6).along, 1.6,
      "Accumulate arc length around a corner");
    near(path_tracking::project_position(repeated, 0, 2, 0.5, 0.2).along, 0.5,
      "Project safely over duplicate path points");
    near(path_tracking::project_position(hairpin, 0, 1, 0.5, 0.5).along, 0.5,
      "Respect the local projection window");
    require(std::isinf(path_tracking::project_position({}, 0, 0, 0.0, 0.0).distance),
      "An empty reference path has no projection");

  const double parallel_cost = tracking_cost(straight, 0, 2, 0.8, 0.4, 1.0, 0.0, 6.0, 2.0);
  const double returning_cost = tracking_cost(straight, 0, 2, 0.75, 0.1, 1.0, 0.0, 6.0, 2.0);
  require(returning_cost < parallel_cost, "Prefer return over parallel offset");
  const double parallel_score = 5.0 * 0.95 + 2.0 * 0.8 + 3.0 - parallel_cost;
  const double returning_score = 5.0 * 0.9 + 2.0 * 0.6 + 3.0 - returning_cost;
  require(returning_score > parallel_score, "Return must overcome moderate clearance preference");
  require(tracking_cost(straight, 0, 2, 0.9, 0.0, 1.0, 0.0, 6.0, 2.0) <
          tracking_cost(straight, 0, 2, 0.2, 0.0, 1.0, 0.0, 6.0, 2.0),
          "Reward approaching target, not merely aligning yaw");
  near(tracking_cost(straight, 0, 2, 0.8, 0.4, 1.0, 0.0, 0.0, 0.0), 0.0,
       "Zero biases preserve legacy scoring");
    near(path_tracking::return_progress(0.4, 0.4, 0.44), 0.0,
         "Parallel travel has no lateral progress");
    require(path_tracking::is_returning(0.4, 0.35, 0.1, 0.44),
      "A five-centimeter return is meaningful within this horizon");
    require(!path_tracking::is_returning(0.4, 0.399, 0.1, 0.44),
      "Numerical-scale improvement is not a return");
    require(path_tracking::is_returning(0.11, 0.10, 0.1, 0.44),
      "Reaching the tolerance counts as returning");
    require(path_tracking::prefer_candidate(true, -10.0, false, 100.0),
      "A safe meaningful return beats any parallel reward");
    require(!path_tracking::prefer_candidate(false, 100.0, true, -10.0),
      "Parallel motion cannot displace an existing safe return");
    require(path_tracking::prefer_candidate(false, 2.0, false, 1.0),
      "Without a return candidate normal avoidance remains available");
    require(path_tracking::prefer_candidate(true, 2.0, true, 1.0),
      "Use scores within the returning candidate class");
    const auto left_rejoin = path_tracking::rejoin_command(0.4, 1.4, 0.22, 1.0);
    near(left_rejoin.first, 0.0, "Turn before driving across the path");
    near(left_rejoin.second, 1.0, "Steer toward the fixed waypoint now");
    const auto right_rejoin = path_tracking::rejoin_command(0.4, -1.4, 0.22, 1.0);
    near(right_rejoin.second, -1.0, "Handle the opposite detour side");
    require(path_tracking::command_error(0.0, 1.0, left_rejoin, 0.22, 1.0) <
      path_tracking::command_error(0.22, 0.0, left_rejoin, 0.22, 1.0),
      "Immediate steering must beat parallel forward motion");
      near(path_tracking::rejoin_command(0.05, 0.0, 0.22, 1.0).first, 0.075,
         "Slow down when approaching the fixed waypoint");
      require(path_tracking::rejoin_command(0.4, 0.7, 0.22, 1.0).first > 0.1,
        "A moderate heading error must allow a moving return arc");
      require(path_tracking::collision_course(0.8, 0.0, -0.42, 0.0, 0.34, 2.0),
        "A head-on obstacle must keep avoidance active");
      require(!path_tracking::collision_course(-0.5, 0.0, -0.42, 0.0, 0.34, 2.0),
        "A passed receding obstacle must release avoidance");
      require(!path_tracking::collision_course(0.5, 0.6, -0.42, 0.0, 0.34, 2.0),
        "A safe lateral pass must not suppress path rejoin");
      require(path_tracking::collision_course(0.4, 0.6, -0.2, -0.3, 0.34, 2.0),
        "A crossing obstacle must still be detected");
      require(!path_tracking::collision_course(0.5, 0.0, 0.0, 0.0, 0.34, 2.0),
        "Constant safe separation is not a closing threat");
      path_tracking::Path dense;
      for (int index = 0; index <= 30; ++index) dense.emplace_back(index * 0.2, 0.0);
      const auto reachable = [](const std::pair<double, double> &) { return true; };
      const auto pruned = path_tracking::prune_lookahead(dense, 1, 1.1, 0.4, 0.0, reachable);
      require(pruned.waypoint == 6, "Prune multiple passed points after a detour");
      near(pruned.projection.first, 1.1, "Project onto the nearest forward segment");
      near(pruned.target.first, 1.45, "Look ahead along arc length from the projection");
      const auto faster = path_tracking::prune_lookahead(dense, 1, 1.1, 0.4, 0.25, reachable);
      near(faster.lookahead, 0.65, "Increase lookahead with actual TurtleBot speeds");
      near(faster.target.first, 1.75, "Move the DWA target forward with speed");
      require(path_tracking::prune_lookahead(dense, 8, 1.1, 0.4, 0.0, reachable).waypoint >= 8,
        "Never move the pruning index backward");
      const auto obstructed = path_tracking::prune_lookahead(dense, 1, 1.1, 0.4, 0.25,
        [](const std::pair<double, double> & point) { return point.first <= 1.7; });
      near(obstructed.lookahead, 0.325, "Shorten a blocked lookahead connector");
      near(obstructed.target.first, 1.425, "Use only a reachable forward target");
      const auto blocked = path_tracking::prune_lookahead(dense, 1, 1.1, 0.4, 0.0,
        [](const std::pair<double, double> &) { return false; });
      require(blocked.waypoint == 1, "Do not prune across an unreachable connector");
      const auto finish = path_tracking::prune_lookahead(dense, 29, 5.95, 0.0, 0.25, reachable);
      require(finish.target == dense.back(), "Clamp lookahead to the final goal");
      reference_planner::Config sampling_config;
      for (double measured : {0.0, sampling_config.wheel_max}) {
        sampling_config.wheel_resolution = 0.5;
        const auto fine_samples = reference_planner::wheel_samples(measured, sampling_config);
        sampling_config.wheel_resolution = 1.0;
        const auto coarse_samples = reference_planner::wheel_samples(measured, sampling_config);
        require(fine_samples.size() > coarse_samples.size(), "Finer wheel lattice offers more arcs");
        for (double coarse : coarse_samples)
          require(std::any_of(fine_samples.begin(), fine_samples.end(), [coarse](double fine) {
            return std::abs(fine - coarse) < 1e-9;
          }), "Retain the previous wheel candidates");
        for (double sample : fine_samples)
          require(std::abs(sample) <= sampling_config.wheel_max + 1e-9, "Respect physical wheel limits");
      }
      std::cout << "Path tracking regression checks passed\n";
}