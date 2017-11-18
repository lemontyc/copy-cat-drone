#!/usr/bin/env python
import rospy
import math
import tf
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Empty
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist

#type(pose) = geometry_msgs.msg.Pose
def quaternion_to_euler_angle(holi):
    
    quaternion = (
        holi.pose.orientation.x,
        holi.pose.orientation.y,
        holi.pose.orientation.z,
        holi.pose.orientation.w)
    
    euler = tf.transformations.euler_from_quaternion(quaternion)
    yaw = euler[2] * ( 180.0 / math.pi)
    print yaw
    return euler

def controller_cb(data):
    global position_controller
    position_controller = data
    
def drone_cb(data):
    global position_drone
    position_drone = data

def r_pid_cp(data):
    global drone_cmd_vel
    drone_cmd_vel.angular.z = data.data

# Nodo 
def pid_rotation():
    global position_controller
    global position_drone
    global drone_cmd_vel
    global drone_rotation
    global controller_rotation

    position_controller = PoseStamped()
    position_drone = PoseStamped()
    drone_cmd_vel = Twist()
    drone_rotation = float()
    controller_rotation = float()
    
    # Initialize node
    rospy.init_node('pid_rotation', anonymous=True)
    # Publishing frecuency 
    rate = rospy.Rate(50) # 50hz

    # Publishers ----------------------------------------------------------------

    # Drone rotation  PID publisher
    pub_pid_state_r = rospy.Publisher("state", Float64, queue_size=10 )
    pub_pid_setpoint_r = rospy.Publisher("setpoint", Float64, queue_size=10 )
    

    # Drone cmd_vel publisher
    pub_cmd_vel = rospy.Publisher('cmd_vel', Twist, queue_size=10)

    # Subscribers ----------------------------------------------------------------

    # Drone rotation PID subscriber
    rospy.Subscriber("control_effort", Float64, r_pid_cp)

    # Drone controller subscriber
    rospy.Subscriber("vrpn_client_node/Quad1/pose", PoseStamped, controller_cb)
    
    # Controlled drone subscriber
    rospy.Subscriber("vrpn_client_node/Quad2/pose", PoseStamped, drone_cb)
    
    
    while not rospy.is_shutdown():
        # Calculate Euuler's angles
        controller_rotation = quaternion_to_euler_angle(position_controller)
        #drone_rotation = quaternion_to_euler_angle(position_drone.pose.orientation.w, position_drone.pose.orientation.x,position_drone.pose.orientation.y,position_drone.pose.orientation.z)

        # Drone's rotation axis PID
        # pub_pid_state_r.publish(drone_rotation )
        pub_pid_setpoint_r.publish(controller_rotation)
        '''
        #print( controller_rotation)
        print("drone: " ,drone_rotation)
        print("controller:    " ,controller_rotation)
        print("Control:    " ,drone_cmd_vel)
        '''
        #pub_cmd_vel.publish(drone_cmd_vel)
        rate.sleep()
        

if __name__ == '__main__':
    pid_rotation()
