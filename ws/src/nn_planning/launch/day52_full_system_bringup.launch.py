from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='nn_planning',
            executable='perception_to_planning_node',
            name='perception_to_planning_node',
            output='screen'
        ),
        Node(
            package='nn_planning',
            executable='local_planner_node',
            name='local_planner_node',
            output='screen'
        ),
        Node(
            package='nn_planning',
            executable='navigation_sim_node',
            name='navigation_sim_node',
            output='screen'
        ),
        Node(
            package='nn_planning',
            executable='behavior_logic_node',
            name='behavior_logic_node',
            output='screen'
        ),
        Node(
            package='nn_planning',
            executable='safety_layer_node',
            name='safety_layer_node',
            output='screen'
        ),
        Node(
            package='nn_planning',
            executable='diagnostics_logger_node',
            name='diagnostics_logger_node',
            output='screen'
        ),
    ])
