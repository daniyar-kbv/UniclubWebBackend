# Generated by Django 3.0.5 on 2020-10-28 04:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0003_delete_coach'),
        ('grades', '0017_auto_20201027_2307'),
    ]

    operations = [
        migrations.CreateModel(
            name='LessonBooking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_type', models.CharField(choices=[('UNICLASS', 'UniClass'), ('UNIPASS', 'UniPass')], max_length=25, verbose_name='Тип продукта')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Ребенок присутствовал'), (1, 'Ребенок отсутствовал'), (2, 'Отменили занятие')], default=None, null=True, verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Статус занятия с ребенком',
                'verbose_name_plural': 'Статусы занятий с детьми',
            },
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='uniclass_users',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='unipass_users',
        ),
        migrations.DeleteModel(
            name='LessonUserStatus',
        ),
        migrations.AddField(
            model_name='lessonbooking',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='grades.Lesson', verbose_name='Занятие'),
        ),
        migrations.AddField(
            model_name='lessonbooking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_statuses', to='person.ClientChildren', verbose_name='Пользователь'),
        ),
    ]
