#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid
from example_interfaces.srv import AddTwoInts


class MapQueryService(Node):
    def __init__(self):
        super().__init__('map_query_service')

        self.latest_map = None

        self.create_subscription(
            OccupancyGrid,
            '/semantic_map',
            self.map_callback,
            10
        )

        self.create_service(
            AddTwoInts,
            '/query_semantic_map',
            self.handle_query
        )

        self.get_logger().info(
            'Map query service started. Service: /query_semantic_map | Input: x=a, y=b'
        )

    def map_callback(self, msg):
        self.latest_map = msg

    def handle_query(self, request, response):
        x = int(request.a)
        y = int(request.b)

        if self.latest_map is None:
            response.sum = -1
            self.get_logger().warn('No semantic map received yet.')
            return response

        width = self.latest_map.info.width
        height = self.latest_map.info.height

        if x < 0 or x >= width or y < 0 or y >= height:
            response.sum = -2
            self.get_logger().warn(f'Out-of-bounds query: ({x}, {y})')
            return response

        idx = y * width + x
        response.sum = int(self.latest_map.data[idx])
        self.get_logger().info(f'Query ({x}, {y}) -> value={response.sum}')
        return response


def main(args=None):
    rclpy.init(args=args)
    node = MapQueryService()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
