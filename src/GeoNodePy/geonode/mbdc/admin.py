from django.contrib import admin

from geonode.mbdc.models import Hero, Featured, Page, Datasource, Topic

class HeroAdmin(admin.ModelAdmin):
	list_display = ('title', 'subtitle', 'active', 'order',)
	list_filter  = ('active',)
	list_editable = ('active', 'order',)

class FeaturedAdmin(admin.ModelAdmin):
	list_display = ('visualization', 'order',)
	list_editable = ('order',)

class PageAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}
	list_display = ('title', 'section', 'order',)
	list_editable = ('order', 'section', )
	ordering = ('section', 'order', )

class DatasourceAdmin(admin.ModelAdmin):
	list_display = ('title', )
	prepopulated_fields = {'slug': ('title',)}

class TopicAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}
	list_display = ('title', 'order', )
	list_editable = ('order',)

admin.site.register(Hero, HeroAdmin)
admin.site.register(Featured, FeaturedAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Datasource, DatasourceAdmin)
admin.site.register(Topic, TopicAdmin)