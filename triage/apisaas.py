from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Patient, TriageRecord, TriageResult, VitalSigns, MedicalStaff
from .serializers import (
    PatientSerializer,
    TriageRecordSerializer,
    TriageResultSerializer,
    VitalSignsSerializer,
    MedicalStaffSerializer,
    TriageHistorySerializer
)
from .filters import TriageRecordFilter

class SaaSPatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class SaaSTriageViewSet(viewsets.ModelViewSet):
    queryset = TriageRecord.objects.all()
    serializer_class = TriageRecordSerializer

class SaaSTriageResultViewSet(viewsets.ModelViewSet):
    queryset = TriageResult.objects.all()
    serializer_class = TriageResultSerializer

class SaaSVitalSignsViewSet(viewsets.ModelViewSet):
    queryset = VitalSigns.objects.all()
    serializer_class = VitalSignsSerializer

class SaaSMedicalStaffViewSet(viewsets.ModelViewSet):
    queryset = MedicalStaff.objects.all()
    serializer_class = MedicalStaffSerializer

# New ViewSet for triage history with filtering
class TriageHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = TriageHistorySerializer
    filterset_class = TriageRecordFilter
    filter_backends = [DjangoFilterBackend]
    
    def get_queryset(self):
        queryset = TriageRecord.objects.all()
        # Include related data to avoid N+1 queries
        queryset = queryset.select_related(
            'patient',
            'nurse',
            'result',
            'vitalsigns'
        )
        return queryset
    