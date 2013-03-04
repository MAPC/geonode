from settings import *

DEBUG = True
# True will also try loading Weave dependencies from :8000
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Christian Spanring', 'cspanring@mapc.org'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'geonode',                      # Or path to database file if using sqlite3.
        'USER': 'django',                      # Not used with sqlite3.
        'PASSWORD': 'django',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

SECRET_KEY = '3=l!*qfg9qo4i-pg586apk=-ki0si2^0rv28+t0q)i=&amp;vrnyo='

# The username and password for a user that can add and
# edit layer details on GeoServer
# GEOSERVER_CREDENTIALS = "admin", "mapc.451"

# MEDIA_ROOT = '/home/django/domains/geonode.metrobostondatacommon.org/public/uploaded'
# STATIC_ROOT = 'home/django/domains/geonode.metrobostondatacommon.org/public/static'

TEMPLATE_DIRS += (
    # '/home/django/domains/ourhealthymass.org/private/masshealth/templates',
    # '/home/django/virtualenvs/geonode/lib/python2.6/site-packages/django/contrib/gis/templates',
)