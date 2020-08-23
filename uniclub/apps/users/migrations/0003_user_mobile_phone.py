# Generated by Django 3.0.5 on 2020-08-23 07:56

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200513_0333'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mobile_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(default="+77087552390", max_length=128, region=None, unique=True, verbose_name='Номер телефона'),
            preserve_default=False,
        ),
    ]
