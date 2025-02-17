#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from interface.msg import MyMsg 
from nav_msgs.msg import Path
from geometry_msgs.msg import Pose
from interface.srv import CreatePlan
from interface.action import Navigate
from rclpy.action import ActionClient

class my_behavioral (Node):
    def __init__(self):
        super().__init__('beh')

        #subscriber
        self.mission_sub=self.create_subscription(MyMsg, '/mission' , self.callback , 10)

        #publishers
        self.state_pub = self.create_publisher(String, '/state' , 10 )
        self.path_pub = self.create_publisher(Path, '/global_plan', 10)

        #service client
        self.ser= self.create_client(CreatePlan, '/create_plan')

        #action client
        self.act=ActionClient(self, Navigate , '/navigate')


    def callback(self,msg):
        if msg.mission_name=="Stop":
            self.state = 'idle'
            self.publish_state()

        elif msg.mission_name=="GoTo":
            self.state= 'create_path'
            self.publish_state()
            self.request_path(msg.target_pose)
            

    def request_path (self, msg):
        while not self.ser.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn("Waiting for Global Planner service...")

        request = CreatePlan.Request()
        request.target_pose = msg

        future = self.ser.call_async(request)
        future.add_done_callback(self.handle_plan_response)


    def handle_plan_response(self, future):
        try:
            response = future.result()
            self.path_pub.publish(response.path)

            self.state = "navigate"
            self.publish_state()
            self.trigger_navigation(response.path)

        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")


    def trigger_navigation(self, response):
        self.act.wait_for_server()
        goal_msg = Navigate.Goal()
        goal_msg.path = response

        send_goal_future = self.act.send_goal_async(goal_msg)

        self.state = 'idle'
        self.publish_state()


    def publish_state(self):
        msg = String()
        msg.data = self.state
        self.state_pub.publish(msg)

def main():
    rclpy.init()
    node = my_behavioral()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()