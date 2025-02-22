from django.contrib import admin
from .models import (
    StandardQuestion,
    SurveyTemplate,
    FollowupRecipient,
    FollowupSurvey,
    SurveyResponse,
    FollowupNotetaking,
    FollowupMessage,
    MessageTemplate,
    SurveyAi,
    BookingOnline
)

@admin.register(StandardQuestion)
class StandardQuestionAdmin(admin.ModelAdmin):
    list_display = [
        'question_text',
        'question_category',
        'question_type',
        'is_active'
    ]
    list_filter = ['question_category', 'question_type', 'is_active']
    search_fields = ['question_text']
    fieldsets = [
        ('基本信息', {
            'fields': ['question_text', 'question_category', 'question_type']
        }),
        ('选项', {
            'fields': [
                'choice_one',
                'choice_two',
                'choice_three',
                'choice_four',
                'choice_five'
            ]
        }),
        ('状态', {
            'fields': ['is_active']
        })
    ]

@admin.register(SurveyTemplate)
class SurveyTemplateAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'survey_name',
        'hospital',
        'created_by',
        'created_at',
        'is_active'
    ]
    list_filter = ['hospital', 'is_active', 'created_at']
    search_fields = ['survey_name']
    fieldsets = [
        ('基本信息', {
            'fields': ['survey_name', 'hospital', 'created_by']
        }),
        ('问题', {
            'fields': [
                'question_1',
                'question_2',
                'question_3',
                'question_4',
                'question_5',
                'question_6',
                'question_7',
                'question_8'
            ]
        }),
        ('状态', {
            'fields': ['is_active']
        })
    ]

@admin.register(FollowupRecipient)
class FollowupRecipientAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'patient_user', 'research_patient', 'survey_status', 'call_status', 'message_reply']
    list_filter = ['research_patient', 'survey_status', 'call_status']
    search_fields = ['phone', 'patient__name_patient']

    def patient_name(self, obj):
        return obj.patient.name_patient if obj.patient else '-'
    patient_name.short_description = '患者姓名'  # Column header in admin

@admin.register(FollowupSurvey)
class FollowupSurveyAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'template', 'completed_at', 'patient_name']
    list_filter = ['hospital', 'completed_at']
    search_fields = ['recipient__patient__name_patient']

    def patient_name(self, obj):
        return obj.recipient.patient.name_patient if obj.recipient and obj.recipient.patient else '-'
    patient_name.short_description = '患者姓名'  # Column header in admin 

@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'survey', 'hospital']
    list_filter = ['hospital']
    fieldsets = [
        ('基本信息', {
            'fields': ['survey', 'hospital']
        }),
        ('回答', {
            'fields': [
                'answer_1',
                'answer_2',
                'answer_3',
                'answer_4',
                'answer_5',
                'answer_6',
                'answer_7',
                'answer_8'
            ]
        })
    ]

    def patient_name(self, obj):
        return obj.survey.recipient.patient.name_patient if obj.survey and obj.survey.recipient and obj.survey.recipient.patient else '-'
    patient_name.short_description = '患者姓名'  # Column header in admin

@admin.register(FollowupNotetaking)
class FollowupNotetakingAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'patient', 'created_by', 'created_at', 'raw_notes', 'processed_notes', 'id']
    list_filter = ['created_at', 'hospital']
    search_fields = ['recipient__patient__name_patient', 'raw_notes']
    
    def patient_name(self, obj):
        return obj.recipient.patient.name_patient if obj.recipient and obj.recipient.patient else '-'
    patient_name.short_description = '患者姓名'  # Column header in admin

@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'template_name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['template_name', 'content']


@admin.register(FollowupMessage)
class FollowupMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'hospital', 'patient_name', 'template', 'sent_at', 'responded_at']
    list_filter = ['hospital', 'sent_at']
    search_fields = ['recipient__patient__name_patient', 'content']

    def patient_name(self, obj):
        return obj.recipient.patient.name_patient if obj.recipient and obj.recipient.patient else '-'
    patient_name.short_description = '患者姓名'  # Column header in admin

@admin.register(SurveyAi)
class SurveyAiAdmin(admin.ModelAdmin):
    list_display = ['analysis_name', 'patient_name', 'hospital', 'created_at', 'analysis_result', 'id']
    list_filter = ['created_at', 'hospital']
    search_fields = ['analysis_name', 'recipients__patient__name_patient']
    
    def patient_name(self, obj):
        # Get all recipient names for this analysis
        names = [r.patient.name_patient for r in obj.recipients.all() if r.patient]
        # Join names with commas, or return '-' if no names
        return ', '.join(names) if names else '-'
    patient_name.short_description = '患者姓名'  # Column header in admin


@admin.register(BookingOnline)
class BookingOnlineAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_patient_name', 'hospital', 'start_time', 'end_time', 'status', "actual_time"]
    search_fields = ['patient_user__first_name', 'hospital__name']  # Update search fields
    list_filter = ['status']

    def get_patient_name(self, obj):
        return obj.patient_user.first_name if obj.patient_user else '-'
    get_patient_name.short_description = '患者姓名'  # Chinese label for the column