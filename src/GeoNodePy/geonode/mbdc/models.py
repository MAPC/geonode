from django.utils.translation import ugettext as _
from django.db import models
from django.db.models import permalink

from markupfield.fields import MarkupField


# limit order from 1-4
HERO_ORDER_CHOICES = tuple((i, i) for i in range(1,5))

SECTION_CHOICES = (
    ('about', 'About the Project'),
    ('resources', 'Resources'),
    ('community', 'Community'),
    ('legal', 'Legal'),
)

class Hero(models.Model):
    """ Content to be showin in the homepage hero (slider) """

    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=50)
    navtitle = models.CharField('Navigation Title', max_length=50, blank=True, null=True, help_text='A short title to be used in the right-hand side link column.')
    navsubtitle = models.CharField('Navigation Subtitle', max_length=50, blank=True, null=True, help_text='A short subtitle to be used in the right-hand side link column.')
    content = models.TextField()
    image = models.ImageField('Image file', upload_to='hero_img', help_text='Image proportions should be 320x220.')
    order = models.IntegerField(blank=True, null=True, choices=HERO_ORDER_CHOICES)

    active = models.BooleanField()
    
    class Meta:
        ordering = ['order']
        verbose_name = _('Hero entry')
        verbose_name_plural = _('Hero entries')

    def __unicode__(self):
        return self.title

class Featured(models.Model):
    """ Weave Visualizations shown on homepage """
    visualization = models.ForeignKey('weave.Visualization')
    order = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['order']
        verbose_name_plural = _('Featured visualizations')

    def __unicode__(self):
        return self.visualization.title


class Page(models.Model):
    """ Content for flat pages organized by sections """

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    section = models.CharField(max_length=20, null=True, blank=True, choices=SECTION_CHOICES)
    order = models.IntegerField(blank=True, null=True)
    content = MarkupField(default_markup_type='markdown', null=True, blank=True)

    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')
        ordering = ['section', 'order', ]

    def __unicode__(self):
        return self.title
      
    @permalink
    def get_absolute_url(self):
        return ("mbdc-page", None, { "slug": self.slug, })

class Datasource(models.Model):
    """ 
    Data sources picklist to be used accross the project. 
    """

    title = models.CharField(max_length=100)
    slug = models.SlugField()

    url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.title

    # @permalink
    # def get_absolute_url(self):
    #   return ("mbdc-page", None, { "slug": self.slug, })


class Topic(models.Model):
    """
    Predifined indicator and data topics (categories), used in applications across the plattform.
    """

    title = models.CharField(max_length=100)
    slug = models.SlugField()

    order = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')
        ordering = ['order']

    def __unicode__(self):
        return self.title

