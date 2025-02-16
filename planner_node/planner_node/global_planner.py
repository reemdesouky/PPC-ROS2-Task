#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from interface.srv import CreatePlan
from nav_msgs.msg import Path , Odometry
from geometry_msgs.msg import Pose , PoseStamped

class my_service(Node):
    def __init__(self):
        super().__init__('global_planner')
        self.ser= self.create_service(CreatePlan, '/create_plan' , self.callback)
        self.sub_odom = self.create_subscription(Odometry , '/odom' , self.sub_callback)

        self.current_pose = Pose()

    def sub_callback(self, msg): 
        self.current_pose = msg.pose.pose

    def callback(self, request, response):
        path_msg = Path()
        path_msg.header.stamp = self.get_clock().now().to_msg()
        path_msg.header.frame_id = "map"

        start_point = PoseStamped()
        start_point.header = path_msg.header
        start_point.pose = self.current_pose  
        path_msg.poses.append(start_point)

        goal_point = PoseStamped()
        goal_point.header = path_msg.header
        goal_point.pose = request.target_pose 
        path_msg.poses.append(goal_point)

        response.path = path_msg
        return response
        

def main():
    rclpy.init()
    service = my_service()
    rclpy.spin(service)

    service.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()