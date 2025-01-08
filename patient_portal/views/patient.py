# patient_portal/views/patient.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from ..models import PatientUser
from triage.models import Patient
from ..serializers.patient_serializer import PatientLoginSerializer, VerifyCodeSerializer
import uuid  # Add this import

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])  # No auth needed for registration
def request_login(request):
    """Step 1: Patient requests login with phone number"""
    serializer = PatientLoginSerializer(data=request.data)
    if serializer.is_valid():
        phone = serializer.validated_data['phone']
        # TODO: Send real SMS here
        # For now, just use '123456' as test code
        return Response({
            'message': 'Verification code sent',
            'phone': phone
        })
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])  # No auth needed for registration
def verify_code(request):
    """Step 2: Verify SMS code and create/link patient account"""
    phone = request.data.get('phone')
    code = request.data.get('code')
    
    # Verify test code
    if code != '123456':  
        return Response({'error': 'Invalid code'}, status=400)
        
    try:
        # Get or create PatientUser account
        patient_user, created = PatientUser.objects.get_or_create(phone=phone)
        
        # Try to find and link existing Patient record
        existing_patient = Patient.objects.filter(patient_phone=phone).first()
        if existing_patient and not existing_patient.patient_user:
            existing_patient.patient_user = patient_user
            existing_patient.save()

        # Generate token for authentication
        token = uuid.uuid4().hex
        
        return Response({
            'token': token,
            'is_new_user': created,
            'has_patient_record': bool(existing_patient)
        })

    except Exception as e:
        return Response({'error': str(e)}, status=400)