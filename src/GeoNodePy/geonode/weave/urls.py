from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template
from geonode.weave import views
from django.conf import settings

urlpatterns = patterns('',
	url(r'^$', views.index, name='weave-index'),
	url(r'^new$', views.new, name='weave-new'),
	url(r'^sessionstate$', views.sessionstate, name='weave-sessionstate'),
	url(r'^(?P<visid>\d+)/$', views.edit, name='weave-edit'),
	url(r'^(?P<visid>\d+)/detail$', views.detail, name='weave-detail'),
	url(r'^(?P<visid>\d+)/embed$', views.embed, name='weave-embed'),
	url(r'^(?P<visid>\d+)/delete$', views.delete, name='weave-delete'),
	url(r'^(?P<visid>\d+)/sessionstate$', views.sessionstate, name='weave-sessionstate'),
	url(r'^(?P<visid>\d+)/permissions$', views.set_permissions, name='weave-setpermissions'),
	url(r'^(?P<visid>\d+)/ajax-permissions$', views.ajax_visualization_permissions, name='ajax_visualization_permissions'),
	url(r'^search/?$', views.search_page, name='weave-search'),
	url(r'^search/api/?$', views.search, name='weave-search-api'),
)
