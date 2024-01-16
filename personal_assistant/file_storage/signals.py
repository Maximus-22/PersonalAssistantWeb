
"""
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .aws import create_user_folder


@receiver(post_save, sender=User)
def create_s3_folders(sender, instance, created, **kwargs):
    if created:
        create_user_folder(instance.id)
"""