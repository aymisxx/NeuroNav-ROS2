import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import torch


class PyTorchWrapperNode(Node):
    def __init__(self):
        super().__init__('pytorch_wrapper_node')

        self.publisher_ = self.create_publisher(String, '/nn/pytorch_status', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)

        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.get_logger().info(f'PyTorch version: {torch.__version__}')
        self.get_logger().info(f'Using device: {self.device}')

    def timer_callback(self):
        x = torch.tensor([[1.0, 2.0], [3.0, 4.0]], device=self.device)
        y = x * 2.0
        msg = String()
        msg.data = f'device={self.device} | tensor_sum={torch.sum(y).item():.2f}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = PyTorchWrapperNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
