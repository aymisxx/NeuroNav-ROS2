#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist


class SafetyLayerNode(Node):
    def __init__(self):
        super().__init__('safety_layer_node')

        self.cmd_sub = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_callback,
            10
        )

        self.safe_pub = self.create_publisher(
            Twist,
            '/cmd_vel_safe',
            10
        )

        self.max_linear = 0.25
        self.max_angular = 0.80

        self.get_logger().info(
            'Safety layer node started. '
            'Subscribed to /cmd_vel, publishing /cmd_vel_safe'
        )

    def clamp(self, value, limit):
        return max(-limit, min(value, limit))

    def cmd_callback(self, msg: Twist):
        safe = Twist()

        safe.linear.x = self.clamp(msg.linear.x, self.max_linear)
        safe.angular.z = self.clamp(msg.angular.z, self.max_angular)

        self.safe_pub.publish(safe)

        self.get_logger().info(
            f'Input cmd_vel linear={msg.linear.x:.2f}, angular={msg.angular.z:.2f} | '
            f'Safe cmd_vel linear={safe.linear.x:.2f}, angular={safe.angular.z:.2f}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = SafetyLayerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
