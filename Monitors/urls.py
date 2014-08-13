from django.conf.urls import patterns, url, include
from models import Host, Monitor
from bsct.urls import URLGenerator
from NetworkTests.views import PerfMonitor

from django.views.generic import ListView, DetailView, UpdateView, DeleteView

bsct_patterns_Host = URLGenerator( Host ).get_urlpatterns( paginate_by = 10 )
bsct_patterns_Mon = URLGenerator( Monitor ).get_urlpatterns( paginate_by = 10 )

urlpatterns = patterns('Monitors.views',
                       
                url( 'monitor/(?P<pk>\d+)$',
                   PerfMonitor.as_view(),
                   name = 'monitor_detail'),
                url( 'monitor/$',
                   ListView.as_view(
                       template_name='projects/monitors_list.html',
                       model=Monitor,
                       ),
                   name = 'monitor_list'),
                url( '', include( bsct_patterns_Host ) ),
                url( '', include( bsct_patterns_Mon ) ),
              )
