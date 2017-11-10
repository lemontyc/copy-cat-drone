#!/usr/bin/env python
import time
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

msg = Twist()
msg.angular.z= -0.25
def move():
        pub = rospy.Publisher("cmd_vel", Twist, queue_size=10 )
        rospy.init_node('move', anonymous=True)
        while not rospy.is_shutdown():
        pub.publish(msg)
        

        
        

if __name__ == '__main__':
        try:
          move()
        except rospy.ROSInterruptException:
          pass