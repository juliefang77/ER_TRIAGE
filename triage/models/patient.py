from django.db import models
from django.core.exceptions import ValidationError
import re

class Patient(models.Model):
    
    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女'),
    ]

    ID_TYPES = [
        ('ID', '居民身份证'),
        ('PASSPORT', '护照'),
        ('HK_MO', '港澳通行证'),
        ('TW', '台湾通行证'),
        ('FOREIGN', '外国人永久居留证'),
        ('OTHER', '其他证件'),
    ]

    name_chinese = models.CharField(
        max_length=50, 
        verbose_name='姓名',
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

    gender = models.CharField(
        max_length=1, 
        choices=GENDER_CHOICES, 
        default='M', 
        verbose_name='性别',
        null=True, 
        blank=True
    )

    date_of_birth = models.DateField(
        verbose_name='出生日期', 
        null=True, 
        blank=True
    )

    phone = models.CharField(
        max_length=11, 
        verbose_name='电话', 
        null=True, 
        blank=True
    )

    address = models.CharField(
        max_length=200, 
        verbose_name='地址', 
        null=True, 
        blank=True
    )
    
    BLOOD_TYPES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('Unknown', '未知'),
    ]

    blood_type = models.CharField(
        max_length=10,
        choices=BLOOD_TYPES,
        default='Unknown',
        verbose_name='血型',
        null=True, 
        blank=True
    )
    
    emergency_contact = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='紧急联系人'
    )
    
    emergency_phone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name='紧急联系人电话'
    )

    allergies = models.TextField(
        null=True,
        blank=True,
        verbose_name='过敏史'
    )

    def __str__(self):
        name = self.name_chinese or "未知"
        id_num = self.id_number or "无证件号"
        return f"{name} ({id_num})"

    def clean(self):
        # Only validate if both id_type and id_number are provided
        if self.id_type and self.id_number:
            if self.id_type == 'ID':
                if not re.match(r'^\d{17}[\dX]$', self.id_number):
                    raise ValidationError({'id_number': '身份证号码格式不正确'})
            
            elif self.id_type == 'PASSPORT':
                if not re.match(r'^[A-Z]{1,2}\d{7,8}$', self.id_number):
                    raise ValidationError({'id_number': '护照号码格式不正确'})