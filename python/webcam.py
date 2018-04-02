#!/usr/bin/python
# coding: utf-8

"""
 Controls the webcam.

 Diego de los Reyes Rodríguez.
 v1.0 Diciembre 2014
"""

from subprocess import call

#ACTIONS

'''
Inits the webcam
'''
def init():
	return True

'''
Takes and save a photo
'''
def takePicture():
	call(["fswebcam", "-r 640x480", "foto.jpg"])

'''
Close the webcam
'''
def quit():
	return True

#END ACTIONS