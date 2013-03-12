from django.utils.translation import ugettext as _
from django.contrib.gis.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.conf import settings

class Program(models.Model):
    title = models.CharField(max_length=100)
    description =  models.TextField(_('Program Description'),
                                    blank=True, default='')
    date = models.DateTimeField(_('Created'), auto_now_add=True)
    image = models.ImageField(_('Image'),
                              upload_to=settings.FILEBROWSER_DIRECTORY + 'programs/img/%y%U',
                              max_length=255,
                              blank=True,
                              default='',
                              help_text="Image will be shown at 120x80 in map info windwo.")
    place = models.ForeignKey('places.Place')

    icon = models.ForeignKey('programs.Icon', blank=True, null=True)

    geometry = models.PointField(_('Location'), srid=26986, null=True, blank=True)

    order = models.IntegerField(default=500, blank=True, null=True)

    user = models.ForeignKey(User, verbose_name=u'Last modified by')
    last_modified = models.DateTimeField(auto_now=True, editable=True)

    objects = models.GeoManager()

    class Meta:
        db_table = 'masshealth_programs_program'
        ordering = ['order']


    def __unicode__(self):
        return 'Program %s @ %s' % (self.title, self.place.name)

    def save(self, *args, **kwargs):
        # defaults location to place-centroid
        if not self.geometry:
            self.geometry = self.place.geometry.centroid

        super(Program, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "%s#%s" % (self.place.get_absolute_url(), slugify(self.title))


class Icon(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    image = models.ImageField(_('Image'),
                              upload_to=settings.FILEBROWSER_DIRECTORY + 'programs/icons/%y%U',
                              max_length=255,
                              blank=True,
                              default='')
    map_icon = models.ImageField(_('Map Icon'),
                              upload_to=settings.FILEBROWSER_DIRECTORY + 'programs/map_icons/%y%U',
                              max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'masshealth_programs_icon'
