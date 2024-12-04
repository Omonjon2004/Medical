from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.account_.models import Users, UserProfile


@receiver(signal=post_save, sender=Users)
def create_account_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

