from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Отображение таблицы Category в админ панели
    """
    list_display = ('id', 'email')
