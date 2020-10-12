import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.core.models import TimestampModel, NameModel
from apps.clubs.models import Club
from apps.grades.models import Course

from . import UserTypes
from .managers import UserManager


class User(NameModel, TimestampModel, AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    username = None
    mobile_phone = PhoneNumberField("Номер телефона", unique=True)
    email = models.EmailField("EMAIL", null=True)

    user_type = models.CharField(
        "Тип пользователя",
        choices=UserTypes.choices,
        default=UserTypes.CLIENT,
        max_length=20,
    )

    favorite_clubs = models.ManyToManyField(
        Club,
        related_name='favorite_users',
        verbose_name='Избранные клубы'
    )
    favorite_courses = models.ManyToManyField(
        Course,
        related_name='favorite_users',
        verbose_name='Избранные занятия'
    )

    is_active = models.BooleanField("Активный", default=False)
    is_staff = models.BooleanField("Сотрудник", default=False)

    secret_key = models.UUIDField("Секретный ключ", default=uuid.uuid4, unique=True)

    USERNAME_FIELD = "mobile_phone"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.mobile_phone} ({self.full_name})"
