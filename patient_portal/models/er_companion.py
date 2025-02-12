from django.db import models

class ErCompanion(models.Model):
    patient_user = models.ForeignKey(
        'patient_portal.PatientUser',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    PRIORITY_CHOICES = [
        ('UNDERSTOOD', '我理解了，下一条！'),
        ('USEFUL', '这个信息对我很有用～'),
    ]
    SYMPTOM_CHOICES = [
        ('USEFUL', '这个信息对我很有用～'),
        ('RELEVANT', '这个信息对我不是很有针对性'),
    ]
    MEDICATION_CHOICES = [
        ('KNOWN', '我已经知道这些信息啦'),
        ('USEFUL', '这个信息对我很有用～'),
    ]
    HEART_CHOICES = [
        ('CALM', '平静的小溪流水'),
        ('URGENT', '急促的鼓点'),
        ('RELAXED', '轻快的散步节奏'),
    ]
    ENERGY_CHOICES = [
        ('FULL', '刚充满电的手机'),
        ('COFFEE', '需要来杯咖啡'),
        ('LOW', '快没电的闹钟'),
    ]
    WEATHER_CHOICES = [
        ('SUNSHINE', '阳光明媚'),
        ('CLOUD', '多云'),
        ('TEMPEST', '暴风雨'),
    ]
    PAYMENT_CHOICES = [
        ('UNPAID', '未支付'),
        ('PAID', '已支付'),
    ]
    # Response Fields
    last_completed_step = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    priority_response = models.CharField(
        max_length=50,
        choices=PRIORITY_CHOICES,
        null=True,
        blank=True
    )
    symptom_response = models.CharField(
        max_length=50,
        choices=SYMPTOM_CHOICES,
        null=True,
        blank=True
    )
    medication_response = models.CharField(
        max_length=50,
        choices=MEDICATION_CHOICES,
        null=True,
        blank=True
    )
    # Assessment Fields
    heart_level = models.CharField(
        max_length=50,
        choices=HEART_CHOICES,
        null=True,
        blank=True
    )
    energy_level = models.CharField(
        max_length=50,
        choices=ENERGY_CHOICES,
        null=True,
        blank=True
    )
    waiting_feel = models.CharField(
        max_length=50,
        choices=WEATHER_CHOICES,
        null=True,
        blank=True
    )

    # Step Completion Fields
    complete_step1 = models.CharField(max_length=255, null=True, blank=True)
    complete_step2 = models.CharField(max_length=255, null=True, blank=True)
    complete_step3 = models.CharField(max_length=255, null=True, blank=True)

    # Status Fields
    payment_status = models.CharField(
        max_length=50,
        choices=PAYMENT_CHOICES,
        null=True,
        blank=True
    )
    terminal_trace = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'er_companion'
        verbose_name = '付费 ER Companion'
        verbose_name_plural = '付费 ER Companion'

    def __str__(self):
        return f"Companion for {self.patient_user} - Step {self.last_completed_step}"