# patient_portal/models/patient_user.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from triage.models import Patient

class PatientUser(AbstractUser):

    phone = models.CharField(
        max_length=20, 
        unique=True,
        verbose_name='手机号',
        null=True,
        blank=True
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='用户名',
        null=True,
        blank=True
    )

    is_verified = models.BooleanField(
        default=False,
        verbose_name='是否验证',
        null=True,
        blank=True
    )

    date_of_birth = models.DateField(
        verbose_name='出生日期',
        null=True,
        blank=True
    )
    
    # Make inherited fields nullable/blankable
    first_name = models.CharField(max_length=150, null=True, blank=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    
    # Remove unused fields from AbstractUser
    is_staff = None
    is_superuser = None
    groups = None
    user_permissions = None
    last_name = None
    email = None
    
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    @property
    def patient(self):
        """Get associated Patient record"""
        return Patient.objects.filter(patient_user=self).first()

    class Meta:
        verbose_name = '患者用户'
        verbose_name_plural = '患者用户'