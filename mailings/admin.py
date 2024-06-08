from django.contrib import admin

from mailings.models import Mail


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    """
    Отображение таблицы пользователей в админ панели
    """
    list_display = ('subject', 'user')
    prepopulated_fields = {'slug': ('subject',)}
