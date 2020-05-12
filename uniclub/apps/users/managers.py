from datetime import timedelta
from typing import Tuple, Optional

from django.conf import settings
from django.contrib.auth.models import BaseUserManager
from django.db.models import Q, Model
from django.utils import timezone

from . import UserTypes


class UserManager(BaseUserManager):
    def __create_user(
        self,
        email,
        password=None,
        user_type=UserTypes.CLIENT,
        first_name=None,
        middle_name=None,
        last_name=None,
        is_staff=False,
        is_active=False,
        is_superuser=False,
    ):
        if not password:
            raise ValueError("Users must have password")
        if not email:
            raise ValueError("Users must have email")

        if email:
            email = self.normalize_email(email)

        user = self.model(
            email=email,
            user_type=user_type,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            is_staff=is_staff,
            is_active=is_active,
            is_superuser=is_superuser,
        )

        if password is not None:
            user.set_password(password)

        user.save(using=self._db)

        return user

    def create_user(self, email, password, **kwargs):
        return self.__create_user(
            email,
            password,
            first_name=kwargs.get("first_name"),
            middle_name=kwargs.get("middle_name"),
            last_name=kwargs.get("last_name"),
            user_type=kwargs.get("user_type"),
            is_staff=kwargs.get("is_staff", False),
            is_active=kwargs.get("is_active", False),
            is_superuser=kwargs.get("is_superuser", False),
        )

    def create_superuser(self, email, password):
        return self.__create_user(
            email, password, is_staff=True, is_active=True, is_superuser=True
        )

    def create(self, **kwargs):
        """
        Important to have this to get factories working by default
        """
        email = kwargs.get("email")
        if not email:
            raise ValueError("Users must have an email address")
        return self.create_user(**kwargs)
