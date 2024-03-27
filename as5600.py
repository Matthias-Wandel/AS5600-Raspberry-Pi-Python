#!/usr/bin/python3
# Very simple code to read AS5600 magnetic encoder with Python
# on raspberry pi
#
# Requires Python smbus module.  Get it using:
#     sudo apt-get install python3-smbus
#
# Make sure Pi's I2c is enabled using
#     sudo raspi-config
#
# Connect Pi's ground to GND and DIR pins
# Connect Pi's 3.3 volts to VCC on AS5600
# Connect Pi's I2c SCL (pin 5) to AS5600 SCL pin
# Connect Pi's I2c SDA (pin 5) to AS5600 SDA pin

import smbus, time, sys, math

#=====================================================================
# Code to read AS5600.  9 lines of python is all it takes.
import smbus
DEVICE_AS5600 = 0x36 # Default device I2C address
bus = smbus.SMBus(1)

def ReadRawAngle(): # Read angle (0-360 represented as 0-4096)
  read_bytes = bus.read_i2c_block_data(DEVICE_AS5600, 0x0C, 2)
  return (read_bytes[0]<<8) | read_bytes[1];

def ReadMagnitude(): # Read magnetism magnitude
  read_bytes = bus.read_i2c_block_data(DEVICE_AS5600, 0x1B, 2)
  return (read_bytes[0]<<8) | read_bytes[1];

#=====================================================================

xcenter = 60 # Assume center of text screen is 60 across, 30 down.
ycenter = 30 # if your screen is 80x50, change to 40 and 25.

def MoveCursor(x,y):
    print("\033[%d;%dH"%(y,x),end="")

# Clear screen
print("\033[2J",end="")


# Draw x and y axis on screen
for a in range (-ycenter, ycenter):
    MoveCursor(xcenter, ycenter+a)
    print("|", end="")

for a in range (-xcenter, xcenter):
    MoveCursor(xcenter+a, ycenter)
    print("-")



histlen = 400
hist_index = 0
hist = [(0,0)] * histlen

while True:
    raw_angle = ReadRawAngle()
    magnitude = ReadMagnitude()

    MoveCursor(0,0)
    print("Raw angle: %4d"%(raw_angle), "m=%4d"%(magnitude), "%6.2f deg  "%(raw_angle*360.0/4096))

    # Now plot X and Y position by graphing on the screen
    xymag = magnitude/1024.0
    cx = int(xcenter+xcenter*xymag*math.cos(raw_angle*math.pi/2048))
    cy = int(ycenter+ycenter*xymag*math.sin(raw_angle*math.pi/2048))

    # delete old mark (keep up to 400 on screen)
    oldpos = hist[hist_index]
    MoveCursor(*oldpos)
    if oldpos[0] == xcenter:
        print("|",end="")
    elif oldpos[1] == ycenter:
        print("-",end="")
    else:
        print(" ",end="")

    # Save new mark positon in array
    hist[hist_index] = (cx,cy)
    hist_index += 1;
    if hist_index >= histlen: hist_index = 0

    # Draw a '#' at the computed X,Y coordinate
    MoveCursor(cx,cy)
    print("#",end="")

    #time.sleep(0.02)



