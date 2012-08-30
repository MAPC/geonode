from django.utils.translation import ugettext as _
from django.db import models
from django.db.models import permalink
from django.conf import settings


# limit order from 1-4
HERO_ORDER_CHOICES = tuple((i, i) for i in range(1,5))

SECTION_CHOICES = (
    ('about', 'About the Project'),
    ('resources', 'Resources'),
    ('community', 'Learning Community'),
    ('legal', 'Legal'),
)

class Hero(models.Model):
    """ Content to be showin in the homepage hero (slider) """

    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=50)
    navtitle = models.CharField('Navigation Title', max_length=50, blank=True, null=True, help_text='A short title to be used in the right-hand side link column.')
    navsubtitle = models.CharField('Navigation Subtitle', max_length=50, blank=True, null=True, help_text='A short subtitle to be used in the right-hand side link column.')
    content = models.TextField(null=True, blank=True)
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
    content = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')
        ordering = ['section', 'order', ]

    def __unicode__(self):
        return self.title
      
    @permalink
    def get_absolute_url(self):
        return ('mbdc-page', None, { 
            'slug': self.slug, 
            'section': self.section,
        })

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

    def get_absolute_url(self):
        return "/explore/gallery/?topics=%i" % self.id


class Calendar(models.Model):
    """ Stores Calendar pages """

    MONTH_CHOICES=(
        (1, 'January'), 
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December'),
    )
    year = models.IntegerField()
    month = models.IntegerField(choices=MONTH_CHOICES)

    title = models.CharField(max_length=100)
    abstract = models.TextField()

    topics = models.ManyToManyField('Topic', related_name='calendar_topics')
    sources = models.ManyToManyField('Datasource', related_name='calendar_sources')

    pdf_page = models.FileField(upload_to='calendar', help_text='Should be a PDF file.')
    thumbnail = models.ImageField(upload_to='calendar', help_text='Image dimensions should be 200x150.')

    class Meta:
        ordering = ['-year', 'month', ]
        verbose_name = _('Calendar page')
        verbose_name_plural = _('Calendar pages')

    def __unicode__(self):
        return self.title


class Upload(models.Model):
    """ Allows content editors to manage media """

    title = models.CharField(blank=False, max_length=100)
    upload = models.FileField(upload_to='uploads')
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_modified', 'title']

    def get_absolute_url(self):
        return "%s%s" % (settings.MEDIA_URL, self.upload)
   