from .models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    """
    Create a profile for every new user
    Args:
        sender (object): Detects when a new User
        entry is created on the database

        created (Bool): determines if the user is
        being created and creates a profile
    """
    if created:
        Profile.objects.create(user=instance)
