from api.validators import year_validator
from django.db import models


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
