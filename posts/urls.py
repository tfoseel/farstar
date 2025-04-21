from django.urls import path
from .views import (
    PostCreateView,
    PostListView,
    PostDeleteView,
    CheckVisibilityView,
)

urlpatterns = [
    path('', PostCreateView.as_view(), name='create_post'),
    path('list/', PostListView.as_view(), name='list_posts'),
    path('<int:pk>/check-visibility/',
         CheckVisibilityView.as_view(), name='check_visibility'),
    path('<int:pk>/', PostDeleteView.as_view(), name='delete_post'),
]
