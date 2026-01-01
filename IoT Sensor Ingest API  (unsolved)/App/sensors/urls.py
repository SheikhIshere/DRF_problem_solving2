# root/App/sensors/urls.py
from django.urls import path
from .views import DeviceListCreateView, ReadingCreateView, ReadingListView

urlpatterns = [
    path('devices/', DeviceListCreateView.as_view(), name='device-list-create'),
    path('readings/', ReadingCreateView.as_view(), name='reading-create'),
    path('readings/list/', ReadingListView.as_view(), name='reading-list'),
]
