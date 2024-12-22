from django.contrib import admin
from .models import Patient, TriageRecord, VitalSigns, MedicalStaff

class VitalSignsInline(admin.StackedInline):
    model = VitalSigns
    extra = 1
    fieldsets = [
        ('基础生命体征', {
            'fields': [
                ('temperature', 'heart_rate', 'respiratory_rate'),
                ('systolic_bp', 'diastolic_bp'),
                'oxygen_saturation'
            ]
        }),
        ('评分', {
            'fields': [
                ('avpu_status', 'pain_score'),
                ('mews_score', 'trauma_score'),
            ]
        }),
        ('其他', {
            'fields': ['blood_glucose']
        })
    ]

class PatientAdmin(admin.ModelAdmin):
    list_display = ('name_chinese', 'pinyin_name', 'gender', 'date_of_birth', 'phone')
    search_fields = ['name_chinese', 'id_number', 'phone']
    fieldsets = [
        ('基本信息', {
            'fields': [
                ('name_chinese', 'pinyin_name'),
                ('gender', 'date_of_birth'),
                ('id_type', 'id_number'), 
                'blood_type'
            ]
        }),
        ('联系方式', {
            'fields': [
                'phone',
                'address',
                ('emergency_contact', 'emergency_phone')
            ]
        }),
        ('医疗信息', {
            'fields': ['allergies']
        })
    ]

class MedicalStaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'staff_id', 'role', 'department')
    list_filter = ['role', 'department']
    search_fields = ['name', 'staff_id']

class TriageRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'registration_time', 'priority_level', 'area', 'status', 'department')
    list_filter = ['priority_level', 'area', 'status', 'treatment_area']
    search_fields = ['patient__name_chinese', 'patient__id_number', 'preliminary_diagnosis']
    inlines = [VitalSignsInline]
    fieldsets = [
        ('患者信息', {
            'fields': ['patient']
        }),
        ('分诊信息', {
            'fields': [
                'arrival_time',
                'arrival_method',
                ('priority_level', 'area'),
                'status',
                'nurse'
            ]
        }),
        ('就诊安排', {
            'fields': [
                'treatment_area',
                'department',
                'preliminary_diagnosis'
            ]
        }),
        ('病情描述', {
            'fields': ['chief_complaint', 'medical_history']
        }),
        ('转诊与复诊', {
            'fields': [
                'transfer_status',
                'followup_type',
                'followup_notes'
            ]
        })
    ]

# Register all models with their admin classes
admin.site.register(Patient, PatientAdmin)
admin.site.register(TriageRecord, TriageRecordAdmin)
admin.site.register(MedicalStaff, MedicalStaffAdmin)