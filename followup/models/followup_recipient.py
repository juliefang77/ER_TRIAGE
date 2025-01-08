from django.db import models
import uuid
from triage.models import TriageRecord, HospitalUser, Patient

class FollowupRecipient(models.Model):
    
    MESSAGE_REPLY_CHOICES = [
        ('WEEKEND', '周末'),
        ('WEEKDAY', '周中白天'),
        ('WEEKNIGHT', '周中晚上'),
        ('ANYTIME', '任意时间'),
        ('NO_REPLY', '未回复')
    ]
    
    SURVEY_STATUS_CHOICES = [
        ('NOT_SENT', '未发送'),
        ('SENT_INCOMPLETE', '已发送未完成'),
        ('COMPLETED', '已完成')
    ]
    
    CALL_STATUS_CHOICES = [
        ('CALLED', '已电话随访'),
        ('NOT_CALLED', '未电话随访')
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