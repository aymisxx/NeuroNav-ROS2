#!/usr/bin/env python3

import time

import cv2
import numpy as np

import rclpy
from rclpy.node import Node

from cv_bridge import CvBridge
from sensor_msgs.msg import Image


class KalmanTracker(Node):
    def __init__(self):
        super().__init__('kalman_tracker')

        self.bridge = CvBridge()

        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        self.kf = cv2.KalmanFilter(4, 2)

        # State: [x, y, vx, vy]^T
        # Measurement: [x, y]^T
        self.kf.transitionMatrix = np.array(
            [[1, 0, 1, 0],
             [0, 1, 0, 1],
             [0, 0, 1, 0],
             [0, 0, 0, 1]],
            dtype=np.float32
        )

        self.kf.measurementMatrix = np.array(
            [[1, 0, 0, 0],
             [0, 1, 0, 0]],
            dtype=np.float32
        )

        self.kf.processNoiseCov = np.eye(4, dtype=np.float32) * 1e-2
        self.kf.measurementNoiseCov = np.eye(2, dtype=np.float32) * 1e-1
        self.kf.errorCovPost = np.eye(4, dtype=np.float32)

        self.initialized = False
        self.last_time = None

        self.get_logger().info(
            'Kalman tracker started. Subscribed to /camera/image_raw'
        )

    def image_callback(self, msg):
        current_time = time.time()

        if self.last_time is None:
            dt = 0.1
        else:
            dt = current_time - self.last_time

        self.last_time = current_time

        # Update transition matrix dynamically using measured dt
        self.kf.transitionMatrix = np.array(
            [[1, 0, dt, 0],
             [0, 1, 0, dt],
             [0, 0, 1, 0],
             [0, 0, 0, 1]],
            dtype=np.float32
        )

        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f'cv_bridge conversion failed: {e}')
            return

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_green = np.array([35, 80, 80])
        upper_green = np.array([85, 255, 255])

        mask = cv2.inRange(hsv, lower_green, upper_green)
        mask = cv2.medianBlur(mask, 5)

        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=2)
        mask = cv2.dilate(mask, kernel, iterations=3)

        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        measured = None

        if contours:
            largest = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest)

            if area > 1500:
                x, y, w, h = cv2.boundingRect(largest)
                cx = int(x + w / 2)
                cy = int(y + h / 2)

                measured = np.array(
                    [[np.float32(cx)], [np.float32(cy)]],
                    dtype=np.float32
                )

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.circle(frame, (cx, cy), 6, (0, 0, 255), -1)
                cv2.putText(
                    frame,
                    'Measured',
                    (cx + 10, cy),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 255),
                    2
                )

                if not self.initialized:
                    self.kf.statePost = np.array(
                        [[np.float32(cx)],
                         [np.float32(cy)],
                         [0.0],
                         [0.0]],
                        dtype=np.float32
                    )
                    self.initialized = True

        if self.initialized:
            prediction = self.kf.predict()
            px, py = int(prediction[0]), int(prediction[1])

            cv2.circle(frame, (px, py), 6, (255, 0, 0), -1)
            cv2.putText(
                frame,
                'Predicted',
                (px + 10, py),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 0, 0),
                2
            )

            if measured is not None:
                estimated = self.kf.correct(measured)
                ex, ey = int(estimated[0]), int(estimated[1])

                cv2.circle(frame, (ex, ey), 6, (0, 255, 255), -1)
                cv2.putText(
                    frame,
                    'Estimated',
                    (ex + 10, ey),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 255),
                    2
                )

        cv2.imshow('Kalman Tracker', frame)
        cv2.imshow('Green Mask', mask)
        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    node = KalmanTracker()

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