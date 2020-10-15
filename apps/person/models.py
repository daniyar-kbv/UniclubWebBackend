from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

from apps.clubs.models import Club
from apps.core.models import NameModel, CityModel
from apps.grades.models import Course

from . import Gender

User = get_user_model()


class AdditionalInformationMixin(models.Model):
    sex = models.CharField("Пол", choices=Gender.choices, max_length=20)
    birth_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class Coach(NameModel):
    class Meta:
        verbose_name = "Тренеры"
        verbose_name_plural = "Тренер"

    club = models.ForeignKey(
        Club, related_name="coaches", on_delete=models.CASCADE, verbose_name="Клуб"
    )
    course = models.ForeignKey(
        Course, related_name="coaches", on_delete=models.CASCADE, verbose_name="Курс"
    )
    image = models.ImageField("Фотография", upload_to="coach/", null=True, blank=True)

    def __str__(self):
        return self.full_name


class ClientProfile(AdditionalInformationMixin):
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профиль"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Пользователь"
    )
    city = models.ForeignKey(
        CityModel, on_delete=models.SET_NULL, null=True, verbose_name="Город"
    )
    image = models.ImageField(
        "Фотография", upload_to="client_profile/", null=True, blank=True
    )

    def __str__(self):
        return f'({self.id}) {self.user.full_name}'


class ClientChildren(NameModel, AdditionalInformationMixin):
    class Meta:
        verbose_name = "Ребенок"
        verbose_name_plural = "Ребенок"

    parent = models.ForeignKey(
        ClientProfile,
        verbose_name="Родитель",
        related_name="children",
        on_delete=models.PROTECT,
    )
    image = models.ImageField(
        "Фотография", upload_to="children/", null=True, blank=True
    )
    mobile_phone = PhoneNumberField("Мобильный телефон")
    email = models.EmailField("Почта", null=True, blank=True)
    city = models.ForeignKey(
        CityModel, on_delete=models.SET_NULL, null=True, verbose_name="Город"
    )

    def __str__(self):
        return self.full_name
