#!/usr/bin/python
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import time
import os
import re
import sys
import datetime
sys.path.append('/usr/share/subterfuge')

   #Ignore Deprication Warnings
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

from django.conf import settings
settings.configure(DATABASE_ENGINE="sqlite3",
                   DATABASE_HOST="",
                   DATABASE_NAME= os.path.dirname(os.path.abspath(__file__)).rstrip("abcdefghijklmnnnopqrstruvwxyz") + "db",
                   DATABASE_USER="",
                   DATABASE_PASSWORD="")

from django.db import models
from main.models import *

def main():
   
   title = sys.argv[1]
   message = sys.argv[2]
   status = "new"

   now = datetime.datetime.now()
   date = now.strftime("%d-%m-%Y %H:%M")
   logmessage = notification(status = status, title = title, message = message, date = date)
   logmessage.save()
	
if __name__ == '__main__':
	main()
