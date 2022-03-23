from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from authentication.forms import SignUpForm
from django.contrib.auth.models import Group

User = get_user_model()


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'authentication/signup_form.html'
    success_url = reverse_lazy('books:book_list')

    def form_valid(self, form):
        user = form.save()
        user.groups.add(Group.objects.get(name='regulars'))
        login(self.request, user)
        return HttpResponseRedirect(self.success_url)
