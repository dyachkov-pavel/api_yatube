from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwner


class PostViewSet(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def list(self, request):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def update(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, obj=post)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data)

    def partial_update(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, obj=post)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data)

    def destroy(self, request, pk=None):       
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, obj=post)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated, IsOwner]

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

    def retrieve(self, request, pk=None, *args, **kwargs):
        post_id = self.kwargs['post_id']
        comment = get_object_or_404(Comment, pk=pk, post__id=post_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        post_id = self.kwargs['post_id']
        comment = get_object_or_404(Comment, pk=pk, post__id=post_id)
        self.check_object_permissions(request, obj=comment)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data)

    def partial_update(self, request, pk=None, *args, **kwargs):
        post_id = self.kwargs['post_id']
        comment = get_object_or_404(Comment, pk=pk, post__id=post_id)
        self.check_object_permissions(request, obj=comment)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        post_id = self.kwargs['post_id']
        comment = get_object_or_404(Comment, pk=pk, post__id=post_id)
        self.check_object_permissions(request, obj=comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
