from followup.models import FollowupSurvey, SurveyResponse, FollowupRecipient, SurveyAi
from rest_framework import serializers

# Page AI analyze survey: 用于在ai分析随访问卷page里，需要展示的patient list fields
class SurveyAnalysisListSerializer(serializers.ModelSerializer):
    # Patient fields
    id_system = serializers.CharField(source='patient.id_system')
    name_patient = serializers.CharField(source='patient.name_patient')
    gender = serializers.CharField(source='patient.gender')
    date_of_birth = serializers.DateField(source='patient.date_of_birth')
    age = serializers.IntegerField(source='patient.age')
    patient_phone = serializers.CharField(source='patient.patient_phone')
    
    # TriageRecord fields
    registration_time = serializers.DateTimeField(source='triage_record.registration_time')
    chief_complaint = serializers.CharField(source='triage_record.chief_complaint')
    chief_symptom = serializers.CharField(source='triage_record.chief_symptom')
    specialty_type = serializers.CharField(source='triage_record.specialty_type')
    
    # TriageResult fields
    priority_level = serializers.IntegerField(source='triage_record.result.priority_level')
    department = serializers.CharField(source='triage_record.result.department')
    
    class Meta:
        model = FollowupRecipient
        fields = [
            # Patient fields
            'id_system',
            'name_patient',
            'gender',
            'date_of_birth',
            'age',
            'patient_phone',
            
            # TriageRecord fields
            'registration_time',
            'chief_complaint',
            'chief_symptom',
            'specialty_type',
            
            # TriageResult fields
            'priority_level',
            'department',
            
            # FollowupRecipient fields
            'id',
            'survey_status',
            'call_status'
        ]

# NOT USED NOW
# Page AI analyze survey: 这个serializer的内容用于input给百度API，来做批量分析
class SurveyLLMAnalysisSerializer(serializers.ModelSerializer):
    patient_info = serializers.SerializerMethodField()
    survey_responses = serializers.SerializerMethodField()

    class Meta:
        model = FollowupRecipient
        fields = ['patient_info', 'survey_responses']

    def get_patient_info(self, obj):
        return {
            'name': obj.patient.name_patient,
            'age': obj.patient.age,  # if available
            'chief_complaint': obj.triage_record.chief_complaint,  # if available
            'specialty_type': obj.triage_record.specialty_type 
        }

    def get_survey_responses(self, obj):
        # Get the survey for this recipient
        survey = obj.surveys.first()
        if not survey:
            return None

        try:
            response = SurveyResponse.objects.get(survey=survey)
            qa_pairs = []
            
            # Simplified Q&A pairs
            for i in range(1, 9):
                question = getattr(survey.template, f'question_{i}')
                if question:
                    qa_pairs.append({
                        'question': question.question_text,
                        'answer': getattr(response, f'answer_{i}'),
                        'category': question.question_category
                    })
            
            return qa_pairs

        except SurveyResponse.DoesNotExist:
            return None
    
# 用于save AI 生成的分析结果稿件, 也用于第一页view 所有已生成的 survey analysis 页
class SurveyAiSerializer(serializers.ModelSerializer):
    # recipient_count = serializers.IntegerField(read_only=True)
    # recipients = SurveyAnalysisListSerializer(many=True, read_only=True) # 此serializer就是list用的
    recipient_count = serializers.SerializerMethodField()
    recipients = serializers.PrimaryKeyRelatedField(
        many=True, 
        read_only=True
    )
    
    class Meta:
        model = SurveyAi
        fields = [
            'id',
            'hospital',
            'created_at',
            'analysis_name',
            'analysis_result',
            'recipient_count',
            'recipients'
        ]
        read_only_fields = ['hospital', 'created_at']

    def get_recipient_count(self, obj):
        return obj.recipients.count()



