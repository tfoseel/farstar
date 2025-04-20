from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'nickname', 'lumen', 'is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('정보', {'fields': ('nickname', 'lumen')}),
        ('권한', {'fields': ('is_staff', 'is_superuser', 'groups')}),
        ('중요 날짜', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nickname', 'password1', 'password2'),
        }),
    )
    search_fields = ['email', 'nickname']
    filter_horizontal = ('groups', 'user_permissions')


admin.site.register(User, UserAdmin)
