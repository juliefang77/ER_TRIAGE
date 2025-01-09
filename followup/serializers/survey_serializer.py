from rest_framework import serializers
from ..models import StandardQuestion, SurveyTemplate
from rest_framework import serializers
from followup.models import FollowupSurvey, SurveyResponse, SurveyTemplate

class StandardQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StandardQuestion
        fields = '__all__'

# 为看template 的 API准备
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

class MassSendSurveySerializer(serializers.Serializer):
    triage_record_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        help_text='List of triage record IDs'
    )
    template_id = serializers.IntegerField(
        required=True,
        help_text='ID of the system template to use'
    )