from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template

from geonode.snapshots import views

from django.conf import settings

urlpatterns = patterns('',
	url(r'^$', views.index, name='snapshots-index'),
	url(r'^(?P<regiontype_slug>[-\w]+)/$', views.get_regiontype, name='snapshots-regiontype'),
	url(r'^(?P<regiontype_slug>[-\w]+)/(?P<regionalunit_slug>[-\w]+)/$', views.get_regionalunit, name='snapshots-regionalunit'),
	url(r'^(?P<regiontype_slug>[-\w]+)/(?P<regionalunit_slug>[-\w]+)/(?P<visid>\d+)/$', views.get_sessionstate, name='snapshots-sessionstate'),

	# regiontype/regionalunit/visid
	# regiontype/regionalunit/datasource

)