from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, User
from .models import Patient


@receiver(post_save, sender=User)
def assign_default_group(sender, instance, created, **kwargs):
    if created and not instance.is_staff:
        group, _ = Group.objects.get_or_create(name='Patients')
        instance.groups.add(group)


@receiver(post_save, sender=Patient)
def log_patient_creation(sender, instance, created, **kwargs):
    if created:
        print(f"New patient created: {instance.first_name} {instance.last_name}")