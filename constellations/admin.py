from django.contrib import admin
from .models import Constellation


@admin.register(Constellation)
class ConstellationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
