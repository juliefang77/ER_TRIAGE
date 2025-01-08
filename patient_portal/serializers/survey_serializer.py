from rest_framework import serializers
from followup.models import FollowupSurvey, SurveyResponse, SurveyTemplate

class PatientSurveyTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyTemplate
        fields = [
            'id',
            'survey_name',
            'question_1',
            'question_2',
            'question_3',
            'question_4',
            'question_5',
            'question_6',
            'question_7',
            'question_8'
        ]

class PatientSurveySerializer(serializers.ModelSerializer):
    template = PatientSurveyTemplateSerializer(source='template', read_only=True)

    class Meta:
        model = FollowupSurvey
        fields = [
            'id',
            'template',
            'status',
            'created_at',
            'completed_at'
        ]
        read_only_fields = ['status', 'created_at', 'completed_at']

class SurveyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResponse
        fields = [
            'answer_1',
            'answer_2',
            'answer_3',
            'answer_4',
            'answer_5',
            'answer_6',
            'answer_7',
            'answer_8'
        ]