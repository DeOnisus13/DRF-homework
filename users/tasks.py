from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def check_users_active():
    """Блокировка пользователя, если он не логинился более 31 дня"""
    users = User.objects.exclude(last_login__isnull=True)
    now = timezone.now()
    for user in users:
        if now - user.last_login > timedelta(days=31):
            user.is_active = False
            user.save()
