# progress/serializers.py
from rest_framework import serializers
from .models import StudentProgress
from courses.serializers import LessonSerializer

class ProgressSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(read_only=True)
    
    class Meta:
        model = StudentProgress
        fields = '__all__'
        read_only_fields = ['student', 'course', 'last_accessed']
    
    def validate(self, data):
        if data.get('score') and data['score'] > 100:
            raise serializers.ValidationError("Score cannot exceed 100")
        return data

class ProgressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProgress
        fields = ['is_completed', 'score', 'notes']