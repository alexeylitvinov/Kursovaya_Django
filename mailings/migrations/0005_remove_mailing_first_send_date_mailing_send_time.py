# Generated by Django 4.2.7 on 2024-06-08 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailings', '0004_mailing_mailingattempt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailing',
            name='first_send_date',
        ),
        migrations.AddField(
            model_name='mailing',
            name='send_time',
            field=models.TimeField(blank=True, null=True, verbose_name='Время отправки'),
        ),
    ]
