from django.db import models
import uuid
from .followup_survey import FollowupSurvey

class SurveyResponse(models.Model):

    hospital = models.ForeignKey(
        'triage.HospitalUser',
        on_delete=models.CASCADE,
        verbose_name='医院',
        null=True,
        blank=True
    )

    survey = models.OneToOneField(
        'FollowupSurvey',
        on_delete=models.CASCADE,
        related_name='response',
        verbose_name='问卷',
        null=True,
        blank=True
    )

    answer_1 = models.TextField(
        verbose_name='答案一',
        null=True,
        blank=True
    )

    answer_2 = models.TextField(
        verbose_name='答案二',
        null=True,
        blank=True
    )

    answer_3 = models.TextField(
        verbose_name='答案三',
        null=True,
        blank=True
    )

    answer_4 = models.TextField(
        verbose_name='答案四',
        null=True,
        blank=True
    )

    answer_5 = models.TextField(
        verbose_name='答案五',
        null=True,
        blank=True
    )

    answer_6 = models.TextField(
        verbose_name='答案六',
        null=True,
        blank=True
    )

    answer_7 = models.TextField(
        verbose_name='答案七',
        null=True,
        blank=True
    )

    answer_8 = models.TextField(
        verbose_name='答案八',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = '问卷回答'
        verbose_name_plural = '问卷回答'

    def __str__(self):
        return f"{self.survey} - 回答"

# SurveyResponse Table Relations:
    # - Links to HospitalUser (ForeignKey)
    # - Links to FollowupSurvey (OneToOne)
    #
    # Fields:
    # 1. hospital | 医院 | ForeignKey (HospitalUser)
    # 2. survey | 问卷 | OneToOneField (FollowupSurvey)
    # 3. uuid | UUID | UUIDField
    # 4. answer_1 | 答案一 | TextField
    # 5. answer_2 | 答案二 | TextField
    # 6. answer_3 | 答案三 | TextField
    # 7. answer_4 | 答案四 | TextField
    # 8. answer_5 | 答案五 | TextField
    # 9. answer_6 | 答案六 | TextField
    # 10. answer_7 | 答案七 | TextField
    # 11. answer_8 | 答案八 | TextField