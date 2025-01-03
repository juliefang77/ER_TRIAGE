# patient_portal/apipatient.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import views
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import PatientTriageSubmission
from .patient_serializer import (
    PatientTriageSubmissionSerializer,
    PendingSubmissionListSerializer,  # Add this import
    PendingSubmissionMappingSerializer
)
from rest_framework.permissions import AllowAny

# Patient submit the form
class PatientTriageSubmissionViewSet(viewsets.ModelViewSet):
    queryset = PatientTriageSubmission.objects.all()
    serializer_class = PatientTriageSubmissionSerializer
    permission_classes = [AllowAny]  # Add this line

    def perform_create(self, serializer):
        # Simply save with PENDING status
        serializer.save(status='PENDING')

# This is the API for listing all PENDING submissions
class PendingSubmissionViewSet(viewsets.ReadOnlyModelViewSet):  # Changed to ReadOnlyModelViewSet
    serializer_class = PendingSubmissionListSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PatientTriageSubmission.objects.filter(
            hospital=self.request.user.hospital,
            status='PENDING'
        )

# This API should be called when nurse opens a pre-filled triage form. Data-mapping is included here
class PendingSubmissionDataViewSet(viewsets.ViewSet):  # Changed to ViewSet
    serializer_class = PendingSubmissionMappingSerializer
    permission_classes = [AllowAny]  # Add this line
    
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





