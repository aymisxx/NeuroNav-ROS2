#!/usr/bin/env python3

import cv2
import numpy as np

import rclpy
from rclpy.node import Node

from cv_bridge import CvBridge
from sensor_msgs.msg import Image

from .centroid_tracker import CentroidTracker


class ObjectTracker(Node):
    def __init__(self):
        super().__init__('object_tracker')

        self.bridge = CvBridge()
        self.ct = CentroidTracker(max_disappeared=10)

        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        self.get_logger().info(
            'Object tracker started. Subscribed to /camera/image_raw'
        )

    def image_callback(self, msg):
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f'cv_bridge conversion failed: {e}')
            return

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Tighter green range to reduce false positives
        lower_green = np.array([35, 80, 80])
        upper_green = np.array([85, 255, 255])

        mask = cv2.inRange(hsv, lower_green, upper_green)

        # Remove salt-and-pepper noise
        mask = cv2.medianBlur(mask, 5)

        # Morphological cleanup
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=2)
        mask = cv2.dilate(mask, kernel, iterations=3)

        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        rects = []

        for cnt in contours:
            area = cv2.contourArea(cnt)

            # Ignore tiny noisy blobs
            if area > 1500:
                x, y, w, h = cv2.boundingRect(cnt)
                rects.append((x, y, x + w, y + h))

                cv2.rectangle(
                    frame, (x, y), (x + w, y + h), (0, 255, 0), 2
                )

        objects = self.ct.update(rects)

        for object_id, centroid in objects.items():
            cx, cy = int(centroid[0]), int(centroid[1])

            cv2.putText(
                frame,
                f'ID {object_id}',
                (cx - 10, cy - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

        cv2.imshow('Object Tracker', frame)
        cv2.imshow('Green Mask', mask)
        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    node = ObjectTracker()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()