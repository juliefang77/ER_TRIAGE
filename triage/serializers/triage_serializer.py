from rest_framework import serializers
from django.contrib.auth import authenticate
from ..models import (
    Patient, 
    TriageRecord, 
    TriageResult, 
    VitalSigns, 
    MedicalStaff, 
    Hospital, 
    HospitalUser, 
    TriageHistoryInfo
)
# Change patient form status to APPROVED upon approval
from patient_portal.models import PatientTriageSubmission

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'

# For other serializers to use to filter for their own patients
class HospitalUserFilterSerializer(serializers.ModelSerializer):
    hospital = HospitalSerializer(read_only=True)  
    
    class Meta:
        model = HospitalUser
        fields = ['id', 'hospital'] 

class MedicalStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalStaff
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class TriageResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TriageResult
        fields = '__all__'

class VitalSignsSerializer(serializers.ModelSerializer):
    injury_position = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True,
        allow_null=True
    )

    class Meta:
        model = VitalSigns
        fields = '__all__'

    def validate_injury_position(self, value):
        valid_choices = [choice[0] for choice in VitalSigns.INJURY_POSITIONS]
        if value:
            for pos in value:
                if pos not in valid_choices:
                    raise serializers.ValidationError(f"Invalid choice: {pos}")
        return value

# Feed into 分诊记录 API
class TriageHistoryInfoSerializer(serializers.ModelSerializer):
    # All fields editable except stay_duration
    assigned_doctor = MedicalStaffSerializer(required=False, allow_null=True)
    assigned_nurse = MedicalStaffSerializer(required=False, allow_null=True)

    class Meta:
        model = TriageHistoryInfo
        fields = '__all__'
        read_only_fields = ('stay_duration',)  # Only this is read-only because it's calculated

# 新建分诊 API serializer 
class TriageRecordSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(required=False, allow_null=True, read_only=True)
    nurse = MedicalStaffSerializer(required=False, allow_null=True, read_only=True)
    result = TriageResultSerializer(required=False, allow_null=True, read_only=True)
    vitalsigns = VitalSignsSerializer(required=False, allow_null=True, read_only=True)
    history_info = TriageHistoryInfoSerializer(required=False, allow_null=True, read_only=True)

    class Meta:
        model = TriageRecord
        fields = '__all__'

# 分诊记录API
class TriageHistorySerializer(serializers.ModelSerializer):
    patient = PatientSerializer(required=False, allow_null=True)
    nurse = MedicalStaffSerializer(required=False, allow_null=True)
    result = TriageResultSerializer(required=False, allow_null=True)
    vitalsigns = VitalSignsSerializer(required=False, allow_null=True)
    history_info = TriageHistoryInfoSerializer(required=False, allow_null=True)

    class Meta:
        model = TriageRecord
        fields = '__all__'

#Authentication Serializers
class HospitalLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                              username=username, password=password)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class HospitalUserSerializer(serializers.ModelSerializer):
    """
    Note: This serializer is for admin management only, 
    not for hospital client authentication
    """
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = HospitalUser
        fields = ('id', 'username', 'password', 'email', 'first_name',
                 'last_name', 'hospital')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Force is_staff to False for all hospital users
        validated_data['is_staff'] = False
        user = HospitalUser.objects.create_user(**validated_data)
        return user

