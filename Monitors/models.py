from django.db import models
from datetime import datetime
from django.utils.translation import ugettext as _

MONITOR_TYPES = (('P','ping'),('H','http-head'))

class Host(models.Model):
    """ Host used in a monitor """
    ip = models.IPAddressField(null=True, blank=True, verbose_name=_('IP address'))
    hostname = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Hostname')) # The FQDN is 255 bytes long max
    added_date = models.DateTimeField(default=datetime.now(), verbose_name=_('Date of creation'))
    
    def __unicode__(self):
        if len(self.hostname) == 0:
            return self.ip
        else:
            return self.hostname
        
    class Meta:
        verbose_name = _('Host')
        verbose_name_plural = _('Hosts')
    
class Monitor(models.Model):
    """ A monitor is used to check a host's health in a certain way """
    type = models.CharField(choices=MONITOR_TYPES, default='http-head', verbose_name=_('Type'), max_length=10)
    host = models.ForeignKey(Host, verbose_name=_('Host'))
    
    def __unicode__(self):
        return "Monitor {} for {}".format(self.type, self.host)
        
    class Meta:
        verbose_name = _('Monitor')
        verbose_name_plural = _('Monitors')