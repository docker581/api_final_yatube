from rest_framework import status, filters
from rest_framework.permissions import (
    BasePermission, 
    IsAuthenticated,
    IsAuthenticatedOrReadOnly, 
    SAFE_METHODS,
)
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from .serializers import (
    PostSerializer, 
    CommentSerializer, 
    GroupSerializer, 
    FollowSerializer,
)
from .models import User, Post, Comment, Group, Follow


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


@permission_classes([IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly])
class PostModelViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):  
        queryset = Post.objects.all()
        group = self.request.query_params.get('group', None)
        if group is not None:
            queryset = queryset.filter(group=group)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@permission_classes([IsAuthenticated, IsOwnerOrReadOnly])
class CommentModelViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        queryset = Comment.objects.filter(post=post_id)
        return queryset    

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs.get('post_id'))
        serializer.save(post=post, author=self.request.user)


@permission_classes([IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly])
class GroupModelViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    http_method_names = ['get', 'post']

    def perform_create(self, serializer):
        serializer.save()


@permission_classes([IsAuthenticated, IsOwnerOrReadOnly])
class FollowModelViewSet(ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    http_method_names = ['get', 'post']

    def get_queryset(self):
        queryset = self.request.user.following.all()
        username = self.request.query_params.get('search', None)
        if username is not None:
            user_id = User.objects.get(username=username).id
            queryset = queryset.filter(user=user_id)
        return queryset 

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)            
