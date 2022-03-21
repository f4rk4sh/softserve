from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Author(models.Model):
    name = models.CharField('name', max_length=255)

    def __str__(self):
        return self.name


class Genre(models.Model):
    genre = models.CharField('genre', max_length=80)

    def __str__(self):
        return self.genre


class Book(models.Model):
    title = models.CharField('title', max_length=255, unique=True)
    cover = models.ImageField('cover', upload_to='covers')
    author = models.ManyToManyField(Author, related_name='books')
    date = models.DateField('publication date', null=True)
    genre = models.ManyToManyField(Genre, related_name='books')
    description = models.TextField('description')
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')

    def get_likes(self):
        return self.likes.user.count()

    def __str__(self):
        return self.title


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    creator = models.CharField('author', max_length=100, blank=True)
    topic = models.CharField('topic', max_length=100, blank=True)
    review = models.TextField('review')
    timestamp = models.DateTimeField('timestamp', auto_now=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return self.topic


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField('comment', max_length=255)
    timestamp = models.DateTimeField('timestamp', auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.comment[:30]
