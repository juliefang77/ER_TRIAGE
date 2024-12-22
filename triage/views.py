from rest_framework import viewsets
from .models import Patient, MedicalStaff, TriageRecord
from .serializers import PatientSerializer, MedicalStaffSerializer, TriageRecordSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class MedicalStaffViewSet(viewsets.ModelViewSet):
    queryset = MedicalStaff.objects.all()
    serializer_class = MedicalStaffSerializer

class TriageRecordViewSet(viewsets.ModelViewSet):
    queryset = TriageRecord.objects.all()
    serializer_class = TriageRecordSerializer