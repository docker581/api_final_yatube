from rest_framework import status, filters
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly, 
)
from rest_framework.viewsets import ModelViewSet, ViewSet, GenericViewSet
from rest_framework.decorators import permission_classes
from rest_framework.mixins import CreateModelMixin, ListModelMixin

from .serializers import (
    PostSerializer, 
    CommentSerializer, 
    GroupSerializer, 
    FollowSerializer,
)
from .models import User, Post, Comment, Group, Follow
from .permissions import IsOwnerOrReadOnly


@permission_classes([IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly])
class PostModelViewSet(ModelViewSet):
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
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        queryset = Comment.objects.filter(post=post_id)
        return queryset   

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs.get('post_id'))
        serializer.save(post=post, author=self.request.user)


@permission_classes([IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly])
class GroupViewset(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


@permission_classes([IsAuthenticated, IsOwnerOrReadOnly])
class FollowViewset(CreateModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = FollowSerializer
    # DEFAULT_FILTER_BACKENDS подключен на уровне всего проекта

    def get_queryset(self):
        queryset = self.request.user.following.all()
        username = self.request.query_params.get('search', None)
        if username is not None:
            user_id = User.objects.get(username=username).id
            queryset = queryset.filter(user=user_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)               
