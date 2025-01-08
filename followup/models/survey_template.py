from django.db import models
from .standard_question import StandardQuestion
from django.utils import timezone

class SurveyTemplate(models.Model):

    survey_name = models.CharField(
        max_length=100,
        verbose_name='模版名称',
        null=True,
        blank=True
    )

    hospital = models.ForeignKey(
        'triage.HospitalUser',
        on_delete=models.CASCADE,
        verbose_name='医院',
        null=True,
        blank=True
    )

    submitted_at = models.DateTimeField(
        default=timezone.now,  # Using timezone.now instead of auto_now_add
        verbose_name='提交时间',
        null=True,
        blank=True
    )

    # Eight question fields
    question_1 = models.ForeignKey(
        'StandardQuestion',
        on_delete=models.SET_NULL,
        related_name='template_question_1',
        verbose_name='问题一',
        null=True,
        blank=True
    )

    question_2 = models.ForeignKey(
        'StandardQuestion',
        on_delete=models.SET_NULL,
        related_name='template_question_2',
        verbose_name='问题二',
        null=True,
        blank=True
    )

    question_3 = models.ForeignKey(
        'StandardQuestion',
        on_delete=models.SET_NULL,
        related_name='template_question_3',
        verbose_name='问题三',
        null=True,
        blank=True
    )

    question_4 = models.ForeignKey(
        'StandardQuestion',
        on_delete=models.SET_NULL,
        related_name='template_question_4',
        verbose_name='问题四',
        null=True,
        blank=True
    )

    question_5 = models.ForeignKey(
        'StandardQuestion',
        on_delete=models.SET_NULL,
        related_name='template_question_5',
        verbose_name='问题五',
        null=True,
        blank=True
    )

    question_6 = models.ForeignKey(
        'StandardQuestion',
        on_delete=models.SET_NULL,
        related_name='template_question_6',
        verbose_name='问题六',
        null=True,
        blank=True
    )

    question_7 = models.ForeignKey(
        'StandardQuestion',
        on_delete=models.SET_NULL,
        related_name='template_question_7',
        verbose_name='问题七',
        null=True,
        blank=True
    )

    question_8 = models.ForeignKey(
        'StandardQuestion',
        on_delete=models.SET_NULL,
        related_name='template_question_8',
        verbose_name='问题八',
        null=True,
        blank=True
    )

    created_by = models.CharField(  # Changed from ForeignKey to CharField
        max_length=100,
        verbose_name='模版创建人',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='模版创建时间',
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='是否启用',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = '随访问卷模版'
        verbose_name_plural = '随访问卷模版'

    def __str__(self):
        return self.survey_name or '未命名模版'

# SurveyTemplate Table Relations:
    # - Links to HospitalUser (ForeignKey)
    # - Links to StandardQuestion (8 ForeignKeys)
    # - Links to MedicalStaff (ForeignKey)
    # - Has many FollowupSurveys (reverse relation)
    #
    # Fields:
    # 1. survey_name | 模版名称 | CharField
    # 2. uuid | UUID | UUIDField
    # 3. hospital | 医院 | ForeignKey (HospitalUser)
    # 4. question_1 | 问题一 | ForeignKey (StandardQuestion)
    # 5. question_2 | 问题二 | ForeignKey (StandardQuestion)
    # 6. question_3 | 问题三 | ForeignKey (StandardQuestion)
    # 7. question_4 | 问题四 | ForeignKey (StandardQuestion)
    # 8. question_5 | 问题五 | ForeignKey (StandardQuestion)
    # 9. question_6 | 问题六 | ForeignKey (StandardQuestion)
    # 10. question_7 | 问题七 | ForeignKey (StandardQuestion)
    # 11. question_8 | 问题八 | ForeignKey (StandardQuestion)
    # 12. created_by | 模版创建人 | ForeignKey (MedicalStaff)
    # 13. created_at | 模版创建时间 | DateTimeField
    # 14. is_active | 是否启用 | BooleanField