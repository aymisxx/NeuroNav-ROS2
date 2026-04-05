import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class ScanProcessingNode(Node):
    def __init__(self):
        super().__init__('scan_processing_node')

        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )
        self.processed_scan_pub = self.create_publisher(
            LaserScan,
            '/scan_processed',
            10
        )

        self.get_logger().info('Scan processing node started. Subscribed to /scan, publishing /scan_processed')

    def scan_callback(self, msg: LaserScan):
        processed_msg = LaserScan()
        processed_msg.header = msg.header
        processed_msg.angle_min = msg.angle_min
        processed_msg.angle_max = msg.angle_max
        processed_msg.angle_increment = msg.angle_increment
        processed_msg.time_increment = msg.time_increment
        processed_msg.scan_time = msg.scan_time
        processed_msg.range_min = msg.range_min
        processed_msg.range_max = msg.range_max
        processed_msg.intensities = list(msg.intensities)

        filtered_ranges = []
        valid_ranges = []

        for r in msg.ranges:
            if math.isfinite(r) and msg.range_min <= r <= msg.range_max:
                filtered_ranges.append(r)
                valid_ranges.append(r)
            else:
                filtered_ranges.append(float('inf'))

        processed_msg.ranges = filtered_ranges
        self.processed_scan_pub.publish(processed_msg)

        total_points = len(msg.ranges)
        valid_points = len(valid_ranges)

        if valid_points > 0:
            min_range = min(valid_ranges)
            max_range = max(valid_ranges)
            avg_range = sum(valid_ranges) / valid_points
            self.get_logger().info(
                f'Scan stats | total={total_points} valid={valid_points} '
                f'min={min_range:.3f} m max={max_range:.3f} m avg={avg_range:.3f} m'
            )
        else:
            self.get_logger().warn(
                f'Scan stats | total={total_points} valid=0 | no valid returns in current scan'
            )


def main(args=None):
    rclpy.init(args=args)
    node = ScanProcessingNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
