#! /usr/bin/env python3

from klampt import *
from klampt.model import ik
from math import radians, degrees
import numpy as np

#target_point = [2.4,0,0.05]
local_point = [1.12,0,0]
local_point2 = [1.1,0,0]
#you will need to change this to the absolute or relative path to Klampt-examples
KLAMPT_EXAMPLES = 'Klampt-examples'

def IK(target_point,alignment,visualization=False):
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
        if(solver.solve()) or True:
            print([degrees(x) for x in robot.getConfig()])
            print(solver.getResidual())
            if visualization:
                vis.add("world",w)    #shows the robot in the solved configuration
                vis.add("local point",link.getWorldPosition(local_point))
                vis.setAttribute("local point","type","Vector3")  #usually the vis module identifies a Config vs a Vector3, but this robot has exactly 3 links
                vis.add("target point",target_point)
                vis.setAttribute("target point","type","Vector3")
                vis.setColor("target point",1,0,0)  #turns the target point red
                vis.show()  #this will pop up the visualization window until you close it
                vis.spin(float('inf'))

    elif alignment == "vertical":
        target_point2 = [target_point[0],target_point[1],target_point[2]+0.02]
        print(target_point2)
        obj = ik.objective(link,local=[local_point, local_point2],world=[target_point, target_point2])
        solver = ik.solver(obj,iters=10000,tol=0.05)
        solver.sampleInitial()
        print(solver.solve())
        if(solver.solve()) or True:
            print([degrees(x) for x in robot.getConfig()])
            print(solver.getResidual())
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
        obj = ik.objective(link,local=local_point,world=target_point)
        solver = ik.solver(obj,iters=10000,tol=0.05)
        solver.sampleInitial()
        print(solver.solve())
        if(solver.solve()) or True:
            print([degrees(x) for x in robot.getConfig()])
            print(solver.getResidual())
            if visualization:
                vis.add("world",w)    #shows the robot in the solved configuration
                vis.add("local point",link.getWorldPosition(local_point))
                vis.setAttribute("local point","type","Vector3")  #usually the vis module identifies a Config vs a Vector3, but this robot has exactly 3 links
                vis.add("target point",target_point)
                vis.setAttribute("target point","type","Vector3")
                vis.setColor("target point",1,0,0)  #turns the target point red
                vis.show()  #this will pop up the visualization window until you close it
                vis.spin(float('inf'))

#IK(target_point,"horizontal",visualization=True)
