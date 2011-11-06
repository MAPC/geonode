from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from geonode.snapshots.models import Regiontype, Regionalunit

def index(request):

	# snapshot types
	snapshot_types = Regiontype.objects.all()

	return render_to_response('snapshots/index.html', locals(), context_instance=RequestContext(request))


def regiontype(request, regiontype_slug):
	# snapshot types
	snapshot_types = Regiontype.objects.all()

	regiontype = get_object_or_404(Regiontype, slug__iexact=regiontype_slug)

	return render_to_response('snapshots/regiontype.html', locals(), context_instance=RequestContext(request))


def regionalunit(request, regiontype_slug, regionalunit_slug):

	# snapshot types
	snapshot_types = Regiontype.objects.all()

	regiontype = get_object_or_404(Regiontype, slug__iexact=regiontype_slug)
	regionalunit = get_object_or_404(Regionalunit, regiontype=regiontype, slug__iexact=regionalunit_slug)

	return render_to_response('snapshots/regionalunit.html', locals(), context_instance=RequestContext(request))



