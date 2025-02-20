from triage.models import Patient, TriageRecord, TriageResult, VitalSigns, TriageHistoryInfo, HospitalUser, Hospital
from triage.serializers.triage_serializer import TriageRecordSerializer, PatientSerializer
from rest_framework import viewsets, permissions
from patient_portal.models import PatientTriageSubmission

# Not used
class SaaSPatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

# 新建分诊
class SaaSTriageViewSet(viewsets.ModelViewSet):
    queryset = TriageRecord.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TriageRecordSerializer

    def perform_create(self, serializer):
        user = self.request.user
        hospital = user.hospital  # Get hospital from user
        # print("Received data:", self.request.data)  # Shows raw incoming data

        # Get the original submission pk from the URL or request data
        patient_submission_pk = self.request.data.get('patient_submission_id') 

        # Get all nested data from request.data
        patient_data = self.request.data.get('patient')
        vitalsigns_data = self.request.data.get('vitalsigns')
        result_data = self.request.data.get('result')
        history_info_data = self.request.data.get('history_info')  # Add this line
        
        # Handle patient creation/retrieval first
        patient = None
        if patient_data:
            id_number = patient_data.get('id_number')
            if id_number:
                patient, created = Patient.objects.get_or_create(
                    id_number=id_number,
                    defaults={**patient_data, 'hospital': hospital}  # Use hospital instead of user
                )
                if not created and not patient.hospital:
                    patient.hospital = hospital
                    patient.save()
            else:
                patient = Patient.objects.create(
                    **patient_data,
                    hospital=hospital  # Use hospital instead of user
                )

        # Create the main triage record
        triage_record = serializer.save(
            hospital=hospital,
            patient=patient
        )

        # Create related objects after triage record exists
        if vitalsigns_data:
            VitalSigns.objects.create(
                triage_record=triage_record,
                **vitalsigns_data
            )

        result_data['triage_status'] = 'IN_PROGRESS'  # Force status to IN_PROGRESS 已分诊
        if result_data:
            TriageResult.objects.create(
                triage_record=triage_record,
                **result_data
            )
        
        # Add history info creation
        if history_info_data:
            TriageHistoryInfo.objects.create(
                triage_record=triage_record,
                **history_info_data
            )

        # 已分诊的患者不再出现在待approve的列表里
        if patient_submission_pk:
            PatientTriageSubmission.objects.filter(
                id=patient_submission_pk,
                hospital=hospital
            ).update(status='APPROVED')

    def get_queryset(self):
        return TriageRecord.objects.select_related(
            'patient',
            'result',
            'vitalsigns',
            'history_info'
        ).filter(hospital=self.request.user.hospital)  # Filter by user's hospital

