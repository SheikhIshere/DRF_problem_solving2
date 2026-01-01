# progress/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProgressViewSet

router = DefaultRouter()
router.register(r'', ProgressViewSet, basename='progress')

urlpatterns = [
    path('<int:course_pk>/', include(router.urls)),
    path('<int:course_pk>/overview/', ProgressViewSet.as_view({'get': 'overview'}), name='progress-overview'),
]