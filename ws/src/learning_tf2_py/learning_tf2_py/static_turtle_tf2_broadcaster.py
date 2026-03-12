import math

from geometry_msgs.msg import TransformStamped
import rclpy
from rclpy.node import Node
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster


def quaternion_from_euler(ai, aj, ak):
    ai /= 2.0
    aj /= 2.0
    ak /= 2.0

    ci = math.cos(ai)
    si = math.sin(ai)
    cj = math.cos(aj)
    sj = math.sin(aj)
    ck = math.cos(ak)
    sk = math.sin(ak)

    q = [0.0, 0.0, 0.0, 0.0]
    q[0] = si * cj * ck - ci * sj * sk
    q[1] = ci * sj * ck + si * cj * sk
    q[2] = ci * cj * sk - si * sj * ck
    q[3] = ci * cj * ck + si * sj * sk

    return q


class StaticFramePublisher(Node):

    def __init__(self):
        super().__init__('static_turtle_tf2_broadcaster')

        self._tf_publisher = StaticTransformBroadcaster(self)

        t = TransformStamped()

        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'world'
        t.child_frame_id = 'mystaticturtle'

        t.transform.translation.x = 1.0
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.0

        quat = quaternion_from_euler(0.0, 0.0, 0.0)
        t.transform.rotation.x = quat[0]
        t.transform.rotation.y = quat[1]
        t.transform.rotation.z = quat[2]
        t.transform.rotation.w = quat[3]

        self._tf_publisher.sendTransform(t)
        self.get_logger().info('Publishing static transform world -> mystaticturtle')


def main():
    rclpy.init()
    node = StaticFramePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    rclpy.shutdown()


if __name__ == '__main__':
    main()