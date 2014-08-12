from django.test import TestCase

from django.core.urlresolvers import reverse

from Monitors.models import Host, Monitor
from NetworkTests.models import HeartBeat


class PerfMonitorTest(TestCase):
    """ Test of the view PerfMonitor """

    def setUp(self):
        # Create a test host and monitor

        self.h1 = Host.objects.create(hostname="www.securem.eu")
        self.m1 = Monitor.objects.create(type='ping', host=self.h1)

        self.h2 = Host.objects.create(ip="4.4.4.4")
        self.m2 = Monitor.objects.create(type='ping', host=self.h2)

        self.response = self.client.get(
            reverse('monitor_detail', kwargs={'pk': self.m1.id}),
            follow=True
            )

        self.response_down = self.client.get(
            reverse('monitor_detail', kwargs={'pk': self.m2.id}),
            follow=True
            )

        self.monitors = [self.m1, self.m2]
        self.responses = [self.response, self.response_down]

    def test_if_reacheable(self):
        """ Tests if the pages are reachable """
        for response in self.responses:
            self.assertEqual(response.status_code, 200,
                             "The page should respond with a HTTP 200 code")
            self.assertContains(response, "<!-- No data yet ! -->",
                                msg_prefix="The page should say there is no data yet")

    def test_if_bagde_up(self):
        """ Tests the badge in the sidebar """

        for id, monitor in enumerate(self.monitors):

            # Get the host status (up/down)
            try:
                is_up = HeartBeat.objects.filter(monitor=monitor).latest("time").is_up

                if is_up:
                    self.assertContains(self.response, "sidebar-host-up",
                                    msg_prefix="The host should appear as up")
                else:
                    self.assertContains(self.response, "sidebar-host-down",
                                    msg_prefix="The host should appear as down")

            except HeartBeat.DoesNotExist:
                self.assertContains(self.response, "sidebar-host-unknown",
                                msg_prefix="The host should appear as unknown")

