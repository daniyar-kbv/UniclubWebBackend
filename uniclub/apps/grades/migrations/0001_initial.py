# Generated by Django 3.0.5 on 2020-05-27 18:37

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('name', models.CharField(max_length=120, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Классы',
                'verbose_name_plural': 'Класс',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time_1', models.TimeField(null=True)),
                ('end_time_1', models.TimeField(null=True)),
                ('start_time_2', models.TimeField(null=True)),
                ('end_time_2', models.TimeField(null=True)),
                ('start_time_3', models.TimeField(null=True)),
                ('end_time_3', models.TimeField(null=True)),
                ('start_time_4', models.TimeField(null=True)),
                ('end_time_4', models.TimeField(null=True)),
                ('start_time_5', models.TimeField(null=True)),
                ('end_time_5', models.TimeField(null=True)),
                ('start_time_6', models.TimeField(null=True)),
                ('end_time_6', models.TimeField(null=True)),
                ('start_time_7', models.TimeField(null=True)),
                ('end_time_7', models.TimeField(null=True)),
                ('name', models.CharField(max_length=120, verbose_name='Название')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('lasting', models.PositiveSmallIntegerField(help_text='в минутах', null=True, verbose_name='Продолжительность занятий')),
                ('intensity', models.CharField(choices=[('ALL', 'Все'), ('LOW', 'Низкая'), ('MEDIUM', 'Средняя'), ('HIGH', 'Высокая')], max_length=20, verbose_name='Интенсивнось занятий')),
                ('level', models.CharField(choices=[('ALL', 'Все'), ('BEGINNER', 'Начальный'), ('MIDDLE', 'Средний'), ('ADVANCED', 'Продвинутый'), ('MASTER', 'Мастер')], max_length=20, verbose_name='Уровень подготовки')),
                ('start_date', models.DateTimeField(verbose_name='Дата начала')),
                ('end_date', models.DateTimeField(verbose_name='Дата окончания')),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='grades.Grade', verbose_name='Класс')),
            ],
            options={
                'verbose_name': 'Занятия',
                'verbose_name_plural': 'Занятие',
            },
        ),
    ]
