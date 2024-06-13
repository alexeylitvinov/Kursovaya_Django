from django.db import models
from pytils.translit import slugify

from users.models import User, Client

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


class Mailing(models.Model):
    class FrequencyChoices(models.TextChoices):
        DAILY = 'D', 'Ежедневно'
        WEEKLY = 'W', 'Еженедельно'
        MONTHLY = 'M', 'Ежемесячно'

    class StatusChoices(models.TextChoices):
        COMPLETED = 'C', 'Завершена'
        CREATED = 'CR', 'Создана'
        RUNNING = 'R', 'Запущена'

    mail = models.ForeignKey(Mail, on_delete=models.CASCADE, verbose_name='Почта')
    first_send_date = models.DateField(**NULLABLE, verbose_name='Дата первой отправки')
    send_time = models.TimeField(**NULLABLE, verbose_name='Время отправки')
    frequency = models.CharField(
        max_length=2,
        choices=FrequencyChoices.choices,
        default=FrequencyChoices.DAILY,
        verbose_name='Периодичность'
    )
    status = models.CharField(
        max_length=2,
        choices=StatusChoices.choices,
        default=StatusChoices.CREATED,
        verbose_name='Статус рассылки'
    )

    def save(self, *args, **kwargs):
        """ При сохранении новой рассылки удаляем все старые рассылки для этого же письма """
        if not self.pk:  # Проверяем, что это создание новой рассылки, а не обновление существующей
            Mailing.objects.filter(mail=self.mail).delete()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'mailing'
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            ('view_all_mailings', 'Может просматривать любые рассылки'),
            ('disable_mailings', 'Может отключать рассылки')
        ]

    def __str__(self):
        return f'Рассылка {self.get_status_display()} с {self.mail}'


class MailingAttempt(models.Model):
    class AttemptStatusChoices(models.TextChoices):
        SUCCESS = 'S', 'Успешно'
        FAILURE = 'F', 'Не успешно'

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')
    last_attempt_date = models.DateTimeField(verbose_name='Дата и время последней попытки')
    status = models.CharField(
        max_length=1,
        choices=AttemptStatusChoices.choices,
        default=AttemptStatusChoices.FAILURE,
        verbose_name='Статус попытки'
    )
    server_response = models.TextField(verbose_name='Ответ почтового сервера', **NULLABLE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, **NULLABLE, verbose_name='Клиент')

    class Meta:
        db_table = 'mailing_attempt'
        verbose_name = 'Попытка'
        verbose_name_plural = 'Попытки'

    def __str__(self):
        return f"Попытка рассылки {self.get_status_display()}"
