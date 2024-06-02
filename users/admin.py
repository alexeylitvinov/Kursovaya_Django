from django.contrib import admin

from users.models import User, Client


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Отображение таблицы Category в админ панели
    """
    list_display = ('id', 'email')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """
    Отображение таблицы Category в админ панели
    """
    list_display = ('email', 'first_name', 'last_name', 'user')
