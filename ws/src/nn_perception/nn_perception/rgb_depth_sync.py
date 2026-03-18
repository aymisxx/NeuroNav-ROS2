import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from message_filters import Subscriber, ApproximateTimeSynchronizer

import numpy as np


class RGBDepthSync(Node):
    def __init__(self):
        super().__init__('rgb_depth_sync')

        self.bridge = CvBridge()

        self.rgb_sub = Subscriber(self, Image, '/camera/image_raw')
        self.depth_sub = Subscriber(self, Image, '/camera/depth/image_raw')

        self.sync = ApproximateTimeSynchronizer(
            [self.rgb_sub, self.depth_sub],
            queue_size=10,
            slop=0.1
        )
        self.sync.registerCallback(self.sync_callback)

        self.get_logger().info(
            'RGB-Depth sync node started. Waiting for synchronized frames...'
        )

    def sync_callback(self, rgb_msg: Image, depth_msg: Image):
        try:
            rgb_image = self.bridge.imgmsg_to_cv2(
                rgb_msg,
                desired_encoding='bgr8'
            )
            depth_image = self.bridge.imgmsg_to_cv2(
                depth_msg,
                desired_encoding='32FC1'
            )

            rgb_h, rgb_w = rgb_image.shape[:2]
            depth_h, depth_w = depth_image.shape[:2]

            depth_min = float(np.min(depth_image))
            depth_max = float(np.max(depth_image))
            depth_mean = float(np.mean(depth_image))

            self.get_logger().info(
                f'SYNC OK | '
                f'RGB: {rgb_w}x{rgb_h} | '
                f'Depth: {depth_w}x{depth_h} | '
                f'Depth[min={depth_min:.2f}, mean={depth_mean:.2f}, max={depth_max:.2f}] | '
                f'RGB stamp={rgb_msg.header.stamp.sec}.{rgb_msg.header.stamp.nanosec:09d} | '
                f'Depth stamp={depth_msg.header.stamp.sec}.{depth_msg.header.stamp.nanosec:09d}'
            )

        except Exception as e:
            self.get_logger().error(f'Failed in sync callback: {e}')


def main(args=None):
    rclpy.init(args=args)

    node = RGBDepthSync()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()