from django.contrib import admin

from geonode.mbdc.models import Hero

class HeroAdmin(admin.ModelAdmin):
	list_display = ('title', 'subtitle', 'active', 'order')
	list_filter  = ('active',)
	list_editable = ('active', 'order',)


admin.site.register(Hero, HeroAdmin)