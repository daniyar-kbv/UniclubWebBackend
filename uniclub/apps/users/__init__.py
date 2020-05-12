from django.db.models import TextChoices

default_app_config = 'apps.users.apps.UsersConfig'


class UserTypes(TextChoices):
    CLIENT = "CLIENT", "Клиент"
    PARTNER = "PARTNER", "Партнер"
