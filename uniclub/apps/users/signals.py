from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from . import UserTypes

User = get_user_model()


@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created and instance.user_type == UserTypes.PARTNER:
        from apps.clubs.models import Club
        Club.objects.create(club_admin=instance)
