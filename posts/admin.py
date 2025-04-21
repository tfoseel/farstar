from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'star', 'created_at')
    list_filter = ('star', 'author')
    search_fields = ('content',)
