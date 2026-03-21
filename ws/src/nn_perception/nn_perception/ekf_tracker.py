#!/usr/bin/env python3

import time

import cv2
import numpy as np

import rclpy
from rclpy.node import Node

from cv_bridge import CvBridge
from sensor_msgs.msg import Image


class EKFTracker(Node):
    def __init__(self):
        super().__init__('ekf_tracker')

        self.bridge = CvBridge()

        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        # State: [x, y, vx, vy]^T
        self.x = np.zeros((4, 1), dtype=np.float32)

        # Covariance
        self.P = np.eye(4, dtype=np.float32)

        # Process noise
        self.Q = np.eye(4, dtype=np.float32) * 1e-2

        # Measurement noise
        self.R = np.eye(2, dtype=np.float32) * 1e-1

        self.initialized = False
        self.last_time = None

        self.get_logger().info('EKF Tracker started.')

    def image_callback(self, msg):
        current_time = time.time()

        if self.last_time is None:
            dt = 0.1
        else:
            dt = current_time - self.last_time

        self.last_time = current_time

        # State transition matrix
        F = np.array(
            [[1, 0, dt, 0],
             [0, 1, 0, dt],
             [0, 0, 1, 0],
             [0, 0, 0, 1]],
            dtype=np.float32
        )

        # Predict
        self.x = F @ self.x
        self.P = F @ self.P @ F.T + self.Q

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
                    self.x = np.array(
                        [[np.float32(cx)],
                         [np.float32(cy)],
                         [0.0],
                         [0.0]],
                        dtype=np.float32
                    )
                    self.initialized = True

        if self.initialized:
            px, py = int(self.x[0]), int(self.x[1])

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
                # Linear measurement model: z = Hx
                H = np.array(
                    [[1, 0, 0, 0],
                     [0, 1, 0, 0]],
                    dtype=np.float32
                )

                z_pred = H @ self.x
                y_residual = measured - z_pred
                S = H @ self.P @ H.T + self.R
                K = self.P @ H.T @ np.linalg.inv(S)

                self.x = self.x + K @ y_residual
                I = np.eye(4, dtype=np.float32)
                self.P = (I - K @ H) @ self.P

                ex, ey = int(self.x[0]), int(self.x[1])

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

        cv2.imshow('EKF Tracker', frame)
        cv2.imshow('EKF Green Mask', mask)
        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    node = EKFTracker()

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