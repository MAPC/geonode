from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

import os

# Global geonode URLs
execfile(os.path.join(settings.PROJECT_ROOT,'urls.py'))

# There appears to be an import order bug (probably
# a Django bug) that results in an exception in
# admin.autodiscover().  It involves "lazy"
# relationships, such as the places ManyToMany field
# in the datastories.models.Story model, where the
# related model is specified as a string, such as
# 'places.Place', in this field's definition.
#
# With DEBUG==False, the models will not have already
# been imported by this point, and the string based
# lazy reference will not have been converted to
# a model reference.  If admin.autodiscover() winds
# up processing datastories first, it will mistakenly
# attempt to use the string as though it were a model
# class.
#
# As a work-around, it seems sufficient to import
# places.models here.  A more general solution is
# to force the app model cache to be populated at
# this point (under the development server this is
# done duirng the "Validating models" phase, and is
# apparently also done when DEBUG==True, at least
# in some configurations).  If you need it, it is:
#
# import django.db.models.loading
# if not django.db.models.loading.app_cache_ready():
#     django.db.models.loading.get_app_errors()
#
# (That's roughly what "Validating models" does.)
import masshealth.places.models

from masshealth.monkey_patches import admin as mpa
mpa.flatpages()

# Site specific URLs
urlpatterns += patterns('',

    # ('^new-weave/$', direct_to_template, {'template': 'new_weave.html'}),
    url(r'^story/', include('masshealth.datastories.urls')),
    url(r'^visualizations/', include('masshealth.visualizations.urls')),
    url(r'^place/', include('masshealth.places.urls')),
    url(r'^crossdomain.xml$', 'masshealth.visualizations.views.crossdomain'),
    url(r'^program/', include('masshealth.programs.urls')),

    (r'^pages/', include('django.contrib.flatpages.urls')),

)

# Global geonode settings
# execfile(os.path.join(settings.PROJECT_ROOT,'urls.py'))