from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model

from apps.core.models import TimestampModel
from apps.person.models import ClientChildren
from apps.products.models import Product

from . import SubscriptionOperations

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

    start_date = models.DateField("Начало подписки")
    end_date = models.DateField("Конец подписки")


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

    def __str__(self):
        return f"{self.operation} ({self.subscription})"
