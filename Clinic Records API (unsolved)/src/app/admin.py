from django.contrib import admin
from .models import Patient, MedicalHistory, DoctorNote


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'date_of_birth', 'gender', 'email']
    list_filter = ['gender', 'blood_type']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ['patient', 'diagnosis', 'date', 'doctor']
    list_filter = ['date', 'doctor']
    search_fields = ['patient__first_name', 'patient__last_name', 'diagnosis']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(DoctorNote)
class DoctorNoteAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'date', 'is_urgent']
    list_filter = ['is_urgent', 'category', 'doctor']
    search_fields = ['patient__first_name', 'patient__last_name', 'note']