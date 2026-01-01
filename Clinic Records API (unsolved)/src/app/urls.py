from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'patients', views.PatientViewSet)
router.register(r'medical-histories', views.MedicalHistoryViewSet)
router.register(r'doctor-notes', views.DoctorNoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', views.UserRegistrationView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', views.UserProfileView.as_view(), name='user_profile'),
]