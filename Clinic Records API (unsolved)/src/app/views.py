from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from .models import Patient, MedicalHistory, DoctorNote
from .serializers import (
    PatientSerializer, MedicalHistorySerializer, DoctorNoteSerializer,
    UserSerializer, UserRegistrationSerializer
)
from .permissions import (
    IsAdminOrReadOnly, IsDoctor, IsPatientOwnerOrStaff,
    IsMedicalHistoryOwnerOrStaff, IsDoctorNoteOwnerOrStaff, CanAccessPatientRecords
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filterset_fields = ['username', 'email', 'is_staff']


class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsPatientOwnerOrStaff]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['gender', 'blood_type']
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Patient.objects.all()
        return Patient.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def medical_history(self, request, pk=None):
        patient = self.get_object()
        medical_history = patient.medical_histories.all()
        serializer = MedicalHistorySerializer(medical_history, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def doctor_notes(self, request, pk=None):
        patient = self.get_object()
        doctor_notes = patient.doctor_notes.all()
        serializer = DoctorNoteSerializer(doctor_notes, many=True)
        return Response(serializer.data)


class MedicalHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = MedicalHistorySerializer
    permission_classes = [IsAuthenticated, IsMedicalHistoryOwnerOrStaff | CanAccessPatientRecords]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['patient', 'doctor', 'date']
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return MedicalHistory.objects.all()
        elif self.request.user.groups.filter(name='Doctors').exists():
            return MedicalHistory.objects.filter(doctor=self.request.user)
        else:
            return MedicalHistory.objects.filter(patient__created_by=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)


class DoctorNoteViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorNoteSerializer
    permission_classes = [IsAuthenticated, IsDoctorNoteOwnerOrStaff | CanAccessPatientRecords]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['patient', 'doctor', 'is_urgent', 'category']
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return DoctorNote.objects.all()
        elif self.request.user.groups.filter(name='Doctors').exists():
            return DoctorNote.objects.filter(doctor=self.request.user)
        else:
            return DoctorNote.objects.filter(patient__created_by=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }
        return Response(data, status=status.HTTP_201_CREATED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user