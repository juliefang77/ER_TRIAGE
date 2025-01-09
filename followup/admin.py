from django.contrib import admin
from .models import (
    StandardQuestion,
    SurveyTemplate,
    FollowupRecipient,
    FollowupSurvey,
    SurveyResponse
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
    list_display = ['patient', 'phone', 'research_patient', 'survey_status', 'call_status']
    list_filter = ['research_patient', 'survey_status', 'call_status']
    search_fields = ['phone', 'patient__name_patient']

@admin.register(FollowupSurvey)
class FollowupSurveyAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'template', 'completed_at']
    list_filter = ['hospital', 'completed_at']
    search_fields = ['recipient__patient__name_patient']

@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ['survey', 'hospital']
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
