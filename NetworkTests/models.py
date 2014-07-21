from django.db import models
from datetime import datetime
from django.utils.translation import ugettext as _
from bsct.models import BSCTModelMixin

from Monitors.models import Host, Monitor, MONITOR_TYPES

class HeartBeat(BSCTModelMixin , models.Model):
    """ Result of a monitoring test """
    
    monitor = models.ForeignKey(Monitor, verbose_name=_('Monitor master'))
    time = models.DateTimeField(default=datetime.now(), verbose_name=_('Date of triggering'))
    is_up = models.BooleanField(verbose_name=_('Host is up'))
    delay = models.FloatField(verbose_name=_('Delay'), null=True, blank=True)
    raw_output = models.TextField(verbose_name=_('Raw output'))
    
    def __unicode__(self):
        return _("Heartbeat for {} at {}".format(self.monitor.host, self.time))
    
    def delay_detail(self):
        return "{} ms".format(self.delay)
    class Meta:
        verbose_name = _('HeartBeat')
        verbose_name_plural = _('HeartBeats')