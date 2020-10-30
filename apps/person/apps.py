from django.apps import AppConfig


class PersonConfig(AppConfig):
    name = 'apps.person'

    def ready(self):
        from . import signals
