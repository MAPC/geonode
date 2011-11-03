from django.template import RequestContext
from django.shortcuts import render_to_response

from geonode.mbdc.models import Hero, Featured
from geonode.weave.models import Visualization
from geonode.weave.utils import get_readable_vis


def index(request): 
	""" Renders homepage """

	hero_entries = Hero.objects.filter(active=True)

	# get set of visualizations viewable by current user
	readable_vis = get_readable_vis(request.user)
	
	# featured visualizations
	featured_visualizations = Featured.objects.filter(visualization__in=readable_vis)

	# get latest 10 visualizations for gallery
	gallery_visualizations = Visualization.objects.filter(id__in=readable_vis).order_by('-last_modified')[:10]

	return render_to_response('mbdc/index.html', locals(), context_instance=RequestContext(request))