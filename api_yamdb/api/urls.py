from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import (CategoriesViewSet, GenresViewSet, TitlesViewSet)

router_v1 = DefaultRouter()
router_v1.register('titles', TitlesViewSet, basename='title')
router_v1.register('categories', CategoriesViewSet, basename='category')
router_v1.register('genres', GenresViewSet, basename='genre')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]