from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateView, UserLoginView, email_verification, password_reset

app_name = UsersConfig.name

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    path('login/password_reset/', password_reset, name='password_reset')
]
