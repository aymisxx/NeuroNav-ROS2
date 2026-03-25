import numpy as np
from scipy.spatial import distance as dist
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import random


class CentroidTracker:
    def __init__(self, max_disappeared=10):
        self.next_object_id = 0
        self.objects = {}          # object_id -> centroid
        self.disappeared = {}      # object_id -> frames disappeared
        self.max_disappeared = max_disappeared

    def register(self, centroid):
        self.objects[self.next_object_id] = centroid
        self.disappeared[self.next_object_id] = 0
        self.next_object_id += 1

    def deregister(self, object_id):
        del self.objects[object_id]
        del self.disappeared[object_id]

    def update(self, input_centroids):
        if len(input_centroids) == 0:
            for object_id in list(self.disappeared.keys()):
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
            return self.objects

        if len(self.objects) == 0:
            for centroid in input_centroids:
                self.register(centroid)
            return self.objects

        object_ids = list(self.objects.keys())
        object_centroids = list(self.objects.values())

        D = dist.cdist(np.array(object_centroids), input_centroids)

        rows = D.min(axis=1).argsort()
        cols = D.argmin(axis=1)[rows]

        used_rows = set()
        used_cols = set()

        for (row, col) in zip(rows, cols):
            if row in used_rows or col in used_cols:
                continue

            object_id = object_ids[row]
            self.objects[object_id] = input_centroids[col]
            self.disappeared[object_id] = 0

            used_rows.add(row)
            used_cols.add(col)

        unused_rows = set(range(D.shape[0])).difference(used_rows)
        unused_cols = set(range(D.shape[1])).difference(used_cols)

        if D.shape[0] >= D.shape[1]:
            for row in unused_rows:
                object_id = object_ids[row]
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
        else:
            for col in unused_cols:
                self.register(input_centroids[col])

        return self.objects


class MultiObjectTrackerNode(Node):
    def __init__(self):
        super().__init__('multi_object_tracker')

        self.tracker = CentroidTracker(max_disappeared=5)

        self.publisher = self.create_publisher(String, '/tracking/objects', 10)

        self.timer = self.create_timer(0.5, self.timer_callback)

        self.get_logger().info("Multi-Object Tracker Node Started")

    def timer_callback(self):
        # 🔥 Persistent simulated objects (REALISTIC motion)

        if not hasattr(self, "sim_objects"):
            self.sim_objects = [
                [100, 100],
                [300, 200],
                [500, 400]
            ]

        detections = []
        for obj in self.sim_objects:
            dx = random.randint(-20, 20)
            dy = random.randint(-20, 20)

            obj[0] = max(0, min(640, obj[0] + dx))
            obj[1] = max(0, min(480, obj[1] + dy))

            detections.append((obj[0], obj[1]))

        detections = np.array(detections)

        objects = self.tracker.update(detections)

        output = []
        for object_id, centroid in objects.items():
            output.append(f"ID {object_id}: ({int(centroid[0])}, {int(centroid[1])})")

        msg = String()
        msg.data = " | ".join(output)

        self.publisher.publish(msg)

        self.get_logger().info(f"Tracked: {msg.data}")


def main(args=None):
    rclpy.init(args=args)
    node = MultiObjectTrackerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()