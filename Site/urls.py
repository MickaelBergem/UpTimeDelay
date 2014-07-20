#-*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include
from Site.views import display_homepage

urlpatterns = patterns('Site.views',
                url(r'^$','display_homepage',name="home"),
              )