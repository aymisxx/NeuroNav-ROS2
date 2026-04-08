from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='nn_perception',
            executable='pytorch_wrapper_node',
            name='pytorch_wrapper_node',
            output='screen'
        )
    ])
