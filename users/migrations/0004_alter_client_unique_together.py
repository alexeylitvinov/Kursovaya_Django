# Generated by Django 4.2.7 on 2024-06-04 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_client_email'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='client',
            unique_together={('user', 'email')},
        ),
    ]