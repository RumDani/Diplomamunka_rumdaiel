"""Gazebo-independent ROS2 adapter for the unchanged Python A* and DWA."""

import copy
import math
import time
import traceback

import rclpy
from geometry_msgs.msg import PoseStamped, Twist
from nav_msgs.msg import OccupancyGrid, Odometry, Path
from rclpy.node import Node
from rclpy.clock import Clock, ClockType
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.qos import DurabilityPolicy, QoSProfile, qos_profile_sensor_data
from rclpy.time import Time
from sensor_msgs.msg import LaserScan, PointCloud2
from sensor_msgs_py import point_cloud2
from std_msgs.msg import Bool, Header
from tf2_ros import Buffer, TransformException, TransformListener
from visualization_msgs.msg import Marker, MarkerArray

from codes_diploma.robot import Obstacle, robotconfig, robotstate, update
from codes_diploma.astar_project.grid_map import GridMap
from codes_diploma.astar_project.astar_variants import get_heuristic
from .python_reference import create_gazebo_scene, create_scene, load_planner_class


class PythonPlannerNode(Node):
    def __init__(self):
        super().__init__("astar_dwa_node")
        self.grid, self.start, self.default_goal, self.state, self.statics, _ = create_scene()
        self.config = robotconfig()
        for name in ("r_kerek", "b", "rob_radius", "a_max", "dt", "predict_time",
                     "safety_margin", "static_safety_margin", "Alfa", "Beta", "Gamma",
                     "w_kerek_resolution", "w_kerek_max"):
            setattr(self.config, name, float(self.declare_parameter(name, float(getattr(self.config, name))).value))
        self.config.w_kerek_min = -self.config.w_kerek_max
        if min(self.config.r_kerek, self.config.b, self.config.dt,
               self.config.predict_time, self.config.w_kerek_resolution, self.config.w_kerek_max) <= 0:
            raise ValueError("Robot dimensions, time steps and wheel limits must be positive.")
        self.external_clock = self.declare_parameter("external_control_ticks", False).value
        self.map_source = self.declare_parameter("map_source", "reference").value
        if self.map_source not in ("reference", "topic"):
            raise ValueError("map_source must be reference or topic")
        self.map_ready = self.map_source == "reference"
        self.map_dirty = True
        self.map_signature = None
        self.map_sequence = 0
        self.map_frame = "odom" if self.map_ready else "map"
        self.base_frame = self.declare_parameter("base_frame", "base_link").value
        self.inflation_radius = float(self.declare_parameter(
            "map_inflation_radius", self.config.rob_radius + self.config.static_safety_margin).value)
        self.occupied_threshold = int(self.declare_parameter("occupied_threshold", 65).value)
        if self.inflation_radius < 0 or not 1 <= self.occupied_threshold <= 100:
            raise ValueError("Invalid map inflation or occupancy threshold")
        world_file = self.declare_parameter("world_file", "").value
        map_resolution = float(self.declare_parameter("map_resolution", 0.2).value)
        if world_file and self.map_source == "reference":
            self.grid, self.start, self.default_goal, self.state, self.statics, _ = create_gazebo_scene(
            world_file, resolution=map_resolution, inflation_radius=self.inflation_radius)
        if not self.map_ready:
            self.statics = []
        self.obstacle_source = self.declare_parameter("obstacle_source", "scan").value
        if self.obstacle_source not in ("scan", "tracked"):
            raise ValueError("obstacle_source must be scan or tracked")
        self.planner = load_planner_class()(self.grid, config=self.config, diagonal=True)
        self.pending_goal = self.default_goal if self.declare_parameter("autostart", False).value else None
        self.requested_goal = None
        self.active = False
        self.control_sequence = 0
        self.last_diagnostic_reason = None
        self.last_diagnostic_wall = -math.inf
        self.odom_stamp = self.obstacle_stamp = None
        self.obstacles = []
        self.pending_tick = None
        self.control_group = MutuallyExclusiveCallbackGroup()
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.cmd_pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.path_pub = self.create_publisher(Path, "/astar_path", 10)
        latched = QoSProfile(depth=1, durability=DurabilityPolicy.TRANSIENT_LOCAL)
        self.map_pub = self.create_publisher(OccupancyGrid, "/astar_map", latched)
        self.goal_pub = self.create_publisher(PoseStamped, "/accepted_goal", latched)
        self.marker_pub = self.create_publisher(MarkerArray, "/astar_dwa_markers", 10)
        self.active_pub = self.create_publisher(Bool, "/controller_active", latched)
        self.done_pub = self.create_publisher(Header, "/control_done", 10)
        self.create_subscription(Odometry, "/odom", self.odom, 10)
        self.create_subscription(OccupancyGrid, "/map", self.map_received, latched,
                     callback_group=self.control_group)
        self.create_subscription(PoseStamped, "/goal_pose", self.goal, 10,
                     callback_group=self.control_group)
        self.create_subscription(PointCloud2, "/tracked_obstacles", self.tracked, 10)
        self.create_subscription(LaserScan, "/scan", self.scan, qos_profile_sensor_data)
        self.create_subscription(Header, "/control_tick", self.control_tick, 10,
                     callback_group=self.control_group)
        self.create_timer(self.config.dt, self.timer, callback_group=self.control_group)
        self.display_clock = Clock(clock_type=ClockType.STEADY_TIME)
        self.create_timer(0.5, self.publish_scene, clock=self.display_clock,
                  callback_group=self.control_group)
        if self.declare_parameter("gazebo_path_debug", False).value:
            from .gazebo_path_node import GazeboPathDisplay
            self.gazebo_path = GazeboPathDisplay(self)
        self.get_logger().info(
            f"python-lidar-reference: grid={self.grid.width}x{self.grid.height}, "
            f"resolution={self.grid.resolution}, start={self.start}, default_goal={self.default_goal}; "
            f"map_source={self.map_source}, obstacles={self.obstacle_source}, external_ticks={self.external_clock}"
        )
        self.get_logger().info(
            f"DIAG_CONFIG schema=slam-waypoints-1 source={__file__} "
            f"map_source={self.map_source} map_ready={self.map_ready} frame={self.map_frame} "
            f"robot_radius={self.config.rob_radius} wheel_radius={self.config.r_kerek} "
            f"half_axle={self.config.b} wheel_limit={self.config.w_kerek_max} "
            f"acceleration={self.config.a_max} dt={self.config.dt} horizon={self.config.predict_time} "
            f"safety_margin={self.config.safety_margin} static_margin={self.config.static_safety_margin} "
            f"weights=({self.config.Alfa},{self.config.Beta},{self.config.Gamma}) "
            f"obstacle_source={self.obstacle_source}")

    def log_control(self, reason, state=None, result=None, visible=None,
                    observed=None, obstacle_stamp=None, command=None, compute_ms=0.0):
        wall_time = time.monotonic()
        if reason == self.last_diagnostic_reason and wall_time - self.last_diagnostic_wall < 2.0:
            return
        self.last_diagnostic_reason = reason
        self.last_diagnostic_wall = wall_time
        state = self.state if state is None else state
        observed = self.obstacles if observed is None else observed
        obstacle_stamp = self.obstacle_stamp if obstacle_stamp is None else obstacle_stamp
        odom_stamp = getattr(state, "odom_stamp", None)
        now = self.get_clock().now().nanoseconds * 1e-9
        odom_age = None if odom_stamp is None else round(now - odom_stamp, 3)
        obstacle_age = None if obstacle_stamp is None else round(now - obstacle_stamp, 3)
        nearest = min(observed, key=lambda obstacle: math.hypot(
            obstacle.x - state.x, obstacle.y - state.y), default=None)
        nearest_info = None if nearest is None else (
            round(math.hypot(nearest.x - state.x, nearest.y - state.y), 3),
            round(nearest.radius, 3), round(nearest.vx, 3), round(nearest.vy, 3))
        moving = sum(math.hypot(obstacle.vx, obstacle.vy) > 0 for obstacle in observed)
        result = {} if result is None else result
        goal_distance = None if self.requested_goal is None else round(math.hypot(
            self.requested_goal[0] - state.x, self.requested_goal[1] - state.y), 3)
        linear = 0.0 if command is None else command.linear.x
        angular = 0.0 if command is None else command.angular.z
        self.get_logger().info(
            f"DIAG_CONTROL seq={self.control_sequence} sim_t={now:.3f} reason={reason} "
            f"frame={self.map_frame} map_seq={self.map_sequence} odom_stamp={odom_stamp} "
            f"obstacle_stamp={obstacle_stamp} odom_age={odom_age} obstacle_age={obstacle_age} "
            f"pose_valid={odom_stamp is not None} pose=({state.x:.3f},{state.y:.3f},{state.irany:.3f}) "
            f"measured=({getattr(state, 'v', 0.0):.3f},{getattr(state, 'w', 0.0):.3f}) "
            f"wheel=({state.w_L:.3f},{state.w_R:.3f}) goal={self.requested_goal} goal_distance={goal_distance} "
            f"waypoint={self.planner.waypoint_index}/{len(self.planner.waypoints)} "
            f"target={result.get('target')} observed={len(observed)} "
            f"visible={0 if visible is None else len(visible)} moving={moving} "
            f"nearest_dist_radius_vx_vy={nearest_info} "
            f"pairs={len(result.get('all_pairs', []))} admissible={len(result.get('safe_pairs', []))} "
            f"cmd=({linear:.3f},{angular:.3f}) compute_ms={compute_ms:.1f}")

    def odom(self, message):
        if not self.map_ready:
            return
        transform = self.frame_transform(message.header.frame_id, message.header.stamp)
        if transform is None:
            return
        offset_x, offset_y, offset_yaw = transform
        orientation = message.pose.pose.orientation
        x, y = message.pose.pose.position.x, message.pose.pose.position.y
        state = robotstate()
        state.x = offset_x + math.cos(offset_yaw) * x - math.sin(offset_yaw) * y
        state.y = offset_y + math.sin(offset_yaw) * x + math.cos(offset_yaw) * y
        state.irany = offset_yaw + math.atan2(
            2.0 * (orientation.w * orientation.z + orientation.x * orientation.y),
            1.0 - 2.0 * (orientation.y ** 2 + orientation.z ** 2),
        )
        state.v, state.w = message.twist.twist.linear.x, message.twist.twist.angular.z
        state.w_L = (state.v - self.config.b * state.w) / self.config.r_kerek
        state.w_R = (state.v + self.config.b * state.w) / self.config.r_kerek
        state.odom_stamp = self.seconds(message.header.stamp)
        self.state = state
        self.odom_stamp = state.odom_stamp

    @staticmethod
    def seconds(stamp):
        return stamp.sec + stamp.nanosec * 1e-9

    def frame_transform(self, source, stamp):
        if source == self.map_frame:
            return 0.0, 0.0, 0.0
        try:
            transform = self.tf_buffer.lookup_transform(
                self.map_frame, source, Time.from_msg(stamp)
            ).transform
        except TransformException:
            self.get_logger().warning(
                f"Waiting for TF: {source} -> {self.map_frame}", throttle_duration_sec=2.0)
            return None
        rotation = transform.rotation
        yaw = math.atan2(2 * (rotation.w * rotation.z + rotation.x * rotation.y),
                         1 - 2 * (rotation.y ** 2 + rotation.z ** 2))
        return transform.translation.x, transform.translation.y, yaw

    def map_received(self, message):
        if self.map_source != "topic":
            return
        info, rotation = message.info, message.info.origin.orientation
        if (info.width <= 0 or info.height <= 0 or info.resolution <= 0 or
                len(message.data) != info.width * info.height or not message.header.frame_id or
                abs(rotation.x) + abs(rotation.y) + abs(rotation.z) > 1e-6):
            self.get_logger().error("Invalid map or rotated origin; an axis-aligned occupancy map is required.")
            return
        signature = (message.header.frame_id, info.width, info.height, info.resolution,
                     info.origin.position.x, info.origin.position.y, tuple(message.data))
        if signature == self.map_signature:
            return
        same_frame = self.map_ready and self.map_frame == message.header.frame_id
        grid = GridMap(info.width, info.height, info.resolution,
                       info.origin.position.x, info.origin.position.y)
        grid.grid = [[2 if value < 0 else int(value >= self.occupied_threshold)
                      for value in message.data[row * info.width:(row + 1) * info.width]]
                     for row in range(info.height)]
        grid.inflate_obstacles(self.inflation_radius)
        self.grid = self.planner.grid_map = grid
        self.map_signature = signature
        self.map_sequence += 1
        self.map_dirty = True
        self.map_frame, self.map_ready = message.header.frame_id, True
        if not same_frame:
            self.active = False
            self.pending_goal = self.requested_goal = None
            self.odom_stamp = self.obstacle_stamp = None
            self.planner.path.clear()
            self.planner.waypoints.clear()
            self.cmd_pub.publish(Twist())
            self.active_pub.publish(Bool(data=False))
        self.publish_scene()
        self.get_logger().info(
            f"DIAG_MAP seq={self.map_sequence} frame={self.map_frame} "
            f"grid={grid.width}x{grid.height} resolution={grid.resolution} "
            f"origin=({grid.origin_x},{grid.origin_y}) "
            f"action={'waypoints_kept' if same_frame else 'frame_reset_wait_goal'} "
            f"goal={self.requested_goal} waypoint={self.planner.waypoint_index}")

    def goal(self, message):
        self.get_logger().info(
            f"DIAG_GOAL reason=received frame={message.header.frame_id} "
            f"xy=({message.pose.position.x},{message.pose.position.y}) "
            f"map_ready={self.map_ready}")
        if not self.map_ready:
            self.get_logger().warning("DIAG_GOAL reason=waiting_map; no SLAM map received yet.")
            return
        target = (message.pose.position.x, message.pose.position.y)
        received = target
        if not all(math.isfinite(value) for value in target):
            self.get_logger().error("DIAG_GOAL reason=nonfinite; goal coordinates must be finite.")
            return
        transform = self.frame_transform(message.header.frame_id or self.map_frame, message.header.stamp)
        if transform is None:
            self.get_logger().warning(
                f"DIAG_GOAL reason=tf_missing source={message.header.frame_id} target={self.map_frame}")
            return
        offset_x, offset_y, yaw = transform
        target = (offset_x + math.cos(yaw) * target[0] - math.sin(yaw) * target[1],
                  offset_y + math.sin(yaw) * target[0] + math.cos(yaw) * target[1])
        goal_cell = self.grid.world_to_grid(*target)
        if not self.grid.is_free(*goal_cell):
            if not self.grid.is_inside(*goal_cell):
                reason = "outside_map"
            elif self.grid.grid[goal_cell[0]][goal_cell[1]] == 2:
                reason = "unknown_cell"
            else:
                reason = "occupied_or_inflated"
            self.get_logger().error(
                f"DIAG_GOAL reason={reason} xy={target} cell={goal_cell} "
                f"grid={self.grid.width}x{self.grid.height} resolution={self.grid.resolution} "
                f"origin=({self.grid.origin_x},{self.grid.origin_y}) "
                f"inflation_radius={self.inflation_radius}; choose observed free space.")
            return
        cell_center = self.grid.grid_to_world(*goal_cell)
        quantization_error = math.hypot(target[0] - cell_center[0], target[1] - cell_center[1])
        self.get_logger().info(
            f"DIAG_GOAL reason=accepted received={received} frame={message.header.frame_id}; "
            f"accepted={target} planning_frame={self.map_frame}; "
            f"goal_cell={goal_cell} cell_center={cell_center} "
            f"cell_center_error={quantization_error:.4f} m")
        self.pending_goal = target
        self.plan_pending_goal()

    def plan_pending_goal(self):
        if self.pending_goal is None or self.odom_stamp is None:
            return
        target, self.pending_goal = self.pending_goal, None
        self.active = False
        self.cmd_pub.publish(Twist())
        self.active_pub.publish(Bool(data=False))
        try:
            self.active = bool(self.planner.plan_global(
                (self.state.x, self.state.y), target, heuristic=get_heuristic("euclidean"),
                smooth=True, samples_per_curve=8
            ))
            if self.active:
                self.requested_goal = target
                endpoint = self.planner.path[-1]
                if self.grid.world_to_grid(*endpoint) == self.grid.world_to_grid(*target):
                    self.planner.path[-1] = target
                    self.planner.bezier_path[-1] = target
                    self.planner.waypoints[-1] = target
                goal_message = PoseStamped()
                goal_message.header.frame_id = self.map_frame
                goal_message.header.stamp = self.get_clock().now().to_msg()
                goal_message.pose.position.x, goal_message.pose.position.y = target
                goal_message.pose.orientation.w = 1.0
                self.goal_pub.publish(goal_message)
                self.get_logger().info(
                    f"Planned goal: requested={target} endpoint={self.planner.path[-1]} "
                    f"waypoints={len(self.planner.waypoints)} frame={self.map_frame}")
        except (ValueError, RuntimeError) as error:
            self.active = False
            self.get_logger().error(f"Global planner failed: {error}")
        self.cmd_pub.publish(Twist())
        self.active_pub.publish(Bool(data=self.active))
        self.publish_scene()

    def tracked(self, message):
        if self.obstacle_source != "tracked" or not self.map_ready:
            return
        transform = self.frame_transform(message.header.frame_id, message.header.stamp)
        if transform is None:
            return
        offset_x, offset_y, yaw = transform
        cosine, sine = math.cos(yaw), math.sin(yaw)
        self.obstacles = [Obstacle(offset_x + cosine * float(row[0]) - sine * float(row[1]),
                                   offset_y + sine * float(row[0]) + cosine * float(row[1]),
                                   radius=float(row[2]),
                                   vx=cosine * float(row[3]) - sine * float(row[4]),
                                   vy=sine * float(row[3]) + cosine * float(row[4]))
                          for row in point_cloud2.read_points(
                              message, field_names=("x", "y", "radius", "vx", "vy"), skip_nans=True)]
        self.obstacle_stamp = self.seconds(message.header.stamp)
        self.run_pending_tick()

    def scan(self, message):
        if self.obstacle_source != "scan" or self.odom_stamp is None:
            return
        try:
            transform = self.tf_buffer.lookup_transform(
                self.map_frame, message.header.frame_id, Time.from_msg(message.header.stamp)
            ).transform
        except TransformException:
            self.get_logger().warning("Waiting for scan-to-map TF.", throttle_duration_sec=2.0)
            return
        rotation = transform.rotation
        sensor_yaw = math.atan2(2 * (rotation.w * rotation.z + rotation.x * rotation.y),
                                1 - 2 * (rotation.y ** 2 + rotation.z ** 2))
        obstacles = []
        for index, value in enumerate(message.ranges):
            angle = message.angle_min + index * message.angle_increment
            if not math.isfinite(value) or not message.range_min <= value <= min(message.range_max, 3.0):
                continue
            x = transform.translation.x + value * math.cos(sensor_yaw + angle)
            y = transform.translation.y + value * math.sin(sensor_yaw + angle)
            if any(math.hypot(x - wall.x, y - wall.y) < wall.radius + 0.05 for wall in self.statics):
                continue
            obstacles.append(Obstacle(x, y, radius=0.0))
        self.obstacles = obstacles
        self.obstacle_stamp = self.seconds(message.header.stamp)

    def control_tick(self, message):
        if self.external_clock:
            self.pending_tick = message
            self.run_pending_tick()

    def run_pending_tick(self):
        if self.pending_tick is None or self.obstacle_stamp is None:
            return
        if self.obstacle_stamp + 1e-6 < self.seconds(self.pending_tick.stamp):
            return
        tick, self.pending_tick = self.pending_tick, None
        self.plan_local()
        self.done_pub.publish(tick)

    def timer(self):
        self.plan_pending_goal()
        self.publish_scene()
        if not self.external_clock:
            self.plan_local()

    def plan_local(self):
        self.control_sequence += 1
        compute_start = time.perf_counter()
        now = self.get_clock().now().nanoseconds * 1e-9
        if not self.active or self.odom_stamp is None or self.obstacle_stamp is None:
            self.cmd_pub.publish(Twist())
            if not self.map_ready:
                reason = "waiting_map"
            elif self.odom_stamp is None:
                reason = "waiting_odometry"
            elif self.obstacle_stamp is None:
                reason = "waiting_obstacles"
            else:
                reason = "inactive"
            self.log_control(reason)
            return
        if now - min(self.odom_stamp, self.obstacle_stamp) > max(0.5, 3 * self.config.dt):
            self.cmd_pub.publish(Twist())
            self.get_logger().warning("Stale odometry/obstacles: stopping.", throttle_duration_sec=2.0)
            self.log_control("stale_input")
            return
        previous_waypoint = self.planner.waypoint_index
        try:
            state = copy.copy(self.state)
            observed = list(self.obstacles)
            obstacle_stamp = self.obstacle_stamp
            sample_stamp = min(state.odom_stamp, obstacle_stamp)
            visible = []
            for obstacle in self.statics + observed:
                dx, dy = obstacle.x - state.x, obstacle.y - state.y
                angle = math.atan2(dy, dx) - state.irany
                if math.hypot(dx, dy) <= 3.0 and abs(math.atan2(math.sin(angle), math.cos(angle))) <= math.pi / 2:
                    visible.append(obstacle)
            result = self.planner.plan_local(state, visible)
            pair = result["best_pair"] if result is not None else None
            ghost = robotstate(x=state.x, y=state.y, irany=state.irany,
                               w_L=state.w_L, w_R=state.w_R)
            left, right = (0.0, 0.0) if pair is None else pair[2:4]
            update(ghost, self.config, left, right, self.config.dt)
            age = self.get_clock().now().nanoseconds * 1e-9 - sample_stamp
            compute_ms = 1000.0 * (time.perf_counter() - compute_start)
            if not self.external_clock and age > max(0.5, 3 * self.config.dt):
                self.planner.waypoint_index = previous_waypoint
                self.cmd_pub.publish(Twist())
                self.get_logger().warning(f"Planner deadline: compute={compute_ms:.0f} ms, sample_age={age:.3f} s; stopping.",
                                          throttle_duration_sec=2.0)
                self.log_control("planner_deadline", state, result, visible,
                                 observed, obstacle_stamp, compute_ms=compute_ms)
                return
            command = Twist()
            command.linear.x, command.angular.z = float(ghost.v), float(ghost.w)
            self.active = result is not None and not result["finished"]
            if not self.active and result is not None and result["finished"]:
                self.get_logger().info(
                    f"Goal reached: requested={self.requested_goal}, "
                    f"endpoint={self.planner.waypoints[-1]}, pose=({state.x:.3f},{state.y:.3f})")
            published_command = command if self.active else Twist()
            self.cmd_pub.publish(published_command)
            self.active_pub.publish(Bool(data=self.active))
            self.publish_scene()
            if result is None:
                reason = "no_local_plan"
            elif result["finished"]:
                reason = "finished"
            else:
                reason = "braking_no_pair" if pair is None else "command"
            self.log_control(reason, state, result, visible, observed,
                             obstacle_stamp, published_command, compute_ms)
        except Exception as error:
            self.planner.waypoint_index = previous_waypoint
            self.active = False
            self.cmd_pub.publish(Twist())
            self.active_pub.publish(Bool(data=False))
            self.log_control("exception")
            self.get_logger().error(f"Python local planner failed: {error}\n{traceback.format_exc()}")

    def publish_scene(self):
        if not self.map_ready:
            return
        path = Path()
        path.header.frame_id, path.header.stamp = self.map_frame, self.get_clock().now().to_msg()
        for x, y in self.planner.path:
            pose = PoseStamped()
            pose.header = path.header
            pose.pose.position.x, pose.pose.position.y = float(x), float(y)
            pose.pose.orientation.w = 1.0
            path.poses.append(pose)
        self.path_pub.publish(path)
        if self.map_dirty:
            grid = OccupancyGrid()
            grid.header = path.header
            grid.info.width, grid.info.height, grid.info.resolution = self.grid.width, self.grid.height, self.grid.resolution
            grid.info.origin.position.x, grid.info.origin.position.y = self.grid.origin_x, self.grid.origin_y
            grid.info.origin.orientation.w = 1.0
            grid.data = [-1 if cell == 2 else 100 if cell else 0 for row in self.grid.grid for cell in row]
            self.map_pub.publish(grid)
            self.map_dirty = False
        markers = MarkerArray()
        robot = Marker()
        robot.header.frame_id, robot.header.stamp = self.base_frame, path.header.stamp
        robot.header.stamp = Time().to_msg()
        robot.frame_locked = True
        robot.ns, robot.id, robot.type, robot.action = "python_reference", 0, Marker.CYLINDER, Marker.ADD
        robot.pose.position.z, robot.pose.orientation.w = 0.05, 1.0
        robot.scale.x = robot.scale.y = 2.0 * self.config.rob_radius
        robot.scale.z = 0.1
        robot.color.g, robot.color.b, robot.color.a = 0.7, 0.9, 0.9
        markers.markers.append(robot)
        if self.planner.waypoints:
            target = Marker()
            target.header, target.ns, target.id = path.header, "python_reference", 1
            target.type, target.action = Marker.SPHERE, Marker.ADD
            target.pose.position.x, target.pose.position.y = self.planner.waypoints[self.planner.waypoint_index]
            target.pose.position.z, target.pose.orientation.w = 0.15, 1.0
            target.scale.x = target.scale.y = target.scale.z = 0.12
            target.color.g, target.color.a = 1.0, 1.0
            markers.markers.append(target)
        if self.requested_goal is not None:
            goal = Marker()
            goal.header, goal.ns, goal.id = path.header, "python_reference", 2
            goal.type, goal.action = Marker.CYLINDER, Marker.ADD
            goal.pose.position.x, goal.pose.position.y = self.requested_goal
            goal.pose.position.z, goal.pose.orientation.w = 0.02, 1.0
            goal.scale.x = goal.scale.y = 0.2
            goal.scale.z = 0.025
            goal.color.r, goal.color.g, goal.color.a = 1.0, 0.4, 1.0
            markers.markers.append(goal)
        self.marker_pub.publish(markers)


def main(args=None):
    rclpy.init(args=args)
    node = PythonPlannerNode()
    executor = MultiThreadedExecutor(num_threads=2)
    executor.add_node(node)
    try:
        executor.spin()
    finally:
        executor.shutdown()
        node.cmd_pub.publish(Twist())
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()