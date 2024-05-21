from rest_framework.serializers import ModelSerializer, SerializerMethodField

from lms_app.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    """Сериализатор для уроков"""

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
