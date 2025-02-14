from django.db import models
from django.utils import timezone

class BookingPayment(models.Model):
    PAYMENT_STATUS = [
        ('PENDING', '待支付'),
        ('PAID', '已支付'),
        ('REFUNDED', '已退款'),
        ('FAILED', '支付失败')
    ]
    patient_user = models.ForeignKey(
        'patient_portal.PatientUser',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    PRICE_OPTIONS = [
        (4000, '40元'),
        (5000, '50元'),
        (6000, '60元'),
        (7000, '70元'),
    ]
    booking_online = models.OneToOneField(
        'followup.BookingOnline',
        on_delete=models.CASCADE,
        related_name='payment',
        null=True,
        blank=True,
        verbose_name='在线预约'
    )
    amount = models.IntegerField(
        choices=PRICE_OPTIONS,
        default=5000,  # Default to 50元
        verbose_name='支付金额(分)',
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='PENDING',
        verbose_name='支付状态',
        null=True,
        blank=True
    )

    terminal_trace = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='收钱吧流水号',
        null=True,
        blank=True
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='支付时间'
    )

    refunded_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='退款时间'
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='创建时间',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Payment for Booking {self.booking_online.id if self.booking_online else 'None'} - {self.status}"

    class Meta:
        verbose_name = '预约支付'
        verbose_name_plural = '预约支付'