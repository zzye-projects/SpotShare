from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSuperAdminOrGET(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (view.action in ('list', 'retrieve')) or \
            user.is_superuser or user.is_staff
    
class ParkingPermissions(BasePermission):
    def has_permission(self, request, view):
        return view.action in ('list', 'retrieve') or \
            request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        if view.action in ('destroy', 'partial_update'):
            return obj.lessor == user or user.is_superuser or user.is_staff or \
                user.addresses.filter(pk=obj.address.pk).exists()
        return view.action == 'retrieve'
    
class VehiclePermissions(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.groups.filter(name='Staff').exists():
            return view.action == 'retrieve'
        return user.is_authenticated
