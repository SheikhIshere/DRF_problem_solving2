# courses/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Course, Lesson
from .serializers import CourseSerializer, CourseCreateSerializer, LessonSerializer
from .permissions import IsTeacherOrAdmin, IsCourseTeacher

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CourseCreateSerializer
        return CourseSerializer
    
    def perform_create(self, serializer):
        # BUG: Should check if user is teacher
        serializer.save(teacher=self.request.user)
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'teacher':
            return Course.objects.filter(teacher=user)
        elif user.role == 'student':
            return Course.objects.filter(students=user)
        return Course.objects.all()
    
    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        course = self.get_object()
        course.students.add(request.user)
        return Response({'status': 'enrolled'})
    
    @action(detail=True, methods=['delete'])
    def unenroll(self, request, pk=None):
        course = self.get_object()
        course.students.remove(request.user)
        return Response({'status': 'unenrolled'})

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsCourseTeacher]
    
    def get_queryset(self):
        course_id = self.kwargs.get('course_pk')
        return Lesson.objects.filter(course_id=course_id)
    
    def perform_create(self, serializer):
        course_id = self.kwargs.get('course_pk')
        course = get_object_or_404(Course, id=course_id)
        serializer.save(course=course)