from django import template

from django.conf import settings

from geonode.mbdc.models import TOPICS

from geonode.snapshots.models import Regiontype, Regionalunit, Visualization
from geonode.snapshots.models import Regiontype

register = template.Library()


@register.inclusion_tag('snapshots/_visualization.html')
def get_visualizations(topic, regiontype, regionalunit):

	# about_pages = Page.objects.filter(section='about')	
	# snapshot_types = Regiontype.objects.all()\\
	# regiontype, topic.0

	# regiontype

	# visualization = get_object_or_404(Visualization, pk=visid)
	# regiontype = get_object_or_404(Regiontype, slug__iexact=regiontype_slug)
	# regionalunit = get_object_or_404(Regionalunit, regiontype=regiontype, slug__iexact=regionalunit_slug)

	visualizations = Visualization.objects.filter(regiontype=regiontype, topic__iexact=topic[0])

	return {
		'topic': topic,
		'visualizations': visualizations,
		'regiontype': regiontype,
		'regionalunit': regionalunit,
		'STATIC_URL': settings.STATIC_URL,
		'WEAVE_URL': settings.WEAVE_URL,
		'SITEURL': settings.SITEURL,
	}