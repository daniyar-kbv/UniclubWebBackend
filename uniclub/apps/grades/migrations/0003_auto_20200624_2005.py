# Generated by Django 3.0.5 on 2020-06-24 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grades', '0002_grade_club'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='grade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='grades.Grade', verbose_name='Класс'),
        ),
    ]
