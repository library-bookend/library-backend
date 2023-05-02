from rest_framework import permissions


class isEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        request_method = ["POST"]
        return (
            request.method in permissions.SAFE_METHODS
            and request.user.is_superuser
            or request.method in request_method
        )
