#!/usr/bin/env python3

from pathlib import Path

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class FinalReleaseNode(Node):
    def __init__(self):
        super().__init__('final_release_node')

        self.release_pub = self.create_publisher(
            String,
            '/release_status',
            10
        )

        self.summary_path = Path('/tmp/day55_release_summary.txt')
        self.timer = self.create_timer(1.0, self.publish_release)

        self.published = False

        self.get_logger().info(
            'Final release node started. Publishing /release_status and writing final summary.'
        )

    def publish_release(self):
        if self.published:
            return

        msg = String()
        msg.data = 'RELEASE_READY'
        self.release_pub.publish(msg)

        text = (
            'Day 55 Final Release Summary\n'
            'project: NeuroNav-ROS2\n'
            'status: RELEASE_READY\n'
            'phase_1: completed\n'
            'phase_2: completed\n'
            'phase_3: completed\n'
            'phase_4: completed\n'
            'final_day: 55\n'
        )
        self.summary_path.write_text(text)

        self.get_logger().info(f'Published release status: {msg.data}')
        self.get_logger().info(f'Wrote final release summary to {self.summary_path}')

        self.published = True


def main(args=None):
    rclpy.init(args=args)
    node = FinalReleaseNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
