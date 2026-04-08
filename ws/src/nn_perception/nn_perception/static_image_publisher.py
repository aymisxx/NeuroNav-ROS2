from pathlib import Path

import cv2
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image


class StaticImagePublisher(Node):
    def __init__(self):
        super().__init__('static_image_publisher')

        self.bridge = CvBridge()
        self.publisher_ = self.create_publisher(Image, '/camera/image_raw', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)

        self.image_path = Path.home() / 'GitHub' / 'NeuroNav-ROS2' / 'assets' / 'day02_camera_stream.png'
        self.frame = cv2.imread(str(self.image_path))

        if self.frame is None:
            self.get_logger().error(f'Failed to load image: {self.image_path}')
            raise RuntimeError(f'Could not load image: {self.image_path}')

        self.get_logger().info(f'Loaded image: {self.image_path}')
        self.get_logger().info('Publishing static image to: /camera/image_raw')

    def timer_callback(self):
        msg = self.bridge.cv2_to_imgmsg(self.frame, encoding='bgr8')
        self.publisher_.publish(msg)
        self.get_logger().info('Published static image frame')


def main(args=None):
    rclpy.init(args=args)
    node = StaticImagePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()