from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        username = view.kwargs.get('username', None)
        if username is None:
            return False
        return request.user.username == username

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.profile == obj


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner != request.user:
            return False
        if request.method == 'PUT':
            return request.data['owner'] == request.user.id
        return True

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.data['owner'] == request.user.id
        return True
