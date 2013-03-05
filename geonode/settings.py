import os
import geonode

# Setting debug to true makes Django serve static media and
# present pretty error pages.
DEBUG = TEMPLATE_DEBUG = True

# Defines the directory that contains the settings file as the PROJECT_ROOT
# It is used for relative settings elsewhere.
PROJECT_ROOT = os.path.dirname(geonode.__file__)

# Activate the Documents application
DOCUMENTS_APP = True

INSTALLED_APPS = (

    # Apps bundled with Django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.humanize',

    # Third party apps

    # Utility
    'pagination',
    'taggit',
    'taggit_templatetags',
    'south',
    'friendlytagloader',
    'geoexplorer',
    'request',

    # Theme
    "pinax_theme_bootstrap_account",
    "pinax_theme_bootstrap",
    'django_forms_bootstrap',

    # Social
    'account',
    'avatar',
    'dialogos',
    'agon_ratings',
    'notification',
    'announcements',
    'actstream',
    'relationships',
    'user_messages',

    # GeoNode internal apps
    'geonode.people',
    'geonode.layers',
    'geonode.upload',
    'geonode.maps',
    'geonode.proxy',
    'geonode.security',
    'geonode.search',
    'geonode.catalogue',
    'geonode.documents',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(message)s',        },
    },
    'handlers': {
        'null': {
            'level':'ERROR',
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level':'ERROR',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "ERROR",
        },
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "geonode": {
            "handlers": ["console"],
            "level": "ERROR",
        },

        "gsconfig.catalog": {
            "handlers": ["console"],
            "level": "ERROR",
        },
        "owslib": {
            "handlers": ["console"],
            "level": "ERROR",
        },
        "pycsw": {
            "handlers": ["console"],
            "level": "ERROR",
        },
        'south': {
            "handlers": ["console"],
            "level": "ERROR",
        },
    },
}

#
# Default GeoNode Site settings
#

# Site id in the Django sites framework
SITE_ID = 1
SITEURL = "http://localhost:8000/"

# Directory of site specific settings
SITE_ROOT = os.path.abspath(os.path.dirname(__file__))

# Site specific templates
TEMPLATE_DIRS = (
    # os.path.join(SITE_ROOT, "templates"),
)

# Site specific static files
STATICFILES_DIRS = [
	# os.path.join(SITE_ROOT, "static"),
]

# Site specific apps
SITE_APPS = ()

# Site specific apps
SITE_MIDDLEWARE_CLASSES = ()

# Global geonode settings
execfile(os.path.join(PROJECT_ROOT,'global_settings.py'))

#
# Global Settings Overrides
#

# Load more settings from a file called local_settings.py if it exists
try:
    from local_settings import *
except ImportError:
    pass
