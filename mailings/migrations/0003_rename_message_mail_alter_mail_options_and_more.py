# Generated by Django 4.2.7 on 2024-06-07 23:26

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mailings', '0002_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Message',
            new_name='Mail',
        ),
        migrations.AlterModelOptions(
            name='mail',
            options={'verbose_name': 'Письмо', 'verbose_name_plural': 'Письма'},
        ),
        migrations.AlterModelTable(
            name='mail',
            table='mails',
        ),
    ]