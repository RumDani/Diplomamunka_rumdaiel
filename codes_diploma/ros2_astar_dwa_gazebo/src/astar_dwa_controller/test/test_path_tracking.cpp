#include "../src/path_tracking.hpp"

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
      std::cout << "Path tracking regression checks passed\n";
}