from api.validators import year_validator
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import User

class Categories(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=200)
    genre = models.ManyToManyField(
        Genres,
        related_name='titles',
    )
    category = models.ForeignKey(
        Categories,
        related_name='titles',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    description = models.TextField(max_length=200)
    year = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[year_validator]
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    Titles = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        Genres,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    title_id = models.ForeignKey(
        Titles, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()    
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.SmallIntegerField(validators=[
            MinValueValidator(1),
            MaxValueValidator(10)])
    pub_date = models.DateTimeField(
        'Дата публикации ревью', auto_now_add=True, db_index=True
    )
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Ревью'
        verbose_name_plural = 'Ревью'

    def __str__(self):
        return self.text[:25]
    

class Comment(models.Model):
    review_id = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )    
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления комментария', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]