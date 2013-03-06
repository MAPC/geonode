from django.utils.translation import ugettext as _
from django.db import models
from django.contrib.auth.models import User

class Hero(models.Model):
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=100,verbose_name='subtitle')
    description =  models.TextField(_('Description'),
                                    blank=True, default='')
    image = models.ImageField(_('Image'),
                              upload_to='heroes/img/%y%U',
                              max_length=255,
                              blank=False)
    rank = models.IntegerField(_('Order'), default=500)
    active = models.BooleanField(_('Active'), default=True)
    show_in = models.CharField(_('Selector'), max_length=200,
                               default='homepage', help_text=_(
        'This hero will only be included by the template tag if this '
        'field matches the tag\'s argument'))

    user = models.ForeignKey(User, verbose_name=u'Last modified by')
    last_modified = models.DateTimeField(auto_now=True, editable=True)

    def __unicode__(self):
        return '%s(%s)' % (self.title, self.type)

    class Meta:
        db_table = 'masshealth_heroes_hero'
        ordering = ['rank', 'title']
