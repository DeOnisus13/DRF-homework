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
    lessons = LessonSerializer(source="lesson", many=True)

    def get_lessons_count(self, obj):
        return obj.lesson.all().count()

    class Meta:
        model = Course
        fields = "__all__"
