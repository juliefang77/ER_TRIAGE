from rest_framework import serializers
from patient_portal.models.patient_user import PatientUser

class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientUser
        fields = [
            'id',
            'phone',
            'username',
            'date_of_birth',
            'gender',
            'id_type',
            'id_number',
            'id_medical_insurance',
            'profile_picture',
            'first_name',
            'is_verified'
        ]
        read_only_fields = ['id', 'is_verified']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("旧密码不正确")
        return value
    
class ForgetPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)

    def validate(self, data):
        """
        Verify that phone and first_name match a user
        """
        try:
            user = PatientUser.objects.get(
                phone=data['phone'],
                first_name=data['first_name']
            )
        except PatientUser.DoesNotExist:
            raise serializers.ValidationError("手机号码或姓名不正确")
        
        return data