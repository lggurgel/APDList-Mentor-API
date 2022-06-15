from rest_framework.permissions import BasePermission, SAFE_METHODS


class UpdatePermission(BasePermission):
    """Allow user to edit their own profile."""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return obj.user.id == request.user.id


class IsMentorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return hasattr(request.user, "mentor")
