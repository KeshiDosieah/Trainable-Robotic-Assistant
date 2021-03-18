#! /usr/bin/env python3
import serial
import time
# create a file
file = open("angle.txt", "r")

for line in file:
  fields = line.split(",")
  angle1 = fields[0]
  angle2 = fields[1]
  angle3 = fields[2]
  angle4 = fields[3]

angles = angle1 + "," + angle2 + "," + angle3 + "," + angle4
print(angles)
arduino = serial.Serial('/dev/ttyACM0', 9600)
while True:
    arduino.write(angles.encode())
    time.sleep(1)
# arduino.close()
