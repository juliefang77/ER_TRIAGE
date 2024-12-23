from django.db import models
from .triage_record import TriageRecord

class TriageResult(models.Model):
    PRIORITY_LEVELS = (
        (1, '一级'),
        (2, '二级'),
        (3, '三级'),
        (4, '四级')
    )
    
    AREAS = (
        ('RED', '红区'),
        ('YELLOW', '黄区'),
        ('GREEN', '绵区')
    )

    TREATMENT_AREAS = [
        ('RESUS', '抢救区'),
        ('OBS', '留观区'),
        ('TREAT', '诊疗区'),
    ]

    TRANSFER_CHOICES = [
        ('NONE', '无需转诊'),
        ('UP', '向上级医院转诊'),
        ('DOWN', '向下级医院转诊'),
    ]

    triage_record = models.OneToOneField(
        TriageRecord,
        on_delete=models.PROTECT,
        related_name='result'
    )

    status = models.CharField(
        max_length=15,
        choices=[
            ('WAITING', '等候中'),
            ('IN_PROGRESS', '就诊中'),
            ('COMPLETED', '已完成'),
            ('LEFT', '离开'),
        ],
        default='WAITING',
        verbose_name='状态'
    )
    
    priority_level = models.IntegerField(
        choices=PRIORITY_LEVELS, 
        default=4,
        verbose_name='分诊等级'
    )
    area = models.CharField(
        max_length=6, 
        choices=AREAS, 
        default='GREEN',
        verbose_name='分区'
    )
    treatment_area = models.CharField(
        max_length=5,
        choices=TREATMENT_AREAS,
        verbose_name='就诊区域',
        null=True,
        blank=True
    )
    department = models.CharField(
        max_length=50,
        verbose_name='分诊科室',
        null=True,
        blank=True
    )
    preliminary_diagnosis = models.TextField(
        verbose_name='初步诊断',
        null=True,
        blank=True
    )
    transfer_status = models.CharField(
        max_length=4,
        choices=TRANSFER_CHOICES,
        default='NONE',
        verbose_name='转诊安排'
    )
    followup_type = models.CharField(
        max_length=10,
        choices=[
            ('NONE', '无需复诊'),
            ('ONLINE', '线上复诊'),
            ('OFFLINE', '线下复诊'),
        ],
        default='NONE',
        verbose_name='复诊安排'
    )
    followup_notes = models.TextField(verbose_name='复诊备注', null=True, blank=True)

    def __str__(self):
        return f"Result for {self.triage_record}"