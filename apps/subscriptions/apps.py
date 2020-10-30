from django.apps import AppConfig


class SubscriptionsConfig(AppConfig):
    name = "apps.subscriptions"
    verbose_name = "Подписки"

    def ready(self):
        from . import signals
