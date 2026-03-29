import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Vector3


class PoseChainingNode(Node):
    def __init__(self):
        super().__init__('pose_chaining_node')

        self.x = 0.0
        self.y = 0.0
        self.total_motion = 0.0
        self.sample_count = 0

        self.delta_sub = self.create_subscription(
            Vector3,
            '/vo_delta',
            self.delta_callback,
            10
        )

        self.pose_pub = self.create_publisher(Vector3, '/vo_pose', 10)

        self.get_logger().info('Pose Chaining Node Started')

    def delta_callback(self, msg: Vector3) -> None:
        self.x += msg.x
        self.y += msg.y
        self.total_motion += msg.z
        self.sample_count += 1

        pose_msg = Vector3()
        pose_msg.x = self.x
        pose_msg.y = self.y
        pose_msg.z = self.total_motion
        self.pose_pub.publish(pose_msg)

        self.get_logger().info(
            f'Pose sample {self.sample_count}: '
            f'x={self.x:.2f}, y={self.y:.2f}, '
            f'cumulative_motion={self.total_motion:.2f}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = PoseChainingNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
