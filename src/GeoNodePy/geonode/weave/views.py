from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

import json
import re
import unicodedata
from urllib import urlencode
import os

import base64
import Image

from django.conf import settings

from geonode.maps.views import _split_query

from geonode.core.models import AUTHENTICATED_USERS, ANONYMOUS_USERS, PermissionLevelMixin
from geonode.maps.models import Contact
from geonode.weave.models import Visualization
from geonode.mbdc.models import Topic, Datasource

# Visualization Thumbnail sizes
DEFAULT_TN_SIZES = dict(featured=(455, 315), gallery=(205,155))


def save_thumbnail(data, path, filename, tn_sizes):
	"""
	Saves a base64 Weave visualization image file with alternative sizes to the given path in MEDIA_ROOT.
	TODO: save in database, otherwise the image bypasses the security architecture

	data: base64 image data 
	path: path under MEDIA_ROOT, without file extension
	tn_sizes: alternative sizes dictionary { thumbnail_type : (width, height) }

	"""

	# check for directory
	if not os.path.exists('%s/%s' % (settings.MEDIA_ROOT, path)):
		os.makedirs('%s/%s' % (settings.MEDIA_ROOT, path))

	# save visualization image
	visimg_data = base64.b64decode(data)
	visimg_filename = '%s/%s%s.png' % (settings.MEDIA_ROOT, path, filename)
	visimg_file = open(visimg_filename,'wb+')
	visimg_file.write(visimg_data)
	visimg_file.close()
	
	# save visualization thumbnails
	if tn_sizes != None:
		for tn_type in tn_sizes:
			tn = Image.open(visimg_filename)
			tn.thumbnail(tn_sizes[tn_type], Image.ANTIALIAS)
			tn.save('%s/%s%s_%s.png' % (settings.MEDIA_ROOT, path, filename, tn_type), 'PNG')

	

def index(request):
	"""
	Renders list of all avialable visualizations.
	Chronological order, paginated.
	"""
	return render_to_response('weave/index.html', locals(), 
		context_instance=RequestContext(request)
	)


@csrf_exempt
@transaction.commit_manually
def new(request):
	"""
	The view returns the default visualization.
	A POST request saves a new visualization.
	"""

	siteurl = settings.SITEURL[:-1]

	if request.method == 'GET':
		perm_change = True
		topics = Topic.objects.all()
		datasources = Datasource.objects.all()
		return render_to_response('weave/edit.html', locals(), 
			context_instance=RequestContext(request)
		)
	elif request.method == 'POST':
		if not request.user.is_authenticated():
			return HttpResponse(loader.render_to_string('401.html', 
				RequestContext(request, {'error_message': 
				_('You must be logged in to save a new visualizations.')})), status=401)
		try: 
			# instantiate new visualization
			visualization = Visualization(owner=request.user)

			visualization.save()
			visualization.set_default_permissions()
			visualization.update_from_viewer(request.POST)
			transaction.commit()

			# save visualization thumbnail
			save_thumbnail(data=request.POST.get('thumbnail'), path='weave_thumbnails/', filename=visualization.id, tn_sizes=DEFAULT_TN_SIZES)

			return HttpResponse(
				'{"visurl": "%s", "visid": "%i"}' % (visualization.get_absolute_url(), visualization.id),
				status=201,
				mimetype='application/json'
			)
		except Exception, e:
			transaction.rollback()
			return HttpResponse(
				"The server could not understand your request: " + str(e),
				status=400, 
				mimetype="text/plain"
			)

@csrf_exempt
@transaction.commit_manually
def edit(request, visid):
	"""	 
	The view that returns the visualization page for given visualization ID.
	A POST request updates given visualization.
	"""

	visualization = get_object_or_404(Visualization, pk=visid)
	siteurl = settings.SITEURL[:-1]

	if request.method == 'GET':

		# check permissons TODO: render to default template
		if not request.user.has_perm("weave.view_visualization", obj=visualization):
			return HttpResponse(loader.render_to_string('401.html', 
				RequestContext(request, {'error_message': 
				_("You are not permitted to view this Visualization.")})), status=401)
		
		# check user permissions
		perm_change = request.user.has_perm("weave.change_visualization", obj=visualization)

		# check visualiation permissions for authenticated users to find out if we can
		# set Visualization public or private in UI
		if visualization.get_gen_level(AUTHENTICATED_USERS) == PermissionLevelMixin.LEVEL_NONE:
			set_perm = 'public'
			get_perm = 'private'
		else:
			set_perm = 'private'
			get_perm = 'public'

		# get related topics
		topics = Topic.objects.all()
		related_topics = visualization.topics.select_related()
		# annotate selected topics
		for topic in topics:
			if topic in related_topics:
				topic.selected = True

		# get datasources
		datasources = Datasource.objects.all()
		related_datasources = visualization.datasources.select_related()
		# annotate selected datasources
		for datasource in datasources:
			if datasource in related_datasources:
				datasource.selected = True

		return render_to_response("weave/edit.html", locals(),
			context_instance=RequestContext(request))

	elif request.method == 'POST':
		# check permissions
		if not request.user.has_perm("weave.change_visualization", obj=visualization):
			return HttpResponse(loader.render_to_string('401.html', 
				RequestContext(request, {'error_message': 
				_("You are not permitted to edit this Visualization.")})), status=401)
		try:
			
			# save visualization thumbnail
			save_thumbnail(data=request.POST.get('thumbnail'), path='weave_thumbnails/', filename=visualization.id, tn_sizes=DEFAULT_TN_SIZES)

			# update existing visualization
			visualization.update_from_viewer(request.POST)
			transaction.commit()
			return HttpResponse(status=201)
		except Exception, e:
			transaction.rollback()
			return HttpResponse(
				"The server could not understand your request: " + str(e),
				status=400, 
				mimetype="text/plain"
			)


def delete(request, visid):
	"""
	Removes an existing Visualization
	FIXME: remove obsolete perm roles
	"""
	visualization = get_object_or_404(Visualization, pk=visid)

	if not request.user.has_perm('weave.delete_visualization', obj=visualization):
		return HttpResponse(loader.render_to_string('401.html', 
			RequestContext(request, {'error_message': 
				_("You are not permitted to delete this Visualization.")})), status=401)

	# delete visualization images
	path = '%s/weave_thumbnails/%i.png' % (settings.MEDIA_ROOT, visualization.id)
	if os.path.isfile(path):
			os.remove(path)
	for tn_type in DEFAULT_TN_SIZES:
		path = '%s/weave_thumbnails/%i_%s.png' % (settings.MEDIA_ROOT, visualization.id, tn_type)
		if os.path.isfile(path):
				os.remove(path)

	visualization.delete()

	return redirect('weave-new')


def sessionstate(request, visid):
	"""
	Returns a JSON session state for given visualization.
	"""
	# visualization 1 is the default visualization
	visualization = get_object_or_404(Visualization, pk=visid)
	# check permissions
	if not request.user.has_perm("weave.view_visualization", obj=visualization):
		return HttpResponse(loader.render_to_string('401.html', 
				RequestContext(request, {'error_message': 
				_("You don't have permission to access this configuration.")})), status=401)
	# return JSON session state
	return HttpResponse(
		visualization.sessionstate,
		status=201,
		mimetype='application/json'
	)


def set_permissions(request, visid):
	""" Toggles public and private Visualiztions """

	visualization = get_object_or_404(Visualization, pk=visid)

	if not request.user.has_perm("weave.change_visualization", obj=visualization):
		return HttpResponse(loader.render_to_string('401.html', 
			RequestContext(request, {'error_message': 
			_("You are not permitted to edit this Visualization.")})), status=401)

	if not request.method == 'POST':
		return HttpResponse(
			'You must use POST for editing Visualization permissions',
			status=405,
			mimetype='text/plain'
		)
	else:
		set_perm = request.POST.get('set_perm')
		if set_perm == 'Private':
			visualization.set_private_permissions()
		elif set_perm == 'Public':
			visualization.set_default_permissions()

		return HttpResponse(
			status=201
		)



def detail(request, visid):
	"""	 
	The view that returns the weave detail page for given visualization ID.
	"""
	visualization = get_object_or_404(Visualization, pk=visid)
	
	if not request.user.has_perm("weave.view_visualization", obj=visualization):
		return HttpResponse(
			"You don't have permission to view this visualizations.",
			mimetype="text/plain",
			status=401
		)
		
	# permissions for permissions editor	
	permissions_json = _perms_info_json(visualization, VISUALIZATION_LEV_NAMES)
	
	return render_to_response("weave/detail.html", locals(), 
		context_instance=RequestContext(request))


def embed(request, visid):
	"""
	The view that creates the embeddable page.
	"""
	visualization = get_object_or_404(Visualization, pk=visid)
	
	if not request.user.has_perm("weave.view_visualization", obj=visualization):
		return HttpResponse(
			"You don't have permission to view this visualizations.",
			mimetype="text/plain",
			status=401
		)
	
	return render_to_response("weave/embed.html", locals(), 
		context_instance=RequestContext(request))	

DEFAULT_VISUALIZATION_SEARCH_BATCH_SIZE = 10
MAX_VISUALIZATION_SEARCH_BATCH_SIZE = 25
def search(request):
	"""
	Should follow GeoNode's map search concept:

	the search accepts: 
	q - general query for keywords across all fields
	start - skip to this point in the results
	limit - max records to return
	sort - field to sort results on
	dir - ASC or DESC, for ascending or descending order

	for ajax requests, the search returns a json structure 
	like this:
	{
	'total': <total result count>,
	'next': <url for next batch if exists>,
	'prev': <url for previous batch if exists>,
	'query_info': {
		'start': <integer indicating where this batch starts>,
		'limit': <integer indicating the batch size used>,
		'q': <keywords used to query>,
	},
	'rows': [
		{
			'title': <map title>,
			'abstract': '...',
			'detail' : <url geonode detail page>,
			'owner': <name of the map's owner>,
			'owner_detail': <url of owner's profile page>,
			'last_modified': <date and time of last modification>
		},
	  ...
	]}
	"""
	if request.method == 'GET':
		params = request.GET
	elif request.method == 'POST':
		params = request.POST
	else:
		return HttpResponse(status=405)

	# grab params directly to implement defaults as
	# opposed to panicy django forms behavior.
	query = params.get('q', '')
	try:
		start = int(params.get('start', '0'))
	except:
		start = 0
	
	try:
		limit = min(int(params.get('limit', DEFAULT_VISUALIZATION_SEARCH_BATCH_SIZE)),
					MAX_VISUALIZATION_SEARCH_BATCH_SIZE)
	except: 
		limit = DEFAULT_VISUALIZATION_SEARCH_BATCH_SIZE


	sort_field = params.get('sort', u'')
	sort_field = unicodedata.normalize('NFKD', sort_field).encode('ascii','ignore')	 
	sort_dir = params.get('dir', 'ASC')
	result = _search(query, start, limit, sort_field, sort_dir)

	result['success'] = True
	return HttpResponse(json.dumps(result), mimetype="application/json")
	

def _search(query, start, limit, sort_field, sort_dir):

	keywords = _split_query(query)

	# catching an empty search
	if len(keywords) == 0:
		# session state #1 is the default one and should not show up in search
		visualizations = Visualization.objects.filter(Q(pk__gt=1))
	else:
		visualizations = Visualization.objects
	for keyword in keywords:
		visualizations = visualizations.filter(
			 Q(pk__gt=1),
			 Q(title__icontains=keyword)
			| Q(abstract__icontains=keyword)
			| Q(sessionstate__icontains=keyword))

	if sort_field:
		order_by = ("" if sort_dir == "ASC" else "-") + sort_field
		visualizations = visualizations.order_by(order_by)

	visualizations_list = []

	for visualization in visualizations.all()[start:start+limit]:
		try:
			owner_name = Contact.objects.get(user=visualization.owner).name
		except:
			owner_name = visualization.owner.username

		visualizationdict = {
			'id' : visualization.id,
			'title' : visualization.title,
			'abstract' : visualization.abstract,
			'detail' : reverse('geonode.weave.views.detail', args=(visualization.id,)),
			'owner' : owner_name,
			'owner_detail' : reverse('profiles.views.profile_detail', args=(visualization.owner.username,)),
			'last_modified' : visualization.last_modified.isoformat()
			}
		visualizations_list.append(visualizationdict)

	result = {'rows': visualizations_list, 
			  'total': visualizations.count()}

	result['query_info'] = {
		'start': start,
		'limit': limit,
		'q': query
	}
	if start > 0: 
		prev = max(start - limit, 0)
		params = urlencode({'q': query, 'start': prev, 'limit': limit})
		result['prev'] = reverse('geonode.weave.views.search') + '?' + params

	next = start + limit + 1
	if next < visualizations.count():
		 params = urlencode({'q': query, 'start': next - 1, 'limit': limit})
		 result['next'] = reverse('geonode.weave.views.search') + '?' + params

	return result


@csrf_exempt    
def search_page(request):
    # for non-ajax requests, render a generic search page

    if request.method == 'GET':
        params = request.GET
    elif request.method == 'POST':
        params = request.POST
    else:
        return HttpResponse(status=405)

    return render_to_response('weave/search.html', RequestContext(request, {
        'init_search': json.dumps(params or {}),
         "site" : settings.SITEURL
    }))

def ajax_visualization_permissions(request, visid):
	visualization = get_object_or_404(Visualization, pk=visid)

	if not request.user.has_perm("weave.change_map_permissions", obj=visualization):
		return HttpResponse(
			'You are not allowed to change permissions for this visualization',
			status=401,
			mimetype='text/plain'
		)

	if not request.method == 'POST':
		return HttpResponse(
			'You must use POST for editing visualization permissions',
			status=405,
			mimetype='text/plain'
		)

	if "authenticated" in request.POST:
		visualization.set_gen_level(AUTHENTICATED_USERS, request.POST['authenticated'])
	elif "anonymous" in request.POST:
		visualization.set_gen_level(ANONYMOUS_USERS, request.POST['anonymous'])
	else:
		user_re = re.compile('^user\\.(.*)')
		for k, level in request.POST.iteritems():
			match = user_re.match(k)
			if match:
				username = match.groups()[0]
				user = User.objects.get(username=username)
				if level == '':
					visualization.set_user_level(user, visualization.LEVEL_NONE)
				else:
					visualization.set_user_level(user, level)

	return HttpResponse(
		"Permissions updated",
		status=200,
		mimetype='text/plain'
	)
		
VISUALIZATION_LEV_NAMES = {
	Visualization.LEVEL_NONE  : _('No Permissions'),
	Visualization.LEVEL_READ  : _('Read Only'),
	Visualization.LEVEL_WRITE : _('Read/Write'),
	Visualization.LEVEL_ADMIN : _('Administrative')
}

def _perms_info_json(obj, level_names):
	info = obj.get_all_level_info()
	# these are always specified even if none
	info[ANONYMOUS_USERS] = info.get(ANONYMOUS_USERS, obj.LEVEL_NONE)
	info[AUTHENTICATED_USERS] = info.get(AUTHENTICATED_USERS, obj.LEVEL_NONE)
	info['users'] = sorted(info['users'].items())
	info['levels'] = [(i, level_names[i]) for i in obj.permission_levels]
	if hasattr(obj, 'owner') and obj.owner: info['owner'] = obj.owner.username
	return json.dumps(info)
