from django.contrib import admin
from weave.models import Visualization

admin.site.register(Visualization, admin.ModelAdmin)