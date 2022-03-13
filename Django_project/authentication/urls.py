from django.urls import path, include
from authentication.views import SingUpView, RegularSignUpView, ModeratorSignUpView


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', SingUpView.as_view(), name='signup'),
    path('signup/regular/', RegularSignUpView.as_view(), name='signup_regular'),
    path('signup/moderator/', ModeratorSignUpView.as_view(), name='signup_moderator')
]
