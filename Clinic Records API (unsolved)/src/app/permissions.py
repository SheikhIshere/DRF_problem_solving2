from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Doctors').exists()


class IsPatientOwnerOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.created_by == request.user


class IsMedicalHistoryOwnerOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.doctor == request.user


class IsDoctorNoteOwnerOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.doctor == request.user


class CanAccessPatientRecords(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if hasattr(obj, 'patient'):
            return obj.patient.created_by == request.user
        return False