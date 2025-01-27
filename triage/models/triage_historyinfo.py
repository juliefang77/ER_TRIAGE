from django.db import models
from django.utils import timezone

class TriageHistoryInfo(models.Model):
    # One-to-One relationship with TriageRecord
    triage_record = models.OneToOneField(
        'TriageRecord',
        on_delete=models.CASCADE,
        related_name='history_info',
        null=True,
        blank=True
    )

    GUAHAO_STATUS_CHOICES = [
        ('REGISTERED', '已挂号'),
        ('NOT_REGISTERED', '未挂号'),
        ('CANCELLED', '已退号'),
    ]

    EDIT_STATUS_CHOICES = [
        ('FIRST_TRIAGE', '初次分诊'),
        ('MODIFIED', '已修改'),
        ('SECOND_TRIAGE', '二次分诊'),
    ]

    # Fields will be added based on your next screenshot
    guahao_status = models.CharField(
        max_length=20,
        choices=GUAHAO_STATUS_CHOICES,
        verbose_name='挂号状态',
        null=True,
        blank=True
    )

    edit_triage = models.CharField(
        max_length=20,
        choices=EDIT_STATUS_CHOICES,
        verbose_name='修改状态',
        default='FIRST_TRIAGE',
        null=True,
        blank=True
    )

    departure_time = models.DateTimeField(
        verbose_name='出科时间',
        null=True,
        blank=True
    )

    stay_duration = models.DurationField(
        verbose_name='滞留急诊科时间',
        null=True,
        blank=True
    )

    def calculate_stay_duration(self):
        """Calculate stay duration when departure time is set"""
        if self.departure_time and self.triage_record.registration_time:
            return self.departure_time - self.triage_record.registration_time
        return None

    def save(self, *args, **kwargs):
        """Override save to calculate stay_duration"""
        # Calculate duration before saving
        if self.departure_time:
            self.stay_duration = self.calculate_stay_duration()
            
        # Save only once
        super().save(*args, **kwargs)

    
    class Meta:
        db_table = 'triage_history_info'
        verbose_name = 'Triage History Info'
        verbose_name_plural = 'Triage History Info'

    def __str__(self):
        return f"History Info for Triage Record {self.triage_record.id}"