#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_msgs.msg import String


class DiagnosticsLoggerNode(Node):
    def __init__(self):
        super().__init__('diagnostics_logger_node')

        self.cmd_sub = self.create_subscription(
            Twist,
            '/cmd_vel_safe',
            self.cmd_callback,
            10
        )

        self.diag_pub = self.create_publisher(
            String,
            '/diagnostics_status',
            10
        )

        self.get_logger().info(
            'Diagnostics logger node started. '
            'Subscribed to /cmd_vel_safe, publishing /diagnostics_status'
        )

    def cmd_callback(self, msg: Twist):
        linear = abs(msg.linear.x)
        angular = abs(msg.angular.z)

        status = String()

        if linear >= 0.25 or angular >= 0.80:
            status.data = 'ALERT'
        elif linear >= 0.15 or angular >= 0.50:
            status.data = 'WARN'
        else:
            status.data = 'OK'

        self.diag_pub.publish(status)

        self.get_logger().info(
            f'Diagnostics: linear={linear:.2f}, angular={angular:.2f} -> {status.data}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = DiagnosticsLoggerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
