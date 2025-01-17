from django.db import models

class MessageTemplate(models.Model):
    # System-set templates for followup messages
    template_name = models.CharField(
        max_length=100,
        verbose_name='模版类型',
        null=True,
        blank=True
    )

    content = models.TextField(
        verbose_name='随访模版',
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        verbose_name='是否启用',
        default=True,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = '随访消息模版'
        verbose_name_plural = '随访消息模版'

    def __str__(self):
        return self.template_name or ''