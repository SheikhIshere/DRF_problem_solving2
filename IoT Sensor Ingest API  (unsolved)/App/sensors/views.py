# root/App/sensors/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import SensorDevice, SensorReading
from .serializers import SensorDeviceSerializer, SensorReadingSerializer

class DeviceListCreateView(generics.ListCreateAPIView):
    serializer_class = SensorDeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SensorDevice.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ReadingCreateView(generics.CreateAPIView):
    serializer_class = SensorReadingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Accept single reading POST at /api/sensors/readings/
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():  # <-- intentional bug: missing raise_exception and wrong status
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            # returns 200 OK (should be 201 CREATED). Tests expect 201.
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReadingListView(generics.ListAPIView):
    serializer_class = SensorReadingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        device_id = self.request.query_params.get('device')
        qs = SensorReading.objects.filter(device__owner=self.request.user)
        if device_id:
            qs = qs.filter(device_id=device_id)
        return qs
"""
Note: The ReadingCreateView.create() currently returns 200 OK for a successful creation. Tests are written expecting 201 CREATED — this will make tests fail (you will find and fix it).
"""