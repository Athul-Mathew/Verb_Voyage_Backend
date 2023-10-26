# your_app/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import models
from .models import Mentor, Notification

@receiver(post_save, sender=Mentor)
def mentor_approval_notification(sender, instance, created, **kwargs):
    if created and instance.is_active:
        # Create a notification when a mentor request is approved
        Notification.objects.create(
            user=instance.user,
            verb='Mentor Registration Approved'
        )
