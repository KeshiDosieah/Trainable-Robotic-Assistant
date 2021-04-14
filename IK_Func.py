#!/usr/bin/env python

from klampt import *
from klampt import vis
from klampt.model import ik
from math import radians, degrees
import numpy as np
import sys
from time import sleep
import serial

final_version = False
# sleep(3)
#target_point = [2.4,0,0.05]
local_point = [1.12,0,0]
local_point2 = [1.1,0,0]

def IK(target_point,alignment,visualization=False):
    global final_version
    w = WorldModel()
    if not w.readFile("myworld.xml"):
        raise RuntimeError("Couldn't read the world file")

    robot= w.robot(0)

    if visualization:
        vis.add("ghost",w.robot(0).getConfig(),color=(0,1,0,0.5))
        robot.setConfig([0,0,0,0])
        vis.add("ghost2",w.robot(0).getConfig(),color=(1,0,0,0.5))

    link = robot.link(3)

    if alignment == "horizontal":
        vec = np.array([target_point[0],target_point[1]])
        dist = np.linalg.norm(vec)
        pt2 = vec - vec/dist*0.02
        target_point2 = [pt2[0], pt2[1], target_point[2]]
        obj = ik.objective(link,local=[local_point, local_point2],world=[target_point, target_point2])
        solver = ik.solver(obj,iters=10000,tol=0.05)
        solver.sampleInitial()
        print(solver.solve())
        if(solver.solve()) or final_version:
            print([degrees(x) for x in robot.getConfig()])        
            if visualization:
                vis.add("world",w)    #shows the robot in the solved configuration
                vis.add("local point",link.getWorldPosition(local_point))
                vis.setAttribute("local point","type","Vector3")  #usually the vis module identifies a Config vs a Vector3, but this robot has exactly 3 links
                vis.add("target point",target_point)
                vis.setAttribute("target point","type","Vector3")
                vis.setColor("target point",1,0,0)  #turns the target point red
                vis.show()  #this will pop up the visualization window until you close it
                vis.spin(float('inf'))
            else:
                return ([degrees(x) for x in robot.getConfig()])
        else:
            raise RuntimeError("Cannot reach position")

    elif alignment == "vertical":
        target_point2 = [target_point[0],target_point[1],target_point[2]+0.02]
        print(target_point2)
        obj = ik.objective(link,local=[local_point, local_point2],world=[target_point, target_point2])
        solver = ik.solver(obj,iters=10000,tol=0.05)
        solver.sampleInitial()
        print(solver.solve())
        if(solver.solve()) or final_version:
            print([degrees(x) for x in robot.getConfig()])
            if visualization:
                vis.add("world",w)    #shows the robot in the solved configuration
                vis.add("local point",link.getWorldPosition(local_point))
                vis.setAttribute("local point","type","Vector3")  #usually the vis module identifies a Config vs a Vector3, but this robot has exactly 3 links
                vis.add("target point",target_point)
                vis.setAttribute("target point","type","Vector3")
                vis.setColor("target point",1,0,0)  #turns the target point red
                vis.show()  #this will pop up the visualization window until you close it
                vis.spin(float('inf'))
            else:
                return ([degrees(x) for x in robot.getConfig()])
        else:
            raise RuntimeError("Cannot reach position")
    else:
        obj = ik.objective(link,local=local_point,world=target_point)
        solver = ik.solver(obj,iters=10000,tol=0.05)
        solver.sampleInitial()
        print(solver.solve())
        if(solver.solve()) or final_version:
            print([degrees(x) for x in robot.getConfig()])
            if visualization:
                vis.add("world",w)    #shows the robot in the solved configuration
                vis.add("local point",link.getWorldPosition(local_point))
                vis.setAttribute("local point","type","Vector3")  #usually the vis module identifies a Config vs a Vector3, but this robot has exactly 3 links
                vis.add("target point",target_point)
                vis.setAttribute("target point","type","Vector3")
                vis.setColor("target point",1,0,0)  #turns the target point red
                vis.show()  #this will pop up the visualization window until you close it
                vis.spin(float('inf'))
            else:
                return ([degrees(x) for x in robot.getConfig()])
        else:
            raise RuntimeError("Cannot reach position")

def getPosition():
    w = WorldModel()
    if not w.readFile("myworld.xml"):
        raise RuntimeError("Couldn't read the world file")

    robot= w.robot(0)
    file = open("angle.txt", "r")
    for line in file:
      fields = line.split(",")
      angle1 = radians(float(fields[0]))
      angle2 = radians(float(fields[1]))
      angle3 = radians(float(fields[2]))
      angle4 = radians(float(fields[3]))
    file.close()

    robot.setConfig([angle1,angle2,angle3,angle4])

    link = robot.link(3)

    return link.getWorldPosition(local_point)


if __name__ == "__main__":
    arduino = serial.Serial('/dev/ttyACM0', 115200)
    file = open("angle.txt", "r")
    for line in file:
      fields = line.split(",")
      angle1 = float(fields[0])
      angle2 = float(fields[1])
      angle3 = float(fields[2])
      angle4 = float(fields[3])
    file.close()

    if sys.argv[1] == "0":
        angles = IK([float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4])],"horizontal")
    elif sys.argv[1] == "1":
        angles = IK([float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4])],"vertical")
    elif sys.argv[1] == "2":
        angles = IK([float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4])],"")
    else:
        raise RuntimeError("Wrong syntax")

    angle_diff1 = angles[0] - angle1
    angle_diff2 = angles[1] - angle2
    angle_diff3 = angles[2] - angle3
    angle_diff4 = angles[3] - angle4
    angle_diff = str(angle_diff1) + "," + str(angle_diff2) + "," + str(angle_diff3) + "," + str(angle_diff4) + "\n"
    arduino.write(angle_diff)
    print(angle_diff)

    file = open("angle.txt", "w")
    file.write("{},{},{},{}\n".format(angles[0],angles[1],angles[2],angles[3]))
    file.close()

    print(getPosition())
