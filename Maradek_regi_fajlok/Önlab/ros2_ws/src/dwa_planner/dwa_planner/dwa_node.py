import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, PoseStamped
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import math
import numpy as np
from tf2_ros import TransformListener, Buffer
from tf2_geometry_msgs import do_transform_point
from geometry_msgs.msg import PointStamped

class DWANode(Node):
    def __init__(self):
        super().__init__('dwa_node')
        # Publikálók
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.filtered_scan_pub = self.create_publisher(LaserScan, '/scan_filtered', 10)

        # Feliratkozók
        self.create_subscription(LaserScan, '/scan', self.scan_cb, 10)
        self.create_subscription(Odometry, '/odom', self.odom_cb, 10)
        self.create_subscription(PoseStamped, '/goal_pose', self.goal_cb, 10)
        
        self.x, self.y, self.yaw = 0.0, 0.0, 0.0
        self.obstacles = []
        self.goal_x, self.goal_y = None, None
        
        # TF2 a SLAM-hez
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.map_x, self.map_y, self.map_yaw = 0.0, 0.0, 0.0
        self.use_slam = False
        
        # Timer-ek
        self.create_timer(0.05, self.update_robot_pose)
        self.create_timer(0.1, self.control_loop)
        
        self.get_logger().info("--- DWA NODE ELINDULT ---")

    def update_robot_pose(self):
        """Lekéri a robot pozícióját a map keretben (SLAM-tól)"""
        try:
            # Ellenőrizzük, hogy létezik-e a transzformáció
            if self.tf_buffer.can_transform('map', 'base_footprint', rclpy.time.Time()):
                transform = self.tf_buffer.lookup_transform('map', 'base_footprint', rclpy.time.Time())
                self.map_x = transform.transform.translation.x
                self.map_y = transform.transform.translation.y
                q = transform.transform.rotation
                self.map_yaw = math.atan2(2*(q.w*q.z + q.x*q.y), 1-2*(q.y*q.y + q.z*q.z))
                self.use_slam = True
            else:
                self.use_slam = False
        except Exception as e:
            self.use_slam = False
            pass

    def goal_cb(self, msg):
        self.goal_x, self.goal_y = msg.pose.position.x, msg.pose.position.y
        self.get_logger().info(f'Új cél: ({self.goal_x}, {self.goal_y})')

    def odom_cb(self, msg):
        self.x, self.y = msg.pose.pose.position.x, msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        self.yaw = math.atan2(2*(q.w*q.z + q.x*q.y), 1-2*(q.y*q.y + q.z*q.z))

    def scan_cb(self, msg):
        self.obstacles = []
        filtered_msg = msg
        new_ranges = list(msg.ranges)

        for i, r in enumerate(new_ranges):
            if 0.25 < r < 3.0 and not math.isinf(r):
                # A DWA belső számításához az akadályokat a robot aktuális pozíciójához viszonyítva tároljuk
                angle = msg.angle_min + i * msg.angle_increment + self.yaw
                ox = self.x + r * math.cos(angle)
                oy = self.y + r * math.sin(angle)
                self.obstacles.append([ox, oy])
            else:
                new_ranges[i] = float('inf')

        filtered_msg.ranges = new_ranges
        self.filtered_scan_pub.publish(filtered_msg)

    def control_loop(self):
        if self.goal_x is None: 
            return
        
        # Használjuk a SLAM pozíciót, ha van
        if self.use_slam:
            current_x = self.map_x
            current_y = self.map_y
            current_yaw = self.map_yaw
        else:
            current_x = self.x
            current_y = self.y
            current_yaw = self.yaw
        
        dist_to_goal = math.hypot(self.goal_x - current_x, self.goal_y - current_y)
        if dist_to_goal < 0.2:
            self.cmd_pub.publish(Twist())
            self.goal_x = None
            self.get_logger().info("CELBA ERTEM!")
            return

        best_v, best_w, max_score = 0.0, 0.0, -1e9
        
        for v in [0.2, 0.3]:  # Több sebesség opció
            for w in np.linspace(-0.8, 0.8, 11):
                new_yaw = current_yaw + w * 1.0
                px = current_x + v * math.cos(new_yaw) * 1.0
                py = current_y + v * math.sin(new_yaw) * 1.0
                
                safe = True
                for ox, oy in self.obstacles:
                    if math.hypot(px - ox, py - oy) < 0.4:
                        safe = False
                        break
                
                if safe:
                    score = -math.hypot(self.goal_x - px, self.goal_y - py)
                    if score > max_score:
                        max_score, best_v, best_w = score, v, w

        msg = Twist()
        msg.linear.x = float(best_v)
        msg.angular.z = float(best_w)
        self.cmd_pub.publish(msg)

def main():
    rclpy.init()
    rclpy.spin(DWANode())
    rclpy.shutdown()

if __name__ == '__main__':
    main()