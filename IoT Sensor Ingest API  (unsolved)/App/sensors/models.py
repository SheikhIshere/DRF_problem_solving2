# root/App/sensors/models.py
from django.db import models
from django.conf import settings

class SensorDevice(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='devices')
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.name} ({self.owner})"

class SensorReading(models.Model):
    device = models.ForeignKey(SensorDevice, on_delete=models.CASCADE, related_name='readings')
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    motion = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
