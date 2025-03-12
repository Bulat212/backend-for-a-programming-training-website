from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from style.models import Style
from .models import User, UserProject

admin.site.register(UserProject)

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'coins', 'stars', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('nickname_id', 'background_profile', 'description', 'photo', 'experience', 'coins', 'stars')}),
    )
    # ist_filter = ('is_staff', 'is_superuser', 'is_active')
    readonly_fields = ('nickname_id', 'background_profile')

    
admin.site.register(User, CustomUserAdmin)
