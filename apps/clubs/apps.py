from django.apps import AppConfig


class ClubsConfig(AppConfig):
    verbose_name = "Клубы"
    name = 'apps.clubs'

    def ready(self):
        import apps.clubs.signals