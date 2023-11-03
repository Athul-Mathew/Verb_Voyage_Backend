# tasks.py

from celery import shared_task
from django.utils import timezone
from .models import UserAccount

@shared_task
def update_subscription_status():
    # Get all user accounts with remaining days greater than 0
    users_with_remaining_days = UserAccount.objects.filter(remaining_subscription_days__gt=0)

    for user in users_with_remaining_days:
        # Decrement the remaining days by 1
        user.remaining_subscription_days -= 1

        # Check if remaining days have reached 0
        if user.remaining_subscription_days == 0:
            user.is_premium = False

        user.save()
