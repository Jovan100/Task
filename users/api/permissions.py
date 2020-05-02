from rest_framework import permissions

class IsAdminOrOwner(permissions.BasePermission):
    message = 'You must be the owner of this object.'

    def has_object_permission(self, request, view, obj):
        try:
            return obj.id == request.user.id or request.user.is_admin
        except:
            return False
