from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from django.contrib.auth.models import User

from geonode.mbdc.models import Hero, Featured, Page, Topic, Datasource
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

	topics = Topic.objects.all()

	return render_to_response('mbdc/index.html', locals(), context_instance=RequestContext(request))

def section(request, section):
	""" Shows the first page in given section """

	section_pages = Page.objects.filter(section__iexact=section)
	page = section_pages[0]

	return render_to_response('mbdc/generic.html', locals(), context_instance=RequestContext(request))

def page(request, slug, section):
	""" Renders a flat page """

	page = get_object_or_404(Page, slug__iexact=slug, section__iexact=section)
	section_pages = Page.objects.filter(section__iexact=section)

	return render_to_response('mbdc/generic.html', locals(), context_instance=RequestContext(request))


def gallery(request):

	topics = Topic.objects.all()
	datasources = Datasource.objects.all()
	users = User.objects.all().order_by('username')

	try:
		# get set of visualizations viewable by current user
		readable_vis = get_readable_vis(request.user)
		params = request.GET.copy()
		# remove page key, we have no valid field
		if 'page' in params: del params['page']
		# build query from other GET parameters
		query = dict([(param,int(params[param])) for param in params], id__in=readable_vis)
		visualizations = Visualization.objects.filter(**query).order_by('-last_modified')

		# for selected options and verbose filter output on page
		if 'datasources' in params: filter_source = Datasource.objects.get(pk=params['datasources'])
		if 'topics' in params: filter_topic = Topic.objects.get(pk=params['topics'])
		if 'owner' in params: filter_user = User.objects.get(pk=params['owner'])

	except:
		# empty object
		visualizations = Visualization.objects.none()

	# TODO: check if pagination provides that value somewhere
	nr_results  = len(visualizations)

	return render_to_response('mbdc/gallery.html', locals(), context_instance=RequestContext(request))