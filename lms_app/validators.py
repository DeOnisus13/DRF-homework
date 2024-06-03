from rest_framework.serializers import ValidationError


def validate_video_link(value):
    if not value.startswith("https://www.youtube.com/"):
        raise ValidationError(
            "В поле 'video_link' присутствует запрещенная ссылка. Допускаются только ссылки на https://youtube.com/")
