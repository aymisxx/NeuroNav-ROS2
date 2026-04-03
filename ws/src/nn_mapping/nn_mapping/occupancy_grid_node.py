import rclpy
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid
from std_msgs.msg import Header


class OccupancyGridNode(Node):
    def __init__(self):
        super().__init__('occupancy_grid_node')
        self.pub = self.create_publisher(OccupancyGrid, '/map', 10)
        self.timer = self.create_timer(1.0, self.publish_map)

        self.width = 5
        self.height = 5
        self.step = 0

    def make_grid(self):
        data = [0] * (self.width * self.height)

        obstacles = [
            (1, 1),
            (2, 1),
            (1, 3),
        ]
        for x, y in obstacles:
            data[y * self.width + x] = 100

        moving_x = self.step % self.width
        moving_y = 2
        data[moving_y * self.width + moving_x] = -1

        return data

    def publish_map(self):
        msg = OccupancyGrid()
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'map'

        msg.info.resolution = 1.0
        msg.info.width = self.width
        msg.info.height = self.height
        msg.info.origin.position.x = 0.0
        msg.info.origin.position.y = 0.0
        msg.info.origin.orientation.w = 1.0

        msg.data = self.make_grid()

        self.pub.publish(msg)
        self.get_logger().info(f'Published updated occupancy grid step={self.step}')
        self.step += 1


def main(args=None):
    rclpy.init(args=args)
    node = OccupancyGridNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()