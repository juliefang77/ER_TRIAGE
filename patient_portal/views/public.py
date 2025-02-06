from ..models.patient_triage import PatientTriageSubmission
from ..serializers.patient_serializer import (
    PatientTriageSubmissionSerializer,
)
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .auth import PatientTokenAuthentication


# Patient submit the form
class PatientTriageSubmissionViewSet(viewsets.ModelViewSet):
    queryset = PatientTriageSubmission.objects.all()
    serializer_class = PatientTriageSubmissionSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def perform_create(self, serializer):
        # Get the authenticated user if any
        patient_user = None
        if self.request.user.is_authenticated:
            patient_user = self.request.user

        # Save with PENDING status and patient_user if authenticated
        serializer.save(
            status='PENDING',
            patient_user=patient_user
        )

# For authenticated patient submissions
class AuthenticatedPatientTriageSubmissionViewSet(viewsets.ModelViewSet):
    queryset = PatientTriageSubmission.objects.all()
    serializer_class = PatientTriageSubmissionSerializer
    authentication_classes = [PatientTokenAuthentication]

    def get_queryset(self):
        # Only return submissions for the logged-in patient
        return self.queryset.filter(patient_user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(
            status='PENDING',
            patient_user=self.request.user
        )