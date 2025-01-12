from django.db.models.signals import post_save
from django.dispatch import receiver
from triage.models import Patient
from .models import PatientUser

@receiver(post_save, sender=Patient)
def link_patient_to_user(sender, instance, created, **kwargs):
    if created:
        try:
            patient_user = PatientUser.objects.get(phone=instance.patient_phone)
            if instance.patient_user != patient_user:
                instance.patient_user = patient_user
                instance.save()
        except PatientUser.DoesNotExist:
            pass