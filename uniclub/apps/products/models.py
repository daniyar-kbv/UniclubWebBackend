from django.db import models


class Benefits(models.Model):
    class Meta:
        verbose_name = "Преимущество"
        verbose_name_plural = "Преимущества"

    name = models.CharField("Текст", max_length=256)

    def __str__(self):
        return self.name


class UniPass(models.Model):
    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"

    name = models.CharField("Название", max_length=56)
    price = models.DecimalField("Цена", max_digits=12, decimal_places=2)
    days_amount = models.PositiveSmallIntegerField("Количество дней", default=0)
    visits_amount = models.PositiveSmallIntegerField("Количество посещении", default=0)
    benefits = models.ManyToManyField(Benefits, verbose_name="Преимущества", null=True, blank=True)

    def __str__(self):
        return self.name
