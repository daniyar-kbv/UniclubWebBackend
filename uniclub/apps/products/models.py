from django.db import models


class Benefits(models.Model):
    name = models.CharField(max_length=256)


class UniPass(models.Model):
    name = models.CharField(max_length=56)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    days_amount = models.PositiveSmallIntegerField(default=0)
    visits_amount = models.PositiveSmallIntegerField(default=0)
    benefits = models.ManyToManyField(Benefits)
