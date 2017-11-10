#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist

controller_pos_Y = 0.0
drone_pos_Y = 0.0

msg = Twist()
msg.angular.x = 0
msg.angular.y = 0
msg.angular.z = 0

msg.linear.x = 0
msg.linear.y = 0
msg.linear.z = 0

def controller_cb(data):
    #print(data.pose.position.y)
    controller_pos_Y = data.pose.position.y
    if controller_pos_Y > 0.1:
        #print("takeoff")
        pub = rospy.Publisher("ardrone/takeoff", Empty, queue_size=10 )
        #rate = rospy.Rate(10) # 10hz
        pub.publish(Empty())
        #rate.sleep()
    else:
        pub = rospy.Publisher("ardrone/land", Empty, queue_size=10 )
        pub.publish(Empty())
        #print("landed")
        
def drone_cb(data):
    #print(data.pose.position.y)
    drone_pos_Y = data.pose.position.y

    print(controller_pos_Y," ",drone_pos_Y)
    msg.linear.z = 0.9
    pub = rospy.Publisher("cmd_vel", Twist, queue_size=10 )
    pub.publish(msg)
    


    



def altittude():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('altittude', anonymous=True)

    rospy.Subscriber("vrpn_client_node/Quad2/pose", PoseStamped, controller_cb)
    rospy.Subscriber("vrpn_client_node/Quad1/pose", PoseStamped, drone_cb)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    altittude()
    