# Generated by Django 3.0.5 on 2020-10-28 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0003_lessonbooking'),
    ]

    operations = [
        migrations.AddField(
            model_name='freezerequest',
            name='duration',
            field=models.CharField(choices=[('THREE_DAYS', 'На 3 дня'), ('ONE_WEEK', 'На неделю'), ('TWO_WEEKS', 'На 2 недели')], default='THREE_DAYS', max_length=25, verbose_name='Время'),
        ),
    ]
