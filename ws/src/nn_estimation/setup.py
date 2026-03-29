from setuptools import find_packages, setup

package_name = 'nn_estimation'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='twilightpriest',
    maintainer_email='aymisxx@proton.me',
    description='IMU and vision fusion nodes for NeuroNav-ROS2',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'imu_vision_fusion = nn_estimation.imu_vision_fusion_node:main',
            'visual_odometry = nn_estimation.visual_odometry_node:main',
            'pose_chaining = nn_estimation.pose_chaining_node:main',
        ],
    },
)