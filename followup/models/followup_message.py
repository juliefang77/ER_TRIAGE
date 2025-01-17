from django.db import models

class FollowupMessage(models.Model):
    # Track individual messages sent to patients
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
        verbose_name='患者',
        null=True,
        blank=True
    )

    template = models.ForeignKey(
        'MessageTemplate',
        on_delete=models.SET_NULL,  # Don't delete messages if template is deleted
        verbose_name='消息模版',
        null=True,
        blank=True
    )

    content = models.TextField(
        verbose_name='信息内容',
        null=True,
        blank=True
    )

    sent_at = models.DateTimeField(
        verbose_name='发送时间',
        auto_now_add=True,
        null=True,
        blank=True
    )
    responded_at = models.DateTimeField(
        verbose_name='回复时间',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = '随访消息'
        verbose_name_plural = '随访消息'

    def __str__(self):
        return f"{self.hospital} - {self.recipient} - {self.sent_at}"