# Generated by Django 3.0.5 on 2020-08-25 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Benefits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Текст')),
            ],
            options={
                'verbose_name': 'Преимущество',
                'verbose_name_plural': 'Преимущества',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название')),
                ('product_type', models.CharField(choices=[('UNICLASS', 'UniClass'), ('UNIPASS', 'UniPass')], max_length=25, verbose_name='Тип продукта')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Стоимость')),
                ('days_amount', models.PositiveSmallIntegerField(default=0, verbose_name='Количество дней')),
                ('visits_amount', models.PositiveSmallIntegerField(default=0, verbose_name='Количество посещении')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
    ]
