#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid
from sensor_msgs.msg import Image
from std_msgs.msg import Header
from cv_bridge import CvBridge
import cv2
import numpy as np


class SemanticMapNode(Node):
    def __init__(self):
        super().__init__('semantic_map_node')

        self.bridge = CvBridge()

        self.map_pub = self.create_publisher(OccupancyGrid, '/semantic_map', 10)
        self.mask_sub = self.create_subscription(
            Image,
            '/camera/segmentation_mask',
            self.mask_callback,
            10
        )

        self.width = 192
        self.height = 108
        self.resolution = 0.05
        self.origin_x = -(self.width * self.resolution) / 2.0
        self.origin_y = -(self.height * self.resolution) / 2.0

        self.get_logger().info(
            'Semantic map node started. Subscribed to /camera/segmentation_mask, publishing /semantic_map'
        )

    def mask_callback(self, msg: Image):
        mask = self.bridge.imgmsg_to_cv2(msg, desired_encoding='mono8')

        resized = cv2.resize(mask, (self.width, self.height), interpolation=cv2.INTER_NEAREST)

        data = []
        semantic_cells = 0

        for row in resized:
            for pixel in row:
                if pixel > 0:
                    data.append(100)
                    semantic_cells += 1
                else:
                    data.append(0)

        semantic_map_msg = OccupancyGrid()
        semantic_map_msg.header = Header()
        semantic_map_msg.header.stamp = self.get_clock().now().to_msg()
        semantic_map_msg.header.frame_id = 'map'

        semantic_map_msg.info.resolution = self.resolution
        semantic_map_msg.info.width = self.width
        semantic_map_msg.info.height = self.height
        semantic_map_msg.info.origin.position.x = self.origin_x
        semantic_map_msg.info.origin.position.y = self.origin_y
        semantic_map_msg.info.origin.orientation.w = 1.0

        semantic_map_msg.data = data

        self.map_pub.publish(semantic_map_msg)
        # Reduced per-frame logging for lighter runtime execution.


def main(args=None):
    rclpy.init(args=args)
    node = SemanticMapNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
