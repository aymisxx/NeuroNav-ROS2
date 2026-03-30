import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Vector3


class DriftAnalysisNode(Node):
    def __init__(self):
        super().__init__('drift_analysis_node')

        self.sample_count = 0
        self.max_drift = 0.0

        self.pose_sub = self.create_subscription(
            Vector3,
            '/vo_pose',
            self.pose_callback,
            10
        )

        self.get_logger().info('Drift Analysis Node Started')

    def pose_callback(self, msg: Vector3) -> None:
        self.sample_count += 1

        drift = math.sqrt((msg.x ** 2) + (msg.y ** 2))
        self.max_drift = max(self.max_drift, drift)

        self.get_logger().info(
            f'Drift sample {self.sample_count}: '
            f'x={msg.x:.2f}, y={msg.y:.2f}, '
            f'drift={drift:.2f}, max_drift={self.max_drift:.2f}, '
            f'cumulative_motion={msg.z:.2f}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = DriftAnalysisNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
