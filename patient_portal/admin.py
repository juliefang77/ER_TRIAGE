# patient_portal/admin.py

from django.contrib import admin
from .models import PatientTriageSubmission, PatientUser, ErCompanion, PatientFeedback

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
                'name_patient','patient_user' , 'gender', 'date_of_birth', 
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

@admin.register(PatientUser)
class PatientUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'first_name', 'patient_phone', 'is_verified', 'is_active', 'date_joined')
    list_filter = ('is_verified', 'is_active')
    search_fields = ('phone', 'patient__name_patient', 'patient__patient_phone')
    ordering = ('-date_joined',)

    def patient_phone(self, obj):
        return obj.patient.patient_phone if obj.patient else '-'
    patient_phone.short_description = '患者电话(matched Patient)'


@admin.register(ErCompanion)
class ErCompanionAdmin(admin.ModelAdmin):
    list_display = (
        'patient_name',
        'patient_phone',
        'last_completed_step',
        'payment_status',
        'created_at'
    )
    
    list_filter = ('payment_status', 'last_completed_step')
    search_fields = ('patient_user__first_name', 'patient_user__phone')
    ordering = ('-created_at',)

    def patient_name(self, obj):
        return obj.patient_user.first_name if obj.patient_user else '-'
    patient_name.short_description = '患者姓名'

    def patient_phone(self, obj):
        return obj.patient_user.phone if obj.patient_user else '-'
    patient_phone.short_description = '患者电话'

@admin.register(PatientFeedback)
class PatientFeedbackAdmin(admin.ModelAdmin):
    list_display = ['get_patient_name', 'contact_phone', 'request_type', 'created_at']
    list_filter = ['request_type', 'created_at']
    search_fields = ['patient_user__first_name', 'contact_phone', 'request_content']

    def get_patient_name(self, obj):
        if obj.patient_user and obj.patient_user.first_name:
            return obj.patient_user.first_name
        return '-'
    get_patient_name.short_description = '患者姓名'
    get_patient_name.admin_order_field = 'patient_user__first_name'