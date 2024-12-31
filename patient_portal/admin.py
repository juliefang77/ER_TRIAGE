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
        'patient_phone',
        'get_injury_positions'  # Add display method for multiple positions
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
                ('injury_position', 'injury_type'),  # Group these together
                'other_inquiry'
            ),
            'classes': ('wide',)  # Make wider for multiple choice display
        }),
        ('Status', {
            'fields': ('hospital', 'status')
        })
    )

    def get_injury_positions(self, obj):
        """Format multiple injury positions for display in list view"""
        if obj.injury_position:
            if isinstance(obj.injury_position, str):
                positions = obj.injury_position.split(',')
            else:
                positions = obj.injury_position
            return ', '.join(pos for pos in positions)
        return '-'
    get_injury_positions.short_description = '损伤部位'  # Column header in list view