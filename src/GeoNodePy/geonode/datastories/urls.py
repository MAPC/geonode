from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template
from geonode.datastories import views

urlpatterns = patterns('',
	url(r'^$', direct_to_template, {'template': 'datastories/index.html'}),
	url(r'^(?P<slug>[-\w]+)/$', views.story, name='datastories-story'),
	url(r'^(?P<slug>[-\w]+)/(?P<page>\d+)$', views.page, name='datastory-page'),
	url(r'^search/?$', views.search_page, name='datastories-search'),
	url(r'^search/api/?$', views.search, name='datastories-search-api'),
)

