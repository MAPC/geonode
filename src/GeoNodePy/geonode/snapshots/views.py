from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from geonode.snapshots.models import Regiontype, Regionalunit, Visualization
from geonode.mbdc.models import TOPICS

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
	# snapshot_types = Regiontype.objects.all()

	regiontype = get_object_or_404(Regiontype, slug__iexact=regiontype_slug)
	regionalunit = get_object_or_404(Regionalunit, regiontype=regiontype, slug__iexact=regionalunit_slug)

	# show all categories except the last one ("Geographic Boundaries")
	topics = TOPICS[:-1]

	visualizations = Visualization.objects.all()

	return render_to_response('snapshots/regionalunit.html', locals(), context_instance=RequestContext(request))


def get_sessionstate(request, regiontype_slug, regionalunit_slug, visid):
	""" Get predefined session state as XML template for given visualization and regional unit """

	visualization = get_object_or_404(Visualization, pk=visid)
	regiontype = get_object_or_404(Regiontype, slug__iexact=regiontype_slug)
	regionalunit = get_object_or_404(Regionalunit, regiontype=regiontype, slug__iexact=regionalunit_slug)

	return render_to_response(visualization.sessionstate.name, locals(), context_instance=RequestContext(request))


def get_topic(request, regiontype_slug, regionalunit_slug, topic_slug):
	""" Render all visualizations for given topic and regional unit """

	regiontype = get_object_or_404(Regiontype, slug__iexact=regiontype_slug)
	regionalunit = get_object_or_404(Regionalunit, regiontype=regiontype, slug__iexact=regionalunit_slug)

	topic_verbose = dict(TOPICS)[topic_slug]

	visualizations = Visualization.objects.filter(regiontype=regiontype, topic__iexact=topic_slug)

	return render_to_response('snapshots/topic.html', locals(), context_instance=RequestContext(request))

























