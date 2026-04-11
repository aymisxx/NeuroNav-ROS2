#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node

from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import PoseStamped


class PerceptionToPlanningNode(Node):
    def __init__(self):
        super().__init__('perception_to_planning_node')

        self.map_sub = self.create_subscription(
            OccupancyGrid,
            '/semantic_map',
            self.map_callback,
            10
        )

        self.goal_pub = self.create_publisher(
            PoseStamped,
            '/planning/goal',
            10
        )

        self.get_logger().info(
            'Perception-to-planning node started. '
            'Subscribed to /semantic_map, publishing /planning/goal'
        )

    def map_callback(self, msg: OccupancyGrid):
        width = msg.info.width
        height = msg.info.height
        resolution = msg.info.resolution
        origin_x = msg.info.origin.position.x
        origin_y = msg.info.origin.position.y

        if width == 0 or height == 0 or len(msg.data) == 0:
            self.get_logger().warn('Received empty semantic map.')
            return

        best_index = None
        best_score = -math.inf

        center_x = width / 2.0
        center_y = height / 2.0

        for idx, value in enumerate(msg.data):
            if value <= 0:
                continue

            x = idx % width
            y = idx // width

            dist_to_center = math.hypot(x - center_x, y - center_y)
            score = float(value) - 0.05 * dist_to_center

            if score > best_score:
                best_score = score
                best_index = idx

        if best_index is None:
            self.get_logger().warn('No valid target found in semantic map.')
            return

        cell_x = best_index % width
        cell_y = best_index // width

        world_x = origin_x + (cell_x + 0.5) * resolution
        world_y = origin_y + (cell_y + 0.5) * resolution

        goal = PoseStamped()
        goal.header.stamp = self.get_clock().now().to_msg()
        goal.header.frame_id = 'map'

        goal.pose.position.x = world_x
        goal.pose.position.y = world_y
        goal.pose.position.z = 0.0
        goal.pose.orientation.w = 1.0

        self.goal_pub.publish(goal)

        self.get_logger().info(
            f'Published planning goal at x={world_x:.2f}, y={world_y:.2f}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = PerceptionToPlanningNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
