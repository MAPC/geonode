from models import Hero
from django.contrib import admin

class HeroAdmin(admin.ModelAdmin):
    list_display = ['title', 'active','rank', 'last_modified', 'user', ]
    list_editable = ['active', 'rank']
    exclude = ('user',)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

class Commonmedia:
    js = (
        '/static/libs/tinymce/jscripts/tiny_mce/tiny_mce.js',
        '/static/js/textareas.js',
    )

admin.site.register(Hero,HeroAdmin,
    Media = Commonmedia,
    )
