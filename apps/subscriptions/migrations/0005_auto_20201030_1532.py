# Generated by Django 3.0.5 on 2020-10-30 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0004_freezerequest_duration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lessonbooking',
            options={'verbose_name': 'Бронирование занятия', 'verbose_name_plural': 'Бронирования занятий'},
        ),
    ]
