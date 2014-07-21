# -*- coding: utf-8 -*-
""" CRON jobs """

from datetime import datetime, timedelta

import cronjobs

from Monitors.models import Monitor

from engine import MonitorEngine

@cronjobs.register
def massive_run():
    """ Runs massively the cron tasks """
    ME = MonitorEngine()
    
    mons = Monitor.objects.filter(
        next_job__lte= datetime.now()
        )
    
    print "Processing {} job(s)...".format(len(mons))
    
    for mon in mons:
        ME.run_and_save(mon)
    
    