import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class LidarPublisher(Node):
    def __init__(self):
        super().__init__('lidar_publisher')
        self.publisher = self.create_publisher(LaserScan, '/scan', 10)
        self.timer = self.create_timer(0.1, self.publish_scan)
        self.step = 0

    def publish_scan(self):
        msg = LaserScan()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'laser_frame'

        msg.angle_min = -math.pi / 2
        msg.angle_max = math.pi / 2
        msg.angle_increment = math.radians(1.0)

        msg.time_increment = 0.0
        msg.scan_time = 0.1

        msg.range_min = 0.2
        msg.range_max = 10.0

        num_readings = int((msg.angle_max - msg.angle_min) / msg.angle_increment) + 1
        ranges = []

        for i in range(num_readings):
            angle = msg.angle_min + i * msg.angle_increment

            base_range = 4.0
            wave = 0.8 * math.sin(3.0 * angle + 0.15 * self.step)

            obstacle_range = base_range + wave

            if abs(angle) < math.radians(10):
                obstacle_range = min(obstacle_range, 2.0 + 0.3 * math.sin(0.1 * self.step))

            obstacle_range = max(msg.range_min, min(msg.range_max, obstacle_range))
            ranges.append(float(obstacle_range))

        msg.ranges = ranges
        msg.intensities = [100.0] * num_readings

        self.publisher.publish(msg)
        self.get_logger().info(f'Published LiDAR scan with {num_readings} beams')
        self.step += 1


def main(args=None):
    rclpy.init(args=args)
    node = LidarPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
