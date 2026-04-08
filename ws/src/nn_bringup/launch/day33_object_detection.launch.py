from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='nn_perception',
            executable='static_image_publisher',
            name='static_image_publisher',
            output='screen'
        ),
        Node(
            package='nn_perception',
            executable='object_detection_node',
            name='object_detection_node',
            output='screen'
        )
    ])