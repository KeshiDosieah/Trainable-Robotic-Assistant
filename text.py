#! /usr/bin/env python3
import serial
import time
import sys
# create a file
file = open("angle.txt", "w")

angles = sys.argv[1] + "," + sys.argv[2] + "," + sys.argv[3] + "," + sys.argv[4] + "\n"
file.write(angles)
print(angles)
arduino = serial.Serial('/dev/ttyACM0', 9600)

arduino.write(angles.encode())
time.sleep(1)
