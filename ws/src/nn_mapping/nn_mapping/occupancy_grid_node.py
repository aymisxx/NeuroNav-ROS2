import math

import rclpy
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Header


class OccupancyGridNode(Node):
    def __init__(self):
        super().__init__('occupancy_grid_node')

        self.map_pub = self.create_publisher(OccupancyGrid, '/map', 10)
        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan_processed',
            self.scan_callback,
            10
        )

        self.width = 20
        self.height = 20
        self.resolution = 0.5
        self.origin_x = -(self.width * self.resolution) / 2.0
        self.origin_y = -(self.height * self.resolution) / 2.0

        self.get_logger().info(
            'Occupancy grid node started. Subscribed to /scan_processed, publishing /map'
        )

    def world_to_grid(self, x: float, y: float):
        gx = int((x - self.origin_x) / self.resolution)
        gy = int((y - self.origin_y) / self.resolution)
        return gx, gy

    def scan_callback(self, msg: LaserScan):
        data = [0] * (self.width * self.height)
        occupied_cells = 0

        angle = msg.angle_min
        for r in msg.ranges:
            if math.isfinite(r) and msg.range_min <= r <= msg.range_max:
                x = r * math.cos(angle)
                y = r * math.sin(angle)

                gx, gy = self.world_to_grid(x, y)

                if 0 <= gx < self.width and 0 <= gy < self.height:
                    idx = gy * self.width + gx
                    if data[idx] != 100:
                        data[idx] = 100
                        occupied_cells += 1

            angle += msg.angle_increment

        occ_msg = OccupancyGrid()
        occ_msg.header = Header()
        occ_msg.header.stamp = self.get_clock().now().to_msg()
        occ_msg.header.frame_id = 'map'

        occ_msg.info.resolution = self.resolution
        occ_msg.info.width = self.width
        occ_msg.info.height = self.height
        occ_msg.info.origin.position.x = self.origin_x
        occ_msg.info.origin.position.y = self.origin_y
        occ_msg.info.origin.orientation.w = 1.0

        occ_msg.data = data

        self.map_pub.publish(occ_msg)
        self.get_logger().info(
            f'Published occupancy grid from scan | occupied_cells={occupied_cells}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = OccupancyGridNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()