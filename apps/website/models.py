from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.grades.models import LessonDay


class FAQ(models.Model):
    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ"

    question = models.CharField("Вопрос", max_length=256)
    answer = models.TextField("Ответ")

    def __str__(self):
        return self.question


class FeedBack(models.Model):
    class Meta:
        verbose_name = "Вопросы пользователей"
        verbose_name_plural = "Вопросы пользователей"

    name = models.CharField("Имя", max_length=256)
    email = models.EmailField("e-mail")
    question = models.TextField("Вопрос")

    def __str__(self):
        return self.name


class PartnerFeedBack(models.Model):
    class Meta:
        verbose_name = "Заявки на партнерство"
        verbose_name_plural = "Заявки на партнерство"

    name = models.CharField("Имя", max_length=256)
    company_name = models.CharField("Название компании", max_length=256, null=True, blank=False)
    email = models.EmailField("e-mail", null=True, blank=True)
    mobile_phone = PhoneNumberField("Мобильный телефон", null=True, blank=True)

    def __str__(self):
        return f"{self.name}({self.company_name})"


class BookingApplication(models.Model):
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    phone_number = PhoneNumberField('Номер телефона')
    email = models.EmailField('Email')
    lesson_days = models.ManyToManyField(
        LessonDay,
        related_name='appilcations',
        verbose_name='Время занятий'
    )

    class Meta:
        verbose_name = 'Заявка на бронирование'
        verbose_name_plural = 'Заявки на бронирование'

    def __str__(self):
        return f'({self.id}) {self.first_name} {self.last_name}'
