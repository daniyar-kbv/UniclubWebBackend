import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.core.models import TimestampModel, NameModel

from . import UserTypes
from .managers import UserManager


class User(NameModel, TimestampModel, AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    mobile_phone = PhoneNumberField("Номер телефона", unique=True)
    email = models.EmailField("EMAIL", null=True)

    user_type = models.CharField(
        "Тип пользователя",
        choices=UserTypes.choices,
        default=UserTypes.CLIENT,
        max_length=20,
    )

    is_active = models.BooleanField("Активный", default=True)
    is_staff = models.BooleanField("Сотрудник", default=False)

    secret_key = models.UUIDField("Секретный ключ", default=uuid.uuid4, unique=True)

    USERNAME_FIELD = "mobile_phone"
    objects = UserManager()

    def __str__(self):
        return f"{self.mobile_phone} ({self.full_name})"
