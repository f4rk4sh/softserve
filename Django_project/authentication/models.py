from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField('username', max_length=100, unique=True)
    email = models.EmailField('email address', unique=True)
    is_regular = models.BooleanField('regular status', default=False)
    is_moderator = models.BooleanField('moderator status', default=False)


class Regular(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class Moderator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

