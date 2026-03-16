import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import cv2
import numpy as np


class DepthPublisher(Node):

    def __init__(self):
        super().__init__('depth_publisher')

        self.depth_publisher = self.create_publisher(
            Image,
            '/camera/depth/image_raw',
            10
        )

        self.timer = self.create_timer(0.1, self.timer_callback)

        self.cap = cv2.VideoCapture(0)
        self.bridge = CvBridge()

        self.width = 640
        self.height = 480

        self.get_logger().info("Depth publisher started")

    def timer_callback(self):

        ret, frame = self.cap.read()

        if not ret:
            self.get_logger().warning("Failed to read frame from camera")
            return

        frame = cv2.resize(frame, (self.width, self.height))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        depth_image = gray.astype(np.float32) / 255.0 * 5.0

        depth_msg = self.bridge.cv2_to_imgmsg(
            depth_image,
            encoding='32FC1'
        )
        depth_msg.header.stamp = self.get_clock().now().to_msg()
        depth_msg.header.frame_id = 'camera_link'

        self.depth_publisher.publish(depth_msg)
        self.get_logger().info("Publishing synthetic depth image")

def main(args=None):

    rclpy.init(args=args)

    node = DepthPublisher()

    rclpy.spin(node)

    node.cap.release()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()