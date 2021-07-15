from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.role == 'admin' or request.user.is_superuser


class IsModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role == 'moderator'


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsSuperUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if (not request.user.is_superuser and
                request.method not in permissions.SAFE_METHODS):
            return False
        return not (
                request.user.is_anonymous
                and request.method not in permissions.SAFE_METHODS
        )
