from django.db import models

class SurveyAi(models.Model):
    hospital = models.ForeignKey(
        'triage.Hospital',
        on_delete=models.CASCADE,
        verbose_name='医院',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='分析时间',
        null=True,
        blank=True
    )
    analysis_name = models.CharField(
        max_length=100,
        verbose_name='AI稿件名称',
        null=True,
        blank=True
    )
    analysis_result = models.TextField(
        verbose_name='AI分析结果',
        null=True,
        blank=True
    )
    recipients = models.ManyToManyField(
        'FollowupRecipient',
        related_name='survey_analyses',
        verbose_name='分析的患者',
        blank=True
    )
    
    class Meta:
        verbose_name = '问卷AI分析结果'
        verbose_name_plural = '问卷AI分析结果'
        ordering = ['-created_at']  # Most recent first
        
    def __str__(self):
        return f"{self.analysis_name or 'Unnamed Analysis'} ({self.recipients.count()} patients)"