#!/usr/bin/python
# coding: utf-8

"""
 Main.

 Diego de los Reyes Rodríguez.
 v1.0 Diciembre 2014
"""
import mico
import signal

'''
Closes the program
'''
def quitHandler(signal, frame):
	mico.sleep()

#End block

'''
Main function
'''
def main():
	#Capture signal Ctrl+C
	signal.signal(signal.SIGINT, quitHandler)

	mico.wake()
	mico.live()
	mico.sleep()

main()
