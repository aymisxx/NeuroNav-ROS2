#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class LifecycleManagerNode(Node):
    def __init__(self):
        super().__init__('lifecycle_manager_node')

        self.state_pub = self.create_publisher(
            String,
            '/lifecycle_state',
            10
        )

        self.states = ['unconfigured', 'inactive', 'active']
        self.index = 0

        self.timer = self.create_timer(2.0, self.publish_state)

        self.get_logger().info(
            'Lifecycle manager node started. Publishing /lifecycle_state'
        )

    def publish_state(self):
        msg = String()
        msg.data = self.states[self.index]
        self.state_pub.publish(msg)

        self.get_logger().info(f'Published lifecycle state: {msg.data}')

        if self.index < len(self.states) - 1:
            self.index += 1


def main(args=None):
    rclpy.init(args=args)
    node = LifecycleManagerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
