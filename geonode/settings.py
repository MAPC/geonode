import os
import geonode

# Setting debug to true makes Django serve static media and
# present pretty error pages.
DEBUG = TEMPLATE_DEBUG = True

# Defines the directory that contains the settings file as the PROJECT_ROOT
# It is used for relative settings elsewhere.
PROJECT_ROOT = os.path.dirname(geonode.__file__)

#
# Default GeoNode Site settings
#

# Site id in the Django sites framework
SITE_ID = 1

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

# Global geonode settings
execfile(os.path.join(PROJECT_ROOT,'global_settings.py'))

LEAFLET_CONFIG = {
    'TILES_URL': 'http://{s}.tile2.opencyclemap.org/transport/{z}/{x}/{y}.png'
}

# Load more settings from a file called local_settings.py if it exists
try:
    from local_settings import *
except ImportError:
    pass
