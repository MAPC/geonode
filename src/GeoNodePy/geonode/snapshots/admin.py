from django.contrib.gis import admin

from geonode.snapshots.models import Regionalunit, Regiontype, Visualization


class RegionalunitAdmin(admin.OSMGeoAdmin):    
    list_filter = ['regiontype', ]
    list_display = ('name', )
    search_fields = ['name', ]
    ordering = ['name', ]
    prepopulated_fields = {'slug': ('name',)}

class RegiontypeAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}

admin.site.register(Regionalunit, RegionalunitAdmin)
admin.site.register(Regiontype, RegiontypeAdmin)
admin.site.register(Visualization, admin.ModelAdmin)