from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Club
from .tasks import remove_new


@receiver(post_save, sender=Club)
def club_saved(sender, instance, created=True, **kwargs):
    if created:
        remove_new.apply_async(args=[instance.id], eta=(timezone.now() + timezone.timedelta(days=10)))
