from django.urls import path
from rest_framework.routers import DefaultRouter

from lms_app.apps import LmsAppConfig
from lms_app.views import (CourseViewSet, LessonCreateAPIView,
                           LessonDestroyAPIView, LessonListAPIView,
                           LessonRetrieveAPIView, LessonUpdateAPIView)

app_name = LmsAppConfig.name

router = DefaultRouter()
router.register(r"course", CourseViewSet, basename="courses")

urlpatterns = [
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lessons/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_get"),
    path("lessons/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson_update"),
    path("lessons/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson_delete"),
] + router.urls
