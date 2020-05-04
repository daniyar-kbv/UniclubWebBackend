from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Address(models.Model):
    name = models.CharField("Адрес", max_length=256, null=True, blank=True)
    longitude = models.CharField("Долгота", max_length=26)
    latitude = models.CharField("Широта", max_length=26)

    class Meta:
        abstract = True


class SocialNetwork(models.Model):
    instagram = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    vk = models.URLField(null=True, blank=True)

    class Meta:
        abstract = True


class ContactInfo(Address, SocialNetwork):
    mobile_phone = PhoneNumberField("Мобильный телефон")
    home_phone = PhoneNumberField("Домашний телефон", blank=True, null=True)
    work_phone = PhoneNumberField("Рабочий телефон", blank=True, null=True)
    email = models.EmailField("Почта", null=True, blank=True)
    website = models.URLField("Сайт", null=True, blank=True)

    class Meta:
        abstract = True


class AdditionalInformation(models.Model):
    competition_frequency = models.CharField(
        "Периодичность внутриклубных соревновании",
        max_length=256,
        blank=True,
        null=True
    )
    parking_available = models.CharField(
        "Парковка", max_length=256, blank=True, null=True
    )
    hazard_information = models.CharField(
        "Информация о травмоопасности", max_length=256, blank=True, null=True
    )
    places_for_parents = models.CharField(
        "Места для родителей", max_length=256, blank=True, null=True
    )
    parent_presence = models.CharField(
        "Посещение родителей", max_length=256, blank=True, null=True
    )
    video_monitoring = models.CharField(
        "Возможность видеонаблюдения", max_length=256, blank=True, null=True
    )
    floor_area = models.CharField(
        "Общая площадь", max_length=256, blank=True, null=True
    )
    number_of_bathrooms = models.CharField(
        "Количество санузлов", max_length=256, blank=True, null=True
    )

    class Meta:
        abstract = True


class Club(ContactInfo, AdditionalInformation):
    name = models.CharField(
        "Название", max_length=52, null=True, blank=True, db_index=True
    )
    image = models.ImageField(
        "Основная фотография клуба"
    )
    full_name = models.CharField(
        "Краткое описание", max_length=256, null=True, blank=True
    )
    description = models.TextField(
        "Полное описание", null=True, blank=True
    )
    club_achievements = models.TextField(
        "Достижения клуба", null=True, blank=True
    )
    club_students_achievements = models.TextField(
        "Достижения студентов клуба", null=True, blank=True
    )
