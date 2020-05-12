from django.db import models
from django.utils import timezone


class NameModel(models.Model):
    first_name = models.CharField("Имя", max_length=150, null=True, blank=True)
    last_name = models.CharField("Фамилия", max_length=150, null=True, blank=True)
    middle_name = models.CharField("Отчество", max_length=150, null=True, blank=True)

    class Meta:
        abstract = True

    @property
    def full_name(self):
        return " ".join(
            filter(None, [self.last_name, self.first_name, self.middle_name])
        )


class TimestampModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField("Создан", default=timezone.now)
    updated_at = models.DateTimeField("Обновлен", auto_now=True)
