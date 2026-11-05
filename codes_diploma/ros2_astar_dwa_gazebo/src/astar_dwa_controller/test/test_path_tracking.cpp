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
  std::cout << "Path tracking regression checks passed\n";
}