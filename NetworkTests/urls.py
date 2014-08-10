from django.conf.urls import patterns, url, include
from models import HeartBeat
from bsct.urls import URLGenerator

bsct_patterns = URLGenerator( HeartBeat ).get_urlpatterns( paginate_by = 100 )

urlpatterns = patterns('NetworkTests.views',
                       
                url( '', include( bsct_patterns ) ),
              )
