from django.db import models
from django.conf import settings
import binascii
import os

class PatientToken(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    user = models.OneToOneField(
        'patient_portal.PatientUser',
        related_name='auth_token',
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @staticmethod
    def generate_key():
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key