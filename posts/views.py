from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwner


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def list(self, request, *args, **kwargs):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        queryset = post.comments.all()
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
