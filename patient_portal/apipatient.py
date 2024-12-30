# patient_portal/apipatient.py

from rest_framework import views
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import PatientTriageSubmission
from .patient_serializer import PatientTriageSubmissionSerializer
from .patient_serializer import PendingSubmissionMappingSerializer

# This API should be called when nurse opens a pre-filled triage form. Data-mapping is included here
class PendingSubmissionDataViewSet(viewsets.ViewSet):  # Changed to ViewSet
    serializer_class = PendingSubmissionMappingSerializer
    
    def retrieve(self, request, pk=None):
        try:
            submission = PatientTriageSubmission.objects.get(
                id=pk,
                hospital=request.user.hospital
            )
            serializer = self.serializer_class(submission)
            return Response(serializer.data)
        except PatientTriageSubmission.DoesNotExist:
            return Response(
                {"detail": "Submission not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

    def get_queryset(self):
        return PatientTriageSubmission.objects.filter(
            hospital=self.request.user.hospital,
            status='PENDING'
        )

# This is the API for listing all PENDING submissions
class PendingSubmissionViewSet(viewsets.ModelViewSet):  # Changed to ModelViewSet
    serializer_class = PatientTriageSubmissionSerializer
    
    def get_queryset(self):
        return PatientTriageSubmission.objects.filter(
            hospital=self.request.user.hospital,
            status='PENDING'
        )

