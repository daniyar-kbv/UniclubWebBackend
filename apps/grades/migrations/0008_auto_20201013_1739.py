# Generated by Django 3.0.5 on 2020-10-13 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grades', '0007_auto_20201013_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='regular_places',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Максимальное количество обычных мест'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='regular_clients',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Текущее количество занятых обычных мест'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='regular_places',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Максимальное количество обычных мест'),
        ),
    ]
