#! /usr/bin/env python
import rospy
import datetime
from hashlib import sha1
from sensor_msgs.msg import Image
from std_msgs.msg import String

def callback(data):
    print(data.data)

rospy.init_node('controller', anonymous=True)

publisher1 = rospy.Publisher('/Actuator', String, queue_size=1)
publisher2 = rospy.Publisher('/Command', String, queue_size=1)
rospy.Subscriber('/Command', String, callback)

rate = rospy.Rate(10)
while not rospy.is_shutdown():
       info1 = "Actuator data"
       info1 = info1 + "("+str(sha1(info1).hexdigest())+")"
       now = datetime.datetime.now()
       info2 = "Command data " + str(now)
       info2 = info2 + "(" + str(sha1(info2).hexdigest()) + ")"
       # rospy.loginfo(info1)
       # rospy.loginfo(info2)
       publisher1.publish(info1)
       publisher2.publish(info2)
       rate.sleep()
