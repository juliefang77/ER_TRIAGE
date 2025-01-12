from django.db import models
from django.utils import timezone

class FollowupNotetaking(models.Model):
    recipient = models.ForeignKey(
        'followup.FollowupRecipient', 
        on_delete=models.CASCADE,
        verbose_name="被随访人",
        blank=True,
        null=True
    )
    hospital = models.ForeignKey(
        'triage.HospitalUser',
        on_delete=models.CASCADE,
        verbose_name="随访医院",
        blank=True,
        null=True
    )
    raw_notes = models.TextField(
        verbose_name="随访原始记录",
        blank=True,
        null=True
    )
    processed_notes = models.TextField(
        verbose_name="随访处理后记录",
        blank=True,
        null=True
    )
    created_by = models.TextField(
        verbose_name="随访医护",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        verbose_name="随访时间",
        default=timezone.now,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "电话随访AI记录"
        verbose_name_plural = "电话随访AI记录"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.recipient} - {self.created_at.strftime('%Y-%m-%d')}"