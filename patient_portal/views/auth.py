from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from ..serializers.auth_serializer import (
    PatientLoginSerializer, 
    PatientRegisterSerializer,
    PatientVerifySerializer
)
from ..models import PatientUser
from django.shortcuts import get_object_or_404
from triage.models import Patient
from ..models.patient_token import PatientToken

class PatientAuthToken(ObtainAuthToken):
    serializer_class = PatientLoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Link all matching patients
        has_patient = False
        matching_patients = Patient.objects.filter(patient_phone=user.phone)
        if matching_patients.exists():
            matching_patients.update(patient_user=user)
            has_patient = True
        
        token, created = PatientToken.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'phone': user.phone,
            'has_patient_record': has_patient
        })

class PatientRegisterView(CreateAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = PatientRegisterSerializer

    def perform_create(self, serializer):
        # Get the password from the validated data
        password = serializer.validated_data.get('password')
        # Save without the password first
        patient = serializer.save(password='')
        # Then set the password properly using set_password
        patient.set_password(password)
        patient.save()

class PatientVerifyView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        phone = request.data.get('phone')
        code = request.data.get('code')

        if code != '123456':
            return Response({'error': 'Invalid code'}, status=400)

        try:
            patient = get_object_or_404(PatientUser, phone=phone)
            patient.is_verified = True
            patient.save()
            
            # Use PatientToken instead of Token
            token, _ = PatientToken.objects.get_or_create(user=patient)
            
            return Response({
                'message': 'Registration complete',
                'token': token.key
            })
        except Exception as e:
            print(f"Error: {str(e)}")
            return Response({'error': str(e)}, status=400)