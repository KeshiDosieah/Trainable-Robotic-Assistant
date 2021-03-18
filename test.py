#! /usr/bin/env python3
import matplotlib.pyplot
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
from mpl_toolkits.mplot3d import Axes3D
my_chain = Chain.from_urdf_file("my_robot.urdf")
ax = matplotlib.pyplot.figure().add_subplot(111, projection='3d')

my_chain.plot(my_chain.inverse_kinematics([0.02, 0.02, 0.02]), ax)
matplotlib.pyplot.show()
