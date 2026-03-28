import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from geometry_msgs.msg import Vector3
from cv_bridge import CvBridge

import cv2
import numpy as np


class VisualOdometryNode(Node):
    def __init__(self):
        super().__init__('visual_odometry_node')

        self.bridge = CvBridge()
        self.orb = cv2.ORB_create(nfeatures=500)
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        self.prev_keypoints = None
        self.prev_descriptors = None
        self.frame_count = 0

        self.image_sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        self.vo_pub = self.create_publisher(Vector3, '/vo_delta', 10)

        self.get_logger().info('Visual Odometry Node Started')

    def image_callback(self, msg: Image) -> None:
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f'cv_bridge conversion failed: {e}')
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        keypoints, descriptors = self.orb.detectAndCompute(gray, None)
        self.frame_count += 1

        num_keypoints = 0 if keypoints is None else len(keypoints)

        if (
            self.prev_descriptors is not None
            and descriptors is not None
            and self.prev_keypoints is not None
            and keypoints is not None
            and len(self.prev_descriptors) > 0
            and len(descriptors) > 0
        ):
            matches = self.bf.match(self.prev_descriptors, descriptors)
            matches = sorted(matches, key=lambda m: m.distance)

            good_matches = [m for m in matches if m.distance < 50]
            num_matches = len(good_matches)

            if num_matches >= 8:
                prev_pts = np.float32(
                    [self.prev_keypoints[m.queryIdx].pt for m in good_matches]
                )
                curr_pts = np.float32(
                    [keypoints[m.trainIdx].pt for m in good_matches]
                )

                displacements = curr_pts - prev_pts
                mean_dx = float(np.mean(displacements[:, 0]))
                mean_dy = float(np.mean(displacements[:, 1]))
                mean_pixel_motion = float(
                    np.mean(np.linalg.norm(displacements, axis=1))
                )
            else:
                mean_dx = 0.0
                mean_dy = 0.0
                mean_pixel_motion = 0.0

            vo_msg = Vector3()
            vo_msg.x = mean_dx
            vo_msg.y = mean_dy
            vo_msg.z = mean_pixel_motion
            self.vo_pub.publish(vo_msg)

            self.get_logger().info(
                f'Frame {self.frame_count}: keypoints={num_keypoints}, '
                f'good_matches={num_matches}, '
                f'mean_dx={mean_dx:.2f}, mean_dy={mean_dy:.2f}, '
                f'mean_pixel_motion={mean_pixel_motion:.2f}'
            )
        else:
            self.get_logger().info(
                f'Frame {self.frame_count}: keypoints={num_keypoints}, waiting_for_previous_frame'
            )

        self.prev_keypoints = keypoints
        self.prev_descriptors = descriptors


def main(args=None):
    rclpy.init(args=args)
    node = VisualOdometryNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
