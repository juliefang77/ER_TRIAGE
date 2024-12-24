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

    def perform_create(self, serializer):
        # Get all data from request
        patient_data = self.request.data.get('patient_data')
        vital_signs_data = self.request.data.get('vital_signs_data')
        triage_result_data = self.request.data.get('triage_result_data')
        
        # Try to find existing patient or create new one
        patient, created = Patient.objects.get_or_create(
            id_number=patient_data.get('id_number'),
            defaults={
                'name_chinese': patient_data.get('name_chinese'),
                'id_type': patient_data.get('id_type'),
                # Add other patient fields as needed
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
    