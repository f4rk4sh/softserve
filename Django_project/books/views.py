from books.models import Book, Author, Genre, Review, Comment
from books.forms import BookForm, AuthorForm, GenreForm, ReviewForm, CommentForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

User = get_user_model()


class SearchMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(title__icontains=self.request.GET.get('q', ''))


class BookListView(SearchMixin, ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'books/book_list.html'
    paginate_by = 10


class BookDetailView(FormMixin, DetailView):
    model = Book
    form_class = CommentForm
    context_object_name = 'book'
    template_name = 'books/book_detail.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        parent = None
        try:
            parent_id = int(self.request.POST.get('parent_id'))
        except:
            parent_id = None
        if parent_id:
            parent = Comment.objects.get(id=parent_id)
            if parent:
                reply_comment = form.save(commit=False)
                reply_comment.author = User.objects.get(id=self.request.user.pk)
                reply_comment.parent = parent
                reply_comment.book = self.get_object()
                reply_comment.save()
        new_comment = form.save(commit=False)
        new_comment.author = User.objects.get(id=self.request.user.pk)
        new_comment.book = self.get_object()
        new_comment.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = self.get_object()
        context['reviews'] = Review.objects.filter(book=self.object.id)
        context['comments'] = Comment.objects.filter(book=self.object.id, parent__isnull=True)
        return context

    def get_success_url(self):
        return reverse_lazy('books:book_detail', kwargs={'pk': self.object.pk})


class BookAddView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_add.html'

    def get_success_url(self):
        return reverse_lazy('books:book_detail', kwargs={'pk': self.object.pk})


class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_update.html'

    def get_success_url(self):
        return reverse_lazy('books:book_detail', kwargs={'pk': self.object.pk})


class BookDeleteView(DeleteView):
    model = Book
    template_name = 'books/delete.html'
    success_url = reverse_lazy('books:book_list')


class AuthorAddView(CreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'books/author_add.html'


class GenreAddView(CreateView):
    model = Genre
    form_class = GenreForm
    template_name = 'books/genre_add.html'


class ReviewDetailView(DetailView):
    model = Review
    context_object_name = 'review'
    template_name = 'books/review_detail.html'


class ReviewAddView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'books/review_add.html'

    def form_valid(self, form):
        review = form.save(commit=False)
        review.author = User.objects.get(id=self.request.user.pk)
        review.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('books:review_detail', kwargs={'pk': self.object.pk})


class ReviewUpdateView(UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'books/review_update.html'

    def get_success_url(self):
        return reverse_lazy('books:review_detail', kwargs={'pk': self.object.book.pk})


class ReviewDeleteView(DeleteView):
    model = Review
    template_name = 'books/delete.html'

    def get_success_url(self):
        return reverse_lazy('books:book_detail', kwargs={'pk': self.object.book.pk})


class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'books/comment_update.html'

    def get_success_url(self):
        return reverse_lazy('books:comment_detail', kwargs={'pk': self.object.book.pk})


class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'books/delete.html'

    def get_success_url(self):
        return reverse_lazy('books:book_detail', kwargs={'pk': self.object.book.pk})
