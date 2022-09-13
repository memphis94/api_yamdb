from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api.validators import year_validator
from users.models import User


class Category(models.Model):
    name = models.CharField('Категория', max_length=256, unique=True)
    slug = models.SlugField('Адрес категории', unique=True, max_length=50)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=256, unique=True)
    slug = models.SlugField('Адрес жанра', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Произведение', max_length=200, db_index=True)
    genre = models.ManyToManyField(
        Genre, verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        verbose_name='Категория',
        on_delete=models.PROTECT
    )

    description = models.TextField('Описание')
    year = models.PositiveSmallIntegerField(
        db_index=True,
        blank=True,
        null=True,
        validators=[year_validator]
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='genres',
        verbose_name='произведение'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='жанр'
    )

    class Meta:
        verbose_name = 'жанр произведения'
        verbose_name_plural = 'жанры произведений'
        ordering = ('genre',)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.SmallIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(10)
    ])
    pub_date = models.DateTimeField(
        'Дата публикации ревью', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Ревью'
        verbose_name_plural = 'Ревью'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_review'
            ),
        ]

    def __str__(self):
        return self.text[:25]


class Comment(models.Model):
    review = models.ForeignKey(
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
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]
