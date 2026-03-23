import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Imu, Image
from std_msgs.msg import Float32

from cv_bridge import CvBridge
import numpy as np


class ImuVisionFusionNode(Node):
    def __init__(self):
        super().__init__('imu_vision_fusion_node')

        self.bridge = CvBridge()

        self.imu_value = 0.0
        self.vision_value = 0.0
        self.alpha = 0.6

        self.imu_sub = self.create_subscription(
            Imu,
            '/imu/data',
            self.imu_callback,
            10
        )

        self.image_sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        self.fusion_pub = self.create_publisher(Float32, '/fusion/state', 10)

        self.get_logger().info('IMU + Vision Fusion Node Started')

    def imu_callback(self, msg: Imu):
        self.imu_value = msg.angular_velocity.z

    def image_callback(self, msg: Image):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            self.vision_value = float(np.mean(cv_image))

            fused_value = self.alpha * self.vision_value + (1.0 - self.alpha) * self.imu_value

            fused_msg = Float32()
            fused_msg.data = fused_value
            self.fusion_pub.publish(fused_msg)

            self.get_logger().info(
                f'IMU: {self.imu_value:.3f}, Vision: {self.vision_value:.3f}, Fused: {fused_value:.3f}'
            )

        except Exception as e:
            self.get_logger().error(f'Failed to process image: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = ImuVisionFusionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()