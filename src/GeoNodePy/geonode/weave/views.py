from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
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

from django.conf import settings

from geonode.maps.views import _split_query

from geonode.core.models import AUTHENTICATED_USERS, ANONYMOUS_USERS
from geonode.maps.models import Contact
from geonode.weave.models import Visualization

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
	if request.method == 'GET':
		# we treat visualization nr 1 as default visualization (session state)
		visualization = get_object_or_404(Visualization, pk=1)
		return render_to_response('weave/edit.html', locals(), 
			context_instance=RequestContext(request)
		)
	elif request.method == 'POST':
		if not request.user.is_authenticated():
			return HttpResponse(
				'You must be logged in to save new visualizations.',
				mimetype="text/plain",
				status=401
			)
		try: 
			# save new visualization
			visualization = Visualization(owner=request.user)
			visualization.save()
			visualization.set_default_permissions()
			visualization.update_from_viewer(request.POST)
			transaction.commit()
			return HttpResponse(
				'{"visid": %i}' % (visualization.id),
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
	
	if request.method == 'GET':
		# check permissons
		if not request.user.has_perm("weave.view_visualization", obj=visualization):
			return HttpResponse(
					"You don't have permission to view this visualizations.",
					mimetype="text/plain",
					status=401)
		return render_to_response("weave/edit.html", locals(),
			context_instance=RequestContext(request))
	elif request.method == 'POST':
		# check permissions
		if not request.user.has_perm("weave.change_visualization", obj=visualization):
			return HttpResponse(
					"You don't have permission to edit this visualizations.",
					mimetype="text/plain",
					status=401)
		try:
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

def sessionstate(request, visid=1):
	"""
	Returns a JSON session state for given visualization.
	"""
	# visualization 1 is the default visualization
	visualization = get_object_or_404(Visualization, pk=visid)
	# check permissions
	if not request.user.has_perm("weave.view_visualization", obj=visualization):
		return HttpResponse(
			"You don't have permission to access this Session State.",
			mimetype="text/plain",
			status=401
		)
	# return JSON session state
	return HttpResponse(
		visualization.sessionstate,
		status=201,
		mimetype='application/json'
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

	visualizations = Visualization.objects
	for keyword in keywords:
		visualizations = visualizations.filter(
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