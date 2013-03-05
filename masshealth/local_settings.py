import masshealth.settings

# Private Settings

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
GEOSERVER_CREDENTIALS = "admin", "geoserver"

DEFAULT_MAP_CENTER = (-71.8, 42.3)

# How tightly zoomed should newly created maps be?
# 0 = entire world;
# maximum zoom is between 12 and 15 (for Google Maps, coverage varies by area)
DEFAULT_MAP_ZOOM = 9

GEOSERVER_BASE_URL = "http://localhost:8080/geoserver/"

MAP_BASELAYERS = [{
    "source": {
        "ptype": "gxp_wmscsource",
        "url": GEOSERVER_BASE_URL + "wms",
        "restUrl": "/gs/rest"
     }
  },{
    "source": {"ptype": "gx_olsource"},
    "type":"OpenLayers.Layer",
    "args":["No background"],
    "visibility": False,
    "fixed": True,
    "group":"background"
  }, {
    "source": {"ptype": "gx_olsource"},
    "type":"OpenLayers.Layer.OSM",
    "args":["OpenStreetMap"],
    "visibility": False,
    "fixed": True,
    "group":"background"
  }, {
    "source": {"ptype": "gxp_mapquestsource"},
    "name":"osm",
    "group":"background",
    "visibility": True
  }, {
    "source": {"ptype": "gxp_bingsource"},
    "name": "Aerial",
    "fixed": True,
    "visibility": False,
    "group":"background"
  }, {
    "source": {"ptype": "gxp_mapboxsource"},
  }, {
    "source": {"ptype": "gx_olsource"},
    "type":"OpenLayers.Layer.OSM",
    "args":["MAPC Basemap", "http://tiles.mapc.org/basemap/${z}/${x}/${y}.png"],
    "visibility": False,
    "fixed": True,
    "group":"background"
  }]

# STATIC_URL = "/static_masshealth/"

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025