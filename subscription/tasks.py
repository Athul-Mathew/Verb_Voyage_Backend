# tasks.py

from celery import shared_task
from datetime import datetime, timedelta
from Accounts.models import UserAccount
from django.utils import timezone


@shared_task
def check_subscription_expiration():
    users_to_check = UserAccount.objects.filter(is_premium=True)

    for user in users_to_check:
        if user.remaining_subscription_days is not None:
            # Calculate remaining days based on the remaining_subscription_days
            remaining_days = user.remaining_subscription_days - 1

            # If there are no remaining days, set the user's premium status to False
            if remaining_days <= 0:
                user.is_premium = False
                user.remaining_subscription_days = 0  # Reset to 0
            else:
                # Update the user's remaining subscription days
                user.remaining_subscription_days = remaining_days

            user.save()