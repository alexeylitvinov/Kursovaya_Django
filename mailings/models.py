from django.db import models
from pytils.translit import slugify

from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Mail(models.Model):
    subject = models.CharField(max_length=200, verbose_name='Тема')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    body = models.TextField(verbose_name='Тело')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.subject)
        super(Mail, self).save(*args, **kwargs)

    class Meta:
        db_table = 'mails'
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'

    def __str__(self):
        return f'{self.subject}, {self.user}'
