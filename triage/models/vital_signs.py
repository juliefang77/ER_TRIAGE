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
        ('HEAD_NECK', '头颈部')
    ]

    INJURY_TYPES = [
        ('LACERATION', '裂伤/挫伤'),
        ('STAB', '刺伤'),
        ('BLUNT', '钝性伤'),
        ('GUNSHOT', '弹道伤')
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
        max_length=20,
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

    def __str__(self):
        if self.triage_record and self.triage_record.patient:
            return f"{self.triage_record.patient} 生命体征"
        return "生命体征记录"
    
