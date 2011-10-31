from django.template import RequestContext
from django.shortcuts import render_to_response

from geonode.mbdc.models import Hero


def index(request): 
	""" Renders homepage """

	hero_entries = Hero.objects.filter(active=True)

	return render_to_response('mbdc/index.html', locals(), context_instance=RequestContext(request))