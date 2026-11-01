import rclpy
from geometry_msgs.msg import Pose
from rclpy.node import Node
from ros_gz_interfaces.srv import SetEntityPose


class MovingObstacle(Node):
    def __init__(self):
        super().__init__("moving_obstacle")
        self.client = self.create_client(
            SetEntityPose, "/world/dwa_world/set_pose"
        )
        self.obstacles = [
            ("moving_obstacle_1", 2.4, 0.4, 0.0, 0.20),
            ("moving_obstacle_2", 6.8, 2.1, -0.25, 0.0),
        ]
        self.time = 0.0
        self.obstacle_index = 0
        self.request_in_flight = False
        self.service_wait_logged = False
        self.timer = self.create_timer(0.10, self.update)

    def update(self):
        dt = 0.10
        self.time += dt
        if not self.client.service_is_ready():
            if not self.service_wait_logged:
                self.get_logger().warning(
                    "A Gazebo set_pose szolgaltatas meg nem erheto el."
                )
                self.service_wait_logged = True
            return
        self.service_wait_logged = False
        if self.request_in_flight:
            return

        self.request_in_flight = True
        name, x, y, vx, vy = self.obstacles[self.obstacle_index]
        request = SetEntityPose.Request()
        request.entity.name = name
        request.entity.type = request.entity.MODEL
        request.pose = Pose()
        request.pose.position.x = x + vx * self.time
        request.pose.position.y = y + vy * self.time
        request.pose.position.z = 0.45
        request.pose.orientation.w = 1.0
        future = self.client.call_async(request)
        future.add_done_callback(self._handle_pose_response)

    def _handle_pose_response(self, future):
        try:
            response = future.result()
        except Exception as error:
            self.get_logger().warning(f"A Gazebo poziciofrissitese sikertelen: {error}")
        else:
            if not response.success:
                self.get_logger().warning(
                    "A Gazebo nem fogadta el a mozgó akadály pozíciófrissítését."
                )
        self.obstacle_index = (self.obstacle_index + 1) % len(self.obstacles)
        self.request_in_flight = False


def main(args=None):
    rclpy.init(args=args)
    node = MovingObstacle()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
