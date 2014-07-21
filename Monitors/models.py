from django.db import models
from datetime import datetime
from django.utils.translation import ugettext as _
from bsct.models import BSCTModelMixin

MONITOR_TYPES = (('P','ping'),('H','http-head'))

class Host(BSCTModelMixin , models.Model):
    """ Host used in a monitor """
    ip = models.IPAddressField(null=True, blank=True, verbose_name=_('IP address'))
    hostname = models.CharField(max_length=255, verbose_name=_('Hostname'), unique=True) # The FQDN is 255 bytes long max, and the hostname should at least be the IP
    added_date = models.DateTimeField(default=datetime.now(), verbose_name=_('Date of creation'))
    
    def __unicode__(self):
        if len(self.hostname) == 0:
            return self.ip
        else:
            return self.hostname
    
    def save(self, *args, **kwargs):
        """ Sanity checks """
        if len(self.hostname) == 0:
           self.hostname = str(self.ip)
        super(Host, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = _('Host')
        verbose_name_plural = _('Hosts')
    
class Monitor(BSCTModelMixin , models.Model):
    """ A monitor is used to check a host's health in a certain way """
    type = models.CharField(choices=MONITOR_TYPES, default='http-head', verbose_name=_('Type'), max_length=10)
    host = models.ForeignKey(Host, verbose_name=_('Host'))
    periodicity = models.IntegerField(default=30,verbose_name=_('Periodicity (minutes)'))
    last_job = models.DateTimeField(default=datetime.now(),verbose_name=_('Last execution'))
    next_job = models.DateTimeField(default=datetime.now(),verbose_name=_('Next scheduled execution'))
    
    def __unicode__(self):
        return "Monitor {} for {}".format(self.type, self.host)
        
    class Meta:
        verbose_name = _('Monitor')
        verbose_name_plural = _('Monitors')