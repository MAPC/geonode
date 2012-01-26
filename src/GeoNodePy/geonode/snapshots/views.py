from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from django.views.decorators.cache import cache_page, never_cache

from geonode.snapshots.models import Regiontype, Regionalunit, Visualization
from geonode.mbdc.models import Topic
from geonode.weave.views import save_thumbnail

import os
import simplejson


def get_thumbnail_list(regiontype, regionalunit):
	""" Returns a list of exisiting Visualization thumbnails """

	# check for existing tumbnail files
	path = '%s/snapshots_thumbnails/%s/%s' % (settings.MEDIA_ROOT, regiontype, regionalunit)
	tn_list = []
	if os.path.exists(path):
		tn_list = [ int(tn[:-4]) for tn in os.listdir(path) if tn[-3:] == 'png']

	return tn_list
	

def index(request):

	# snapshot types
	snapshot_types = Regiontype.objects.all()

	return render_to_response('snapshots/index.html', locals(), context_instance=RequestContext(request))


def get_regiontype(request, regiontype_slug):
	# snapshot types
	snapshot_types = Regiontype.objects.all()

	regiontype = get_object_or_404(Regiontype, slug__iexact=regiontype_slug)

	regionalunits = Regionalunit.objects.filter(regiontype=regiontype).order_by('name')

	return render_to_response('snapshots/regiontype.html', locals(), context_instance=RequestContext(request))


def get_regionalunit(request, regiontype_slug, regionalunit_slug):
	""" Render page for regional unit with one (first) visualization per topic """
	# snapshot types

	regiontype = get_object_or_404(Regiontype, slug__iexact=regiontype_slug)
	regionalunit = get_object_or_404(Regionalunit, regiontype=regiontype, slug__iexact=regionalunit_slug)
	try:
		overviewmap = Visualization.objects.get(regiontype=regiontype, overviewmap=True)
	except:
		pass

	# show all categories except the last one ("Geographic Boundaries")
	topics = Topic.objects.all()

	# build the town select dropdown
	regionalunits = Regionalunit.objects.all()

	tn_list = get_thumbnail_list(regiontype_slug, regionalunit_slug)

	return render_to_response('snapshots/regionalunit.html', locals(), context_instance=RequestContext(request))


def get_sessionstate(request, regiontype_slug, regionalunit_slug, visid):
	""" Get predefined session state as XML template for given visualization and regional unit """

	visualization = get_object_or_404(Visualization, pk=visid)
	regiontype = get_object_or_404(Regiontype, slug__iexact=regiontype_slug)
	regionalunit = get_object_or_404(Regionalunit, regiontype=regiontype, slug__iexact=regionalunit_slug)
	
	return render_to_response(visualization.sessionstate.name, locals(), context_instance=RequestContext(request), mimetype='application/xml')


@never_cache
def create_thumbnails(request, regiontype_slug, regionalunit_slug):
	"""" 
	Receives base64 data from currently shown visualizations and creates thumbnails.
	Called before the print layout.
	"""

	if not request.method == 'POST':
		return HttpResponse(
			'You must use POST to create thumbnails.',
			status=405,
			mimetype='text/plain'
		)
	else:
		visualizations = simplejson.loads(request.POST['visualizations'])

		for visualization in visualizations:
			# save visualization thumbnail if it doesn't exist
			path = 'snapshots_thumbnails/%s/%s/' % (regiontype_slug, regionalunit_slug)
			filename = visualizations[visualization]['visid']
			if not os.path.isfile('%s/%s%s.png' % (settings.MEDIA_ROOT, path, filename)):
				save_thumbnail(data=visualizations[visualization]['thumbnail'], path=path, filename='%s' % (filename), tn_sizes=None)

		return HttpResponse(
			status=201
		)


@cache_page(60 * 15)
def print_regionalunit(request, regiontype_slug, regionalunit_slug):
	""" Renders a printer friendly layout """

	printvis = request.GET['visualizations'].split(',')

	regiontype = get_object_or_404(Regiontype, slug__iexact=regiontype_slug)
	regionalunit = get_object_or_404(Regionalunit, regiontype=regiontype, slug__iexact=regionalunit_slug)

	visualizations = Visualization.objects.filter(id__in=printvis, overviewmap=False)

	try:
		overviewmap = Visualization.objects.get(id__in=printvis, overviewmap=True)
	except:
		pass

	return render_to_response('snapshots/print.html', locals(), context_instance=RequestContext(request))


@cache_page(60 * 15)
def get_topic(request, regiontype_slug, regionalunit_slug, topic_slug):
	""" Render all visualizations for given topic and regional unit """

	regiontype = get_object_or_404(Regiontype, slug__iexact=regiontype_slug)
	regionalunit = get_object_or_404(Regionalunit, regiontype=regiontype, slug__iexact=regionalunit_slug)

	topic = get_object_or_404(Topic, slug__iexact=topic_slug)

	visualizations = Visualization.objects.filter(regiontype=regiontype, topics=topic)

	tn_list = get_thumbnail_list(regiontype_slug, regionalunit_slug)

	return render_to_response('snapshots/topic.html', locals(), context_instance=RequestContext(request))




























