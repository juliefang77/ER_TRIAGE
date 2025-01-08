# patient_portal/views/patient.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from ..models import PatientUser
from ..patient_serializer import PatientLoginSerializer, VerifyCodeSerializer
import uuid  # Add this import

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])  # Add this to remove all auth checks
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
@authentication_classes([])  # Add this to remove all auth checks
def verify_code(request):
    phone = request.data.get('phone')
    code = request.data.get('code')
    
    if code != '123456':  # Test code
        return Response({'error': 'Invalid code'}, status=400)
        
    # Get or create patient user
    patient, created = PatientUser.objects.get_or_create(phone=phone)
    
    # Generate a simple token string
    token = uuid.uuid4().hex
    
    return Response({
        'token': token,
        'is_new_user': created
    })