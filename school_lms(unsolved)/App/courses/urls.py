# courses/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet

router = DefaultRouter()
router.register(r'', CourseViewSet, basename='course')

lesson_router = DefaultRouter()
lesson_router.register(r'', LessonViewSet, basename='lesson')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:course_pk>/lessons/', include(lesson_router.urls)),
]