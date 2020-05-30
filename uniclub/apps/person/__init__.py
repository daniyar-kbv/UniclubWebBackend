from django.db.models import TextChoices


class Gender(TextChoices):
    MALE = "MALE", "Мужской"
    FEMALE = "FEMALE", "Женский"
