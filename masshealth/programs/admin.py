from django.contrib.gis import admin
from django.conf import settings

from models import Program, Icon

try:
    _model_admin = admin.OSMGeoAdmin
except AttributeError:
    _model_admin = admin.ModelAdmin

# default GeoAdmin overloads
admin.GeoModelAdmin.default_lon = -7912100
admin.GeoModelAdmin.default_lat = 5210000
admin.GeoModelAdmin.default_zoom = 9
admin.GeoModelAdmin.openlayers_url = "%s/libs/openlayers/OpenLayers.js" % (settings.STATIC_URL)

def place_name(obj):
    return obj.place.name
place_name.short_description = 'Town'

class ProgramAdmin(_model_admin):
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'image', 'icon', 'order')
        }),
        ('Program Location', {
            'fields': ('place', 'geometry')
        }),
    )
    list_display = ['title', place_name, 'order', 'last_modified', 'user',]
    list_editable = ['order']
    ordering = ['place', 'order']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()
    
class Commonmedia:
    js = (
        '/static/libs/tinymce/jscripts/tiny_mce/tiny_mce.js',
        '/static/js/textareas.js',
    )


admin.site.register(Program, ProgramAdmin,
    Media = Commonmedia,
    )
admin.site.register(Icon)
