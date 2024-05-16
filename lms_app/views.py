from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.viewsets import ModelViewSet

from lms_app.models import Course, Lesson
from lms_app.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(ModelViewSet):
    """ViewSet для модели курсов"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonCreateAPIView(CreateAPIView):
    """Generic-класс для создания урока"""
    serializer_class = LessonSerializer


class LessonListAPIView(ListAPIView):
    """Generic-класс для вывода списка уроков"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(RetrieveAPIView):
    """Generic-класс для вывода одного урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateAPIView(UpdateAPIView):
    """Generic-класс для редактирования урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyAPIView(DestroyAPIView):
    """Generic-класс для удаления урока"""
    queryset = Lesson.objects.all()
