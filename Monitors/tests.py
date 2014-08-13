from django.test import TestCase

from django.core.urlresolvers import reverse

from Monitors.models import Host, Monitor, MONITOR_TYPES
from NetworkTests.models import HeartBeat
from NetworkTests.engine import MonitorEngine


class HostDownDisplayTest(TestCase):
    def setUp(self):
        self.h1 = Host.objects.create(hostname="idonotexist.neitherdoi")
        self.m1 = Monitor.objects.create(type='ping', host=self.h1)
        self.ME = MonitorEngine()

    def test_display_list(self):
        # TODO
        pass

    def test_display_detail_before_run(self):
        # Get the page
        response = self.client.get(
            reverse('monitor_detail', kwargs={'pk': self.m1.id}),
            follow=True
            )

        self.assertEqual(response.status_code, 200,
                         "The page should respond with a HTTP 200 code")

    def test_display_detail_after_run(self):
        # Run the engine
        hb1 = self.ME.run_and_save(self.m1)
        # Get the page
        response = self.client.get(
            reverse('monitor_detail', kwargs={'pk': self.m1.id}),
            follow=True
            )

        self.assertEqual(response.status_code, 200,
                         "The page should respond with a HTTP 200 code")
