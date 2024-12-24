from django.contrib import admin
from django.utils import timezone  # Add this import
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
    list_display = ('name_chinese', 'gender', 'date_of_birth', 'phone')
    search_fields = ['name_chinese', 'id_number', 'phone']
    fieldsets = [
        ('基本信息', {
            'fields': [
                'name_chinese',
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
    # Remove registration_time from list_display temporarily
    list_display = ('patient', 'get_priority_level', 'get_area', 'get_status', 'get_department')

    # Add date hierarchy for better date navigation
    # date_hierarchy = 'registration_time'
    
     # Enhanced filters
    list_filter = [
        ('registration_time', admin.DateFieldListFilter),  # Uncomment this
        'result__priority_level',
        'result__area',
        'result__status',
        'result__department',
        'result__treatment_area',
        'nurse__department'
    ]

    # Enhanced search
    search_fields = ['patient__name_chinese', 'patient__id_number']  # Enable searching by patient name and ID

    raw_id_fields = ['patient', 'nurse']  # Adds a lookup widget for selecting patients
    
    inlines = [VitalSignsInline, TriageResultInline]
    
    fieldsets = [
        ('患者信息', {
            'fields': ['patient']
        }),
        ('分诊信息', {
            'fields': [
                'registration_time',  # Add this back
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

    # def get_registration_time(self, obj):
        #if obj.registration_time:
            #return timezone.localtime(obj.registration_time).strftime("%Y-%m-%d %H:%M:%S")
        #return None
    #get_registration_time.short_description = '登记时间'

class TriageResultAdmin(admin.ModelAdmin):
    list_display = ['triage_record', 'priority_level', 'area', 'status', 'department']
    list_filter = [
        'priority_level',
        'area',
        'status',
        'department',
        'treatment_area'
    ]
    search_fields = [
        'preliminary_diagnosis',
        'triage_record__patient__name_chinese',
        'department'
    ]
    
    fieldsets = [
        ('分诊结果', {
            'fields': [
                'triage_record',  # Add this field
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

# Register all models
admin.site.register(Patient, PatientAdmin)
admin.site.register(TriageRecord, TriageRecordAdmin)
admin.site.register(MedicalStaff, MedicalStaffAdmin)
admin.site.register(TriageResult, TriageResultAdmin)  # Add TriageResultAdmin here