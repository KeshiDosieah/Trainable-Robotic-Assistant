#!/usr/bin/env python
import serial

arduino = serial.Serial('/dev/ttyACM0', 9600)
while True:
    angle_data = str(arduino.readline())
    print(angle_data)
