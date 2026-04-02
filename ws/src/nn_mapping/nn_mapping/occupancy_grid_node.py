import rclpy
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid
from std_msgs.msg import Header


class OccupancyGridNode(Node):
    def __init__(self):
        super().__init__('occupancy_grid_node')
        self.pub = self.create_publisher(OccupancyGrid, '/map', 10)
        self.timer = self.create_timer(1.0, self.publish_map)

    def publish_map(self):
        msg = OccupancyGrid()
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'map'

        msg.info.resolution = 1.0
        msg.info.width = 5
        msg.info.height = 5
        msg.info.origin.position.x = 0.0
        msg.info.origin.position.y = 0.0
        msg.info.origin.orientation.w = 1.0

        msg.data = [
            0, 0, 0, 0, 0,
            0, 100, 100, 0, 0,
            0, 0, -1, 0, 0,
            0, 100, 0, 0, 0,
            0, 0, 0, 0, 0,
        ]

        self.pub.publish(msg)
        self.get_logger().info('Published toy occupancy grid')

def main(args=None):
    rclpy.init(args=args)
    node = OccupancyGridNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
