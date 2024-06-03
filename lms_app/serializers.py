from rest_framework.serializers import ModelSerializer, SerializerMethodField, URLField

from lms_app.models import Course, Lesson
from lms_app.validators import validate_video_link


class LessonSerializer(ModelSerializer):
    """Сериализатор для уроков"""
    video_link = URLField(validators=[validate_video_link], allow_null=True, allow_blank=True)

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    """Сериализатор для курсов"""

    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(source="lesson", many=True, read_only=True)
    is_subscribed = SerializerMethodField()

    def get_lessons_count(self, obj):
        return obj.lesson.all().count()

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        user = None
        if request:
            user = request.user
        return obj.subscription_set.filter(user=user).exists()

    class Meta:
        model = Course
        fields = "__all__"
