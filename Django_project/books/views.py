from django.db.models import Q, Count
from django.http import HttpResponseRedirect
from books.models import Book, Author, Genre, Review, Comment
from books.forms import BookForm, AuthorForm, GenreForm, ReviewForm, CommentForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

User = get_user_model()


class SearchMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            Q(title__icontains=self.request.GET.get('q', '')) |
            Q(author__name__icontains=self.request.GET.get('q', ''))
        ).annotate(like_count=Count('likes')).order_by('-like_count')


class BookListView(SearchMixin, ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'books/book_list.html'
    paginate_by = 8


class BookDetailView(LoginRequiredMixin, PermissionRequiredMixin, FormMixin, DetailView):
    permission_required = 'books.view_book'
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


class BookAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'books.add_book'
    model = Book
    form_class = BookForm
    template_name = 'books/book_add.html'

    def get_success_url(self):
        return reverse_lazy('books:book_detail', kwargs={'pk': self.object.pk})


class BookUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'books.change_book'
    model = Book
    form_class = BookForm
    template_name = 'books/book_update.html'

    def get_success_url(self):
        return reverse_lazy('books:book_detail', kwargs={'pk': self.object.pk})


class BookDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'books.delete_book'
    model = Book
    template_name = 'books/delete.html'
    success_url = reverse_lazy('books:book_list')


class AuthorAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'books.add_author'
    permission_denied_message = 'only moderators'
    model = Author
    form_class = AuthorForm
    template_name = 'books/author_add.html'


class GenreAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'books.add_genre'
    model = Genre
    form_class = GenreForm
    template_name = 'books/genre_add.html'


class ReviewDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'books.view_review'
    model = Review
    context_object_name = 'review'
    template_name = 'books/review_detail.html'


class ReviewAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'books.add_review'
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


class ReviewUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'books.change_review'
    model = Review
    form_class = ReviewForm
    template_name = 'books/review_update.html'

    def get_success_url(self):
        return reverse_lazy('books:review_detail', kwargs={'pk': self.object.book.pk})


class ReviewDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'books.delete_review'
    model = Review
    template_name = 'books/delete.html'

    def get_success_url(self):
        return reverse_lazy('books:book_detail', kwargs={'pk': self.object.book.pk})


class CommentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'books.change_comment'
    model = Comment
    form_class = CommentForm
    template_name = 'books/comment_update.html'

    def get_success_url(self):
        return reverse_lazy('books:book_detail', kwargs={'pk': self.object.book.pk})


class CommentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'books.delete_comment'
    model = Comment
    template_name = 'books/delete.html'

    def get_success_url(self):
        return reverse_lazy('books:book_detail', kwargs={'pk': self.object.book.pk})


class BookAddLike(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'books.add_like'

    def post(self, request, pk, *args, **kwargs):
        book = Book.objects.get(pk=pk)
        is_dislike = False
        for dislike in book.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        if is_dislike:
            book.dislikes.remove(request.user)
        is_like = False
        for like in book.likes.all():
            if like == request.user:
                is_like = True
                break
        if not is_like:
            book.likes.add(request.user)
        if is_like:
            book.likes.remove(request.user)
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
