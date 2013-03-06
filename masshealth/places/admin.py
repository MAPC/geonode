from django.contrib.gis import admin
from models import Place

try:
    _model_admin = admin.OSMGeoAdmin
except AttributeError:
    _model_admin = admin.ModelAdmin

class PlaceAdmin(_model_admin):
    list_display = ['name', 'last_modified', 'user', ]
    exclude = ('user', 'geometry', )

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


class Commonmedia:
    js = (
        '/static/libs/tinymce/jscripts/tiny_mce/tiny_mce.js',
        '/static/js/textareas.js',
    )
    
admin.site.register(Place, PlaceAdmin,
    Media = Commonmedia,
    )
