import os
import geonode
import masshealth

# Setting debug to true makes Django serve static media and
# present pretty error pages.
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Defines the directory that contains the settings file as the PROJECT_ROOT
# It is used for relative settings elsewhere.
PROJECT_ROOT = os.path.dirname(geonode.__file__)

#
# Default GeoNode Site settings
#

# Site id in the Django sites framework
SITE_ID = 2
SITEURL = "http://localhost:8000/"

ADMINS = (
    ('Christian Spanring', 'cspanring@mapc.org'),
)

# Directory of site specific settings
SITE_ROOT = os.path.abspath(os.path.dirname(__file__))

# Site specific templates
TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
)

# Site specific static files
STATICFILES_DIRS = [
    # os.path.join(SITE_ROOT, "static"),
    os.path.join(SITE_ROOT, 'static'),
]

# Site specific apps
SITE_APPS = (

    'django.contrib.flatpages',
    'django.contrib.gis',
    'django.contrib.markup',

    'masshealth.datastories',
    'masshealth.heroes',
    'masshealth.places',
    'masshealth.programs',
    'masshealth.visualizations',

)

SITE_MIDDLEWARE_CLASSES = (

    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

)

# Weave
WEAVE_URL = 'http://metrobostondatacommon.org/weave/'


DEBUG_TOOLBAR = DEBUG
if DEBUG_TOOLBAR:
    INTERNAL_IPS = ('127.0.0.1','10.0.2.2')
    SITE_MIDDLEWARE_CLASSES = ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.version.VersionDebugPanel',
        'debug_toolbar.panels.timer.TimerDebugPanel',
        'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
        'debug_toolbar.panels.headers.HeaderDebugPanel',
        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        'debug_toolbar.panels.template.TemplateDebugPanel',
        'debug_toolbar.panels.sql.SQLDebugPanel',
        'debug_toolbar.panels.signals.SignalDebugPanel',
        'debug_toolbar.panels.logger.LoggingPanel',
    )
    SITE_APPS += ('debug_toolbar',)
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }

# Global geonode settings
execfile(os.path.join(PROJECT_ROOT,'global_settings.py'))

#
# Global Settings Overrides
#

# Location of url mappings
ROOT_URLCONF = 'masshealth.urls'

# STATIC_URL = "/static_masshealth/"

FILEBROWSER_DIRECTORY = 'masshealth_filebrowser/'

# Load more settings from a file called local_settings.py if it exists
try:
    from local_settings import *
except ImportError:
    pass