from django.contrib import admin
from . import models

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'slug')
    fields = ('name', 'owner', 'short_description')

admin.site.register(models.Membership)
admin.site.register(models.OccupiedBlock)
admin.site.register(models.Project, ProjectAdmin)
