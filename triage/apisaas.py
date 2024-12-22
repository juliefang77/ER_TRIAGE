from rest_framework import viewsets
from .models import Patient, TriageRecord, VitalSigns, MedicalStaff
from .serializers import (
    PatientSerializer, 
    TriageRecordSerializer,
    VitalSignsSerializer,
    MedicalStaffSerializer
)

class SaaSPatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class SaaSTriageViewSet(viewsets.ModelViewSet):
    queryset = TriageRecord.objects.all()
    serializer_class = TriageRecordSerializer

class SaaSVitalSignsViewSet(viewsets.ModelViewSet):
    queryset = VitalSigns.objects.all()
    serializer_class = VitalSignsSerializer

class SaaSMedicalStaffViewSet(viewsets.ModelViewSet):
    queryset = MedicalStaff.objects.all()
    serializer_class = MedicalStaffSerializer