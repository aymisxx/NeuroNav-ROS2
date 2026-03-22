import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu


class ImuPublisher(Node):
    def __init__(self):
        super().__init__('imu_publisher')

        self.publisher_ = self.create_publisher(Imu, '/imu/data', 10)
        self.timer = self.create_timer(0.1, self.publish_imu_data)  # 10 Hz
        self.t = 0.0

        self.get_logger().info('IMU Publisher Started')

    def publish_imu_data(self):
        msg = Imu()

        now = self.get_clock().now().to_msg()
        msg.header.stamp = now
        msg.header.frame_id = 'imu_link'

        # Simulated angular velocity (rad/s)
        msg.angular_velocity.x = 0.1 * math.sin(self.t)
        msg.angular_velocity.y = 0.1 * math.cos(self.t)
        msg.angular_velocity.z = 0.2 * math.sin(0.5 * self.t)

        # Simulated linear acceleration (m/s^2)
        msg.linear_acceleration.x = 0.5 * math.sin(self.t)
        msg.linear_acceleration.y = 0.3 * math.cos(self.t)
        msg.linear_acceleration.z = 9.81

        # Orientation unknown for now
        msg.orientation_covariance[0] = -1.0

        self.publisher_.publish(msg)
        self.get_logger().info('Publishing IMU data')

        self.t += 0.1


def main(args=None):
    rclpy.init(args=args)
    node = ImuPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()