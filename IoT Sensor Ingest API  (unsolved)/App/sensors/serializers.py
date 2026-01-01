# root/App/sensors/serializers.py
from rest_framework import serializers
from .models import SensorDevice, SensorReading

class SensorDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorDevice
        fields = ('id','owner','name','location')
        read_only_fields = ('owner',)

class SensorReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorReading
        fields = ('id','device','temperature','humidity','motion','created_at')
        read_only_fields = ('created_at',)

    def validate_temperature(self, value):
        # allowed temperature range -50..100
        if value is None:
            return value
        if value < -50 or value > 100:
            raise serializers.ValidationError("temperature out of range")
        return value

    def create(self, validated_data):
        # normal create
        return SensorReading.objects.create(**validated_data)
