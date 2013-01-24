from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'masshealth.programs.views',

    url(r'^geojson/$', 'all_geojson'),
)
