from django.http import HttpResponse
from django.utils import simplejson
from django.template.defaultfilters import truncatewords

from models import Program

def build_program_geojson(programs):
    """ 
    Takes a Program Queryset and returns a GeoJSON object 
    with title, description and image-url properties. 
    """

    features = []

    for program in programs:
        # truncatewords
        properties = dict(title=program.title, description=truncatewords(program.description,20), absolute_url=program.get_absolute_url(), map_icon='layer-0')
        if program.image:
            properties['image_url'] = program.image.url
        if program.icon:
            properties['map_icon'] = program.icon.map_icon.url
        geometry = simplejson.loads(program.geometry.geojson)
        feature = dict(type='Feature', geometry=geometry, properties=properties)
        features.append(feature)

    response = dict(type='FeatureCollection', features=features)

    return simplejson.dumps(response)


def all_geojson(request):
    """
    Return a GeoJSON representation of all Programs.
    """

    try:
      programs = Program.objects.transform(4326).all().select_related()
    except Program.DoesNotExist:
      raise Http404

    geojson = build_program_geojson(programs)

    return HttpResponse(geojson, mimetype='application/json')


def place_geojson(request, place_slug):
    """
    Return a GeoJSON representation of all Programs in a Place.
    """

    try:
        programs = Program.objects.transform(4326).filter(place__slug__iexact=place_slug).select_related()
    except Program.DoesNotExist:
        raise Http404

    geojson = build_program_geojson(programs)

    return HttpResponse(geojson, mimetype='application/json')
