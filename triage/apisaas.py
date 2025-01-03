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
    filter_backends = [DjangoFilterBackend]
    filterset_class = TriageRecordFilter

    def perform_create(self, serializer):
        hospital_user = self.request.user
        print("Received data:", self.request.data)  # Raw data
        print("Serializer data:", serializer.validated_data)  # Validated data
        print("User:", hospital_user)  # Check user
        serializer.save(hospital=hospital_user)

    def get_queryset(self):
        return TriageRecord.objects.select_related(
            'patient',
            'nurse',
            'result',
            'vitalsigns',
            'history_info'
        ).all()

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
        queryset = TriageRecord.objects.select_related(
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

