from followup.models import FollowupSurvey, SurveyResponse, FollowupRecipient
from rest_framework import serializers

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

# 这个serializer的内容用于input给百度API
class SurveyLLMAnalysisSerializer(serializers.ModelSerializer):
    patient_info = serializers.SerializerMethodField()
    survey_responses = serializers.SerializerMethodField()

    class Meta:
        model = FollowupSurvey
        fields = ['patient_info', 'survey_responses']

    def get_patient_info(self, obj):
        return {
            'name': obj.recipient.patient.name_patient,
            'age': obj.recipient.patient.age,  # if available
            'chief_complaint': obj.recipient.triage_record.chief.complaint,  # if available
            'specialty_type': obj.recipient.triage_record.specialty_type 
        }

    def get_survey_responses(self, obj):
        try:
            response = SurveyResponse.objects.get(survey=obj)
            qa_pairs = []
            
            # Simplified Q&A pairs
            for i in range(1, 9):
                question = getattr(obj.template, f'question_{i}')
                if question:
                    qa_pairs.append({
                        'question': question.question_text,
                        'answer': getattr(response, f'answer_{i}'),
                        'category': question.question_category
                    })
            
            return qa_pairs

        except SurveyResponse.DoesNotExist:
            return None