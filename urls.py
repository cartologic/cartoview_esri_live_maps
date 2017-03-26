from django.conf.urls import patterns, url

import views
from . import APP_NAME

urlpatterns = patterns('',
    url(r'^new/$', views.new, name='%s.new' % APP_NAME),
    url(r'^(?P<resource_id>\d+)/view/$', views.view, name='%s.view' % APP_NAME),
    url(r'^(?P<resource_id>\d+)/edit/$', views.edit, name='%s.edit' % APP_NAME),
    url(r'^proxy/$', views.proxy, name='%s.proxy' % APP_NAME),
)
