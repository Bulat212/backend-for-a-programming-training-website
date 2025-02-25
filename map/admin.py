from django.contrib import admin

from map.models import ProjectMap, ProjectPosition

# Register your models here.
admin.site.register(ProjectPosition)
admin.site.register(ProjectMap)

# @admin.register(Project)
# class ProjectAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('name',)}
