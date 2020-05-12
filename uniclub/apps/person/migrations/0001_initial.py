# Generated by Django 3.0.5 on 2020-05-12 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clubs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Фамилия')),
                ('middle_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Отчество')),
                ('image', models.ImageField(upload_to='coach/', verbose_name='Фотография')),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coaches', to='clubs.Club')),
            ],
            options={
                'verbose_name': 'Тренеры',
                'verbose_name_plural': 'Тренер',
            },
        ),
    ]
