from setuptools import setup
import os
from glob import glob

package_name = 'ppc_behavior'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='reem',
    maintainer_email='reemibraahiim1@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'beh = ppc_behavior.beh:main',
            'my_mission = ppc_behavior.my_mission:main',
            'global_planner = ppc_behavior.global_planner:main',
            'local_planner = ppc_behavior.local_planner:main',
        ],
    },
)
