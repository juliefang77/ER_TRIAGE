from django.db import models
from django.utils import timezone

class BookingOnline(models.Model):
    APPOINTMENT_STATUS = [
        ('PATIENT_SUBMITTED', '患者已下单'),
        ('HOSPITAL_ACCEPTED', '医院已接受订单'),
        ('CONSULTATION_COMPLETED', '问诊已完成'),
        ('CANCELLED', '医院已拒绝')
    ]

    patient_user = models.ForeignKey(
        'patient_portal.PatientUser',
        on_delete=models.SET_NULL,
        verbose_name='下单患者',
        null=True,
        blank=True
    )

    patient = models.ForeignKey(
        'triage.Patient',
        on_delete=models.SET_NULL,
        verbose_name='对应患者',
        null=True,
        blank=True
    )

    hospital = models.ForeignKey(
        'triage.Hospital',
        on_delete=models.SET_NULL,
        verbose_name='接单医院',
        null=True,
        blank=True
    )

    start_time = models.DateTimeField(
        verbose_name='最早时间',
        null=True,
        blank=True
    )

    end_time = models.DateTimeField(
        verbose_name='最晚时间',
        null=True,
        blank=True
    )

    payment_id = models.CharField(
        max_length=100,
        verbose_name='支付ID',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        verbose_name='下单时间',
        default=timezone.now
    )

    status = models.CharField(
        max_length=50,
        choices=APPOINTMENT_STATUS,
        default='PATIENT_SUBMITTED',
        verbose_name='订单状态',
        null=True,
        blank=True
    )

    actual_time = models.DateTimeField(
        verbose_name='实际完成/取消时间',
        null=True,
        blank=True,
        help_text='完成或取消时的实际时间'
    )

    def save(self, *args, **kwargs):
        # Auto-set actual_time when status changes to completed or cancelled
        if self.pk:  # Only for existing objects
            old_instance = BookingOnline.objects.get(pk=self.pk)
            if old_instance.status != self.status and self.status in ['CONSULTATION_COMPLETED', 'CANCELLED']:
                self.actual_time = timezone.now()
        super().save(*args, **kwargs)

    qr_code = models.CharField(
        max_length=255, 
        verbose_name='支付二维码编号',  # Changed to be more specific
        default="NO.0257426067",    # Your fixed QR code number
        null=True, 
        blank=True
    )

    terminal_trace = models.CharField(max_length=100, verbose_name='终端流水号', null=True, blank=True)

    class Meta:
        verbose_name = '预约付费线上问诊'
        verbose_name_plural = '预约付费线上问诊'

    def __str__(self):
        return f"Appointment {self.id} - {self.patient_user} - {self.status}"