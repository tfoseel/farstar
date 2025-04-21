from django.contrib import admin
from .models import Star


@admin.register(Star)
class StarAdmin(admin.ModelAdmin):
    list_display = ('name', 'constellation', 'ra',
                    'dec', 'magnitude', 'spectral_type')
    list_filter = ('constellation',)
    search_fields = ('name',)
