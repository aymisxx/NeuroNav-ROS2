from setuptools import find_packages, setup

package_name = 'nn_mapping'

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
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'semantic_map_node = nn_mapping.semantic_map_node:main',
            'occupancy_grid_node = nn_mapping.occupancy_grid_node:main',
            'scan_processing_node = nn_mapping.scan_processing_node:main',
            'map_query_service = nn_mapping.map_query_service:main',
            'language_goal_node = nn_mapping.language_goal_node:main',
        ],
    },
)
