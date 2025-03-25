from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from style.models import Style
from .models import ProgressLog, User, UserProgress, UserProject, UserSkill

admin.site.register(UserProject)
admin.site.register(UserProgress)
admin.site.register(ProgressLog)
admin.site.register(UserSkill)

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'coins', 'stars', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('nickname_id', 'background_profile', 'description', 'photo', 'experience', 'coins', 'stars')}),
    )
    # ist_filter = ('is_staff', 'is_superuser', 'is_active')
    readonly_fields = ('nickname_id', 'background_profile')

    
admin.site.register(User, CustomUserAdmin)
