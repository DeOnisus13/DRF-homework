from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from config.settings import NULLABLE
from lms_app.models import Course, Lesson


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


class Payment(models.Model):
    """Модель платежей"""

    PAYMENT_METHOD_CHOICES = {"cash": "Наличные", "card": "Перевод на счет"}

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="user")
    payment_date = models.DateTimeField(default=timezone.now, **NULLABLE, verbose_name="Дата оплаты")
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Оплаченный курс")
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Оплаченный урок")
    payment_amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    payment_method = models.CharField(max_length=15, choices=PAYMENT_METHOD_CHOICES, verbose_name="Способ оплаты")

    def __str__(self):
        return f"{self.user} - {self.payment_amount}р. - {self.course if self.course else self.lesson}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
