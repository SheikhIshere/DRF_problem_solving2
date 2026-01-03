from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Patient(models.Model):
    # FIX: adding patient user relationship
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('U', 'Prefer not to say'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField(blank=True)
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
        blank=True
    )
    email = models.EmailField(blank=True)
    emergency_contact = models.CharField(max_length=200, blank=True)
    blood_type = models.CharField(max_length=5, blank=True)
    allergies = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_patients')
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['date_of_birth']),
        ]


class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_histories')
    diagnosis = models.TextField()
    treatment = models.TextField()
    date = models.DateField()
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='medical_histories')
    notes = models.TextField(blank=True)
    prescription = models.TextField(blank=True)
    follow_up_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.patient} - {self.diagnosis[:50]}"
    
    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name_plural = 'Medical Histories'


class DoctorNote(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='doctor_notes')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_notes')
    note = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_urgent = models.BooleanField(default=False)
    category = models.CharField(max_length=50, default='General')
    
    def __str__(self):
        return f"Note by {self.doctor} for {self.patient}"
    
    class Meta:
        ordering = ['-date']