from django.db import models

from config.settings import NULLABLE


class Course(models.Model):
    """Модель курса"""

    name = models.CharField(max_length=100, verbose_name="Название")
    preview = models.ImageField(upload_to="lms_app/", **NULLABLE, verbose_name="Превью")
    description = models.TextField(**NULLABLE, verbose_name="Описание")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    """Модель урока"""

    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(**NULLABLE, verbose_name="Описание")
    preview = models.ImageField(upload_to="lms_app/", **NULLABLE, verbose_name="Превью")
    video_link = models.URLField(max_length=200, **NULLABLE, verbose_name="Ссылка на видео")
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Курс")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
