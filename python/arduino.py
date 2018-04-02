#!/usr/bin/python
# coding: utf-8

"""
 Drivers Arduino.

 Diego de los Reyes Rodríguez.
 v1.0 Diciembre 2014
"""
import serial
import ConfigParser

#ATTRIBUTES

# Serial device
ser = ''

# Position of the servo
position = 90

# Amount of light
light = -1
 
#END ATTRIBUTES

#ACTIONS

'''
Starts the communication and set the position of the servo
'''
def init():
	global ser
	cfg = ConfigParser.ConfigParser()
	cfg.read(["config.cfg"])
	port = cfg.get("arduino", "port")
	ser = serial.Serial(port, 9600) # send serial data to Arduino
	moveCenter()

'''
Turns right the servo
'''
def moveRight():
	global ser
	ser.write('a')

'''
Turns left the servo
'''
def moveLeft():
	global ser
	ser.write('d')

'''
Center the servo
'''
def moveCenter():
	global ser
	ser.write('x')

'''
Gets the current position of the servo
'''
def getPosition():
	global position
	return float(position)

'''
Gets the amount of light
'''
def getLight():
	global light
	return int(light)

'''
Updates the information of the sensors
'''
def updateSensors():
	global light
	global position
	ser.write('o')
	ser.write('p')
	message = ''
	while ser.inWaiting() > 0:
		message = ser.readline().split(":")
		if message[0] == "Light":
			light = message[1]
		elif message[0] == "Cam":
			position = message[1]
			
		message = ''

'''
Close the communication
'''
def quit():
	ser.close()

#END ACTIONS