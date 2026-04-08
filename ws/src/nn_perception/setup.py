from setuptools import find_packages, setup

package_name = 'nn_perception'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name],
        ),
        (
            'share/' + package_name,
            ['package.xml'],
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='duskpriest',
    maintainer_email='aymisxx@proton.me',
    description='ROS2 perception nodes for NeuroNav project',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'edge_detector = nn_perception.edge_detector:main',
            'orb_features = nn_perception.orb_features:main',
            'depth_processor = nn_perception.depth_processor:main',
            'rgb_depth_sync = nn_perception.rgb_depth_sync:main',
            'object_tracker = nn_perception.object_tracker:main',
            'kalman_tracker = nn_perception.kalman_tracker:main',
            'ekf_tracker = nn_perception.ekf_tracker:main',
            'multi_object_tracker = nn_perception.multi_object_tracker:main',
            'pytorch_wrapper_node = nn_perception.pytorch_wrapper_node:main',
        ],
    },
)
