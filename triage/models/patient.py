from django.db import models
from django.core.exceptions import ValidationError
import re
import uuid

class Patient(models.Model):
    
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

    INSURANCE_TYPES = [
        ('SELF', '自费'),
        ('PUBLIC', '公费'),
        ('MEDICAL', '医保'),
        ('COMMERCIAL', '商保'),
        ('EMPLOYEE', '本院职工'),
        ('EMPLOYEE_FAMILY', '职工家属'),
        ('OTHER_REGION', '异地医保'),
        ('NEW_RURAL', '新农合'),
        ('URBAN_RURAL', '城乡医保'),
        ('FIVE_SPECIAL', '五保特困'),
        ('LOW_INCOME', '低保'),
        ('MILITARY', '军烈'),
        ('EARTHQUAKE_512', '512地震'),
        ('MINOR_INJURY', '轻轨工伤'),
        ('RAILWAY', '铁路医保'),
        ('ROAD_FUND', '道路基金'),
        ('DISABILITY', '复员伤残'),
        ('DISABLED', '残疾'),
        ('SPONSOR', '担保'),
        ('HOMELESS', '无主病人'),
        ('LEAVE', '离休'),
        ('WORK_INJURY', '工伤'),
        ('CAR_INJURY', '车伤'),
        ('MATERNITY', '生育'),
        ('SPECIAL', '特约')
    ]

    PATIENT_TYPES = [
        ('THREE_NO', '三无人员'),
        ('LOW_INCOME', '低保户'),
        ('SPECIAL_POVERTY', '特困户'),
        ('CARD_POVERTY', '建卡贫困户'),
        ('FIVE_GUARANTEE', '五保户'),
        ('MILITARY_8023', '8023部队'),
        ('ACTIVE_MILITARY', '现役军人'),
        ('RETIRED_MILITARY', '退伍军人'),
        ('ORPHANED', '失独人员')
    ]

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

    # Add UUID as primary key
    id_system = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='唯一标识'
    )

    patient_user = models.ForeignKey(
        'patient_portal.PatientUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='patients'  # Now one user can have multiple patients
    )

    # used for integrating with other HIS softwares
    id_his = models.CharField(
        max_length=50,
        verbose_name='HIS系统ID',
        null=True,
        blank=True
    ) 
    
    # Add hospital relationship
    hospital = models.ForeignKey(
        'HospitalUser',
        on_delete=models.CASCADE,
        related_name='patients',
        verbose_name='所属医院',
        null=True, # Nullable for now
        blank=True
    )

    name_patient = models.CharField(
        max_length=50, 
        verbose_name='姓名',
        null=True,
        blank=True
    )


    pinyin_name = models.CharField(
        max_length=100,
        verbose_name='拼音姓名',
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

    age = models.IntegerField(
        verbose_name='年龄',
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

    nationality = models.CharField(
        max_length=50,
        verbose_name='国籍',
        null=True,
        blank=True
    )

    ethinicity = models.CharField(
        max_length=50,
        verbose_name='民族',
        null=True,
        blank=True
    )

    profession = models.CharField(
        max_length=100,
        verbose_name='职业',
        null=True,
        blank=True
    )

    id_medical_insurance = models.CharField(
        max_length=16,
        verbose_name='医保卡号',
        null=True,
        blank=True
    )

    id_social_insurance = models.CharField(
        max_length=9,
        verbose_name='社保卡号',
        null=True,
        blank=True
    )

    id_hospital_card = models.CharField(
        max_length=50,
        verbose_name='诊疗卡号',
        null=True,
        blank=True
    )

    insurance_type = models.CharField(
        max_length=20,
        choices=INSURANCE_TYPES,
        default='SELF',
        verbose_name='费别',
        null=True,
        blank=True
    )

    patient_phone = models.CharField(
        max_length=11, 
        verbose_name='电话', 
        null=True, 
        blank=True
    )

    patient_address = models.CharField(
        max_length=200, 
        verbose_name='地址', 
        null=True, 
        blank=True
    )

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

    emergency_relation = models.CharField(
        max_length=50,
        verbose_name='紧急联系人关系',
        null=True,
        blank=True
    )

    patient_type = models.CharField(
        max_length=20,
        choices=PATIENT_TYPES,
        default='THREE_NO',
        verbose_name='身份标识',
        null=True,
        blank=True
    )

    allergies = models.TextField(
        null=True,
        blank=True,
        verbose_name='过敏史'
    )

    def __str__(self):
        name = self.name_patient or "未知"
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



# Fields:
# 1. id_system | 唯一标识 | UUIDField (primary key)
# 2. id_his | HIS系统ID | CharField
# 3. name_patient | 姓名 | CharField
# 4. pinyin_name | 拼音姓名 | CharField
# 5. gender | 性别 | CharField (choices: "M", "F")
# 6. date_of_birth | 出生日期 | DateField
# 7. age | 年龄 | IntegerField
# 8. id_type | 证件类型 | CharField (choices: "ID", "HUKOU", "HMT", "PERMANENT", "PASSPORT", "MILITARY")
# 9. id_number | 证件号码 | CharField
# 10. nationality | 国籍 | CharField
# 11. ethinicity | 民族 | CharField
# 12. profession | 职业 | CharField
# 13. id_medical_insurance | 医保卡号 | CharField
# 14. id_social_insurance | 社保卡号 | CharField
# 15. id_hospital_card | 诊疗卡号 | CharField
# 16. insurance_type | 费别 | CharField (choices: "SELF", "PUBLIC", "MEDICAL", "COMMERCIAL", "EMPLOYEE", "EMPLOYEE_FAMILY", "OTHER_REGION", "NEW_RURAL", "URBAN_RURAL", "FIVE_SPECIAL", "LOW_INCOME", "MILITARY", "EARTHQUAKE_512", "MINOR_INJURY", "RAILWAY", "ROAD_FUND", "DISABILITY", "DISABLED", "SPONSOR", "HOMELESS", "LEAVE", "WORK_INJURY", "CAR_INJURY", "MATERNITY", "SPECIAL")
# 17. patient_phone | 电话 | CharField
# 18. patient_address | 地址 | CharField
# 19. blood_type | 血型 | CharField (choices: "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Unknown")
# 20. emergency_contact | 紧急联系人 | CharField
# 21. emergency_phone | 紧急联系人电话 | CharField
# 22. emergency_relation | 紧急联系人关系 | CharField
# 23. patient_type | 身份标识 | CharField (choices: "THREE_NO", "LOW_INCOME", "SPECIAL_POVERTY", "CARD_POVERTY", "FIVE_GUARANTEE", "MILITARY_8023", "ACTIVE_MILITARY", "RETIRED_MILITARY", "ORPHANED")
# 24. allergies | 过敏史 | TextField
# patient_user | onetoone to PatientUser in patient_portal app