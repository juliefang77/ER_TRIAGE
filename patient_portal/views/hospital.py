from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import views
from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import PatientTriageSubmission
from ..serializers.patient_serializer import (
    PendingSubmissionListSerializer,  
    PendingSubmissionMappingSerializer
)
from rest_framework.permissions import AllowAny


# This is the API for listing all PENDING submissions
class PendingSubmissionViewSet(viewsets.ReadOnlyModelViewSet):  # Changed to ReadOnlyModelViewSet
    serializer_class = PendingSubmissionListSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PatientTriageSubmission.objects.filter(
            hospital=self.request.user,
            status='PENDING'
        )

# This API should be called when nurse opens a pre-filled triage form. Data-mapping is included here
class PendingSubmissionDataViewSet(viewsets.ViewSet):  # Changed to ViewSet
    serializer_class = PendingSubmissionMappingSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]  # Add this line
    
    def retrieve(self, request, pk=None):
        try:
            submission = PatientTriageSubmission.objects.get(
                id=pk,
                hospital=request.user
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
            hospital=self.request.user,
            status='PENDING'
        )