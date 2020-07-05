from django.db import models

from . import ProductType


class Benefits(models.Model):
    class Meta:
        verbose_name = "Преимущество"
        verbose_name_plural = "Преимущества"

    name = models.CharField("Текст", max_length=256)

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    name = models.CharField("Название", max_length=256)
    product_type = models.CharField(
        "Тип продукта",
        choices=ProductType.choices,
        max_length=25
    )
    price = models.DecimalField("Стоимость", max_digits=12, decimal_places=2)
    days_amount = models.PositiveSmallIntegerField("Количество дней", default=0)
    visits_amount = models.PositiveSmallIntegerField("Количество посещении", default=0)

    def __str__(self):
        return self.name
