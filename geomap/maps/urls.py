from django.conf.urls import patterns, url
from maps import views


urlpatterns = patterns('',
    url(r'^$', views.mapshow, name='mapshow'),
    url(r'^maptest$', views.mapshow, name='mapshow'),
    url(r'^alertjson$', views.alertjson, name='alertjson'),
)


