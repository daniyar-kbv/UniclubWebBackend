# Generated by Django 3.0.5 on 2020-10-19 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AgeGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='Название')),
                ('from_age', models.PositiveSmallIntegerField(verbose_name='От')),
                ('to_age', models.PositiveSmallIntegerField(verbose_name='До')),
            ],
            options={
                'verbose_name': 'Возрастная группа',
                'verbose_name_plural': 'Возрастные группы',
            },
        ),
    ]
