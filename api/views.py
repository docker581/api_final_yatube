from rest_framework import status, filters
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly, 
)
from rest_framework.viewsets import ModelViewSet, ViewSet, GenericViewSet
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
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
        return Comment.objects.filter(post=post_id)   

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs.get('post_id'))
        serializer.save(post=post, author=self.request.user)


@permission_classes([IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly])
class GroupViewset(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


@permission_classes([IsAuthenticated, IsOwnerOrReadOnly])
class FollowViewset(CreateModelMixin, ListModelMixin, GenericViewSet):
    def list(self, request):       
        follow = self.request.user.following.all()
        username = self.request.query_params.get('search', None)
        if username is not None:
            user_id = User.objects.get(username=username).id
            follow = follow.filter(user=user_id)
        serializer = FollowSerializer(follow, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = FollowSerializer(
            data=request.data, 
            context={'request': self.request},
        )
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)               
