import os
from django.contrib.gis.utils import LayerMapping

from models import Regionalunit

muni_mapping = {
	'unitid': 'muni_id',
	'name': 'name',
	'geometry': 'MULTIPOLYGON'
}

muni_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/MAPC_municipalities.shp'))

def load_muni(verbose=True):
    lm = LayerMapping(Regionalunit, muni_shp, muni_mapping, transform=False, encoding='iso-8859-1')

    lm.save(strict=True, verbose=verbose)