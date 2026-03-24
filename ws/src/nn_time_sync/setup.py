from setuptools import find_packages, setup

package_name = 'nn_time_sync'

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
    description='Time synchronization experiments for NeuroNav ROS 2.',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'time_sync_node = nn_time_sync.time_sync_node:main',
        ],
    },
)