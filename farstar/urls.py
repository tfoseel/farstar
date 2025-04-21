from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/constellations/', include('constellations.urls')),
    path('api/stars/', include('stars.urls')),
    path('api/posts/', include('posts.urls')),
    path('api/lumen/', include('lumen.urls')),
    path('api/payments/', include('payments.urls')),
]
