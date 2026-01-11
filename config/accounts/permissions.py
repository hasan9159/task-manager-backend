from rest_framework.permissions import BasePermission

class IsTaskOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        # ADMIN can access everything
        if user.role == 'ADMIN':
            return True

        # INTERN can access ONLY assigned tasks
        return obj.assigned_to == user
