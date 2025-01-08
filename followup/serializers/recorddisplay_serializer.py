from rest_framework import serializers
from triage.models import TriageRecord
from triage.serializers import PatientSerializer, MedicalStaffSerializer, TriageResultSerializer, HospitalUserFilterSerializer
from followup.models import FollowupRecipient

class FollowupRecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowupRecipient
        fields = '__all__'

class FollowupTriageRecordSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(required=False, allow_null=True)
    nurse = MedicalStaffSerializer(required=False, allow_null=True)
    hospital = HospitalUserFilterSerializer(required=False, allow_null=True)
    recipient = FollowupRecipientSerializer(required=False, allow_null=True)
    result = TriageResultSerializer(required=False, allow_null=True) 

    class Meta:
        model = TriageRecord
        fields = '__all__'