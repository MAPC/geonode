from django.contrib.gis.db import models

# lazy translation
from django.utils.translation import ugettext_lazy as _

# south introspection rules 
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^django\.contrib\.gis\.db\.models\.fields\.MultiPolygonField'])
except ImportError:
    pass

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
	regiontype = models.ForeignKey('regiontype', blank=True, null=True)
	geometry = models.MultiPolygonField(srid=26986)

	objects = models.GeoManager()

	class Meta:
		ordering = ['name']
		verbose_name = _('Regional unit')
		verbose_name_plural = _('Regional units')

	def __unicode__(self):
	 	return self.name