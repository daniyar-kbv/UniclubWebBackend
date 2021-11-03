from typing import Iterable, cast, List
from datetime import datetime, timedelta

from django.db import models, transaction
from django.db.models import Count, Q
from django.contrib.postgres.fields import ArrayField, JSONField
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.core.models import TimestampModel, ReviewMixin, NameModel, GradeType
from apps.clubs.models import Club
from apps.users.models import User
from apps.person.models import ClientChildren
from apps.utils import general

from . import Levels, Intensities, Durations

import constants


class FreePlacesMixin(models.Model):
    unipass_places = models.PositiveSmallIntegerField(
        "Максимальное количество мест для UniPass", default=0
    )
    uniclass_places = models.PositiveSmallIntegerField(
        "Максимальное количество мест для UniClass", default=0
    )
    regular_places = models.PositiveSmallIntegerField(
        "Максимальное общее количество мест", default=0
    )

    class Meta:
        abstract = True


class BookedPlacesMixin(models.Model):
    unipass_clients = models.PositiveSmallIntegerField(
        "Текущее количество занятых мест UniPass", default=0
    )
    uniclass_clients = models.PositiveSmallIntegerField(
        "Текущее количество занятых мест UniClass", default=0
    )
    regular_clients = models.PositiveSmallIntegerField(
        "Текущее общее количество занятых мест", default=0
    )

    class Meta:
        abstract = True


class Coach(NameModel):
    class Meta:
        verbose_name = "Тренеры"
        verbose_name_plural = "Тренер"

    club = models.ForeignKey(
        Club, related_name="coaches", on_delete=models.CASCADE, verbose_name="Клуб"
    )
    image = models.ImageField("Фотография", upload_to="coach/", null=True, blank=True)
    additional_information = models.TextField('Дополнительная информация', null=True, blank=True)
    grade_type = models.ForeignKey(
        GradeType,
        on_delete=models.PROTECT,
        related_name='coaches',
        verbose_name='Вид занятий',
        null=True,
        blank=False
    )

    def __str__(self):
        return f'({self.id}) {self.full_name}'


class Course(FreePlacesMixin, TimestampModel):
    class Meta:
        verbose_name = "Курсы"
        verbose_name_plural = "Курс"
        ordering = ['id']

    club = models.ForeignKey(
        Club,
        related_name="courses",
        verbose_name="Клуб",
        on_delete=models.CASCADE,
        null=True,
        blank=False
    )
    grade_type = models.ForeignKey(
        GradeType,
        related_name='courses',
        verbose_name='Вид занятия',
        on_delete=models.PROTECT,
        null=True,
        blank=False
    )
    name = models.CharField("Название", max_length=120)
    description = models.TextField("Описание", null=True)
    price = models.DecimalField("Стоимость", max_digits=12, decimal_places=2)

    lesson_duration = models.PositiveSmallIntegerField(
        "Продолжительность занятий", help_text="в минутах", null=True
    )
    course_duration = models.CharField(
        "Продолжительность курса", max_length=20, choices=Durations.choices
    )
    intensity = models.CharField(
        "Интенсивнось занятий", max_length=20, choices=Intensities.choices
    )
    level = models.CharField(
        "Уровень подготовки", max_length=20, choices=Levels.choices
    )

    start_date = models.DateField("Дата начала")
    end_date = models.DateField("Дата окончания")

    from_age = models.PositiveSmallIntegerField(
        "Возраст от", help_text="в годах", null=True, blank=False
    )
    to_age = models.PositiveSmallIntegerField(
        "Возраст до", help_text="в годах", null=True, blank=False
    )
    additional_conditions = models.TextField(
        "Дополнительные условия", null=True, blank=True
    )
    needed_inventory = models.CharField(
        "Необходимый инвентарь", max_length=500, null=True, blank=True
    )
    needed_accessories = models.CharField(
        "Необходимые принадлежности", max_length=500, null=True, blank=True
    )
    dress_code = models.CharField(
        "Форма одежды", max_length=500, null=True, blank=True
    )
    is_certificate = models.BooleanField(
        "Сертификат об окончании курса", default=False, null=True, blank=True
    )
    coaches = models.ManyToManyField(
        Coach,
        related_name='courses',
        verbose_name='Тренера'
    )

    def __str__(self):
        return f'({self.id}) {self.name}'


class LessonDay(models.Model):
    class Meta:
        verbose_name = "День занятия"
        verbose_name_plural = "Дни занятий"
        ordering = ['weekday', 'start_time']

    course = models.ForeignKey(
        Course,
        related_name="lesson_days",
        on_delete=models.CASCADE
    )
    weekday = models.PositiveSmallIntegerField(
        verbose_name="День недели",
        choices=constants.WEEKDAYS,
        null=False,
        blank=False
    )
    coach = models.ForeignKey(
        Coach,
        verbose_name='Тренер',
        related_name='lesson_days',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    start_time = models.TimeField("Время начала")
    end_time = models.TimeField("Время окончания")

    def __str__(self):
        return f'({self.id}) {self.course.name}: {general.get_value_from_choices(constants.WEEKDAYS, self.weekday)}, {self.start_time}-{self.end_time}'


class Lesson(FreePlacesMixin, BookedPlacesMixin, TimestampModel):
    class Meta:
        verbose_name = "Занятие"
        verbose_name_plural = "Занятия"

    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        related_name="lessons",
        null=True
    )

    lesson_day = models.ForeignKey(
        LessonDay,
        on_delete=models.CASCADE,
        verbose_name='День занятия',
        related_name='lesson_days',
        null=True,
        blank=False
    )

    day = models.DateField("День проведения")
    start_time = models.TimeField("Время начала")
    end_time = models.TimeField("Время конца")

    favorite_users = models.ManyToManyField(
        User,
        related_name='favorite_lessons',
        verbose_name='Пользователи (избранное)',
        blank=True
    )

    coach = models.ForeignKey(
        Coach,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Тренер',
        null=True,
        blank=False
    )

    @classmethod
    @transaction.atomic
    def generate_lessons_for_course(cls, course: Course):
        if not course.lesson_days:
            raise ValueError("Course must have lesson days")

        start_date, end_date = (
            course.start_date, course.end_date
        )
        delta = timedelta(days=1)

        Lesson.objects.filter(
            Q(course=course) & Q(Q(day__lte=course.start_date) | Q(day__gte=course.end_date))).delete()

        lesson_days = LessonDay.objects.filter(course=course)

        while start_date <= end_date:
            weekday = start_date.weekday()
            try:
                lesson_day = lesson_days.get(weekday=weekday)
                if not Lesson.objects.filter(lesson_day=lesson_day, day=start_date).exists():
                    new_lesson = cls(
                        lesson_day_id=lesson_day.id,
                        course=course,
                        day=start_date,
                        start_time=lesson_day.start_time,
                        end_time=lesson_day.end_time,
                        coach=lesson_day.coach
                    )
                    new_lesson.save()
            except:
                pass
            start_date += delta

    def __str__(self):
        return f"({self.id}) Занитие по курсу {self.course.name} " \
               f"({self.day} с {self.start_time} по {self.end_time})"


class CourseReview(ReviewMixin):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='course_reviews',
        verbose_name='Пользователь'
    )
    helped = models.ManyToManyField(
        User,
        related_name='course_helped',
        verbose_name='Помог',
        blank=True
    )
    not_helped = models.ManyToManyField(
        User,
        related_name='course_not_helped',
        verbose_name='Не помог',
        blank=True
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Курс'
    )

    class Meta:
        verbose_name = 'Отзыв курса'
        verbose_name_plural = 'Отзывы курсов'

    def __str__(self):
        return f'({self.id}) {self.user.full_name}, {self.course}'
