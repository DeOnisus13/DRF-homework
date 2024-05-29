from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    message = "Доступ только для модераторов"

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderators").exists()


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
