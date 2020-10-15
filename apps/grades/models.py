from typing import Iterable, cast, List
from datetime import datetime, timedelta

from django.db import models, transaction
from django.contrib.postgres.fields import ArrayField, JSONField
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.core.models import TimestampModel, ReviewMixin
from apps.clubs.models import Club
from apps.users.models import User

from . import Levels, Intensities, Durations


class GradeType(models.Model):
    class Meta:
        verbose_name = "Вид занятия"
        verbose_name_plural = "Виды занятий"
    name = models.CharField("Название", max_length=120)

    def __str__(self):
        return f'({self.id}) {self.name}'


class Grade(TimestampModel):
    class Meta:
        verbose_name = "Вид занятия клуба"
        verbose_name_plural = "Виды занятий клуба"

    club = models.ForeignKey(
        Club,
        related_name="grades",
        verbose_name="Клуб",
        on_delete=models.CASCADE
    )
    grade_type = models.ForeignKey(
        GradeType,
        related_name='grades',
        verbose_name='Вид занятия',
        on_delete=models.CASCADE,
        null=True,
        blank=False
    )

    def __str__(self):
        return f'({self.id}) {self.club.name}: {self.grade_type.name}'


class FreePlacesMixin(models.Model):
    unipass_places = models.PositiveSmallIntegerField(
        "Максимальное количество мест для UniPass", default=0
    )
    uniclass_places = models.PositiveSmallIntegerField(
        "Максимальное количество мест для UniClass", default=0
    )
    regular_places = models.PositiveSmallIntegerField(
        "Максимальное количество обычных мест", default=0
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
        "Текущее количество занятых обычных мест", default=0
    )

    class Meta:
        abstract = True


class Course(FreePlacesMixin, TimestampModel):
    class Meta:
        verbose_name = "Курсы"
        verbose_name_plural = "Курс"

    grade = models.ForeignKey(
        Grade,
        verbose_name="Занятие",
        on_delete=models.CASCADE,
        related_name="courses"
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

    def __str__(self):
        return f'({self.id}) {self.name}'


class LessonDay(models.Model):
    class Meta:
        verbose_name = "День занятия"
        verbose_name_plural = "Дни занятий"

    course = models.ForeignKey(
        Course,
        related_name="lesson_days",
        on_delete=models.CASCADE
    )
    weekday = models.PositiveSmallIntegerField(
        verbose_name="День недели",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(6)
        ]
    )
    start_time = models.TimeField("Время начала")
    end_time = models.TimeField("Время окончания")


class Lesson(FreePlacesMixin, BookedPlacesMixin, TimestampModel):
    class Meta:
        verbose_name = "Занятие"
        verbose_name_plural = "Занятия"

    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        verbose_name="Курс",
        related_name="lessons",
        null=True
    )

    day = models.DateField("День проведения")
    start_time = models.TimeField("Время начала")
    end_time = models.TimeField("Время конца")

    favorite_users = models.ManyToManyField(
        User,
        related_name='favorite_lessons',
        verbose_name='Пользователи (избранное)'
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

        lesson_days = {
            lesson_day.weekday: {
                "start_time": lesson_day.start_time,
                "end_time": lesson_day.end_time
            }
            for lesson_day in cast(Iterable[LessonDay], course.lesson_days.all())
        }

        while start_date <= end_date:
            weekday = start_date.weekday()
            if weekday in lesson_days.keys():
                new_lesson = cls(
                    course=course,
                    day=start_date,
                    start_time=lesson_days[weekday]["start_time"],
                    end_time=lesson_days[weekday]["end_time"],
                    unipass_places=course.unipass_places,
                    uniclass_places=course.uniclass_places,
                    regular_places=course.regular_places,
                )
                new_lesson.save()
            start_date += delta

    def __str__(self):
        return f"Занитие по курсу {self.course.name} " \
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
        verbose_name='Помог'
    )
    not_helped = models.ManyToManyField(
        User,
        related_name='course_not_helped',
        verbose_name='Не помог'
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
