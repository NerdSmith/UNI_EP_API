from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCurator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.get_role() == 'curator'

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.get_role() == 'curator'


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class CurrentUserOrAdmin(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        user = request.user
        user_w_role = request.user.get_related_role()
        return user.is_staff or (user_w_role and obj.pk == user_w_role.pk)
