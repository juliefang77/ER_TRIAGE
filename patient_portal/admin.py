# patient_portal/admin.py

from django.contrib import admin
from .models import PatientTriageSubmission

@admin.register(PatientTriageSubmission)
class PatientTriageSubmissionAdmin(admin.ModelAdmin):
    list_display = [
        'name_patient',
        'hospital',
        'status',
        'chief_complaint',
        'date_of_birth',
        'patient_phone'
    ]
    
    list_filter = ['status', 'hospital']
    search_fields = ['name_patient', 'id_number', 'patient_phone']
    
    # Group fields in the detail view
    fieldsets = (
        ('Patient Info', {
            'fields': (
                'name_patient', 'gender', 'date_of_birth', 
                'id_type', 'id_number', 'patient_phone',
                'id_medical_insurance', 'id_hospital_card',
                'insurance_type', 'patient_type'
            )
        }),
        ('Medical Info', {
            'fields': (
                'chief_complaint', 'chief_symptom',
                'pain_score', 'temperature',
                'injury_position', 'injury_type',
                'other_inquiry'
            )
        }),
        ('Status', {
            'fields': ('hospital', 'status')
        })
    )