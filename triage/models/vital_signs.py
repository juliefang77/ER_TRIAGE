from django.db import models
from .triage_record import TriageRecord

class VitalSigns(models.Model):
    triage_record = models.OneToOneField(
        TriageRecord, 
        on_delete=models.CASCADE,
        related_name='vitalsigns',  # Add this to match select_related
        null=True,  # Added null=True
        blank=True  # Added blank=True
    )

    CONSCIOUS_STATUS_CHOICES = [
        ('CLEAR', '清醒'),
        ('DROWSY', '嗜睡'),
        ('LETHARGY', '昏睡'),
        ('SEMI_COMA', '半昏迷'),
        ('COMA', '昏迷')
    ]

    INJURY_POSITIONS = [
        ('LIMBS_SKIN', '四肢/皮肤'),
        ('BACK', '背部'),
        ('CHEST', '胸部'),
        ('ABDOMEN', '腹部'),
        ('HEAD_NECK', '头颈部'),
        ('BUTTOCKS', '臀部')  # Added 臀部
    ]

    INJURY_TYPES = [
        ('LACERATION', '裂伤/挫伤'),
        ('STAB', '刺伤'),
        ('BLUNT', '钝性伤'),
        ('GUNSHOT', '弹道伤'),
        ('BURN', '烧伤')  # Added 烧伤
    ]

    EYE_RESPONSES = [
        ('NORMAL', '正常睁眼'),
        ('CALL', '呼唤睁眼'),
        ('PAIN', '刺痛睁眼'),
        ('NONE', '无反应')
    ]

    VERBAL_RESPONSES = [
        ('CORRECT', '回答正确'),
        ('INCORRECT', '回答错误'),
        ('INCOHERENT', '语无伦次'),
        ('SOUNDS_ONLY', '只能发声'),
        ('NONE', '不能发声')
    ]

    MOTOR_RESPONSES = [
        ('OBEY', '遵嘱运动'),
        ('LOCALIZE_PAIN', '刺痛定位'),
        ('WITHDRAW_PAIN', '躲避刺痛'),
        ('FLEXION_PAIN', '刺痛肢屈'),
        ('EXTENSION_PAIN', '刺痛肢伸'),
        ('NONE', '无反应')
    ]
    
    temperature = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        verbose_name='体温',
        null=True, 
        blank=True
    )
    
    systolic_bp = models.IntegerField(
        verbose_name='收缩压', 
        null=True, 
        blank=True
    )
    
    diastolic_bp = models.IntegerField(
        verbose_name='舒张压', 
        null=True, 
        blank=True
    ) 
    
    heart_rate = models.IntegerField(
        verbose_name='心率', 
        null=True, 
        blank=True
    )
    
    respiratory_rate = models.IntegerField(
        verbose_name='呼吸频率', 
        null=True, 
        blank=True
    )
    
    avpu_status = models.CharField(
        max_length=1,
        choices=[
            ('A', '清醒'),
            ('V', '对声音有反应'),
            ('P', '对疼痛有反应'),
            ('U', '无反应')
        ],
        default='A',
        verbose_name='AVPU评分',
        null=True,
        blank=True
    )

    # blood_potassium 血钾 number 
    blood_potassium = models.DecimalField(
        max_digits=4,  # Allows values like 3.5, 5.2, etc.
        decimal_places=1,
        verbose_name='血钾',
        null=True,
        blank=True,
        help_text='mmol/L'  # Standard unit for blood potassium
    )
    
    oxygen_saturation = models.IntegerField(
        verbose_name='血氧饱和度', 
        null=True, 
        blank=True
    )
    
    blood_glucose = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        verbose_name='血糖',
        null=True,
        blank=True
    )

    # conscious_status 意识
    conscious_status = models.CharField(
        max_length=20,
        choices=CONSCIOUS_STATUS_CHOICES,
        verbose_name='意识',
        null=True,
        blank=True
    )

    pain_score = models.IntegerField(
        verbose_name='疼痛评分',
        choices=[(i, str(i)) for i in range(7)],  # 0-7 scale
        null=True,
        blank=True
    )

    trauma_score = models.IntegerField(
        verbose_name='创伤评分',
        choices=[(i, str(i)) for i in range(13)],  # 0-12 scale for RTS
        null=True,
        blank=True
    )

    # newly added
    injury_position = models.CharField(
        max_length=255,
        choices=INJURY_POSITIONS,
        verbose_name='损伤部位',
        null=True,
        blank=True
    )

    injury_type = models.CharField(
        max_length=20,
        choices=INJURY_TYPES,
        verbose_name='损伤类型',
        null=True,
        blank=True
    )

    eyeopen_status = models.CharField(
        max_length=20,
        choices=EYE_RESPONSES,
        verbose_name='睁眼反应',
        null=True,
        blank=True
    )

    response_status = models.CharField(
        max_length=20,
        choices=VERBAL_RESPONSES,
        verbose_name='语言反应',
        null=True,
        blank=True
    )

    move_status = models.CharField(
        max_length=20,
        choices=MOTOR_RESPONSES,
        verbose_name='运动反应',
        null=True,
        blank=True
    )

    gcs_score = models.IntegerField(
        verbose_name='GCS评分',
        null=True,
        blank=True
    )

    rems_score = models.IntegerField(
        verbose_name='REMS评分',
        null=True,
        blank=True
    )


    measurement_time = models.DateTimeField(
        auto_now_add=True, 
        null=True, 
        blank=True,
        verbose_name='测量时间'
    )
    
    mews_score = models.IntegerField(
        verbose_name='MEWS评分', 
        null=True, 
        blank=True,
        default=0
    )

    revised_trauma = models.IntegerField(
        verbose_name='修订创伤评分（前端自动生成）',
        null=True,
        blank=True
    )

    def __str__(self):
        if self.triage_record and self.triage_record.patient:
            return f"{self.triage_record.patient} 生命体征"
        return "生命体征记录"
    
# VitalSigns Table Relations:
# - Links to TriageRecord (OneToOne through reverse relation)

# Fields:
# 1. triage_record | 分诊记录 | OneToOneField (TriageRecord)
# 2. temperature | 体温 | DecimalField(3,1)
# 3. systolic_bp | 收缩压 | IntegerField
# 4. diastolic_bp | 舒张压 | IntegerField
# 5. heart_rate | 心率 | IntegerField
# 6. respiratory_rate | 呼吸频率 | IntegerField
# 7. avpu_status | AVPU评分 | CharField (choices)
# 8. blood_potassium | 血钾 | DecimalField(4,1)
# 9. oxygen_saturation | 血氧饱和度 | IntegerField
# 10. blood_glucose | 血糖 | DecimalField(5,1)
# 11. conscious_status | 意识 | CharField (choices)
# 12. pain_score | 疼痛评分 | IntegerField (0-6)
# 13. trauma_score | 创伤评分 | IntegerField (0-12)
# 14. injury_position | 损伤部位 | CharField (multiple choices)
# 15. injury_type | 损伤类型 | CharField (choices)
# 16. eyeopen_status | 睁眼反应 | CharField (choices)
# 17. response_status | 语言反应 | CharField (choices)
# 18. move_status | 运动反应 | CharField (choices)
# 19. gcs_score | GCS评分 | IntegerField
# 20. rems_score | REMS评分 | IntegerField
# 21. measurement_time | 测量时间 | DateTimeField
# 22. mews_score | MEWS评分 | IntegerField
# revised_trauma