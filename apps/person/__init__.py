from django.db.models import TextChoices

default_app_config = 'apps.person.apps.PersonConfig'


class Gender(TextChoices):
    MALE = "MALE", "Мужской"
    FEMALE = "FEMALE", "Женский"
