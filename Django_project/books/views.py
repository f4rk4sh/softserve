from django.shortcuts import render
from books.models import Book, Author, Genre
from books.forms import BookAddForm, BookUpdateForm, AuthorAddForm, AuthorUpdateForm, GenreAddForm, GenreUpdateForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView


class BookListView(ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'books/book_list.html'


class BookDetailView(DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'books/book_detail.html'


class BookAddView(CreateView):
    model = Book
    form_class = BookAddForm
    template_name = 'books/book_add.html'


class BookUpdateView(UpdateView):
    model = Book
    form_class = BookUpdateForm
    template_name = 'books/book_update.html'


class AuthorAddView(CreateView):
    model = Author
    form_class = AuthorAddForm
    template_name = 'books/author_add.html'


class AuthorUpdateView(UpdateView):
    model = Author
    form_class = AuthorUpdateForm
    template_name = 'books/author_update.html'


class GenreAddView(CreateView):
    model = Genre
    form_class = GenreAddForm
    template_name = 'books/genre_add.html'


class GenreUpdateView(UpdateView):
    model = Genre
    form_class = GenreUpdateForm
    template_name = 'books/genre_update.html'


