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
        'PASSWORD': 'mapc.django',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '9876',                      # Set to empty string for default. Not used with sqlite3.
    }
}

SECRET_KEY = '3=l!*qfg9qo4i-pg586apk=-ki0si2^0rv28+t0q)i=&amp;vrnyo='

# The username and password for a user that can add and
# edit layer details on GeoServer
# GEOSERVER_BASE_URL = "http://localhost:8080/geoserver/"
GEOSERVER_BASE_URL = "http://metrobostondatacommon.org/geoserver/"
GEOSERVER_CREDENTIALS = "admin", "mapc.451"

MEDIA_ROOT = '/var/www/public/geonode.metrobostondatacommon.org/uploaded'
STATIC_ROOT = '/var/www/public/geonode.metrobostondatacommon.org/static'

TEMPLATE_DIRS += (
    # '/home/django/domains/ourhealthymass.org/private/masshealth/templates',
    # '/home/django/virtualenvs/geonode/lib/python2.6/site-packages/django/contrib/gis/templates',
)

EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'AKIAIFJGGNCL3QHARMYQ'
EMAIL_HOST_PASSWORD = 'AsY5911gvTIYA6T6drMqDhSt5MPG1leQpvdjA3Rb0sG5'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'MAPC Web App <webapp@mapc.org>'


