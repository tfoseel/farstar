from django.urls import path
from .views import StarPostListView

urlpatterns = [
    path('<int:pk>/posts/', StarPostListView.as_view(), name='star_posts'),
]
