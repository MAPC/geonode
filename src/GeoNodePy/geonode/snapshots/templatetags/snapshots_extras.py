from django import template

from django.conf import settings

from geonode.mbdc.models import Topic

from geonode.snapshots.models import Regiontype, Regionalunit, Visualization
from geonode.snapshots.models import Regiontype

register = template.Library()


@register.inclusion_tag('snapshots/_visualization.html')
def get_visualizations(topic, regiontype, regionalunit):
	""" renders flash visualization for given arguments """

	visualizations = Visualization.objects.filter(regiontype=regiontype, topics=topic, overviewmap=False)

	return {
		'topic': topic,
		'visualizations': visualizations,
		'regiontype': regiontype,
		'regionalunit': regionalunit,
		'STATIC_URL': settings.STATIC_URL,
		'WEAVE_URL': settings.WEAVE_URL,
		'SITEURL': settings.SITEURL,
	}