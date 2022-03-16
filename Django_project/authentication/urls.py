from django.urls import path, include
from authentication.views import SignUpView


urlpatterns = [
    path('', include('django.contrib.auth.urls'), name='login'),
    path('signup/', SignUpView.as_view(), name='signup')
]
