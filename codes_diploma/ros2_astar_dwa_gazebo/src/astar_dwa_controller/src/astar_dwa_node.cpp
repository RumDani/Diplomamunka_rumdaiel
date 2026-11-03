#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <functional>
#include <limits>
#include <memory>
#include <optional>
#include <queue>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

#include "geometry_msgs/msg/pose_stamped.hpp"
#include "geometry_msgs/msg/transform_stamped.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include "nav_msgs/msg/occupancy_grid.hpp"
#include "nav_msgs/msg/path.hpp"
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"
#include "tf2_ros/transform_broadcaster.h"
#include "visualization_msgs/msg/marker_array.hpp"

namespace {
struct Obstacle { double x, y, radius; };
struct Pose { double x{0.0}, y{0.0}, yaw{0.0}; };
double angle_error(double value) { return std::atan2(std::sin(value), std::cos(value)); }
double distance(double ax, double ay, double bx, double by) {
  return std::hypot(ax - bx, ay - by);
}
}

class AStarDwaNode final : public rclcpp::Node {
public:
  AStarDwaNode() : Node("astar_dwa_node") {
    cmd_topic_ = declare_parameter("cmd_vel_topic", std::string("/cmd_vel"));
    odom_topic_ = declare_parameter("odom_topic", std::string("/odom"));
    scan_topic_ = declare_parameter("scan_topic", std::string("/scan"));
    goal_topic_ = declare_parameter("goal_topic", std::string("/goal_pose"));
    path_topic_ = declare_parameter("path_topic", std::string("/astar_path"));
    goal_x_ = declare_parameter("goal_x", 0.0);
    goal_y_ = declare_parameter("goal_y", 0.0);
    map_size_ = declare_parameter("map_size", 16.0);
    map_height_ = declare_parameter("map_height", 4.0);
    map_origin_x_ = declare_parameter("map_origin_x", 0.0);
    map_origin_y_ = declare_parameter("map_origin_y", 0.0);
    initial_pose_x_ = declare_parameter("initial_pose_x", 0.5);
    initial_pose_y_ = declare_parameter("initial_pose_y", 0.5);
    resolution_ = declare_parameter("resolution", 0.20);
    robot_radius_ = declare_parameter("robot_radius", 0.28);
    max_linear_velocity_ = declare_parameter("max_linear_velocity", 0.32);
    max_angular_velocity_ = declare_parameter("max_angular_velocity", 1.0);
    wheel_radius_ = declare_parameter("wheel_radius", 0.033);
    wheel_base_ = declare_parameter("wheel_base", 0.08);
    wheel_max_ = declare_parameter("wheel_max", 15.0);
    wheel_resolution_ = declare_parameter("wheel_resolution", 1.0);
    acceleration_limit_ = declare_parameter("acceleration_limit", 2.0);
    predict_time_ = declare_parameter("predict_time", 3.0);
    safety_margin_ = declare_parameter("safety_margin", 0.15);
    max_linear_velocity_ = 0.40;
    max_angular_velocity_ = 1.20;
    safety_margin_ = 0.15;
    alpha_ = declare_parameter("alpha", 5.0);
    beta_ = declare_parameter("beta", 2.0);
    gamma_ = declare_parameter("gamma", 3.0);
    known_obstacle_x_ = declare_parameter(
      "known_obstacle_x", std::vector<double>{});
    known_obstacle_y_ = declare_parameter(
      "known_obstacle_y", std::vector<double>{});
    known_obstacle_radius_ = declare_parameter(
      "known_obstacle_radius", std::vector<double>{});
    const double period = declare_parameter("control_period", 0.10);
    cmd_pub_ = create_publisher<geometry_msgs::msg::Twist>(cmd_topic_, 10);
    path_pub_ = create_publisher<nav_msgs::msg::Path>(path_topic_, 10);
    map_pub_ = create_publisher<nav_msgs::msg::OccupancyGrid>(
      "/astar_map", rclcpp::QoS(1).transient_local().reliable());
    marker_pub_ = create_publisher<visualization_msgs::msg::MarkerArray>("/astar_dwa_markers", 10);
    tf_broadcaster_ = std::make_unique<tf2_ros::TransformBroadcaster>(*this);
    odom_sub_ = create_subscription<nav_msgs::msg::Odometry>(
      odom_topic_, 10, [this](nav_msgs::msg::Odometry::ConstSharedPtr msg) { odom(msg); });
    scan_sub_ = create_subscription<sensor_msgs::msg::LaserScan>(
      scan_topic_, 10, [this](sensor_msgs::msg::LaserScan::ConstSharedPtr msg) { scan(msg); });
    goal_sub_ = create_subscription<geometry_msgs::msg::PoseStamped>(
      goal_topic_, 10, [this](geometry_msgs::msg::PoseStamped::ConstSharedPtr msg) {
        goal_x_ = msg->pose.position.x; goal_y_ = msg->pose.position.y;
        has_goal_ = true;
        RCLCPP_INFO(get_logger(), "Uj cel: x=%.2f m, y=%.2f m", goal_x_, goal_y_); });
    timer_ = create_wall_timer(
      std::chrono::duration_cast<std::chrono::milliseconds>(
        std::chrono::duration<double>(period)),
      [this]() { control(); });
    RCLCPP_INFO(get_logger(), "Robotfüggetlen A* + DWA C++ node elindult");
  }

private:
  void odom(const nav_msgs::msg::Odometry::ConstSharedPtr msg) {
    const auto & q = msg->pose.pose.orientation;
    pose_.x = msg->pose.pose.position.x + initial_pose_x_;
    pose_.y = msg->pose.pose.position.y + initial_pose_y_;
    pose_.yaw = std::atan2(2.0 * (q.w * q.z + q.x * q.y),
                           1.0 - 2.0 * (q.y * q.y + q.z * q.z));
    geometry_msgs::msg::TransformStamped transform;
    transform.header.stamp = msg->header.stamp;
    transform.header.frame_id = "odom";
    transform.child_frame_id = "base_link";
    transform.transform.translation.x = pose_.x;
    transform.transform.translation.y = pose_.y;
    transform.transform.rotation = q;
    tf_broadcaster_->sendTransform(transform);
    transform.header.frame_id = "base_link";
    transform.child_frame_id = "base_scan";
    transform.transform.translation.x = 0.0;
    transform.transform.translation.y = 0.0;
    transform.transform.translation.z = 0.16;
    transform.transform.rotation.x = 0.0;
    transform.transform.rotation.y = 0.0;
    transform.transform.rotation.z = 0.0;
    transform.transform.rotation.w = 1.0;
    tf_broadcaster_->sendTransform(transform);
    have_odom_ = true;
  }
  void scan(const sensor_msgs::msg::LaserScan::ConstSharedPtr msg) {
    scan_ = msg;
    have_scan_ = true;
  }
  int map_width() const {
    return std::max(3, static_cast<int>(std::ceil(map_size_ / resolution_)));
  }
  int map_height() const {
    return std::max(3, static_cast<int>(std::ceil(map_height_ / resolution_)));
  }
  std::vector<Obstacle> obstacles() const {
    std::vector<Obstacle> result;
    if (!scan_) return result;
    const auto static_obstacles = planning_obstacles();
    constexpr double max_sensor_distance = 3.0;
    constexpr double front_half_angle = 1.57079632679;
    for (std::size_t i = 0; i < scan_->ranges.size(); ++i) {
      const double r = scan_->ranges[i];
      if (!std::isfinite(r) || r < scan_->range_min || r > scan_->range_max) continue;
      if (r < 0.12) continue;
      const double relative_angle =
        scan_->angle_min + static_cast<double>(i) * scan_->angle_increment;
      if (r > max_sensor_distance || std::abs(angle_error(relative_angle)) > front_half_angle)
        continue;
      const double a = pose_.yaw + relative_angle;
      const double obstacle_x = pose_.x + r * std::cos(a);
      const double obstacle_y = pose_.y + r * std::sin(a);
      if (distance(pose_.x, pose_.y, obstacle_x, obstacle_y) < robot_radius_) continue;
      const double boundary_filter = robot_radius_ + safety_margin_ + 0.12;
      if (obstacle_x < map_origin_x_ + boundary_filter ||
          obstacle_x > map_origin_x_ + map_size_ - boundary_filter ||
          obstacle_y < map_origin_y_ + boundary_filter ||
          obstacle_y > map_origin_y_ + map_height_ - boundary_filter) {
        continue;
      }
      bool static_wall_point = false;
      for (const auto & static_obstacle : static_obstacles) {
        if (distance(obstacle_x, obstacle_y, static_obstacle.x, static_obstacle.y) <=
            static_obstacle.radius + robot_radius_ + safety_margin_) {
          static_wall_point = true;
          break;
        }
      }
      if (static_wall_point) continue;
      result.push_back({obstacle_x, obstacle_y, 0.0});
    }
    return result;
  }
  std::vector<Obstacle> planning_obstacles() const {
    std::vector<Obstacle> result;
    const std::size_t count = std::min(
      {known_obstacle_x_.size(), known_obstacle_y_.size(), known_obstacle_radius_.size()});
    for (std::size_t i = 0; i < count; ++i)
      result.push_back({known_obstacle_x_[i], known_obstacle_y_[i], known_obstacle_radius_[i]});
    return result;
  }
  std::vector<std::pair<double, double>> astar(
    const std::vector<Obstacle> & sensed_obstacles) const {
    const int width = std::max(3, static_cast<int>(std::ceil(map_size_ / resolution_)));
    const int height = map_height();
    const double ox = map_origin_x_, oy = map_origin_y_;
    std::vector<bool> blocked(width * height, false);
    auto inside = [width, height](int r, int c) { return r >= 0 && c >= 0 && r < height && c < width; };
    auto index = [width](int r, int c) { return r * width + c; };
    auto cell = [resolution = resolution_, ox, oy](double x, double y) {
      return std::pair<int, int>{static_cast<int>(std::floor((y - oy) / resolution)),
                                 static_cast<int>(std::floor((x - ox) / resolution))};
    };
    auto world = [resolution = resolution_, ox, oy](int r, int c) {
      return std::pair<double, double>{ox + (c + 0.5) * resolution, oy + (r + 0.5) * resolution};
    };
    (void)sensed_obstacles;
    const auto search_obstacles = planning_obstacles();
    for (const auto & obstacle : search_obstacles) {
      const auto center = cell(obstacle.x, obstacle.y);
      const double inflation = robot_radius_ + obstacle.radius + 0.25;
      const int radius = static_cast<int>(std::ceil(
        inflation / resolution_));
      for (int r = center.first - radius; r <= center.first + radius; ++r)
        for (int c = center.second - radius; c <= center.second + radius; ++c)
          if (inside(r, c)) {
            const auto point = world(r, c);
            if (distance(point.first, point.second, obstacle.x, obstacle.y) <= inflation) {
              blocked[index(r, c)] = true;
            }
          }
    }
    const double boundary_margin = robot_radius_ + safety_margin_;
    for (int r = 0; r < height; ++r) {
      for (int c = 0; c < width; ++c) {
        const auto point = world(r, c);
        if (point.first < ox + boundary_margin ||
            point.first > ox + map_size_ - boundary_margin ||
            point.second < oy + boundary_margin ||
            point.second > oy + map_height_ - boundary_margin) {
          blocked[index(r, c)] = true;
        }
      }
    }
    const auto start = cell(pose_.x, pose_.y), target = cell(goal_x_, goal_y_);
    if (!inside(start.first, start.second) || !inside(target.first, target.second) ||
        blocked[index(start.first, start.second)] || blocked[index(target.first, target.second)]) {
      RCLCPP_WARN_THROTTLE(
        get_logger(), *get_clock(), 5000,
        "A* ervenytelen kezdo/celcella: start=(%d,%d), cel=(%d,%d), "
        "start_blocked=%s, cel_blocked=%s",
        start.first, start.second, target.first, target.second,
        (inside(start.first, start.second) && blocked[index(start.first, start.second)])
          ? "igen" : "nem",
        (inside(target.first, target.second) && blocked[index(target.first, target.second)])
          ? "igen" : "nem");
      return {};
    }
    struct Entry { double f, g; int r, c; bool operator>(const Entry & other) const { return f > other.f; } };
    std::priority_queue<Entry, std::vector<Entry>, std::greater<Entry>> open;
    std::vector<double> cost(width * height, std::numeric_limits<double>::infinity());
    std::vector<int> parent(width * height, -1);
    auto heuristic = [&target](int r, int c) { return std::hypot(target.first - r, target.second - c); };
    open.push({heuristic(start.first, start.second), 0.0, start.first, start.second});
    cost[index(start.first, start.second)] = 0.0;
    const int directions[8][2] = {{1,0},{-1,0},{0,1},{0,-1},{1,1},{1,-1},{-1,1},{-1,-1}};
    while (!open.empty()) {
      const auto current = open.top(); open.pop();
      if (current.g > cost[index(current.r, current.c)]) continue;
      if (current.r == target.first && current.c == target.second) break;
      for (const auto & direction : directions) {
        const int nr = current.r + direction[0], nc = current.c + direction[1];
        if (!inside(nr, nc) || blocked[index(nr, nc)]) continue;
        if (direction[0] && direction[1] &&
            (blocked[index(current.r, nc)] || blocked[index(nr, current.c)])) continue;
        const double ng = current.g + ((direction[0] && direction[1]) ? std::sqrt(2.0) : 1.0);
        if (ng < cost[index(nr, nc)]) {
          cost[index(nr, nc)] = ng; parent[index(nr, nc)] = index(current.r, current.c);
          open.push({ng + heuristic(nr, nc), ng, nr, nc});
        }
      }
    }
    std::vector<std::pair<double, double>> path;
    int current = index(target.first, target.second), start_index = index(start.first, start.second);
    if (current != start_index && parent[current] < 0) return path;
    while (current >= 0) {
      path.push_back(world(current / width, current % width));
      if (current == start_index) break;
      current = parent[current];
    }
    std::reverse(path.begin(), path.end());
    return path;
  }
  void publish_map() {
    nav_msgs::msg::OccupancyGrid map;
    map.header.frame_id = "odom";
    map.header.stamp = now();
    map.info.resolution = resolution_;
    map.info.width = static_cast<std::uint32_t>(map_width());
    map.info.height = static_cast<std::uint32_t>(map_height());
    map.info.origin.position.x = map_origin_x_;
    map.info.origin.position.y = map_origin_y_;
    map.info.origin.orientation.w = 1.0;
    map.data.assign(map.info.width * map.info.height, 0);
    auto cell = [this](double x, double y) {
      return std::pair<int, int>{
        static_cast<int>(std::floor((x - map_origin_x_) / resolution_)),
        static_cast<int>(std::floor((y - map_origin_y_) / resolution_))};
    };
    const int width = static_cast<int>(map.info.width);
    for (const auto & obstacle : planning_obstacles()) {
      const auto center = cell(obstacle.x, obstacle.y);
      const int radius = static_cast<int>(std::ceil(
        (obstacle.radius + robot_radius_ + safety_margin_) / resolution_));
      for (int y = center.second - radius; y <= center.second + radius; ++y) {
        for (int x = center.first - radius; x <= center.first + radius; ++x) {
          if (x >= 0 && y >= 0 && x < width && y < map_height()) {
            const double dx = (x + 0.5) * resolution_ - (center.first + 0.5) * resolution_;
            const double dy = (y + 0.5) * resolution_ - (center.second + 0.5) * resolution_;
            if (std::hypot(dx, dy) <= obstacle.radius + robot_radius_ + safety_margin_) {
            map.data[y * width + x] = 100;
            }
          }
        }
      }
    }
    map_pub_->publish(map);
  }
  std::pair<double, double> wheel_kinematics(double left, double right) const {
    const double velocity = ((left + right) / 2.0) * wheel_radius_;
    const double angular = ((right - left) / (2.0 * wheel_base_)) * wheel_radius_;
    return {velocity, angular};
  }
  std::pair<double, double> dwa(double target_x, double target_y,
                                const std::vector<Obstacle> & sensed) {
    const double wheel_acceleration = acceleration_limit_ / wheel_radius_;
    const double left_min = std::max(-wheel_max_, wheel_left_ - wheel_acceleration * dt_);
    const double left_max = std::min(wheel_max_, wheel_left_ + wheel_acceleration * dt_);
    const double right_min = std::max(-wheel_max_, wheel_right_ - wheel_acceleration * dt_);
    const double right_max = std::min(wheel_max_, wheel_right_ + wheel_acceleration * dt_);
    double best_score = -std::numeric_limits<double>::infinity();
    double best_left = wheel_left_, best_right = wheel_right_;
    bool found_candidate = false;
    std::size_t rejected_velocity = 0;
    std::size_t rejected_boundary = 0;
    std::size_t rejected_obstacle = 0;
    std::size_t rejected_braking = 0;
    std::size_t tested_candidates = 0;
    const double dist_to_goal = distance(pose_.x, pose_.y, target_x, target_y);
    const double adaptive_predict_time = dist_to_goal < 1.0
      ? std::max(0.5, dist_to_goal * 2.0) : predict_time_;
    const double v_max_robot = max_linear_velocity_;
    const double v_target = std::min(
      v_max_robot, std::max(0.08, dist_to_goal * 1.4));
    for (double left = left_min; left <= left_max + wheel_resolution_ * 0.5;
         left += wheel_resolution_) {
      for (double right = right_min; right <= right_max + wheel_resolution_ * 0.5;
           right += wheel_resolution_) {
        ++tested_candidates;
        const auto candidate = wheel_kinematics(left, right);
        const double v = candidate.first;
        if (v < 0.0) {
          ++rejected_velocity;
          continue;
        }
        if (v > max_linear_velocity_ ||
            std::abs(candidate.second) > max_angular_velocity_) {
          ++rejected_velocity;
          continue;
        }
        double x = pose_.x, y = pose_.y, yaw = pose_.yaw;
        double simulated_left = wheel_left_, simulated_right = wheel_right_;
        double collision_distance = 10.0;
        bool safe = true;
        double accumulated_dist = 0.0;
        for (double t = 0.0; t < adaptive_predict_time; t += dt_) {
          simulated_left += std::clamp(
            left - simulated_left, -wheel_acceleration * dt_, wheel_acceleration * dt_);
          simulated_right += std::clamp(
            right - simulated_right, -wheel_acceleration * dt_, wheel_acceleration * dt_);
          const auto simulated = wheel_kinematics(simulated_left, simulated_right);
          if (std::abs(simulated.second) > 1e-6) {
            x += (simulated.first / simulated.second) *
              (std::sin(yaw + simulated.second * dt_) - std::sin(yaw));
            y -= (simulated.first / simulated.second) *
              (std::cos(yaw + simulated.second * dt_) - std::cos(yaw));
          } else {
            x += simulated.first * std::cos(yaw) * dt_;
            y += simulated.first * std::sin(yaw) * dt_;
          }
          yaw += simulated.second * dt_;
          accumulated_dist += std::abs(simulated.first) * dt_;
          const double margin = robot_radius_ + safety_margin_;
          if (x < map_origin_x_ + margin ||
              x > map_origin_x_ + map_size_ - margin ||
              y < map_origin_y_ + margin ||
              y > map_origin_y_ + map_height_ - margin) {
            collision_distance = accumulated_dist;
            if (collision_distance < 0.55) {
              safe = false;
              ++rejected_boundary;
            }
            break;
          }
          for (const auto & obstacle : sensed) {
            if (distance(pose_.x, pose_.y, obstacle.x, obstacle.y) < robot_radius_) continue;
            if (distance(x, y, obstacle.x, obstacle.y) <=
                robot_radius_ + obstacle.radius + safety_margin_) {
              collision_distance = accumulated_dist;
              if (collision_distance < 0.55) {
                safe = false;
                ++rejected_obstacle;
              }
              break;
            }
          }
          if (!safe || collision_distance < 10.0) break;
        }
        if (!safe) continue;
        if (std::abs(candidate.first) >
          std::sqrt(2.0 * acceleration_limit_ * collision_distance)) {
          ++rejected_braking;
          continue;
        }
        const double goal_heading = std::atan2(target_y - y, target_x - x);
        const double heading_score =
          (M_PI - std::abs(angle_error(goal_heading - yaw))) / M_PI;
        const double distance_score = collision_distance;
        const double velocity_score =
          1.0 - (std::abs(v_target - candidate.first) / v_max_robot);
        const double score = alpha_ * heading_score + beta_ * distance_score +
          gamma_ * velocity_score;
        if (score > best_score) {
          best_score = score;
          best_left = left;
          best_right = right;
          found_candidate = true;
        }
      }
    }
    RCLCPP_INFO_THROTTLE(
      get_logger(), *get_clock(), 2000,
      "DWA jeloltek: teszt=%zu, sebesseg=%zu, hatar=%zu, akadaly=%zu, fekezes=%zu, elfogadott=%s",
      tested_candidates, rejected_velocity, rejected_boundary, rejected_obstacle,
      rejected_braking, found_candidate ? "igen" : "nem");
    if (!found_candidate) {
      const double recovery_speed = std::min(max_linear_velocity_, 0.08);
      const double recovery_step = recovery_speed * dt_;
      const double recovery_x = pose_.x + recovery_step * std::cos(pose_.yaw);
      const double recovery_y = pose_.y + recovery_step * std::sin(pose_.yaw);
      const double boundary_margin = robot_radius_ + safety_margin_;
      bool recovery_safe =
        recovery_x >= map_origin_x_ + boundary_margin &&
        recovery_x <= map_origin_x_ + map_size_ - boundary_margin &&
        recovery_y >= map_origin_y_ + boundary_margin &&
        recovery_y <= map_origin_y_ + map_height_ - boundary_margin;
      for (const auto & obstacle : sensed) {
        if (distance(pose_.x, pose_.y, obstacle.x, obstacle.y) < robot_radius_) continue;
        if (distance(recovery_x, recovery_y, obstacle.x, obstacle.y) <=
            robot_radius_ + obstacle.radius + safety_margin_) {
          recovery_safe = false;
          break;
        }
      }
      if (recovery_safe) {
        const double recovery_wheel = std::min(
          wheel_max_, recovery_speed / wheel_radius_);
        wheel_left_ = recovery_wheel;
        wheel_right_ = recovery_wheel;
        RCLCPP_WARN_THROTTLE(
          get_logger(), *get_clock(), 2000,
          "DWA nem talalt jeloltet; biztonsagos lassu elorehaladas indul.");
        return wheel_kinematics(wheel_left_, wheel_right_);
      }
      const double reverse_speed = std::min(max_linear_velocity_, 0.04);
      const double reverse_step = reverse_speed * dt_;
      const double reverse_x = pose_.x - reverse_step * std::cos(pose_.yaw);
      const double reverse_y = pose_.y - reverse_step * std::sin(pose_.yaw);
      bool reverse_safe =
        reverse_x >= map_origin_x_ + boundary_margin &&
        reverse_x <= map_origin_x_ + map_size_ - boundary_margin &&
        reverse_y >= map_origin_y_ + boundary_margin &&
        reverse_y <= map_origin_y_ + map_height_ - boundary_margin;
      for (const auto & obstacle : sensed) {
        if (distance(pose_.x, pose_.y, obstacle.x, obstacle.y) < robot_radius_) continue;
        if (distance(reverse_x, reverse_y, obstacle.x, obstacle.y) <=
            robot_radius_ + obstacle.radius + safety_margin_) {
          reverse_safe = false;
          break;
        }
      }
      if (reverse_safe) {
        const double reverse_wheel = std::min(
          wheel_max_, reverse_speed / wheel_radius_);
        wheel_left_ = -reverse_wheel;
        wheel_right_ = -reverse_wheel;
        RCLCPP_WARN_THROTTLE(
          get_logger(), *get_clock(), 2000,
          "DWA nem talalt eloremeno jeloltet; lassu hatramenet indul.");
        return wheel_kinematics(wheel_left_, wheel_right_);
      }
      const double target_heading = std::atan2(target_y - pose_.y, target_x - pose_.x);
      const double turn_error = angle_error(target_heading - pose_.yaw);
      wheel_left_ = 0.0;
      wheel_right_ = 0.0;
      const double turn_command = std::abs(turn_error) > 0.15
        ? std::clamp(turn_error, -max_angular_velocity_, max_angular_velocity_)
        : 0.5 * max_angular_velocity_;
      return {0.0, turn_command};
    }
    wheel_left_ = best_left;
    wheel_right_ = best_right;
    return wheel_kinematics(wheel_left_, wheel_right_);
  }
  visualization_msgs::msg::Marker make_marker(
    int id, int type, double x, double y, double z,
    double scale, float r, float g, float b) const {
    visualization_msgs::msg::Marker marker;
    marker.header.frame_id = "odom";
    marker.header.stamp = now();
    marker.ns = "astar_dwa";
    marker.id = id;
    marker.type = type;
    marker.action = visualization_msgs::msg::Marker::ADD;
    marker.pose.position.x = x;
    marker.pose.position.y = y;
    marker.pose.position.z = z;
    marker.pose.orientation.w = 1.0;
    marker.scale.x = scale;
    marker.scale.y = scale;
    marker.scale.z = scale;
    marker.color.r = r;
    marker.color.g = g;
    marker.color.b = b;
    marker.color.a = 0.9;
    marker.lifetime = rclcpp::Duration::from_seconds(0.4);
    return marker;
  }
  void publish_debug(const std::vector<std::pair<double, double>> & path,
                     double target_x, double target_y,
                     double velocity, double angular_velocity) {
    visualization_msgs::msg::MarkerArray markers;
    auto goal = make_marker(0, visualization_msgs::msg::Marker::SPHERE,
                            target_x, target_y, 0.35, 0.45, 0.1, 1.0, 0.2);
    markers.markers.push_back(goal);
    auto goal_ring = make_marker(3, visualization_msgs::msg::Marker::CYLINDER,
                                 target_x, target_y, 0.03, 1.0, 0.1, 1.0, 0.2);
    goal_ring.scale.z = 0.04;
    goal_ring.color.a = 0.75;
    markers.markers.push_back(goal_ring);
    auto goal_text = make_marker(4, visualization_msgs::msg::Marker::TEXT_VIEW_FACING,
                                 target_x, target_y, 0.85, 0.1, 0.1, 1.0, 0.2);
    goal_text.text = "CEL";
    goal_text.scale.z = 0.28;
    goal_text.color.a = 1.0;
    markers.markers.push_back(goal_text);
    auto path_marker = make_marker(1, visualization_msgs::msg::Marker::LINE_STRIP,
                                   0.0, 0.0, 0.18, 0.1, 0.1, 1.0, 0.2);
    path_marker.points.clear();
    for (const auto & point : path) {
      geometry_msgs::msg::Point p;
      p.x = point.first; p.y = point.second; p.z = 0.08;
      path_marker.points.push_back(p);
    }
    markers.markers.push_back(path_marker);
    int id = 10;
    for (const auto & obstacle : planning_obstacles()) {
      auto marker = make_marker(id++, visualization_msgs::msg::Marker::CYLINDER,
                                obstacle.x, obstacle.y, 0.45,
                                obstacle.radius * 2.0, 0.9, 0.15, 0.1);
      marker.scale.z = 0.9;
      markers.markers.push_back(marker);
      auto safety = make_marker(id++, visualization_msgs::msg::Marker::CYLINDER,
                                obstacle.x, obstacle.y, 0.02,
                                2.0 * (obstacle.radius + robot_radius_ + safety_margin_),
                                1.0, 0.35, 0.05);
      safety.scale.z = 0.02;
      safety.color.a = 0.25;
      markers.markers.push_back(safety);
    }
    int sensed_id = 100;
    for (const auto & obstacle : obstacles()) {
      auto marker = make_marker(sensed_id++,
                                visualization_msgs::msg::Marker::SPHERE,
                                obstacle.x, obstacle.y, 0.16, 0.10,
                                1.0, 0.75, 0.05);
      marker.color.a = 0.85;
      markers.markers.push_back(marker);
    }
    auto trajectory = make_marker(2, visualization_msgs::msg::Marker::LINE_STRIP,
                                  0.0, 0.0, 0.22, 0.09, 0.2, 0.6, 1.0);
    trajectory.points.clear();
    double x = pose_.x, y = pose_.y, yaw = pose_.yaw;
    for (int step = 0; step < 15; ++step) {
      x += velocity * std::cos(yaw) * 0.1;
      y += velocity * std::sin(yaw) * 0.1;
      yaw += angular_velocity * 0.1;
      geometry_msgs::msg::Point p;
      p.x = x; p.y = y; p.z = 0.12;
      trajectory.points.push_back(p);
    }
    markers.markers.push_back(trajectory);
    auto robot = make_marker(5, visualization_msgs::msg::Marker::CYLINDER,
                             pose_.x, pose_.y, 0.04, 0.58, 0.2, 0.7, 1.0);
    robot.scale.z = 0.05;
    robot.color.a = 0.35;
    markers.markers.push_back(robot);
    auto heading = make_marker(6, visualization_msgs::msg::Marker::ARROW,
                               pose_.x, pose_.y, 0.28, 0.08, 0.2, 0.7, 1.0);
    heading.points.clear();
    geometry_msgs::msg::Point start, end;
    start.x = pose_.x; start.y = pose_.y; start.z = 0.28;
    end.x = pose_.x + 0.55 * std::cos(pose_.yaw);
    end.y = pose_.y + 0.55 * std::sin(pose_.yaw); end.z = 0.28;
    heading.points = {start, end};
    heading.scale.x = 0.08; heading.scale.y = 0.14; heading.scale.z = 0.14;
    markers.markers.push_back(heading);
    marker_pub_->publish(markers);
  }
  void control() {
    if (!have_odom_) return;
    publish_map();
    if (!have_scan_) {
      publish_debug({}, pose_.x, pose_.y, 0.0, 0.0);
      return;
    }
    if (!has_goal_) {
      cmd_pub_->publish(geometry_msgs::msg::Twist{});
      publish_debug({}, pose_.x, pose_.y, 0.0, 0.0);
      return;
    }
    const auto sensed_obstacles = obstacles();
    static std::vector<std::pair<double, double>> cached_path;
    static std::size_t waypoint_index = 0;
    static double last_astar_goal_x = std::numeric_limits<double>::quiet_NaN();
    static double last_astar_goal_y = std::numeric_limits<double>::quiet_NaN();
    const bool goal_changed =
      !std::isfinite(last_astar_goal_x) ||
      distance(last_astar_goal_x, last_astar_goal_y, goal_x_, goal_y_) > 1e-6;
    if (cached_path.empty() || goal_changed) {
      cached_path = astar(sensed_obstacles);
      waypoint_index = 0;
      last_astar_goal_x = goal_x_;
      last_astar_goal_y = goal_y_;
    }
    const auto & path = cached_path;
    nav_msgs::msg::Path path_msg; path_msg.header.frame_id = "odom";
    path_msg.header.stamp = now();
    for (const auto & point : path) {
      geometry_msgs::msg::PoseStamped pose;
      pose.header = path_msg.header; pose.pose.position.x = point.first;
      pose.pose.position.y = point.second; pose.pose.orientation.w = 1.0;
      path_msg.poses.push_back(pose);
    }
    path_pub_->publish(path_msg);
    geometry_msgs::msg::Twist command;
    if (path.empty()) {
      last_linear_velocity_ = 0.0;
      last_angular_velocity_ = 0.0;
      cmd_pub_->publish(command);
      RCLCPP_WARN_THROTTLE(
        get_logger(), *get_clock(), 5000,
        "Az A* nem talalt elerheto utvonalat; a robot megall.");
      publish_debug({}, goal_x_, goal_y_, 0.0, 0.0);
      return;
    }
    while (waypoint_index + 1 < path.size()) {
      const auto & current_waypoint = path[waypoint_index];
      const auto & next_waypoint = path[waypoint_index + 1];
      const double to_current_x = current_waypoint.first - pose_.x;
      const double to_current_y = current_waypoint.second - pose_.y;
      const double direction_x = next_waypoint.first - current_waypoint.first;
      const double direction_y = next_waypoint.second - current_waypoint.second;
      const bool passed_waypoint =
        to_current_x * direction_x + to_current_y * direction_y < 0.0;
      if (distance(pose_.x, pose_.y, current_waypoint.first, current_waypoint.second) <= 0.20 ||
          passed_waypoint) {
        ++waypoint_index;
      } else {
        break;
      }
    }
    if (distance(pose_.x, pose_.y, goal_x_, goal_y_) < 0.3) {
      last_linear_velocity_ = 0.0;
      last_angular_velocity_ = 0.0;
      cmd_pub_->publish(command);
      return;
    }
    const double boundary_margin = robot_radius_ + safety_margin_;
    if (pose_.x < map_origin_x_ + boundary_margin ||
        pose_.x > map_origin_x_ + map_size_ - boundary_margin ||
        pose_.y < map_origin_y_ + boundary_margin ||
        pose_.y > map_origin_y_ + map_height_ - boundary_margin) {
      last_linear_velocity_ = 0.0;
      last_angular_velocity_ = 0.0;
      cmd_pub_->publish(command);
      RCLCPP_WARN_THROTTLE(
        get_logger(), *get_clock(), 5000,
        "A robot a palya biztonsagi hataran kivul van; sebesseg nullazva.");
      publish_debug(path, pose_.x, pose_.y, 0.0, 0.0);
      return;
    }
    std::size_t nearest_index = waypoint_index;
    double nearest_distance = distance(
      pose_.x, pose_.y, path[nearest_index].first, path[nearest_index].second);
    for (std::size_t index = waypoint_index + 1; index < path.size(); ++index) {
      const double candidate_distance = distance(
        pose_.x, pose_.y, path[index].first, path[index].second);
      if (candidate_distance < nearest_distance) {
        nearest_distance = candidate_distance;
        nearest_index = index;
      }
    }
    waypoint_index = std::max(waypoint_index, nearest_index);
    std::size_t target_index = waypoint_index;
    if (nearest_distance <= 0.60) {
      while (target_index + 1 < path.size() &&
             distance(pose_.x, pose_.y, path[target_index].first, path[target_index].second) < 0.30) {
        ++target_index;
      }
    }
    double target_x = path[target_index].first;
    double target_y = path[target_index].second;
    const double target_heading = std::atan2(target_y - pose_.y, target_x - pose_.x);
    const auto velocity = dwa(target_x, target_y, sensed_obstacles);
    RCLCPP_INFO_THROTTLE(
      get_logger(), *get_clock(), 2000,
      "Frontier vezerles: cel=(%.2f, %.2f), waypoint=(%.2f, %.2f), waypoint_tav=%.2f, ut=%zu pont, cmd=(%.2f, %.2f)",
      goal_x_, goal_y_, target_x, target_y,
      distance(pose_.x, pose_.y, target_x, target_y), path.size(),
      velocity.first, velocity.second);
    command.linear.x = std::clamp(velocity.first, -max_linear_velocity_, max_linear_velocity_);
    command.angular.z = std::clamp(velocity.second, -max_angular_velocity_, max_angular_velocity_);
    publish_debug(path, target_x, target_y, command.linear.x, command.angular.z);
    cmd_pub_->publish(command);
  }

  std::string cmd_topic_, odom_topic_, scan_topic_, goal_topic_, path_topic_;
  double goal_x_, goal_y_, map_size_, map_height_, map_origin_x_, map_origin_y_;
  double initial_pose_x_, initial_pose_y_;
  double resolution_, robot_radius_;
  double max_linear_velocity_, max_angular_velocity_;
  std::vector<double> known_obstacle_x_, known_obstacle_y_, known_obstacle_radius_;
  Pose pose_; sensor_msgs::msg::LaserScan::ConstSharedPtr scan_;
  bool have_odom_{false}, have_scan_{false}, has_goal_{false};
  double wheel_radius_{0.033}, wheel_base_{0.08}, wheel_max_{15.0};
  double wheel_resolution_{1.0}, acceleration_limit_{2.0};
  double predict_time_{3.0}, safety_margin_{0.15};
  double alpha_{5.0}, beta_{2.0}, gamma_{3.0}, dt_{0.1};
  double wheel_left_{0.0}, wheel_right_{0.0};
  double last_linear_velocity_{0.0}, last_angular_velocity_{0.0};
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr cmd_pub_;
  rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr path_pub_;
  rclcpp::Publisher<nav_msgs::msg::OccupancyGrid>::SharedPtr map_pub_;
  rclcpp::Publisher<visualization_msgs::msg::MarkerArray>::SharedPtr marker_pub_;
  std::unique_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster_;
  rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr odom_sub_;
  rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr scan_sub_;
  rclcpp::Subscription<geometry_msgs::msg::PoseStamped>::SharedPtr goal_sub_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char ** argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<AStarDwaNode>());
  rclcpp::shutdown();
  return 0;
}
