from django.contrib import admin
from geonode.datastories.models import Datastory, Page, Visualizationpage, Mappage, Storypage, Textpage


class DatastoryAdmin(admin.ModelAdmin):
	list_display = ('title', 'owner',)
	exclude = ('owner',)
	prepopulated_fields = {'slug': ('title',)}
	search_fields = ('title', 'abstract',)
	
	def save_model(self, request, obj, form, change):
		if getattr(obj, 'owner', None) is None:
			obj.owner = request.user
		obj.save()

class PageAdmin(admin.ModelAdmin):
	list_display = ('title', 'owner',)
	exclude = ('owner',)
	
	def save_model(self, request, obj, form, change):
		if getattr(obj, 'owner', None) is None:
			obj.owner = request.user
		obj.save()
	

class StorypageAdmin(admin.ModelAdmin):
	list_display = ('pk', 'datastory', 'page', 'pageorder')
	list_editable= ('pageorder',)
	list_display_links = ('pk',)
	ordering = ['datastory', 'pageorder']

admin.site.register(Datastory, DatastoryAdmin)
admin.site.register(Storypage, StorypageAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Visualizationpage, PageAdmin)
admin.site.register(Mappage, PageAdmin)
admin.site.register(Textpage, PageAdmin)