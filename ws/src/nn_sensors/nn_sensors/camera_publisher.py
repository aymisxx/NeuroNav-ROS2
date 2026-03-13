import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge

import cv2


class CameraPublisher(Node):

    def __init__(self):
        super().__init__('camera_publisher')

        self.image_publisher_ = self.create_publisher(Image, '/camera/image_raw', 10)
        self.camera_info_publisher_ = self.create_publisher(CameraInfo, '/camera/camera_info', 10)

        self.timer = self.create_timer(0.1, self.timer_callback)

        self.cap = cv2.VideoCapture(0)

        self.bridge = CvBridge()

        self.width = 640
        self.height = 480

    def timer_callback(self):

        ret, frame = self.cap.read()

        if ret:
            frame = cv2.resize(frame, (self.width, self.height))

            stamp = self.get_clock().now().to_msg()

            img_msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            img_msg.header.stamp = stamp
            img_msg.header.frame_id = "camera_link"

            cam_info_msg = CameraInfo()
            cam_info_msg.header.stamp = stamp
            cam_info_msg.header.frame_id = "camera_link"
            cam_info_msg.height = self.height
            cam_info_msg.width = self.width
            cam_info_msg.distortion_model = "plumb_bob"
            cam_info_msg.d = [0.0, 0.0, 0.0, 0.0, 0.0]

            cam_info_msg.k = [
                525.0, 0.0, 320.0,
                0.0, 525.0, 240.0,
                0.0, 0.0, 1.0
            ]

            cam_info_msg.r = [
                1.0, 0.0, 0.0,
                0.0, 1.0, 0.0,
                0.0, 0.0, 1.0
            ]

            cam_info_msg.p = [
                525.0, 0.0, 320.0, 0.0,
                0.0, 525.0, 240.0, 0.0,
                0.0, 0.0, 1.0, 0.0
            ]

            self.image_publisher_.publish(img_msg)
            self.camera_info_publisher_.publish(cam_info_msg)

            self.get_logger().info("Publishing camera frame and camera info")


def main(args=None):

    rclpy.init(args=args)

    node = CameraPublisher()

    rclpy.spin(node)

    node.cap.release()

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()