import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import cv2


class EdgeDetector(Node):

    def __init__(self):
        super().__init__('edge_detector')

        self.bridge = CvBridge()

        self.declare_parameter('threshold1', 100)
        self.declare_parameter('threshold2', 200)

        self.threshold1 = self.get_parameter('threshold1').value
        self.threshold2 = self.get_parameter('threshold2').value

        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        self.publisher = self.create_publisher(
            Image,
            '/camera/edges',
            10
        )

        self.get_logger().info(
            f"Edge detector started (threshold1={self.threshold1}, threshold2={self.threshold2})"
        )

    def image_callback(self, msg):

        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(gray, self.threshold1, self.threshold2)

        edge_msg = self.bridge.cv2_to_imgmsg(edges, encoding='8UC1')

        self.publisher.publish(edge_msg)


def main(args=None):

    rclpy.init(args=args)

    node = EdgeDetector()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()