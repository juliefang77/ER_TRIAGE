from django.db import models
from .patient import Patient
from .medical_staff import MedicalStaff
from django.utils import timezone 

class TriageRecord(models.Model):
    ARRIVAL_METHODS = [
        ('WALK', '步行'),
        ('CARRIED', '抱送'),
        ('STRETCHER', '扶入'),
        ('WHEELCHAIR', '轮椅'),
        ('FLATBED', '平车'),
        ('LOCAL_120', '本院120'),
        ('EXTERNAL_120', '外院120'),
        ('POLICE_110', '110'),
        ('DOA', '院外死亡')
    ]

    SPEED_CHANNEL_CHOICES = [
        ('CHEST_PAIN', '胸痛'),
        ('STROKE', '卒中'),
        ('TRAUMA', '创伤'),
        ('PEDIATRIC_EMERGENCY', '危重儿童和新生儿'),
        ('HIGH_RISK_PREGNANCY', '高危孕产妇'),
        ('POISONING', '中毒'),
        ('COVID', '新冠肺炎'),
        ('CARDIAC_ARREST', '心衰'),
        ('BRAIN_INJURY', '重型颅脑损伤'),
        ('RESPIRATORY_FAILURE', '呼吸衰竭'),
        ('VACCINE_REACTION', '新冠疫苗不良反应'),
        ('CARDIOVASCULAR', '心血管'),
        ('CARDIOPULMONARY_ARREST', '心跳呼吸骤停'),
        ('SHOCK', '休克'),
        ('OTHER', '其他')
    ]

    SPECIALTY_TYPE_CHOICES = [
        ('CHEST_PAIN', '胸痛'),
        ('POST_STROKE', '卒中过'),
        ('TRAUMA', '创伤'),
        ('HIGH_RISK_PREGNANCY', '高危孕产妇'),
        ('PEDIATRIC_EMERGENCY', '危急儿童和新生儿')
    ]

    OTHER_INQUIRY_CHOICES = [
        ('ADMISSION_CERT', '开住院证'),
        ('PRESCRIPTION', '开药'),
        ('MEDICAL_ORDER', '开单'),
        ('NUCLEIC_TEST', '核酸检测')
    ]

    SURGERY_TYPE_CHOICES = [
        ('DEBRIDEMENT', '清创'),
        ('SUTURE', '缝合'),
        ('REMOVAL', '拆线'),
        ('MEDICATION_CHANGE', '换药')
    ]

    MASS_INJURY_CHOICES = [
        ('YES', '是'),
        ('NO', '否')
    ]
    
    patient = models.ForeignKey(
        Patient, 
        on_delete=models.PROTECT,
        related_name='triage_records',  # This allows reverse lookup
        null=True,
        blank=True
    )

    hospital = models.ForeignKey(
        'HospitalUser',
        on_delete=models.PROTECT,
        related_name='triage_records',  # Added related_name
        verbose_name='所属医院',
        null=True,
        blank=True
    )
    
    
    # Keep this as is since it's auto-generated
    registration_time = models.DateTimeField(
        default=timezone.now,  # Change auto_now_add to default
        verbose_name='登记时间'
    )
    
    nurse = models.ForeignKey(
        MedicalStaff, 
        on_delete=models.PROTECT, 
        related_name='triage_records', 
        verbose_name='分诊护士',
        null=True,
        blank=True
    )
    
    illness_time = models.DateTimeField(
        verbose_name='发病时间',
        null=True,
        blank=True
    )
    
    arrival_method = models.CharField(
        max_length=20,
        choices=ARRIVAL_METHODS,
        default='WALK',
        verbose_name='来院方式',
        null=True,
        blank=True
    )
    
    chief_complaint = models.TextField(
        verbose_name='主诉', 
        null=True, 
        blank=True
    )
    
    medical_history = models.TextField(
        verbose_name='既往史', 
        null=True, 
        blank=True
    )

    speed_channel = models.CharField(
        max_length=30,
        choices=SPEED_CHANNEL_CHOICES,
        verbose_name='绿色通道',
        null=True,
        blank=True
    )

    specialty_type = models.CharField(
        max_length=30,
        choices=SPECIALTY_TYPE_CHOICES,
        verbose_name='专科中心',
        null=True,
        blank=True
    )

    other_inquiry = models.CharField(
        max_length=20,
        choices=OTHER_INQUIRY_CHOICES,
        verbose_name='非急诊类',
        null=True,
        blank=True
    )

    surgery_type = models.CharField(
        max_length=20,
        choices=SURGERY_TYPE_CHOICES,
        verbose_name='手术',
        null=True,
        blank=True
    )

    ifmass_injury = models.CharField(
        max_length=5,
        choices=MASS_INJURY_CHOICES,
        verbose_name='是否群伤',
        null=True,
        blank=True
    )

    def __str__(self):
        patient_str = self.patient if self.patient else "未知患者"
        return f"{patient_str} - {self.registration_time}"

# TriageRecord Table Relations:
# - Links to Patient (ForeignKey)
# - Links to HospitalUser (ForeignKey)
# - Links to MedicalStaff (ForeignKey)
# - Has one TriageResult (OneToOne through reverse relation)

# Fields:
# 1. patient | 患者 | ForeignKey (Patient)
# 2. hospital | 所属医院 | ForeignKey (HospitalUser)
# 3. registration_time | 登记时间 | DateTimeField
# 4. nurse | 分诊护士 | ForeignKey (MedicalStaff)
# 5. illness_time | 发病时间 | DateTimeField
# 6. arrival_method | 来院方式 | CharField (choices)
# 7. chief_complaint | 主诉 | TextField
# 8. medical_history | 既往史 | TextField
# 9. speed_channel | 绿色通道 | CharField (choices)
# 10. specialty_type | 专科中心 | CharField (choices)
# 11. other_inquiry | 非急诊类 | CharField (choices)
# 12. surgery_type | 手术 | CharField (choices)
# 13. ifmass_injury | 是否群伤 | CharField (choices)