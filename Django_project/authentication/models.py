from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    REGULAR = 1
    MODERATOR = 2
    ADMIN = 3

    ROLE_CHOICES = (
        (REGULAR, 'Regular'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
    )
    username = models.CharField('username', max_length=100, unique=True)
    email = models.EmailField('email address', unique=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=1)


