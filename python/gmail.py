#!/usr/bin/python
# coding: utf-8

"""
 Sends and receives emails using Gmail.

 Diego de los Reyes Rodríguez.
 v1.0 Diciembre 2014
"""
import imaplib
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import email
import time
import ConfigParser

from subprocess import call

#ATTRIBUTES

#Username of the gmail account of the robot
user = ''

#END ATTRIBUTES

#ACTIONS

'''
Log in gmail
'''
def init():
	global imapClient
	global mailServer
	global user

	cfg = ConfigParser.ConfigParser()
	cfg.read(["config.cfg"])
	user = cfg.get("gmail", "user")
	password = cfg.get("gmail", "password")

	# Connect
	imapClient = imaplib.IMAP4_SSL("imap.gmail.com")
	mailServer = smtplib.SMTP("smtp.gmail.com", 587)

	mailServer.ehlo()
	mailServer.starttls()
	mailServer.ehlo()

	# Login
	imapClient.login(user, password)
	mailServer.login(user, password)

'''
Returns the unread messages
'''
def receive():
	global imapClient

	# Choose folder inbox
	imapClient.select("INBOX")

	# Fetch unseen messages
	_, message_ids = imapClient.search(None, "UNSEEN")

	mails = []

	for msg_id in message_ids[0].split():
		# Download the message
		_, data = imapClient.fetch(msg_id, "(RFC822)")
	        # Parse data using email module
		msg = email.message_from_string(data[0][1])
		mails.append(msg)	

	return mails

'''
Send a message with a picture
'''
def send(mailTo, subject, body):
	global mailServer
	global user

	#Create message
	message = MIMEMultipart()
	message["From"] = user
	message["To"]	= mailTo
	message["Subject"] = subject

	#Attach the text
	text = MIMEText(body)
	message.attach(text)

	#Attach the picture
	file = open("foto.jpg", "rb")
	content = MIMEImage(file.read())
	content.add_header('Content-Disposition', 'attachment; filename = "foto.jpg"')
	message.attach(content)

	#Send
	mailServer.sendmail(message["From"], message["To"], message.as_string())

'''
Close the connection
'''
def quit():
	global imapClient
	global mailServer

	imapClient.close()
	imapClient.logout()

	mailServer.close()

#END ACTIONS