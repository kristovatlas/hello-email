'''
Description: Sends an email to let you know that the server this script is run from is still alive and well.
Author: kristovatlas [at-symbol] gmail [period] com
'''

#timestamp
import time
import datetime

#generating email alerts
import smtplib
from email.mime.text import MIMEText

#logging
import os.path

#configuration
import ConfigParser

#set the current working directory to the location of the script
os.chdir(os.path.dirname(os.path.realpath(__file__)))

#modify the contents of this configuration file in order to configure the script's behavior
config_filename = 'hello.cfg'

config = ConfigParser.RawConfigParser()

try:
	config.readfp(open(config_filename))
except ConfigParser.Error:
	sys.exit("Could not read or parse '%s'" % config_filename)

config.read(config_filename)

timestamp_format = '%Y-%m-%d %H:%M:%S'

email_message = config.get('Email','email_message')
email_address_from = config.get('Email','email_address_from')
email_address_to = config.get('Email','email_address_to')
email_server = config.get('Email','email_server')
email_username = config.get('Email','email_username')
email_password = config.get('Email','email_password')
email_port = config.get('Email','email_port')

#based on: https://docs.python.org/2/library/email-examples.html
def send_email():
	timestamp = datetime.datetime.fromtimestamp(time.time()).strftime(timestamp_format)
	msg = MIMEText(email_message)
	msg['Subject'] = email_message + " at " + str(timestamp)
	msg['From'] = email_address_from
	msg['To'] = email_address_to
	to_list = email_address_to
	if (',' in email_address_to):
		#multiple recipients
		to_list = email_address_to.split(",")

	s = smtplib.SMTP(email_server, email_port) if email_port is not None and email_port else smtplib.STMP(email_server)
	try:
		s.login(email_username, email_password)
	except:
		print("Error: Trouble logging in... check your mail server, username, and password?")
	#for a single recipient, sendmail() will accept a string. for multiple recipients,
	# it requires a list as an argument.
	s.sendmail(msg['From'], to_list, msg.as_string())
	s.quit()

send_email()
print("Done.")