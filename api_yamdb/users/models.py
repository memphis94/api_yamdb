from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = (
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    )
    role = models.CharField(
        max_length=20,
        choices=ROLES,
        default=USER)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
