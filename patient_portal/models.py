# patient_portal/models.py

from django.db import models
from triage.models import Hospital
import uuid  # Add this import

class PatientTriageSubmission(models.Model):
    # Choice Definitions

    # Add UUID field as primary key
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    STATUS_CHOICES = [
        ('PENDING', '待处理'),
        ('APPROVED', '已通过'),
        # Optionally add more statuses if needed
    ]

    GENDER_CHOICES = [
        ('F', '女'),
        ('M', '男')
    ]

    ID_TYPE_CHOICES = [
        ('ID_CARD', '居民身份证'),
        ('HUKOU', '居民户口本'),
        ('HK_MC_TW', '港澳台居民来往内地通行证'),
        ('FOREIGNER', '外国人永久居留证'),
        ('PASSPORT', '护照'),
        ('MILITARY', '军官证')
    ]

    CHIEF_SYMPTOM_CHOICES = [
        ('BLEEDING', '加压止血无法控制/急性出血'),
        ('CHEST_PAIN', '胸痛胸闷，呼吸困难'),
        ('PREGNANCY_PAIN', '孕妇剧烈腹痛'),
        ('HIGH_FEVER', '持续高烧>38.5摄氏度'),
        ('CONSCIOUSNESS', '突发意识改变（嗜睡，定向障碍，昏厥）'),
        ('HEAD_INJURY', '头/眼受伤')
    ]

    INSURANCE_TYPE_CHOICES = [
        ('SELF_PAY', '自费'),
        ('PUBLIC', '公费'),
        ('MEDICAL_INSURANCE', '医保'),
        ('COMMERCIAL', '商保'),
        ('HOSPITAL_STAFF', '本院职工'),
        ('STAFF_FAMILY', '职工家属'),
        ('OTHER_LOCATION', '异地医保'),
        ('NEW_RURAL', '新农合'),
        ('URBAN_RURAL', '城乡医保'),
        ('FIVE_GUARANTEES', '五保特困'),
        ('LOW_INSURANCE', '低保'),
        ('MILITARY', '军烈'),
        ('EARTHQUAKE', '512地震'),
        ('RAILWAY_STAFF', '轻轨工伤'),
        ('RAILWAY_INSURANCE', '铁路医保'),
        ('ROAD_FUND', '道路基金'),
        ('DISABILITY', '复员伤残'),
        ('DISABLED', '残疾'),
        ('ISOLATION', '担保'),
        ('HOMELESS', '无主病人'),
        ('HIGH_VALUE', '高价'),
        ('WORK_INJURY', '工伤'),
        ('TRAFFIC_INJURY', '车伤'),
        ('MATERNITY', '生育'),
        ('SPECIAL_AGREEMENT', '特约')
    ]

    PATIENT_TYPE_CHOICES = [
        ('THREE_NOS', '三无人员'),
        ('LOW_INCOME', '低保户'),
        ('SPECIAL_CARE', '特困户'),
        ('POOR_CARD', '建卡贫困户'),
        ('FIVE_GUARANTEES', '五保户'),
        ('8023_TEAM', '8023部队'),
        ('ACTIVE_MILITARY', '现役军人'),
        ('RETIRED_MILITARY', '退伍军人'),
        ('MISSING_PERSON', '失独人员')
    ]

    OTHER_INQUIRY_CHOICES = [
        ('ADMISSION_CERT', '开住院证'),
        ('PRESCRIPTION', '开药'),
        ('MEDICAL_CERT', '开单'),
        ('NUCLEIC_TEST', '核酸检测')
    ]


    INJURY_TYPE_CHOICES = [
        ('LACERATION', '裂伤/挫伤'),
        ('STAB', '刺伤'),
        ('BLUNT', '钝性伤'),
        ('GUNSHOT', '弹道伤'),
        ('BURN', '烧伤')  # Added 烧伤
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING',
        verbose_name='状态'
    )

    # Hospital Info
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.SET_NULL,  # If hospital is deleted, set this field to NULL
        verbose_name='医院',
        null=True,
        blank=True
    )

    # Patient Basic Info
    name_patient = models.CharField(
        max_length=100,
        verbose_name='患者姓名',
        null=True,
        blank=True
    )
    
    gender = models.CharField(
        max_length=10,
        verbose_name='性别',
        choices=GENDER_CHOICES,
        null=True,
        blank=True
    )
    
    date_of_birth = models.DateField(
        verbose_name='出生日期',
        null=True,
        blank=True
    )
    
    id_type = models.CharField(
        max_length=20,
        verbose_name='证件类型',
        choices=ID_TYPE_CHOICES,
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
        max_length=50,
        verbose_name='医保卡号',
        null=True,
        blank=True
    )
    
    id_hospital_card = models.CharField(
        max_length=50,
        verbose_name='诊疗卡号',
        null=True,
        blank=True
    )
    
    patient_phone = models.CharField(
        max_length=11,
        verbose_name='患者电话',
        null=True,
        blank=True
    )
    
    chief_complaint = models.TextField(
        verbose_name='主诉',
        null=True,
        blank=True
    )
    
    chief_symptom = models.CharField(
        max_length=20,
        verbose_name='快捷分诊',
        choices=CHIEF_SYMPTOM_CHOICES,
        null=True,
        blank=True
    )

    # Additional Fields
    insurance_type = models.CharField(
        max_length=50,
        verbose_name='费别',
        choices=INSURANCE_TYPE_CHOICES,
        null=True,
        blank=True
    )

    pain_score = models.IntegerField(
        verbose_name='疼痛评分',
        null=True,
        blank=True
    )

    temperature = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        verbose_name='体温',
        null=True,
        blank=True
    )

    injury_position = models.CharField(
        max_length=255,
        verbose_name='小人图/损伤部位',
        null=True,
        blank=True
    )

    injury_type = models.CharField(
        max_length=50,
        verbose_name='损伤类型',
        choices=INJURY_TYPE_CHOICES,
        null=True,
        blank=True
    )

    other_inquiry = models.CharField(
        max_length=50,
        verbose_name='非急诊类',
        choices=OTHER_INQUIRY_CHOICES,
        null=True,
        blank=True
    )

    patient_type = models.CharField(
        max_length=50,
        verbose_name='身份标识',
        choices=PATIENT_TYPE_CHOICES,
        null=True,
        blank=True
    )

    waitlist_id = models.CharField(
        max_length=10,
        verbose_name='分诊排号',
        null=True,  
        blank=True,
    )

    class Meta:
        verbose_name = '患者分诊提交'
        verbose_name_plural = '患者分诊提交'

    def __str__(self):
        hospital_name = self.hospital.name if self.hospital else 'Unknown'
        return f"{self.name_patient or 'Unknown'} - {hospital_name}"


# PatientTriageSubmission Table Relations:
# - Links to Hospital (ForeignKey)

# Fields:
# 1. hospital | 医院 | ForeignKey (Hospital)
# 2. name_patient | 患者姓名 | CharField
# 3. gender | 性别 | CharField (choices)
# 4. date_of_birth | 出生日期 | DateField
# 5. id_type | 证件类型 | CharField (choices)
# 6. id_number | 证件号码 | CharField
# 7. id_medical_insurance | 医保卡号 | CharField
# 8. id_hospital_card | 诊疗卡号 | CharField
# 9. patient_phone | 患者电话 | CharField
# 10. chief_complaint | 主诉 | TextField
# 11. chief_symptom | 快捷分诊 | CharField (choices)
# 12. insurance_type | 费别 | CharField (choices)
# 13. pain_score | 疼痛评分 | IntegerField
# 14. temperature | 体温 | DecimalField
# 15. injury_position | 小人图/损伤部位 | CharField (choices)
# 16. injury_type | 损伤类型 | CharField (choices)
# 17. other_inquiry | 非急诊类 | CharField (choices)
# 18. patient_type | 身份标识 | CharField (choices)
# 19. uuid | Primary key
# 20. status | 状态 ｜ 待处理、已通过