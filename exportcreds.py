#!/usr/bin/python
import os
import re
import sys
import time
import datetime
import urllib
from django.conf import settings
settings.configure(DATABASE_ENGINE="sqlite3",
                   DATABASE_HOST="",
                   DATABASE_NAME= os.path.dirname(__file__) + "/db",
                   DATABASE_USER="",
                   DATABASE_PASSWORD="")

from django.db import models
from main.models import *


	#Get Globals from Database
for creds in credentials.objects.all():
	source	      = creds.source
	username       = creds.username
	password			= creds.password
	date				= creds.date

def main():

	if os.path.isfile(os.path.dirname(__file__) + '/credentials.txt'):
		with open(str(os.path.dirname(os.path.abspath(__file__))) + '/credentials.txt', 'a') as file:
			file.writelines(source + ", " + username + ", " + password + ", " + date + "\n")
	else:
		os.system("touch " + os.path.dirname(__file__) + '/credentials.txt')
		with open(str(os.path.dirname(os.path.abspath(__file__))) + '/credentials.txt', 'w') as file:
			file.writelines("source, username, password, date\n")
			file.writelines(source + ", " + username + ", " + password + ", " + date + "\n")


if __name__ == '__main__':
    main()	
