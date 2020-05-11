from django.db import models

from apps.clubs.models import Club


class Coach(models.Model):
    class Meta:
        verbose_name = "Тренеры"
        verbose_name_plural = "Тренер"

    club = models.ForeignKey(
        Club, related_name="coaches", on_delete=models.CASCADE
    )
    full_name = models.CharField(max_length=256)
    image = models.ImageField(upload_to="coach/")

    def __str__(self):
        return self.full_name