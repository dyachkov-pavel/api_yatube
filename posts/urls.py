from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet
from rest_framework.authtoken import views


router_posts_v1 = DefaultRouter()
router_posts_v1.register('posts', PostViewSet, basename='post-list')
router_posts_v1.register(r'posts/(?P<post_id>.+)/comments', CommentViewSet, basename='comment-list')

urlpatterns = [
    path('v1/', include(router_posts_v1.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
]
