from django.conf import settings
from django.db import models

from config.settings import NULLABLE


class Course(models.Model):
    """Модель курса"""

    name = models.CharField(max_length=100, verbose_name="Название")
    preview = models.ImageField(upload_to="lms_app/", **NULLABLE, verbose_name="Превью")
    description = models.TextField(**NULLABLE, verbose_name="Описание")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Владелец")
    price = models.PositiveIntegerField(default=0, verbose_name="Цена курса")

    def __str__(self):
        return f"{self.name} - {self.price} - {self.owner}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ("id",)


class Lesson(models.Model):
    """Модель урока"""

    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(**NULLABLE, verbose_name="Описание")
    preview = models.ImageField(upload_to="lms_app/", **NULLABLE, verbose_name="Превью")
    video_link = models.URLField(max_length=200, **NULLABLE, verbose_name="Ссылка на видео")
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Курс",
                               related_name="lesson")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Владелец")

    def __str__(self):
        return f"{self.name} - {self.course}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ("id",)


class Subscription(models.Model):
    """Модель подписки пользователя на курс"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name="Подписчик",
                             related_name="course_subscription")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, verbose_name="Курс",
                               related_name="course_subscription")

    def __str__(self):
        return f"{self.course} - {self.user}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ("id",)
