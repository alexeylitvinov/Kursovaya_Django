from django.contrib import admin

from blogs.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """
    Отображение таблицы клиентов в админ панели
    """
    list_display = ('title', 'publication_date', 'views', 'author')
    prepopulated_fields = {'slug': ('title',)}
