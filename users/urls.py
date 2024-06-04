from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.services import password_reset, email_verification
from users.views import UserCreateView, UserLoginView, UserListView, ClientListView, \
    ClientDetailView, ClientCreateView

app_name = UsersConfig.name

urlpatterns = [
    path('users/', UserListView.as_view(), name='users'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    path('login/password_reset/', password_reset, name='password_reset'),
    path('clients/', ClientListView.as_view(), name='clients'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('create/', ClientCreateView.as_view(), name='client_create')
]
