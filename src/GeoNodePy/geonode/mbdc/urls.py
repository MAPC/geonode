from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template

from geonode.mbdc import views

from django.conf import settings

urlpatterns = patterns('',
	url(r'^(?P<slug>[-\w]+)/$', views.page, name='mbdc-page'),
)