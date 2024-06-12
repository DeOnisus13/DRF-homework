from django.shortcuts import get_object_or_404
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from lms_app.models import Course, Lesson, Subscription
from lms_app.paginators import LMSPaginator
from lms_app.serializers import CourseSerializer, LessonSerializer
from lms_app.tasks import update_course_mail
from users.permissions import IsModerator, IsOwner


class CourseViewSet(ModelViewSet):
    """ViewSet для модели курсов"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = LMSPaginator

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModerator,)
        elif self.action in ["list", "retrieve", "update"]:
            self.permission_classes = (IsModerator | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (IsOwner,)
        return [permission() for permission in self.permission_classes]

    def perform_update(self, serializer):
        instance = serializer.save()
        recipients = instance.course_subscription.values_list("user__email", flat=True)
        update_course_mail.delay(list(recipients), instance.name)


class LessonCreateAPIView(CreateAPIView):
    """Generic-класс для создания урока"""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(ListAPIView):
    """Generic-класс для вывода списка уроков"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner,]
    pagination_class = LMSPaginator


class LessonRetrieveAPIView(RetrieveAPIView):
    """Generic-класс для вывода одного урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner,]


class LessonUpdateAPIView(UpdateAPIView):
    """Generic-класс для редактирования урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(DestroyAPIView):
    """Generic-класс для удаления урока"""
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class SubscriptionAPIView(APIView):
    """Класс представления для добавления/удаления подписки на курс"""
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)
        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"
        return Response({"message": message})
