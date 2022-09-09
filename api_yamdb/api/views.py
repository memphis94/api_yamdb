from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import  viewsets
from django_filters import rest_framework as filters
from .filters import TitlesFilter
from .mixins import GetCreateDeleteViewSet
from rest_framework.filters import SearchFilter


from reviews.models import Categories,Comment, Genres, Review, Titles
from .permission import (GenresTitlesPermission, ReviewCommentPermission)
from .serializers import (CategoriesSerializer, CommentSerializer,
                          GenresSerializer, ReviewSerializer,
                          TitleSerializer, TitleCreateSerializer)

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

class CommentViewSet(viewsets.ModelViewSet):    
    serializer_class = CommentSerializer
    permission_classes = (ReviewCommentPermission, )

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(review=review, author=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):    
    serializer_class = ReviewSerializer
    permission_classes = (ReviewCommentPermission,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        if self.request.user.reviews.filter(title=title_id).exists():
            raise ValidationError("Можно добавить только один отзыв")

        title = get_object_or_404(Titles, pk=title_id)
        serializer.save(author=self.request.user, title=title)
