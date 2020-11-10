from decimal import Decimal

from django.db import models
from django.contrib.auth import get_user_model

from apps.core.models import CityModel, TimestampModel, ReviewMixin, GradeType, AdministrativeDivision

from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()


class Address(models.Model):
    city = models.ForeignKey(
        CityModel,
        on_delete=models.CASCADE,
        verbose_name='Город',
        null=True,
        blank=False
    )
    address = models.CharField("Адрес", max_length=256, null=True)
    latitude = models.FloatField("Долгота", null=True)
    longitude = models.FloatField("Широта", null=True)

    class Meta:
        abstract = True


class SocialNetwork(models.Model):
    instagram = models.URLField(null=True)
    facebook = models.URLField(null=True)
    vk = models.URLField(null=True)

    class Meta:
        abstract = True


class ContactInfo(Address, SocialNetwork):
    mobile_phone = PhoneNumberField("Мобильный телефон")
    home_phone = PhoneNumberField("Домашний телефон", null=True)
    work_phone = PhoneNumberField("Рабочий телефон", null=True)
    email = models.EmailField("Почта", null=True)
    website = models.URLField("Сайт", null=True)

    class Meta:
        abstract = True


class AdditionalInformation(models.Model):
    image = models.ImageField(
        "Основная фотография клуба", upload_to="club_images/", null=True
    )
    short_description = models.CharField(
        "Краткое описание", max_length=256, null=True
    )
    description = models.TextField(
        "Полное описание", null=True
    )
    competition_frequency = models.CharField(
        "Периодичность внутриклубных соревновании", max_length=256, null=True
    )
    hazard_information = models.CharField(
        "Информация о травмоопасности", max_length=256, blank=True, null=True
    )
    student_achievements = models.TextField(
        "Достижения учеников клуба", null=True
    )
    events_information = models.TextField(
        "Информация об участии клуба в различных мероприятиях", null=True
    )
    other_services = models.TextField(
        "Другие услуги клуба", null=True
    )
    parking_available = models.BooleanField(
        "Парковка", null=True
    )
    places_for_parents = models.BooleanField(
        "Места для родителей", null=True
    )
    parent_presence = models.BooleanField(
        "Посещение родителей", null=True
    )
    video_monitoring = models.BooleanField(
        "Возможность видеонаблюдения", null=True
    )
    classes_for_disabled = models.BooleanField(
        "Занятия для людей с ограниченными возможностями", null=True
    )
    floor_area = models.DecimalField(
        "Общая площадь", max_digits=10, decimal_places=2, null=True
    )
    number_of_bathrooms = models.PositiveSmallIntegerField(
        "Количество санузлов", null=True
    )
    number_of_changing_rooms = models.PositiveSmallIntegerField(
        "Количество раздевалок", null=True,
    )
    total_number_of_students = models.PositiveIntegerField(
        "Количество студентов со дня открытия", null=True
    )
    social_reviews = models.URLField(
        "Отзывы в социальных сетях", null=True
    )
    from_age = models.PositiveSmallIntegerField(
        "Возраст от", help_text="в годах", null=True, blank=False
    )
    to_age = models.PositiveSmallIntegerField(
        "Возраст до", help_text="в годах", null=True, blank=False
    )
    is_new = models.BooleanField(
        'Новый', null=False, blank=True, default=True
    )
    grade_types = models.ManyToManyField(
        GradeType,
        related_name='clubs',
        verbose_name='Виды занятий',
        blank=True
    )

    class Meta:
        abstract = True


class Club(ContactInfo, AdditionalInformation):
    class Meta:
        verbose_name = "Клубы"
        verbose_name_plural = "Клуб"

    club_admin = models.OneToOneField(
       User, on_delete=models.PROTECT, related_name="club", null=True,
    )
    name = models.CharField(
        "Название", max_length=52, null=True, db_index=True
    )
    favorite_users = models.ManyToManyField(
        User,
        related_name='favorite_clubs',
        verbose_name='Пользователи (избранное)',
        blank=True
    )

    def __str__(self):
        return f'({self.id}) {str(self.name)}'


class ClubImage(models.Model):
    club = models.ForeignKey(Club, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="club_images/")


class ClubReview(ReviewMixin):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='club_reviews',
        verbose_name='Пользователь'
    )
    helped = models.ManyToManyField(
        User,
        related_name='club_helped',
        verbose_name='Помог',
        blank=True
    )
    not_helped = models.ManyToManyField(
        User,
        related_name='club_not_helped',
        verbose_name='Не помог',
        blank=True
    )
    club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Клуб'
    )

    class Meta:
        verbose_name = 'Отзыв клуба'
        verbose_name_plural = 'Отзывы клубов'

    def __str__(self):
        return f'({self.id}) {self.user.full_name}, {self.club}'
