#! /usr/bin/env python
import rospy
from hashlib import sha1
from std_msgs.msg import String


def callback1(data):
    print(data.data)

def callback2(data):
    print(data.data)

rospy.init_node('arduino', anonymous=True)

publisher = rospy.Publisher('/Sensor', String, queue_size=1)
rospy.Subscriber('/Command', String, callback1)
rospy.Subscriber('/Actuator', String, callback2)

rate = rospy.Rate(10)
while not rospy.is_shutdown():
    info="sensor data"
    info = info + "(" + str(sha1(info).hexdigest()) + ")"
    # rospy.loginfo(info)
    publisher.publish(info)
    rate.sleep()
