#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped


class LanguageGoalNode(Node):
    def __init__(self):
        super().__init__('language_goal_node')

        self.goal_pub = self.create_publisher(PoseStamped, '/language_goal', 10)

        self.goal_dict = {
            'plant': (2.0, 1.0),
            'chair': (4.0, 2.0),
            'table': (6.0, 3.0),
        }

        self.create_subscription(
            String,
            '/language_query',
            self.query_callback,
            10
        )

        self.get_logger().info(
            'Language goal node started. Subscribed to /language_query, publishing /language_goal'
        )

    def query_callback(self, msg):
        label = msg.data.strip().lower()

        if label not in self.goal_dict:
            self.get_logger().warn(f'Unknown label: {label}')
            return

        x, y = self.goal_dict[label]

        goal = PoseStamped()
        goal.header.stamp = self.get_clock().now().to_msg()
        goal.header.frame_id = 'map'
        goal.pose.position.x = x
        goal.pose.position.y = y
        goal.pose.orientation.w = 1.0

        self.goal_pub.publish(goal)
        self.get_logger().info(f'Language query "{label}" -> goal ({x}, {y})')


def main(args=None):
    rclpy.init(args=args)
    node = LanguageGoalNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
