#!/usr/bin/python
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import time
import os
import re
import sys
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

def globalvars():
	#Get Globals from Database
	for settings in setup.objects.all():
		interface     = settings.iface
		gateway       = settings.gateway
		attackerip    = settings.ip
		routermac     = settings.routermac
		smartarp      = settings.smartarp
		arprate       = int(settings.arprate)
		
	globalvars = {
		"interface"		:   interface,
		"gateway"		:   gateway,
		"attackerip"	:   attackerip,
		"routermac"		:   routermac,
		"smartarp"		:   smartarp,
		"arprate"		:   arprate
	}
	return globalvars

