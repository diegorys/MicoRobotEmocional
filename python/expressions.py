#!/usr/bin/python
# coding: utf-8

"""
 Emotion expressions.

 Diego de los Reyes Rodríguez.
 v1.0 Diciembre 2014
"""
import random
import pygame
import imaplib
import time
import signal
import sys
import os

#Definimos algunos colores
NEGRO 	= (0, 0, 0)
BLANCO 	= (255, 255, 255)

# Definimos las expresiones
EXPRESION_ABURRIDO		= 0
EXPRESION_ASUSTADO		= 1
EXPRESION_ATURDIDO		= 2
EXPRESION_AVERGONZADO		= 3
EXPRESION_CONFUNDIDO		= 4
EXPRESION_ENAMORADO		= 5
EXPRESION_ENFADADO		= 6
EXPRESION_ENFERMO		= 7
EXPRESION_FELIZ			= 8
EXPRESION_HAMBRIENTO		= 9
EXPRESION_NORMAL		= 10
EXPRESION_NOSTALGICO		= 11
EXPRESION_PENSATIVO		= 12
EXPRESION_SOMNOLIENTO 		= 13
EXPRESION_SORPRENDIDO 		= 14
EXPRESION_TRISTE 		= 15

# Movimiento de los ojos
POS_OJO_DERECHO		= 94
POS_OJO_IZQUIERDO	= 363
POS_OJO_Y		= 114
DESPLAZAMIENTO_OJO 	= 30

#Attributes
 
# Creamos una pantalla de 480x360 para la cara.
pantalla = pygame.display.set_mode([480, 360], pygame.FULLSCREEN)
 
# Establecemos el nombre de la ventana.
pygame.display.set_caption('Emociones')
 
reloj = pygame.time.Clock()
 
# Establecemos la posición de los gráficos
posicion_base = [0, 0]
 
# Carga y sitúa los gráficos.
expresiones = []
expresiones.append(pygame.image.load("expresiones/aburrido.jpg").convert())
expresiones.append(pygame.image.load("expresiones/asustado.jpg").convert())
expresiones.append(pygame.image.load("expresiones/aturdido.jpg").convert())
expresiones.append(pygame.image.load("expresiones/avergonzado.jpg").convert())
expresiones.append(pygame.image.load("expresiones/confundido.jpg").convert())
expresiones.append(pygame.image.load("expresiones/enamorado.jpg").convert())
expresiones.append(pygame.image.load("expresiones/enfadado.jpg").convert())
expresiones.append(pygame.image.load("expresiones/enfermo.jpg").convert())
expresiones.append(pygame.image.load("expresiones/feliz.jpg").convert())
expresiones.append(pygame.image.load("expresiones/hambriento.jpg").convert())
expresiones.append(pygame.image.load("expresiones/normal.jpg").convert())
expresiones.append(pygame.image.load("expresiones/nostalgico.jpg").convert())
expresiones.append(pygame.image.load("expresiones/pensativo.jpg").convert())
expresiones.append(pygame.image.load("expresiones/somnoliento.jpg").convert())
expresiones.append(pygame.image.load("expresiones/sorprendido.jpg").convert())
expresiones.append(pygame.image.load("expresiones/triste.jpg").convert())

expresion = EXPRESION_NORMAL
eyes_x = 0
eyes_y = 0
font = ''
message = ''

alive = False

#Block Actions

def init():
	global font
	global alive

	pygame.init()
	font = pygame.font.Font(None, 20)
	alive = True

def setEmotion(emotion):
	global expresion
	expresion = emotion

def getEmotion():
	global expresion
	return expresion

def setText(text):
	global message
	message = unicode(text, "UTF-8")

def setEyes(x, y):
	global eyes_x
	global eyes_y
	eyes_x = x
	eyes_y = y

def isAlive():
	global alive
	return alive

def refresh():
	global expresion
	global eyes_x
	global eyes_y
	global message
	global alive

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			alive = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				alive = False

	pantalla.blit(expresiones[expresion], posicion_base)

	#Dibujamos una elipse sólida, usando un rectángulo para definir sus bordes.
	pygame.draw.ellipse(pantalla, NEGRO, [POS_OJO_DERECHO+(DESPLAZAMIENTO_OJO*eyes_x), POS_OJO_Y+(DESPLAZAMIENTO_OJO*eyes_y), 20, 20]) 
	pygame.draw.ellipse(pantalla, NEGRO, [POS_OJO_IZQUIERDO+(DESPLAZAMIENTO_OJO*eyes_x), POS_OJO_Y+(DESPLAZAMIENTO_OJO*eyes_y), 20, 20])

	label = font.render(message, 1, NEGRO)
	pantalla.blit(label, (40, 330))

	pygame.display.flip()

def quit():
	pygame.quit ()

#End block Actions