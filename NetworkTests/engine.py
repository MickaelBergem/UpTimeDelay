# -*- coding: utf-8 -*-
""" Engine of UTD """

import subprocess
import re
import string
from django.db.models import F
from datetime import timedelta
from django.utils import timezone
from django.conf import settings

import cronjobs

from Monitors.models import Host, Monitor, MONITOR_TYPES
from models import HeartBeat

class MonitorEngine:
    def run(self, mon):
        hb = HeartBeat()
        hb.monitor = mon
        
        if mon.type == 'ping' or mon.type == 'P':
            # First, register the execution
            hb.monitor.last_job = timezone.now()
            hb.monitor.next_job = timezone.now() + timedelta(minutes=hb.monitor.periodicity)
            hb.monitor.save()
            
            # Let's ping !
            self.raw_ping(mon.host.hostname)
            
            hb.raw_output = self.ping_response
        
            # `ping` returns 0 if host is up
            hb.is_up = (self.ping_response_raw.returncode == 0)
        
            # Parsing the response :
            delays = []
            for line in hb.raw_output.split("\n"):
                ping_body = r"^\d+ bytes from ((?P<hostname>[^ ]+) \([0-9a-f.:]+\)|[0-9a-f.:]+): icmp_seq=\d+ ttl=\d+ time=(?P<delay>.*)"
                
                m = re.match(ping_body, line, re.I)
                if m:
                    delay = m.group("delay")
                    m2 = re.match("^([0-9.]+) ([ms]+)$", delay)
                    if m2:
                        if m2.group(2) == "ms":
                            delays.append(float(m2.group(1)))
                        elif m2.group(2) == "s":
                            delays.append(float(m2.group(1))*1000.)
                        else:
                            raise Exception("Unable to parse time unity in delay : {}".format(m2.group(2)))
                    else:
                        raise Exception("Unable to parse delay : {}".format(delay))
                #else:
                    #print line
            
            # Computing the average delay
            if len(delays) == 0:
                hb.delay = 0
            else:
                hb.delay = sum(delays)/len(delays)
        else:
            raise Exception("Type '{}' not recognized !".format(mon.type))
        
        return hb
    def run_and_save(self, mon):
        hb = self.run(mon)
        hb.save()
        
    def raw_ping(self, host, asynchronous=False):
        try:
            self.ping_response_raw = subprocess.Popen([settings.PING_CMD, "-c4", "-w100", "-i0.2", host], stdout=subprocess.PIPE)

            if not asynchronous:
                cm = self.ping_response_raw.communicate()
                self.ping_response = cm[0]
            else:
                self.ping_response = 'Not loaded yet...'

        except OSError:
            raise Exception('ping executable not found ! Please set the PING_CMD settings in the settings.py file :)')
