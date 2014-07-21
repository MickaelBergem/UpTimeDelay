from django.test import TestCase
from datetime import datetime

from Monitors.models import Host, Monitor, MONITOR_TYPES
from models import HeartBeat
from engine import MonitorEngine

class PingTest(TestCase):
    def setUp(self):
        self.h1 = Host.objects.create(hostname="www.securem.eu", ip="178.32.167.243")
        self.h2 = Host.objects.create(hostname="178.32.167.243")
        self.m1 = Monitor.objects.create(type='ping', host=self.h1)
        self.m2 = Monitor.objects.create(type='ping', host=self.h2)
        
        self.mons_correct = [self.m1,self.m2]
        self.mons = [self.m1,self.m2]
        self.ME = MonitorEngine()
        
    def test_ping_correct_host(self):
        
        for mon in self.mons_correct:
            hb1 = self.ME.run(mon)
            
            self.assertIsInstance(hb1, HeartBeat
                                , msg = "The runMonitor response should be a HeartBeat instance")
            
            self.assertEqual(hb1.time.date(), datetime.now().date()
                            , msg=  "The HeartBeat object must have the day of generation : today")
            
            self.assertEqual(hb1.is_up, True
                            , msg=  "The host "+self.h1.ip+" is expected to be online...")
            
            self.assertGreater(hb1.delay, 0
                            , msg=  "The delay should be greater than 0")
            
            self.assertNotEqual(hb1.raw_output, ''
                            , msg=  "The raw_output must never be empty")
            
    def test_run_general(self):
        
        for mon in self.mons:
            hb1 = self.ME.run(mon)
            
            self.assertIsInstance(hb1, HeartBeat
                                , msg = "The runMonitor response should be a HeartBeat instance")
            
            self.assertEqual(hb1.time.date(), datetime.now().date()
                            , msg=  "The HeartBeat object must have the day of generation : today")
            
            self.assertNotEqual(hb1.raw_output, ''
                            , msg=  "The raw_output must never be empty")