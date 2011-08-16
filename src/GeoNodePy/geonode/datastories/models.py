from django.utils.translation import ugettext as _

from django.db import models

from django.contrib.auth.models import User

from geonode.maps.models import Map
from geonode.weave.models import Visualization
		
		
class Page(models.Model):
	""" 
	The is the parent class for all possible page types.
	"""
	
	title = models.CharField(_('Title'), max_length=100)
	owner = models.ForeignKey(User, verbose_name=_('owner'), blank=True, null=True)
	last_modified = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
		return '%s by %s' % (self.title, (self.owner.username if self.owner else "<Anonymous>"))

class Textpage(Page):
	"""
	A page showing text only.
	"""
	
	abstract = models.TextField(_('Abstract'), blank=True, null=True)
		
class Visualizationpage(Page):
	"""
	A page showing a Weave visualization.
	"""
	
	caption = models.TextField(_('Caption'), blank=True, null=True)
	visualization = models.ForeignKey(Visualization)
	
	@models.permalink
	def get_absolute_url(self):
		return ('geonode.weave.views.edit', None, { 'visid': self.visualization.id, })
	
class Mappage(Page):
	"""
	A page showing a Map.
	"""
	
	caption = models.TextField(_('Caption'), blank=True, null=True)
	map = models.ForeignKey(Map)
	
	@models.permalink
	def get_absolute_url(self):
		return ('geonode.maps.views.view', None, { 'mapid': self.map.id, })


class Datastory(models.Model):
	"""
	Model to store a data story, a step-by-step walk through data exploration.
	"""

	title = models.CharField(_('Title'), max_length=100)
	slug  = models.SlugField(max_length=100)
	abstract = models.TextField(_('Abstract'), blank=True, null=True)

	owner = models.ForeignKey(User, verbose_name=_('owner'), blank=True, null=True)
	last_modified = models.DateTimeField(auto_now_add=True)

	datastory = models.ManyToManyField(Page, through='Storypage')

	def __unicode__(self):
		return '%s by %s' % (self.title, (self.owner.username if self.owner else "<Anonymous>"))

	class Meta:
		unique_together = (('title', 'owner'),)
		verbose_name_plural = "Datastories"

class Storypage(models.Model):
	"""
	Amending the ManyToMany Datastory-Page relation with additional information.
	"""
	
	datastory = models.ForeignKey(Datastory)
	page = models.ForeignKey(Page)
	pageorder = models.IntegerField('Order')

