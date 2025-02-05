from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from ..models import PatientUser

class PatientLoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        if phone and password:
            try:
                user = PatientUser.objects.get(phone=phone)
                if user.check_password(password):
                    if not user.is_verified:
                        raise serializers.ValidationError('Phone number not verified')
                    attrs['user'] = user
                    return attrs
                else:
                    raise serializers.ValidationError('Invalid password')
            except PatientUser.DoesNotExist:
                raise serializers.ValidationError('User not found')
        else:
            raise serializers.ValidationError('Must include "phone" and "password"')

class PatientRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = PatientUser
        fields = ['phone', 'password']

    def create(self, validated_data):
        # Remove password from validated_data as we'll set it properly in the view
        password = validated_data.pop('password')
        return super().create(validated_data)

class PatientVerifySerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()

    def validate(self, attrs):
        phone = attrs.get('phone')
        code = attrs.get('code')

        if code != '123456':  # Test code
            raise serializers.ValidationError('Invalid code')

        try:
            user = PatientUser.objects.get(phone=phone)
            attrs['user'] = user
            return attrs
        except PatientUser.DoesNotExist:
            raise serializers.ValidationError('User not found')