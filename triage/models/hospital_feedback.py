from django.db import models
from triage.models import HospitalUser

class HospitalFeedback(models.Model):
    REQUEST_TYPE_CHOICES = [
        ('SOFTWARE', '软件功能'),
        ('INFO', '医院信息更新'),
        ('BILLING', '咨询费用'),
        ('OTHER', '其他'),
    ]

    hospital_user = models.ForeignKey(
        HospitalUser,
        on_delete=models.SET_NULL,
        verbose_name='医院用户',
        null=True,
        blank=True
    )

    contact = models.CharField(
        max_length=50,
        verbose_name='联系人',
        null=True,
        blank=True
    )

    contact_phone = models.CharField(
        max_length=20,
        verbose_name='联系电话',
        null=True,
        blank=True
    )

    request_type = models.CharField(
        max_length=20,
        choices=REQUEST_TYPE_CHOICES,
        verbose_name='问题类型',
        null=True,
        blank=True
    )

    request_content = models.TextField(
        verbose_name='问题描述',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='提交时间',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = '医院反馈feedback'
        verbose_name_plural = '医院反馈feedback'

    def __str__(self):
        return f"{self.hospital_user} - {self.get_request_type_display()} - {self.created_at}"