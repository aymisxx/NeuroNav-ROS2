#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Pose2D
from std_msgs.msg import String


class TestAutomationNode(Node):
    def __init__(self):
        super().__init__('test_automation_node')

        self.pose_pub = self.create_publisher(
            Pose2D,
            '/sim_pose',
            10
        )

        self.behavior_sub = self.create_subscription(
            String,
            '/behavior_state',
            self.behavior_callback,
            10
        )

        self.test_pub = self.create_publisher(
            String,
            '/test_status',
            10
        )

        self.expected_state = 'CRUISE'
        self.test_sent = False
        self.test_done = False

        self.timer = self.create_timer(1.0, self.run_test)

        self.get_logger().info(
            'Test automation node started. '
            'Publishing /sim_pose, listening to /behavior_state, publishing /test_status'
        )

    def run_test(self):
        if self.test_sent:
            return

        pose = Pose2D()
        pose.x = 0.6
        pose.y = 0.2
        pose.theta = 0.0

        self.pose_pub.publish(pose)
        self.test_sent = True

        self.get_logger().info(
            f'Sent test pose x={pose.x:.2f}, y={pose.y:.2f}, expecting state={self.expected_state}'
        )

    def behavior_callback(self, msg: String):
        if self.test_done or not self.test_sent:
            return

        result = String()
        if msg.data == self.expected_state:
            result.data = 'PASS'
        else:
            result.data = f'FAIL (expected {self.expected_state}, got {msg.data})'

        self.test_pub.publish(result)
        self.test_done = True

        self.get_logger().info(f'Test result: {result.data}')


def main(args=None):
    rclpy.init(args=args)
    node = TestAutomationNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
