#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist


def controller_cb(data):
    global controller_pos_Y
    controller_pos_Y = data.pose.position.y

def drone_cb(data):
    global drone_pos_Y
    drone_pos_Y = data.pose.position.y

def altitude():
    global controller_pos_Y
    global drone_pos_Y
    global msg

    controller_pos_Y = float()
    drone_pos_Y = float()
    msg = Twist()

    # Publishers
    pub_takeoff= rospy.Publisher("ardrone/takeoff", Empty, queue_size=10 )
    pub_land = rospy.Publisher("ardrone/land", Empty, queue_size=10 )

    pub_vel = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rospy.init_node('altitude', anonymous=True)
    rate = rospy.Rate(50) # 50hz
    rospy.Subscriber("vrpn_client_node/Quad1/pose", PoseStamped, controller_cb)
    rospy.Subscriber("vrpn_client_node/Quad2/pose", PoseStamped, drone_cb)


    

    while not rospy.is_shutdown():
        # Landed
        if controller_pos_Y < 0.1:
            pub_land.publish(Empty())
            print("landed")
        # Takeoff
        elif controller_pos_Y > 0.1 and controller_pos_Y < 0.2:
            pub_takeoff.publish(Empty())
            print("liftoff")
        elif controller_pos_Y > 0.2 and (drone_pos_Y < controller_pos_Y):
            msg.linear.z = 0.8
            pub_vel.publish(msg)
            print("Subiendo")
        elif controller_pos_Y > 0.2 and (drone_pos_Y > controller_pos_Y):
            msg.linear.z = 0.0
            pub_vel.publish(msg)
            print("estable")




        rate.sleep()


if __name__ == '__main__':
    altitude()
