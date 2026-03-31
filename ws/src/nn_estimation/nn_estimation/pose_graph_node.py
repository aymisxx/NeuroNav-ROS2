import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Vector3


class PoseGraphNode(Node):
    def __init__(self):
        super().__init__('pose_graph_node')

        self.pose_count = 0
        self.graph_nodes = []
        self.graph_edges = []
        self.last_graph_node_id = None

        self.node_stride = 5
        self.min_distance = 2.0

        self.pose_sub = self.create_subscription(
            Vector3,
            '/vo_pose',
            self.pose_callback,
            10
        )

        self.get_logger().info('Pose Graph Node Started')

    def pose_callback(self, msg: Vector3) -> None:
        self.pose_count += 1

        current_x = msg.x
        current_y = msg.y
        current_motion = msg.z

        if self.pose_count % self.node_stride != 0:
            return

        if self.graph_nodes:
            last_node = self.graph_nodes[-1]
            dx = current_x - last_node['x']
            dy = current_y - last_node['y']
            distance = math.sqrt(dx * dx + dy * dy)

            if distance < self.min_distance:
                self.get_logger().info(
                    f'Pose sample {self.pose_count}: '
                    f'graph node skipped, distance={distance:.2f} < '
                    f'{self.min_distance:.2f}'
                )
                return

        new_node_id = len(self.graph_nodes)

        self.graph_nodes.append({
            'id': new_node_id,
            'x': current_x,
            'y': current_y,
            'motion': current_motion,
        })

        if self.last_graph_node_id is not None:
            self.graph_edges.append({
                'from': self.last_graph_node_id,
                'to': new_node_id,
            })

            self.get_logger().info(
                f'Edge added: {self.last_graph_node_id} -> {new_node_id}'
            )

        self.last_graph_node_id = new_node_id

        self.get_logger().info(
            f'Graph node {new_node_id} added at '
            f'x={current_x:.2f}, y={current_y:.2f}, '
            f'cumulative_motion={current_motion:.2f} | '
            f'total_nodes={len(self.graph_nodes)}, '
            f'total_edges={len(self.graph_edges)}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = PoseGraphNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()