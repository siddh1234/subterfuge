#!/usr/bin/python
import os
import re
import sys
sys.path.append('/usr/share/subterfuge')
import time
import subprocess

#Ignore Deprication Warnings
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

#Subterfuge Database Models
from django.conf import settings
settings.configure(DATABASE_ENGINE="sqlite3",
                   DATABASE_HOST="",
                   DATABASE_NAME= "/usr/share/subterfuge/db",
                   DATABASE_USER="",
                   DATABASE_PASSWORD="")

from django.db import models
from modules.models import *


target = 'Unknown'
ports = []
quickos = 'Unknown'
operatingsystem = 'Unknown'
mac = 'Unknown'
hostname = 'Unknown'

def main():

	if len(sys.argv) < 2:
		print 'Please use IP address of target as an argument.'
		exit()	

	else:
		target = sys.argv[1]
		if os.path.exists(str(os.path.dirname(__file__)).rstrip("abcdefghijklmnnnopqrstruvwxyz") + 'utilities/scans/' + target + '.xml') == False:
		   os.system('touch ' + str(os.path.dirname(__file__)).rstrip("abcdefghijklmnnnopqrstruvwxyz") + 'utilities/scans/' + target + '.xml')
		   scanner = subprocess.Popen(['nmap', '-T4', '-F', '-A', "-oX", str(os.path.dirname(__file__)).rstrip("abcdefghijklmnnnopqrstruvwxyz") + 'utilities/scans/' + target + ".xml", target], stdout=subprocess.PIPE)
		   #Add Record/Set Scan Bit
		   #Check for Existing IP Address
		   try:
		      check = scan.objects.get(address = target)
		      if check != 0:
		         scan.objects.filter(address = target).update(scanning = "1")         
		   except:
		      log = scan(address = target, scanning = "1")
		      log.save()
            
		   os.system('python ' + str(os.path.dirname(__file__)).rstrip("abcdefghijklmnnnopqrstruvwxyz") + 'utilities/scanindicator.py ' + str(scanner.pid) + ' ' + target + '&')
		   
		else:
		   scanParse(target)
	      
	      
	      
	   #if os.path.exists('/proc/' + str(scan.pid)) == False:
		#i = scan.stdout.read()a
		#i = "0"
		#print info
		#os.system('nmap -T4 -F -O ' + target + ' > ' + target)

		
def scanParse(target):

	quickos = 'Unknown'
	operatingsystem = 'Unknown'
	mac = 'Unknown'
	hostname = 'Unknown'
	
	#scancheck = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
	#print scancheck.stdout.read()
	

	f = open(str(os.path.dirname(__file__)).rstrip("abcdefghijklmnnnopqrstruvwxyz") + 'utilities/scans/' + target + ".xml", 'r')
	output = f.readlines()
	
	for i in output:
	      #Get PORTS
	   if i.startswith('<port proto'):
	       port = i.split('portid="')[1]
	       port = port.split('"')[0]
	       ports.append(port)
	       
	      #Get OS
	   elif i.startswith('<osmatch'):
	       operatingsystem = i.split('name="')[1]
	       operatingsystem = operatingsystem.split('"')[0]
	       if operatingsystem.startswith('Apple'):
	            quickos = 'osx'
	       if operatingsystem.startswith('Windows'):
	            quickos = 'win'
	       if operatingsystem.startswith('Linux'):
	            quickos = 'lnx'		            
   
	      #Get MAC
	   elif (i.find('addrtype="mac"')) >= 0:
	       mac = i.split('addr="')[1]
	       mac = mac.split('"')[0]
	       
	      #Get HOSTNAME
	   elif (i.find('NetBIOS name:') >= 0):
			temp = i.partition(', ')
			temp2 = temp[0]
			temp3 = temp2.partition('NetBIOS name:')
			temp4 = temp3[2]
			hostname = temp4
			
	   f.close()
	
	"""
	for i in output:
		print i
		if (i.find('portid="') >= 0):
			if (i.find('open') >= 0):
				temp = i.rpartition('/tcp')
				temp2 = temp[0]
				temp3 = temp2.rstrip('\n')
				ports.append(temp3)	
		if (i.find('Running:') >= 0):
			if (i.find('Windows') >= 0):
				quickos = 'win'
				temp = i.rpartition(': ')
				temp2 = temp[2]
				operatingsystem = temp2.rstrip('\n')
			elif (i.find('Mac') >= 0):
				quickos = 'osx'
				temp = i.rpartition(': ')
				temp2 = temp[2]
				operatingsystem = temp2.rstrip('\n')
			elif (i.find('Linux') >= 0):
				quickos = 'lnx'
				temp = i.rpartition(': ')
				temp2 = temp[2]
				operatingsystem = temp2.rstrip('\n')
		if (i.find('Windows') >= 0):
			quickos = 'win'
		if (i.find('Mac') >= 0):
			quickos = 'osx'
		if (i.find('Linux') >= 0):
			quickos = 'lnx'
		if (i.find('MAC Address:') >= 0):
			temp = i.rpartition(': ')
			temp2 = temp[2]
			temp3 = temp2.rpartition(' (')
			temp4 = temp3[0]
			mac = temp4.rstrip('\n')
		if (i.find('Nmap scan report for') >= 0):
			temp = i.rpartition('for ')
			temp2 = temp[2]
			temp3 = temp2.rpartition(' (')
			temp4 = temp3[0]
			hostname = temp4.rstrip('\n')	
		if (i.find('NetBIOS name:') >= 0):
			temp = i.partition(', ')
			temp2 = temp[0]
			temp3 = temp2.partition('NetBIOS name:')
			temp4 = temp3[2]
			hostname = temp4
		if (i.find('OS:') >= 0):
			if (i.find('Service Info:') < 0):
				temp = i.rpartition('OS: ')
				temp2 = temp[2]
				operatingsystem = temp2.rstrip('\n')
	"""
		
			
		
	if (len(hostname) < 1):
		hostname = 'Unknown'
	time.sleep(.5)
	#os.system('rm ' + target)
	print 'target: ' + target
	print 'ports: ', ports
	print 'quickos: ' + quickos
	print 'operatingsystem: ' + operatingsystem
	print 'MAC: ' + mac
	print 'hostname: ' + hostname
	insert(target, ports, quickos, operatingsystem, mac, hostname)
			
			
   #insert into database
def insert(target, ports, os, osdetails, mac, hostname):
   scan.objects.filter(address = target).update(address = target, ports = ports, osdetails = osdetails, hostname = hostname)
   iptrack.objects.filter(address = target).update(mac = mac, os = os)
      #Clear Scan Bit
   scan.objects.filter(address = target).update(scanning = "0")
      ####ADD CHECK FOR EXISTING RECORD
   #log = scan(address = target, ports = ports, osdetails = osdetails, hostname = hostname)
   #log.save()
   

if __name__ == '__main__':
			 main()
