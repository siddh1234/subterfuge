#####################################################################
#This file is for use to fully reset the Subterfuge Database
#It should only be necessary due to significant develompent changes
#Usage MUST be as follows:
#rm db && rm base_db
#./manage.py syncdb
#python dbconfigure.py
#This will rebuild the Database from scratch
#####################################################################


import os
from django.conf import settings
settings.configure(DATABASE_ENGINE="sqlite3",
                   DATABASE_HOST="",
                   DATABASE_NAME="db",
                   DATABASE_USER="",
                   DATABASE_PASSWORD="")

from django.db import models
from main.models import *
from modules.models import *


    #Create Settings Data Space
table = setup(autoconf = "no")
table.save()

    #Build Default Settings
print "Setting Database Default Configuration..."       
setup.objects.update(autoconf = "yes")
setup.objects.update(ploadrate = "3")
setup.objects.update(injectrate = "6")
setup.objects.update(arprate = "8")
setup.objects.update(smartarp = "yes")


    #Build Netview Module
print "Configuring Database Space for Modules..."     
print "Building HTTP Code Injection Module"    
newmod = installed(name = "httpcodeinjection")
newmod.save()
print "Building Tunnel Block Module"   
newmod = installed(name = "tunnelblock")
newmod.save()
print "Building Denial of Service Module"   
newmod = installed(name = "dos")
newmod.save()

