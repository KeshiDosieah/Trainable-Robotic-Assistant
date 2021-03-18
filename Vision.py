#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from hashlib import sha1
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge


def callback(data):
    print(data.data)

rospy.init_node('vision', anonymous=True)

publisher = rospy.Publisher('/Image', Image, queue_size=1)
rospy.Subscriber('/Command', String, callback)

rate = rospy.Rate(10)
vid = cv2.VideoCapture(0)
bridge = CvBridge()
while not rospy.is_shutdown() and True:

    ret, frame = vid.read()
    # msg = CompressedImage()
    # msg.header.stamp = rospy.Time.now()
    # msg.format = "jpeg"
    # msg.data = np.array(cv2.imencode('.jpg', frame)[1]).tostring()
    imgMsg = bridge.cv2_to_imgmsg(frame, "bgr8")
    publisher.publish(imgMsg)

cv2.destroyAllWindows()
# After the loop release the cap object
vid.release()
