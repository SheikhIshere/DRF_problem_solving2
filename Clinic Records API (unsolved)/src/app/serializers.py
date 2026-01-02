from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Patient, MedicalHistory, DoctorNote


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']
        # FIX: for security never use admin stuff for user
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class PatientSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    def get_age(self, obj):
        import datetime
        today = datetime.date.today()
        return today.year - obj.date_of_birth.year - (
            (today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day)
        )
    
    def validate_email(self, value):
        if value and Patient.objects.filter(email=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("A patient with this email already exists.")
        return value


class MedicalHistorySerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.get_full_name', read_only=True)
    
    class Meta:
        model = MedicalHistory
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_follow_up_date(self, value):
        if value and value < self.initial_data.get('date'):
            raise serializers.ValidationError("Follow-up date cannot be before the diagnosis date.")
        return value


class DoctorNoteSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.get_full_name', read_only=True)
    
    class Meta:
        model = DoctorNote
        fields = '__all__'
        read_only_fields = ['date']
    
    def validate(self, data):
        if not data.get('note', '').strip():
            raise serializers.ValidationError({"note": "Note cannot be empty."})
        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user