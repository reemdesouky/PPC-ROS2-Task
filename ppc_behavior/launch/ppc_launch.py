import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ppc_behavior',
            executable='my_mission',
            name='my_mission',
            output='screen'
        ),
        Node(
            package='ppc_behavior',
            executable='beh',
            name='beh',
            output='screen'
        ),
        Node(
            package='ppc_behavior',
            executable='global_planner',
            name='global_planner',
            output='screen'
        ),
        Node(
            package='ppc_behavior',
            executable='local_planner',
            name='local_planner',
            output='screen'
        )
    ])
