#include <algorithm>
#include <atomic>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <sstream>
#include <thread>
#include <functional>
#include <limits>
#include <memory>
#include <queue>
#include <string>
#include <utility>
#include <vector>

#include "geometry_msgs/msg/pose_stamped.hpp"
#include "geometry_msgs/msg/transform_stamped.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include "nav_msgs/msg/occupancy_grid.hpp"
#include "nav_msgs/msg/path.hpp"
#include "rclcpp/rclcpp.hpp"
#include "rclcpp/create_timer.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"
#include "tf2_ros/transform_broadcaster.h"
#include "visualization_msgs/msg/marker_array.hpp"
#include "path_tracking.hpp"

namespace {
struct Obstacle { double x, y, radius, vx{0.0}, vy{0.0}; };
struct Track { double x, y, vx, vy; };
struct Pose { double x{0.0}, y{0.0}, yaw{0.0}; };
double angle_error(double value) { return std::atan2(std::sin(value), std::cos(value)); }
double distance(double ax, double ay, double bx, double by) {
  return std::hypot(ax - bx, ay - by);
}
}  // namespace

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
    map_size_ = declare_parameter("map_size", 8.2);
    map_height_ = declare_parameter("map_height", 5.2);
    map_origin_x_ = declare_parameter("map_origin_x", 0.0);
    map_origin_y_ = declare_parameter("map_origin_y", 0.0);
    initial_pose_x_ = declare_parameter("initial_pose_x", 0.8);
    initial_pose_y_ = declare_parameter("initial_pose_y", 0.8);
    resolution_ = declare_parameter("resolution", 0.20);
    robot_radius_ = declare_parameter("robot_radius", 0.22);
    max_linear_velocity_ = declare_parameter("max_linear_velocity", 0.26);
    max_angular_velocity_ = declare_parameter("max_angular_velocity", 1.0);
    wheel_radius_ = declare_parameter("wheel_radius", 0.033);
    wheel_base_ = declare_parameter("wheel_base", 0.08);
    wheel_max_ = declare_parameter("wheel_max", 15.0);
    wheel_resolution_ = declare_parameter("wheel_resolution", 0.5);
    acceleration_limit_ = declare_parameter("acceleration_limit", 2.0);
    predict_time_ = declare_parameter("predict_time", 2.5);
    safety_margin_ = declare_parameter("safety_margin", 0.08);
    min_ttc_ = declare_parameter("min_ttc", 1.0);
    static_safety_margin_ = declare_parameter("static_safety_margin", 0.03);
    lookahead_distance_ = declare_parameter("lookahead_distance", 0.25);
    planning_margin_ = declare_parameter("planning_margin", 0.30);
    gazebo_path_debug_ = declare_parameter("gazebo_path_debug", true);
    gazebo_world_ = declare_parameter("gazebo_world", std::string("dwa_world"));
    alpha_ = declare_parameter("alpha", 5.0);
    beta_ = declare_parameter("beta", 2.0);
    gamma_ = declare_parameter("gamma", 3.0);
    path_distance_bias_ = declare_parameter("path_distance_bias", 6.0);
    goal_distance_bias_ = declare_parameter("goal_distance_bias", 2.0);
    known_obstacle_x_ = declare_parameter("known_obstacle_x", std::vector<double>{});
    known_obstacle_y_ = declare_parameter("known_obstacle_y", std::vector<double>{});
    known_obstacle_radius_ = declare_parameter("known_obstacle_radius", std::vector<double>{});
    const double period = declare_parameter("control_period", 0.10);
    dt_ = period;
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
        blocked_cycles_ = 0;
        need_replan_ = true;
        RCLCPP_INFO(get_logger(), "Uj cel: x=%.2f m, y=%.2f m", goal_x_, goal_y_); });
    timer_ = rclcpp::create_timer(
      this, get_clock(), rclcpp::Duration::from_seconds(period), [this]() { control(); });
    RCLCPP_INFO(get_logger(), "Robotfuggetlen A* + DWA C++ node elindult (Stabilizalt verzio)");
  }

  ~AStarDwaNode() override {
    if (debug_thread_.joinable()) debug_thread_.join();
  }

private:
  std::string build_path_sdf(const std::vector<std::pair<double, double>> & path) const {
    std::ostringstream s;
    s.precision(4);
    s << std::fixed;
    s << "<?xml version=\"1.0\"?>\n<sdf version=\"1.8\">\n<model name=\"debug_path\">\n"
         "<static>true</static>\n<link name=\"link\">\n";
    for (std::size_t i = 0; i < path.size(); ++i) {
      s << "<visual name=\"wp_" << i << "\"><pose>" << path[i].first << " " << path[i].second
        << " 0.04 0 0 0</pose><cast_shadows>false</cast_shadows><geometry><sphere><radius>0.035"
           "</radius></sphere></geometry><material><ambient>0.1 0.9 0.2 1</ambient>"
           "<diffuse>0.1 0.9 0.2 1</diffuse></material></visual>\n";
      if (i + 1 < path.size()) {
        const double dx = path[i + 1].first - path[i].first;
        const double dy = path[i + 1].second - path[i].second;
        const double len = std::hypot(dx, dy);
        if (len < 1e-3) continue;
        s << "<visual name=\"seg_" << i << "\"><pose>" << (path[i].first + dx / 2.0) << " "
          << (path[i].second + dy / 2.0) << " 0.03 0 0 " << std::atan2(dy, dx)
          << "</pose><cast_shadows>false</cast_shadows><geometry><box><size>" << len
          << " 0.035 0.01</size></box></geometry><material><ambient>0.1 0.4 1 1</ambient>"
             "<diffuse>0.1 0.4 1 1</diffuse></material></visual>\n";
      }
    }
    s << "</link>\n</model>\n</sdf>\n";
    return s.str();
  }

  void update_gazebo_path(const std::vector<std::pair<double, double>> & path) {
    if (!gazebo_path_debug_ || path.size() < 2 || debug_busy_) return;
    const double now_s = now().seconds();
    if (now_s - last_debug_time_ < 1.5) return;
    bool changed = last_debug_path_.size() < 2 ||
      std::abs(static_cast<int>(path.size()) - static_cast<int>(last_debug_path_.size())) > 2;
    if (!changed) {
      const auto & a = path.back();
      const auto & b = last_debug_path_.back();
      changed = distance(a.first, a.second, b.first, b.second) > 0.1;
    }
    if (!changed) return;
    last_debug_time_ = now_s;
    last_debug_path_ = path;
    const std::string sdf = build_path_sdf(path);
    const std::string world = gazebo_world_;
    if (debug_thread_.joinable()) debug_thread_.join();
    debug_busy_ = true;
    debug_thread_ = std::thread([this, sdf, world]() {
      const std::string file = "/tmp/astar_debug_path.sdf";
      {
        std::ofstream out(file);
        out << sdf;
      }
      const std::string cmd =
        "gz service -s /world/" + world + "/remove --reqtype gz.msgs.Entity "
        "--reptype gz.msgs.Boolean --timeout 1000 --req 'name: \"debug_path\" type: MODEL' "
        ">/dev/null 2>&1; "
        "gz service -s /world/" + world + "/create --reqtype gz.msgs.EntityFactory "
        "--reptype gz.msgs.Boolean --timeout 3000 --req 'sdf_filename: \"" + file + "\"' "
        ">/dev/null 2>&1";
      const int rc = std::system(cmd.c_str());
      (void)rc;
      debug_busy_ = false;
    });
  }

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

  std::vector<Obstacle> planning_obstacles() const {
    std::vector<Obstacle> result;
    const std::size_t count = std::min(
      {known_obstacle_x_.size(), known_obstacle_y_.size(), known_obstacle_radius_.size()});
    for (std::size_t i = 0; i < count; ++i)
      result.push_back({known_obstacle_x_[i], known_obstacle_y_[i], known_obstacle_radius_[i]});
    return result;
  }

  bool line_free(double ax, double ay, double bx, double by,
                 const std::vector<Obstacle> & statics) const {
    const double len = distance(ax, ay, bx, by);
    const int n = std::max(1, static_cast<int>(std::ceil(len / 0.05)));
    for (int k = 0; k <= n; ++k) {
      const double t = static_cast<double>(k) / n;
      const double x = ax + (bx - ax) * t, y = ay + (by - ay) * t;
      for (const auto & o : statics)
        if (distance(x, y, o.x, o.y) < o.radius + robot_radius_ - 0.02) return false;
    }
    return true;
  }

  std::vector<Obstacle> obstacles() {
    std::vector<Obstacle> pts;
    std::vector<std::size_t> scan_index;
    if (!scan_) return pts;
    constexpr double max_dist = 3.0;
    constexpr double half_fov = 1.57079632679;
    for (std::size_t i = 0; i < scan_->ranges.size(); ++i) {
      const double r = scan_->ranges[i];
      if (!std::isfinite(r) || r < scan_->range_min || r > scan_->range_max) continue;
      const double rel = scan_->angle_min + static_cast<double>(i) * scan_->angle_increment;
      if (r > max_dist || std::abs(angle_error(rel)) > half_fov) continue;
      const double a = pose_.yaw + rel;
      pts.push_back({pose_.x + r * std::cos(a), pose_.y + r * std::sin(a), 0.0});
      scan_index.push_back(i);
    }

    std::vector<std::vector<std::size_t>> clusters;
    for (std::size_t k = 0; k < pts.size(); ++k) {
      bool join = false;
      if (!clusters.empty()) {
        const std::size_t last = clusters.back().back();
        join = (scan_index[k] - scan_index[last] <= 2) &&
               distance(pts[k].x, pts[k].y, pts[last].x, pts[last].y) < 0.15;
      }
      if (join) clusters.back().push_back(k); else clusters.push_back({k});
    }

    const auto statics = planning_obstacles();
    const double now_s = now().seconds();
    const double dt = now_s - last_track_time_;
    std::vector<Track> new_tracks;
    for (const auto & cl : clusters) {
      double cx = 0.0, cy = 0.0;
      for (auto k : cl) { cx += pts[k].x; cy += pts[k].y; }
      cx /= static_cast<double>(cl.size());
      cy /= static_cast<double>(cl.size());
      const double extent = distance(pts[cl.front()].x, pts[cl.front()].y,
                                     pts[cl.back()].x, pts[cl.back()].y);
      bool near_static = false;
      for (const auto & s : statics)
        if (distance(cx, cy, s.x, s.y) < s.radius + 0.25) { near_static = true; break; }
      double vx = 0.0, vy = 0.0;
      if (!near_static && extent < 0.6 && dt > 0.02 && dt < 0.5) {
        const Track * best = nullptr;
        double best_d = 0.35;
        for (const auto & t : tracks_) {
          const double d = distance(cx, cy, t.x, t.y);
          if (d < best_d) { best_d = d; best = &t; }
        }
        if (best) {
          vx = 0.6 * best->vx + 0.4 * (cx - best->x) / dt;
          vy = 0.6 * best->vy + 0.4 * (cy - best->y) / dt;
          const double sp = std::hypot(vx, vy);
          if (sp < 0.06) { vx = 0.0; vy = 0.0; }
          else if (sp > 0.6) { vx *= 0.6 / sp; vy *= 0.6 / sp; }
        }
      }
      new_tracks.push_back({cx, cy, vx, vy});
      for (auto k : cl) { pts[k].vx = vx; pts[k].vy = vy; }
    }
    tracks_ = new_tracks;
    last_track_time_ = now_s;
    return pts;
  }

  // ---------------------------------------------------------------------- A*
  std::vector<std::pair<double, double>> astar(
    const std::vector<Obstacle> & sensed_obstacles, bool use_sensed) const {
    const int width = map_width();
    const int height = map_height();
    const double ox = map_origin_x_, oy = map_origin_y_;
    std::vector<bool> blocked(static_cast<std::size_t>(width) * height, false);
    auto inside = [width, height](int r, int c) { return r >= 0 && c >= 0 && r < height && c < width; };
    auto index = [width](int r, int c) { return r * width + c; };
    auto cell = [resolution = resolution_, ox, oy](double x, double y) {
      return std::pair<int, int>{static_cast<int>(std::floor((y - oy) / resolution)),
                                 static_cast<int>(std::floor((x - ox) / resolution))};
    };
    auto world = [resolution = resolution_, ox, oy](int r, int c) {
      return std::pair<double, double>{ox + (c + 0.5) * resolution, oy + (r + 0.5) * resolution};
    };

    auto inflate = [&](const Obstacle & obstacle) {
      const auto center = cell(obstacle.x, obstacle.y);
      const double inflation = robot_radius_ + obstacle.radius + planning_margin_;
      const int radius = static_cast<int>(std::ceil(inflation / resolution_));
      for (int r = center.first - radius; r <= center.first + radius; ++r)
        for (int c = center.second - radius; c <= center.second + radius; ++c)
          if (inside(r, c)) {
            const auto p = world(r, c);
            if (distance(p.first, p.second, obstacle.x, obstacle.y) <= inflation)
              blocked[index(r, c)] = true;
          }
    };

    const auto statics = planning_obstacles();
    for (const auto & obstacle : statics) inflate(obstacle);
    if (use_sensed) {
      for (const auto & o : sensed_obstacles) {
        if (distance(pose_.x, pose_.y, o.x, o.y) < 0.35) continue;
        bool known = false;
        for (const auto & s : statics)
          if (distance(o.x, o.y, s.x, s.y) < s.radius + 0.25) { known = true; break; }
        if (known) continue;
        inflate({o.x, o.y, 0.05});
      }
    }

    const double boundary_margin = robot_radius_ + safety_margin_;
    for (int r = 0; r < height; ++r)
      for (int c = 0; c < width; ++c) {
        const auto p = world(r, c);
        if (p.first < ox + boundary_margin || p.first > ox + map_size_ - boundary_margin ||
            p.second < oy + boundary_margin || p.second > oy + map_height_ - boundary_margin)
          blocked[index(r, c)] = true;
      }

    const auto start = cell(pose_.x, pose_.y);
    const auto target = cell(goal_x_, goal_y_);
    if (!inside(start.first, start.second) || !inside(target.first, target.second) ||
        blocked[index(target.first, target.second)]) {
      RCLCPP_WARN_THROTTLE(
        get_logger(), *get_clock(), 5000,
        "A* ervenytelen kezdo/celcella: start=(%d,%d), cel=(%d,%d)",
        start.first, start.second, target.first, target.second);
      return {};
    }
    blocked[index(start.first, start.second)] = false;
    for (int dr = -1; dr <= 1; ++dr)
      for (int dc = -1; dc <= 1; ++dc) {
        const int rr = start.first + dr, cc = start.second + dc;
        if (!inside(rr, cc)) continue;
        const auto p = world(rr, cc);
        bool hard = false;
        for (const auto & o : statics)
          if (distance(p.first, p.second, o.x, o.y) < o.radius + 0.12) { hard = true; break; }
        if (!hard) blocked[index(rr, cc)] = false;
      }

    struct Entry {
      double f, g; int r, c;
      bool operator>(const Entry & other) const { return f > other.f; }
    };
    std::priority_queue<Entry, std::vector<Entry>, std::greater<Entry>> open;
    const std::size_t total = static_cast<std::size_t>(width) * height;
    std::vector<double> cost(total, std::numeric_limits<double>::infinity());
    std::vector<int> parent(total, -1);
    auto heuristic = [&target](int r, int c) { return std::hypot(target.first - r, target.second - c); };
    open.push({heuristic(start.first, start.second), 0.0, start.first, start.second});
    cost[index(start.first, start.second)] = 0.0;
    const int directions[8][2] = {{1,0},{-1,0},{0,1},{0,-1},{1,1},{1,-1},{-1,1},{-1,-1}};
    while (!open.empty()) {
      const auto current = open.top(); open.pop();
      if (current.g > cost[index(current.r, current.c)]) continue;
      if (current.r == target.first && current.c == target.second) break;
      for (const auto & d : directions) {
        const int nr = current.r + d[0], nc = current.c + d[1];
        if (!inside(nr, nc) || blocked[index(nr, nc)]) continue;
        if (d[0] && d[1] && (blocked[index(current.r, nc)] || blocked[index(nr, current.c)])) continue;
        const double ng = current.g + ((d[0] && d[1]) ? std::sqrt(2.0) : 1.0);
        if (ng < cost[index(nr, nc)]) {
          cost[index(nr, nc)] = ng;
          parent[index(nr, nc)] = index(current.r, current.c);
          open.push({ng + heuristic(nr, nc), ng, nr, nc});
        }
      }
    }
    std::vector<std::pair<double, double>> path;
    int current = index(target.first, target.second);
    const int start_index = index(start.first, start.second);
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
    map.info.resolution = static_cast<float>(resolution_);
    map.info.width = static_cast<std::uint32_t>(map_width());
    map.info.height = static_cast<std::uint32_t>(map_height());
    map.info.origin.position.x = map_origin_x_;
    map.info.origin.position.y = map_origin_y_;
    map.info.origin.orientation.w = 1.0;
    map.data.assign(map.info.width * map.info.height, 0);
    const int width = static_cast<int>(map.info.width);
    const int height = static_cast<int>(map.info.height);
    for (const auto & obstacle : planning_obstacles()) {
      const double inflation = obstacle.radius + robot_radius_ + planning_margin_;
      const int radius = static_cast<int>(std::ceil(inflation / resolution_));
      const int cc = static_cast<int>(std::floor((obstacle.x - map_origin_x_) / resolution_));
      const int cr = static_cast<int>(std::floor((obstacle.y - map_origin_y_) / resolution_));
      for (int r = cr - radius; r <= cr + radius; ++r)
        for (int c = cc - radius; c <= cc + radius; ++c)
          if (r >= 0 && c >= 0 && r < height && c < width) {
            const double px = map_origin_x_ + (c + 0.5) * resolution_;
            const double py = map_origin_y_ + (r + 0.5) * resolution_;
            if (distance(px, py, obstacle.x, obstacle.y) <= inflation)
              map.data[static_cast<std::size_t>(r) * width + c] = 100;
          }
    }
    map_pub_->publish(map);
  }

  // --------------------------------------------------------------------- DWA
  std::pair<double, double> wheel_kinematics(double left, double right) const {
    const double velocity = ((left + right) / 2.0) * wheel_radius_;
    const double angular = ((right - left) / (2.0 * wheel_base_)) * wheel_radius_;
    return {velocity, angular};
  }

  std::pair<double, double> dwa(double target_x, double target_y,
                                std::size_t target_index,
                                const std::vector<Obstacle> & sensed) {
    const double wa = acceleration_limit_ / wheel_radius_;
    const double left_min = std::max(-wheel_max_, wheel_left_ - wa * dt_);
    const double left_max = std::min(wheel_max_, wheel_left_ + wa * dt_);
    const double right_min = std::max(-wheel_max_, wheel_right_ - wa * dt_);
    const double right_max = std::min(wheel_max_, wheel_right_ + wa * dt_);
    const double clearance_limit = robot_radius_ + safety_margin_;
    const double goal_dist = distance(pose_.x, pose_.y, target_x, target_y);
    const double horizon = std::clamp(goal_dist * 2.0, 0.8, predict_time_);

    std::vector<double> init_clear(sensed.size(), 0.0);
    for (std::size_t j = 0; j < sensed.size(); ++j) {
      const bool mv = std::hypot(sensed[j].vx, sensed[j].vy) > 0.0;
      init_clear[j] = distance(pose_.x, pose_.y, sensed[j].x, sensed[j].y) -
                      (robot_radius_ + (mv ? safety_margin_ : static_safety_margin_) + sensed[j].radius);
    }
    double best_score = -std::numeric_limits<double>::infinity();
    double best_left = 0.0, best_right = 0.0;
    bool found = false;
    std::size_t n_test = 0, n_vel = 0, n_ttc = 0, n_brake = 0;

    for (double left = left_min; left <= left_max + 1e-9; left += wheel_resolution_) {
      for (double right = right_min; right <= right_max + 1e-9; right += wheel_resolution_) {
        ++n_test;
        const auto cand = wheel_kinematics(left, right);
        if (cand.first < 0.0 || cand.first > max_linear_velocity_ ||
            std::abs(cand.second) > max_angular_velocity_) {
          ++n_vel;
          continue;
        }

        double x = pose_.x, y = pose_.y, yaw = pose_.yaw;
        double sl = wheel_left_, sr = wheel_right_;
        double arc = 0.0, collision_dist = 10.0, min_clear = 3.0;
        bool hit = false;
        int steps = 0;
        for (double t = 0.0; t < horizon; t += dt_, ++steps) {
          sl += std::clamp(left - sl, -wa * dt_, wa * dt_);
          sr += std::clamp(right - sr, -wa * dt_, wa * dt_);
          const auto s = wheel_kinematics(sl, sr);
          if (std::abs(s.second) > 1e-6) {
            x += (s.first / s.second) * (std::sin(yaw + s.second * dt_) - std::sin(yaw));
            y -= (s.first / s.second) * (std::cos(yaw + s.second * dt_) - std::cos(yaw));
          } else {
            x += s.first * std::cos(yaw) * dt_;
            y += s.first * std::sin(yaw) * dt_;
          }
          yaw += s.second * dt_;
          arc += std::abs(s.first) * dt_;
          const double tt = (steps + 1) * dt_;

          if (x < map_origin_x_ + clearance_limit ||
              x > map_origin_x_ + map_size_ - clearance_limit ||
              y < map_origin_y_ + clearance_limit ||
              y > map_origin_y_ + map_height_ - clearance_limit) {
            collision_dist = arc;
            hit = true;
            break;
          }
          for (std::size_t j = 0; j < sensed.size(); ++j) {
            const auto & o = sensed[j];
            const double ox = o.x + o.vx * tt;
            const double oy = o.y + o.vy * tt;
            const bool moving = std::hypot(o.vx, o.vy) > 0.0;
            const double margin = moving ? safety_margin_ : static_safety_margin_;
            const double clear = distance(x, y, ox, oy) - (robot_radius_ + margin + o.radius);
            min_clear = std::min(min_clear, clear);
            if (clear <= 0.0 && clear < init_clear[j] - 0.005) {
              collision_dist = arc;
              hit = true;
              break;
            }
          }
          if (hit) break;
        }

        if (cand.first > std::sqrt(2.0 * acceleration_limit_ * collision_dist) + 1e-9) {
          ++n_brake;
          continue;
        }
        if (hit && cand.first > 1e-3 && collision_dist < cand.first * min_ttc_) {
          ++n_ttc;
          continue;
        }

        const double goal_heading = std::atan2(target_y - y, target_x - x);
        const double heading_score = (M_PI - std::abs(angle_error(goal_heading - yaw))) / M_PI;
        const double clear_score = std::clamp(min_clear / 1.0, 0.0, 1.0);
        const double v_target = std::min(max_linear_velocity_, std::max(0.08, goal_dist * 1.4));
        const double vel_score = 1.0 - std::abs(v_target - cand.first) / max_linear_velocity_;
        // Keep the original local A* reference: a detour must not become a parallel route.
        const std::size_t first = waypoint_index_ > 0 ? waypoint_index_ - 1 : 0;
        const std::size_t last = std::min(target_index + 1, current_path_.size() - 1);
        const double tracking_cost = path_tracking::tracking_cost(
          current_path_, first, last, x, y, target_x, target_y,
          path_distance_bias_, goal_distance_bias_);
        const double score = alpha_ * heading_score + beta_ * clear_score + gamma_ * vel_score -
                             tracking_cost;
        if (score > best_score) {
          best_score = score;
          best_left = left;
          best_right = right;
          found = true;
        }
      }
    }
    RCLCPP_INFO_THROTTLE(
      get_logger(), *get_clock(), 2000,
      "DWA: teszt=%zu sebesseg=%zu fekezes=%zu ttc=%zu elfogadott=%s",
      n_test, n_vel, n_brake, n_ttc, found ? "igen" : "nem");

    if (found) {
      blocked_cycles_ = 0;
      wheel_left_ = best_left;
      wheel_right_ = best_right;
      return wheel_kinematics(wheel_left_, wheel_right_);
    }

    RCLCPP_WARN_THROTTLE(
      get_logger(), *get_clock(), 2000,
      "DWA: nincs elfogadhato jelolt (fekezes=%zu ttc=%zu), blokkolt ciklusok=%d",
      n_brake, n_ttc, blocked_cycles_ + 1);
    ++blocked_cycles_;
    wheel_left_ = 0.0;
    wheel_right_ = 0.0;
    const Obstacle * nearest = nullptr;
    double nd = 1.2;
    for (const auto & o : sensed) {
      const double d = distance(pose_.x, pose_.y, o.x, o.y);
      if (d < nd) { nd = d; nearest = &o; }
    }
    if (nearest) {
      const double side = angle_error(
        std::atan2(nearest->y - pose_.y, nearest->x - pose_.x) - pose_.yaw);
      if (std::abs(side) > 0.15) recovery_dir_ = side > 0.0 ? -1 : 1;
    }
    return {0.0, recovery_dir_ * 0.6 * max_angular_velocity_};
  }

  // ------------------------------------------------------------ vizualizacio
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
    markers.markers.push_back(make_marker(
      0, visualization_msgs::msg::Marker::SPHERE, target_x, target_y, 0.35, 0.45, 0.1, 1.0, 0.2));
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
                                2.0 * (obstacle.radius + robot_radius_ + planning_margin_),
                                1.0, 0.35, 0.05);
      safety.scale.z = 0.02;
      safety.color.a = 0.25;
      markers.markers.push_back(safety);
    }
    int sensed_id = 1000;
    for (const auto & obstacle : sensed_cache_) {
      const bool moving = std::hypot(obstacle.vx, obstacle.vy) > 0.0;
      auto marker = make_marker(sensed_id++, visualization_msgs::msg::Marker::SPHERE,
                                obstacle.x, obstacle.y, 0.16, 0.10,
                                moving ? 1.0f : 1.0f, moving ? 0.1f : 0.75f, moving ? 0.1f : 0.05f);
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
                             pose_.x, pose_.y, 0.04, 2.0 * robot_radius_, 0.2, 0.7, 1.0);
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

  // ---------------------------------------------------------------- vezerles
  void stop_robot() {
    last_linear_velocity_ = 0.0;
    last_angular_velocity_ = 0.0;
    wheel_left_ = 0.0;
    wheel_right_ = 0.0;
    cmd_pub_->publish(geometry_msgs::msg::Twist{});
  }

  void control() {
    if (!have_odom_) return;
    publish_map();
    if (!have_scan_) {
      publish_debug({}, pose_.x, pose_.y, 0.0, 0.0);
      return;
    }
    sensed_cache_ = obstacles();
    const auto & sensed_obstacles = sensed_cache_;
    if (!has_goal_) {
      cmd_pub_->publish(geometry_msgs::msg::Twist{});
      publish_debug({}, pose_.x, pose_.y, 0.0, 0.0);
      return;
    }

    if (current_path_.empty() || need_replan_ ||
        (waypoint_index_ < current_path_.size() &&
         distance(pose_.x, pose_.y, current_path_[waypoint_index_].first,
                  current_path_[waypoint_index_].second) > 1.2)) {
      auto new_path = astar({}, false);
      if (!new_path.empty() || current_path_.empty()) {
        current_path_ = std::move(new_path);
        waypoint_index_ = 0;
      }
      need_replan_ = false;
      last_replan_time_ = now().seconds();
      RCLCPP_INFO(get_logger(), "A* (statikus terkep) utvonal: %zu pont", current_path_.size());
    }
    const auto path = current_path_;

    nav_msgs::msg::Path path_msg;
    path_msg.header.frame_id = "odom";
    path_msg.header.stamp = now();
    for (const auto & point : path) {
      geometry_msgs::msg::PoseStamped pose;
      pose.header = path_msg.header;
      pose.pose.position.x = point.first;
      pose.pose.position.y = point.second;
      pose.pose.orientation.w = 1.0;
      path_msg.poses.push_back(pose);
    }
    path_pub_->publish(path_msg);
    update_gazebo_path(path);

    geometry_msgs::msg::Twist command;
    if (path.empty()) {
      stop_robot();
      RCLCPP_WARN_THROTTLE(get_logger(), *get_clock(), 5000,
                           "Az A* nem talalt elerheto utvonalat; a robot megall.");
      publish_debug({}, goal_x_, goal_y_, 0.0, 0.0);
      return;
    }
    if (distance(pose_.x, pose_.y, goal_x_, goal_y_) < 0.3) {
      stop_robot();
      return;
    }
    const double boundary_margin = robot_radius_ + safety_margin_;
    if (pose_.x < map_origin_x_ + boundary_margin ||
        pose_.x > map_origin_x_ + map_size_ - boundary_margin ||
        pose_.y < map_origin_y_ + boundary_margin ||
        pose_.y > map_origin_y_ + map_height_ - boundary_margin) {
      stop_robot();
      RCLCPP_WARN_THROTTLE(get_logger(), *get_clock(), 5000,
                           "A robot a palya biztonsagi hataran kivul van; sebesseg nullazva.");
      publish_debug(path, pose_.x, pose_.y, 0.0, 0.0);
      return;
    }

    const auto statics = planning_obstacles();
    {
      const std::size_t window_end = std::min(path.size(), waypoint_index_ + 8);
      double best_d = std::numeric_limits<double>::infinity();
      std::size_t closest = waypoint_index_;
      bool found_visible = false;
      for (std::size_t i = waypoint_index_; i < window_end; ++i) {
        if (!line_free(pose_.x, pose_.y, path[i].first, path[i].second, statics)) continue;
        const double d = distance(pose_.x, pose_.y, path[i].first, path[i].second);
        if (d < best_d) { best_d = d; closest = i; found_visible = true; }
      }
      if (found_visible) {
        waypoint_index_ = std::max(waypoint_index_, closest);
      } else if (now().seconds() - last_replan_time_ > 1.0) {
        need_replan_ = true;
      }
    }
    std::size_t target_index = path.size() - 1;
    {
      double accumulated = 0.0;
      for (std::size_t i = waypoint_index_; i + 1 < path.size(); ++i) {
        accumulated += distance(path[i].first, path[i].second, path[i + 1].first, path[i + 1].second);
        if (accumulated >= lookahead_distance_) { target_index = i + 1; break; }
      }
      while (target_index > waypoint_index_ &&
             !line_free(pose_.x, pose_.y, path[target_index].first, path[target_index].second,
                        statics))
        --target_index;
    }
    double target_x = path[target_index].first, target_y = path[target_index].second;

    double nearest_obstacle = std::numeric_limits<double>::infinity();
    for (const auto & o : sensed_obstacles)
      nearest_obstacle = std::min(nearest_obstacle, distance(pose_.x, pose_.y, o.x, o.y));

    const double target_heading = std::atan2(target_y - pose_.y, target_x - pose_.x);
    const double heading_error = angle_error(target_heading - pose_.yaw);
    if (std::abs(heading_error) > 0.95 && nearest_obstacle > 0.85) {
      wheel_left_ = 0.0;
      wheel_right_ = 0.0;
      command.angular.z = std::clamp(heading_error, -max_angular_velocity_, max_angular_velocity_);
      publish_debug(path, target_x, target_y, 0.0, command.angular.z);
      cmd_pub_->publish(command);
      return;
    }

    const auto velocity = dwa(target_x, target_y, target_index, sensed_obstacles);
    const double path_error = path_tracking::distance_to_path(
      path, waypoint_index_ > 0 ? waypoint_index_ - 1 : 0,
      std::min(target_index + 1, path.size() - 1), pose_.x, pose_.y);
    RCLCPP_INFO_THROTTLE(
      get_logger(), *get_clock(), 2000,
      "Vezerles: cel=(%.2f, %.2f), waypoint=(%.2f, %.2f), ut=%zu pont, akadaly_tav=%.2f, "
      "utvonal_elteres=%.3f m, cmd=(%.2f, %.2f)",
      goal_x_, goal_y_, target_x, target_y, path.size(), nearest_obstacle,
      path_error, velocity.first, velocity.second);
    command.linear.x = std::clamp(velocity.first, 0.0, max_linear_velocity_);
    command.angular.z = std::clamp(velocity.second, -max_angular_velocity_, max_angular_velocity_);
    last_linear_velocity_ = command.linear.x;
    last_angular_velocity_ = command.angular.z;
    publish_debug(path, target_x, target_y, command.linear.x, command.angular.z);
    cmd_pub_->publish(command);
  }

  // ------------------------------------------------------------------- tagok
  std::string cmd_topic_, odom_topic_, scan_topic_, goal_topic_, path_topic_;
  double goal_x_{0.0}, goal_y_{0.0}, map_size_{8.2}, map_height_{5.2};
  double map_origin_x_{0.0}, map_origin_y_{0.0};
  double initial_pose_x_{0.0}, initial_pose_y_{0.0};
  double resolution_{0.2}, robot_radius_{0.22};
  double max_linear_velocity_{0.26}, max_angular_velocity_{1.0};
  std::vector<double> known_obstacle_x_, known_obstacle_y_, known_obstacle_radius_;
  Pose pose_;
  sensor_msgs::msg::LaserScan::ConstSharedPtr scan_;
  bool have_odom_{false}, have_scan_{false}, has_goal_{false};
  double wheel_radius_{0.033}, wheel_base_{0.08}, wheel_max_{15.0};
  double wheel_resolution_{0.5}, acceleration_limit_{2.0};
  double predict_time_{2.5}, safety_margin_{0.08}, min_ttc_{1.0};
  double alpha_{5.0}, beta_{2.0}, gamma_{3.0}, dt_{0.1};
  double path_distance_bias_{6.0}, goal_distance_bias_{2.0};
  double wheel_left_{0.0}, wheel_right_{0.0};
  double last_linear_velocity_{0.0}, last_angular_velocity_{0.0};
  std::vector<Track> tracks_;
  std::vector<Obstacle> sensed_cache_;
  double last_track_time_{0.0};
  double sensed_until_{0.0};
  int recovery_dir_{1};
  int blocked_cycles_{0};
  double static_safety_margin_{0.03};
  double planning_margin_{0.30};
  double lookahead_distance_{0.25};
  double last_replan_time_{-100.0};
  std::vector<std::pair<double, double>> current_path_;
  std::size_t waypoint_index_{0};
  bool need_replan_{true};
  bool gazebo_path_debug_{true};
  std::string gazebo_world_{"dwa_world"};
  std::vector<std::pair<double, double>> last_debug_path_;
  double last_debug_time_{-100.0};
  std::atomic<bool> debug_busy_{false};
  std::thread debug_thread_;
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