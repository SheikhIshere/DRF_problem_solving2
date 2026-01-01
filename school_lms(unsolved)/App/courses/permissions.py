# courses/permissions.py
from rest_framework import permissions

class IsTeacherOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['teacher', 'admin']

class IsCourseTeacher(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return obj.course.teacher == request.user