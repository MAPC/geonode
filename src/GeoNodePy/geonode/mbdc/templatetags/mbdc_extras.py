from django import template

from geonode.mbdc.models import Page
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