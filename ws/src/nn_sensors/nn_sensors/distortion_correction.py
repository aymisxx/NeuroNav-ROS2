import os
import yaml
import cv2
import numpy as np

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from ament_index_python.packages import get_package_share_directory


class DistortionCorrectionNode(Node):
    def __init__(self):
        super().__init__('distortion_correction_node')

        self.bridge = CvBridge()

        self.declare_parameter('input_topic', '/camera/image_raw')
        self.declare_parameter('output_topic', '/camera/image_rect')

        input_topic = self.get_parameter('input_topic').get_parameter_value().string_value
        output_topic = self.get_parameter('output_topic').get_parameter_value().string_value

        calib_file = os.path.join(
            get_package_share_directory('nn_sensors'),
            'ost.yaml'
        )

        self.camera_matrix, self.dist_coeffs = self.load_calibration(calib_file)

        self.subscription = self.create_subscription(
            Image,
            input_topic,
            self.image_callback,
            10
        )

        self.publisher = self.create_publisher(Image, output_topic, 10)

        self.get_logger().info(f'Subscribed to: {input_topic}')
        self.get_logger().info(f'Publishing undistorted images to: {output_topic}')
        self.get_logger().info(f'Loaded calibration from: {calib_file}')

    def load_calibration(self, calib_file):
        if not os.path.exists(calib_file):
            raise FileNotFoundError(f'Calibration file not found: {calib_file}')

        with open(calib_file, 'r') as f:
            data = yaml.safe_load(f)

        camera_matrix = np.array(
            data['camera_matrix']['data'],
            dtype=np.float64
        ).reshape(3, 3)

        dist_coeffs = np.array(
            data['distortion_coefficients']['data'],
            dtype=np.float64
        )

        return camera_matrix, dist_coeffs

    def image_callback(self, msg):
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            undistorted = cv2.undistort(frame, self.camera_matrix, self.dist_coeffs)

            out_msg = self.bridge.cv2_to_imgmsg(undistorted, encoding='bgr8')
            out_msg.header = msg.header
            self.publisher.publish(out_msg)

        except Exception as e:
            self.get_logger().error(f'Failed to process image: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = DistortionCorrectionNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()