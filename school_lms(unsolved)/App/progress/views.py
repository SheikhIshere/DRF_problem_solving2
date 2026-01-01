# progress/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import StudentProgress
from .serializers import ProgressSerializer, ProgressUpdateSerializer
from courses.models import Course, Lesson

class ProgressViewSet(viewsets.ModelViewSet):
    serializer_class = ProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        course_id = self.kwargs.get('course_pk')
        
        if user.role == 'teacher':
            # Teachers can see all progress for their courses
            return StudentProgress.objects.filter(course__teacher=user, course_id=course_id)
        else:
            # Students can only see their own progress
            return StudentProgress.objects.filter(student=user, course_id=course_id)
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return ProgressUpdateSerializer
        return ProgressSerializer
    
    def perform_create(self, serializer):
        course_id = self.kwargs.get('course_pk')
        lesson_id = self.kwargs.get('lesson_pk')
        
        course = get_object_or_404(Course, id=course_id)
        lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
        
        serializer.save(student=self.request.user, course=course, lesson=lesson)
    
    @action(detail=False, methods=['get'])
    def overview(self, request, course_pk=None):
        progress = self.get_queryset()
        completed = progress.filter(is_completed=True).count()
        total = Lesson.objects.filter(course_id=course_pk).count()
        
        if total > 0:
            percentage = (completed / total) * 100
        else:
            percentage = 0
            
        return Response({
            'completed': completed,
            'total': total,
            'percentage': percentage
        })