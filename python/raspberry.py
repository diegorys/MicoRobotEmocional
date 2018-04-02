#!/usr/bin/python
# coding: utf-8

"""
 Drives GPIO ports of the Raspberry Pi.

 Diego de los Reyes Rodríguez.
 v1.0 Diciembre 2014
"""
import RPi.GPIO as GPIO
import time
import ConfigParser

#ATTRIBUTES

# Port of the led
led = 0
 
#END ATTRIBUTES

#ACTIONS

'''
Starts the gpio port
'''
def init():
	global led
	cfg = ConfigParser.ConfigParser()
	cfg.read(["config.cfg"])
	led = int(cfg.get("raspberry", "port"))

	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(led, GPIO.OUT)

'''
Alerts ok action
'''
def alertOk():
	global led
	GPIO.output(led, True)
	time.sleep(1)
	GPIO.output(led, False)

'''
Alerts ko action
'''
def alertKo():
	global led
	GPIO.output(led, True)
	time.sleep(0.2)
	GPIO.output(led, False)
	time.sleep(0.2)
	GPIO.output(7, True)
	time.sleep(0.2)
	GPIO.output(7, False)

'''
Cleans up the gpio ports
'''
def quit():
	GPIO.cleanup()

#END ACTIONS