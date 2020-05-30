from django.db import models

from apps.clubs.models import Club
from apps.core.models import NameModel, CityModel

from . import Gender


class Coach(NameModel):
    class Meta:
        verbose_name = "Тренеры"
        verbose_name_plural = "Тренер"

    club = models.ForeignKey(
        Club, related_name="coaches", on_delete=models.CASCADE, verbose_name="Клуб"
    )
    image = models.ImageField("Фотография", upload_to="coach/", null=True, blank=True)

    def __str__(self):
        return self.full_name


class ClientProfile(models.Model):
    city = models.ForeignKey(
        CityModel, on_delete=models.SET_NULL, null=True, verbose_name="Город"
    )
    image = models.ImageField(
        "Фотография", upload_to="client_profile/", null=True, blank=True
    )
    sex = models.CharField("Пол", choices=Gender.choices, max_length=20)
    birth_date = models.DateTimeField(null=True, blank=True)
