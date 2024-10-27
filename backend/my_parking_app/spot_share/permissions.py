from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSuperAdminOrGET(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (view.action in ('list', 'retrieve')) or \
            user.is_superuser or user.is_staff
    
class IsOwnerStaffAdminSuperOrGETOrPOST(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        return (view.action in ('list', 'retrieve', 'create')) or \
            obj.lessor == user or user.is_superuser or \
            user.is_staff or (user.groups.filter(name='Staff').exists() and \
                              obj.address in user.addresses.all())