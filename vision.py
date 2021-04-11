#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from hashlib import sha1
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import time
from cv2 import aruco


def callback(data):
    print(data.data)

rospy.init_node('vision', anonymous=True)

publisher = rospy.Publisher('/Image', Image, queue_size=1)

rospy.Subscriber('/Command', String, callback)

ARUCO_PARAMETERS = aruco.DetectorParameters_create()
ARUCO_DICT = aruco.Dictionary_get(aruco.DICT_6X6_250)


cameraMatrix=cv2.UMat(np.array([[ 609.710537, 0.000000, 303.200522 ],
               [0.000000, 606.011374, 258.905227],
               [0.000000, 0.000000, 1.000000]],dtype=np.float32))

distCoeffs = cv2.UMat(np.array([0.084930, -0.153198, 0.011283, -0.000882, 0.000000],dtype=np.float32))



#rate = rospy.Rate(10)
vid = cv2.VideoCapture(0)
time.sleep(3)
vid.set(3,640) #width
vid.set(4,480) #height
vid.set(cv2.CAP_PROP_FPS,40) #fps
#camera = PiCamera()
#camera.resolution = (640,480)
#camera.framerate = 60
#rawCapture = PiRGBArray(camera, size=(640,480))
#stream = camera.capture_continuous(rawCapture, format="bgr8", use_video_port=True)
bridge = CvBridge()
#frame = None
#stopped = False
while not rospy.is_shutdown() and True:
    corners = []
    # Capturing each frame of our video stream
    ret,QueryImg = vid.read()
    #QueryImg = cv2.resize(QueryImg,(640, 480), interpolation = cv2.INTER_CUBIC)

    # QueryImg = QueryImg[20::, ::]

    # grayscale image
    gray = cv2.cvtColor(QueryImg, cv2.COLOR_BGR2GRAY)

    originalImg = QueryImg
    originalImg=bridge.cv2_to_imgmsg(np.array(originalImg), "bgr8")
    publisher.publish(originalImg)
    # Detect Aruco markers
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, ARUCO_DICT, parameters=ARUCO_PARAMETERS)


    if corners != []: #And push button is pressed

        # c = corners[0][0]

        # centre = (c[:,0].mean(),c[:,1].mean())

    #Outline all of the markers detected in our image
        QueryImg = aruco.drawDetectedMarkers(QueryImg, corners,ids, borderColor=(255, 0, 255))

        for i in range(len(corners)):
            rvec, tvec = aruco.estimatePoseSingleMarkers(corners[i], 0.02, cameraMatrix,distCoeffs)
            # QueryImg = aruco.drawAxis(QueryImg, cameraMatrix, distCoeffs, rvec, tvec, 0.01)
            # print(cv2.UMat.get(tvec))
            # rotM = np.zeros(shape=(3,3))
            # print(cv2.Rodrigues(rvec,rotM,jacobian=0))

            centre = (corners[i][0][:,0].mean(),corners[i][0][:,1].mean())
            QueryImg = cv2.circle(QueryImg, centre, radius=5, color=(0,255,0), thickness=-1)


    # Exit at the end of the video on the 'q' keypress


    #ret, frame = vid.read()
    #msg = CompressedImage()
    #msg.header.stamp = rospy.Time.now()
    #msg.format = "jpeg"
    #msg.data = np.array(cv2.imencode('.jpg', frame)[1]).tostring()


#cv2.destroyAllWindows()
# After the loop release the cap object
vid.release()
