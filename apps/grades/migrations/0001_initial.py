# Generated by Django 3.0.5 on 2020-08-29 20:54

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clubs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('unipass_places', models.PositiveSmallIntegerField(default=0, verbose_name='Максимальное количество мест для UniPass')),
                ('uniclass_places', models.PositiveSmallIntegerField(default=0, verbose_name='Максимальное количество мест для UniClass')),
                ('name', models.CharField(max_length=120, verbose_name='Название')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Стоимость')),
                ('lesson_duration', models.PositiveSmallIntegerField(help_text='в минутах', null=True, verbose_name='Продолжительность занятий')),
                ('course_duration', models.CharField(choices=[('PERIODIC', 'Периодичный'), ('LONG', 'Продолжительный')], max_length=20, verbose_name='Продолжительность курса')),
                ('intensity', models.CharField(choices=[('ALL', 'Все'), ('LOW', 'Низкая'), ('MEDIUM', 'Средняя'), ('HIGH', 'Высокая')], max_length=20, verbose_name='Интенсивнось занятий')),
                ('level', models.CharField(choices=[('ALL', 'Все'), ('BEGINNER', 'Начальный'), ('MIDDLE', 'Средний'), ('ADVANCED', 'Продвинутый'), ('MASTER', 'Мастер')], max_length=20, verbose_name='Уровень подготовки')),
                ('start_date', models.DateField(verbose_name='Дата начала')),
                ('end_date', models.DateField(verbose_name='Дата окончания')),
            ],
            options={
                'verbose_name': 'Курсы',
                'verbose_name_plural': 'Курс',
            },
        ),
        migrations.CreateModel(
            name='LessonDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(6)], verbose_name='День недели')),
                ('start_time', models.TimeField(verbose_name='Время начала')),
                ('end_time', models.TimeField(verbose_name='Время окончания')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_days', to='grades.Course')),
            ],
            options={
                'verbose_name': 'Дни занятии',
                'verbose_name_plural': 'День занятия',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('unipass_places', models.PositiveSmallIntegerField(default=0, verbose_name='Максимальное количество мест для UniPass')),
                ('uniclass_places', models.PositiveSmallIntegerField(default=0, verbose_name='Максимальное количество мест для UniClass')),
                ('unipass_clients', models.PositiveSmallIntegerField(default=0, verbose_name='Текущее количество занятых мест UniPass')),
                ('uniclass_clients', models.PositiveSmallIntegerField(default=0, verbose_name='Текущее количество занятых мест UniClass')),
                ('day', models.DateField(verbose_name='День проведения')),
                ('start_time', models.TimeField(verbose_name='Время начала')),
                ('end_time', models.TimeField(verbose_name='Время конца')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='lessons', to='grades.Course', verbose_name='Курс')),
            ],
            options={
                'verbose_name': 'Занятия',
                'verbose_name_plural': 'Заниятие',
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('name', models.CharField(max_length=120, verbose_name='Название')),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='clubs.Club', verbose_name='Клуб')),
            ],
            options={
                'verbose_name': 'Классы',
                'verbose_name_plural': 'Класс',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='grade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='grades.Grade', verbose_name='Класс'),
        ),
    ]
