# patient_portal/models/patient_user.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from triage.models import Patient

class PatientUser(AbstractUser):

    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女'),
    ]
    ID_TYPES = [
        ('ID', '居民身份证'),
        ('HUKOU', '居民户口本'),
        ('HMT', '港澳台居民来往内地通行证'),
        ('PERMANENT', '外国人永久居留证'),
        ('PASSPORT', '护照'),
        ('MILITARY', '军官证')
    ]
    
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
    gender = models.CharField(
        max_length=1, 
        choices=GENDER_CHOICES, 
        default='M', 
        verbose_name='性别',
        null=True, 
        blank=True
    )
    id_type = models.CharField(
        max_length=10,
        choices=ID_TYPES,
        default='ID',
        verbose_name='证件类型',
        null=True,
        blank=True
    )
    id_number = models.CharField(
        max_length=18, 
        verbose_name='证件号码',
        null=True,
        blank=True
    )
    id_medical_insurance = models.CharField(
        max_length=16,
        verbose_name='医保卡号',
        null=True,
        blank=True
    )
    profile_picture = models.IntegerField(
        verbose_name='头像',
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