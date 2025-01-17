from rest_framework import serializers
from ..models import StandardQuestion, SurveyTemplate
from rest_framework import serializers
from followup.models import FollowupSurvey, SurveyResponse, SurveyTemplate
from patient_portal.serializers.survey_serializer import PatientSurveyTemplateSerializer

class StandardQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StandardQuestion
        fields = '__all__'

# 为看template 的 API准备 (includes question details)
class SurveyTemplateDetailSerializer(serializers.ModelSerializer):
    # Nested serializer for questions
    questions = serializers.SerializerMethodField()
    created_by = serializers.CharField()  # Changed this line - no need for source or read_only

    class Meta:
        model = SurveyTemplate
        fields = [
            'id',
            'survey_name',
            'questions',
            'created_by',
            'created_at',
            'is_active'
        ]

    def get_questions(self, obj):
        questions = []
        # Collect all non-null questions in order
        for i in range(1, 9):
            question = getattr(obj, f'question_{i}')
            if question:
                questions.append({
                    'position': i,
                    'id': question.id,
                    'question_text': question.question_text,
                    'question_type': question.question_type,
                    'question_category': question.question_category,
                    'choice_one': question.choice_one,
                    'choice_two': question.choice_two,
                    'choice_three': question.choice_three,
                    'choice_four': question.choice_four,
                    'choice_five': question.choice_five,
                })
        return questions

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

# 群发survey
class MassSendSurveySerializer(serializers.Serializer):
    triage_record_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        help_text='List of triage record IDs'
    )
    template_id = serializers.IntegerField(
        required=True,
        help_text='ID of the template to use'
    )

# 查看已发送的 surveys list
class PatientSurveyHistorySerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='recipient.patient.name_patient')
    survey_name = serializers.CharField(source='template.survey_name')
    survey_status = serializers.CharField(source='recipient.survey_status')  # Fix: get from recipient
    
    class Meta:
        model = FollowupSurvey
        fields = [
            'id',
            'patient_name',
            'survey_name',
            'created_at',
            'completed_at',
            'survey_status'
        ]

# 查看某一个已经填写的具体的survey 细节
class ManagementSurveyDetailSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='recipient.patient.name_patient')
    survey_name = serializers.CharField(source='template.survey_name')
    survey_status = serializers.CharField(source='recipient.survey_status')
    survey_response = serializers.SerializerMethodField()
    
    class Meta:
        model = FollowupSurvey
        fields = [
            'id',
            'patient_name',
            'survey_name',
            'created_at',
            'completed_at',
            'survey_status',
            'survey_response'
        ]

    def get_survey_response(self, obj):
        try:
            response = SurveyResponse.objects.get(survey=obj)
            questions = []
            
            # Loop through all 8 questions
            for i in range(1, 9):
                question = getattr(obj.template, f'question_{i}')
                if question:
                    choices = [
                        question.choice_one,
                        question.choice_two,
                        question.choice_three,
                        question.choice_four,
                        question.choice_five
                    ]
                    # Remove None/empty choices
                    choices = [c for c in choices if c]
                    
                    questions.append({
                        'question_number': i,
                        'question': question.question_text,
                        'type': question.question_type,
                        'category': question.question_category,
                        'choices': choices if question.question_type == 'SINGLE_CHOICE' else None,
                        'answer': getattr(response, f'answer_{i}')
                    })
            
            return questions

        except SurveyResponse.DoesNotExist:
            return None

# 人工发送问卷页面，左上角“选择问卷模版” search function
class SurveyTemplateSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyTemplate
        fields = ['id', 'survey_name', 'created_at']