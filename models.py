from django.db import models

class credentials(models.Model):
    source      = models.CharField(max_length=300)
    username    = models.CharField(max_length=300)
    password    = models.CharField(max_length=300)
    date        = models.CharField(max_length=300)

class setup(models.Model):
    ip          = models.CharField(max_length=300)
    iface       = models.CharField(max_length=300)
    gateway     = models.CharField(max_length=300)
    autoconf    = models.CharField(max_length=300)
    ploadrate   = models.CharField(max_length=300)
    injectrate  = models.CharField(max_length=300)
    arprate     = models.CharField(max_length=300)
    smartarp    = models.CharField(max_length=300)
    routermac   = models.CharField(max_length=300)
    autoupdate  = models.CharField(max_length=300)
   
class progdirs(models.Model):
    nmap        = models.CharField(max_length=300)
    metasploit  = models.CharField(max_length=300)
    evilgrade   = models.CharField(max_length=300)

class notification(models.Model):
    status      = models.CharField(max_length=300)
    title       = models.CharField(max_length=300, default = 'Alert')
    message     = models.CharField(max_length=300)
    date        = models.CharField(max_length=300)
