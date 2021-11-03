from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import LessonBooking
from apps.products import ProductType


@receiver(post_save, sender=LessonBooking)
def booking_saved(sender, instance, created, **kwargs):
    if created:
        lesson = instance.lesson
        if instance.subscription.product.product_type == ProductType.UNIPASS:
            lesson.unipass_clients += 1
        elif instance.subscription.product.product_type == ProductType.UNICLASS:
            lesson.uniclass_clients += 1
        lesson.regular_clients += 1
        lesson.save()


@receiver(pre_delete, sender=LessonBooking)
def booking_pre_delete(sender, instance, created, **kwargs):
    lesson = instance.lesson
    if instance.subscription.product.product_type == ProductType.UNIPASS:
        lesson.unipass_clients -= 1
    elif instance.subscription.product.product_type == ProductType.UNICLASS:
        lesson.uniclass_clients -= 1
    lesson.regular_clients -= 1
    lesson.save()
