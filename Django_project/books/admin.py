from django.contrib import admin
from books.models import Book, Author, Genre, Review, Comment


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'description']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['genre']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['author', 'book', 'creator', 'timestamp', 'topic', 'review']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'book', 'timestamp', 'comment', 'parent']
