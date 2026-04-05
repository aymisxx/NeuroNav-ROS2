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
            package='nn_sensors',
            executable='lidar_publisher',
            name='lidar_publisher',
            output='screen'
        ),

        Node(
            package='nn_estimation',
            executable='imu_vision_fusion',
            name='fusion_node',
            output='screen'
        ),

        Node(
            package='nn_estimation',
            executable='visual_odometry',
            name='visual_odometry_node',
            output='screen'
        ),

        Node(
            package='nn_estimation',
            executable='pose_chaining',
            name='pose_chaining_node',
            output='screen'
        ),

        Node(
            package='nn_perception',
            executable='multi_object_tracker',
            name='multi_object_tracker',
            output='screen'
        ),

    ])
