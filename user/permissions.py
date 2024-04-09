from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id


class CreateOnly(permissions.BasePermission):
    """
    Allow any one to register a user
    """

    def has_permission(self, request, view):
        return request.method == "POST"
