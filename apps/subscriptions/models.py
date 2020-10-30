from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model

from apps.core.models import TimestampModel
from apps.person.models import ClientChildren
from apps.products.models import Product
from apps.grades.models import Course, Lesson
from apps.clubs.models import Club

from . import (
    SubscriptionOperations, FreezeRequestDesicion, SubscriptionStatuses, FreezeDuration
)

import constants

User = get_user_model()


class Subscription(TimestampModel):
    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    id = models.UUIDField(default=uuid4, primary_key=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="subscriptions",
        verbose_name="Товар"
    )
    customer = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="subscriptions",
        verbose_name="Покупатель"
    )
    child = models.ForeignKey(
        ClientChildren,
        on_delete=models.PROTECT,
        related_name="subcriptions",
        verbose_name="Пользователь"
    )
    visits_amount = models.PositiveSmallIntegerField(
        "Количество посещении", default=0
    )
    status = models.CharField(
        "Статус подписки",
        max_length=20,
        choices=SubscriptionStatuses.choices,
        default=SubscriptionStatuses.ACTIVE
    )
    club = models.ForeignKey(
        Club,
        on_delete=models.PROTECT,
        related_name='subscriptions',
        verbose_name='Клуб',
        null=True,
        blank=True
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name='subscriptions',
        verbose_name='Курс',
        null=True,
        blank=True
    )

    start_date = models.DateField("Начало подписки")
    end_date = models.DateField("Конец подписки")

    def add_history_record(self, operation: str) -> None:
        SubscriptionHistoryRecord.objects.create(
            subscription=self,
            operation=operation
        )

    def __str__(self):
        return f"({self.id}) {self.product.name}"


class SubscriptionHistoryRecord(TimestampModel):
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.PROTECT,
        related_name="history_records",
        verbose_name="Подписка"
    )
    operation = models.CharField(
        "Операция", max_length=256, choices=SubscriptionOperations.choices
    )


class FreezeRequest(TimestampModel):
    class Meta:
        verbose_name = "Запрос на заморозку подписки"
        verbose_name_plural = "Запросы на заморозку абонемента"

    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name="freeze_requests",
        verbose_name="Подписка"
    )
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="freeze_requests",
        verbose_name="Покупатель"
    )
    duration = models.CharField(
        'Время',
        choices=FreezeDuration.choices,
        default=FreezeDuration.THREE_DAYS,
        max_length=25
    )
    desicion = models.CharField(
        "Решение",
        choices=FreezeRequestDesicion.choices,
        default=FreezeRequestDesicion.NOT_PROCESSED,
        max_length=25
    )


class LessonBooking(models.Model):
    user = models.ForeignKey(
        ClientChildren,
        on_delete=models.CASCADE,
        related_name='lesson_statuses',
        verbose_name='Пользователь',
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name='Занятие',
        related_name='bookings'
    )
    subscription = models.ForeignKey(
        Subscription,
        verbose_name="Подписка",
        on_delete=models.CASCADE,
        related_name='bookings',
    )
    status = models.PositiveSmallIntegerField(
        'Статус',
        choices=constants.LESSON_STATUSES,
        default=None,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Бронирование занятия'
        verbose_name_plural = 'Бронирования занятий'

    def __str__(self):
        return f'({self.id}) {self.user}, {self.lesson.course.name}'

