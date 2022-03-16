from django.urls import path
from books.views import BookListView, BookDetailView, BookAddView, BookUpdateView, AuthorAddView, AuthorUpdateView, \
    GenreAddView, GenreUpdateView

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path(r'<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('add_book/', BookAddView.as_view(), name='book_add'),
    path(r'update_book/<int:pk>/', BookUpdateView.as_view(), name='book_update'),
    path('add_author/', AuthorAddView.as_view(), name='author_add'),
    path(r'update_author/<int:pk>/', AuthorUpdateView.as_view(), name='author_update'),
    path('add_genre/', GenreAddView.as_view(), name='genre_add'),
    path(r'update_genre/<int:pk>/', GenreUpdateView.as_view(), name='genre_update')
]
