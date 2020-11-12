from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        username = view.kwargs.get('username', None)
        if username is None:
            return False
        return request.user.username == username


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user and request.data.owner != request.user
