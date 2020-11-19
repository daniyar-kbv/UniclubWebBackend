from django.db import models
from django.utils import timezone
from django.conf import settings

from apps.core.models import TimestampModel
from apps.users.models import User

import datetime


class PasswordRestoreRequestManager(models.Manager):
    def active(self):
        created_min = timezone.now() - datetime.timedelta(minutes=settings.OTP_VALIDITY_PERIOD)
        return self.filter(~models.Q(is_used=True) & models.Q(created_at__gte=created_min))


class PasswordRestoreRequest(TimestampModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='password_restore_requests'
    )
    is_used = models.BooleanField('Использовано', default=False, blank=True)

    objects = PasswordRestoreRequestManager()

    class Meta:
        verbose_name = 'Запрос на восстановление пароля'
        verbose_name_plural = 'Запросы на восстановление пароля'

    def __str__(self):
        return f'({self.id}) {self.user} {self.created_at}'
