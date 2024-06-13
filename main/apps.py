from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        """Настройки конфигурации для периодического запуска задачи"""
        from mailings.services import schedule_mailing_tasks
        schedule_mailing_tasks()
