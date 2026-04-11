#!/usr/bin/env python3

import math
from pathlib import Path

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist, Pose2D


class NavigationSimNode(Node):
    def __init__(self):
        super().__init__('navigation_sim_node')

        self.cmd_sub = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_callback,
            10
        )

        self.pose_pub = self.create_publisher(
            Pose2D,
            '/sim_pose',
            10
        )

        self.dt = 0.1
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.v = 0.0
        self.w = 0.0

        self.traj_file = Path('/tmp/day44_sim_traj.csv')
        self.traj_file.write_text('t,x,y,theta\n')
        self.sim_time = 0.0

        self.timer = self.create_timer(self.dt, self.update_sim)

        self.get_logger().info(
            'Navigation sim node started. '
            'Subscribed to /cmd_vel, publishing /sim_pose'
        )

    def cmd_callback(self, msg: Twist):
        self.v = float(msg.linear.x)
        self.w = float(msg.angular.z)

        self.get_logger().info(
            f'Received cmd_vel linear={self.v:.2f}, angular={self.w:.2f}'
        )

    def update_sim(self):
        self.theta += self.w * self.dt
        self.x += self.v * math.cos(self.theta) * self.dt
        self.y += self.v * math.sin(self.theta) * self.dt
        self.sim_time += self.dt

        pose = Pose2D()
        pose.x = self.x
        pose.y = self.y
        pose.theta = self.theta
        self.pose_pub.publish(pose)

        with self.traj_file.open('a') as f:
            f.write(f'{self.sim_time:.2f},{self.x:.4f},{self.y:.4f},{self.theta:.4f}\n')


def main(args=None):
    rclpy.init(args=args)
    node = NavigationSimNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
