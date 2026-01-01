# root/App/sensors/tests.py
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import CustomUser
from sensors.models import SensorDevice, SensorReading
from rest_framework_simplejwt.tokens import RefreshToken

class SensorAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='tester', password='testpass')
        # create another user to ensure isolation
        self.other = CustomUser.objects.create_user(username='other', password='otherpass')

        self.device = SensorDevice.objects.create(owner=self.user, name='device1', location='lab')
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.auth_header = f'Bearer {self.token}'

    def test_create_reading_requires_auth(self):
        url = reverse('reading-create')
        data = {
            'device': self.device.id,
            'temperature': 25.5,
            'humidity': 40.0,
            'motion': False
        }
        # without auth should be 401
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_reading_success(self):
        url = reverse('reading-create')
        data = {
            'device': self.device.id,
            'temperature': 22.2,
            'humidity': 44.0,
            'motion': True
        }
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header)
        resp = self.client.post(url, data, format='json')
        # test expects creation to return 201
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SensorReading.objects.count(), 1)
        reading = SensorReading.objects.first()
        self.assertAlmostEqual(reading.temperature, 22.2)

    def test_list_readings_filters_by_device(self):
        # create two readings for two devices and ensure filter works
        other_device = SensorDevice.objects.create(owner=self.user, name='device2')
        SensorReading.objects.create(device=self.device, temperature=10)
        SensorReading.objects.create(device=other_device, temperature=20)
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header)
        url = reverse('reading-list') + f'?device={self.device.id}'
        resp = self.client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
