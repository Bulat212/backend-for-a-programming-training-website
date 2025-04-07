from django.contrib import admin

from project.models import Language, Project, ProjectLanguage

# Register your models here.

admin.site.register(Language)
admin.site.register(ProjectLanguage)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
