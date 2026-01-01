# courses/serializers.py
from rest_framework import serializers
from .models import Course, Lesson
from users.serializers import UserSerializer

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class CourseSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)
    students = UserSerializer(many=True, read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'teacher']

class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'description', 'code', 'start_date', 'end_date']
    
    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("Start date must be before end date")
        return data