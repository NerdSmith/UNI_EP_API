from rest_framework.permissions import BasePermission


class IsCurator(BasePermission):
    def has_permission(self, request, view):
        if request.user.get_role() == 'curator':
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.get_role() == 'curator':
            return True
        return False
