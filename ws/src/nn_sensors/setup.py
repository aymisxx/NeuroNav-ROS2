from setuptools import setup

package_name = 'nn_sensors'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='duskpriest',
    maintainer_email='aymisxx@proton.me',
    description='Sensor interface nodes for NeuroNav-ROS2.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'camera_publisher = nn_sensors.camera_publisher:main',
            'image_viewer = nn_sensors.image_viewer:main',
        ],
    },
)