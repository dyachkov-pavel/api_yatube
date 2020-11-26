from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet
from rest_framework.authtoken import views


router_posts = DefaultRouter()
router_posts.register(r'posts', PostViewSet, basename='post-list')
router_comments = DefaultRouter()
router_comments.register(r'comments', CommentViewSet, basename='comment-list')

urlpatterns = [
    path('api/v1/', include(router_posts.urls)),
    path('api/v1/posts/<int:post_id>/', include(router_comments.urls)),
    path('api/v1/api-token-auth/', views.obtain_auth_token),
]
