from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    return LaunchDescription([

        Node(
            package='nn_sensors',
            executable='camera_publisher',
            name='camera_publisher',
            output='screen'
        ),

        Node(
            package='nn_sensors',
            executable='imu_publisher',
            name='imu_publisher',
            output='screen'
        ),

        Node(
            package='nn_estimation',
            executable='imu_vision_fusion',  # ✅ FIXED
            name='fusion_node',
            output='screen'
        ),

        Node(
            package='nn_perception',
            executable='multi_object_tracker',
            name='multi_object_tracker',
            output='screen'
        ),

    ])