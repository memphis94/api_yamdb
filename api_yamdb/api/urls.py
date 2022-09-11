from rest_framework.routers import DefaultRouter
from django.urls import include, path

from users.views import UserViewSet
from .views import (CategoriesViewSet, CommentViewSet, GenresViewSet, ReviewViewSet, TitlesViewSet)

router_v1 = DefaultRouter()
router_v1.register('titles', TitlesViewSet, basename='title')
router_v1.register('categories', CategoriesViewSet, basename='category')
router_v1.register('genres', GenresViewSet, basename='genre')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment',
)
router_v1.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include('users.urls')),
]