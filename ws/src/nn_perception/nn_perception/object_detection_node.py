from pathlib import Path

import cv2
import rclpy
import torch
from PIL import Image as PILImage
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image
from torchvision.models.detection import FasterRCNN_ResNet50_FPN_Weights
from torchvision.models.detection import fasterrcnn_resnet50_fpn


class ObjectDetectionNode(Node):
    def __init__(self):
        super().__init__('object_detection_node')

        self.bridge = CvBridge()
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.get_logger().info(f'Using device: {self.device}')

        self.image_topic = '/camera/image_raw'
        self.output_topic = '/nn/detections/image'
        self.score_threshold = 0.70
        self.asset_saved = False

        weights = FasterRCNN_ResNet50_FPN_Weights.DEFAULT
        self.categories = weights.meta['categories']
        self.preprocess = weights.transforms()

        self.model = fasterrcnn_resnet50_fpn(weights=weights)
        self.model.to(self.device)
        self.model.eval()

        self.subscription = self.create_subscription(
            Image,
            self.image_topic,
            self.image_callback,
            10
        )

        self.publisher_ = self.create_publisher(Image, self.output_topic, 10)

        self.asset_dir = Path.home() / 'GitHub' / 'NeuroNav-ROS2' / 'assets'
        self.asset_dir.mkdir(parents=True, exist_ok=True)
        self.asset_path = self.asset_dir / 'day33_object_detection.jpg'

        self.get_logger().info(f'Subscribed to: {self.image_topic}')
        self.get_logger().info(f'Publishing annotated detections to: {self.output_topic}')
        self.get_logger().info(f'Visual asset will be saved to: {self.asset_path}')

    def image_callback(self, msg: Image):
        try:
            frame_bgr = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f'cv_bridge conversion failed: {e}')
            return

        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        pil_image = PILImage.fromarray(frame_rgb)
        tensor = self.preprocess(pil_image).to(self.device)

        with torch.no_grad():
            prediction = self.model([tensor])[0]

        annotated = frame_bgr.copy()
        detections_kept = 0

        boxes = prediction['boxes'].detach().cpu().numpy()
        labels = prediction['labels'].detach().cpu().numpy()
        scores = prediction['scores'].detach().cpu().numpy()

        for box, label, score in zip(boxes, labels, scores):
            if score < self.score_threshold:
                continue

            x1, y1, x2, y2 = box.astype(int)
            class_name = self.categories[label] if label < len(self.categories) else f'class_{label}'
            caption = f'{class_name}: {score:.2f}'

            cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                annotated,
                caption,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
                cv2.LINE_AA
            )
            detections_kept += 1

        out_msg = self.bridge.cv2_to_imgmsg(annotated, encoding='bgr8')
        out_msg.header = msg.header
        self.publisher_.publish(out_msg)

        self.get_logger().info(f'Published annotated frame | detections_kept={detections_kept}')

        if detections_kept > 0 and not self.asset_saved:
            cv2.imwrite(str(self.asset_path), annotated)
            self.asset_saved = True
            self.get_logger().info(f'Saved visual asset: {self.asset_path}')


def main(args=None):
    rclpy.init(args=args)
    node = ObjectDetectionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()