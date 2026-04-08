from setuptools import find_packages, setup

package_name = 'nn_pytorch_wrapper'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=[]),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Ayushman Mishra',
    maintainer_email='aymisxx@proton.me',
    description='PyTorch wrapper node for NeuroNav-ROS2.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'pytorch_wrapper_node = nn_pytorch_wrapper.pytorch_wrapper_node:main',
        ],
    },
)
