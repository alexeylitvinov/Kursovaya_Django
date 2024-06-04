import random
import secrets
import string

from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView
from users.services import send_confirmation_email

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserAuthenticationForm, ClientForm
from users.models import User, Client


class UserCreateView(CreateView):
    """
    Регистрация нового пользователя
    """
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        """
        Подтверждение регистрации с отсылкой письма на email пользователя
        """
        user = form.save()
        send_confirmation_email(self.request, user, EMAIL_HOST_USER)
        return super().form_valid(form)

    # def form_valid(self, form):
    #     """
    #     Подтверждение регистрации с отсылкой письма на email пользователя
    #     """
    #     user = form.save()
    #     user.is_active = False
    #     token = secrets.token_hex(16)
    #     user.token = token
    #     user.save()
    #     host = self.request.get_host()
    #     url = f'http://{host}/users/email-confirm/{token}/'
    #     send_mail(
    #         subject='Подтверждение почты',
    #         message=f'Перейдите по ссылке чтобы закончить процесс регистрации {url}',
    #         from_email=EMAIL_HOST_USER,
    #         recipient_list=[user.email]
    #     )
    #     return super().form_valid(form)


# def email_verification(request, token):
#     user = get_object_or_404(User, token=token)
#     user.is_active = True
#     user.save()
#     return redirect(reverse('users:login'))


class UserLoginView(LoginView):
    """
    Авторизация пользователя
    """
    model = User
    form_class = UserAuthenticationForm
    success_url = reverse_lazy('users:login')
    template_name = "users/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context


# def password_reset(request):
#     """
#     Установка рандомного пароля пользователя
#     """
#     if request.method == 'POST':
#         email = request.POST['email']
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return render(
#                 request, 'users/password_reset.html', {
#                     'error': 'Пользователь с таким адресом электронной почты не найден', 'title': 'Ошибка'
#                 }
#             )
#         new_password = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=8))
#         user.set_password(new_password)
#         user.save()
#         send_mail(
#             'Ваш новый пароль',
#             'Ваш новый пароль: {}'.format(new_password),
#             from_email=EMAIL_HOST_USER,
#             recipient_list=[user.email],
#             fail_silently=False,
#         )
#         return render(request, 'users/password_reset_done.html', {'title': 'Подтверждение'})
#     return render(request, 'users/password_reset.html', {'title': 'Сброс пароля'})


class UserListView(ListView):
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Пользователи'
        context['user_count'] = User.objects.count() - 1
        return context

    def get_queryset(self):
        return User.objects.filter(is_superuser=False)


class ClientListView(ListView):
    model = Client

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Client.objects.filter(user=self.request.user)
        else:
            return Client.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Клиенты'
        context['client_count'] = self.get_queryset().count()
        return context


class ClientDetailView(DetailView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Клиент'
        return context


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('users:clients')

    def form_valid(self, form):
        client = form.save(commit=False)
        client.user = self.request.user
        try:
            client.save()
        except IntegrityError:
            messages.error(self.request, 'Клиент с таким email уже существует.')
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить клиента'
        return context
