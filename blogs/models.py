from django.db import models

from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, **NULLABLE, verbose_name='URL')
    content = models.TextField(verbose_name='Статья')
    image = models.ImageField(upload_to='blogs_images', **NULLABLE, verbose_name='Изображение')
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    publication_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')

    class Meta:
        db_table = 'blogs'
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'

    def __str__(self):
        return f'{self.title}, {self.publication_date}, {self.views}, {self.author}'
