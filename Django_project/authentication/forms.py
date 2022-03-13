from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from authentication.models import Regular, Moderator
from django.contrib.auth import get_user_model

User = get_user_model()


class RegularSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_regular = True
        user.save()
        regular = Regular.objects.create(user=user)
        return user


class ModeratorSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_moderator = True
        user.save()
        moderator = Moderator.objects.create(user=user)
        return user
