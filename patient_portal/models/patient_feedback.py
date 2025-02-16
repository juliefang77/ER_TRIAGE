from django.db import models
from patient_portal.models import PatientUser

class PatientFeedback(models.Model):
    REQUEST_TYPE_CHOICES = [
        ('REFUND', '退款'),
        ('APP', 'app功能'),
        ('HOSPITAL', '医院信息'),
        ('PERSONAL', '个人信息'),
        ('OTHER', '其他'),
    ]

    patient_user = models.ForeignKey(
        PatientUser,
        on_delete=models.SET_NULL,
        verbose_name='患者用户',
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
        verbose_name = '患者提交feedback'
        verbose_name_plural = '患者提交feedback'

    def __str__(self):
        return f"{self.patient_user} - {self.get_request_type_display()} - {self.created_at}"