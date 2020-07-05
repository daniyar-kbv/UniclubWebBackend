from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model

from apps.core.models import TimestampModel
# from apps.products.models import UniPass
from apps.person.models import ClientChildren

User = get_user_model()


class Subscription(TimestampModel):
    class Meta:
        verbose_name = "Подписка UniPass"
        verbose_name_plural = "Подписки UniPass"

    id = models.UUIDField(default=uuid4, primary_key=True)
    # unipass = models.ForeignKey(
    #     UniPass,
    #     on_delete=models.PROTECT,
    #     related_name="subscriptions",
    #     verbose_name="UniPass"
    # )
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
