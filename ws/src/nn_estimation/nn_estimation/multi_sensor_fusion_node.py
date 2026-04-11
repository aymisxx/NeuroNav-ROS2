#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from nav_msgs.msg import OccupancyGrid
from std_msgs.msg import String


class MultiSensorFusionNode(Node):
    def __init__(self):
        super().__init__('multi_sensor_fusion_node')

        self.latest_image = None
        self.latest_map = None

        self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        self.create_subscription(
            OccupancyGrid,
            '/semantic_map',
            self.map_callback,
            10
        )

        self.fusion_pub = self.create_publisher(String, '/fusion_status', 10)

        self.get_logger().info(
            'Multi-sensor fusion node started. Subscribed to /camera/image_raw and /semantic_map, publishing /fusion_status'
        )

    def image_callback(self, msg):
        self.latest_image = msg
        self.publish_fusion_status()

    def map_callback(self, msg):
        self.latest_map = msg
        self.publish_fusion_status()

    def publish_fusion_status(self):
        if self.latest_image is None or self.latest_map is None:
            return

        width = self.latest_map.info.width
        height = self.latest_map.info.height
        nonzero = sum(1 for v in self.latest_map.data if v > 0)

        fused = String()
        fused.data = (
            f'fusion_ok | image={self.latest_image.width}x{self.latest_image.height} '
            f'| semantic_map={width}x{height} | occupied_cells={nonzero}'
        )

        self.fusion_pub.publish(fused)
        self.get_logger().info(fused.data)


def main(args=None):
    rclpy.init(args=args)
    node = MultiSensorFusionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
