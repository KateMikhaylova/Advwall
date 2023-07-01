from rest_framework.permissions import BasePermission


class IsUser(BasePermission):
    """
    Allows authenticated user access to corresponding user instance.
    """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return request.user == obj
