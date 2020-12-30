from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    PostModelViewSet,
    CommentModelViewSet, 
    GroupModelViewSet,
    FollowModelViewSet,
)

router = DefaultRouter()
router.register(
    r'posts/(?P<post_id>\d+)/comments', 
    CommentModelViewSet, 
    basename='comments',
 )
router.register(r'posts', PostModelViewSet, basename='posts')
router.register(r'group', GroupModelViewSet, basename='groups')
router.register(r'follow', FollowModelViewSet, basename='followers') 

urlpatterns = router.urls
urlpatterns += [
    path(
        'token/', 
        TokenObtainPairView.as_view(), 
        name='token_obtain_pair',
    ),
    path(
        'token/refresh/', 
        TokenRefreshView.as_view(), 
        name='token_refresh',
    ),
]
