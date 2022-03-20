from django.forms import ModelForm
from books.models import Book, Author, Genre, Review, Comment


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = '__all__'


class GenreForm(ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        exclude = ['author']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ['author', 'book', 'parent']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CommentForm, self).__init__(*args, **kwargs)
