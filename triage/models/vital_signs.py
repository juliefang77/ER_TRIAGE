from django.db import models
from .triage_record import TriageRecord

class VitalSigns(models.Model):
    triage_record = models.OneToOneField(TriageRecord, on_delete=models.CASCADE)
    temperature = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        verbose_name='体温',
        null=True, 
        blank=True
    )
    systolic_bp = models.IntegerField(verbose_name='收缩压', null=True, blank=True)
    diastolic_bp = models.IntegerField(verbose_name='舒张压', null=True, blank=True) 
    heart_rate = models.IntegerField(verbose_name='心率', null=True, blank=True)
    respiratory_rate = models.IntegerField(verbose_name='呼吸频率', null=True, blank=True)
    avpu_status = models.CharField(
        max_length=1,
        choices=[('A', 'Alert'), ('V', 'Voice'), ('P', 'Pain'), ('U', 'Unresponsive')],
        default='A',
        verbose_name='AVPU评分'
    )
    oxygen_saturation = models.IntegerField(verbose_name='血氧饱和度', null=True, blank=True)
    
    blood_glucose = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        verbose_name='血糖',
        null=True,
        blank=True
    )

    pain_score = models.IntegerField(
        verbose_name='疼痛评分',
        choices=[(i, str(i)) for i in range(11)],  # 0-10 scale
        null=True,
        blank=True
    )

    trauma_score = models.IntegerField(  # Added
        verbose_name='创伤评分',
        choices=[(i, str(i)) for i in range(13)],  # 0-12 scale for RTS
        null=True,
        blank=True
    )

    measurement_time = models.DateTimeField(auto_now_add=True, verbose_name='测量时间')
    
    mews_score = models.IntegerField(verbose_name='MEWS评分', default=0)

    def __str__(self):
        return f"{self.triage_record.patient} 生命体征"
