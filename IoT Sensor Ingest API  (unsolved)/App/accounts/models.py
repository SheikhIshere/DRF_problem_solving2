# root/App/accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

def profile_picture_upload_to(instance, filename):
    return f'profiles/{instance.username}/{filename}'

class CustomUser(AbstractUser):
    token_balance = models.IntegerField(default=0)
    profile_picture = models.ImageField(upload_to=profile_picture_upload_to, null=True, blank=True)

    def __str__(self):
        return self.username
