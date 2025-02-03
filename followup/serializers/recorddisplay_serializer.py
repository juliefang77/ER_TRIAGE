from rest_framework import serializers
from triage.models import TriageRecord, VitalSigns, Patient, TriageResult, Hospital
from triage.serializers.triage_serializer import HospitalUserFilterSerializer
from followup.models import FollowupRecipient

class FollowupRecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowupRecipient
        fields = '__all__'

class InjurySerializer(serializers.ModelSerializer):
    VALID_POSITIONS = ['L', 'B', 'C', 'A', 'H', 'P']

    injury_position = serializers.ListField(
        child=serializers.CharField(max_length=1),
        required=False,
        allow_empty=True,
        allow_null=True
    )

    def to_internal_value(self, data):
        validated_data = super().to_internal_value(data)
        
        if 'injury_position' in validated_data and validated_data['injury_position']:
            validated_data['injury_position'] = ','.join(validated_data['injury_position'])
        
        return validated_data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        
        if instance.injury_position:
            # Clean and process the string
            cleaned = instance.injury_position.replace("'", "").replace("[", "").replace("]", "")
            positions = [pos.strip() for pos in cleaned.split(',') if pos.strip()]
            ret['injury_position'] = positions
                
        return ret

    class Meta:
        model = VitalSigns
        fields = [
            'id',
            'injury_type',
            'injury_position'
        ]

class SimplePatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id_system', 'name_patient', 'patient_phone', 'gender', 'date_of_birth', 'age']  

class SimpleResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TriageResult
        fields = ['id', 'priority_level', 'department']

class SimpleHospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id', 'name']

class FollowupTriageRecordSerializer(serializers.ModelSerializer):
    patient = SimplePatientSerializer(required=False, allow_null=True)
    recipient = FollowupRecipientSerializer(required=False, allow_null=True)
    result = SimpleResultSerializer(required=False, allow_null=True) 
    vitalsigns = InjurySerializer(required=False, allow_null=True)
    hospital = SimpleHospitalSerializer(read_only=True)  

    has_followup = serializers.BooleanField(read_only=True)
    has_note = serializers.BooleanField(read_only=True) 

    class Meta:
        model = TriageRecord
        fields = [
            'id',
            'patient',
            'hospital',
            'recipient',
            'result',
            'vitalsigns',
            'registration_time',  
            'chief_complaint',
            'chief_symptom',
            'specialty_type',
            'has_followup',       # annotated field
            'has_note'       # annotated field
        ]