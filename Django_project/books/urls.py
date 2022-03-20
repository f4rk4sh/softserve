from django.urls import path
from books.views import BookListView,  BookDetailView, BookAddView, BookUpdateView, BookDeleteView, \
    AuthorAddView, GenreAddView, ReviewDetailView, ReviewAddView, ReviewUpdateView, ReviewDeleteView, \
    CommentDetailView, CommentUpdateView, CommentDeleteView

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path(r'book/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path(r'add/book/', BookAddView.as_view(), name='book_add'),
    path(r'book/<int:pk>/edit', BookUpdateView.as_view(), name='book_update'),
    path(r'book/<int:pk>/delete', BookDeleteView.as_view(), name='book_delete'),
    path(r'add/author/', AuthorAddView.as_view(), name='author_add'),
    path(r'add/genre/', GenreAddView.as_view(), name='genre_add'),
    path(r'review/<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),
    path(r'add/review/', ReviewAddView.as_view(), name='review_add'),
    path(r'review/<int:pk>/edit', ReviewUpdateView.as_view(), name='review_update'),
    path(r'review/<int:pk>/delete', ReviewDeleteView.as_view(), name='review_delete'),
    path(r'comment/<int:pk>/', CommentDetailView.as_view(), name='comment_detail'),
    path(r'comment/<int:pk>/edit', CommentUpdateView.as_view(), name='comment_update'),
    path(r'comment/<int:pk>/delete', CommentDeleteView.as_view(), name='comment_delete'),
]
