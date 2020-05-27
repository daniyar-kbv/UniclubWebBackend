from django.db import models

from apps.core.models import TimestampModel

from . import Levels, Intensities


class Grade(TimestampModel):
    class Meta:
        verbose_name = "Классы"
        verbose_name_plural = "Класс"

    name = models.CharField("Название", max_length=120)

    def __str__(self):
        return self.name


class ClassDays(models.Model):
    class Meta:
        abstract = True

    start_time_1 = models.TimeField(null=True)
    end_time_1 = models.TimeField(null=True)

    start_time_2 = models.TimeField(null=True)
    end_time_2 = models.TimeField(null=True)

    start_time_3 = models.TimeField(null=True)
    end_time_3 = models.TimeField(null=True)

    start_time_4 = models.TimeField(null=True)
    end_time_4 = models.TimeField(null=True)

    start_time_5 = models.TimeField(null=True)
    end_time_5 = models.TimeField(null=True)

    start_time_6 = models.TimeField(null=True)
    end_time_6 = models.TimeField(null=True)

    start_time_7 = models.TimeField(null=True)
    end_time_7 = models.TimeField(null=True)


class Lesson(ClassDays):
    class Meta:
        verbose_name = "Занятия"
        verbose_name_plural = "Занятие"

    grade = models.ForeignKey(
        Grade,
        verbose_name="Класс",
        on_delete=models.CASCADE,
        related_name="grades"
    )
    name = models.CharField("Название", max_length=120)
    description = models.TextField("Описание", null=True)
    lasting = models.PositiveSmallIntegerField(
        "Продолжительность занятий", help_text="в минутах", null=True
    )
    intensity = models.CharField(
        "Интенсивнось занятий", max_length=20, choices=Intensities.choices
    )
    level = models.CharField(
        "Уровень подготовки", max_length=20, choices=Levels.choices
    )
    start_date = models.DateTimeField("Дата начала")
    end_date = models.DateTimeField("Дата окончания")

    def __str__(self):
        return self.name
