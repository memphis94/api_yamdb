from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import  viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TitleFilter
from .mixins import GetCreateDeleteViewSet
from rest_framework.filters import SearchFilter
from django.core.exceptions import ValidationError


from reviews.models import Category, Genre, Review, Title
from .permission import (GenreTitlePermission, ReviewCommentPermission)
from .serializers import (CategorySerializer, CommentSerializer, GenreSerializer,
                        ReviewSerializer,TitleSerializer, TitleCreateSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    )
    serializer_class = TitleSerializer
    permission_classes = (GenreTitlePermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleCreateSerializer
        return TitleSerializer


class GenreViewSet(GetCreateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (GenreTitlePermission,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(GetCreateDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (GenreTitlePermission,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CommentViewSet(viewsets.ModelViewSet):    
    serializer_class = CommentSerializer
    permission_classes = (ReviewCommentPermission,)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):    
    serializer_class = ReviewSerializer
    permission_classes = (ReviewCommentPermission,)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        if self.request.user.reviews.filter(title=title_id).exists():
            raise ValidationError("Можно добавить только один отзыв") 
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)
