from django.db import models
import uuid
from .followup_recipient import FollowupRecipient
from .survey_template import SurveyTemplate

class FollowupSurvey(models.Model):

    hospital = models.ForeignKey(
        'triage.HospitalUser',
        on_delete=models.CASCADE,
        verbose_name='医院',
        null=True,
        blank=True
    )

    recipient = models.ForeignKey(
        'FollowupRecipient',
        on_delete=models.CASCADE,
        related_name='surveys',
        verbose_name='问卷填写人',
        null=True,
        blank=True
    )

    template = models.ForeignKey(
        'SurveyTemplate',
        on_delete=models.SET_NULL,
        related_name='instances',
        verbose_name='问卷模版',
        null=True,
        blank=True
    )

    completed_at = models.DateTimeField(
        verbose_name='填写时间',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = '随访问卷'
        verbose_name_plural = '随访问卷'

    def __str__(self):
        return f"{self.recipient} - {self.template} - {self.completed_at or '未完成'}"
    
# FollowupSurvey Table Relations:
    # - Links to HospitalUser (ForeignKey)
    # - Links to FollowupRecipient (ForeignKey)
    # - Links to SurveyTemplate (ForeignKey)
    # - Has many SurveyResponses (reverse relation)
    #
    # Fields:
    # 1. hospital | 医院 | ForeignKey (HospitalUser)
    # 2. uuid | UUID | UUIDField
    # 3. recipient | 问卷填写人 | ForeignKey (FollowupRecipient)
    # 4. template | 问卷模版 | ForeignKey (SurveyTemplate)
    # 5. completed_at | 填写时间 | DateTimeField