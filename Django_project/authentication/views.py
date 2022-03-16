from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from authentication.forms import SignUpForm


User = get_user_model()


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'authentication/signup_form.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('base.html')
