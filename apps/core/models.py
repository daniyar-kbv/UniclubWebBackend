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

    @property
    def created_at_pretty(self):
        return self.created_at.strftime("%d/%m/%Y %H:%M:%S")

    @property
    def updated_at_pretty(self):
        return self.updated_at.strftime("%d/%m/%Y %H:%M:%S")


class CityModel(models.Model):
    class Meta:
        verbose_name = "Города"
        verbose_name_plural = "Город"

    name = models.CharField("Название", max_length=256)

    def __str__(self):
        return f'({self.id}) {self.name}'


class AdministrativeDivision(models.Model):
    class Meta:
        verbose_name = 'Административное деление'
        verbose_name_plural = 'Административные деления'

    name = models.CharField("Название", max_length=256)
    city = models.ForeignKey(
        CityModel,
        on_delete=models.CASCADE,
        verbose_name='Город',
        related_name='administrative_divisions'
    )

    def __str__(self):
        return f'({self.id}) {self.name}'


class ReviewMixin(TimestampModel):
    rating = models.PositiveSmallIntegerField('Рейтинг', default=0)
    advantages = models.TextField('Достоинства', null=True, blank=True)
    disadvantages = models.TextField('Недостатки', null=True, blank=True)
    comment = models.TextField('Комментарий', null=True, blank=True)

    class Meta:
        abstract = True


class GradeType(models.Model):
    class Meta:
        verbose_name = "Вид занятия"
        verbose_name_plural = "Виды занятий"

    name = models.CharField("Название", max_length=120)

    def __str__(self):
        return f'({self.id}) {self.name}'
