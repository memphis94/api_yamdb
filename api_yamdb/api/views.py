from django.db.models import Avg
from rest_framework import  viewsets
from django_filters import rest_framework as filters
from .filters import TitlesFilter
from .mixins import GetCreateDeleteViewSet
from rest_framework.filters import SearchFilter


from reviews.models import Categories, Genres, Titles

from .permission import (GenresTitlesPermission)
from .serializers import (CategoriesSerializer,
                          GenresSerializer, TitleSerializer,
                          TitleCreateSerializer)

class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.annotate(
        rating=Avg('reviews__score')
    )
    serializer_class = TitleSerializer
    permission_classes = (GenresTitlesPermission)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleCreateSerializer
        return TitleSerializer


class CategoriesViewSet(GetCreateDeleteViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (GenresTitlesPermission)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenresViewSet(GetCreateDeleteViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (GenresTitlesPermission)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
