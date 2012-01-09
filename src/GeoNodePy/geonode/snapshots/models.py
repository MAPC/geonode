from django.contrib.gis.db import models
from django.db.models import permalink
from django.core.files.storage import FileSystemStorage

# lazy translation
from django.utils.translation import ugettext_lazy as _

from geonode.mbdc.models import TOPICS

import os

# south introspection rules 
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^django\.contrib\.gis\.db\.models\.fields\.MultiPolygonField'])
except ImportError:
    pass

SNAPSHOTS_PATH = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_PATH = FileSystemStorage(location=os.path.join(SNAPSHOTS_PATH,'templates'))

class Regiontype(models.Model):
	""" Types of geographies to create snapshots for. """

	name = models.CharField(max_length=100)
	slug = models.SlugField()

	class Meta:
		verbose_name = _('Regional type')
		verbose_name_plural = _('Regional types')

	def __unicode__(self):
	 	return self.name

class Regionalunit(models.Model):
	""" Regional units for snapshots. """

	unitid = models.CharField(max_length=20)
	# unitid = models.IntegerField()
	name = models.CharField(max_length=100)
	slug = models.SlugField()
	regiontype = models.ForeignKey('Regiontype', blank=True, null=True)
	geometry = models.MultiPolygonField(srid=26986)

	objects = models.GeoManager()

	class Meta:
		ordering = ['name']
		verbose_name = _('Regional unit')
		verbose_name_plural = _('Regional units')

	def __unicode__(self):
	 	return self.name

class Visualization(models.Model):
	""" Visualizations for Snapshot pages 
		TODO: add thumbnail flag, slug
	"""

	# title, topic, session state, year, source
	title = models.CharField(max_length=100)
	topic = models.CharField(max_length=20, choices=TOPICS)

	regiontype = models.ForeignKey('Regiontype', default=1)

	sessionstate = models.FileField(_('Session State'), upload_to='snapshots/visualizations', storage=TEMPLATE_PATH, help_text='Weave session state XML incl. Django template variable {{ regionalunit.unitid }}')

	year = models.CharField(max_length=20, blank=True, null=True)
	source = models.ManyToManyField('mbdc.Datasource', blank=True, null=True)

	def __unicode__(self):
	 	return self.title

	@permalink
	def get_sessionstate_url(self, regiontype_slug, regionalunit_slug):

	 	return ('snapshots-sessionstate', None, { 
	 			'visid': self.id, 
	 			'regiontype_slug': regiontype_slug,
	 			'regionalunit_slug': regionalunit_slug,
	 		})