#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from interface.action import Navigate
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry , Path
import math
from tf_transformations import euler_from_quaternion

class my_action(Node):
    def __init__(self):
        super().__init__("local_planner")
        self.count_from_server = ActionServer(self, Navigate , "/navigate" , execute_callback= self.execute_callback)
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)

        self.current_x = 0.0
        self.current_y = 0.0
        self.current_yaw = 0.0

    def odom_callback(self, msg):
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y

        quaternion = msg.pose.pose.orientation
        quaternion_list = [quaternion.x, quaternion.y, quaternion.z, quaternion.w]
        _, _, self.current_yaw = euler_from_quaternion(quaternion_list)




    def execute_callback(self, goal):
        path = goal.request.path.poses
        if not path:
            goal.abort()
            return Navigate.Result(success=False)


        final_pose = path[-1].pose
        goal_x = final_pose.position.x
        goal_y = final_pose.position.y

        self.rotate_towards(goal_x, goal_y)

        for waypoint in path:
            remaining_distance = self.calculate_distance(waypoint.pose)

            self.move_to_waypoint(waypoint.pose)

            feedback_msg = Navigate.Feedback()
            feedback_msg.remaining_distance = int(remaining_distance)
            goal.publish_feedback(feedback_msg)

        self.stop_robot()

        goal.succeed()
        return Navigate.Result(success=True)

    def rotate_towards(self, goal_x, goal_y):
        dx = goal_x - self.current_x
        dy = goal_y - self.current_y
        desired_yaw = math.atan2(dy, dx)

        while rclpy.ok():
            error = desired_yaw - self.current_yaw

            error = (error + math.pi) % (2 * math.pi) - math.pi  

            if abs(error) < 0.087:
                break

            twist = Twist()
            twist.angular.z = 0.5 * error  
            self.cmd_vel_pub.publish(twist)

            rclpy.spin_once(self)

        self.stop_robot()

    def stop_robot(self):
        twist = Twist()
        self.cmd_vel_pub.publish(twist)

    def calculate_distance(self, goal_pose):
        dx = goal_pose.position.x - self.current_x
        dy = goal_pose.position.y - self.current_y
        return math.sqrt(dx**2 + dy**2)

def main(args = None):
    rclpy.init(args=args)
    node = my_action()

    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()