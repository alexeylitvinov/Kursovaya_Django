import random
import secrets
import string

from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserAuthenticationForm
from users.models import User


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
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Перейдите по ссылке чтобы закончить процесс регистрации {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


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


def password_reset(request):
    """
    Установка рандомного пароля пользователя
    """
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(
                request, 'users/password_reset.html', {
                    'error': 'Пользователь с таким адресом электронной почты не найден', 'title': 'Ошибка'
                }
            )
        new_password = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=8))
        user.set_password(new_password)
        user.save()
        send_mail(
            'Ваш новый пароль',
            'Ваш новый пароль: {}'.format(new_password),
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return render(request, 'users/password_reset_done.html', {'title': 'Подтверждение'})
    return render(request, 'users/password_reset.html', {'title': 'Сброс пароля'})
