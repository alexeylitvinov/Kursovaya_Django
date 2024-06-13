from django.core.management import BaseCommand

from mailings.services import schedule_mailing_tasks


class Command(BaseCommand):
    """Кастомная команда запуска периодической рассылки писем"""
    def handle(self, *args, **options):
        schedule_mailing_tasks()
