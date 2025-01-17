from triage.models import Patient, TriageRecord
from triage.serializers.triage_serializer import TriageRecordSerializer, PatientSerializer
from rest_framework import viewsets

class SaaSPatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class SaaSTriageViewSet(viewsets.ModelViewSet):
    queryset = TriageRecord.objects.all()
    serializer_class = TriageRecordSerializer

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