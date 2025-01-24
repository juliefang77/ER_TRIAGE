from triage.models import Patient, TriageRecord, TriageResult, VitalSigns
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

        # Get all nested data from request.data
        patient_data = self.request.data.get('patient')
        vitalsigns_data = self.request.data.get('vitalsigns')
        result_data = self.request.data.get('result')
        
        # Handle patient creation/retrieval first
        patient = None
        if patient_data:
            id_number = patient_data.get('id_number')
            if id_number:
                patient, created = Patient.objects.get_or_create(
                    id_number=id_number,
                    defaults={**patient_data, 'hospital': hospital_user}
                )
                if not created and not patient.hospital:
                    patient.hospital = hospital_user
                    patient.save()
            else:
                patient = Patient.objects.create(
                    **patient_data,
                    hospital=hospital_user
                )

        # Create the main triage record
        triage_record = serializer.save(
            hospital=hospital_user,
            patient=patient
        )

        # Create related objects after triage record exists
        if vitalsigns_data:
            VitalSigns.objects.create(
                triage_record=triage_record,
                **vitalsigns_data
            )

        if result_data:
            TriageResult.objects.create(
                triage_record=triage_record,
                **result_data
            )

    def get_queryset(self):
        return TriageRecord.objects.select_related(
            'patient',
            'nurse',
            'result',
            'vitalsigns',
            'history_info'
        ).all()