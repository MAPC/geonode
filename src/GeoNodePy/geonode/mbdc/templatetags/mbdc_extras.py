from django import template

from django.conf import settings

from geonode.mbdc.models import Page, TOPICS
from geonode.snapshots.models import Regiontype

register = template.Library()

@register.inclusion_tag('mbdc/_header_about.html')
def get_header_about():

	about_pages = Page.objects.filter(section='about')

	return {
		'about_pages': about_pages,
	}

@register.inclusion_tag('mbdc/_header_primarynav.html')
def get_header_primarynav():

	snapshot_types = Regiontype.objects.all()

	return {
		'snapshot_types': snapshot_types,
	}

@register.inclusion_tag('mbdc/_footer.html')
def get_footer():

	about_pages = Page.objects.filter(section='about')	
	snapshot_types = Regiontype.objects.all()

	return {
		'about_pages': about_pages,
		'topics': TOPICS[:-1],
		'snapshot_types': snapshot_types,
		'STATIC_URL': settings.STATIC_URL
	}