from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


class PostViewSet(viewsets.ViewSet):

    def list(self, request):
        if request.auth is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        if request.auth is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        if request.auth is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def update(self, request, pk=None):
        if request.auth is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data)

    def partial_update(self, request, pk=None):
        if request.auth is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data)

    def destroy(self, request, pk=None):
        if request.auth is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)        
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        if request.auth is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        queryset = post.comments.all()
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if request.auth is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, *args, **kwargs):
        if request.auth is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        post_id = self.kwargs['post_id']
        comment = get_object_or_404(Comment, pk=pk, post__id=post_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        if request.auth is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        post_id = self.kwargs['post_id']
        comment = get_object_or_404(Comment, pk=pk, post__id=post_id)
        if comment.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data)

    def partial_update(self, request, pk=None, *args, **kwargs):
        if request.auth is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        post_id = self.kwargs['post_id']
        comment = get_object_or_404(Comment, pk=pk, post__id=post_id)
        if comment.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(
            comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        if request.auth is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        post_id = self.kwargs['post_id']
        comment = get_object_or_404(Comment, pk=pk, post__id=post_id)
        if comment.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
