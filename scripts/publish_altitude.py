#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Empty
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist


def controller_cb(data):
    global controller_pos_Y
    controller_pos_Y = data.pose.position.y
    
def drone_cb(data):
    global drone_pos_Y
    drone_pos_Y = data.pose.position.y

def altitude_pid_cp(data):
    global drone_y_vel
    drone_y_vel = data.data
    #print(type(drone_y_vel))

# Nodo 
def publish_altitude():
    global controller_pos_Y
    global drone_pos_Y
    global msg
    global drone_y_vel
    
    drone_y_vel = float()
    controller_pos_Y = float()
    drone_pos_Y = float()
    msg = Twist()
    
    # Publishers
    publish_state = rospy.Publisher("state", Float64, queue_size=10 )
    publish_setpoint = rospy.Publisher("setpoint", Float64, queue_size=10 )
    pub_vel = rospy.Publisher('cmd_vel', Twist, queue_size=10)

    rospy.init_node('publish_altitude', anonymous=True)
    rate = rospy.Rate(50) # 50hz
    rospy.Subscriber("vrpn_client_node/Quad1/pose", PoseStamped, controller_cb)
    rospy.Subscriber("vrpn_client_node/Quad2/pose", PoseStamped, drone_cb)
    rospy.Subscriber("control_effort", Float64, altitude_pid_cp)

    
    
    
    while not rospy.is_shutdown():
        publish_state.publish(drone_pos_Y)
        publish_setpoint.publish(controller_pos_Y)
        msg.linear.z = drone_y_vel
        pub_vel.publish(msg)
        rate.sleep()
        

if __name__ == '__main__':
    publish_altitude()
    