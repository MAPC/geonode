from django.utils.translation import ugettext as _
from django.db import models

# limit order from 1-4
HERO_ORDER_CHOICES = tuple((i, i) for i in range(1,5))

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
    