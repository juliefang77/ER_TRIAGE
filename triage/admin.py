from django.contrib import admin
from .models import Patient, TriageRecord, TriageResult, VitalSigns, MedicalStaff

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

class TriageResultInline(admin.StackedInline):
    model = TriageResult
    fieldsets = [
        ('分诊结果', {
            'fields': [
                ('priority_level', 'area'),
                'status',
                'treatment_area',
                'department',
                'preliminary_diagnosis'
            ]
        }),
        ('转诊与复诊', {
            'fields': [
                'transfer_status',
                'followup_type',
                'followup_notes'
            ]
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
    list_display = ('patient', 'registration_time', 'get_priority_level', 'get_area', 'get_status', 'get_department')
    list_filter = ['result__priority_level', 'result__area', 'result__status', 'result__treatment_area']
    search_fields = ['patient__name_chinese', 'patient__id_number', 'result__preliminary_diagnosis']
    inlines = [VitalSignsInline, TriageResultInline]
    
    fieldsets = [
        ('患者信息', {
            'fields': ['patient']
        }),
        ('分诊信息', {
            'fields': [
                'arrival_time',
                'arrival_method',
                'nurse'
            ]
        }),
        ('病情描述', {
            'fields': ['chief_complaint', 'medical_history']
        })
    ]

    def get_priority_level(self, obj):
        return obj.result.priority_level if obj.result else None
    get_priority_level.short_description = '分诊等级'

    def get_area(self, obj):
        return obj.result.area if obj.result else None
    get_area.short_description = '分区'

    def get_status(self, obj):
        return obj.result.status if obj.result else None
    get_status.short_description = '状态'

    def get_department(self, obj):
        return obj.result.department if obj.result else None
    get_department.short_description = '科室'

# Register all models
admin.site.register(Patient, PatientAdmin)
admin.site.register(TriageRecord, TriageRecordAdmin)
admin.site.register(MedicalStaff, MedicalStaffAdmin)
admin.site.register(TriageResult)  # Added this