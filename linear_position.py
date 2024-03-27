#!/usr/bin/python3
# Code I used to show linear position with my lego rack and pinion
# to turn magnet against AS5600 chip.


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
def MoveCursor(x,y):
    print("\033[%d;%dH"%(y,x),end="")

def ClearScreen():
    print("\033[2J",end="")


#ClearScreen()

cx = 0
ext_angle = 2048;
while True:
    
    raw_angle = 4095-ReadRawAngle()
    magnitude = ReadMagnitude()
    
    # If the encoder values wraps around, don't jump back, just keep going linearly.
    delta = (raw_angle-ext_angle) %4095
    if delta > 2048: delta -= 4096
    ext_angle = ext_angle+delta
    
    ocx = cx
    cx = ext_angle*130/4096+1
    if cx < 1: cx = 1
    
    MoveCursor(0,50)
    print("Raw angle: %4d"%(raw_angle), "m=%4d"%(magnitude))

    # Move a square across the screen to show position
    for l in range(0,8):
        # Erase at old position
        MoveCursor(ocx,l+52)
        print("           ", end="")
        
        # Draw at new position
        MoveCursor(cx,l+52)
        print("###########", end="");
    




