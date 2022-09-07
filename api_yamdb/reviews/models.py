from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator



class Review(models.Model):
    title_id = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
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
        ordering = ['-pub_date']
        verbose_name = 'Ревью'
        verbose_name_plural = 'Ревью'

    def __str__(self):
        return self.text[:25]
    


class Comment(models.Model):
    review_id = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField() 
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления комментария', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]