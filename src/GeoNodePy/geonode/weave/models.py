from django.utils.translation import ugettext as _

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User, Permission

from geonode.core.models import PermissionLevelMixin
from geonode.core.models import AUTHENTICATED_USERS, ANONYMOUS_USERS

from geonode.mbdc.models import Topic, Datasource

import simplejson

try:
	from south.modelsinspector import add_introspection_rules
	add_introspection_rules([], ['^jsonfield\.fields\.JSONField'])
except ImportError:
	pass

class Visualization(models.Model, PermissionLevelMixin):
	"""
	Model to store Weave session state, based on GeoNode's Map model
	"""

	title = models.CharField(_('Title'), max_length=100, blank=True, null=True)
	"""
	A display name suitable for search results and page headers
	"""

	year = models.CharField(max_length=50, blank=True, null=True)
	"""
	Year(s) as String to support timeranges, as in ACS for instance.
	"""

	abstract = models.TextField(_('Abstract'), blank=True, null=True)
	"""
	A longer description of the themes in the visualization.
	"""

	topics = models.ManyToManyField('mbdc.Topic', related_name='weave_topics', blank=True, null=True)
	"""
	Topic category under which the visualization should be listed
	"""

	datasources = models.ManyToManyField('mbdc.Datasource', related_name='weave_datasources', blank=True, null=True)
	"""
	List of data sources used in visualization
	"""

	owner = models.ForeignKey(User, verbose_name=_('owner'))
	"""
	The user that created/owns this map.
	"""

	original = models.ForeignKey('self', blank=True, null=True)
	""" 
	The original object if duplicated. 
	"""

	last_modified = models.DateTimeField(auto_now=True)
	"""
	The last time the map was modified.
	"""

	# TODO: cleanup Booleans from Python 'True' to JavaScript 'true'
	# sessionstate = JSONField(_('Session State'))
	# ...if we ever need the JSONField
	sessionstate = models.TextField(_('Session State'))
	"""
	The configuration that specifies all aspects of a visualization.
	"""

	def __unicode__(self):
		return '%s by %s' % (self.title, (self.owner.username if self.owner else "<Anonymous>"))

	def update_from_viewer(self, conf):
		"""
		Update this Visualization's details by parsing a JSON object as produced by
		a Weave Flash instance.	 

		This method automatically persists to the database!
		"""
		self.title = conf['title']
		self.year = conf['year']
		self.abstract = conf['abstract']
		self.sessionstate = conf['sessionstate']

		try:
			self.original = Visualization.objects.get(pk=conf['original'])
		except:
			pass

		self.save()

		try:
			# remove obsolete related topics
			self.topics.clear()
			# update related topics
			related_topics = simplejson.loads(conf['topics'])
			for topic_id in related_topics:
				self.topics.add(Topic.objects.get(pk=topic_id))
		except:
			pass
		

		try:
			# remove obsolete related topics
			self.datasources.clear()
			# update datasources
			datasources = simplejson.loads(conf['datasources'])
			for datasource_id in datasources:
				self.datasources.add(Datasource.objects.get(pk=datasource_id))
		except:
			pass
	
	@models.permalink
	def get_absolute_url(self):
		return ('geonode.weave.views.edit', None, { 'visid': self.id, })
	
	class Meta:
		ordering = ['-last_modified']
		# custom permissions, 
		# change and delete are standard in django
		permissions = (('view_visualization', 'Can view'), 
					   ('change_visualization_permissions', "Can change permissions"), )

	# Permission Level Constants
	# LEVEL_NONE inherited
	LEVEL_READ	= 'visualization_readonly'
	LEVEL_WRITE = 'visualization_readwrite'
	LEVEL_ADMIN = 'visualization_admin'

	def set_default_permissions(self):
		self.set_gen_level(ANONYMOUS_USERS, self.LEVEL_READ)
		self.set_gen_level(AUTHENTICATED_USERS, self.LEVEL_READ)

		# remove specific user permissions
		current_perms =	 self.get_all_level_info()
		for username in current_perms['users'].keys():
			user = User.objects.get(username=username)
			self.set_user_level(user, self.LEVEL_NONE)

		# assign owner admin privs
		if self.owner:
			self.set_user_level(self.owner, self.LEVEL_ADMIN)


	def set_private_permissions(self):
		""" Only owner can access Visualization """
		self.set_gen_level(ANONYMOUS_USERS, self.LEVEL_NONE)
		self.set_gen_level(AUTHENTICATED_USERS, self.LEVEL_NONE)
