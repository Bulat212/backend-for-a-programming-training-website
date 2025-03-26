from django.contrib import admin

from project.models import Language, Project

# Register your models here.
# admin.site.register(Project)
# admin.site.register(Language)

admin.site.register(Language)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
