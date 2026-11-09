#include <chrono>
#include <deque>
#include <memory>
#include <stdexcept>
#include <string>

#include "geometry_msgs/msg/pose_stamped.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "nav_msgs/msg/occupancy_grid.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include "nav_msgs/msg/path.hpp"
#include "rclcpp/rclcpp.hpp"
#include "rclcpp/create_timer.hpp"
#include "sensor_msgs/msg/point_cloud2.hpp"
#include "sensor_msgs/point_cloud2_iterator.hpp"
#include "std_msgs/msg/bool.hpp"
#include "tf2/exceptions.h"
#include "tf2_ros/buffer.h"
#include "tf2_ros/transform_listener.h"
#include "reference_planner.hpp"

namespace planner = reference_planner;

class ReferenceController final : public rclcpp::Node {
public:
  ReferenceController() : Node("astar_dwa_node") {
    config_.wheel_radius = declare_parameter("r_kerek", config_.wheel_radius);
    config_.half_axle = declare_parameter("b", config_.half_axle);
    config_.wheel_max = declare_parameter("w_kerek_max", config_.wheel_max);
    config_.wheel_resolution = declare_parameter("w_kerek_resolution", config_.wheel_resolution);
    config_.acceleration = declare_parameter("a_max", config_.acceleration);
    config_.dt = declare_parameter("dt", config_.dt);
    config_.predict_time = declare_parameter("predict_time", config_.predict_time);
    config_.radius = declare_parameter("rob_radius", config_.radius);
    config_.safety_margin = declare_parameter("safety_margin", config_.safety_margin);
    config_.static_margin = declare_parameter("static_safety_margin", config_.static_margin);
    config_.alpha = declare_parameter("Alfa", config_.alpha);
    config_.beta = declare_parameter("Beta", config_.beta);
    config_.gamma = declare_parameter("Gamma", config_.gamma);
    config_.dynamic_clearance_weight = declare_parameter("dynamic_clearance_weight", config_.dynamic_clearance_weight);
    config_.dynamic_clearance_distance = declare_parameter("dynamic_clearance_distance", config_.dynamic_clearance_distance);
    config_.waypoint_slowdown = declare_parameter("enable_waypoint_slowdown", false);
    inflation_ = declare_parameter("map_inflation_radius", config_.radius + config_.static_margin);
    for (double value : {config_.wheel_radius, config_.half_axle, config_.wheel_max,
                        config_.wheel_resolution, config_.acceleration, config_.dt,
                        config_.predict_time, config_.radius, config_.dynamic_clearance_distance})
      if (!std::isfinite(value) || value <= 0.0) throw std::invalid_argument("Invalid robot parameter");
    for (double value : {inflation_, config_.safety_margin, config_.static_margin,
                        config_.alpha, config_.beta, config_.gamma, config_.dynamic_clearance_weight})
      if (!std::isfinite(value) || value < 0.0) throw std::invalid_argument("Invalid margin or weight");
    buffer_ = std::make_unique<tf2_ros::Buffer>(get_clock());
    listener_ = std::make_unique<tf2_ros::TransformListener>(*buffer_);
    command_pub_ = create_publisher<geometry_msgs::msg::Twist>("/cmd_vel", 10);
    const auto latched = rclcpp::QoS(1).transient_local();
    active_pub_ = create_publisher<std_msgs::msg::Bool>("/controller_active", latched);
    path_pub_ = create_publisher<nav_msgs::msg::Path>("/astar_path", latched);
    goal_pub_ = create_publisher<geometry_msgs::msg::PoseStamped>("/accepted_goal", latched);
    map_pub_ = create_publisher<nav_msgs::msg::OccupancyGrid>("/astar_map", latched);
    map_sub_ = create_subscription<nav_msgs::msg::OccupancyGrid>("/map", latched,
      [this](nav_msgs::msg::OccupancyGrid::ConstSharedPtr message) { receive_map(message); });
    odom_sub_ = create_subscription<nav_msgs::msg::Odometry>("/odom", rclcpp::SensorDataQoS(),
      [this](nav_msgs::msg::Odometry::ConstSharedPtr message) {
        odometry_.push_back(message);
        if (odometry_.size() > 50) odometry_.pop_front();
      });
    obstacle_sub_ = create_subscription<sensor_msgs::msg::PointCloud2>("/tracked_obstacles", 10,
      [this](sensor_msgs::msg::PointCloud2::ConstSharedPtr message) {
        clouds_.push_back(message);
        if (clouds_.size() > 10) clouds_.pop_front();
      });
    goal_sub_ = create_subscription<geometry_msgs::msg::PoseStamped>("/goal_pose", 10,
      [this](geometry_msgs::msg::PoseStamped::ConstSharedPtr message) {
        pending_goal_ = message;
        active_ = false;
        waypoints_.clear();
        path_.clear();
        publish_path();
        stop("new_goal");
      });
    timer_ = rclcpp::create_timer(this, get_clock(), rclcpp::Duration::from_seconds(config_.dt),
                                 [this]() { control(); });
    RCLCPP_INFO(get_logger(),
      "DIAG_CONFIG backend=cpp-python-reference schema=cpp-dwa-8 lidar_fov=360 pruning=25 path_progress=1 dt=%.3f horizon=%.3f radius=%.3f "
      "half_axle=%.4f wheel_max=%.3f weights=(%.1f,%.1f,%.1f) dynamic_clearance_weight=%.1f dynamic_clearance_distance=%.2f wheel_resolution=%.2f",
      config_.dt, config_.predict_time, config_.radius, config_.half_axle,
      config_.wheel_max, config_.alpha, config_.beta, config_.gamma, config_.dynamic_clearance_weight,
      config_.dynamic_clearance_distance, config_.wheel_resolution);
  }

  void shutdown_command() { command_pub_->publish(geometry_msgs::msg::Twist{}); }

private:
  static double seconds(const builtin_interfaces::msg::Time & stamp) {
    return stamp.sec + stamp.nanosec * 1e-9;
  }
  static double yaw(const geometry_msgs::msg::Quaternion & rotation) {
    return std::atan2(2.0 * (rotation.w * rotation.z + rotation.x * rotation.y),
                      1.0 - 2.0 * (rotation.y * rotation.y + rotation.z * rotation.z));
  }
  bool transform(const std::string & source, const builtin_interfaces::msg::Time & stamp,
                 geometry_msgs::msg::Transform & result) {
    if (source.empty()) return false;
    if (source == frame_) {
      result = geometry_msgs::msg::Transform{};
      result.rotation.w = 1.0;
      return true;
    }
    try {
      result = buffer_->lookupTransform(frame_, source, rclcpp::Time(stamp)).transform;
      return true;
    } catch (const tf2::TransformException & error) {
      RCLCPP_WARN_THROTTLE(get_logger(), *get_clock(), 2000,
        "DIAG_TF_CPP %s -> %s: %s", source.c_str(), frame_.c_str(), error.what());
      return false;
    }
  }
  static planner::Point project(double x, double y, const geometry_msgs::msg::Transform & transform) {
    const double heading = yaw(transform.rotation);
    return {transform.translation.x + std::cos(heading) * x - std::sin(heading) * y,
            transform.translation.y + std::sin(heading) * x + std::cos(heading) * y};
  }
  void receive_map(nav_msgs::msg::OccupancyGrid::ConstSharedPtr message) {
    const auto & info = message->info;
    if (message->header.frame_id.empty() || !std::isfinite(info.resolution) || info.resolution <= 0.0 ||
        info.width == 0 || info.height == 0 || info.width > 10000 || info.height > 10000 ||
        message->data.size() != static_cast<std::size_t>(info.width) * info.height ||
        !std::isfinite(info.origin.position.x) || !std::isfinite(info.origin.position.y) ||
        std::abs(yaw(info.origin.orientation)) > 1e-6 ||
        std::abs(info.origin.orientation.x) > 1e-6 || std::abs(info.origin.orientation.y) > 1e-6) {
      RCLCPP_ERROR(get_logger(), "DIAG_MAP invalid or rotated map");
      return;
    }
    if (!frame_.empty() && frame_ != message->header.frame_id) {
      active_ = false;
      path_.clear();
      waypoints_.clear();
      have_odom_ = have_obstacles_ = false;
      odometry_.clear();
      clouds_.clear();
      stop("map_frame_changed");
    }
    frame_ = message->header.frame_id;
    grid_.width = static_cast<int>(info.width);
    grid_.height = static_cast<int>(info.height);
    grid_.resolution = info.resolution;
    grid_.origin_x = info.origin.position.x;
    grid_.origin_y = info.origin.position.y;
    grid_.blocked.resize(message->data.size());
    static_occupied_.resize(message->data.size());
    for (std::size_t index = 0; index < message->data.size(); ++index) {
      static_occupied_[index] = message->data[index] >= 65;
      grid_.blocked[index] = message->data[index] < 0 ? 2 : message->data[index] >= 65 ? 1 : 0;
    }
    const int radius = static_cast<int>(std::ceil(inflation_ / grid_.resolution));
    for (int row = 0; row < grid_.height; ++row) {
      for (int column = 0; column < grid_.width; ++column) {
        if (message->data[static_cast<std::size_t>(row) * grid_.width + column] < 65) continue;
        for (int delta_row = -radius; delta_row <= radius; ++delta_row) {
          for (int delta_column = -radius; delta_column <= radius; ++delta_column) {
            const int next_row = row + delta_row, next_column = column + delta_column;
            if (next_row < 0 || next_column < 0 || next_row >= grid_.height || next_column >= grid_.width ||
                std::hypot(delta_row, delta_column) * grid_.resolution > inflation_) continue;
            grid_.blocked[static_cast<std::size_t>(next_row) * grid_.width + next_column] = 1;
          }
        }
      }
    }
    auto inflated = *message;
    for (std::size_t index = 0; index < grid_.blocked.size(); ++index)
      inflated.data[index] = grid_.blocked[index] == 2 ? -1 : grid_.blocked[index] == 1 ? 100 : 0;
    map_pub_->publish(inflated);
    have_map_ = true;
    publish_path();
    RCLCPP_INFO(get_logger(), "DIAG_MAP cpp size=%dx%d resolution=%.3f preserved_waypoints=%zu",
      grid_.width, grid_.height, grid_.resolution, waypoints_.size());
  }
  void process_inputs() {
    if (!have_map_) return;
    for (auto iterator = odometry_.rbegin(); iterator != odometry_.rend(); ++iterator) {
      const auto & message = **iterator;
      geometry_msgs::msg::Transform conversion;
      if (!transform(message.header.frame_id, message.header.stamp, conversion)) continue;
      const auto position = project(message.pose.pose.position.x, message.pose.pose.position.y, conversion);
      if (active_ && have_odom_) {
        const double elapsed = std::max(0.0, seconds(message.header.stamp) - odom_stamp_);
        const double jump = std::hypot(position.first - state_.x, position.second - state_.y);
        const double limit = std::max(0.5, config_.wheel_max * config_.wheel_radius * elapsed + 0.2);
        if (jump > limit) {
          active_ = false;
          pending_goal_.reset();
          waypoints_.clear();
          path_.clear();
          publish_path();
          stop("localization_jump");
          RCLCPP_ERROR(get_logger(),
            "DIAG_LOCALIZATION jump=%.3f limit=%.3f previous=(%.3f,%.3f) received=(%.3f,%.3f); "
            "navigation cancelled; verify localization before sending a new goal",
            jump, limit, state_.x, state_.y, position.first, position.second);
        }
      }
      state_.x = position.first;
      state_.y = position.second;
      state_.yaw = yaw(message.pose.pose.orientation) + yaw(conversion.rotation);
      state_.velocity = message.twist.twist.linear.x;
      state_.angular = message.twist.twist.angular.z;
      state_.left = (state_.velocity - state_.angular * config_.half_axle) / config_.wheel_radius;
      state_.right = (state_.velocity + state_.angular * config_.half_axle) / config_.wheel_radius;
      odom_stamp_ = seconds(message.header.stamp);
      have_odom_ = std::isfinite(state_.x) && std::isfinite(state_.y) && std::isfinite(state_.yaw) &&
        std::isfinite(state_.left) && std::isfinite(state_.right);
      break;
    }
    while (!odometry_.empty() && seconds(odometry_.front()->header.stamp) <= odom_stamp_) odometry_.pop_front();
    for (auto iterator = clouds_.rbegin(); iterator != clouds_.rend(); ++iterator) {
      const auto & message = **iterator;
      geometry_msgs::msg::Transform conversion;
      if (!transform(message.header.frame_id, message.header.stamp, conversion)) continue;
      std::vector<planner::Obstacle> points;
      std::vector<bool> represented_static_cells(static_occupied_.size(), false);
      const double heading = yaw(conversion.rotation);
      try {
        if (!message.data.empty()) {
          sensor_msgs::PointCloud2ConstIterator<float> point_x(message, "x"), point_y(message, "y"),
            radius(message, "radius"), velocity_x(message, "vx"), velocity_y(message, "vy");
          for (; point_x != point_x.end(); ++point_x, ++point_y, ++radius, ++velocity_x, ++velocity_y) {
            if (!std::isfinite(*point_x) || !std::isfinite(*point_y) || !std::isfinite(*radius) ||
                !std::isfinite(*velocity_x) || !std::isfinite(*velocity_y) || *radius < 0.0) continue;
            const auto position = project(*point_x, *point_y, conversion);
            const auto [row, column] = grid_.cell(position);
            if (row >= 0 && column >= 0 && row < grid_.height && column < grid_.width) {
              const auto cell_index = static_cast<std::size_t>(row) * grid_.width + column;
              if (cell_index < static_occupied_.size() && static_occupied_[cell_index]) {
                if (represented_static_cells[cell_index]) continue;
                represented_static_cells[cell_index] = true;
                const auto cell_center = grid_.world(row, column);
                points.push_back({cell_center.first, cell_center.second,
                  grid_.resolution / std::sqrt(2.0), 0.0, 0.0});
                continue;
              }
            }
            points.push_back({position.first, position.second, *radius,
              std::cos(heading) * *velocity_x - std::sin(heading) * *velocity_y,
              std::sin(heading) * *velocity_x + std::cos(heading) * *velocity_y});
          }
        }
      } catch (const std::runtime_error & error) {
        RCLCPP_ERROR(get_logger(), "DIAG_CLOUD invalid fields: %s", error.what());
        have_obstacles_ = false;
        return;
      }
      obstacles_ = std::move(points);
      obstacle_stamp_ = seconds(message.header.stamp);
      have_obstacles_ = true;
      break;
    }
    while (!clouds_.empty() && seconds(clouds_.front()->header.stamp) <= obstacle_stamp_) clouds_.pop_front();
  }
  void publish_path() {
    nav_msgs::msg::Path message;
    message.header.frame_id = frame_.empty() ? "map" : frame_;
    // Zero stamp: RViz uses the latest TF, so the path is not dropped when the map->odom TF lags behind.
    message.header.stamp = rclcpp::Time(0, 0, get_clock()->get_clock_type());
    for (const auto & point : path_) {
      geometry_msgs::msg::PoseStamped pose;
      pose.header = message.header;
      pose.pose.position.x = point.first;
      pose.pose.position.y = point.second;
      pose.pose.orientation.w = 1.0;
      message.poses.push_back(pose);
    }
    path_pub_->publish(message);
  }
  void plan_goal() {
    if (!pending_goal_ || !have_map_ || !have_odom_) return;
    geometry_msgs::msg::Transform conversion;
    const auto message = pending_goal_;
    if (!transform(message->header.frame_id.empty() ? frame_ : message->header.frame_id,
                   message->header.stamp, conversion)) return;
    pending_goal_.reset();
    const auto goal = project(message->pose.position.x, message->pose.position.y, conversion);
    if (!std::isfinite(goal.first) || !std::isfinite(goal.second)) { stop("invalid_goal"); return; }
    path_ = grid_.smooth(grid_.astar({state_.x, state_.y}, goal));
    if (path_.empty()) { publish_path(); stop("no_global_path"); return; }
    path_.back() = goal;
    if (!grid_.safe(path_)) { path_.clear(); publish_path(); stop("unsafe_endpoint"); return; }
    waypoints_ = planner::resample(path_);
    waypoint_ = std::min<std::size_t>(1, waypoints_.size() - 1);
    active_ = true;
    auto accepted = *message;
    accepted.header.frame_id = frame_;
    accepted.header.stamp = now();
    accepted.pose.position.x = goal.first;
    accepted.pose.position.y = goal.second;
    goal_pub_->publish(accepted);
    publish_path();
    RCLCPP_INFO(get_logger(), "DIAG_GOAL cpp accepted=(%.3f,%.3f) waypoints=%zu", goal.first, goal.second, waypoints_.size());
  }
  void stop(const char * reason) {
    shutdown_command();
    std_msgs::msg::Bool status;
    status.data = active_;
    active_pub_->publish(status);
    RCLCPP_INFO_THROTTLE(get_logger(), *get_clock(), 2000, "DIAG_CONTROL cpp reason=%s", reason);
  }
  void control() {
    process_inputs();
    if (!have_map_ || !have_odom_ || !have_obstacles_) { stop("waiting_inputs"); return; }
    const double age = now().seconds() - std::min(odom_stamp_, obstacle_stamp_);
    if (age > std::max(0.5, 3.0 * config_.dt) || age < -0.05) { stop("stale_input"); return; }
    plan_goal();
    if (!active_ || waypoints_.empty()) { stop("inactive"); return; }
    const double goal_distance = std::hypot(waypoints_.back().first - state_.x, waypoints_.back().second - state_.y);
    const double tolerance = std::max(0.05, std::min(0.2, goal_distance * 0.2));
    if (goal_distance <= tolerance) { active_ = false; stop("finished"); return; }
    const auto previous_waypoint = waypoint_;
    const auto tracking = path_tracking::prune_lookahead(
      waypoints_, waypoint_, state_.x, state_.y, state_.velocity,
      [this](const planner::Point & point) {
        return grid_.safe(planner::Path{{state_.x, state_.y}, point});
      });
    waypoint_ = tracking.waypoint;
    auto obstacles = obstacles_;
    for (auto & obstacle : obstacles) {
      obstacle.x += obstacle.vx * (odom_stamp_ - obstacle_stamp_);
      obstacle.y += obstacle.vy * (odom_stamp_ - obstacle_stamp_);
    }
    const auto start = std::chrono::steady_clock::now();
    const auto result = planner::optimise(config_, state_, tracking.target,
                        tracking.target == waypoints_.back(), obstacles, &waypoints_, waypoint_);
    const double compute_ms = std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - start).count();
    if (now().seconds() - std::min(odom_stamp_, obstacle_stamp_) > std::max(0.5, 3.0 * config_.dt)) {
      waypoint_ = previous_waypoint;
      stop("planner_deadline");
      return;
    }
    auto predicted = state_;
    planner::update(predicted, config_, result.command);
    geometry_msgs::msg::Twist command;
    command.linear.x = predicted.velocity;
    command.angular.z = predicted.angular;
    command_pub_->publish(command);
    std_msgs::msg::Bool status;
    status.data = active_;
    active_pub_->publish(status);
    std::size_t moving_points = 0;
    double max_obstacle_speed = 0.0;
    for (const auto & obstacle : obstacles) {
      const double speed = std::hypot(obstacle.vx, obstacle.vy);
      if (speed > 0.0) ++moving_points;
      max_obstacle_speed = std::max(max_obstacle_speed, speed);
    }
    RCLCPP_INFO_THROTTLE(get_logger(), *get_clock(), 1000,
      "DIAG_CONTROL cpp reason=%s pose=(%.3f,%.3f,%.3f) measured=(%.3f,%.3f) "
      "waypoint=%zu/%zu pruned=%zu lookahead=%.3f target_index=%zu target=(%.3f,%.3f) observed=%zu pairs=%zu admissible=%zu "
      "reject_velocity=%zu reject_dynamic=%zu reject_dynamic_now=%zu reject_braking=%zu forward_pairs=%zu moving_points=%zu max_obstacle_speed=%.3f "
      "score_progress=%.3f score_dynamic=%.3f score_distance=%.3f clearance_gain=%.3f clearance_preferred=%d "
      "cmd=(%.3f,%.3f) avoidance_priority=%d reorient=%d goal_heading_error=%.3f odom_age=%.3f obstacle_age=%.3f compute_ms=%.2f",
      result.found ? "command" : "braking_no_pair", state_.x, state_.y, state_.yaw,
      state_.velocity, state_.angular, waypoint_, waypoints_.size(), waypoint_ - previous_waypoint,
      tracking.lookahead, tracking.target_index, tracking.target.first, tracking.target.second,
      obstacles.size(), result.candidates, result.admissible,
      result.rejected_velocity, result.rejected_dynamic, result.rejected_dynamic_now, result.rejected_braking,
      result.forward_pairs, moving_points, max_obstacle_speed,
      result.score_progress, result.score_dynamic, result.score_distance,
      result.clearance_gain, result.clearance_preferred,
      command.linear.x, command.angular.z,
      result.approaching_obstacle, result.reorient,
      planner::angle_error(std::atan2(tracking.target.second - state_.y,
          tracking.target.first - state_.x) - state_.yaw),
      now().seconds() - odom_stamp_, now().seconds() - obstacle_stamp_, compute_ms);
  }

  planner::Config config_;
  planner::Grid grid_;
  planner::State state_;
  planner::Path path_, waypoints_;
  std::vector<planner::Obstacle> obstacles_;
  std::vector<bool> static_occupied_;
  std::size_t waypoint_{0};
  double inflation_{0.0}, odom_stamp_{0.0}, obstacle_stamp_{0.0};
  bool have_map_{false}, have_odom_{false}, have_obstacles_{false}, active_{false};
  std::string frame_;
  std::deque<nav_msgs::msg::Odometry::ConstSharedPtr> odometry_;
  std::deque<sensor_msgs::msg::PointCloud2::ConstSharedPtr> clouds_;
  geometry_msgs::msg::PoseStamped::ConstSharedPtr pending_goal_;
  std::unique_ptr<tf2_ros::Buffer> buffer_;
  std::unique_ptr<tf2_ros::TransformListener> listener_;
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr command_pub_;
  rclcpp::Publisher<std_msgs::msg::Bool>::SharedPtr active_pub_;
  rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr path_pub_;
  rclcpp::Publisher<nav_msgs::msg::OccupancyGrid>::SharedPtr map_pub_;
  rclcpp::Publisher<geometry_msgs::msg::PoseStamped>::SharedPtr goal_pub_;
  rclcpp::Subscription<nav_msgs::msg::OccupancyGrid>::SharedPtr map_sub_;
  rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr odom_sub_;
  rclcpp::Subscription<sensor_msgs::msg::PointCloud2>::SharedPtr obstacle_sub_;
  rclcpp::Subscription<geometry_msgs::msg::PoseStamped>::SharedPtr goal_sub_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char ** argv) {
  rclcpp::init(argc, argv);
  auto node = std::make_shared<ReferenceController>();
  rclcpp::spin(node);
  if (rclcpp::ok()) node->shutdown_command();
  rclcpp::shutdown();
  return 0;
}