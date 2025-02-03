from ..models.patient_triage import PatientTriageSubmission
from ..serializers.patient_serializer import (
    PatientTriageSubmissionSerializer,
)
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


# Patient submit the form
# Patient submit the form
class PatientTriageSubmissionViewSet(viewsets.ModelViewSet):
    queryset = PatientTriageSubmission.objects.all()
    serializer_class = PatientTriageSubmissionSerializer
    permission_classes = [AllowAny]  # Add this line

    def perform_create(self, serializer):
        # Simply save with PENDING status
        serializer.save(status='PENDING')