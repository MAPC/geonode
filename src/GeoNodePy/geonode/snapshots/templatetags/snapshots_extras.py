from django import template

from django.conf import settings

from geonode.mbdc.models import Topic

from geonode.snapshots.models import Regiontype, Regionalunit, Visualization
from geonode.snapshots.models import Regiontype

register = template.Library()


@register.inclusion_tag('snapshots/_visualization.html', takes_context=True)
def get_visualizations(context, topic, regiontype, regionalunit, tn_list):
	""" renders flash visualization for given arguments """

	visualizations = Visualization.objects.filter(regiontype=regiontype, topics=topic, overviewmap=False)

	return {
		'topic': topic,
		'visualizations': visualizations,
		'regiontype': regiontype,
		'regionalunit': regionalunit,
		'tn_list': tn_list,
		'STATIC_URL': context['STATIC_URL'],
		'WEAVE_URL': context['WEAVE_URL'],
		'SITEURL': context['SITEURL'],
		'MEDIA_URL': context['MEDIA_URL'],
	}