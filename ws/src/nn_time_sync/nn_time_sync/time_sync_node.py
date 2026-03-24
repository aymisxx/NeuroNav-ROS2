import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Imu, Image
from message_filters import Subscriber, ApproximateTimeSynchronizer


class TimeSyncNode(Node):

    def __init__(self):
        super().__init__('time_sync_node')

        self.get_logger().info('Approximate Time Sync Node Started')

        self.imu_sub = Subscriber(self, Imu, '/imu/data')
        self.image_sub = Subscriber(self, Image, '/camera/image_raw')

        self.sync = ApproximateTimeSynchronizer(
            [self.imu_sub, self.image_sub],
            queue_size=10,
            slop=0.1
        )
        self.sync.registerCallback(self.synced_callback)

    def synced_callback(self, imu_msg: Imu, image_msg: Image):
        imu_time = imu_msg.header.stamp.sec + imu_msg.header.stamp.nanosec * 1e-9
        image_time = image_msg.header.stamp.sec + image_msg.header.stamp.nanosec * 1e-9
        dt = abs(imu_time - image_time)

        if dt < 0.01:
            quality = 'EXCELLENT'
        elif dt < 0.03:
            quality = 'GOOD'
        elif dt < 0.05:
            quality = 'FAIR'
        else:
            quality = 'POOR'

        self.get_logger().info(
            f"[SYNCED] IMU Time: {imu_time:.6f}, "
            f"Image Time: {image_time:.6f}, "
            f"Delta: {dt:.6f} sec, "
            f"Quality: {quality}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = TimeSyncNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()