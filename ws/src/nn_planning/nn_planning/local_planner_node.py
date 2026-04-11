#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped, Twist


class LocalPlannerNode(Node):
    def __init__(self):
        super().__init__('local_planner_node')

        self.declare_parameter('max_linear', 0.5)
        self.declare_parameter('max_angular', 1.0)
        self.declare_parameter('k_linear', 0.6)
        self.declare_parameter('k_angular', 1.2)
        self.declare_parameter('goal_tolerance', 0.05)

        self.max_linear = float(self.get_parameter('max_linear').value)
        self.max_angular = float(self.get_parameter('max_angular').value)
        self.k_linear = float(self.get_parameter('k_linear').value)
        self.k_angular = float(self.get_parameter('k_angular').value)
        self.goal_tolerance = float(self.get_parameter('goal_tolerance').value)

        self.goal_sub = self.create_subscription(
            PoseStamped,
            '/planning/goal',
            self.goal_callback,
            10
        )

        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.get_logger().info(
            'Local planner node started. '
            'Subscribed to /planning/goal, publishing /cmd_vel'
        )

        self.get_logger().info(
            f'Params: max_linear={self.max_linear:.2f}, '
            f'max_angular={self.max_angular:.2f}, '
            f'k_linear={self.k_linear:.2f}, '
            f'k_angular={self.k_angular:.2f}, '
            f'goal_tolerance={self.goal_tolerance:.2f}'
        )

    def goal_callback(self, msg: PoseStamped):
        gx = msg.pose.position.x
        gy = msg.pose.position.y

        distance = math.hypot(gx, gy)
        heading = math.atan2(gy, gx)

        cmd = Twist()

        if distance < self.goal_tolerance:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            self.get_logger().info('Goal is very close. Publishing stop command.')
        else:
            cmd.linear.x = min(self.k_linear * distance, self.max_linear)
            cmd.angular.z = max(-self.max_angular, min(self.k_angular * heading, self.max_angular))

            self.get_logger().info(
                f'Goal received x={gx:.2f}, y={gy:.2f} | '
                f'cmd_vel linear={cmd.linear.x:.2f}, angular={cmd.angular.z:.2f}'
            )

        self.cmd_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = LocalPlannerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
