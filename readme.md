<html>
<h1>Connecting AS5600 magnetic encoder to Raspberry Pi</h1>
<img src="breadboard.jpg">
This turns out to be quite simple, but I foudn no examples for it on the internet,
so I decided to add this github page so others can find it.
<p>
<b>Connections:
<table>
<tr><th>Pi pin<th>Pi function<th>AS5600 board
<tr><td>01<td>3.3V DC power<td>VCC
<tr><td>03<td>GPIO 02 / I2C SDA<td>SDA
<tr><td>05<td>GPIO 03 / I2C SCL<td>SCL
<tr><td>09<td>Ground<td>GROUND<br>and DIR
</table>
<img src="schematic.jpg">
The actual code to talk to the AS5600 chip is just 9 lines of python:
<pre>
import smbus
DEVICE_AS5600 = 0x36 # Default device I2C address
bus = smbus.SMBus(1)

def ReadRawAngle(): # Read angle (0-360 represented as 0-4096)
  read_bytes = bus.read_i2c_block_data(DEVICE_AS5600, 0x0C, 2)
  return (read_bytes[0]<<8) | read_bytes[1];

def ReadMagnitude(): # Read magnetism magnitude
  read_bytes = bus.read_i2c_block_data(DEVICE_AS5600, 0x1B, 2)
  return (read_bytes[0]<<8) | read_bytes[1];
</pre>

This code is contained in several stand alone python programs in this
repository which I used for testing the AS5600 chip.
<p>
I used a stepper motor to rotate the magnet to check for accuracy.

