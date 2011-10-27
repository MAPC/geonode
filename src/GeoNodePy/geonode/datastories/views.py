from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from geonode.datastories.models import Datastory

# Create your views here.

def story(request, slug):
	"""
	Returns overview/intro for a Datastory.
	"""
	
	datastory = get_object_or_404(Datastory, slug=slug)
	
	return 'gut'
	
def page(request):
	"""
	Returns a single Datastory-Page
	"""
	return 'gut'

def search_page(request):
	"""
	Returns page with paginated search results.
	"""
	return 'gut'

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
	return 'gut'

