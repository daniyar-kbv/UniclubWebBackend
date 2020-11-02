from django.db.models import TextChoices

default_app_config = 'apps.clubs.apps.ClubsConfig'


class ClientType(TextChoices):
    UNICLASS = "UNICLASS", "UniClass"
    UNIPASS = "UNIPASS", "UniPass"
    ALL = "ALL", "Все"
