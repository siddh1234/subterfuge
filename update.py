#!/usr/bin/python
import os
import sys
import time
import socket
from versioninfo import *
sys.path.append('/usr/share/subterfuge')

   #Ignore Deprication Warnings
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from django.conf import settings
settings.configure(DATABASE_ENGINE="sqlite3",
                   DATABASE_HOST="",
                   DATABASE_NAME= os.path.dirname(os.path.abspath(__file__)) + "/db",
                   DATABASE_USER="",
                   DATABASE_PASSWORD="")

from django.db import models
from main.models import *

#Get Globals from Database
for settings in setup.objects.all():
        autoupdate     = settings.autoupdate

def main():
	print "Updating Subterfuge..."
		#Build Revision
	os.system('svn update /usr/share/subterfuge')

		#Versioning Management
        info = os.popen('svn info /usr/share/subterfuge')
	svninfo = info.readlines()
	info.close()
		#Get Current Version
	for line in svninfo:
		if line.startswith("Revision:"):
				#Get Revision Number
			revision = line.split(" ")[1]

		#Determine Release Number & set version
	release = int(revision) - initial_revision_number
	version = str(major_release_version) + "." + str(minor_release_version) + "." + str(release)



	if int(current_revision_number) == int(revision):
		print "Subterfuge is already at the latest version"
	else:
			#Additional Configuration
		print "Configuring Subterfuge..."
		os.system("python /usr/share/subterfuge/configure.py") 
		print "Done!"

	print "Subterfuge " + version
	
def updatecheck():
 try:
   if autoupdate == "yes":
		#Only Update Once
           setup.objects.update(autoupdate = "no")

	   print "Checking for updates. You can disable this feature through the settings page."
		   #Calculate version info
	   release = int(current_revision_number) - int(initial_revision_number)
	   version = str(major_release_version) + "." + str(minor_release_version) + "." + str(release)
		   #Check For New Updates
	   HOST = 'kinozoa.com' #Update Server
	   PORT = 5733 #Update Port
	   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	   s.connect((HOST, PORT))
	   s.send('getversion')
	   data = s.recv(1024)
	   s.close()
	   newversion = data.strip('\n')

	   if version != newversion:
	      os.system("python /usr/share/subterfuge/update.py")
	   else:
	      print "Subterfuge is still cutting edge!"
	      print "Current version is: " + version

           time.sleep(5)
		#Reset Autoupdate	
           setup.objects.update(autoupdate = "yes")


 except:
  pass 

if __name__ == '__main__':
   main()	
