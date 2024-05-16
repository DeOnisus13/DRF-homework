from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import NULLABLE


class User(AbstractUser):
    """Модель пользователя"""

    username = None
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Введите свой email")
    phone = models.CharField(max_length=35, **NULLABLE, verbose_name="Телефон")
    city = models.CharField(max_length=50, **NULLABLE, verbose_name="Город")
    avatar = models.ImageField(upload_to="users/", **NULLABLE, verbose_name="Аватарка")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
