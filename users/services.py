import random
import secrets
import string

from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from config.settings import EMAIL_HOST_USER
from users.models import User


def password_reset(request):
    """Функция для установки рандомного пароля для пользователя"""
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


def email_verification(request, token):
    """Верификация пользователя по почте"""
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


def send_confirmation_email(request, user, email_host_user):
    """Отправка письма с подтверждением на email пользователя"""
    user.is_active = False
    token = secrets.token_hex(16)
    user.token = token
    user.save()
    host = request.get_host()
    url = f'http://{host}/users/email-confirm/{token}/'
    send_mail(
        subject='Подтверждение почты',
        message=f'Перейдите по ссылке чтобы закончить процесс регистрации {url}',
        from_email=email_host_user,
        recipient_list=[user.email]
    )
