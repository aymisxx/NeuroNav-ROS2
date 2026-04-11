#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Pose2D
from std_msgs.msg import String


class BehaviorLogicNode(Node):
    def __init__(self):
        super().__init__('behavior_logic_node')

        self.pose_sub = self.create_subscription(
            Pose2D,
            '/sim_pose',
            self.pose_callback,
            10
        )

        self.state_pub = self.create_publisher(
            String,
            '/behavior_state',
            10
        )

        self.idle_radius = 0.20
        self.cruise_radius = 1.00

        self.get_logger().info(
            'Behavior logic node started. '
            'Subscribed to /sim_pose, publishing /behavior_state'
        )

    def pose_callback(self, msg: Pose2D):
        r = math.hypot(msg.x, msg.y)

        state = String()
        if r < self.idle_radius:
            state.data = 'IDLE'
        elif r < self.cruise_radius:
            state.data = 'CRUISE'
        else:
            state.data = 'RECOVER'

        self.state_pub.publish(state)

        self.get_logger().info(
            f'sim_pose x={msg.x:.2f}, y={msg.y:.2f}, r={r:.2f} -> state={state.data}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = BehaviorLogicNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
