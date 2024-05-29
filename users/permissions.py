from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    message = "Доступ только для модераторов"

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderators").exists()
