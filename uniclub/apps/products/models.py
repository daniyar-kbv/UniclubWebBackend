from django.db import models


class Benefits(models.Model):
    class Meta:
        verbose_name = "Преимущество"
        verbose_name_plural = "Преимущества"

    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class UniPass(models.Model):
    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"

    name = models.CharField(max_length=56)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    days_amount = models.PositiveSmallIntegerField(default=0)
    visits_amount = models.PositiveSmallIntegerField(default=0)
    benefits = models.ManyToManyField(Benefits)

    def __str__(self):
        return self.name
