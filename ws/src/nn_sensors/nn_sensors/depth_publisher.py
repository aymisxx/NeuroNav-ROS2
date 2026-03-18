import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import cv2
import numpy as np


class DepthPublisher(Node):

    def __init__(self):
        super().__init__('depth_publisher')

        self.bridge = CvBridge()

        self.depth_publisher = self.create_publisher(
            Image,
            '/camera/depth/image_raw',
            10
        )

        self.rgb_subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        self.width = 640
        self.height = 480

        self.get_logger().info(
            'Depth publisher started. Subscribed to /camera/image_raw'
        )

    def image_callback(self, msg: Image):
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f'Failed to convert RGB image: {e}')
            return

        try:
            frame = cv2.resize(frame, (self.width, self.height))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Synthetic depth: map intensity to 0-5 meters
            depth_image = gray.astype(np.float32) / 255.0 * 5.0

            depth_msg = self.bridge.cv2_to_imgmsg(
                depth_image,
                encoding='32FC1'
            )
            depth_msg.header = msg.header
            depth_msg.header.frame_id = 'camera_link'

            self.depth_publisher.publish(depth_msg)

        except Exception as e:
            self.get_logger().error(f'Failed to publish depth image: {e}')


def main(args=None):
    rclpy.init(args=args)

    node = DepthPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()