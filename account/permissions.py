from rest_framework import permissions
from .models import RequestModel


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        username = view.kwargs.get('username', None)
        if username is None:
            return True
        return request.user.username == username

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.profile == obj


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner != request.user:
            return False
        if request.data:
            return request.data['owner'] == request.user.id
        return True

    def has_permission(self, request, view):
        if request.data:
            return request.data['owner'] == request.user.id
        return True


class RequestPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.data:
            if request.method == 'POST':
                return request.data['source'] == request.user.id
        elif request.method == 'PUT':
            req_id = view.kwargs.get('pk', None)
            if req_id is None:
                return True
            target_id = RequestModel.objects.get(id=req_id).target
            return target_id == request.user
        return True
