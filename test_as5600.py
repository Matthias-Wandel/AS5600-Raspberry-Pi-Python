#!/usr/bin/python3
# Code I used to test accuracy of AS5600 agaisnt stepper motor, and 
# stepper motor accuracy against AS4500 chip
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

import time, sys, math
import RPi.GPIO as GPIO

#===============================================================
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

#===============================================================
# Code to control stepper motor
   
def init_motor(motor):
    global line_clock, line_dir, line_enable

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    if motor:
        line_clock  = 23
        line_dir    = 24
        line_enable = 25
    else:
        line_clock  = 26
        line_dir    = 19
        line_enable = 13

    GPIO.setup(line_enable, GPIO.OUT, initial=False) # Start enabled
    GPIO.setup(line_dir,    GPIO.OUT, initial=False)
    GPIO.setup(line_clock,  GPIO.OUT, initial=False)
    
    if motor == 0: time.sleep(0.5) # this one takes a while to wake up.

def DoSteps(steps, delay = 1):
    global line_clock, line_dir, line_enable
    duse = delay/1000
    GPIO.output(line_enable, 0) # enable
    
    if steps < 0:
        steps = -steps
        GPIO.output(line_dir, False)
    else:
        GPIO.output(line_dir, True)
    
    for x in range (0,steps):
        GPIO.output(line_clock, True)
        #time.sleep(duse)
        GPIO.output(line_clock, False)
        time.sleep(duse)

#===============================================================
# Code to move cursor

def MoveCursor(x,y):
    print("\033[%d;%dH"%(y,x),end="")

def ClearScreen():
    print("\033[2J",end="")

#===============================================================
init_motor(1)

if 0:
    # check the motor
    print("do steps")
    DoSteps(200*8*5) # full turn.
    sys.exit()


raw_angle_start = ReadRawAngle()
StepCount = 0
print("raw_angle_start = ",raw_angle_start);

of = open("angles.csv","w");

while True:
    time.sleep(0.1)
    raw_angle = ReadRawAngle()
    magnitude = ReadMagnitude()

    SensorAngle = (raw_angle+4096-raw_angle_start) & 4095;
    SensorAngleDeg = (SensorAngle * 360.0)/4096;
    MotorAngleDeg = StepCount * 360.0 / (200*8) # 8x microstepping

    mag = magnitude/4096.0
    diff = SensorAngleDeg-MotorAngleDeg
    if diff >= 360: diff -= 360
    if diff <= -360: diff += 360
    print ("%6.2f,%6.2f, %5.3f  d=%5.3f"%(MotorAngleDeg, SensorAngleDeg, mag, diff))
    print ("%6.2f,%6.2f, %5.3f"%(MotorAngleDeg, SensorAngleDeg, mag), file=of)

    increment = 1
    DoSteps(increment)
    StepCount += increment
    if StepCount > 200*8: StepCount -= 200*8



