#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np


class SemanticSegmentationNode(Node):
    def __init__(self):
        super().__init__('semantic_segmentation_node')

        self.bridge = CvBridge()

        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        self.publisher = self.create_publisher(
            Image,
            '/camera/segmentation_mask',
            10
        )

        self.get_logger().info('Semantic segmentation node started. Subscribed to /camera/image_raw, publishing /camera/segmentation_mask')

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_green = np.array([35, 40, 40])
        upper_green = np.array([85, 255, 255])

        mask = cv2.inRange(hsv, lower_green, upper_green)

        segmented_msg = self.bridge.cv2_to_imgmsg(mask, encoding='mono8')
        segmented_msg.header = msg.header
        self.publisher.publish(segmented_msg)


def main(args=None):
    rclpy.init(args=args)
    node = SemanticSegmentationNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()