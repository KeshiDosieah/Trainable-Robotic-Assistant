#!/usr/bin/env python
import rospy
import cv2
import serial
import time
import sys
import numpy as np
from hashlib import sha1
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import time
from cv2 import aruco
#from IK_Func import *

target = None
request = False
home_position = [1.8,0,1] #Sa to bzn check si li bon/ To bzn calibrate home position la
arduino = serial.Serial('/dev/ttyACM1', 9600)

def callback3(data):
    global target, request, arduino
    target = data.data
    request = True
    print(target)

    file = open("angle.txt", "r")
    for line in file:
      fields = line.split(",")
      angle1 = float(fields[0])
      angle2 = float(fields[1])
      angle3 = float(fields[2])
      angle4 = float(fields[3])
    file.close()

    # angles = IK(home_position,"horizontal")
    # angle_diff1 = angles[0] - angle1
    # angle_diff2 = angles[1] - angle2
    # angle_diff3 = angles[2] - angle3
    # angle_diff4 = angles[3] - angle4
    # angle_diff = str(angle_diff1) + "," + str(angle_diff2) + "," + str(angle_diff3) + "," + str(angle_diff4) + "\n"
    # arduino.write(angle_diff)
    #
    # file = open("angle.txt", "w")
    # file.write("{},{},{},{}\n".format(angles[0],angles[1],angles[2],angles[3]))
    # file.close()
    #print(angles[0])
    arduino.write("start\n")


rospy.init_node('vision', anonymous=True)

publisher = rospy.Publisher('/Image', Image, queue_size=1)

rospy.Subscriber('/Command', String, callback3)

ARUCO_PARAMETERS = aruco.DetectorParameters_create()
ARUCO_DICT = aruco.Dictionary_get(aruco.DICT_6X6_250)


cameraMatrix=cv2.UMat(np.array([[ 609.710537, 0.000000, 303.200522 ],
               [0.000000, 606.011374, 258.905227],
               [0.000000, 0.000000, 1.000000]],dtype=np.float32))

distCoeffs = cv2.UMat(np.array([0.084930, -0.153198, 0.011283, -0.000882, 0.000000],dtype=np.float32))


#rate = rospy.Rate(10)
vid = cv2.VideoCapture(3)
time.sleep(3)
vid.set(3,640) #width
vid.set(4,480) #height
vid.set(cv2.CAP_PROP_FPS,40) #fps

bridge = CvBridge()

while not rospy.is_shutdown() and True:
    corners = []
    # Capturing each frame of our video stream
    ret,QueryImg = vid.read()
    #QueryImg = cv2.resize(QueryImg,(640, 480), interpolation = cv2.INTER_CUBIC)

    originalImg = QueryImg
    originalImg=bridge.cv2_to_imgmsg(np.array(originalImg), "bgr8")
    publisher.publish(originalImg)
    # QueryImg = QueryImg[20::, ::]
    if request:
        # grayscale image
        gray = cv2.cvtColor(QueryImg, cv2.COLOR_BGR2GRAY)

        # Detect Aruco markers
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, ARUCO_DICT, parameters=ARUCO_PARAMETERS)

        if corners != []: #And push button is pressed


            # c = corners[0][0]

            # centre = (c[:,0].mean(),c[:,1].mean())

        #Outline all of the markers detected in our image
            # QueryImg = aruco.drawDetectedMarkers(QueryImg, corners,ids, borderColor=(255, 0, 255))

            for i in range(len(corners)):
                # rvec, tvec = aruco.estimatePoseSingleMarkers(corners[i], 0.02, cameraMatrix,distCoeffs)
                # QueryImg = aruco.drawAxis(QueryImg, cameraMatrix, distCoeffs, rvec, tvec, 0.01)
                # print(cv2.UMat.get(tvec))
                # rotM = np.zeros(shape=(3,3))
                # print(cv2.Rodrigues(rvec,rotM,jacobian=0))

                centre = (corners[i][0][:,0].mean(),corners[i][0][:,1].mean())
                # QueryImg = cv2.circle(QueryImg, centre, radius=5, color=(0,255,0), thickness=-1)
                # print(ids[i][0])
                if (ids[i][0] == int(target)):
                    print("found")
                    arduino.write("found\n")
                    request = False

vid.release()
