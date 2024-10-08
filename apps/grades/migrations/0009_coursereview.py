# Generated by Django 3.0.5 on 2020-10-13 16:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grades', '0008_auto_20201013_1739'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('rating', models.PositiveSmallIntegerField(default=0, verbose_name='Рейтинг')),
                ('advantages', models.TextField(blank=True, null=True, verbose_name='Достоинства')),
                ('disadvantages', models.TextField(blank=True, null=True, verbose_name='Недостатки')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='grades.Course', verbose_name='Курс')),
                ('helped', models.ManyToManyField(related_name='course_helped', to=settings.AUTH_USER_MODEL, verbose_name='Помог')),
                ('not_helped', models.ManyToManyField(related_name='course_not_helped', to=settings.AUTH_USER_MODEL, verbose_name='Не помог')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_reviews', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Отзыв курса',
                'verbose_name_plural': 'Отзывы курсов',
            },
        ),
    ]
