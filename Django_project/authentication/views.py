from django.shortcuts import redirect
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from authentication.forms import RegularSignUpForm, ModeratorSignUpForm

User = get_user_model()


class SingUpView(TemplateView):
    template_name = 'authentication/signup.html'


class RegularSignUpView(CreateView):
    model = User
    form_class = RegularSignUpForm
    template_name = 'authentication/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'regular'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('base.html')


class ModeratorSignUpView(CreateView):
    model = User
    form_class = ModeratorSignUpForm
    template_name = 'authentication/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'moderator'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('base.html')
