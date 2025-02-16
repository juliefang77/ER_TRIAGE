from django.contrib import admin
from django.utils import timezone
from django.contrib.auth.admin import UserAdmin
from .models import Patient, TriageRecord, TriageResult, VitalSigns, MedicalStaff, Hospital, HospitalUser, TriageHistoryInfo, MassInjury, HospitalFeedback

class VitalSignsInline(admin.StackedInline):
    model = VitalSigns
    extra = 1
    fieldsets = [
        ('基础生命体征', {
            'fields': [
                ('temperature', 'heart_rate', 'respiratory_rate'),
                ('systolic_bp', 'diastolic_bp'),
                'oxygen_saturation',
                'blood_potassium'
            ]
        }),
        ('评分', {
            'fields': [
                ('avpu_status', 'pain_score'),
                ('mews_score', 'trauma_score'),
                'gcs_score',
                'rems_score'
            ]
        }),
        ('意识状态', {
            'fields': [
                'conscious_status',
                ('eyeopen_status', 'response_status', 'move_status')
            ]
        }),
        ('创伤信息', {
            'fields': [
                'injury_position',
                'injury_type'
            ]
        }),
        ('其他', {
            'fields': ['blood_glucose']
        })
    ]
    readonly_fields = ['measurement_time']  # Add this if you want to show it as read-only

class TriageResultInline(admin.StackedInline):
    model = TriageResult
    fieldsets = [
        ('分诊结果', {
            'fields': [
                ('priority_level', 'triage_area'),
                'triage_status',
                'treatment_area',
                'department',
                'preliminary_diagnosis'
            ]
        }),
        ('转诊信息', {
            'fields': [
                'patient_nextstep',
                'transfer_status',
                'transfer_hospital',
                'transfer_reason',
                'triage_group'
            ]
        }),
        ('复诊安排', {
            'fields': [
                'followup_type',
                'followup_info'
            ]
        })
    ]

class PatientAdmin(admin.ModelAdmin):
    list_display = ('name_patient', 'pinyin_name', 'gender', 'age', 'patient_phone', 'hospital','patient_user')
    search_fields = ['name_patient', 'pinyin_name', 'id_number', 'patient_phone']
    list_filter = ['gender', 'hospital']
    
    fieldsets = [
        ('基本信息', {
            'fields': [
                ('name_patient', 'pinyin_name'),
                ('gender', 'date_of_birth', 'age'),
                ('nationality', 'ethinicity'),
                'profession'
            ]
        }),
        ('证件信息', {
            'fields': [
                ('id_type', 'id_number'),
                ('id_medical_insurance', 'id_social_insurance', 'id_hospital_card'),
                'insurance_type',
                'patient_type'
            ]
        }),
        ('联系方式', {
            'fields': [
                'patient_phone',
                'patient_address',
                ('emergency_contact', 'emergency_phone', 'emergency_relation')
            ]
        }),
        ('医疗信息', {
            'fields': [
                'blood_type',
                'allergies'
            ]
        }),
        ('系统信息', {
            'fields': [
                'hospital',
                'id_his'
            ]
        })
    ]

class MedicalStaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'staff_id', 'role', 'department', 'hospital')
    list_filter = ['role', 'hospital']
    search_fields = ['name', 'staff_id']
    
    fieldsets = [
        ('基本信息', {
            'fields': [
                'name',
                'staff_id',
                'role',
                'department',
                'hospital'
            ]
        })
    ]

class TriageRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'registration_time', 'get_priority_level', 'get_triage_area', 'nurse', 'hospital')
    list_filter = [
        ('registration_time', admin.DateFieldListFilter),
        'result__priority_level',
        'result__triage_area',
        'hospital'
    ]
    search_fields = ['patient__name_patient', 'patient__id_number', 'chief_complaint']
    raw_id_fields = ['patient']
    inlines = [VitalSignsInline, TriageResultInline]
    
    fieldsets = [
        ('基本信息', {
            'fields': [
                'patient',
                'hospital',
                'nurse'
            ]
        }),
        ('就诊信息', {
            'fields': [
                'registration_time',
                'illness_time',
                'arrival_method',
            ]
        }),
        ('分类信息', {
            'fields': [
                'speed_channel',
                'specialty_type',
                'other_inquiry',
                'surgery_type',
                'ifmass_injury',
                'mass_event'
            ]
        }),
        ('病情描述', {
            'fields': [
                'chief_complaint',
                'chief_symptom',
                'medical_history'
            ]
        })
    ]

    def get_priority_level(self, obj):
        return obj.result.priority_level if obj.result else None
    get_priority_level.short_description = '分诊等级'

    def get_triage_area(self, obj):
        return obj.result.triage_area if obj.result else None
    get_triage_area.short_description = '分区'

class TriageResultAdmin(admin.ModelAdmin):
    list_display = ['triage_record', 'priority_level', 'triage_area', 'triage_status', 'department']
    list_filter = ['priority_level', 'triage_area', 'triage_status']
    search_fields = [
        'preliminary_diagnosis',
        'triage_record__patient__name_patient',
        'department'
    ]
    
    fieldsets = [
        ('分诊结果', {
            'fields': [
                'triage_record',
                ('priority_level', 'triage_area'),
                'triage_status',
                'treatment_area',
                'department',
                'preliminary_diagnosis'
            ]
        }),
        ('转诊信息', {
            'fields': [
                'patient_nextstep',
                'transfer_status',
                'transfer_hospital',
                'transfer_reason',
                'triage_group'
            ]
        }),
        ('复诊安排', {
            'fields': [
                'followup_type',
                'followup_info'
            ]
        })
    ]

class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_number', 'is_active')
    search_fields = ['name', 'address']
    list_filter = ['is_active']
    fieldsets = [
        ('基本信息', {
            'fields': [
                'name',
                'address',
                'contact_number',
                'is_active', 'city', 'district', 'level'
            ]
        })
    ]

class HospitalUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'name', 'first_name', 'last_name', 'hospital', 'is_active')
    list_filter = ('is_active', 'hospital')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('name', 'first_name', 'last_name', 'email')}),
        ('Hospital info', {'fields': ('hospital',)}),
        ('Permissions', {'fields': ('is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'hospital', 'email', 'first_name', 'last_name'),
        }),
    )
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

@admin.register(TriageHistoryInfo)
class TriageHistoryInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_patient_name', 'guahao_status', 'departure_time', 'stay_duration']
    list_filter = ['guahao_status']
    raw_id_fields = ['triage_record']  # Use raw_id_fields for ForeignKey
    
    def get_patient_name(self, obj):
        return obj.triage_record.patient.name_patient if obj.triage_record and obj.triage_record.patient else ''
    get_patient_name.short_description = '患者姓名'

@admin.register(MassInjury)
class MassInjuryAdmin(admin.ModelAdmin):
    list_display = ['mass_name', 'mass_type', 'mass_time', 'mass_number']
    list_filter = ['mass_type']
    search_fields = ['mass_name', 'mass_notes']

@admin.register(HospitalFeedback)
class HospitalFeedbackAdmin(admin.ModelAdmin):
    list_display = ['get_user_name', 'contact', 'request_type', 'created_at']
    list_filter = ['request_type', 'created_at']
    search_fields = ['hospital_user__name', 'contact', 'contact_phone', 'request_content']

    def get_user_name(self, obj):
        if obj.hospital_user:
            return obj.hospital_user.name
        return '-'
    get_user_name.short_description = '医院用户名称'
    get_user_name.admin_order_field = 'hospital_user__name'

# Register all models
admin.site.register(Patient, PatientAdmin)
admin.site.register(TriageRecord, TriageRecordAdmin)
admin.site.register(MedicalStaff, MedicalStaffAdmin)
admin.site.register(TriageResult, TriageResultAdmin)
admin.site.register(Hospital, HospitalAdmin)
admin.site.register(HospitalUser, HospitalUserAdmin)