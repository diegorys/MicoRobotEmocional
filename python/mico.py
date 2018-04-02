#!/usr/bin/python
# coding: utf-8

"""
 Emotional robot MiCo

 Diego de los Reyes Rodríguez.
 v1.0 Diciembre 2014
"""
import ConfigParser
import sys
import random
import expressions
import gmail
import time
import arduino
import raspberry
import webcam
import os

#CONSTANTS

# Time refresh
REFRESH_TIME = 0.5

#Commands
COMMAND_TAKE_PICTURE 	= "Comando foto"
COMMAND_MOVE_RIGHT 	= "Comando derecha"
COMMAND_MOVE_LEFT 	= "Comando izquierda"
COMMAND_MOVE_CENTER	= "Comando centrar"
COMMAND_EXIT		= "Comando salir"

#END CONSTANTS

#ATTRIBUTES

#Check if the robot is awake
isAwake = False

#Num of orders
numOrders = 0

#Num of errors
numErrors = 0

#Num of pictures
numPictures = 0

#Num of normal cycles
numNormalCycles = 0

#Num of memory cycles
numMemoryCycles = 0

#Personality
boredom_threshold = 0
shame_threshold = 0
anger_threshold = 0
sick_threshold = 0
darkness_threshold = 0
luminosity_threshold = 0
photographer_threshold = 0
memory_threshold = 0

#Mail to send pictures
mailto = ''

#END ATTRIBUTES

#ACTIONS

'''
Takes a photo and saves it
'''
def takePicture():
	global numPictures
	global mailto

	numPictures += 1
	webcam.takePicture()
	gmail.send(mailto, "Foto sacada por MiCo", "MiCo ha sacado la foto adjunta a petición del usuario.")

'''
Moves the webcam to the right
'''
def moveRight():
	arduino.moveRight()

'''
Moves the webcam to the left
'''
def moveLeft():
	arduino.moveLeft()

'''
Moves the webcam to the center
'''
def moveCenter():
	arduino.moveCenter()

#END ACTIONS

#MiCo

'''
Wakes up to the robot.
'''
def wake():
	global isAwake

	global boredom_threshold
	global shame_threshold
	global anger_threshold
	global sick_threshold
	global darkness_threshold
	global luminosity_threshold
	global photographer_threshold
	global memory_threshold

	global mailto

	expressions.init()
	arduino.init()
	gmail.init()
	raspberry.init()
	webcam.init()

	cfg = ConfigParser.ConfigParser()
	cfg.read(["config.cfg"])

	boredom_threshold = int(cfg.get("personality", "boredom_threshold"))
	shame_threshold = int(cfg.get("personality", "shame_threshold"))
	anger_threshold = int(cfg.get("personality", "anger_threshold"))
	sick_threshold = int(cfg.get("personality", "sick_threshold"))
	darkness_threshold = int(cfg.get("personality", "darkness_threshold"))
	luminosity_threshold = int(cfg.get("personality", "luminosity_threshold"))
	photographer_threshold = int(cfg.get("personality", "photographer_threshold"))
	memory_threshold = int(cfg.get("personality", "memory_threshold"))

	mailto = cfg.get("gmail", "mailto")

	print memory_threshold
	print mailto

	isAwake = True

'''
Lifecycle
'''
def live():
	global isAwake

	while isAwake:
		executeCommands()
		if isAwake:
			feelEmotions()
			resetMemory()
			arduino.updateSensors()
			updateEyes()
			expressions.refresh()
			isAwake = expressions.isAlive()
			time.sleep(REFRESH_TIME)

'''
Executes orders
'''
def executeCommands():
	global numOrders
	global numErrors

	messages = gmail.receive()

	if len(messages) <= 0:
		numOrders = 0
	
	#Checks the emails
	for msg in messages:
		command = msg["subject"]
		print "Recibido: ",command
		numOrders += 1
		try:
			raspberry.alertOk()
			res = actions[command]()
			print "OK"
		except:
			numErrors += 1
			print "Error ",command,": ",sys.exc_info()[0]
			raspberry.alertKo()
	
'''
Emotion engine
'''
def feelEmotions():
	global numNormalCycles
	global boredom_threshold

	if not feelLight():
		if not feelErrors():
			if not feelOrders():
				if not feelPictures():
					numNormalCycles += 1
					if numNormalCycles < boredom_threshold:
						expressions.setEmotion(expressions.EXPRESION_NORMAL)
						expressions.setText("")
					else:
						# If I don't do nothing, I'm bored
						expressions.setEmotion(expressions.EXPRESION_ABURRIDO)
						expressions.setText("¡Me aburro!")

	expression = expressions.getEmotion()

	# If I do something I'm not bored
	if expression != expressions.EXPRESION_NORMAL and expression != expressions.EXPRESION_ABURRIDO:
		numNormalCycles = 0

'''
Determines whether the orders affects the robot
'''
def feelErrors():
	global shame_threshold

	affect = False
	
	if numErrors > shame_threshold:
		affect = True
		expressions.setEmotion(expressions.EXPRESION_AVERGONZADO)
		expressions.setText("Upss... Ha habido un error... ¡Qué vergüenza!")

	return affect

'''
Determines whether the orders affects the robot
'''
def feelOrders():
	global numOrders
	global anger_threshold
	global sick_threshold

	affect = False
	
	if numOrders > sick_threshold:
		affect = True
		expressions.setEmotion(expressions.EXPRESION_ENFERMO)
		expressions.setText("Estoy agotado...")
	if numOrders > anger_threshold:
		affect = True
		expressions.setEmotion(expressions.EXPRESION_ENFADADO)
		expressions.setText("¡Deja de mandarme cosas!")
	elif numOrders > 0:
		affect = True
		expressions.setEmotion(expressions.EXPRESION_PENSATIVO)
		expressions.setText("A ver qué me has pedido...")

	return affect

'''
Determines whether the light affects the robot
'''
def feelLight():
	global darkness_threshold
	global luminosity_threshold

	affect = False

	light = arduino.getLight()

	if light < darkness_threshold and light >= 0:
		affect = True
		expressions.setEmotion(expressions.EXPRESION_ASUSTADO)
		expressions.setText("¡Qué miedo, no hay luz!")
	elif light > luminosity_threshold:
		affect = True
		expressions.setEmotion(expressions.EXPRESION_ATURDIDO)
		expressions.setText("¡Me está dando toda la luz en la cara!")

	return affect

'''
Determines whether the photos affects the robot
'''
def feelPictures():
	global numPictures
	global photographer_threshold

	affect = False
	
	if numPictures > photographer_threshold:
		affect = True
		expressions.setEmotion(expressions.EXPRESION_ENAMORADO)
		expressions.setText("¡Cuántas fotos!")
	elif numPictures > 0:
		affect = True
		expressions.setText("¡Me gustan las fotos!")
		expressions.setEmotion(expressions.EXPRESION_FELIZ)

	return affect

'''
Resets the memory of the robot
'''
def resetMemory():
	global numMemoryCycles
	global numPictures
	global numOrders
	global numErrors
	global memory_threshold

	numMemoryCycles += 1

	if numMemoryCycles > memory_threshold:
		numPictures = resetPositiveParam(numPictures)
		numOrders   = resetPositiveParam(numOrders)
		numErrors   = resetPositiveParam(numErrors)
		numMemoryCycles = 0

'''
Subtrats one. If the number is negative, set zero.
'''
def resetPositiveParam(x):
	x -= 1
	if x < 0:
		x = 0
	return x

'''
Moves the eyes depending of the light
'''
def updateEyes():
	position = arduino.getPosition()
	x = (2*position/180)-1.0;
	expressions.setEyes(x, 0)

'''
Stops the robot and goes to sleep
'''
def sleep():
	global isAwake
	isAwake = False
	arduino.quit()
	expressions.quit()
	gmail.quit()
	raspberry.quit()
	webcam.quit()
	os._exit(1)

actions = {COMMAND_MOVE_RIGHT: 	 moveRight,
	   COMMAND_MOVE_CENTER:  moveCenter,
	   COMMAND_MOVE_LEFT: 	 moveLeft,
	   COMMAND_TAKE_PICTURE: takePicture,
	   COMMAND_EXIT: 	 sleep}

#End MiCo