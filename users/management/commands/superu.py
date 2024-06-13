import os

from django.core.management import BaseCommand
from dotenv import load_dotenv

from users.models import User

load_dotenv()


class Command(BaseCommand):
    """Кастомная команда создания суперпользователя"""

    def handle(self, *args, **options):
        user = User.objects.create(email=os.getenv('S_EMAIL'))
        user.set_password(os.getenv('S_PASSWORD'))
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
