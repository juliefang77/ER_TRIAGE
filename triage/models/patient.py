from django.db import models
from django.core.exceptions import ValidationError
import re

class Patient(models.Model):
    
    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女'),
    ]

    # Basic identification
    ID_TYPES = [
        ('ID', '居民身份证'),
        ('PASSPORT', '护照'),
        ('HK_MO', '港澳通行证'),
        ('TW', '台湾通行证'),
        ('FOREIGN', '外国人永久居留证'),
        ('OTHER', '其他证件'),
    ]

    id_type = models.CharField(
        max_length=10,
        choices=ID_TYPES,
        default='ID',
        verbose_name='证件类型'
    )
    id_number = models.CharField(max_length=18, verbose_name='证件号码', null=True, blank=True)
    name_chinese = models.CharField(max_length=50, verbose_name='姓名', null=True, blank=True)
    pinyin_name = models.CharField(max_length=100, verbose_name='拼音', null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', verbose_name='性别')
    date_of_birth = models.DateField(verbose_name='出生日期', null=True, blank=True)
    phone = models.CharField(max_length=11, verbose_name='电话', null=True, blank=True)
    address = models.CharField(max_length=200, verbose_name='地址', null=True, blank=True)
    
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

    # New fields
    blood_type = models.CharField(
        max_length=10,
        choices=BLOOD_TYPES,
        default='Unknown',
        verbose_name='血型'
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
        return f"{self.name_chinese or '未知'} ({self.id_number or '无证件号'})"

    def clean(self):
        # Validate ID number format based on ID type
        if self.id_type == 'ID':
            # 身份证号码: 18位数字，最后一位可能是X
            if not re.match(r'^\d{17}[\dX]$', self.id_number):
                raise ValidationError({'id_number': '身份证号码格式不正确'})
        
        elif self.id_type == 'PASSPORT':
            # 护照号码: 1-2个字母 + 7-8个数字
            if not re.match(r'^[A-Z]{1,2}\d{7,8}$', self.id_number):
                raise ValidationError({'id_number': '护照号码格式不正确'})