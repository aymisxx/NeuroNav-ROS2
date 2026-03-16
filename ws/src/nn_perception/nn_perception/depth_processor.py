import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import cv2
import numpy as np


class DepthProcessor(Node):

    def __init__(self):
        super().__init__('depth_processor')

        self.bridge = CvBridge()

        self.subscription = self.create_subscription(
            Image,
            '/camera/depth/image_raw',
            self.depth_callback,
            10
        )

        self.publisher = self.create_publisher(
            Image,
            '/camera/depth_visual',
            10
        )

        self.get_logger().info("Depth processor node started")

    def depth_callback(self, msg):

        depth_image = self.bridge.imgmsg_to_cv2(
            msg,
            desired_encoding='passthrough'
        )

        # Replace invalid depth values
        depth_image = np.nan_to_num(depth_image)

        # Normalize depth for visualization
        depth_normalized = cv2.normalize(
            depth_image,
            None,
            0,
            255,
            cv2.NORM_MINMAX
        )

        depth_visual = depth_normalized.astype(np.uint8)

        depth_msg = self.bridge.cv2_to_imgmsg(
            depth_visual,
            encoding='8UC1'
        )

        self.publisher.publish(depth_msg)


def main(args=None):

    rclpy.init(args=args)

    node = DepthProcessor()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()