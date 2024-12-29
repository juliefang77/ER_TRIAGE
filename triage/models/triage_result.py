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
        ('GREEN', '绿区')
    )

    TREATMENT_AREAS = [
        ('RESUS', '抢救区'),
        ('OBS', '留观区'),
        ('TREAT', '诊疗区'),
    ]

    TRANSFER_STATUS_CHOICES = [
        ('NONE', '无需转诊'),
        ('HIGHER', '向上级医院转诊'),
        ('LOWER', '向下级医院转诊')
    ]

    TRIAGE_GROUP_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    ]


    triage_record = models.OneToOneField(
        TriageRecord,
        on_delete=models.PROTECT,
        related_name='result',
        null=True,
        blank=True
    )

    triage_status = models.CharField(
        max_length=15,
        choices=[
            ('WAITING', '未分诊'),
            ('IN_PROGRESS', '已分诊'),
            ('COMPLETED', '已就医'),
            ('LEFT', '离开'),
        ],
        default='WAITING',
        verbose_name='状态',
        null=True,
        blank=True
    )
    
    priority_level = models.IntegerField(
        choices=PRIORITY_LEVELS, 
        default=4,
        verbose_name='分诊等级',
        null=True,
        blank=True
    )

    triage_area = models.CharField(
        max_length=6, 
        choices=AREAS, 
        default='GREEN',
        verbose_name='分区',
        null=True,
        blank=True
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

    #patient_nextstep 患者去向
    #transfer_status 转诊安排
    #transfer_hospital 转诊医院
    #transfer_reason 转诊原因
    #triage_group 组别 
    patient_nextstep = models.TextField(
        verbose_name='患者去向',
        null=True,
        blank=True
    )

    transfer_status = models.CharField(
        max_length=20,
        verbose_name='转诊安排',
        choices=TRANSFER_STATUS_CHOICES,
        null=True,
        blank=True
    )

    transfer_hospital = models.CharField(
        max_length=100,
        verbose_name='转诊医院',
        null=True,
        blank=True
    )

    transfer_reason = models.TextField(
        verbose_name='转诊原因',
        null=True,
        blank=True
    )

    triage_group = models.CharField(
        max_length=1,
        verbose_name='组别',
        choices=TRIAGE_GROUP_CHOICES,
        null=True,
        blank=True
    )


    preliminary_diagnosis = models.TextField(
        verbose_name='初步诊断',
        null=True,
        blank=True
    )


    followup_type = models.CharField(
        max_length=10,
        choices=[
            ('NONE', '无需复诊'),
            ('ONLINE', '线上复诊'),
            ('OFFLINE', '线下复诊'),
        ],
        default='NONE',
        verbose_name='复诊安排',
        null=True,
        blank=True
    )

    followup_info = models.TextField(
        verbose_name='复诊备注', 
        null=True, 
        blank=True
    )

    def __str__(self):
        if self.triage_record:
            return f"Result for {self.triage_record}"
        return "Triage Result"