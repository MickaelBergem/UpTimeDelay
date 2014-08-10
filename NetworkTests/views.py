#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from NetworkTests.models import HeartBeat
from Monitors.models import Host,Monitor

# Showing HB
class PerfMonitor( DetailView ):
    model = Monitor
    template_name = 'dataviz/list_heartbeats.html'

    def get_context_data(self, **kwargs):
        context = super(PerfMonitor, self).get_context_data(**kwargs)
        
        hbs = HeartBeat.objects.filter(monitor = context['object'])
        
        context['object'].uptime_pc = round(100.0 * len(hbs.filter(is_up=True)) / len(hbs))
        context['object'].meandelay = round(sum(hb.delay for hb in hbs if hb.is_up) / len(hbs))
        
        context['object'].heartbeats = hbs
        
        return context
