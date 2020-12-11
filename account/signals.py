from django.dispatch import receiver
from django.contrib.auth.models import User
from account.models import User, UserProfile
from django.db.models.signals import (
    post_save,
)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
