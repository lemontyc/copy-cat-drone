#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Empty
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist


def controller_cb(data):
    global position_controller
    position_controller = data
    
def drone_cb(data):
    global position_drone
    position_drone = data

def x_pid_cp(data):
    global drone_cmd_vel
    drone_cmd_vel.linear.x = data.data


# Nodo 
def pid_x():
    global position_controller
    global position_drone
    global drone_cmd_vel

    position_controller = PoseStamped()
    position_drone = PoseStamped()
    drone_cmd_vel = Twist()
    
    # Initialize node
    rospy.init_node('pid_x', anonymous=True)
    # Publishing frecuency 
    rate = rospy.Rate(50) # 50hz

    # Publishers ----------------------------------------------------------------

    # Drone X axis PID publisher
    pub_pid_state_x = rospy.Publisher("state", Float64, queue_size=10 )
    pub_pid_setpoint_x = rospy.Publisher("setpoint", Float64, queue_size=10 )
    

    # Drone cmd_vel publisher
    pub_cmd_vel = rospy.Publisher('cmd_vel', Twist, queue_size=10)

    # Subscribers ----------------------------------------------------------------

    # Drone X axis PID subscriber
    rospy.Subscriber("control_effort", Float64, x_pid_cp)

    # Drone controller subscriber
    rospy.Subscriber("vrpn_client_node/Quad1/pose", PoseStamped, controller_cb)
    
    # Controlled drone subscriber
    rospy.Subscriber("vrpn_client_node/Quad2/pose", PoseStamped, drone_cb)
    
    
    while not rospy.is_shutdown():

        # Drone's X axis PID
        pub_pid_state_x.publish(position_drone.pose.position.z)
        pub_pid_setpoint_x.publish(position_controller.pose.position.z)


        print(drone_cmd_vel)
        pub_cmd_vel.publish(drone_cmd_vel)
        rate.sleep()
        

if __name__ == '__main__':
    pid_x()