# root/App/sensors/admin.py
from django.contrib import admin
from .models import SensorDevice, SensorReading

admin.site.register(SensorDevice)
admin.site.register(SensorReading)
