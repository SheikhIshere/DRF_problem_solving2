from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi

# schema_view = get_schema_view(
#     openapi.Info(
#         title="Clinic Records API",
#         default_version='v1',
#         description="API for managing clinic records",
#         terms_of_service="https://www.google.com/policies/terms/",
#         contact=openapi.Contact(email="contact@clinic.local"),
#         license=openapi.License(name="BSD License"),
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('app.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]