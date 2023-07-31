from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCurator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.get_role() == 'curator'

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.get_role() == 'curator'


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
