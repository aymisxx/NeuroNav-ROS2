#!/usr/bin/env python3

from pathlib import Path

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Pose2D, PoseStamped, Twist
from std_msgs.msg import String


class DemoRecorderNode(Node):
    def __init__(self):
        super().__init__('demo_recorder_node')

        self.goal_count = 0
        self.cmd_count = 0
        self.pose_count = 0
        self.behavior_count = 0
        self.diagnostics_count = 0

        self.create_subscription(PoseStamped, '/planning/goal', self.goal_cb, 10)
        self.create_subscription(Twist, '/cmd_vel_safe', self.cmd_cb, 10)
        self.create_subscription(Pose2D, '/sim_pose', self.pose_cb, 10)
        self.create_subscription(String, '/behavior_state', self.behavior_cb, 10)
        self.create_subscription(String, '/diagnostics_status', self.diagnostics_cb, 10)

        self.summary_path = Path('/tmp/day53_demo_summary.txt')
        self.timer = self.create_timer(5.0, self.write_summary)

        self.get_logger().info(
            'Demo recorder node started. '
            'Recording counts from /planning/goal, /cmd_vel_safe, /sim_pose, '
            '/behavior_state, /diagnostics_status'
        )

    def goal_cb(self, _msg):
        self.goal_count += 1

    def cmd_cb(self, _msg):
        self.cmd_count += 1

    def pose_cb(self, _msg):
        self.pose_count += 1

    def behavior_cb(self, _msg):
        self.behavior_count += 1

    def diagnostics_cb(self, _msg):
        self.diagnostics_count += 1

    def write_summary(self):
        text = (
            'Day 53 Demo Summary\n'
            f'planning_goal_messages: {self.goal_count}\n'
            f'cmd_vel_safe_messages: {self.cmd_count}\n'
            f'sim_pose_messages: {self.pose_count}\n'
            f'behavior_state_messages: {self.behavior_count}\n'
            f'diagnostics_status_messages: {self.diagnostics_count}\n'
        )
        self.summary_path.write_text(text)
        self.get_logger().info(f'Wrote demo summary to {self.summary_path}')


def main(args=None):
    rclpy.init(args=args)
    node = DemoRecorderNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
