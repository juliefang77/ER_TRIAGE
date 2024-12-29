from django.db import models
from django.db import models
from triage.models import TriageRecord, Patient

'''class FollowupRecord(models.Model):
    triage_record = models.ForeignKey(TriageRecord, on_delete=models.CASCADE, related_name='followups')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='followups')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    STATUS_CHOICES = (
        ('PENDING', '待随访'),
        ('IN_PROGRESS', '已加入随访计划'),
        ('COMPLETED', '已随访'),
    )
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='PENDING')
    
    notes = models.TextField(verbose_name='随访记录', blank=True)
    next_followup_time = models.DateTimeField(null=True, blank=True)

class FollowupNote(models.Model):
    followup_record = models.ForeignKey(FollowupRecord, on_delete=models.CASCADE, related_name='notes')
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(verbose_name='备注')
    staff = models.ForeignKey('triage.MedicalStaff', on_delete=models.SET_NULL, null=True)
'''
