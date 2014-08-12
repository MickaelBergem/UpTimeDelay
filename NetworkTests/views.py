#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from NetworkTests.models import HeartBeat
from Monitors.models import Host,Monitor


# Showing HB
class PerfMonitor(DetailView):
    model = Monitor
    template_name = 'dataviz/list_heartbeats.html'

    def get_context_data(self, **kwargs):
        context = super(PerfMonitor, self).get_context_data(**kwargs)

        hbs = HeartBeat.objects.filter(monitor = context['object'])

        if len(hbs) > 0:
            context['object'].uptime_pc = round(100.0 * len(hbs.filter(is_up=True)) / len(hbs))
            context['object'].meandelay = round(sum(hb.delay for hb in hbs if hb.is_up) / len(hbs.filter(is_up=True)), 1)
        else:
            context['object'].uptime_pc = "NA"
            context['object'].meandelay = "NA"

        context['object'].heartbeats = hbs

        try:
            is_up = HeartBeat.objects.filter(monitor=context['object']).latest("time").is_up
            context['object'].state = "up" if is_up else "down"

        except HeartBeat.DoesNotExist:
            context['object'].state = "unknown"

        return context
