# Generated by Django 3.0.5 on 2020-07-06 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grades', '0007_auto_20200705_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12, verbose_name='Стоимость'),
            preserve_default=False,
        ),
    ]
