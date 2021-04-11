#! /usr/bin/env python3
import matplotlib.pyplot
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
from mpl_toolkits.mplot3d import Axes3D
import sys
import math
import numpy as np
import serial
import time

ax = matplotlib.pyplot.figure().add_subplot(111, projection='3d')
# ax.set_aspect('equal')

my_chain = Chain(name='OWI-535', links=[
    OriginLink(),
    URDFLink(
      name="base_link",
      translation_vector=[0, 0, 0],
      orientation=[0, 0, 0],
      rotation=[0, 0, 1],
      bounds=[-120/180*math.pi,120/180*math.pi],
    ),
    URDFLink(
      name="link1",
      translation_vector=[0, 0, 4.5],
      orientation=[0, 0, 0],
      rotation=[0, 1, 0],
      bounds=[-100/180*math.pi,-45/180*math.pi],
    ),
    URDFLink(
      name="link2",
      translation_vector=[9, 0, 0],
      orientation=[0, 0, 0],
      rotation=[0, 1, 0],
      bounds=[-130/180*math.pi,130/180*math.pi],
    ),
    URDFLink(
      name="link3",
      translation_vector=[11.1, 0, 0],
      orientation=[0, 0, 0],
      rotation=[0, 1, 0],
      bounds=[-60/180*math.pi,60/180*math.pi],
    ),
    URDFLink(
      name="link4",
      translation_vector=[11.5, 0, 0],
      orientation=[0, 0, 0],
      rotation=[0, 0, 0],
    )
])

file = open("angle.txt", "r")

for line in file:
  fields = line.split(",")
  angle1 = fields[0]
  angle2 = fields[1]
  angle3 = fields[2]
  angle4 = fields[3]

file.close()

Joint_positions = my_chain.inverse_kinematics([sys.argv[1], sys.argv[2], sys.argv[3]])
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
m5 = float("{0:.3f}".format(np.rad2deg(Joint_positions[1])-float(angle1)))
m4 = float("{0:.3f}".format(np.rad2deg(Joint_positions[2])-float(angle2)))
m3 = float("{0:.3f}".format(np.rad2deg(Joint_positions[3])-float(angle3)))
m2 = float("{0:.3f}".format(np.rad2deg(Joint_positions[4])-float(angle4)))

print("Joint angles (deg):", end ="\t")
print(np.rad2deg(Joint_positions[1:5]))
print(m5)
print(m4)
print(m3)
print(m2)
print("Position xyz (cm):", end ="\t")
print(my_chain.forward_kinematics(Joint_positions)[:3,3])
my_chain.plot(Joint_positions, ax)
angles = str(m5) + "," + str(m4) + "," + str(m3) + "," + str(m2) + "\n"
# arduino = serial.Serial('/dev/ttyACM3', 9600)
# time.sleep(1)
#
# arduino.write(angles.encode())
# time.sleep(1)

M5 = float("{0:.3f}".format(np.rad2deg(Joint_positions[1])))
M4 = float("{0:.3f}".format(np.rad2deg(Joint_positions[2])))
M3 = float("{0:.3f}".format(np.rad2deg(Joint_positions[3])))
M2 = float("{0:.3f}".format(np.rad2deg(Joint_positions[4])))
updated_angle = str(M5) + "," + str(M4) + "," + str(M3) + "," + str(M2) + "\n"

#file = open("angle.txt", "w")
#file.write(updated_angle)
matplotlib.pyplot.show()
