from django.db import models
import uuid
from triage.models import TriageRecord, HospitalUser, Patient

class FollowupRecipient(models.Model):
    
    MESSAGE_REPLY_CHOICES = [
        ('WEEKEND', '周末 (WEEKEND)'),
        ('WEEK_DAY', '周中白天 (WEEK_DAY)'),
        ('WEEK_NIGHT', '周中晚上 (WEEK_NIGHT)'),
        ('ANYTIME', '任意时间 (ANYTIME)'),
        ('NOT_YET', '未回复 (NOT_YET)')
    ]

    SURVEY_STATUS_CHOICES = [
        ('NO_SEND', '未发送 (NO_SEND)'),
        ('NO_RESPONSE', '已发送未完成 (NO_RESPONSE)'),
        ('YES_RESPONSE', '已完成 (YES_RESPONSE)')
    ]

    CALL_STATUS_CHOICES = [
        ('YES_CALL', '已电话随访 (YES_CALL)'),
        ('NO_CALL', '未电话随访 (NO_CALL)')
    ]
    
    patient = models.ForeignKey(
        'triage.Patient', 
        on_delete=models.CASCADE, 
        verbose_name='随访病人',
        null=True,
        blank=True
    )

    hospital = models.ForeignKey(
        'triage.HospitalUser', 
        on_delete=models.CASCADE, 
        verbose_name='随访医院',
        null=True,
        blank=True
    )
    triage_record = models.OneToOneField(
        TriageRecord, 
        on_delete=models.CASCADE, 
        verbose_name='随访患者分诊记录',
        related_name='recipient',  # Add this line
        null=True,
        blank=True
    )

    # Add phone field
    phone = models.CharField(
        max_length=20,
        verbose_name='联系电话',
        null=True,
        blank=True
    )

    # Add research_patient field
    research_patient = models.BooleanField(
        verbose_name='重点随访对象',
        null=True,
        blank=True
    )

    message_reply = models.CharField(
        max_length=20,
        choices=MESSAGE_REPLY_CHOICES,
        verbose_name='回复时间偏好',
        null=True,
        blank=True
    )
    
    survey_status = models.CharField(
        max_length=20,
        choices=SURVEY_STATUS_CHOICES,
        default='NOT_SENT',
        verbose_name='问卷状态',
        null=True,
        blank=True
    )
    
    call_status = models.CharField(
        max_length=20,
        choices=CALL_STATUS_CHOICES,
        default='NOT_CALLED',
        verbose_name='电话随访状态',
        null=True,
        blank=True
    )

    # FollowupRecipient Table Relations:
    # - Links to Patient (ForeignKey)
    # - Links to HospitalUser (ForeignKey)
    # - Links to TriageRecord (OneToOne)
    # - Has many FollowupSurveys (reverse relation)
    # - Has many FollowupNotetakings (reverse relation)
    # 
    # Fields:
    # 1. patient | 随访病人 | ForeignKey (Patient)
    # 2. uuid | UUID | UUIDField
    # 3. hospital | 随访医院 | ForeignKey (HospitalUser)
    # 4. triage_record | 随访患者分诊记录 | OneToOneField (TriageRecord)
    # 5. message_reply | 回复时间偏好 | CharField (choices)
    # 6. survey_status | 问卷状态 | CharField (choices)
    # 7. call_status | 电话随访状态 | CharField (choices)
    # phone | 
    # research_patient | 