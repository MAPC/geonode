from django.contrib.auth import authenticate, get_backends as get_auth_backends

from geonode.weave.models import Visualization

def get_readable_vis(user):
	"""
	Returns a set of viewable weave visualizations for given user. 
	"""

	readable_vis = set()
	for bck in get_auth_backends():
		if hasattr(bck, 'objects_with_perm'):
			readable_vis.update(bck.objects_with_perm(user, 'weave.view_visualization', Visualization))
	
	return readable_vis