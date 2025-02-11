#!/usr/bin/env python3
import rclpy
from interface.msg import MyMsg 
from rclpy.node import Node
from std_srvs.srv import Trigger 
from interface.srv import MissionRequest
from geometry_msgs.msg import Pose

class my_service(Node):
    def __init__(self):
        super().__init__('my_mission')
        self.ser= self.create_service(Trigger, "/start_mission" , self.callback)
        self.pub=self.create_publisher(MyMsg, '/mission' , 10)
    
    def callback(self, request, response):
        mission_name=request.mission_name
        target_pose=request.target_pose

        if mission_name not in ["GoTo", "Stop"]:
            self.get_logger().warn("INVALID REQUEST RECIEVED")
            response.accepted = False
            response.message = "Invalid mission name"
            return response
        
        mission_msg = MyMsg()
        mission_msg.mission_name = mission_name
        mission_msg.target_pose = target_pose

        self.publisher.publish(mission_msg)
        self.get_logger().info('Mission Published!')

        response.accepted = True
        response.message = "mission approved"
        return response

        

def main():
    rclpy.init()
    service = my_service()
    rclpy.spin(service)

    service.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()