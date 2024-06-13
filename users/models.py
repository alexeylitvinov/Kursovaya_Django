from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    company_name = models.CharField(max_length=100, verbose_name='Компания')
    first_name = models.CharField(max_length=50, **NULLABLE, verbose_name='Имя')
    last_name = models.CharField(max_length=50, **NULLABLE, verbose_name='Фамилия')
    token = models.CharField(max_length=100, **NULLABLE, verbose_name='Токен')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            ('view_user_list', 'Может просматривать список пользователей'),
            ('block_users', 'Может блокировать пользователей')
        ]

    def __str__(self):
        return f'{self.company_name}'


class Client(models.Model):
    email = models.EmailField(verbose_name='Почта')
    first_name = models.CharField(max_length=50, **NULLABLE, verbose_name='Имя')
    last_name = models.CharField(max_length=50, **NULLABLE, verbose_name='Фамилия')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        unique_together = ('user', 'email',)
        db_table = 'contacts'
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return f'{self.first_name}, {self.last_name}, {self.email}'
