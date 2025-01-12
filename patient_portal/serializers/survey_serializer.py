from rest_framework import serializers
from followup.models import FollowupSurvey, SurveyResponse, SurveyTemplate, StandardQuestion

class PatientSurveyTemplateSerializer(serializers.ModelSerializer):
    question_1_details = serializers.SerializerMethodField()
    question_2_details = serializers.SerializerMethodField()
    question_3_details = serializers.SerializerMethodField()
    question_4_details = serializers.SerializerMethodField()
    question_5_details = serializers.SerializerMethodField()
    question_6_details = serializers.SerializerMethodField()
    question_7_details = serializers.SerializerMethodField()
    question_8_details = serializers.SerializerMethodField()

    class Meta:
        model = SurveyTemplate
        fields = [
            'id',
            'survey_name',
            'question_1', 'question_1_details',
            'question_2', 'question_2_details',
            'question_3', 'question_3_details',
            'question_4', 'question_4_details',
            'question_5', 'question_5_details',
            'question_6', 'question_6_details',
            'question_7', 'question_7_details',
            'question_8', 'question_8_details'
        ]

    def get_question_details(self, question):
        if not question:
            return None
        try:
            # If it's already a StandardQuestion object
            if isinstance(question, StandardQuestion):
                question_obj = question
            # If it's an ID
            else:
                question_obj = StandardQuestion.objects.get(id=question)

            return {
                'text': question_obj.question_text,
                'type': question_obj.question_type,
                'category': question_obj.question_category,
                'choices': [
                    question_obj.choice_one,
                    question_obj.choice_two,
                    question_obj.choice_three,
                    question_obj.choice_four,
                    question_obj.choice_five
                ] if question_obj.question_type == 'SINGLE_CHOICE' else None
            }
        except StandardQuestion.DoesNotExist:
            return None

    def get_question_1_details(self, obj):
        return self.get_question_details(obj.question_1)

    def get_question_2_details(self, obj):
        return self.get_question_details(obj.question_2)

    def get_question_3_details(self, obj):
        return self.get_question_details(obj.question_3)

    def get_question_4_details(self, obj):
        return self.get_question_details(obj.question_4)

    def get_question_5_details(self, obj):
        return self.get_question_details(obj.question_5)

    def get_question_6_details(self, obj):
        return self.get_question_details(obj.question_6)

    def get_question_7_details(self, obj):
        return self.get_question_details(obj.question_7)

    def get_question_8_details(self, obj):
        return self.get_question_details(obj.question_8)

class PatientSurveySerializer(serializers.ModelSerializer):
    template = PatientSurveyTemplateSerializer() # remove source = template
    survey_status = serializers.CharField(source='recipient.survey_status', read_only=True)
    
    class Meta:
        model = FollowupSurvey
        fields = [
            'id',
            'template',
            'survey_status',
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