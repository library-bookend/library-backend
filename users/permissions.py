from rest_framework import permissions


class isEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        request_method = ["POST"]
        return (
            request.method in permissions.SAFE_METHODS
            and request.user.is_superuser
            or request.method in request_method
        )
    
class IsEmployeeOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.employee == request.user