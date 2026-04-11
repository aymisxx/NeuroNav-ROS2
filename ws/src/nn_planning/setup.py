from setuptools import find_packages, setup

package_name = 'nn_planning'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/day52_full_system_bringup.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ay',
    maintainer_email='aymisxx@proton.me',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'perception_to_planning_node = nn_planning.perception_to_planning_node:main',
            'local_planner_node = nn_planning.local_planner_node:main',
            'navigation_sim_node = nn_planning.navigation_sim_node:main',
            'safety_layer_node = nn_planning.safety_layer_node:main',
            'behavior_logic_node = nn_planning.behavior_logic_node:main',
            'lifecycle_manager_node = nn_planning.lifecycle_manager_node:main',
            'diagnostics_logger_node = nn_planning.diagnostics_logger_node:main',
            'test_automation_node = nn_planning.test_automation_node:main',
            'stress_test_node = nn_planning.stress_test_node:main',
            'demo_recorder_node = nn_planning.demo_recorder_node:main',
        ],
    },
)
