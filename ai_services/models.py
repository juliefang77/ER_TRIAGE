from django.db import models

# Create your models here.
from django.db import models

class AIUsageLog(models.Model):
    service = models.CharField(
        max_length=50,  # 'baidu', etc.
        blank=True,
        null=True
    )
    endpoint = models.CharField(
        max_length=100,  # specific API endpoint used
        blank=True,
        null=True
    )
    tokens_used = models.IntegerField(
        blank=True,
        null=True
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=0,
        blank=True,
        null=True
    )
    success = models.BooleanField(
        default=True,
        blank=True,
        null=True
    )
    error_message = models.TextField(
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "AI使用记录"
        verbose_name_plural = "AI使用记录"

    def __str__(self):
        return f"{self.service} - {self.created_at}"