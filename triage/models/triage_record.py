from django.db import models
from .patient import Patient
from .medical_staff import MedicalStaff
from django.utils import timezone 

class TriageRecord(models.Model):
    ARRIVAL_METHODS = (
        ('WALK', '步行'),
        ('WHEELCHAIR', '轮椅'),
        ('STRETCHER', '担架'),
        ('AMB_120', '120'),
        ('SELF', '自行来院'),
    )

    patient = models.ForeignKey(
        Patient, 
        on_delete=models.PROTECT,
        related_name='triage_records',  # This allows reverse lookup
        null=True,
        blank=True
    )
    
    # Keep this as is since it's auto-generated
    registration_time = models.DateTimeField(
        default=timezone.now,  # Change auto_now_add to default
        verbose_name='登记时间'
    )
    
    nurse = models.ForeignKey(
        MedicalStaff, 
        on_delete=models.PROTECT, 
        verbose_name='分诊护士',
        null=True,
        blank=True
    )
    
    arrival_time = models.DateTimeField(
        verbose_name='发病时间',
        null=True,
        blank=True
    )
    
    arrival_method = models.CharField(
        max_length=10,
        choices=ARRIVAL_METHODS,
        default='WALK',
        verbose_name='来院方式',
        null=True,
        blank=True
    )
    
    chief_complaint = models.TextField(
        verbose_name='主诉', 
        null=True, 
        blank=True
    )
    
    medical_history = models.TextField(
        verbose_name='既往史', 
        null=True, 
        blank=True
    )

    def __str__(self):
        patient_str = self.patient if self.patient else "未知患者"
        return f"{patient_str} - {self.registration_time}"