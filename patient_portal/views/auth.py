from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from ..models import PatientUser
from triage.models import Patient

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def register(request):
    """Register new patient with phone and password"""
    phone = request.data.get('phone')
    password = request.data.get('password')
    
    if PatientUser.objects.filter(phone=phone).exists():
        return Response({'error': 'Phone number already registered'}, status=400)
        
    patient_user = PatientUser.objects.create(
        phone=phone,
        password=make_password(password),
        is_verified=False
    )
    
    return Response({
        'message': 'Verification code sent',
        'phone': phone
    })

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def verify_registration(request):
    """Verify phone with SMS code"""
    phone = request.data.get('phone')
    code = request.data.get('code')
    
    if code != '123456':  # Test code
        return Response({'error': 'Invalid code'}, status=400)
        
    try:
        patient_user = PatientUser.objects.get(phone=phone)
        patient_user.is_verified = True
        patient_user.save()
        
        return Response({
            'message': 'Registration complete'
        })
    except PatientUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def login(request):
    phone = request.data.get('phone')
    password = request.data.get('password')
    
    try:
        patient_user = PatientUser.objects.get(phone=phone)
        
        if not patient_user.is_verified:
            return Response({'error': 'Phone number not verified'}, status=400)
            
        if not check_password(password, patient_user.password):
            return Response({'error': 'Invalid password'}, status=400)
            
        # Link all matching patients
        has_patient = False
        matching_patients = Patient.objects.filter(patient_phone=phone)
        if matching_patients.exists():
            matching_patients.update(patient_user=patient_user)
            has_patient = True
            
        return Response({
            'message': 'Login successful',
            'has_patient_record': has_patient
        })
        
    except PatientUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=400)