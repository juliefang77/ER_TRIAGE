from rest_framework import viewsets, serializers
from django_filters.rest_framework import DjangoFilterBackend
from .models import Patient, TriageRecord, TriageResult, VitalSigns, MedicalStaff, Hospital, HospitalUser
from .serializers import (
    PatientSerializer,
    TriageRecordSerializer,
    TriageResultSerializer,
    TriageHistorySerializer,
    VitalSignsSerializer,
    MedicalStaffSerializer,
    HospitalUserSerializer,
    HospitalLoginSerializer
)
from .filters import TriageRecordFilter
# Authentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
# Pagination and history
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
# Change patient form status to APPROVED upon approval
from patient_portal.models import PatientTriageSubmission

class SaaSPatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class SaaSTriageViewSet(viewsets.ModelViewSet):
    queryset = TriageRecord.objects.all()
    serializer_class = TriageRecordSerializer
    # Add these lines for filtering
    filter_backends = [DjangoFilterBackend]
    filterset_class = TriageRecordFilter

    def get_queryset(self):
        # Optimize queries with select_related
        return TriageRecord.objects.select_related(
            'patient',
            'nurse',
            'result',
            'vitalsigns',
            'history_info'
        ).all()

    # Keep your existing perform_create method
    def perform_create(self, serializer):
        # Get all data from request
        patient_data = self.request.data.get('patient_data')
        vital_signs_data = self.request.data.get('vital_signs_data')
        triage_result_data = self.request.data.get('triage_result_data')
        submission_id = self.request.data.get('submission_id')  # Add this line
        
        # Try to find existing patient or create new one
        patient, created = Patient.objects.get_or_create(
            id_number=patient_data.get('id_number'),
            defaults={
                'name_chinese': patient_data.get('name_chinese'),
                'id_type': patient_data.get('id_type'),
            }
        )

        # Create triage record and link to patient
        triage_record = serializer.save(patient=patient)
        
        # Create vital signs and link to triage record
        if vital_signs_data:
            VitalSigns.objects.create(
                triage_record=triage_record,
                **vital_signs_data
            )
        
        # Create triage result and link to triage record
        if triage_result_data:
            TriageResult.objects.create(
                triage_record=triage_record,
                **triage_result_data
            )
        
        # Add just this part to update submission status
        if submission_id:
            PatientTriageSubmission.objects.filter(
                id=submission_id,
                hospital=self.request.user.hospital
            ).update(status='APPROVED')

# Custom pagination class
class TriageHistoryPagination(PageNumberPagination):
    page_size = 20  # Number of records per page
    page_size_query_param = 'page_size'
    max_page_size = 100

# Triage history view, ranking from most recent
class TriageHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = TriageHistorySerializer  # Use the history-specific serializer
    pagination_class = TriageHistoryPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter
    ]
    filterset_class = TriageRecordFilter
    ordering = ['-registration_time']  # Default ordering by most recent first
    
    def get_queryset(self):
        return TriageRecord.objects.select_related(
            'patient',
            'nurse',
            'result',
            'vitalsigns',
            'history_info'
        ).all()

class SaaSVitalSignsViewSet(viewsets.ModelViewSet):
    queryset = VitalSigns.objects.all()
    serializer_class = VitalSignsSerializer
    # Remove perform_create method

class SaaSTriageResultViewSet(viewsets.ModelViewSet):
    queryset = TriageResult.objects.all()
    serializer_class = TriageResultSerializer
    # Remove perform_create method

class SaaSMedicalStaffViewSet(viewsets.ModelViewSet):
    queryset = MedicalStaff.objects.all()
    serializer_class = MedicalStaffSerializer

#Authentication for hospitals

class CustomAuthToken(ObtainAuthToken):
    serializer_class = HospitalLoginSerializer  # Specify the serializer class
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'hospital': user.hospital.id if user.hospital else None
        })

