from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied

class IsSuperAdminOrGET(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method == 'GET' or user.is_superuser or user.is_staff:
            return True
        return False