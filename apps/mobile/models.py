from django.db import models


class AgeGroup(models.Model):
    name = models.CharField('Название', max_length=10)
    from_age = models.PositiveSmallIntegerField('От')
    to_age = models.PositiveSmallIntegerField('До')

    class Meta:
        verbose_name = 'Возрастная группа'
        verbose_name_plural = 'Возрастные группы'
        ordering = ['from_age']

    def __str__(self):
        return f'({self.id}) {self.name}'
