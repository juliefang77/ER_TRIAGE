from rest_framework import viewsets
from rest_framework.response import Response
from triage.models import Patient
from .patient_serializer import PatientSelfRegistrationSerializer

class PatientSelfRegistrationViewSet(viewsets.ModelViewSet):
    # Tells DRF which serializer to use for converting data between JSON and Python objects
    serializer_class = PatientSelfRegistrationSerializer
    
    # Define which records this ViewSet can access
    def get_queryset(self):
        # If patient is viewing records (GET request)
        if self.request.method == 'GET':
            # Return all triage records for this patient ID
            return Patient.objects.filter(
                id_number=self.request.query_params.get('id_number')
            ).prefetch_related(
                'triage_records',  # Load related triage records efficiently
                'triage_records__result',  # Load triage results
                'triage_records__vital_signs'  # Load vital signs
            )
        # For other methods (POST/create), return empty queryset
        return Patient.objects.none()

    # Handle patient registration (POST request)
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient = serializer.save()
        
        return Response({
            'message': '登记成功',
            'patient_id': patient.id  # Return ID so patient can look up records later
        })