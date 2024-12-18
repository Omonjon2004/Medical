from rest_framework import permissions


class IsDoctorReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'DOCTOR' or request.user.role == 'ADMIN':
            return True
        return False


class IsPatientReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'PATIENT' or request.user.role == 'ADMIN':
            return True
        return False


class IsAdminReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if hasattr(request.user, 'role') and request.user.role == 'ADMIN':
            return True

        if request.user.is_superuser:
            return True

        return False
