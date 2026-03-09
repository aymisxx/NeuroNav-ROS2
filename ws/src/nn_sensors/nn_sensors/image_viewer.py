import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import cv2


class ImageViewer(Node):

    def __init__(self):
        super().__init__('image_viewer')

        self.declare_parameter('image_topic', '/camera/image_raw')
        image_topic = self.get_parameter('image_topic').get_parameter_value().string_value

        self.bridge = CvBridge()

        self.subscription = self.create_subscription(
            Image,
            image_topic,
            self.listener_callback,
            10
        )

        self.get_logger().info(f"Subscribing to: {image_topic}")

    def listener_callback(self, msg):

        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')

        cv2.imshow("Camera Feed", frame)
        cv2.waitKey(1)

        self.get_logger().info(f"Receiving camera frame ({msg.encoding})")


def main(args=None):

    rclpy.init(args=args)

    node = ImageViewer()

    rclpy.spin(node)

    cv2.destroyAllWindows()
    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()