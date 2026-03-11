import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import cv2


class ORBFeatures(Node):

    def __init__(self):
        super().__init__('orb_features')

        self.bridge = CvBridge()

        self.orb = cv2.ORB_create(nfeatures=500)

        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        self.publisher = self.create_publisher(
            Image,
            '/camera/orb_features',
            10
        )

        self.get_logger().info("ORB feature detector started")

    def image_callback(self, msg):

        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        keypoints, descriptors = self.orb.detectAndCompute(gray, None)

        output = cv2.drawKeypoints(
            frame,
            keypoints,
            None,
            color=(0,255,0),
            flags=0
        )

        feature_msg = self.bridge.cv2_to_imgmsg(output, encoding='bgr8')

        self.publisher.publish(feature_msg)


def main(args=None):

    rclpy.init(args=args)

    node = ORBFeatures()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()