# your_app/apps.py

from django.apps import AppConfig

class YourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mentors'

    def ready(self):
        import mentors.signals  # noqa
