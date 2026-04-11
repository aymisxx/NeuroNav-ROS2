#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_msgs.msg import String


class StressTestNode(Node):
    def __init__(self):
        super().__init__('stress_test_node')

        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.status_pub = self.create_publisher(
            String,
            '/stress_status',
            10
        )

        self.total_steps = 20
        self.step = 0

        self.timer = self.create_timer(0.1, self.run_stress_test)

        self.get_logger().info(
            'Stress test node started. Publishing burst commands on /cmd_vel and summary on /stress_status'
        )

    def run_stress_test(self):
        if self.step < self.total_steps:
            cmd = Twist()
            cmd.linear.x = 0.2 + 0.05 * math.sin(self.step)
            cmd.angular.z = 0.4 * math.cos(self.step)
            self.cmd_pub.publish(cmd)
            self.step += 1
            return

        status = String()
        status.data = f'COMPLETE: published {self.total_steps} commands'
        self.status_pub.publish(status)
        self.get_logger().info(status.data)
        self.timer.cancel()

def main(args=None):
    rclpy.init(args=args)
    node = StressTestNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
